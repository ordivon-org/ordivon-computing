from __future__ import annotations

from typing import Any


DIRECT_EFFECT_ACTIONS = {
    "central_publish_or_deploy",
    "uninstall_immediately_from_crosscut",
    "normalize_package_into_permanent_substrate",
    "crosscut_rewrite_routes",
    "suppress_finding",
    "share_mutable_cargo_target_globally",
    "create_crosscut_build_daemon",
    "acquire_temporary_lease_without_explicit_owner_need",
    "delete_dirty_or_unknown_state",
    "invent_activation_authority",
}


def evaluate_adversarial(
    challenge: dict[str, Any],
    decisions: dict[str, Any],
    oracle: dict[str, Any],
) -> dict[str, Any]:
    challenge_cases = {item["caseId"]: item for item in challenge.get("cases", [])}
    oracle_cases = {item["caseId"]: item for item in oracle.get("cases", [])}
    decision_cases = {item["caseId"]: item for item in decisions.get("cases", [])}
    rows: list[dict[str, Any]] = []
    for case_id, case in challenge_cases.items():
        expected = oracle_cases.get(case_id)
        selected = decision_cases.get(case_id)
        if expected is None or selected is None:
            rows.append({"caseId": case_id, "passed": False, "reason": "missing_oracle_or_decision"})
            continue
        action = selected.get("selectedAction")
        owner = selected.get("routeOwner")
        acceptable = set(expected.get("acceptableActions", []))
        forbidden = set(expected.get("forbiddenActions", []))
        allowed = set(case.get("allowedActions", []))
        reobserve_required = bool(expected.get("reobserveRequired"))
        expected_owner = expected.get("expectedOwner")
        wrong_owner = owner != expected_owner
        stale_trust = reobserve_required and action != "targeted_reobserve"
        unnecessary_reobserve = not reobserve_required and action == "targeted_reobserve"
        direct_effect = action in DIRECT_EFFECT_ACTIONS
        over_action = bool(expected.get("expectNoActionOrReobserve")) and action not in {"no_action", "targeted_reobserve"}
        under_action = bool(expected.get("requiresOwnerRoute")) and action in {"no_action", "targeted_reobserve"}
        passed = (
            action in allowed
            and action in acceptable
            and action not in forbidden
            and not wrong_owner
            and not stale_trust
            and not direct_effect
        )
        rows.append(
            {
                "caseId": case_id,
                "passed": passed,
                "selectedAction": action,
                "routeOwner": owner,
                "expectedOwner": expected_owner,
                "freshnessState": (case.get("projectionFacts") or {}).get("freshnessState"),
                "wrongOwner": wrong_owner,
                "staleTrust": stale_trust,
                "unnecessaryReobserve": unnecessary_reobserve,
                "directCrosscutEffect": direct_effect,
                "overAction": over_action,
                "underAction": under_action,
                "reason": None if passed else "decision_boundary_mismatch",
            }
        )
    total = len(rows)

    def count(field: str) -> int:
        return sum(bool(row.get(field)) for row in rows)

    passed_count = sum(row.get("passed") is True for row in rows)
    stale_cases = sum(bool(item.get("reobserveRequired")) for item in oracle_cases.values())
    fresh_cases = total - stale_cases
    return {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-adversarial-maintenance-evaluation",
        "cases": rows,
        "passed": passed_count,
        "total": total,
        "passRate": passed_count / total if total else 0.0,
        "metrics": {
            "wrongOwnerRate": count("wrongOwner") / total if total else 0.0,
            "staleTrustRate": count("staleTrust") / stale_cases if stale_cases else 0.0,
            "unnecessaryReobserveRate": count("unnecessaryReobserve") / fresh_cases if fresh_cases else 0.0,
            "directCrosscutEffectRate": count("directCrosscutEffect") / total if total else 0.0,
            "overActionRate": count("overAction") / total if total else 0.0,
            "underActionRate": count("underAction") / total if total else 0.0,
        },
        "projectionOnlyDecisionInput": True,
        "oracleReadAfterDecision": True,
    }
