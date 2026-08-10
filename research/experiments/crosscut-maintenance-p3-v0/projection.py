from __future__ import annotations

from typing import Any

from freshness import canonical_digest, freshness_envelope


def build_temporal_projection(
    *,
    snapshots: list[dict[str, Any]],
    event_hints: list[dict[str, Any]],
    now_ms: int,
    current_bindings: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    bindings = current_bindings or {}
    signals = []
    for snapshot in snapshots:
        signal_id = str(snapshot["signalId"])
        envelope = freshness_envelope(
            snapshot,
            now_ms=now_ms,
            event_hints=event_hints,
            current_binding_identity=bindings.get(signal_id),
        )
        signals.append(
            {
                "signalId": signal_id,
                "owner": snapshot.get("owner"),
                "facts": snapshot.get("facts"),
                "freshness": envelope["freshness"],
                "snapshotDigest": snapshot.get("snapshotDigest"),
                "actionableWithoutReobservation": envelope["freshness"]["actionableWithoutReobservation"],
            }
        )
    actionable = [item["signalId"] for item in signals if item["actionableWithoutReobservation"]]
    reobserve = [item["signalId"] for item in signals if not item["actionableWithoutReobservation"]]
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-temporal-maintenance-projection",
        "truthRole": "rebuildable-read-only-projection",
        "signals": signals,
        "eventHints": [
            {
                "eventKind": item.get("eventKind"),
                "occurredAtMs": item.get("occurredAtMs"),
                "targetedKeys": item.get("targetedKeys"),
                "eventHintDigest": item.get("eventHintDigest"),
                "receiptDigest": item.get("receiptDigest"),
            }
            for item in event_hints
        ],
        "summary": {
            "signals": len(signals),
            "actionableSignals": actionable,
            "reobserveSignals": reobserve,
            "fresh": sum(item["freshness"]["freshnessState"] == "fresh" for item in signals),
            "invalidated": sum(item["freshness"]["freshnessState"] == "invalidated" for item in signals),
            "stale": sum(item["freshness"]["freshnessState"] == "stale" for item in signals),
            "unbounded": sum(item["freshness"]["freshnessState"] == "freshness_unbounded" for item in signals),
            "immutableBound": sum(item["freshness"]["freshnessState"] == "immutable_bound" for item in signals),
            "bindingChanged": sum(item["freshness"]["freshnessState"] == "binding_changed" for item in signals),
        },
        "truthBoundary": {
            "projectionAuthoritative": False,
            "ownerNativeFactsRemainAuthoritative": True,
            "eventHintsInvalidateButDoNotReplaceTruth": True,
            "reobservationRequiredBeforeSubstantiveActionOnInvalidFact": True,
            "ownerFreshnessBoundsRemainOwnerLocal": True,
            "immutableEvidenceUsesIdentityApplicabilityNotAge": True,
            "centralEventStoreRequired": False,
            "centralEffectAuthorized": False,
        },
    }
    result["projectionDigest"] = canonical_digest(result)
    return result
