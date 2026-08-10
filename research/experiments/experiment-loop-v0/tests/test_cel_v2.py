from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from build_p0_policy_corpus import build
from cel import canonical_digest, decide_eligibility, load_record, seal, select_policy


class CELV2Tests(unittest.TestCase):
    def test_plan_v2_recompiles_capabilities_not_phase_names(self) -> None:
        plan = json.loads((ROOT / "plan-v2.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["planId"], "CEL-R4-002")
        self.assertEqual(plan["status"], "ready_for_minimal_self_customer")
        self.assertFalse(plan["prerequisitePolicy"]["phaseNameStatusIsAuthority"])
        self.assertTrue(all(item["satisfied"] for item in plan["prerequisites"]))
        rendered = json.dumps(plan["prerequisites"], sort_keys=True)
        self.assertNotIn("p0_passed_and_p1_core_passed", rendered)
        self.assertNotIn("deterministic_smoke_and_repeated_native_baseline_passed", rendered)
        self.assertEqual(plan["integrity"]["payloadDigest"], canonical_digest(plan))

    def test_p0_corpus_is_25_with_20_5_split(self) -> None:
        trajectories, labels = build()
        self.assertEqual(len(trajectories), 25)
        self.assertEqual(len(labels), 25)
        self.assertEqual(sum(item["split"] == "development" for item in trajectories), 20)
        self.assertEqual(sum(item["split"] == "holdout" for item in trajectories), 5)
        self.assertEqual(
            {item["trajectoryId"] for item in trajectories},
            {item["trajectoryId"] for item in labels},
        )

    def test_selection_policy_separates_observation_from_campaign_evidence(self) -> None:
        trajectories, labels = build()
        label_by_id = {item["trajectoryId"]: item for item in labels}
        valid = next(item for item in trajectories if item["validity"] == "valid")
        invalid = next(item for item in trajectories if item["validity"] != "valid")
        baseline = {
            "policyId": "baseline",
            "mode": "observation_always_required_v1",
            "requiredClaims": ["observation_complete", "configuration_exact"],
        }
        candidate = {"policyId": "candidate", "mode": "campaign_declared_evidence_v2"}
        self.assertFalse(decide_eligibility(valid, baseline).eligible)
        self.assertTrue(label_by_id[valid["trajectoryId"]]["expectedEligible"])
        self.assertTrue(decide_eligibility(valid, candidate).eligible)
        self.assertFalse(decide_eligibility(invalid, candidate).eligible)
        self.assertFalse(label_by_id[invalid["trajectoryId"]]["expectedEligible"])

    def test_hard_gate_policy_selection_rejects_false_inclusion(self) -> None:
        decision = select_policy(
            [
                {
                    "policyId": "unsafe",
                    "falseInclusions": 1,
                    "falseExclusions": 0,
                    "correct": 24,
                },
                {
                    "policyId": "safe",
                    "falseInclusions": 0,
                    "falseExclusions": 1,
                    "correct": 24,
                },
            ]
        )
        self.assertEqual(decision["winnerPolicyId"], "safe")

    def test_record_integrity_round_trip(self) -> None:
        value = seal({"schemaVersion": 1, "kind": "fixture", "value": 1})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertEqual(load_record(path), value)


if __name__ == "__main__":
    unittest.main()
