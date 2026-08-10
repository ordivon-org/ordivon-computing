from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def event_targets(event_kind: str) -> tuple[str, ...]:
    mapping = {
        "runtime.release.result": ("source-delivery", "runtime-health"),
        "git.publish.result": ("source-delivery",),
        "workstation.temporary-equipment.acquire": ("temporary-equipment", "workstation-package-policy"),
        "workstation.temporary-equipment.release": ("temporary-equipment", "workstation-package-policy"),
        "runtime.workspace.closed": ("workspace-lifecycle",),
        "runtime.workspace.dirty-review": ("workspace-lifecycle", "dirty-aging"),
    }
    return mapping.get(event_kind, ())


def make_event_hint(
    *,
    event_kind: str,
    occurred_at_ms: int,
    owner: str,
    receipt_digest: str | None = None,
) -> dict[str, Any]:
    result = {
        "eventKind": event_kind,
        "occurredAtMs": int(occurred_at_ms),
        "owner": owner,
        "targetedKeys": list(event_targets(event_kind)),
        "receiptDigest": receipt_digest,
    }
    result["eventHintDigest"] = canonical_digest(result)
    return result


def make_snapshot(
    *,
    signal_id: str,
    owner: str,
    observed_at_ms: int,
    invalidation_keys: list[str],
    facts: dict[str, Any],
    max_age_ms: int | None,
    source_digest: str | None = None,
    temporal_class: str = "dynamic",
    binding_identity: dict[str, str] | None = None,
) -> dict[str, Any]:
    if temporal_class not in {"dynamic", "immutable_evidence"}:
        raise ValueError("temporal_class must be dynamic or immutable_evidence")
    if max_age_ms is not None and max_age_ms <= 0:
        raise ValueError("max_age_ms must be positive when provided")
    if temporal_class == "immutable_evidence" and binding_identity is None:
        raise ValueError("immutable_evidence requires binding_identity")
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-signal-snapshot",
        "truthRole": "rebuildable-read-only-projection",
        "signalId": signal_id,
        "owner": owner,
        "observedAtMs": int(observed_at_ms),
        "temporalClass": temporal_class,
        "bindingIdentity": binding_identity,
        "maxAgeMs": max_age_ms,
        "invalidationKeys": sorted(set(invalidation_keys)),
        "facts": facts,
        "sourceDigest": source_digest,
    }
    result["snapshotDigest"] = canonical_digest(result)
    return result


def assess_freshness(
    snapshot: dict[str, Any],
    *,
    now_ms: int,
    event_hints: list[dict[str, Any]],
    current_binding_identity: dict[str, str] | None = None,
) -> dict[str, Any]:
    observed_at = int(snapshot["observedAtMs"])
    age_ms = max(0, int(now_ms) - observed_at)
    temporal_class = snapshot.get("temporalClass", "dynamic")
    bound_identity = snapshot.get("bindingIdentity")
    keys = set(snapshot.get("invalidationKeys") or [])
    matching = []
    for event in event_hints:
        if int(event.get("occurredAtMs", 0)) <= observed_at:
            continue
        targeted = set(event.get("targetedKeys") or [])
        if keys & targeted:
            matching.append(
                {
                    "eventKind": event.get("eventKind"),
                    "occurredAtMs": event.get("occurredAtMs"),
                    "eventHintDigest": event.get("eventHintDigest"),
                    "receiptDigest": event.get("receiptDigest"),
                    "matchedKeys": sorted(keys & targeted),
                }
            )
    max_age = snapshot.get("maxAgeMs")
    if temporal_class == "immutable_evidence":
        if current_binding_identity is not None and current_binding_identity != bound_identity:
            state = "binding_changed"
            reason = "current_identity_differs_from_evidence_binding"
        else:
            state = "immutable_bound"
            reason = "digest_or_revision_bound_evidence_does_not_age"
    elif matching:
        state = "invalidated"
        reason = "owner_event_after_observation"
    elif max_age is None:
        state = "freshness_unbounded"
        reason = "no_owner_freshness_bound"
    elif age_ms > int(max_age):
        state = "stale"
        reason = "age_exceeded_owner_bound"
    else:
        state = "fresh"
        reason = "within_owner_bound_and_not_invalidated"
    actionable = state in {"fresh", "immutable_bound"}
    return {
        "signalId": snapshot.get("signalId"),
        "owner": snapshot.get("owner"),
        "snapshotDigest": snapshot.get("snapshotDigest"),
        "freshnessState": state,
        "reason": reason,
        "observedAtMs": observed_at,
        "ageMs": age_ms,
        "temporalClass": temporal_class,
        "bindingIdentity": bound_identity,
        "currentBindingIdentity": current_binding_identity,
        "maxAgeMs": max_age,
        "matchedInvalidations": matching if temporal_class == "dynamic" else [],
        "reobserveRequired": not actionable,
        "actionableWithoutReobservation": actionable,
        "projectionStillAuthoritative": False,
    }


def freshness_envelope(
    snapshot: dict[str, Any],
    *,
    now_ms: int,
    event_hints: list[dict[str, Any]],
    current_binding_identity: dict[str, str] | None = None,
) -> dict[str, Any]:
    freshness = assess_freshness(
        snapshot, now_ms=now_ms, event_hints=event_hints, current_binding_identity=current_binding_identity
    )
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-freshness-envelope",
        "truthRole": "rebuildable-read-only-projection",
        "snapshot": snapshot,
        "freshness": freshness,
        "truthBoundary": {
            "eventHintIsNotOwnerState": True,
            "invalidationForcesReobservationBeforeAction": True,
            "noGlobalFreshnessTtl": True,
            "ownerSuppliesFreshnessBound": True,
            "projectionMayNotPerformOwnerEffect": True,
        },
    }
    result["envelopeDigest"] = canonical_digest(result)
    return result
