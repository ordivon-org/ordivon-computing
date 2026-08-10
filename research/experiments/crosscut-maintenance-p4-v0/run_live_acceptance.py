#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def read_json(name: str) -> dict[str, Any]:
    value = json.loads((EVIDENCE / name).read_text())
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} must be an object")
    return value


def git_head(repo: str) -> str:
    return subprocess.run(["/usr/bin/git", "-C", repo, "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    live = read_json("live-event-ablation.json")
    world = read_json("world-temporal-consumer.json")
    benchmark = read_json("reobservation-benchmark.json")
    capture = read_json("live-owner-capture-before-noop-publish.json")

    noop = live["realNoOpPublish"]
    if noop["ownerStateChanged"] is not False:
        raise RuntimeError("no-op publish evidence claims an owner change")
    if noop["p3UnnecessaryReobservations"] != 4 or noop["p4UnnecessaryReobservations"] != 0:
        raise RuntimeError("live no-op invalidation ablation did not reproduce 4 -> 0")

    changed = live["ownerScopeCounterfactualChangedPublish"]
    if changed["p3FalsePositiveReobservations"] != 3 or changed["p4FalsePositiveReobservations"] != 0:
        raise RuntimeError("owner-scope ablation did not reproduce 3 -> 0 cross-owner false positives")

    sparse = live["sparseEvents"]
    if sparse["noHint"]["staleExposureMs"] <= sparse["delayedHintBeforeArrival"]["staleExposureMs"]:
        raise RuntimeError("delayed hint did not reduce stale exposure relative to no hint")
    if sparse["delayedHintBeforeArrival"]["staleExposureMs"] <= sparse["immediateHint"]["staleExposureMs"]:
        raise RuntimeError("immediate hint did not reduce stale exposure relative to delayed hint")
    if sparse["delayedHintAfterArrival"]["deduplicatedReplays"] != 1:
        raise RuntimeError("exact event replay was not deduplicated")
    if sparse["outOfOrderOldHintAfterNewObservation"]["matchedInvalidations"] != 0:
        raise RuntimeError("out-of-order old event invalidated a newer observation")
    if sparse["noHintNoOwnerBound"]["actionable"] is not False:
        raise RuntimeError("unbounded no-event state became actionable")

    build = live["stableBuildEvidence"]
    if build["validity"]["freshnessState"] != "binding_changed":
        raise RuntimeError("P2 stable-build evidence did not become binding_changed on current Runtime")
    release = live["runtimeRelease"]
    if release["historicalP3SnapshotValidityAtRelease"]["freshnessState"] != "invalidated":
        raise RuntimeError("real Runtime release did not invalidate historical Runtime delivery")
    if release["historicalP3SnapshotAlreadyPastAgeBoundAtRelease"] is not True:
        raise RuntimeError("P4 expected the old Runtime snapshot to have already expired by age")

    if world["focusedOwnerNativeTest"]["passed"] != 22 or world["focusedOwnerNativeTest"]["failed"] != 0:
        raise RuntimeError("World temporal second-consumer tests did not pass")
    if world["implementationDifference"]["exactSharedCodeContractEarned"] is not False:
        raise RuntimeError("P4 incorrectly promoted a shared temporal package")
    if world["implementationDifference"]["sharedSemanticInvariantSupported"] is not True:
        raise RuntimeError("World did not independently support the temporal laws")
    current_world_revision = git_head("/root/projects/ordivon-world")
    if current_world_revision != world["worldRevision"]:
        raise RuntimeError("World second-consumer evidence binding changed; revalidate current World")

    costs = benchmark["counterfactualCosts"]
    if costs["p3KeyOnlyNoOpPublishMs"] <= 0 or costs["p4OwnerScopedNoChangePublishMs"] != 0.0:
        raise RuntimeError("reobservation benchmark did not preserve no-op cost reduction")
    if costs["p4ChangedPublishAvoidedMs"] <= 0:
        raise RuntimeError("owner-scoped changed publish did not avoid cross-owner reobservation cost")

    runtime_status = json.loads(subprocess.run(["/usr/local/libexec/ordivon/ordivon-runtime-status", "--health", "--json"], text=True, capture_output=True, check=True).stdout)
    runtime_source = git_head("/root/projects/ordivon-runtime")
    runtime_active = (runtime_status.get("deployment") or {}).get("commit")
    if runtime_status.get("status") != "healthy" or runtime_source != runtime_active:
        raise RuntimeError("current Runtime source/active production is not converged and healthy")

    env = dict(os.environ)
    env["PATH"] = "/root/tools/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/wsl/lib:/root/.local/bin"
    lease = json.loads(subprocess.run(["/usr/bin/python3", "/root/workstation-lab/scripts/temporary_equipment.py", "status", "--package", "msitools"], env=env, text=True, capture_output=True, check=True).stdout)
    if lease.get("state") != "absent":
        raise RuntimeError("P4 left or encountered an active msitools lease")

    result: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-maintenance-p4-acceptance",
        "truthRole": "rebuildable-read-only-acceptance",
        "realNoOpPublish": {
            "p3UnnecessaryReobservations": noop["p3UnnecessaryReobservations"],
            "p4UnnecessaryReobservations": noop["p4UnnecessaryReobservations"],
            "p3WorkloadFalsePositiveRate": noop["p3WorkloadFalsePositiveRate"],
            "p4WorkloadFalsePositiveRate": noop["p4WorkloadFalsePositiveRate"],
        },
        "ownerScope": {
            "p3FalsePositiveReobservations": changed["p3FalsePositiveReobservations"],
            "p4FalsePositiveReobservations": changed["p4FalsePositiveReobservations"],
            "p3FalsePositiveShareOfInvalidations": changed["p3FalsePositiveShareOfInvalidations"],
            "p4FalsePositiveShareOfInvalidations": changed["p4FalsePositiveShareOfInvalidations"],
        },
        "sparseEvents": sparse,
        "reobservationBenchmark": benchmark,
        "runtime": {
            "sourceRevision": runtime_source,
            "activeRevision": runtime_active,
            "publishedRevisionAtInitialCapture": capture["ownerFacts"]["ordivon-runtime"]["publishedRevision"],
            "stableBuildEvidenceState": build["validity"]["freshnessState"],
            "releaseCommit": release["commit"],
            "releaseResultDigest": release["resultFileDigest"],
        },
        "worldSecondConsumer": {
            "revision": world["worldRevision"],
            "currentRevision": current_world_revision,
            "focusedTestsPassed": world["focusedOwnerNativeTest"]["passed"],
            "sharedSemanticInvariantSupported": world["implementationDifference"]["sharedSemanticInvariantSupported"],
            "exactSharedCodeContractEarned": world["implementationDifference"]["exactSharedCodeContractEarned"],
        },
        "msitoolsLeaseState": lease.get("state"),
        "promotionDecision": {
            "sharedTemporalSemanticLaw": True,
            "sharedTemporalPackage": False,
            "centralEventBroker": False,
            "globalFreshnessTtl": False,
            "invalidationIdentity": "owner+key",
            "eventOccurrenceAndAvailabilitySeparated": True,
            "eventsAreAccelerationNotCompleteness": True,
            "noChangeResultInvalidates": False,
            "exactReplayCreatesNewInvalidation": False,
            "crossClockOrderingAssumed": False,
        },
    }
    result["acceptanceDigest"] = canonical_digest(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "acceptanceDigest": result["acceptanceDigest"], "runtime": runtime_source, "p3NoopCostMs": costs["p3KeyOnlyNoOpPublishMs"], "p4ChangedAvoidedMs": costs["p4ChangedPublishAvoidedMs"], "worldTests": 22, "leaseState": lease.get("state")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
