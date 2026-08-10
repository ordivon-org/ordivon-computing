#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

from sparse_events import run_sparse_event_falsifiers
from temporal import assess_temporal_validity, make_event_hint


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
HOST_CLOCK = "ordivon-host-wall-clock-ms"
NOOP_PUSH_JOB = "job-019feba8-0bde-7a71-b326-8740a69dd682"
NOOP_PUSH_FINISHED_AT_MS = 1786365089976
NOOP_PUSH_STDERR_DIGEST = "sha256:47e930bfa8547af0e275fdc8f30ee4b5eded740e9615307434258197298b0ea5"


def load_p3_module():
    path = ROOT.parent / "crosscut-maintenance-p3-v0" / "freshness.py"
    spec = importlib.util.spec_from_file_location("p3_freshness_for_ablation", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P3 freshness module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def p3_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-signal-snapshot",
        "truthRole": "rebuildable-read-only-projection",
        "signalId": snapshot["signalId"],
        "owner": snapshot["owner"],
        "observedAtMs": snapshot["observedAtMs"],
        "temporalClass": snapshot["temporalClass"],
        "bindingIdentity": snapshot.get("bindingIdentity"),
        "maxAgeMs": snapshot.get("maxAgeMs"),
        "invalidationKeys": snapshot["invalidationKeys"],
        "facts": snapshot["facts"],
        "sourceDigest": None,
        "snapshotDigest": snapshot["snapshotDigest"],
    }


def evaluate_event(snapshot_rows: list[dict[str, Any]], *, p4_event: dict[str, Any], p3_event: dict[str, Any], now_ms: int) -> dict[str, Any]:
    p3 = load_p3_module()
    p3_rows = []
    p4_rows = []
    for snapshot in snapshot_rows:
        p3_result = p3.assess_freshness(p3_snapshot(snapshot), now_ms=now_ms, event_hints=[p3_event])
        p4_result = assess_temporal_validity(snapshot, now_ms=now_ms, event_hints=[p4_event])
        p3_rows.append({"signalId": snapshot["signalId"], "owner": snapshot["owner"], "state": p3_result["freshnessState"], "reobserve": p3_result["reobserveRequired"]})
        p4_rows.append({"signalId": snapshot["signalId"], "owner": snapshot["owner"], "state": p4_result["freshnessState"], "reobserve": p4_result["reobserveRequired"], "transport": p4_result["eventTransport"]})
    return {"p3": p3_rows, "p4": p4_rows}


def count_reobserve(rows: list[dict[str, Any]]) -> int:
    return sum(bool(row["reobserve"]) for row in rows)


def main() -> int:
    capture = json.loads((EVIDENCE / "live-owner-capture-before-noop-publish.json").read_text())
    snapshots = capture["snapshots"]
    no_change_event = make_event_hint(event_kind="git.publish.result", owner="ordivon-computing", occurred_at_ms=NOOP_PUSH_FINISHED_AT_MS, available_at_ms=NOOP_PUSH_FINISHED_AT_MS, ordering_domain=HOST_CLOCK, change_disposition="no_change", evidence_digest=NOOP_PUSH_STDERR_DIGEST, event_identity=NOOP_PUSH_JOB)
    p3_noop_event = {"eventKind": "git.publish.result", "occurredAtMs": NOOP_PUSH_FINISHED_AT_MS, "owner": "ordivon-computing", "targetedKeys": ["source-delivery"], "receiptDigest": NOOP_PUSH_STDERR_DIGEST}
    noop = evaluate_event(snapshots, p4_event=no_change_event, p3_event=p3_noop_event, now_ms=NOOP_PUSH_FINISHED_AT_MS)

    changed_event = make_event_hint(event_kind="git.publish.result", owner="ordivon-computing", occurred_at_ms=NOOP_PUSH_FINISHED_AT_MS, available_at_ms=NOOP_PUSH_FINISHED_AT_MS, ordering_domain=HOST_CLOCK, change_disposition="changed", evidence_digest=NOOP_PUSH_STDERR_DIGEST, event_identity="counterfactual:changed-computing-publish")
    p3_changed_event = dict(p3_noop_event)
    changed = evaluate_event(snapshots, p4_event=changed_event, p3_event=p3_changed_event, now_ms=NOOP_PUSH_FINISHED_AT_MS)

    source_signal_ids = [row["signalId"] for row in snapshots if "source-delivery" in row["invalidationKeys"]]
    computing_signal = "ordivon-computing:source-delivery"
    noop_p3 = count_reobserve(noop["p3"])
    noop_p4 = count_reobserve(noop["p4"])
    changed_p3 = count_reobserve(changed["p3"])
    changed_p4 = count_reobserve(changed["p4"])
    expected_changed = 1
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p4-live-event-ablation",
        "liveSnapshotCapturedAtMs": capture["capturedAtMs"],
        "workloadSignals": len(snapshots),
        "sourceDeliverySignals": source_signal_ids,
        "realNoOpPublish": {
            "jobId": NOOP_PUSH_JOB,
            "finishedAtMs": NOOP_PUSH_FINISHED_AT_MS,
            "stderrDigest": NOOP_PUSH_STDERR_DIGEST,
            "stderrSemantic": "Everything up-to-date",
            "ownerStateChanged": False,
            "p3ReobserveSignals": [row["signalId"] for row in noop["p3"] if row["reobserve"]],
            "p4ReobserveSignals": [row["signalId"] for row in noop["p4"] if row["reobserve"]],
            "p3UnnecessaryReobservations": noop_p3,
            "p4UnnecessaryReobservations": noop_p4,
            "p3WorkloadFalsePositiveRate": noop_p3 / len(snapshots),
            "p4WorkloadFalsePositiveRate": noop_p4 / len(snapshots),
        },
        "ownerScopeCounterfactualChangedPublish": {
            "purpose": "Hold event kind/key/time constant while changing only the owner-reported change disposition to isolate owner scope.",
            "expectedReobserveSignals": [computing_signal],
            "p3ReobserveSignals": [row["signalId"] for row in changed["p3"] if row["reobserve"]],
            "p4ReobserveSignals": [row["signalId"] for row in changed["p4"] if row["reobserve"]],
            "p3FalsePositiveReobservations": max(0, changed_p3 - expected_changed),
            "p4FalsePositiveReobservations": max(0, changed_p4 - expected_changed),
            "p3FalsePositiveShareOfInvalidations": max(0, changed_p3 - expected_changed) / changed_p3 if changed_p3 else 0.0,
            "p4FalsePositiveShareOfInvalidations": max(0, changed_p4 - expected_changed) / changed_p4 if changed_p4 else 0.0,
        },
        "runtimeRelease": capture["runtimeRelease"],
        "stableBuildEvidence": capture["stableBuildEvidence"],
        "sparseEvents": run_sparse_event_falsifiers(),
        "decisions": {
            "invalidationIdentity": "owner+key",
            "eventOccurrenceEqualsAvailability": False,
            "noChangeEventInvalidates": False,
            "eventReplayCreatesNewInvalidation": False,
            "absenceOfEventProvesFreshness": False,
            "centralEventBrokerEarned": False,
        },
    }
    path = EVIDENCE / "live-event-ablation.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"path": str(path), "noopP3FalsePositives": noop_p3, "noopP4FalsePositives": noop_p4, "changedP3FalsePositives": result["ownerScopeCounterfactualChangedPublish"]["p3FalsePositiveReobservations"], "changedP4FalsePositives": result["ownerScopeCounterfactualChangedPublish"]["p4FalsePositiveReobservations"], "stableBuildEvidence": capture["stableBuildEvidence"]["validity"]["freshnessState"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
