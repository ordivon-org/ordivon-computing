from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any

from cel import decide_eligibility, load_record, select_policy, write_record

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURE = ROOT / "research/experiments/experiment-loop-v0/fixtures/p0-policy-v1"

BASELINE_POLICY = {
    "policyId": "observation_always_required_v1",
    "mode": "observation_always_required_v1",
    "requiredClaims": [
        "observation_complete",
        "configuration_exact",
        "independent_grader_complete",
        "no_unresolved_effect",
        "candidate_mutation_frozen",
    ],
}

CANDIDATE_POLICY = {
    "policyId": "campaign_declared_evidence_v2",
    "mode": "campaign_declared_evidence_v2",
}


def _join_labels(
    corpus: dict[str, Any], evaluator: dict[str, Any], *, split: str
) -> list[dict[str, Any]]:
    labels = {item["trajectoryId"]: item for item in evaluator["labels"]}
    cases: list[dict[str, Any]] = []
    for trajectory in corpus["trajectories"]:
        if trajectory["split"] != split:
            continue
        label = labels.get(trajectory["trajectoryId"])
        if label is None:
            raise ValueError(f"missing evaluator label for {trajectory['trajectoryId']}")
        cases.append((trajectory, label))
    if not cases:
        raise ValueError(f"no cases for split {split}")
    return cases


def evaluate(
    corpus: dict[str, Any], evaluator: dict[str, Any], policy: dict[str, Any], *, split: str
) -> dict[str, Any]:
    false_inclusions = 0
    false_exclusions = 0
    correct = 0
    results = []
    for trajectory, label in _join_labels(corpus, evaluator, split=split):
        decision = decide_eligibility(trajectory, policy)
        expected = bool(label["expectedEligible"])
        matches = decision.eligible == expected
        correct += int(matches)
        false_inclusions += int(decision.eligible and not expected)
        false_exclusions += int((not decision.eligible) and expected)
        results.append(
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
        "split": split,
        "total": len(results),
        "correct": correct,
        "falseInclusions": false_inclusions,
        "falseExclusions": false_exclusions,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-dir", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    corpus = load_record(
        args.fixture_dir / "trajectory-corpus-v1.json",
        expected_kind="ordivon.cel-policy-trajectory-corpus",
    )
    evaluator = load_record(
        args.fixture_dir / "evaluator-labels-v1.json",
        expected_kind="ordivon.cel-policy-evaluator-labels",
    )
    if corpus["trajectoryCount"] < 20:
        raise ValueError("self-change corpus must contain at least 20 trajectories")

    policies = (BASELINE_POLICY, CANDIDATE_POLICY)
    campaign = write_record(
        args.output_dir / "campaign.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-campaign-manifest",
            "campaignId": "CEL-P1-SELECTION-ELIGIBILITY-001",
            "question": "Should CEL require Observation completeness for every Trial, or require only the evidence claims declared by the exact Campaign?",
            "baseRevision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "planRef": "research/experiments/experiment-loop-v0/plan-v2.json#CEL-R4-002",
            "corpusRef": str((args.fixture_dir / "trajectory-corpus-v1.json").relative_to(ROOT)),
            "evaluatorRef": str((args.fixture_dir / "evaluator-labels-v1.json").relative_to(ROOT)),
            "changeSurface": ["trial_selection_policy.required_evidence_claims"],
            "forbiddenSurface": [
                "trajectory_validity_labels",
                "evaluator_labels",
                "P0_verifier_outcomes",
                "owner_authority",
                "product_state",
            ],
            "policies": list(policies),
            "developmentCount": corpus["splitCounts"]["development"],
            "holdoutCount": corpus["splitCounts"]["holdout"],
            "promotionBoundary": "research_policy_only",
        },
    )

    development = [evaluate(corpus, evaluator, policy, split="development") for policy in policies]
    development_decision = select_policy(development)
    write_record(
        args.output_dir / "development-evaluation.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-policy-evaluation",
            "campaignDigest": campaign["integrity"]["payloadDigest"],
            "split": "development",
            "evaluations": development,
            "decision": development_decision,
        },
    )

    winner_id = development_decision["winnerPolicyId"]
    if winner_id is None:
        holdout_evaluations: list[dict[str, Any]] = []
        final_disposition = "stop_no_development_winner"
    else:
        winner = next(policy for policy in policies if policy["policyId"] == winner_id)
        holdout = evaluate(corpus, evaluator, winner, split="holdout")
        holdout_evaluations = [holdout]
        if holdout["falseInclusions"] == 0 and holdout["falseExclusions"] == 0:
            final_disposition = "promote_research_policy"
        else:
            final_disposition = "rollback_candidate"

    write_record(
        args.output_dir / "holdout-evaluation.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-policy-evaluation",
            "campaignDigest": campaign["integrity"]["payloadDigest"],
            "split": "holdout",
            "evaluations": holdout_evaluations,
            "candidateVisibleLabels": False,
        },
    )

    closeout = write_record(
        args.output_dir / "closeout.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-campaign-closeout",
            "campaignId": campaign["campaignId"],
            "campaignDigest": campaign["integrity"]["payloadDigest"],
            "developmentDecision": development_decision,
            "holdoutEvaluations": holdout_evaluations,
            "disposition": final_disposition,
            "researchPolicyWinner": winner_id if final_disposition == "promote_research_policy" else None,
            "negativeResultRetained": any(
                item["falseExclusions"] > 0 or item["falseInclusions"] > 0
                for item in development
            ),
            "automaticProductPromotion": False,
            "worldModelRound002Required": False,
            "limitations": [
                "Corpus is P0-family evidence from one Provider/model configuration.",
                "This campaign tests Trial-selection evidence semantics, not model intelligence.",
                "A promoted policy remains research-local until another campaign or owner consumer contradicts it.",
            ],
        },
    )
    print(json.dumps({
        "disposition": closeout["disposition"],
        "winner": closeout["researchPolicyWinner"],
        "development": development,
        "holdout": holdout_evaluations,
    }, ensure_ascii=False, sort_keys=True))
    return 0 if final_disposition == "promote_research_policy" else 2


if __name__ == "__main__":
    raise SystemExit(main())
