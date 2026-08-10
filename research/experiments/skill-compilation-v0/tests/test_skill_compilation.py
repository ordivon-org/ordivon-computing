from __future__ import annotations
import json, pathlib, sys, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from skill_compiler import compile_candidates
class SkillCompilationTests(unittest.TestCase):
    def setUp(self):
        self.discovery=json.loads((ROOT/"fixtures/discovery-incidents.json").read_text())
    def test_mechanical_source_landing_is_rejected_as_skill(self):
        result=compile_candidates(self.discovery)
        self.assertEqual(result["sourceLanding"]["admission"],"rejected")
        self.assertIn("git_runtime",result["sourceLanding"]["reason"])
    def test_recovery_candidate_requires_repeated_cross_operation_evidence(self):
        result=compile_candidates(self.discovery)
        skill=result["recoverySkill"]
        self.assertIsNotNone(skill)
        self.assertIn("durable_exec",skill["operationClasses"])
        self.assertIn("workspace_mutate",skill["operationClasses"])
        self.assertIn("host_checkpoint",skill["operationClasses"])
        self.assertIn("external_effect_inside_exec",skill["operationClasses"])
    def test_skill_does_not_own_execution_or_publication(self):
        skill=compile_candidates(self.discovery)["recoverySkill"]
        self.assertEqual(skill["executionOwner"],"existing_Tool_Runtime_Host_or_domain_authority")
        self.assertIn("create_new_execution_authority",skill["forbidden"])
        self.assertIn("blind_redispatch",skill["forbidden"])
    def test_skill_disappears_without_repeated_evidence(self):
        d=json.loads(json.dumps(self.discovery)); d["actualRuntimeEvidence"]=d["actualRuntimeEvidence"][:1]
        self.assertIsNone(compile_candidates(d)["recoverySkill"])
    def test_fixture_split_is_10_5(self):
        s=json.loads((ROOT/"fixtures/recovery-scenarios.json").read_text())["scenarios"]
        self.assertEqual(sum(x["split"]=="development" for x in s),10)
        self.assertEqual(sum(x["split"]=="holdout" for x in s),5)
        self.assertNotEqual({x["id"] for x in s if x["split"]=="development"},{x["id"] for x in s if x["split"]=="holdout"})
if __name__=="__main__": unittest.main()
