#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from typing import Any

from temporal import assess_temporal_validity, make_event_hint, make_snapshot


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
HOST_CLOCK = "ordivon-host-wall-clock-ms"


def git_head(repo: Path) -> str:
    return subprocess.run(["/usr/bin/git", "-C", str(repo), "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()


def remote_head(repo: Path) -> str | None:
    proc = subprocess.run(["/usr/bin/git", "-C", str(repo), "ls-remote", "--heads", "origin", "refs/heads/main"], text=True, capture_output=True, check=False, timeout=20)
    return proc.stdout.split()[0] if proc.returncode == 0 and proc.stdout.strip() else None


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def delivery(source: str, published: str | None, active: str | None = None) -> dict[str, Any]:
    if published is None:
        state = "publication_unknown"
    elif active is None:
        state = "source_published" if source == published else "source_not_published"
    elif source == published == active:
        state = "converged"
    elif source == active and source != published:
        state = "active_source_not_published"
    elif source == published and source != active:
        state = "published_source_not_active"
    elif published == active and source != active:
        state = "source_ahead_of_published_active_identity"
    else:
        state = "three_way_divergence"
    return {"sourceRevision": source, "publishedRevision": published, "activeRevision": active, "semanticState": state}


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    now = int(time.time() * 1000)
    repos = {
        "ordivon-computing": Path("/root/projects/ordivon-computing"),
        "ordivon-runtime": Path("/root/projects/ordivon-runtime"),
        "ordivon-world": Path("/root/projects/ordivon-world"),
        "ordivon-host": Path("/root/projects/ordivon-host"),
    }
    runtime_status = json.loads(subprocess.run(["/usr/local/libexec/ordivon/ordivon-runtime-status", "--health", "--json"], text=True, capture_output=True, check=True).stdout)
    runtime_active = (runtime_status.get("deployment") or {}).get("commit")
    facts: dict[str, Any] = {}
    snapshots = []
    for owner, repo in repos.items():
        source = git_head(repo)
        published = remote_head(repo)
        active = runtime_active if owner == "ordivon-runtime" else None
        value = delivery(source, published, active)
        facts[owner] = value
        snapshots.append(make_snapshot(signal_id=f"{owner}:source-delivery", owner=owner, observed_at_ms=now, ordering_domain=HOST_CLOCK, invalidation_keys=["source-delivery"], facts=value, max_age_ms=30_000 if owner == "ordivon-runtime" else 60_000))

    runtime_health = {
        "status": runtime_status.get("status"),
        "deployedCommit": runtime_active,
        "toolCount": (runtime_status.get("deployment") or {}).get("toolCount"),
        "restarts": (runtime_status.get("service") or {}).get("restarts"),
        "recoveryRequired": (runtime_status.get("registry") or {}).get("recoveryRequired"),
    }
    snapshots.append(make_snapshot(signal_id="ordivon-runtime:runtime-health", owner="ordivon-runtime", observed_at_ms=now, ordering_domain=HOST_CLOCK, invalidation_keys=["runtime-health"], facts=runtime_health, max_age_ms=30_000))

    env = dict(os.environ)
    env["PATH"] = "/root/tools/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/wsl/lib:/root/.local/bin"
    lease = json.loads(subprocess.run(["/usr/bin/python3", "/root/workstation-lab/scripts/temporary_equipment.py", "status", "--package", "msitools"], env=env, text=True, capture_output=True, check=True).stdout)
    snapshots.append(make_snapshot(signal_id="workstation:package-policy:msitools", owner="workstation", observed_at_ms=now, ordering_domain=HOST_CLOCK, invalidation_keys=["temporary-equipment", "workstation-package-policy"], facts=lease, max_age_ms=60_000))

    p3 = json.loads((ROOT.parent / "crosscut-maintenance-p3-v0" / "evidence" / "current-temporal-projection.json").read_text())
    p3_build = next(item for item in p3["projection"]["signals"] if item["signalId"] == "runtime:stable-build-evidence")
    build_binding = p3_build["freshness"]["bindingIdentity"]
    build_snapshot = make_snapshot(signal_id="ordivon-runtime:stable-build-evidence", owner="ordivon-runtime", observed_at_ms=int(p3_build["freshness"]["observedAtMs"]), ordering_domain=HOST_CLOCK, invalidation_keys=[], facts=p3_build["facts"], max_age_ms=None, temporal_class="immutable_evidence", binding_identity=build_binding)
    current_runtime_binding = {"runtimeRevision": git_head(repos["ordivon-runtime"])}
    build_validity = assess_temporal_validity(build_snapshot, now_ms=now, event_hints=[], current_binding_identity=current_runtime_binding)

    release_dir = Path("/var/lib/ordivon/deployments/effect-d300288213fd0b6bde70a17588dea94f2cdbc2ba07a29367eabfee0d3ea1e2e5")
    release_result = json.loads((release_dir / "result.json").read_text())
    release_event = make_event_hint(event_kind="runtime.release.result", owner="ordivon-runtime", occurred_at_ms=int(release_result["finishedAtMs"]), available_at_ms=int(release_result["finishedAtMs"]), ordering_domain=HOST_CLOCK, change_disposition="changed", receipt_digest=file_digest(release_dir / "result.json"), event_identity=str(release_result["releaseEffect"]["effectId"]))
    p3_runtime = next(item for item in p3["projection"]["signals"] if item["signalId"] == "runtime:source-delivery")
    historical_runtime_snapshot = make_snapshot(signal_id="ordivon-runtime:p3-source-delivery", owner="ordivon-runtime", observed_at_ms=int(p3_runtime["freshness"]["observedAtMs"]), ordering_domain=HOST_CLOCK, invalidation_keys=["source-delivery"], facts=p3_runtime["facts"], max_age_ms=int(p3_runtime["freshness"]["maxAgeMs"]))
    release_invalidation = assess_temporal_validity(historical_runtime_snapshot, now_ms=int(release_result["finishedAtMs"]), event_hints=[release_event])

    document = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p4-live-owner-capture",
        "capturedAtMs": now,
        "orderingDomain": HOST_CLOCK,
        "ownerFacts": facts,
        "runtimeHealth": runtime_health,
        "msitoolsLease": lease,
        "snapshots": snapshots,
        "runtimeRelease": {
            "event": release_event,
            "resultFileDigest": file_digest(release_dir / "result.json"),
            "previousCommit": json.loads((release_dir / "manifest.json").read_text()).get("previousCommit"),
            "commit": release_result.get("commit"),
            "historicalP3SnapshotValidityAtRelease": release_invalidation,
            "historicalP3SnapshotAlreadyPastAgeBoundAtRelease": int(release_result["finishedAtMs"]) > int(p3_runtime["freshness"]["observedAtMs"]) + int(p3_runtime["freshness"]["maxAgeMs"]),
        },
        "stableBuildEvidence": {
            "boundIdentity": build_binding,
            "currentIdentity": current_runtime_binding,
            "validity": build_validity,
        },
    }
    path = EVIDENCE / "live-owner-capture-before-noop-publish.json"
    path.write_text(json.dumps(document, indent=2) + "\n")
    print(json.dumps({"path": str(path), "capturedAtMs": now, "runtimeState": facts["ordivon-runtime"]["semanticState"], "computingState": facts["ordivon-computing"]["semanticState"], "stableBuildEvidence": build_validity["freshnessState"], "runtimeReleaseInvalidation": release_invalidation["freshnessState"], "releaseSnapshotAlreadyExpiredByAge": document["runtimeRelease"]["historicalP3SnapshotAlreadyPastAgeBoundAtRelease"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
