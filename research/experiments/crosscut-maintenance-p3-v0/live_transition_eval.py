#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from freshness import freshness_envelope, make_event_hint, make_snapshot


def main() -> int:
    root = Path(__file__).resolve().parent
    evidence = root / "evidence"
    before = json.loads((evidence / "stale-before.json").read_text())
    active = json.loads((evidence / "after-acquire.json").read_text())
    after_release = json.loads((evidence / "after-release.json").read_text())
    events = json.loads((evidence / "owner-events-live.json").read_text())["events"]
    acquire = events[0]
    release = events[1]

    acquire_hint = make_event_hint(event_kind=acquire["eventKind"], occurred_at_ms=acquire["occurredAtMs"], owner=acquire["owner"], receipt_digest=acquire["receiptDigest"])
    release_hint = make_event_hint(event_kind=release["eventKind"], occurred_at_ms=release["occurredAtMs"], owner=release["owner"], receipt_digest=release["receiptDigest"])

    before_snapshot = make_snapshot(
        signal_id=before["signalId"], owner=before["owner"], observed_at_ms=before["observedAtMs"],
        invalidation_keys=["temporary-equipment", "workstation-package-policy"], facts=before["facts"], max_age_ms=60_000,
    )
    active_snapshot = make_snapshot(
        signal_id=active["signalId"], owner=active["owner"], observed_at_ms=active["observedAtMs"],
        invalidation_keys=["temporary-equipment", "workstation-package-policy"], facts=active["facts"], max_age_ms=60_000,
    )
    first = freshness_envelope(before_snapshot, now_ms=acquire["occurredAtMs"] + 1, event_hints=[acquire_hint])
    second = freshness_envelope(active_snapshot, now_ms=release["occurredAtMs"] + 1, event_hints=[release_hint])
    first_deadline = before["observedAtMs"] + 60_000
    second_deadline = active["observedAtMs"] + 60_000
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p3-live-stale-transition-evaluation",
        "beforeAcquire": {
            "snapshotLeaseState": before["facts"]["temporaryEquipment"]["state"],
            "currentLeaseStateAfterEvent": active["facts"]["temporaryEquipment"]["state"],
            "freshness": first["freshness"],
            "legacyActionWithoutInvalidation": "route_owner_review",
            "requiredActionWithInvalidation": "targeted_reobserve",
            "staleWindowPreventedMs": max(0, first_deadline - acquire["occurredAtMs"]),
        },
        "beforeRelease": {
            "snapshotLeaseState": active["facts"]["temporaryEquipment"]["state"],
            "currentLeaseStateAfterEvent": after_release["facts"]["temporaryEquipment"]["state"],
            "freshness": second["freshness"],
            "legacyActionWithoutInvalidation": "no_action",
            "requiredActionWithInvalidation": "targeted_reobserve",
            "staleWindowPreventedMs": max(0, second_deadline - release["occurredAtMs"]),
        },
        "leaseLeftActive": after_release["facts"]["temporaryEquipment"]["active"],
        "centralEventStoreRequired": False,
        "globalFreshnessTtlPromoted": False,
    }
    (evidence / "live-stale-transition-evaluation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
