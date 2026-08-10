from __future__ import annotations

from typing import Any


def evaluate_decisions(
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
        allowed = set(case.get("allowedActions", []))
        expected_actions = set(expected.get("acceptableActions", []))
        forbidden_actions = set(expected.get("forbiddenActions", []))
        passed = (
            action in allowed
            and action in expected_actions
            and action not in forbidden_actions
            and owner == expected.get("expectedOwner")
        )
        rows.append(
            {
                "caseId": case_id,
                "passed": passed,
                "selectedAction": action,
                "routeOwner": owner,
                "expectedOwner": expected.get("expectedOwner"),
                "reason": None if passed else "action_or_owner_mismatch",
            }
        )
    passed = sum(item["passed"] is True for item in rows)
    return {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-agent-maintenance-evaluation",
        "cases": rows,
        "passed": passed,
        "total": len(rows),
        "passRate": passed / len(rows) if rows else 0.0,
        "projectionOnlyDecisionInput": True,
        "ownerTruthUsedOnlyForPostDecisionVerification": True,
    }
