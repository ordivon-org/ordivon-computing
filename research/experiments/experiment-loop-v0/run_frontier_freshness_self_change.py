from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Callable

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from cel import load_record, write_record
from frontier_freshness import baseline_syntax_only, candidate_git_relation

P1_CLOSEOUT = ROOT / "research/experiments/experiment-loop-v0/p1-bounded-rsi-closeout.json"
PLAN_V5 = ROOT / "research/experiments/experiment-loop-v0/plan-v5.json"

POLICIES: tuple[tuple[str, Callable[[dict], dict]], ...] = (
    ("syntactic_revision_v1", baseline_syntax_only),
    ("git_relation_freshness_v2", candidate_git_relation),
)


def _cases(corpus: dict, labels: dict, split: str) -> list[tuple[dict, dict]]:
    by_id = {item["projectId"]: item for item in labels["labels"]}
    result = []
    for entry in corpus["entries"]:
        if entry["split"] != split:
            continue
        label = by_id[entry["projectId"]]
        result.append((entry, label))
    if not result:
        raise RuntimeError(f"no cases for {split}")
    return result


def evaluate(corpus: dict, labels: dict, split: str, policy_id: str, policy: Callable[[dict], dict]) -> dict:
    rows = []
    false_current = 0
    false_stale = 0
    state_mismatch = 0
    for entry, label in _cases(corpus, labels, split):
        actual = policy(entry)
        expected_current = bool(label["expectedCurrent"])
        expected_state = label["expectedFreshnessState"]
        actual_current = bool(actual["current"])
        actual_state = actual["freshnessState"]
        false_current += int(actual_current and not expected_current)
        false_stale += int((not actual_current) and expected_current)
        state_mismatch += int(actual_state != expected_state)
        rows.append(
            {
                "projectId": entry["projectId"],
                "expectedCurrent": expected_current,
                "actualCurrent": actual_current,
                "expectedFreshnessState": expected_state,
                "actualFreshnessState": actual_state,
                "matchesCurrent": actual_current == expected_current,
                "matchesState": actual_state == expected_state,
            }
        )
    return {
        "policyId": policy_id,
        "split": split,
        "total": len(rows),
        "correctCurrent": sum(int(row["matchesCurrent"]) for row in rows),
        "correctState": sum(int(row["matchesState"]) for row in rows),
        "falseCurrent": false_current,
        "falseStale": false_stale,
        "stateMismatch": state_mismatch,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    p1 = load_record(P1_CLOSEOUT, expected_kind="ordivon.computing-p1-bounded-rsi-closeout")
    if not p1["claims"]["secondGenerationChangeDrivenByImprovedLoop"]:
        raise RuntimeError("P2 requires the P1 second-generation self-change evidence")
    plan = json.loads(PLAN_V5.read_text(encoding="utf-8"))
    promoted = {item["policyId"] for item in plan["promotedResearchPolicies"]}
    if not {"campaign_declared_evidence_v2", "capability_evidence_v1"} <= promoted:
        raise RuntimeError("P2 requires both P1 promoted research policies")

    corpus = load_record(args.fixture_dir / "corpus.json", expected_kind="ordivon.world-model-frontier-freshness-corpus")
    labels = load_record(args.fixture_dir / "evaluator-labels.json", expected_kind="ordivon.world-model-frontier-freshness-labels")
    if corpus["splitCounts"] != {"development": 7, "holdout": 3}:
        raise RuntimeError("P2 freshness split differs")

    campaign = write_record(
        args.output_dir / "campaign.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-campaign-manifest",
            "campaignId": "CEL-P2-FRONTIER-FRESHNESS-003",
            "generation": 3,
            "parentPlanRef": "research/experiments/experiment-loop-v0/plan-v5.json#CEL-R4-005",
            "question": "Can Computer distinguish a historically valid world-model observation from a current owner checkout without inferring a shared world-model change from revision movement alone?",
            "changeSurface": ["world_model_frontier_freshness_policy"],
            "forbiddenSurface": ["owner_facts", "owner_product_state", "shared_world_model_claims", "product_merge_or_deploy"],
            "policies": [item[0] for item in POLICIES],
            "corpusRef": str((args.fixture_dir / "corpus.json").relative_to(ROOT)),
            "evaluatorRef": str((args.fixture_dir / "evaluator-labels.json").relative_to(ROOT)),
            "developmentCount": 7,
            "holdoutCount": 3,
            "promotionBoundary": "computing_world_model_observation_method_only",
            "sourceRevision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        },
    )

    development = [evaluate(corpus, labels, "development", policy_id, policy) for policy_id, policy in POLICIES]
    admissible = [item for item in development if item["falseCurrent"] == 0 and item["falseStale"] == 0]
    admissible.sort(key=lambda item: (item["stateMismatch"], -item["correctState"], item["policyId"]))
    winner = admissible[0] if admissible else None
    decision = {
        "winnerPolicyId": winner["policyId"] if winner else None,
        "reason": "zero false-current/false-stale hard gate, then exact revision-relation state match" if winner else "no admissible candidate",
    }
    write_record(args.output_dir / "development-evaluation.json", {"schemaVersion": 1, "kind": "ordivon.cel-frontier-freshness-evaluation", "campaignDigest": campaign["integrity"]["payloadDigest"], "split": "development", "evaluations": development, "decision": decision})

    holdout = []
    disposition = "stop_no_winner"
    if winner is not None:
        policy = dict(POLICIES)[winner["policyId"]]
        evaluated = evaluate(corpus, labels, "holdout", winner["policyId"], policy)
        holdout.append(evaluated)
        if evaluated["falseCurrent"] == 0 and evaluated["falseStale"] == 0 and evaluated["stateMismatch"] == 0:
            disposition = "promote_third_generation_research_policy"
        else:
            disposition = "rollback_third_generation_candidate"
    write_record(args.output_dir / "holdout-evaluation.json", {"schemaVersion": 1, "kind": "ordivon.cel-frontier-freshness-evaluation", "campaignDigest": campaign["integrity"]["payloadDigest"], "split": "holdout", "evaluations": holdout})
    closeout = write_record(
        args.output_dir / "closeout.json",
        {
            "schemaVersion": 1,
            "kind": "ordivon.cel-campaign-closeout",
            "campaignId": campaign["campaignId"],
            "generation": 3,
            "developmentDecision": decision,
            "holdoutEvaluations": holdout,
            "disposition": disposition,
            "researchPolicyWinner": winner["policyId"] if disposition.startswith("promote") else None,
            "crossWorkloadTransfer": True,
            "evidenceFamily": "owner-native cross-project Git revision freshness rather than P0 Provider/Trial evidence",
            "automaticWorldModelRevision": False,
            "automaticProductPromotion": False,
            "meaning": "Revision movement creates review pressure and freshness state; it does not itself create a shared world-model claim.",
        },
    )
    print(json.dumps({"development": development, "holdout": holdout, "disposition": closeout["disposition"]}, sort_keys=True))
    return 0 if disposition == "promote_third_generation_research_policy" else 2


if __name__ == "__main__":
    raise SystemExit(main())
