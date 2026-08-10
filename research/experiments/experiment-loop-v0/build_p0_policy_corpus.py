from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from cel import canonical_digest, write_record

ROOT = Path(__file__).resolve().parents[3]
P0 = ROOT / "research/experiments/p0-consumer-falsification-v0/evidence"
LIVE = P0 / "live"


def _split_rank(trajectory_id: str) -> int:
    return int(hashlib.sha256(trajectory_id.encode("utf-8")).hexdigest()[:16], 16)


def _common_claims() -> dict[str, bool]:
    return {
        "observation_complete": False,
        "configuration_exact": True,
        "independent_grader_complete": True,
        "no_unresolved_effect": True,
        "candidate_mutation_frozen": True,
    }


def _trajectory(
    *,
    trajectory_id: str,
    evidence_ref: str,
    validity: str,
    semantic_outcome: str,
    expected_eligible: bool,
    failure_attribution: str = "none",
    evidence_claims: dict[str, bool] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    claims = evidence_claims or _common_claims()
    trajectory = {
        "schemaVersion": 1,
        "kind": "ordivon.cel-policy-trajectory",
        "trajectoryId": trajectory_id,
        "split": "unassigned",
        "sourceEvidenceRef": evidence_ref,
        "validity": validity,
        "semanticOutcome": semantic_outcome,
        "failureAttribution": failure_attribution,
        "evidenceClaims": claims,
        "campaignRequiredEvidenceClaims": [
            "configuration_exact",
            "independent_grader_complete",
            "no_unresolved_effect",
            "candidate_mutation_frozen",
        ],
    }
    label = {
        "trajectoryId": trajectory_id,
        "expectedEligible": expected_eligible,
        "labelAuthority": "P0 retained trial/evaluator disposition",
    }
    return trajectory, label


def build() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectories: list[dict[str, Any]] = []
    labels: list[dict[str, Any]] = []

    for replicate in range(1, 6):
        path = LIVE / f"p0-a-live-r{replicate}.json"
        receipt = json.loads(path.read_text(encoding="utf-8"))
        for cell in receipt["cells"]:
            trajectory, label = _trajectory(
                trajectory_id=f"p0-a-r{replicate}-{cell['cellId'].lower()}",
                evidence_ref=str(path.relative_to(ROOT)),
                validity="valid" if cell["trialValid"] else "invalid",
                semantic_outcome="accepted" if cell["semanticAccepted"] else "rejected",
                expected_eligible=bool(cell["trialValid"]),
            )
            trajectories.append(trajectory)
            labels.append(label)

    for fixture in ("act", "hold"):
        for replicate in range(1, 4):
            path = LIVE / f"p0-b-{fixture}-r{replicate}.json"
            receipt = json.loads(path.read_text(encoding="utf-8"))
            for cell in receipt["cells"]:
                trajectory, label = _trajectory(
                    trajectory_id=f"p0-b-{fixture}-r{replicate}-{cell['treatment']}",
                    evidence_ref=str(path.relative_to(ROOT)),
                    validity="valid" if cell["trialValid"] else "invalid",
                    semantic_outcome="accepted" if cell["semanticAccepted"] else "rejected",
                    expected_eligible=bool(cell["trialValid"]),
                )
                trajectories.append(trajectory)
                labels.append(label)

    closeout_ref = "research/experiments/p0-consumer-falsification-v0/evidence/p0-live-closeout.json"
    diagnostics = (
        (
            "p0-diagnostic-provider-transport",
            "invalid",
            "not_reached",
            "infrastructure",
            {
                "observation_complete": False,
                "configuration_exact": True,
                "independent_grader_complete": False,
                "no_unresolved_effect": False,
                "candidate_mutation_frozen": True,
            },
        ),
        (
            "p0-diagnostic-budget-preflight",
            "invalid",
            "not_reached",
            "evaluator",
            {
                "observation_complete": False,
                "configuration_exact": False,
                "independent_grader_complete": False,
                "no_unresolved_effect": True,
                "candidate_mutation_frozen": True,
            },
        ),
        (
            "p0-diagnostic-validity-conflation",
            "unknown",
            "unknown",
            "evaluator",
            {
                "observation_complete": False,
                "configuration_exact": True,
                "independent_grader_complete": False,
                "no_unresolved_effect": True,
                "candidate_mutation_frozen": False,
            },
        ),
    )
    for trajectory_id, validity, outcome, attribution, claims in diagnostics:
        trajectory, label = _trajectory(
            trajectory_id=trajectory_id,
            evidence_ref=closeout_ref,
            validity=validity,
            semantic_outcome=outcome,
            expected_eligible=False,
            failure_attribution=attribution,
            evidence_claims=claims,
        )
        trajectories.append(trajectory)
        labels.append(label)

    trajectories.sort(key=lambda item: item["trajectoryId"])
    labels.sort(key=lambda item: item["trajectoryId"])
    holdout_ids = {
        item["trajectoryId"]
        for item in sorted(
            trajectories,
            key=lambda item: _split_rank(item["trajectoryId"]),
        )[:5]
    }
    for item in trajectories:
        item["split"] = (
            "holdout" if item["trajectoryId"] in holdout_ids else "development"
        )
    return trajectories, labels


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    trajectories, labels = build()
    output = args.output_dir
    corpus = {
        "schemaVersion": 1,
        "kind": "ordivon.cel-policy-trajectory-corpus",
        "corpusId": "CEL-P1-P0-POLICY-CORPUS-001",
        "source": "P0 current-revision live consumer falsification",
        "trajectoryCount": len(trajectories),
        "splitCounts": {
            "development": sum(item["split"] == "development" for item in trajectories),
            "holdout": sum(item["split"] == "holdout" for item in trajectories),
        },
        "trajectories": trajectories,
    }
    evaluator = {
        "schemaVersion": 1,
        "kind": "ordivon.cel-policy-evaluator-labels",
        "evaluatorId": "CEL-P1-P0-POLICY-EVALUATOR-001",
        "corpusDigest": canonical_digest(corpus),
        "labels": labels,
        "candidateVisible": False,
    }
    write_record(output / "trajectory-corpus-v1.json", corpus)
    write_record(output / "evaluator-labels-v1.json", evaluator)
    print(json.dumps({"trajectoryCount": len(trajectories), "splitCounts": corpus["splitCounts"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
