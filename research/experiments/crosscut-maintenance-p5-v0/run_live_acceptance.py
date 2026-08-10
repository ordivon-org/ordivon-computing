#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
EVIDENCE = ROOT / "evidence"


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def read_json(name: str) -> dict[str, Any]:
    return json.loads((EVIDENCE / name).read_text())


def git_head(repo: str) -> str:
    return subprocess.run(["/usr/bin/git", "-C", repo, "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()


def main() -> int:
    inventory = read_json("pre-contraction-inventory.json")
    contracts = read_json("owner-temporal-contracts.json")
    contraction = read_json("contraction-result.json")
    court = json.loads((ROOT / "feature-court.json").read_text())

    for row in inventory["families"]:
        if (REPO / row["path"]).exists():
            raise RuntimeError(f"archived crosscut family returned to active tree: {row['path']}")
        observed_tree = subprocess.run(["/usr/bin/git", "-C", str(REPO), "rev-parse", f"{inventory['baseRevision']}:{row['path']}"], text=True, capture_output=True, check=True).stdout.strip()
        if observed_tree != row["treeObject"]:
            raise RuntimeError(f"historical recovery tree changed for {row['family']}")

    current = {
        "ordivon-host": git_head("/root/projects/ordivon-host"),
        "workstation": git_head("/root/workstation-lab"),
        "ordivon-world": git_head("/root/projects/ordivon-world"),
        "ordivon-runtime": git_head("/root/projects/ordivon-runtime"),
        "ordivon-computing": git_head("/root/projects/ordivon-computing"),
    }
    bound = {row["owner"]: row["revision"] for row in contracts["owners"]}
    changed = {owner: {"bound": bound[owner], "current": current[owner]} for owner in bound if current[owner] != bound[owner]}
    if changed:
        raise RuntimeError(f"owner evidence binding changed; revalidate before acceptance: {changed}")

    runtime_status = json.loads(subprocess.run(["/usr/local/libexec/ordivon/ordivon-runtime-status", "--health", "--json"], text=True, capture_output=True, check=True).stdout)
    if runtime_status.get("status") != "healthy":
        raise RuntimeError("Runtime is not healthy")
    if (runtime_status.get("deployment") or {}).get("commit") != current["ordivon-runtime"]:
        raise RuntimeError("Runtime source/active identity diverged at P5 acceptance")
    if (runtime_status.get("registry") or {}).get("recoveryRequired") != 0:
        raise RuntimeError("Runtime requires recovery")

    env = dict(os.environ)
    env["PATH"] = "/root/tools/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/wsl/lib:/root/.local/bin"
    lease = json.loads(subprocess.run(["/usr/bin/python3", "/root/workstation-lab/scripts/temporary_equipment.py", "status", "--package", "msitools"], env=env, text=True, capture_output=True, check=True).stdout)
    if lease.get("state") != "absent":
        raise RuntimeError("P5 encountered an active msitools lease")

    verdict_counts: dict[str, int] = {}
    for row in court["rows"]:
        verdict_counts[row["verdict"]] = verdict_counts.get(row["verdict"], 0) + 1
    if verdict_counts.get("inconclusive", 0):
        raise RuntimeError("P5 final court still contains inconclusive features")
    if contraction["activeOldFamilyPathsRemaining"] != 0:
        raise RuntimeError("old family paths remain active")
    if not contraction["genericAdapterDeletionAblation"]["fullComputingGatePassed"]:
        raise RuntimeError("generic adapter deletion did not survive Computing gate")

    result: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-maintenance-p5-acceptance",
        "truthRole": "deterministic-contraction-acceptance",
        "ownerBindings": current,
        "runtime": {
            "status": runtime_status.get("status"),
            "sourceRevision": current["ordivon-runtime"],
            "activeRevision": (runtime_status.get("deployment") or {}).get("commit"),
            "toolCount": (runtime_status.get("deployment") or {}).get("toolCount"),
            "recoveryRequired": (runtime_status.get("registry") or {}).get("recoveryRequired"),
        },
        "msitoolsLeaseState": lease.get("state"),
        "featureCourt": {"rows": len(court["rows"]), "verdictCounts": verdict_counts, "universalTemporalAdapterEarned": contracts["universalAdapterEarned"]},
        "contraction": {
            "removedFamilies": contraction["removed"]["families"],
            "removedFiles": contraction["removed"]["files"],
            "removedBytes": contraction["removed"]["bytes"],
            "removedLines": contraction["removed"]["lines"],
            "gitRecoveryFamiliesVerified": contraction["gitRecovery"]["familiesVerified"],
            "fullComputingGatePassed": contraction["genericAdapterDeletionAblation"]["fullComputingGatePassed"],
            "existenceGauntletPassed": contraction["existenceGauntletAfterRealContraction"]["passed"],
        },
        "promotionDecision": {
            "sharedTemporalSemanticLaw": True,
            "sharedTemporalImplementation": False,
            "centralEventBroker": False,
            "globalFreshnessTtl": False,
            "globalTimeOntology": False,
            "p0ToP4ExecutableApparatusActive": False,
            "ownerNativeContractsPreferred": True,
            "gitHistoryIsArchive": True,
            "coreEditRequired": False,
        },
    }
    result["acceptanceDigest"] = canonical_digest(result)
    output = EVIDENCE / "p5-live-acceptance.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "acceptanceDigest": result["acceptanceDigest"], "verdictCounts": verdict_counts, "runtime": current["ordivon-runtime"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
