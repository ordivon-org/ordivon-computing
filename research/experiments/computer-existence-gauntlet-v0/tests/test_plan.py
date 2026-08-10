from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class PlanTests(unittest.TestCase):
 def test_every_feature_has_removal_attack_and_survival_evidence(self):
  d=json.loads((HERE/'feature-inventory.json').read_text()); self.assertGreaterEqual(len(d['features']),40)
  for f in d['features']:
   self.assertTrue(f['initialAttack']); self.assertTrue(f['minimumSurvivalEvidence']); self.assertTrue(f['paths'])
 def test_no_scalar_verdict(self):
  d=json.loads((HERE/'plan-v1.json').read_text()); self.assertEqual(d['verdicts'],['retain','narrow','localize','archive','delete','inconclusive']); self.assertNotIn('score',d)
 def test_control_is_first_wave(self):
  d=json.loads((HERE/'plan-v1.json').read_text()); self.assertEqual(d['waves'][0],'CONTROL')
if __name__=='__main__':unittest.main()
