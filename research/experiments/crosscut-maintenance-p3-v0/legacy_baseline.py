from __future__ import annotations

from typing import Any


def legacy_decision(case: dict[str, Any]) -> dict[str, Any]:
    """Approximate P2 action selection when freshness metadata is absent.

    This is an interface ablation, not an Agent benchmark: it deliberately acts on the
    visible snapshot state and cannot know that a later owner event invalidated it.
    """
    facts = case.get("legacyProjectionFacts") or case.get("projectionFacts") or {}
    owner = facts.get("owner")
    state = facts.get("semanticState") or facts.get("deliveryState")
    if state in {"active_source_not_published", "source_not_published"}:
        action = "route_publication_gap_to_owner"
    elif state in {"forbidden_package_without_lease", "ambiguous_temporary_equipment_need"}:
        action = "route_owner_review"
    elif state == "network_owner_error":
        action = "route_network_owner"
    elif state == "private_build_reuse_proved":
        action = "route_runtime_build_owner"
    elif state in {"converged", "advisory_only", "healthy", "temporary_lease_active"}:
        action = "no_action"
    else:
        action = "route_owner_review"
    return {"caseId": case["caseId"], "selectedAction": action, "routeOwner": owner}


def run_legacy_baseline(challenge: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-p3-legacy-baseline",
        "cases": [legacy_decision(case) for case in challenge.get("cases", [])],
    }
