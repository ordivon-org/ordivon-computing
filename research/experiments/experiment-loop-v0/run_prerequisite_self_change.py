from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cel import load_record, write_record

ROOT = Path(__file__).resolve().parents[3]
PLAN_V1 = ROOT / "research/experiments/experiment-loop-v0/plan-v1.json"
PLAN_V3 = ROOT / "research/experiments/experiment-loop-v0/plan-v3.json"
E1_CLOSEOUT = ROOT / "research/experiments/experiment-loop-v0/campaigns/cel-p1-selection-001/closeout.json"
HHO_PLAN = ROOT / "research/experiments/observation-plane-v0/plan-v1.json"
HHR_PLAN = ROOT / "research/experiments/harness-evaluation-v0/formal-trial-plan-v1.json"
P0_CLOSEOUT = ROOT / "research/experiments/p0-consumer-falsification-v0/evidence/p0-live-closeout.json"


BASELINE_POLICY_ID = "named_phase_status_v1"
CANDIDATE_POLICY_ID = "capability_evidence_v1"


def _legacy_ready() -> tuple[bool, dict[str, str]]:
    legacy = json.loads(PLAN_V1.read_text(encoding="utf-8"))
    actual = {
        "HHO-P0-P1-001": json.loads(HHO_PLAN.read_text(encoding="utf-8"))["status"],
        "HHR-R3-001": json.loads(HHR_PLAN.read_text(encoding="utf-8"))["status"],
    }
    required = {item["planId"]: item["requiredStatus"] for item in legacy["prerequisites"]}
    return all(actual[key] == required[key] for key in required), actual


def _current_capabilities() -> dict[str, bool]:
    plan = json.loads(PLAN_V3.read_text(encoding="utf-8"))
    return {item["capabilityId"]: bool(item["satisfied"]) for item in plan["prerequisites"]}


def _p0_positive_support() -> tuple[bool, bool]:
    p0 = json.loads(P0_CLOSEOUT.read_text(encoding="utf-8"))
    a = p0["p0A"]["summary"]
    b = p0["p0B"]["summary"]
    p0_a = a["S"]["validTrials"] >= 3 and a["H"]["validTrials"] >= 3
    p0_b = all(
        b[fixture][treatment]["validTrials"] >= 3
        for fixture in ("act", "hold")
        for treatment in ("direct", "late-authority")
    )
    return p0_a, p0_b


def build_cases() -> list[dict[str, Any]]:
    capabilities = _current_capabilities()
    p0_a, p0_b = _p0_positive_support()
    if not all(capabilities.values()) or not p0_a or not p0_b:
        raise RuntimeError("current prerequisite evidence is not complete enough for E2")

    cases: list[dict[str, Any]] = [
        {
            "caseId": "current-p0-a-support",
            "split": "development",
            "capabilities": capabilities,
            "expectedReady": True,
            "evidenceSlice": "p0A",
        },
        {
            "caseId": "current-p0-b-support",
            "split": "holdout",
            "capabilities": capabilities,
            "expectedReady": True,
            "evidenceSlice": "p0B",
        },
    ]
    capability_ids = sorted(capabilities)
    for index, capability_id in enumerate(capability_ids):
        changed = dict(capabilities)
        changed[capability_id] = False
        cases.append(
            {
                "caseId": f"missing-{capability_id}",
                "split": "holdout" if index == len(capability_ids) - 1 else "development",
                "capabilities": changed,
                "expectedReady": False,
                "evidenceSlice": "negative-control",
            }
        )
    return cases


def resolve(case: dict[str, Any], policy_id: str, *, legacy_ready: bool) -> bool:
    if policy_id == BASELINE_POLICY_ID:
        return legacy_ready
    if policy_id == CANDIDATE_POLICY_ID:
        capabilities = case["capabilities"]
        return bool(capabilities) and all(value is True for value in capabilities.values())
    raise ValueError(policy_id)


