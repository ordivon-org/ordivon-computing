#!/usr/bin/env python3
"""Validate the narrow current experiment-local contract template."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "research" / "experiment-contract-v1.json"


def digest(document: dict[str, Any]) -> str:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def check() -> list[str]:
    issues: list[str] = []
    try:
        document = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"experiment contract cannot be loaded: {error}"]

    def require(condition: bool, message: str) -> None:
        if not condition:
            issues.append(message)

    require(document.get("schemaVersion") == 1, "experiment contract schema differs")
    require(document.get("kind") == "ordivon.experiment-local-contract-template", "experiment contract kind differs")
    require(document.get("contractId") == "EXPERIMENT-CONTRACT-001", "experiment contract identity differs")
    require(document.get("status") == "current_template", "experiment contract status differs")
    require(document.get("integrity", {}).get("payloadDigest") == digest(document), "experiment contract digest differs")

    declarations = document.get("requiredDeclarations")
    expected = {
        "mission", "questionOrHypothesis", "evidenceSelection", "strongBaseline",
        "minimalCandidateOrNoChange", "independentOracle", "developmentSplit", "holdoutSplit",
        "invalidityConditions", "authorityBoundary", "budget", "stopRule",
        "deletionOrNoChangeOutcome", "rollbackRule", "publicationBoundary",
    }
    require(isinstance(declarations, list) and set(declarations) == expected, "experiment required declaration set differs")
    require(isinstance(declarations, list) and len(declarations) == len(set(declarations)), "experiment declarations are duplicated")

    invariants = set(document.get("invariants", []))
    for required in {
        "local_contract_is_frozen_before_competitive_evaluation",
        "oracle_is_independent_of_candidate_output",
        "invalid_campaign_is_retained_and_not_rescored",
        "negative_null_and_delete_results_are_first_class",
        "template_does_not_choose_the_hypothesis_or_correct_answer",
        "product_and_domain_authority_remain_owner_local",
        "persistent_self_change_requires_rollback_rehearsal_or_explicit_non_applicability",
        "no_post_validity_tuning_solely_to_chase_promotion",
    }:
        require(required in invariants, f"experiment invariant is missing: {required}")

    localization = document.get("localizationRule")
    require(isinstance(localization, str) and "own exact local record" in localization, "experiment localization rule differs")
    require(isinstance(localization, str) and "authorizes no experiment" in localization, "experiment template claims execution authority")
    require("claimBoundary" in document, "experiment contract claim boundary is missing")
    return sorted(set(issues))


if __name__ == "__main__":
    issues = check()
    print(json.dumps({"schemaVersion": 1, "kind": "ordivon-experiment-contract-check", "ok": not issues, "issues": issues}, indent=2, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if not issues else 1)
