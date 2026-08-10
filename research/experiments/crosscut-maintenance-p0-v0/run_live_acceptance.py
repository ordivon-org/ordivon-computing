from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "packages" / "content-cli" / "src"))
sys.path.insert(0, str(HERE))

from compatibility import summarize
from dirty_aging import classify_dirty_workspaces
from maintenance import build_projection, canonical_digest
from ordivon_content.baseline import build_baseline

RUNTIME_LIFECYCLE = Path("/usr/local/libexec/ordivon/ordivon-runtime-lifecycle")
RUNTIME_CACHE = Path("/usr/local/libexec/ordivon/ordivon-runtime-cache")
RUNTIME_STATUS = Path("/usr/local/libexec/ordivon/ordivon-runtime-status")
WORLD_DOCTOR = Path("/root/projects/ordivon-world/.venv/bin/ordivon-world-doctor")
WORKSTATION_DOCTOR = Path("/root/workstation-lab/scripts/agent_workstation_doctor.py")
DATABASE = Path("/var/lib/ordivon/registry/registry.sqlite3")
STORE = Path("/var/lib/ordivon/runtime")
POLICY = Path("/etc/ordivon/workspace-retention.json")


def run_json(command: list[str]) -> tuple[dict, float]:
    started = time.perf_counter()
    completed = subprocess.run(command, text=True, capture_output=True, check=True)
    return json.loads(completed.stdout), (time.perf_counter() - started) * 1000


def lifecycle(*, measure_bytes: bool) -> tuple[dict, float]:
    command = [str(RUNTIME_LIFECYCLE), "inspect", "--database", str(DATABASE), "--runtime-store-root", str(STORE), "--policy-file", str(POLICY)]
    if measure_bytes:
        command.append("--measure-bytes")
    return run_json(command)


def cache() -> tuple[dict, float]:
    return run_json([str(RUNTIME_CACHE), "inspect", "--database", str(DATABASE), "--runtime-store-root", str(STORE)])


def runtime_status() -> tuple[dict, float]:
    return run_json([str(RUNTIME_STATUS), "--health", "--json"])


def conformance_status() -> dict:
    env = dict(os.environ)
    env["PATH"] = "/root/.local/bin:/usr/local/bin:/usr/bin:/bin"
    completed = subprocess.run([sys.executable, "scripts/ordivon_conformance.py", "gate"], cwd=ROOT, env=env, text=True, capture_output=True, check=False)
    stderr = completed.stderr.strip()
    blocked_by = None
    if completed.returncode != 0:
        if "vale is required" in stderr:
            blocked_by = "vale_missing"
        elif "required" in stderr:
            blocked_by = stderr.splitlines()[-1][:240]
        else:
            blocked_by = "gate_failed"
    return {"passed": completed.returncode == 0, "exitCode": completed.returncode, "blockedBy": blocked_by, "stderrTail": stderr[-1000:]}


