from __future__ import annotations

from typing import Any

from temporal import assess_temporal_validity, make_event_hint, make_snapshot


def stale_exposure_ms(*, observed_at_ms: int, max_age_ms: int, changed_at_ms: int, hint_available_at_ms: int | None) -> int:
    expiry = observed_at_ms + max_age_ms
    stop = expiry if hint_available_at_ms is None else min(expiry, hint_available_at_ms)
    return max(0, stop - changed_at_ms)


def run_sparse_event_falsifiers() -> dict[str, Any]:
    observed = 1_000
    changed = 12_000
    max_age = 60_000
    snapshot = make_snapshot(
        signal_id="owner-x:dynamic",
        owner="owner-x",
        observed_at_ms=observed,
        ordering_domain="experiment-clock-ms",
        invalidation_keys=["dynamic-state"],
        facts={"state": "A"},
        max_age_ms=max_age,
    )
    immediate = make_event_hint(
        event_kind="owner-x.changed",
        owner="owner-x",
        occurred_at_ms=changed,
        available_at_ms=changed + 1,
        ordering_domain="experiment-clock-ms",
        change_disposition="changed",
        targeted_keys=["dynamic-state"],
        event_identity="event-x",
    )
    delayed = make_event_hint(
        event_kind="owner-x.changed",
        owner="owner-x",
        occurred_at_ms=changed,
        available_at_ms=25_000,
        ordering_domain="experiment-clock-ms",
        change_disposition="changed",
        targeted_keys=["dynamic-state"],
        event_identity="event-x",
    )
    duplicate = dict(delayed)
    duplicate["availableAtMs"] = 26_000
    duplicate["eventHintDigest"] = "transport-replay-ignored-for-semantic-identity"

    before_delayed_arrival = assess_temporal_validity(
        snapshot, now_ms=20_000, event_hints=[delayed]
    )
    after_delayed_arrival = assess_temporal_validity(
        snapshot, now_ms=26_000, event_hints=[delayed, duplicate]
    )
    immediate_result = assess_temporal_validity(
        snapshot, now_ms=13_000, event_hints=[immediate]
    )
    no_hint = assess_temporal_validity(snapshot, now_ms=20_000, event_hints=[])

    newer_snapshot = make_snapshot(
        signal_id="owner-x:dynamic",
        owner="owner-x",
        observed_at_ms=20_000,
        ordering_domain="experiment-clock-ms",
        invalidation_keys=["dynamic-state"],
        facts={"state": "B"},
        max_age_ms=max_age,
    )
    out_of_order = assess_temporal_validity(
        newer_snapshot, now_ms=26_000, event_hints=[delayed]
    )

    unbounded = make_snapshot(
        signal_id="owner-x:unbounded",
        owner="owner-x",
        observed_at_ms=observed,
        ordering_domain="experiment-clock-ms",
        invalidation_keys=["dynamic-state"],
        facts={"state": "A"},
        max_age_ms=None,
    )
    unbounded_result = assess_temporal_validity(
        unbounded, now_ms=20_000, event_hints=[]
    )

    return {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p4-sparse-event-falsifiers",
        "noHint": {
            "state": no_hint["freshnessState"],
            "actionable": no_hint["actionableWithoutReobservation"],
            "absenceProvesNoChange": no_hint["absenceOfVisibleEventProvesNoOwnerChange"],
            "staleExposureMs": stale_exposure_ms(
                observed_at_ms=observed,
                max_age_ms=max_age,
                changed_at_ms=changed,
                hint_available_at_ms=None,
            ),
        },
        "delayedHintBeforeArrival": {
            "state": before_delayed_arrival["freshnessState"],
            "notYetAvailable": before_delayed_arrival["eventTransport"]["notYetAvailable"],
            "staleExposureMs": stale_exposure_ms(
                observed_at_ms=observed,
                max_age_ms=max_age,
                changed_at_ms=changed,
                hint_available_at_ms=25_000,
            ),
        },
        "delayedHintAfterArrival": {
            "state": after_delayed_arrival["freshnessState"],
            "deduplicatedReplays": after_delayed_arrival["eventTransport"]["deduplicatedReplays"],
            "matchedInvalidations": len(after_delayed_arrival["matchedInvalidations"]),
        },
        "immediateHint": {
            "state": immediate_result["freshnessState"],
            "staleExposureMs": stale_exposure_ms(
                observed_at_ms=observed,
                max_age_ms=max_age,
                changed_at_ms=changed,
                hint_available_at_ms=changed + 1,
            ),
        },
        "outOfOrderOldHintAfterNewObservation": {
            "state": out_of_order["freshnessState"],
            "olderThanSnapshot": out_of_order["eventTransport"]["olderThanSnapshot"],
            "matchedInvalidations": len(out_of_order["matchedInvalidations"]),
        },
        "noHintNoOwnerBound": {
            "state": unbounded_result["freshnessState"],
            "actionable": unbounded_result["actionableWithoutReobservation"],
        },
        "conclusion": {
            "eventsEliminateStaleness": False,
            "eventsAccelerateInvalidation": True,
            "ownerFreshnessBoundStillNeededWhenActionableWithoutEvent": True,
            "unboundedWithoutHintIsActionable": False,
        },
    }
