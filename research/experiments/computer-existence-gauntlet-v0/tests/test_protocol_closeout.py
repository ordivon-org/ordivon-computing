from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class ProtocolCloseoutTests(unittest.TestCase):
 def test_semantic_state_deletion_passed_current_targets(self):
  d=json.loads((HERE/'evidence/protocol-wave-v1.json').read_text()); a=next(x for x in d['ablations'] if x['featureId']=='PROTO-06'); self.assertEqual((a['hostTests'],a['harnessTests'],a['gameTests']),('99/99','220/220','7/7'))
 def test_effect_and_binding_are_localization_not_semantic_deletion_claims(self):
  d=json.loads((HERE/'protocol-wave-v1-closeout.json').read_text()); self.assertIn('localize candidate',d['preliminaryDispositions']['PROTO-02']); self.assertIn('localize candidate',d['preliminaryDispositions']['PROTO-03'])
if __name__=='__main__':unittest.main()