def owner_doctors() -> tuple[list[dict], float]:
    started = time.perf_counter()
    world, _ = run_json([str(WORLD_DOCTOR), "--repo", "/root/projects/ordivon-world", "--offline"])
    world_checks = world.get("checks", [])
    summaries = [{
        "owner": "ordivon-world",
        "sourceKind": world.get("kind"),
        "status": world.get("status"),
        "checks": len(world_checks),
        "failedChecks": [item.get("name") for item in world_checks if item.get("status") not in {"ok", "skipped"}],
        "skippedChecks": sum(item.get("status") == "skipped" for item in world_checks),
    }]
    completed = subprocess.run([sys.executable, str(WORKSTATION_DOCTOR), "--pretty"], text=True, capture_output=True, check=False)
    workstation = json.loads(completed.stdout)
    workstation_checks = workstation.get("checks", [])
    summaries.append({
        "owner": "workstation-lab",
        "sourceKind": "agent-workstation-doctor",
        "status": workstation.get("status"),
        "checks": len(workstation_checks),
        "failedChecks": [{"name": item.get("name"), "severity": item.get("severity")} for item in workstation_checks if not item.get("ok")],
        "skippedChecks": 0,
    })
    return summaries, (time.perf_counter() - started) * 1000


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-status", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    host_status = json.loads(args.host_status.read_text(encoding="utf-8"))
    runtime_health, runtime_health_ms = runtime_status()
    fast_runs: list[float] = []
    fast_report: dict | None = None
    for _ in range(3):
        fast_report, elapsed = lifecycle(measure_bytes=False)
        fast_runs.append(elapsed)
    measured_report, measured_ms = lifecycle(measure_bytes=True)
    cache_report, cache_ms = cache()
    content = build_baseline(repository_parent=Path("/root/projects"))
    conformance = conformance_status()
    doctors, owner_doctor_ms = owner_doctors()

    compatibility_entries = [
        {"id": "compat:semantic-core:raw-reducer-source-aliases", "owner": "ordivon-computing", "path": "research/experiments/semantic-core-v0/{kernel.py,journal.py}", "reason": "historical ReferenceKernel/JournalKernel source names were retained only for experiment-local tests", "removalPredicate": "repository-wide search finds no current consumer outside self-maintained compatibility tests and no durable decode requirement", "evidenceRefs": ["repository-wide-grep:ReferenceKernel|JournalKernel", "semantic-core-v0 targeted tests"], "currentConsumers": [], "protectedState": [], "recoveryRequirements": [], "externalContracts": [], "removed": True},
        {"id": "compat:semantic-core:effectspec-journal-decode", "owner": "ordivon-computing", "path": "research/experiments/semantic-core-v0/src/anc_semantic_core/{model.py,journal.py}", "reason": "retained historical Journal payloads use the EffectSpec type name", "removalPredicate": "all retained Journal evidence is migrated or archived with a proven decoder-independent representation", "evidenceRefs": ["semantic-core-v0 journal compatibility tests"], "currentConsumers": [], "protectedState": ["retained schema-v2/v3 Journal histories"], "recoveryRequirements": ["genesis replay of accepted historical evidence"], "externalContracts": []},
    ]
    compatibility_summary = summarize(compatibility_entries)
    now_ms = int(time.time() * 1000)
    dirty = classify_dirty_workspaces(measured_report, now_ms=now_ms)
    assert fast_report is not None
    projection = build_projection(host_status=host_status, runtime_status=runtime_health, runtime_lifecycle=measured_report, runtime_cache=cache_report, content_baseline=content, conformance_status=conformance, owner_doctors=doctors, compatibility_summary=compatibility_summary, dirty_aging_summary={key: value for key, value in dirty.items() if key != "queue"})
    fast_median = statistics.median(fast_runs)
    cadence = {"fastRunsMs": fast_runs, "fastMedianMs": fast_median, "byteMeasuredRunMs": measured_ms, "byteMeasurementSlowdown": measured_ms / fast_median if fast_median else None, "runtimeHealthMs": runtime_health_ms, "cacheInspectMs": cache_ms, "ownerDoctorMs": owner_doctor_ms, "decision": "split_fast_classification_from_byte_measurement" if measured_ms > fast_median * 3 else "no_split_earned", "recommendedFastClassificationCadence": "hourly" if measured_ms > fast_median * 3 else "daily", "recommendedByteMeasurementCadence": "daily", "mutationAuthorized": False}
    evidence = {"schemaVersion": 1, "kind": "ordivon.crosscut-maintenance-p0-acceptance", "capturedAtMs": now_ms, "computingRevision": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(), "hostStatusDigest": canonical_digest(host_status), "runtimeStatusDigest": canonical_digest(runtime_health), "runtimeLifecycleDigest": canonical_digest(measured_report), "runtimeCacheDigest": canonical_digest(cache_report), "contentBaselineDigest": canonical_digest(content), "conformanceStatus": conformance, "ownerDoctors": doctors, "cadenceExperiment": cadence, "compatibility": compatibility_summary, "compatibilityErasure": {"removed": ["ReferenceKernel", "JournalKernel"], "retained": ["EffectSpec historical Journal decode"]}, "dirtyAging": dirty, "maintenanceProjection": projection}
    evidence["acceptanceDigest"] = canonical_digest(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "acceptanceDigest": evidence["acceptanceDigest"], "runtimeStatus": runtime_health.get("status"), "conformance": conformance, "ownerDoctors": doctors, "fastMedianMs": cadence["fastMedianMs"], "byteMeasuredRunMs": cadence["byteMeasuredRunMs"], "decision": cadence["decision"], "dirtyCounts": dirty["counts"], "maintenanceSummary": projection["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
