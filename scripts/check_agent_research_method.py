#!/usr/bin/env python3
"""Validate the Agent-first Ordivon research method and its first consumer."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
METHOD_PATH = ROOT / "research" / "research-method-v1.json"
CEL_PATH = ROOT / "research" / "experiments" / "experiment-loop-v0" / "plan-v1.json"


def canonical_digest(document: dict[str, Any]) -> str:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _require(condition: bool, message: str, issues: list[str]) -> None:
    if not condition:
        issues.append(message)


def _unique_strings(value: Any, label: str, issues: list[str]) -> set[str]:
    _require(isinstance(value, list) and bool(value), f"{label} must be non-empty", issues)
    if not isinstance(value, list):
        return set()
    _require(
        all(isinstance(item, str) and item for item in value),
        f"{label} entries must be strings",
        issues,
    )
    strings = [item for item in value if isinstance(item, str)]
    _require(len(strings) == len(set(strings)), f"{label} entries must be unique", issues)
    return set(strings)


def check_method(root: Path = ROOT) -> list[str]:
    issues: list[str] = []
    try:
        method = json.loads((root / "research" / "research-method-v1.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"research method cannot be loaded: {error}"]

    _require(method.get("schemaVersion") == 1, "unsupported research method schema", issues)
    _require(method.get("kind") == "ordivon.agent-first-research-method", "invalid research method kind", issues)
    _require(method.get("methodId") == "AFR-M1-001", "invalid research method identity", issues)
    _require(method.get("status") == "active_method", "research method is not active", issues)

    integrity = method.get("integrity")
    _require(isinstance(integrity, dict), "research method integrity is missing", issues)
    if isinstance(integrity, dict):
        _require(integrity.get("algorithm") == "sha256", "research method integrity algorithm differs", issues)
        _require(
            integrity.get("canonicalization") == "ordivon-evidence-json-v1",
            "research method canonicalization differs",
            issues,
        )
        _require(
            integrity.get("payloadDigest") == canonical_digest(method),
            "research method payload digest differs",
            issues,
        )

    principles = _unique_strings(method.get("principles"), "research principles", issues)
    for required in {
        "agent_is_default_research_operator",
        "human_attention_is_reserved_for_purpose_consequence_and_boundary_change",
        "externalization_is_a_hypothesis_not_a_presumption",
        "strong_classical_and_simpler_agent_baselines_precede_new_structure",
        "negative_null_and_deletion_results_are_first_class",
        "no_raw_private_chain_of_thought_is_required",
    }:
        _require(required in principles, f"required research principle is missing: {required}", issues)

    authority = method.get("authority")
    _require(isinstance(authority, dict), "research authority map is missing", issues)
    if isinstance(authority, dict):
        _require(
            set(authority)
            == {
                "humanPurposeAuthority",
                "agentResearchOperator",
                "deterministicResearchPolicy",
                "productAndDomainOwners",
            },
            "research authority roles differ",
            issues,
        )
        agent = authority.get("agentResearchOperator", {})
        human = authority.get("humanPurposeAuthority", {})
        if isinstance(agent, dict):
            may = _unique_strings(agent.get("mayProceedWithoutHumanWhen"), "Agent autonomous conditions", issues)
            escalate = _unique_strings(agent.get("mustEscalateWhen"), "Agent escalation conditions", issues)
            _require("work_is_private_or_research_only" in may, "private research is not autonomously admitted", issues)
            _require("effects_are_reversible_or_reconciled" in may, "reversible research condition is missing", issues)
            _require("research_mission_changes" in escalate, "mission-change escalation is missing", issues)
            _require("irreversible_or_public_effect_is_requested" in escalate, "irreversible-effect escalation is missing", issues)
        if isinstance(human, dict):
            does_not_own = _unique_strings(human.get("doesNotOwn"), "human non-authority", issues)
            _require("trial_validity" in does_not_own, "human purpose authority may not own Trial validity", issues)
            _require(
                "routine_reversible_private_research_steps" in does_not_own,
                "routine private research still depends on human authority",
                issues,
            )

    expected_stages = [
        "OBSERVE",
        "PLACE_RESPONSIBILITY",
        "PROPOSE_EXTERNALIZATION",
        "PREFLIGHT",
        "EXPERIMENT",
        "DISPOSE",
        "SINK_OR_REMOVE",
    ]
    loop = method.get("loop")
    _require(isinstance(loop, list), "research loop must be a list", issues)
    if isinstance(loop, list):
        _require([item.get("stage") for item in loop if isinstance(item, dict)] == expected_stages, "research loop stages differ", issues)
        for item in loop:
            _require(isinstance(item, dict), "research loop entry must be an object", issues)
            if isinstance(item, dict):
                _require(bool(item.get("goal")), f"research stage goal is missing: {item.get('stage')}", issues)
                _require(bool(item.get("gate")), f"research stage gate is missing: {item.get('stage')}", issues)

    burden_classes = _unique_strings(method.get("burdenClasses"), "burden classes", issues)
    for required in {
        "token_reconstruction",
        "mechanical_translation",
        "continuity_recovery",
        "human_runtime",
        "compute_orchestration",
        "relational_cognitive_state",
    }:
        _require(required in burden_classes, f"required burden class is missing: {required}", issues)

    gates = _unique_strings(method.get("admissionGates"), "admission gates", issues)
    for required in {
        "observed_burden_exists_in_real_or_representative_agent_work",
        "a_mature_classical_or_simpler_agent_baseline_is_named",
        "candidate_externalizes_a_specific_responsibility_not_a_theme",
        "benefit_is_independently_observable",
        "rollback_or_deletion_path_is_explicit",
        "routine_private_reversible_research_requires_no_human_intervention",
    }:
        _require(required in gates, f"required admission gate is missing: {required}", issues)

    records = method.get("records")
    _require(isinstance(records, dict), "research records are missing", issues)
    if isinstance(records, dict):
        _require(
            set(records)
            == {
                "BurdenObservation",
                "ResponsibilityPlacement",
                "ExternalizationHypothesis",
                "AdmissionRecord",
                "ExternalizationDecision",
            },
            "research record set differs",
            issues,
        )
        for name, declaration in records.items():
            if isinstance(declaration, dict):
                _unique_strings(declaration.get("required"), f"{name} required fields", issues)

    existing = method.get("existingAuthorities")
    _require(isinstance(existing, dict), "existing authority references are missing", issues)
    if isinstance(existing, dict):
        for label, relative in existing.items():
            _require(isinstance(relative, str) and bool(relative), f"invalid authority ref: {label}", issues)
            if isinstance(relative, str):
                _require((root / relative).exists(), f"missing authority ref: {label} -> {relative}", issues)

    method_doc = root / "research" / "AGENT-FIRST-RESEARCH-METHOD.md"
    _require(method_doc.is_file(), "human-readable research method projection is missing", issues)

    try:
        cel = json.loads((root / "research" / "experiments" / "experiment-loop-v0" / "plan-v1.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        issues.append(f"CEL plan cannot be loaded: {error}")
    else:
        _require(cel.get("methodRef") == "research/research-method-v1.json", "CEL does not consume the Agent-first research method", issues)
        decisions = cel.get("decisions", {})
        _require(decisions.get("agentOwnsBoundedResearchProgression") is True, "CEL is not Agent-led for bounded research progression", issues)
        _require(decisions.get("humanAttentionIsConsequenceBounded") is True, "CEL human attention is not consequence-bounded", issues)
        _require(decisions.get("productPromotionOwnedByProductAuthority") is True, "CEL product promotion authority is unclear", issues)
        _require("humanOwnsPromotion" not in decisions, "legacy human-owned research promotion remains in CEL", issues)

    return sorted(set(issues))


def main() -> int:
    issues = check_method()
    print(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "ordivon-agent-first-research-method-check",
                "ok": not issues,
                "issues": issues,
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
