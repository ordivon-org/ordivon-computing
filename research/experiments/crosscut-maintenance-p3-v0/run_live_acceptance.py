#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise RuntimeError(f"{path} must contain an object")
    return value


def git_head(repo: Path) -> str:
    return subprocess.run(["/usr/bin/git", "-C", str(repo), "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workstation-root", type=Path, default=Path("/root/workstation-lab"))
    parser.add_argument("--runtime-repo", type=Path, default=Path("/root/projects/ordivon-runtime"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    evidence = root / "evidence"
    live_transition = read_json(evidence / "live-stale-transition-evaluation.json")
    agent_eval = read_json(evidence / "holdout-agent-evaluation.json")
    legacy_eval = read_json(evidence / "holdout-legacy-evaluation.json")
    ambiguity = read_json(evidence / "temporary-equipment-domain-ambiguity.json")
    current_projection = read_json(evidence / "current-temporal-projection.json")
    build_evidence = read_json(root.parent / "crosscut-maintenance-p2-v0" / "evidence" / "stable-presentation-build.json")

    if agent_eval.get("passRate") != 1.0 or agent_eval.get("passed") != 32:
        raise RuntimeError("P3 Agent adversarial holdout did not pass 32/32")
    agent_metrics = agent_eval.get("metrics") or {}
    for metric in ["wrongOwnerRate", "staleTrustRate", "unnecessaryReobserveRate", "directCrosscutEffectRate", "overActionRate", "underActionRate"]:
        if float(agent_metrics.get(metric, 1.0)) != 0.0:
            raise RuntimeError(f"Agent metric {metric} is not zero")
    legacy_metrics = legacy_eval.get("metrics") or {}
    if float(legacy_eval.get("passRate", 1.0)) >= float(agent_eval["passRate"]):
        raise RuntimeError("freshness ablation did not improve over legacy projection")
    if float(legacy_metrics.get("staleTrustRate", 0.0)) != 1.0:
        raise RuntimeError("legacy ablation did not reproduce stale-trust failure")
    if float(legacy_metrics.get("overActionRate", 0.0)) <= 0.0:
        raise RuntimeError("legacy ablation did not reproduce over-action")

    for name in ["beforeAcquire", "beforeRelease"]:
        transition = live_transition[name]
        freshness = transition["freshness"]
        if freshness.get("freshnessState") != "invalidated" or freshness.get("reobserveRequired") is not True:
            raise RuntimeError(f"{name} did not invalidate stale owner state")
        if int(transition.get("staleWindowPreventedMs", 0)) <= 0:
            raise RuntimeError(f"{name} did not prevent a stale decision window")
    if live_transition.get("leaseLeftActive") is not False:
        raise RuntimeError("P3 stale transition experiment left a lease active")
    if live_transition.get("centralEventStoreRequired") is not False or live_transition.get("globalFreshnessTtlPromoted") is not False:
        raise RuntimeError("P3 accidentally promoted central temporal authority")

    inference = ambiguity.get("inferenceBoundary") or {}
    if inference.get("explicitOwnerNeedProved") is not False:
        raise RuntimeError("temporary-equipment ambiguity evidence incorrectly claims explicit owner need")
    if inference.get("automaticLeaseAcquisitionAllowed") is not False or inference.get("automaticPackageRemovalAllowed") is not False:
        raise RuntimeError("temporary-equipment ambiguity incorrectly authorizes an effect")

    env = dict(os.environ)
    env["PATH"] = "/root/tools/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/wsl/lib:/root/.local/bin"
    lease_proc = subprocess.run(
        ["/usr/bin/python3", str(args.workstation_root / "scripts" / "temporary_equipment.py"), "status", "--package", "msitools"],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    lease_now = json.loads(lease_proc.stdout)
    if lease_now.get("state") != "absent":
        raise RuntimeError("P3 final acceptance found an active msitools lease")

    runtime_source = git_head(args.runtime_repo)
    build_revision = str(build_evidence["runtimeRevision"])
    current_build_applicability = "immutable_bound" if runtime_source == build_revision else "binding_changed"

    current_truth_boundary = current_projection["projection"]["truthBoundary"]
    required_false = {
        "projectionAuthoritative": False,
        "centralEventStoreRequired": False,
        "centralEffectAuthorized": False,
    }
    for key, expected in required_false.items():
        if current_truth_boundary.get(key) is not expected:
            raise RuntimeError(f"temporal projection boundary changed: {key}")
    if current_truth_boundary.get("eventHintsInvalidateButDoNotReplaceTruth") is not True:
        raise RuntimeError("owner events must remain invalidation hints, not replacement truth")
    if current_truth_boundary.get("immutableEvidenceUsesIdentityApplicabilityNotAge") is not True:
        raise RuntimeError("immutable evidence temporal semantics regressed")

    result: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-maintenance-p3-acceptance",
        "truthRole": "rebuildable-read-only-acceptance",
        "agentHoldout": {"passed": agent_eval["passed"], "total": agent_eval["total"], "passRate": agent_eval["passRate"], "metrics": agent_metrics},
        "legacyAblation": {"passed": legacy_eval["passed"], "total": legacy_eval["total"], "passRate": legacy_eval["passRate"], "metrics": legacy_metrics},
        "liveStaleTransitions": {
            "beforeAcquireStaleWindowPreventedMs": live_transition["beforeAcquire"]["staleWindowPreventedMs"],
            "beforeReleaseStaleWindowPreventedMs": live_transition["beforeRelease"]["staleWindowPreventedMs"],
            "leaseLeftActive": live_transition["leaseLeftActive"],
        },
        "temporaryEquipmentAmbiguity": inference,
        "currentOwnerTruth": {
            "msitoolsLeaseState": lease_now.get("state"),
            "runtimeSourceRevision": runtime_source,
            "buildEvidenceRevision": build_revision,
            "buildEvidenceApplicability": current_build_applicability,
        },
        "decisions": {
            "ownerEventsAreInvalidationHintsOnly": True,
            "centralEventStore": False,
            "globalFreshnessTtl": False,
            "maintenanceDaemon": False,
            "crosscutEffectAuthority": False,
            "topicSimilarityCanAuthorizeTemporaryEquipment": False,
            "immutableEvidenceAgesOutByWallClock": False,
        },
    }
    result["acceptanceDigest"] = canonical_digest(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "acceptanceDigest": result["acceptanceDigest"], "agentPassRate": result["agentHoldout"]["passRate"], "legacyPassRate": result["legacyAblation"]["passRate"], "legacyStaleTrustRate": result["legacyAblation"]["metrics"]["staleTrustRate"], "buildEvidenceApplicability": current_build_applicability, "leaseState": lease_now.get("state")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
