from __future__ import annotations
import json, pathlib, sys, unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from evaluator import evaluate_candidate, join_verified, source_gate
from host_coordination import exercise_host_coordination

class P4ApparatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus=json.loads((HERE/"fixtures/corpus.json").read_text())["scenarios"]
        cls.hidden=json.loads((HERE/"fixtures/evaluator-cases.json").read_text())["casesByScenario"]
        cls.refs=json.loads((HERE/"fixtures/reference-sources.json").read_text())["sources"]
    def test_corpus_is_six_three_and_hides_evaluator_cases(self):
        self.assertEqual(sum(s["split"]=="development" for s in self.corpus),6)
        self.assertEqual(sum(s["split"]=="holdout" for s in self.corpus),3)
        self.assertEqual(set(self.hidden),{s["scenarioId"] for s in self.corpus})
        self.assertTrue(all("hiddenCases" not in s for s in self.corpus))
    def test_reference_sources_pass_and_buggy_sources_are_falsifiable(self):
        for s in self.corpus:
            sid=s["scenarioId"]
            good=evaluate_candidate(s,self.refs[sid],self.hidden[sid])
            self.assertTrue(good["authoritative"]["allPassed"],sid)
            bad=evaluate_candidate(s,s["buggySource"],self.hidden[sid])
            self.assertFalse(bad["authoritative"]["allPassed"],sid)
    def test_source_gate_rejects_effectful_imports(self):
        ok,reason=source_gate("import os\ndef f(x): return x","f")
        self.assertFalse(ok); self.assertIn("forbidden-node",reason)
    def test_join_uses_verifier_acceptance_not_candidate_confidence(self):
        def c(cid,passed,total,changes):
            return {"candidateId":cid,"artifactDigest":"sha256:"+("a" if cid=="a" else "b")*64,"evaluation":{"authoritative":{"allPassed":passed==total,"passed":passed,"total":total},"changedLines":changes}}
        joined=join_verified([c("a",3,4,1),c("b",4,4,20)])
        self.assertTrue(joined["accepted"]); self.assertEqual(joined["selectedCandidateId"],"b")
    def test_host_multi_join_survives_partial_reopen(self):
        candidates=[]
        for cid,artifact_char,source_char in (("x","a","c"),("y","b","d")):
            src="def f(x):\n    return x\n"
            candidates.append({"candidateId":cid,"artifactDigest":"sha256:"+artifact_char*64,"sourceDigest":"sha256:"+source_char*64,"summary":"ok","evaluation":{"authoritative":{"allPassed":cid=="x","passed":2 if cid=="x" else 1,"total":2},"changedLines":1}})
        join={"accepted":True,"selectedArtifactDigest":candidates[0]["artifactDigest"],"selectedCandidateId":"x","acceptedCandidateCount":1,"candidateCount":2,"bestAuthoritativePassed":2,"authoritativeTotal":2}
        receipt=exercise_host_coordination(scenario_id="fixture",treatment="multi-independent",candidates=candidates,join=join)
        self.assertEqual(receipt["taskCount"],2); self.assertEqual(receipt["participantCount"],2)
        self.assertFalse(receipt["responsibilityAmbiguous"]); self.assertEqual(receipt["branchEffectIntentCount"],0)
        self.assertTrue(receipt["staleSnapshotBlocked"]); self.assertTrue(receipt["partialApplyRecoveryPassed"])
    def test_rejected_verification_cannot_advance_task(self):
        c={"candidateId":"x","artifactDigest":"sha256:"+"a"*64,"sourceDigest":"sha256:"+"b"*64,"summary":"bad","evaluation":{"authoritative":{"allPassed":False,"passed":0,"total":2},"changedLines":1}}
        join={"accepted":False,"selectedArtifactDigest":c["artifactDigest"],"selectedCandidateId":"x","acceptedCandidateCount":0,"candidateCount":1,"bestAuthoritativePassed":0,"authoritativeTotal":2}
        receipt=exercise_host_coordination(scenario_id="reject",treatment="single-reflect",candidates=[c,c],join=join)
        self.assertTrue(receipt["rejectedAdvanceBlocked"]); self.assertTrue(receipt["partialApplyRecoveryPassed"])
    def test_plan_does_not_pre_authorize_multi_infrastructure(self):
        p=json.loads((HERE/"plan-v1.json").read_text()); adm=p["infrastructureAdmission"]
        self.assertTrue(adm["existingHostGoalCoordinatorFirst"])
        self.assertTrue(all(v is False for k,v in adm.items() if k!="existingHostGoalCoordinatorFirst"))
        self.assertEqual(p["controls"]["modelCallsPerGoalPerTreatment"],2)
if __name__=="__main__": unittest.main()
