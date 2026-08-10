from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from conflicts import summarize_findings
from promotion import assess_shared_lifecycle_promotion

HERE = Path(__file__).resolve().parent

HUMAN_PATH = "/root/tools/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/wsl/lib:/root/.local/bin"


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def run_json(command: list[str], *, env: dict[str, str] | None = None) -> dict[str, Any]:
    completed = subprocess.run(command, text=True, capture_output=True, check=True, env=env)
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise ValueError(f"command did not emit an object: {command[0]}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workstation-root", type=Path, default=Path("/root/workstation-lab"))
    parser.add_argument("--world-root", type=Path, default=Path("/root/projects/ordivon-world"))
    parser.add_argument("--conformance-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    evidence_root = HERE / "evidence"
    sccache = read_json(evidence_root / "sccache-benchmark.json")
    cadence = read_json(evidence_root / "cadence-fast-scan.json")
    dirty_review = read_json(evidence_root / "dirty-review-live.json")
    provider = read_json(evidence_root / "workstation-ruff-provider.json")
    observer_context = read_json(evidence_root / "observer-context.json")
    conformance = read_json(args.conformance_receipt)
    if conformance.get("status") != "passed":
        raise RuntimeError("Computing conformance receipt is not passed")

    environment = dict(os.environ)
    environment["PATH"] = HUMAN_PATH
    workstation = run_json(
        [sys.executable, str(args.workstation_root / "scripts" / "agent_workstation_doctor.py"), "--pretty"],
        env=environment,
    )
    world_doctor = args.world_root / ".venv" / "bin" / "ordivon-world-doctor"
    world = run_json([str(world_doctor), "--repo", str(args.world_root), "--offline"])

    workstation_findings = [item for item in workstation.get("checks", []) if not item.get("ok")]
    conflicts = summarize_findings(
        workstation_findings,
        observer_path=HUMAN_PATH,
        canonical_human_path=HUMAN_PATH,
    )
    conflicts["resolvedEvidence"] = [
        {"classification": "observer_context_mismatch", "evidence": observer_context},
        {"classification": "provider_placement_drift", "evidence": provider},
    ]

    ruff_owner = subprocess.run(
        ["/usr/bin/pacman", "-Qo", "/usr/bin/ruff"], text=True, capture_output=True, check=True
    ).stdout.strip()
    provider_live = {
        "systemRuff": "/usr/bin/ruff",
        "systemRuffOwner": ruff_owner,
        "userLocalRuffPresent": (Path("/root/.local/bin/ruff").exists() or Path("/root/.local/bin/ruff").is_symlink()),
    }
    if provider_live["userLocalRuffPresent"]:
        raise RuntimeError("user-local Ruff returned after provider convergence")

    promotion = assess_shared_lifecycle_promotion(
        [
            {
                "owner": "ordivon-computing",
                "materiallyDifferent": True,
                "requiresExactSharedVocabulary": True,
                "deletionFailure": "Maintenance Projection loses its stable lifecycle classification",
            },
            {
                "owner": "ordivon-runtime",
                "materiallyDifferent": True,
                "requiresExactSharedVocabulary": False,
                "deletionFailure": "Runtime retains owner-native retention/reclaim classification",
            },
            {
                "owner": "ordivon-world",
                "materiallyDifferent": True,
                "requiresExactSharedVocabulary": False,
                "deletionFailure": "World retains owner-native provider and retention/GC semantics",
            },
        ]
    )

    result: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-maintenance-p1-acceptance",
        "truthRole": "rebuildable-read-only-acceptance",
        "sccache": sccache,
        "runtimeCadence": cadence,
        "dirtyReview": dirty_review,
        "computingConformance": {
            "status": conformance.get("status"),
            "repositoryRevision": conformance.get("repositoryRevision"),
            "protocolVersion": conformance.get("protocolVersion"),
            "elapsedMs": conformance.get("elapsedMs"),
            "integrity": conformance.get("integrity"),
        },
        "workstationDoctor": {
            "status": workstation.get("status"),
            "summary": workstation.get("summary"),
        },
        "worldDoctor": {
            "status": world.get("status"),
            "checks": len(world.get("checks", [])),
            "skipped": sum(item.get("status") == "skipped" for item in world.get("checks", [])),
        },
        "crossOwnerConflicts": conflicts,
        "ruffProvider": provider_live,
        "promotion": promotion,
        "decisions": {
            "defaultSccacheForRuntime": False,
            "sharedMutableCargoTarget": False,
            "automaticDirtyDeletion": False,
            "newHourlyLifecycleTimer": False,
            "centralCrossOwnerPolicy": False,
            "sharedLifecycleProductionPackage": promotion["productionSharedPackageEarned"],
            "newCrosscutRepository": False,
        },
    }
    result["acceptanceDigest"] = canonical_digest(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "acceptanceDigest": result["acceptanceDigest"],
                "conformance": result["computingConformance"]["status"],
                "workstationDoctor": result["workstationDoctor"],
                "worldDoctor": result["worldDoctor"],
                "conflictCounts": conflicts["counts"],
                "promotion": promotion["decision"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
