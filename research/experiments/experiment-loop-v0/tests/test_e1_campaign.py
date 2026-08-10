from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from cel import canonical_digest

class E1CampaignTests(unittest.TestCase):
    def test_selection_self_change_survives_holdout(self) -> None:
        root = ROOT / "campaigns/cel-p1-selection-001"
        closeout = json.loads((root / "closeout.json").read_text())
        self.assertEqual(closeout["integrity"]["payloadDigest"], canonical_digest(closeout))
        self.assertEqual(closeout["disposition"], "promote_research_policy")
        self.assertEqual(closeout["researchPolicyWinner"], "campaign_declared_evidence_v2")
        development = json.loads((root / "development-evaluation.json").read_text())
        rows = {x["policyId"]: x for x in development["evaluations"]}
        self.assertEqual(rows["observation_always_required_v1"]["falseExclusions"], 18)
        self.assertEqual(rows["campaign_declared_evidence_v2"]["falseInclusions"], 0)
        self.assertEqual(rows["campaign_declared_evidence_v2"]["falseExclusions"], 0)
        holdout = json.loads((root / "holdout-evaluation.json").read_text())["evaluations"][0]
        self.assertEqual(holdout["total"], 5)
        self.assertEqual(holdout["correct"], 5)
        self.assertEqual(holdout["falseInclusions"], 0)
        self.assertEqual(holdout["falseExclusions"], 0)

    def test_plan_v3_promotes_only_research_policy(self) -> None:
        plan = json.loads((ROOT / "plan-v3.json").read_text())
        self.assertEqual(plan["integrity"]["payloadDigest"], canonical_digest(plan))
        self.assertEqual(plan["searchPolicy"]["selectionEligibilityPolicy"], "campaign_declared_evidence_v2")
        self.assertFalse(plan["decisions"]["automaticMergeAuthorized"])
        self.assertFalse(plan["decisions"]["automaticDeploymentAuthorized"])

if __name__ == "__main__":
    unittest.main()
