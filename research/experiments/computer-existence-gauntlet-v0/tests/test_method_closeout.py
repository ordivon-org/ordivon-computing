from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class MethodCloseoutTests(unittest.TestCase):
 def test_campaign_valid_and_global_method_does_not_survive(self):
  d=json.loads((HERE/'method-wave-v1-closeout.json').read_text()); self.assertTrue(d['validCampaign']); self.assertFalse(d['globalMethodSurvivalRulePassed']); self.assertGreater(d['globalToLocalTokenRatio'],2.0)
 def test_global_regresses_holdout(self):
  d=json.loads((HERE/'method-wave-v1-closeout.json').read_text()); m=d['metrics']['holdout']; self.assertLess(m['global-method-plus-local']['correct'],m['local-manifest']['correct'])
 def test_no_v2_retention_tuning(self):
  d=json.loads((HERE/'method-wave-v1-closeout.json').read_text()); self.assertTrue(any('No V2' in x for x in d['claimBoundary']))
if __name__=='__main__':unittest.main()
