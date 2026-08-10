from __future__ import annotations

import hashlib
import json
from typing import Any


class TemporalProjectionError(ValueError):
    pass


class EventHintConflict(TemporalProjectionError):
    pass


_EVENT_TARGETS: dict[str, tuple[str, ...]] = {
    "runtime.release.result": ("source-delivery", "runtime-health"),
    "git.publish.result": ("source-delivery",),
    "workstation.temporary-equipment.acquire": (
        "temporary-equipment",
        "workstation-package-policy",
    ),
    "workstation.temporary-equipment.release": (
        "temporary-equipment",
        "workstation-package-policy",
    ),
    "runtime.workspace.closed": ("workspace-lifecycle",),
    "runtime.workspace.dirty-review": ("workspace-lifecycle", "dirty-aging"),
}


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def event_targets(event_kind: str) -> tuple[str, ...]:
    return _EVENT_TARGETS.get(event_kind, ())


def make_snapshot(
    *,
    signal_id: str,
    owner: str,
    observed_at_ms: int,
    ordering_domain: str,
    invalidation_keys: list[str],
    facts: dict[str, Any],
    max_age_ms: int | None,
    temporal_class: str = "dynamic",
    binding_identity: dict[str, str] | None = None,
) -> dict[str, Any]:
    if temporal_class not in {"dynamic", "immutable_evidence"}:
        raise TemporalProjectionError("unsupported temporal class")
    if not ordering_domain:
        raise TemporalProjectionError("ordering_domain is required")
    if max_age_ms is not None and max_age_ms <= 0:
        raise TemporalProjectionError("max_age_ms must be positive")
    if temporal_class == "immutable_evidence" and binding_identity is None:
        raise TemporalProjectionError("immutable evidence requires binding identity")
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p4-signal-snapshot",
        "truthRole": "rebuildable-read-only-projection",
        "signalId": signal_id,
        "owner": owner,
        "observedAtMs": int(observed_at_ms),
        "orderingDomain": ordering_domain,
        "temporalClass": temporal_class,
        "bindingIdentity": binding_identity,
        "maxAgeMs": max_age_ms,
        "invalidationKeys": sorted(set(invalidation_keys)),
        "facts": facts,
    }
    result["snapshotDigest"] = canonical_digest(result)
    return result


def make_event_hint(
    *,
    event_kind: str,
    owner: str,
    occurred_at_ms: int,
    available_at_ms: int,
    ordering_domain: str,
    change_disposition: str = "unknown",
    receipt_digest: str | None = None,
    evidence_digest: str | None = None,
    event_identity: str | None = None,
    targeted_keys: list[str] | None = None,
) -> dict[str, Any]:
    if change_disposition not in {"changed", "no_change", "unknown"}:
        raise TemporalProjectionError("unsupported change disposition")
    if not owner or not ordering_domain:
        raise TemporalProjectionError("event owner and ordering domain are required")
    if available_at_ms < occurred_at_ms:
        raise TemporalProjectionError("event cannot be available before it occurred")
    targets = sorted(set(targeted_keys if targeted_keys is not None else event_targets(event_kind)))
    semantic = {
        "eventKind": event_kind,
        "owner": owner,
        "occurredAtMs": int(occurred_at_ms),
        "orderingDomain": ordering_domain,
        "changeDisposition": change_disposition,
        "targetedKeys": targets,
        "receiptDigest": receipt_digest,
        "evidenceDigest": evidence_digest,
    }
    semantic_digest = canonical_digest(semantic)
    identity = event_identity or receipt_digest or evidence_digest or semantic_digest
    result = {
        **semantic,
        "availableAtMs": int(available_at_ms),
        "eventIdentity": identity,
        "eventSemanticDigest": semantic_digest,
    }
    result["eventHintDigest"] = canonical_digest(result)
    return result


def normalize_event_hints(
    event_hints: list[dict[str, Any]], *, now_ms: int, ordering_domain: str
) -> dict[str, Any]:
    by_identity: dict[str, dict[str, Any]] = {}
    duplicate_count = 0
    unavailable = 0
    foreign_clock = 0
    for raw in event_hints:
        identity = str(raw.get("eventIdentity", ""))
        semantic_digest = str(raw.get("eventSemanticDigest", ""))
        if not identity or not semantic_digest:
            raise TemporalProjectionError("event hint lacks durable identity")
        existing = by_identity.get(identity)
        if existing is not None:
            if existing["eventSemanticDigest"] != semantic_digest:
                raise EventHintConflict(f"conflicting event replay: {identity}")
            duplicate_count += 1
            if int(raw["availableAtMs"]) < int(existing["availableAtMs"]):
                by_identity[identity] = raw
            continue
        by_identity[identity] = raw

    visible: list[dict[str, Any]] = []
    for event in by_identity.values():
        if event.get("orderingDomain") != ordering_domain:
            foreign_clock += 1
            continue
        if int(event["availableAtMs"]) > int(now_ms):
            unavailable += 1
            continue
        visible.append(event)
    visible.sort(key=lambda item: (int(item["occurredAtMs"]), str(item["eventIdentity"])))
    return {
        "visible": visible,
        "uniqueEvents": len(by_identity),
        "deduplicatedReplays": duplicate_count,
        "notYetAvailable": unavailable,
        "foreignOrderingDomain": foreign_clock,
    }