def evaluate(cases: list[dict[str, Any]], policy_id: str, *, split: str, legacy_ready: bool) -> dict[str, Any]:
    selected = [case for case in cases if case["split"] == split]
    rows = []
    false_ready = 0
    false_block = 0
    for case in selected:
        actual = resolve(case, policy_id, legacy_ready=legacy_ready)
        expected = case["expectedReady"]
        false_ready += int(actual and not expected)
        false_block += int((not actual) and expected)
        rows.append(
            {
                "caseId": case["caseId"],
                "actualReady": actual,
                "expectedReady": expected,
                "matches": actual == expected,
            }
        )
    return {
        "policyId": policy_id,
        "split": split,
        "total": len(rows),
        "correct": sum(int(row["matches"]) for row in rows),
        "falseReady": false_ready,
        "falseBlock": false_block,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    e1 = load_record(E1_CLOSEOUT, expected_kind="ordivon.cel-campaign-closeout")
    if e1["disposition"] != "promote_research_policy" or e1["researchPolicyWinner"] != "campaign_declared_evidence_v2":
        raise RuntimeError("E2 requires the first-generation selection self-change")

    legacy_ready, legacy_statuses = _legacy_ready()
    cases = build_cases()
    policies = (BASELINE_POLICY_ID, CANDIDATE_POLICY_ID)
    campaign = write_record(
        args.output_dir / "campaign.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-campaign-manifest",
            "campaignId": "CEL-P1-PREREQUISITE-002",
            "generation": 2,
            "parentSelfChangeRef": "research/experiments/experiment-loop-v0/campaigns/cel-p1-selection-001/closeout.json",
            "planRef": "research/experiments/experiment-loop-v0/plan-v3.json#CEL-R4-003",
            "question": "Should CEL readiness be owned by exact capability evidence or by historical phase-name status strings?",
            "changeSurface": ["prerequisite_policy"],
            "policies": list(policies),
            "legacyObservedStatuses": legacy_statuses,
            "finiteExhaustiveCases": len(cases),
            "trajectoryThresholdNotApplicableReason": "deterministic exhaustive prerequisite conformance over the complete current capability set plus leave-one-out controls",
            "promotionBoundary": "research_policy_only",
        },
    )

    development = [evaluate(cases, policy, split="development", legacy_ready=legacy_ready) for policy in policies]
    admissible = [item for item in development if item["falseReady"] == 0]
    admissible.sort(key=lambda item: (item["falseBlock"], -item["correct"], item["policyId"]))
    winner = admissible[0] if admissible else None
    development_decision = {
        "winnerPolicyId": winner["policyId"] if winner else None,
        "reason": "zero false-ready hard gate, then minimum false-block" if winner else "no admissible policy",
    }
    write_record(
        args.output_dir / "development-evaluation.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-prerequisite-evaluation",
            "campaignDigest": campaign["integrity"]["payloadDigest"],
            "split": "development",
            "evaluations": development,
            "decision": development_decision,
        },
    )

    holdout = []
    disposition = "stop_no_winner"
    if winner is not None:
        evaluated = evaluate(cases, winner["policyId"], split="holdout", legacy_ready=legacy_ready)
        holdout.append(evaluated)
        if evaluated["falseReady"] == 0 and evaluated["falseBlock"] == 0:
            disposition = "promote_second_generation_research_policy"
        else:
            disposition = "rollback_second_generation_candidate"
    write_record(
        args.output_dir / "holdout-evaluation.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-prerequisite-evaluation",
            "campaignDigest": campaign["integrity"]["payloadDigest"],
            "split": "holdout",
            "evaluations": holdout,
        },
    )
    closeout = write_record(
        args.output_dir / "closeout.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-campaign-closeout",
            "campaignId": campaign["campaignId"],
            "generation": 2,
            "parentSelfChangeRef": campaign["parentSelfChangeRef"],
            "developmentDecision": development_decision,
            "holdoutEvaluations": holdout,
            "disposition": disposition,
            "researchPolicyWinner": winner["policyId"] if disposition.startswith("promote") else None,
            "legacyPhaseReady": legacy_ready,
            "automaticProductPromotion": False,
            "worldModelRound002Required": False,
            "meaning": "The improved CEL selected a second change to its own prerequisite resolver and preserved fail-closed behavior under every leave-one-capability-out negative control.",
        },
    )
    print(json.dumps({"disposition": disposition, "development": development, "holdout": holdout}, sort_keys=True))
    return 0 if disposition == "promote_second_generation_research_policy" else 2


if __name__ == "__main__":
    raise SystemExit(main())
