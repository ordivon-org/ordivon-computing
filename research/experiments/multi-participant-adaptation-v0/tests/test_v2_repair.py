from __future__ import annotations
import hashlib,json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class P4V2RepairTests(unittest.TestCase):
    def test_v2_preserves_frozen_scientific_artifacts(self):
        p=json.loads((HERE/"plan-v2.json").read_text())
        actual={rel:"sha256:"+hashlib.sha256((HERE/rel).read_bytes()).hexdigest() for rel in p["frozenArtifactDigests"]}
        self.assertEqual(actual,p["frozenArtifactDigests"])
        v1=json.loads((HERE/"plan-v1.json").read_text())
        self.assertEqual(p["multiPromotionRule"],v1["multiPromotionRule"])
        for key in ("sameProviderModelRequired","sameVisibleTaskRequired","sameIndependentVerifierRequired","sameJoinRuleRequired","branchEffectsAllowed","developmentScenarios","holdoutScenarios"):
            self.assertEqual(p["controls"][key],v1["controls"][key])
    def test_v2_repairs_only_provider_presentation_boundary(self):
        p=json.loads((HERE/"plan-v2.json").read_text())
        self.assertEqual(p["supersedes"],"MULTI-P4-001")
        self.assertEqual(p["controls"]["semanticCandidateSlotsPerGoalPerTreatment"],2)
        self.assertEqual(p["controls"]["maxProviderAttemptsPerCandidateSlot"],2)
        self.assertTrue(p["controls"]["providerPresentationRetryCountsTowardTokens"])
        self.assertFalse(p["presentationRepair"]["comparisonOutcomeFromV1Authorized"])
        self.assertTrue(p["presentationRepair"]["candidateSemanticsUnchanged"])
    def test_v2_runner_does_not_fabricate_assistant_history(self):
        source=(HERE/"run_live_p4_v2.py").read_text()
        self.assertNotIn("{'role':'assistant'",source)
        self.assertIn("priorCandidate",source)
        self.assertIn("visibleVerifier",source)
        self.assertIn("presentationAttempt",source)
        self.assertIn("providerAttempts",source)
    def test_v1_diagnosis_forbids_retrospective_win(self):
        d=json.loads((HERE/"evidence/live/evaluator-diagnosis.json").read_text())
        self.assertEqual(d["scientificDisposition"],"invalidate_competitive_comparison")
        self.assertFalse(d["retrospectiveRescoreAuthorized"])
        self.assertFalse(d["multiAdvantageClaimAuthorized"])
if __name__=="__main__": unittest.main()