def assess_temporal_validity(
    snapshot: dict[str, Any],
    *,
    now_ms: int,
    event_hints: list[dict[str, Any]],
    current_binding_identity: dict[str, str] | None = None,
) -> dict[str, Any]:
    observed_at = int(snapshot["observedAtMs"])
    ordering_domain = str(snapshot["orderingDomain"])
    age_ms = max(0, int(now_ms) - observed_at)
    temporal_class = str(snapshot.get("temporalClass", "dynamic"))
    bound_identity = snapshot.get("bindingIdentity")
    keys = set(snapshot.get("invalidationKeys") or [])
    owner = str(snapshot.get("owner", ""))
    normalized = normalize_event_hints(
        event_hints, now_ms=now_ms, ordering_domain=ordering_domain
    )

    matching: list[dict[str, Any]] = []
    suppressed_no_change = 0
    suppressed_cross_owner = 0
    older_than_snapshot = 0
    for event in normalized["visible"]:
        targeted = set(event.get("targetedKeys") or [])
        if not (keys & targeted):
            continue
        if str(event.get("owner")) != owner:
            suppressed_cross_owner += 1
            continue
        if int(event["occurredAtMs"]) <= observed_at:
            older_than_snapshot += 1
            continue
        if event.get("changeDisposition") == "no_change":
            suppressed_no_change += 1
            continue
        matching.append(
            {
                "eventIdentity": event["eventIdentity"],
                "eventKind": event["eventKind"],
                "occurredAtMs": event["occurredAtMs"],
                "availableAtMs": event["availableAtMs"],
                "changeDisposition": event["changeDisposition"],
                "matchedKeys": sorted(keys & targeted),
                "receiptDigest": event.get("receiptDigest"),
                "evidenceDigest": event.get("evidenceDigest"),
            }
        )

    max_age = snapshot.get("maxAgeMs")
    if temporal_class == "immutable_evidence":
        if current_binding_identity is None:
            state = "binding_unknown"
            reason = "current_applicability_identity_not_observed"
        elif current_binding_identity != bound_identity:
            state = "binding_changed"
            reason = "current_identity_differs_from_evidence_binding"
        else:
            state = "immutable_bound"
            reason = "identity_bound_evidence_still_applies"
    elif matching:
        state = "invalidated"
        reason = "owner_change_event_after_observation"
    elif max_age is None:
        state = "freshness_unbounded"
        reason = "no_owner_freshness_bound"
    elif age_ms > int(max_age):
        state = "stale"
        reason = "age_exceeded_owner_bound"
    else:
        state = "fresh"
        reason = "within_owner_bound_and_no_visible_matching_change_event"

    actionable = state in {"fresh", "immutable_bound"}
    residual_ms = None
    if temporal_class == "dynamic" and max_age is not None and state == "fresh":
        residual_ms = max(0, int(max_age) - age_ms)
    return {
        "signalId": snapshot.get("signalId"),
        "owner": owner,
        "snapshotDigest": snapshot.get("snapshotDigest"),
        "freshnessState": state,
        "reason": reason,
        "observedAtMs": observed_at,
        "ageMs": age_ms,
        "orderingDomain": ordering_domain,
        "temporalClass": temporal_class,
        "bindingIdentity": bound_identity,
        "currentBindingIdentity": current_binding_identity,
        "maxAgeMs": max_age,
        "residualFreshnessWindowMs": residual_ms,
        "matchedInvalidations": matching,
        "eventTransport": {
            "uniqueEvents": normalized["uniqueEvents"],
            "deduplicatedReplays": normalized["deduplicatedReplays"],
            "notYetAvailable": normalized["notYetAvailable"],
            "foreignOrderingDomain": normalized["foreignOrderingDomain"],
            "suppressedNoChange": suppressed_no_change,
            "suppressedCrossOwner": suppressed_cross_owner,
            "olderThanSnapshot": older_than_snapshot,
        },
        "reobserveRequired": not actionable,
        "actionableWithoutReobservation": actionable,
        "absenceOfVisibleEventProvesNoOwnerChange": False,
        "eventAccelerationOnly": True,
        "projectionStillAuthoritative": False,
    }
