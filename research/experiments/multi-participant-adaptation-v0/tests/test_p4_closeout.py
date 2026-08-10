from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
RESEARCH=HERE.parents[1]
class P4CloseoutTests(unittest.TestCase):
    def test_v2_is_valid_but_fails_preregistered_multi_promotion(self):
        p=json.loads((HERE/"evidence/live-v2/closeout.json").read_text())
        self.assertTrue(p["validCampaign"])
        self.assertEqual(p["acceptedGoalGain"],{"development":2,"holdout":0,"combined":2})
        self.assertFalse(p["multiPromotionRulePassed"])
        self.assertEqual(p["disposition"],"reject_generic_multi_agent_advantage")
        self.assertLess(p["tokenRatioMultiToBaseline"],1.0)
        for split in ("developmentMetrics","holdoutMetrics"):
            for treatment in ("single-reflect","multi-independent"):
                self.assertEqual(p[split][treatment]["invalidScenarios"],0)
                self.assertEqual(p[split][treatment]["presentationCorrections"],0)
    def test_v1_never_becomes_comparative_evidence(self):
        d=json.loads((HERE/"evidence/live/evaluator-diagnosis.json").read_text())
        self.assertEqual(d["scientificDisposition"],"invalidate_competitive_comparison")
        self.assertFalse(d["retrospectiveRescoreAuthorized"]); self.assertFalse(d["multiAdvantageClaimAuthorized"])
    def test_closeout_separates_error_diversity_from_generic_superiority(self):
        p=json.loads((HERE/"p4-multi-closeout.json").read_text())
        self.assertTrue(p["interpretation"]["developmentMultiSignal"])
        self.assertFalse(p["interpretation"]["holdoutMultiSuperiority"])
        self.assertTrue(p["interpretation"]["errorDecorrelationObserved"])
        self.assertFalse(p["claims"]["genericMultiAgentCognitiveAdvantageProven"])
        self.assertFalse(p["claims"]["crossWorkloadMultiAdvantageProven"])
        self.assertFalse(p["claims"]["openEndedRSIProven"])
    def test_existing_host_coordination_is_sufficient_for_minimum_pattern(self):
        p=json.loads((HERE/"p4-multi-closeout.json").read_text()); c=p["coordination"]
        self.assertTrue(c["existingHostGoalCoordinatorSufficientForMinimumPattern"])
        self.assertEqual(c["treatmentGoalsExercised"],18); self.assertEqual(c["acceptedTreatmentGoals"],14)
        self.assertEqual(c["branchEffectIntents"],0); self.assertEqual(c["responsibilityAmbiguities"],0)
        self.assertTrue(c["allTreatmentRecoveryPathsPassed"]); self.assertTrue(c["artifactBindingSmokePassed"])
        self.assertFalse(c["newCoordinationPrimitiveUsed"])
        for key in ("newMultiAgentFrameworkAuthorized","newSchedulerAuthorized","newMessageBusAuthorized","newOrganizationLayerAuthorized","newParticipantRegistryAuthorized"):
            self.assertFalse(p["claims"][key])
    def test_artifact_binding_smoke_is_revision_fenced_and_recoverable(self):
        p=json.loads((HERE/"evidence/artifact-binding-smoke.json").read_text())
        self.assertEqual(p["taskCount"],2); self.assertEqual(p["participantCount"],2)
        self.assertTrue(p["initialSnapshotStaleAfterArtifactBinding"]); self.assertTrue(p["candidateBoundSnapshotStaleAfterFirstResult"])
        self.assertTrue(p["partialApplyReopenPassed"]); self.assertTrue(p["allFinalRevisionsAdvanced"]); self.assertTrue(p["taskEventsCarryVerification"])
        self.assertFalse(p["newCoordinationPrimitiveUsed"])
    def test_portfolio_moves_multi_to_deferred_m4_without_advancing_adapt(self):
        p=json.loads((RESEARCH/"portfolio.json").read_text()); multi=next(q for q in p["questions"] if q["id"]=="ANC-MULTI-001"); adapt=next(q for q in p["questions"] if q["id"]=="ANC-ADAPT-001")
        self.assertEqual((multi["status"],multi["maturity"],multi["priority"]),("deferred","M4","P2"))
        self.assertEqual(adapt["maturity"],"M5"); self.assertIn("category-driven",adapt["nextAction"])
    def test_no_rollback_is_required_without_promotion(self):
        p=json.loads((HERE/"p4-multi-closeout.json").read_text())
        self.assertFalse(p["rollback"]["required"]); self.assertFalse(p["claims"]["newMultiAgentFrameworkAuthorized"])
if __name__=="__main__": unittest.main()
