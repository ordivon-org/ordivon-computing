from __future__ import annotations
import json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class P3SkillCloseoutTests(unittest.TestCase):
    def test_first_campaign_is_retained_but_invalid_for_selection(self):
        p=json.loads((ROOT/"evidence/live-ablation/evaluator-diagnosis.json").read_text())
        self.assertEqual(p["scientificDisposition"],"invalidate_selection_evaluator_contract")
        self.assertFalse(p["retrospectiveRescoreAuthorized"])
        self.assertEqual(p["rawTrajectoryCount"],25)
    def test_repaired_campaign_rejects_skill(self):
        d=json.loads((ROOT/"evidence/live-ablation-v2/development.json").read_text())
        h=json.loads((ROOT/"evidence/live-ablation-v2/holdout.json").read_text())
        self.assertEqual(d["winner"],"baseline")
        self.assertEqual(d["metrics"]["baseline"]["accepted"],8)
        self.assertEqual(d["metrics"]["skill"]["accepted"],6)
        self.assertGreater(d["metrics"]["skill"]["tokens"],d["metrics"]["baseline"]["tokens"])
        self.assertEqual(sum(r["score"]["accepted"] for r in h["rows"]),3)
        self.assertFalse(h["holdoutPassed"])
    def test_candidate_never_becomes_execution_authority(self):
        p=json.loads((ROOT/"plan-v1.json").read_text())
        self.assertFalse(p["candidateSkill"]["promotionAuthorized"])
        self.assertFalse(p["candidateSkill"]["executionAuthorityOwned"])
        self.assertFalse(p["admissionControls"]["newSkillRepositoryAuthorized"])
        self.assertFalse(p["admissionControls"]["skillRuntimeAuthorized"])
        self.assertFalse(p["decision"]["skillCompilationProven"])
        self.assertFalse(p["decision"]["rollbackRequired"])
    def test_p3_closeout_keeps_rsi_claim_bounded(self):
        p=json.loads((ROOT/"p3-skill-closeout.json").read_text())
        self.assertEqual(p["status"],"complete_negative_skill_falsification")
        self.assertFalse(p["claims"]["candidateSkillPromoted"])
        self.assertFalse(p["claims"]["dynamicSkillCompilationProven"])
        self.assertFalse(p["claims"]["genericSkillLayerAuthorized"])
        self.assertFalse(p["claims"]["openEndedRSIProven"])
        self.assertFalse(p["claims"]["p2CrossEvidenceRSIEvidenceInvalidated"])
    def test_rejected_candidate_is_evidence_only(self):
        p=json.loads((ROOT/"skill/reconcile-before-redispatch.disposition.json").read_text())
        self.assertEqual(p["status"],"rejected_not_promoted")
        self.assertFalse(p["activeCapability"])
        self.assertFalse(p["executionAuthority"])
if __name__=="__main__": unittest.main()
