from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from cel import canonical_digest

class E2CampaignTests(unittest.TestCase):
    def test_second_generation_self_change_survives_holdout(self) -> None:
        root = ROOT / "campaigns/cel-p1-prerequisite-002"
        closeout = json.loads((root / "closeout.json").read_text())
        self.assertEqual(closeout["integrity"]["payloadDigest"], canonical_digest(closeout))
        self.assertEqual(closeout["generation"], 2)
        self.assertEqual(closeout["disposition"], "promote_second_generation_research_policy")
        self.assertEqual(closeout["researchPolicyWinner"], "capability_evidence_v1")
        development = json.loads((root / "development-evaluation.json").read_text())
        rows = {x["policyId"]: x for x in development["evaluations"]}
        self.assertEqual(rows["named_phase_status_v1"]["falseBlock"], 1)
        self.assertEqual(rows["named_phase_status_v1"]["falseReady"], 0)
        self.assertEqual(rows["capability_evidence_v1"]["correct"], 5)
        self.assertEqual(rows["capability_evidence_v1"]["falseReady"], 0)
        self.assertEqual(rows["capability_evidence_v1"]["falseBlock"], 0)
        holdout = json.loads((root / "holdout-evaluation.json").read_text())["evaluations"][0]
        self.assertEqual(holdout["total"], 2)
        self.assertEqual(holdout["correct"], 2)
        self.assertEqual(holdout["falseReady"], 0)
        self.assertEqual(holdout["falseBlock"], 0)

    def test_plan_v4_retains_first_generation_and_no_product_authority(self) -> None:
        plan = json.loads((ROOT / "plan-v4.json").read_text())
        self.assertEqual(plan["integrity"]["payloadDigest"], canonical_digest(plan))
        self.assertEqual(plan["prerequisitePolicy"]["mode"], "capability_evidence_v1")
        ids = [x["policyId"] for x in plan["promotedResearchPolicies"]]
        self.assertIn("campaign_declared_evidence_v2", ids)
        self.assertIn("capability_evidence_v1", ids)
        self.assertFalse(plan["decisions"]["automaticMergeAuthorized"])
        self.assertFalse(plan["decisions"]["automaticDeploymentAuthorized"])
        self.assertEqual(plan["boundedRSIEvidence"]["claimLimit"], "bounded_recursive_self_improvement_evidence_not_open_ended_RSI")

if __name__ == "__main__":
    unittest.main()
