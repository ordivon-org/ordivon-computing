#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import statistics
import subprocess
import time


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
REPOS = {
    "ordivon-computing": "/root/projects/ordivon-computing",
    "ordivon-runtime": "/root/projects/ordivon-runtime",
    "ordivon-world": "/root/projects/ordivon-world",
    "ordivon-host": "/root/projects/ordivon-host",
}


def observe(repo: str) -> dict[str, str | None]:
    source = subprocess.run(["/usr/bin/git", "-C", repo, "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()
    remote = subprocess.run(["/usr/bin/git", "-C", repo, "ls-remote", "--heads", "origin", "refs/heads/main"], text=True, capture_output=True, check=True, timeout=20)
    published = remote.stdout.split()[0] if remote.stdout.strip() else None
    return {"sourceRevision": source, "publishedRevision": published}


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    samples: dict[str, list[float]] = {}
    final_facts = {}
    for owner, repo in REPOS.items():
        rows = []
        for _ in range(3):
            started = time.perf_counter()
            final_facts[owner] = observe(repo)
            rows.append((time.perf_counter() - started) * 1000)
        samples[owner] = rows
    medians = {owner: statistics.median(values) for owner, values in samples.items()}
    p3_noop_cost = sum(medians.values())
    p4_noop_cost = 0.0
    p3_changed_cost = p3_noop_cost
    p4_changed_cost = medians["ordivon-computing"]
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p4-source-delivery-reobservation-benchmark",
        "samplesMs": samples,
        "p50Ms": medians,
        "finalFacts": final_facts,
        "counterfactualCosts": {
            "p3KeyOnlyNoOpPublishMs": p3_noop_cost,
            "p4OwnerScopedNoChangePublishMs": p4_noop_cost,
            "p3KeyOnlyChangedComputingPublishMs": p3_changed_cost,
            "p4OwnerScopedChangedComputingPublishMs": p4_changed_cost,
            "p4ChangedPublishAvoidedMs": p3_changed_cost - p4_changed_cost,
        },
        "note": "Reobservation latency includes real git ls-remote origin/main network observation. These timings measure current operator cost, not a universal SLA.",
    }
    path = EVIDENCE / "reobservation-benchmark.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"path": str(path), "p50Ms": medians, "p3NoopCostMs": p3_noop_cost, "p4NoopCostMs": p4_noop_cost, "p4ChangedAvoidedMs": p3_changed_cost - p4_changed_cost}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
