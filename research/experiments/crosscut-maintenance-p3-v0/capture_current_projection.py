#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import time

from freshness import make_snapshot
from projection import build_temporal_projection


def git_head(repo: Path) -> str:
    return subprocess.run(["/usr/bin/git", "-C", str(repo), "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()


def remote_head(repo: Path) -> str | None:
    proc = subprocess.run(["/usr/bin/git", "-C", str(repo), "ls-remote", "--heads", "origin", "refs/heads/main"], text=True, capture_output=True, check=False, timeout=20)
    return proc.stdout.split()[0] if proc.returncode == 0 and proc.stdout.strip() else None


def delivery_state(source: str | None, published: str | None, active: str | None, *, deployable: bool) -> str:
    if source is None:
        return "source_unknown"
    if published is None:
        return "publication_unknown"
    if not deployable:
        return "source_published" if source == published else "source_not_published"
    if active is None:
        return "activation_unknown"
    if source == published == active:
        return "converged"
    if source == active and source != published:
        return "active_source_not_published"
    if source == published and source != active:
        return "published_source_not_active"
    if published == active and source != active:
        return "source_ahead_of_published_active_identity"
    return "three_way_divergence"


def main() -> int:
    root = Path(__file__).resolve().parent
    evidence = root / "evidence"
    now = int(time.time() * 1000)
    runtime_repo = Path("/root/projects/ordivon-runtime")
    computing_repo = Path("/root/projects/ordivon-computing")
    world_repo = Path("/root/projects/ordivon-world")
    workstation = Path("/root/workstation-lab")

    runtime_status = json.loads(subprocess.run(["/usr/local/libexec/ordivon/ordivon-runtime-status", "--health", "--json"], text=True, capture_output=True, check=True).stdout)
    runtime_source = git_head(runtime_repo)
    runtime_published = remote_head(runtime_repo)
    runtime_active = (runtime_status.get("deployment") or {}).get("commit")
    runtime_delivery = {
        "sourceRevision": runtime_source,
        "publishedRevision": runtime_published,
        "activeRevision": runtime_active,
        "semanticState": delivery_state(runtime_source, runtime_published, runtime_active, deployable=True),
        "healthy": runtime_status.get("status") == "healthy",
    }

    computing_source = git_head(computing_repo)
    computing_published = remote_head(computing_repo)
    computing_delivery = {
        "sourceRevision": computing_source,
        "publishedRevision": computing_published,
        "semanticState": delivery_state(computing_source, computing_published, None, deployable=False),
    }
    world_source = git_head(world_repo)
    world_published = remote_head(world_repo)
    world_delivery = {
        "sourceRevision": world_source,
        "publishedRevision": world_published,
        "semanticState": delivery_state(world_source, world_published, None, deployable=False),
    }

    env = dict(os.environ)
    env["PATH"] = "/root/tools/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/wsl/lib:/root/.local/bin"
    lease = json.loads(subprocess.run(["/usr/bin/python3", str(workstation / "scripts" / "temporary_equipment.py"), "status", "--package", "msitools"], env=env, text=True, capture_output=True, check=True).stdout)
    doctor = json.loads(subprocess.run(["/usr/bin/python3", str(workstation / "scripts" / "agent_workstation_doctor.py"), "--pretty"], env=env, text=True, capture_output=True, check=True).stdout)
    package_finding = next(item for item in doctor["checks"] if item["name"] == "package-forbidden:msitools")

    build_evidence = json.loads((root.parent / "crosscut-maintenance-p2-v0" / "evidence" / "stable-presentation-build.json").read_text())
    build_revision = str(build_evidence["runtimeRevision"])

    snapshots = [
        make_snapshot(signal_id="runtime:source-delivery", owner="ordivon-runtime", observed_at_ms=now, invalidation_keys=["source-delivery", "runtime-health"], facts=runtime_delivery, max_age_ms=30_000),
        make_snapshot(signal_id="computing:source-delivery", owner="ordivon-computing", observed_at_ms=now, invalidation_keys=["source-delivery"], facts=computing_delivery, max_age_ms=60_000),
        make_snapshot(signal_id="world:source-delivery", owner="ordivon-world", observed_at_ms=now, invalidation_keys=["source-delivery"], facts=world_delivery, max_age_ms=60_000),
        make_snapshot(signal_id="workstation:package-policy:msitools", owner="workstation", observed_at_ms=now, invalidation_keys=["temporary-equipment", "workstation-package-policy"], facts={"temporaryEquipment": lease, "packageFinding": package_finding}, max_age_ms=60_000),
        make_snapshot(signal_id="runtime:stable-build-evidence", owner="ordivon-runtime", observed_at_ms=now, invalidation_keys=[], facts={"decision": build_evidence.get("decision"), "binaryDigestsEqual": build_evidence.get("binaryDigestsEqual"), "privateBackingIsolationPreserved": build_evidence.get("privateBackingIsolationPreserved")}, max_age_ms=None, temporal_class="immutable_evidence", binding_identity={"runtimeRevision": build_revision}),
    ]
    projection = build_temporal_projection(
        snapshots=snapshots,
        event_hints=[],
        now_ms=now,
        current_bindings={"runtime:stable-build-evidence": {"runtimeRevision": runtime_source}},
    )
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p3-current-temporal-projection",
        "capturedAtMs": now,
        "ownerFacts": {
            "runtimeDelivery": runtime_delivery,
            "computingDelivery": computing_delivery,
            "worldDelivery": world_delivery,
            "workstationDoctorSummary": doctor.get("summary"),
            "msitoolsLease": lease,
            "runtimeBuildEvidenceRevision": build_revision,
        },
        "projection": projection,
    }
    (evidence / "current-temporal-projection.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"capturedAtMs": now, "runtimeDelivery": runtime_delivery["semanticState"], "computingDelivery": computing_delivery["semanticState"], "worldDelivery": world_delivery["semanticState"], "msitoolsLease": lease.get("state"), "buildEvidenceFreshness": next(item for item in projection["signals"] if item["signalId"] == "runtime:stable-build-evidence")["freshness"]["freshnessState"], "summary": projection["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
