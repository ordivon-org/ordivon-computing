from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


class CELRecordError(ValueError):
    pass


def canonical_digest(value: dict[str, Any]) -> str:
    payload = dict(value)
    payload.pop("integrity", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evidence-json-v1",
        "payloadDigest": canonical_digest(result),
    }
    return result


def validate_integrity(value: dict[str, Any]) -> None:
    integrity = value.get("integrity")
    if not isinstance(integrity, dict):
        raise CELRecordError("record integrity is missing")
    if integrity.get("algorithm") != "sha256":
        raise CELRecordError("unsupported record integrity algorithm")
    if integrity.get("payloadDigest") != canonical_digest(value):
        raise CELRecordError("record payload digest differs")


def load_record(path: Path, *, expected_kind: str | None = None) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CELRecordError(f"record must be an object: {path}")
    validate_integrity(value)
    if expected_kind is not None and value.get("kind") != expected_kind:
        raise CELRecordError(
            f"record kind differs for {path}: {value.get('kind')!r} != {expected_kind!r}"
        )
    return value


def write_record(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    sealed = seal(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sealed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return sealed


@dataclass(frozen=True)
class EligibilityDecision:
    eligible: bool
    reason: str


def _claim_true(trajectory: dict[str, Any], claim: str) -> bool:
    claims = trajectory.get("evidenceClaims")
    return isinstance(claims, dict) and claims.get(claim) is True


def decide_eligibility(
    trajectory: dict[str, Any],
    policy: dict[str, Any],
) -> EligibilityDecision:
    """Apply one frozen Trial-selection policy without reading evaluator labels.

    The evaluator-owned ``expectedEligible`` field is deliberately ignored here.
    """

    if trajectory.get("validity") != "valid":
        return EligibilityDecision(False, "validity_not_valid")

    mode = policy.get("mode")
    if mode == "observation_always_required_v1":
        required = tuple(policy.get("requiredClaims", ()))
    elif mode == "campaign_declared_evidence_v2":
        required = tuple(trajectory.get("campaignRequiredEvidenceClaims", ()))
        if not required:
            return EligibilityDecision(False, "campaign_required_claims_missing")
    else:
        raise CELRecordError(f"unsupported eligibility policy mode: {mode!r}")

    missing = [claim for claim in required if not _claim_true(trajectory, claim)]
    if missing:
        return EligibilityDecision(False, "missing:" + ",".join(sorted(missing)))
    return EligibilityDecision(True, "eligible")


def evaluate_policy(
    trajectories: Iterable[dict[str, Any]],
    policy: dict[str, Any],
) -> dict[str, Any]:
    cases = []
    false_inclusions = 0
    false_exclusions = 0
    correct = 0
    total = 0
    for trajectory in trajectories:
        total += 1
        decision = decide_eligibility(trajectory, policy)
        expected = trajectory.get("expectedEligible")
        if not isinstance(expected, bool):
            raise CELRecordError("trajectory expectedEligible must be boolean")
        matches = decision.eligible == expected
        correct += int(matches)
        false_inclusions += int(decision.eligible and not expected)
        false_exclusions += int((not decision.eligible) and expected)
        cases.append(
            {
                "trajectoryId": trajectory["trajectoryId"],
                "expectedEligible": expected,
                "actualEligible": decision.eligible,
                "decisionReason": decision.reason,
                "matchesEvaluator": matches,
            }
        )
    return {
        "policyId": policy["policyId"],
        "total": total,
        "correct": correct,
        "falseInclusions": false_inclusions,
        "falseExclusions": false_exclusions,
        "cases": cases,
    }


def select_policy(evaluations: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Deterministic hard-gate selection for eligibility policy candidates."""

    values = list(evaluations)
    admissible = [item for item in values if item["falseInclusions"] == 0]
    if not admissible:
        return {
            "disposition": "stop_no_admissible_candidate",
            "winnerPolicyId": None,
            "reason": "every candidate false-included evaluator-rejected trajectories",
        }
    admissible.sort(
        key=lambda item: (
            item["falseExclusions"],
            -item["correct"],
            item["policyId"],
        )
    )
    leader = admissible[0]
    tied = [
        item
        for item in admissible
        if (
            item["falseExclusions"],
            item["correct"],
        )
        == (
            leader["falseExclusions"],
            leader["correct"],
        )
    ]
    if len(tied) != 1:
        return {
            "disposition": "inconclusive_tie",
            "winnerPolicyId": None,
            "reason": "multiple candidates have the same evaluator outcome",
        }
    return {
        "disposition": "provisional_winner",
        "winnerPolicyId": leader["policyId"],
        "reason": "zero false inclusions and minimum false exclusions",
    }


def evaluate_split(
    trajectories: Iterable[dict[str, Any]],
    policies: Iterable[dict[str, Any]],
    *,
    split: str,
) -> list[dict[str, Any]]:
    selected = [item for item in trajectories if item.get("split") == split]
    if not selected:
        raise CELRecordError(f"no trajectories for split {split!r}")
    return [evaluate_policy(selected, policy) for policy in policies]


def bounded_stop_decision(
    ordered_evaluator_cases: list[dict[str, Any]],
    *,
    minimum_cases: int,
    false_inclusion_ceiling: int = 0,
    false_exclusion_ceiling: int = 0,
) -> dict[str, Any]:
    """A tiny deterministic stopping policy used only after a winner is frozen.

    The policy never changes evaluator labels or candidate outcomes. It asks when
    enough already-evaluated cases exist to stop a bounded conformance campaign.
    """

    if minimum_cases < 1:
        raise CELRecordError("minimum_cases must be positive")
    seen = 0
    false_inclusions = 0
    false_exclusions = 0
    for case in ordered_evaluator_cases:
        seen += 1
        expected = bool(case["expectedEligible"])
        actual = bool(case["actualEligible"])
        false_inclusions += int(actual and not expected)
        false_exclusions += int((not actual) and expected)
        if (
            seen >= minimum_cases
            and false_inclusions <= false_inclusion_ceiling
            and false_exclusions <= false_exclusion_ceiling
        ):
            return {
                "stop": True,
                "evaluatedCases": seen,
                "falseInclusions": false_inclusions,
                "falseExclusions": false_exclusions,
                "reason": "minimum evidence reached with hard gates satisfied",
            }
    return {
        "stop": False,
        "evaluatedCases": seen,
        "falseInclusions": false_inclusions,
        "falseExclusions": false_exclusions,
        "reason": "declared evidence exhausted before stop gate",
    }
