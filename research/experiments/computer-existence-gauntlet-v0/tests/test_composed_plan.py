from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class ComposedPlanTests(unittest.TestCase):
 def test_shadow_does_not_cross_owner_write_boundary(self):
  d=json.loads((HERE/'composed-plan-v1.json').read_text()); self.assertTrue(any('Host owner admission' in x for x in d['deliberatelyNotApplied'])); self.assertIn('does not authorize cross-owner localization',d['claimBoundary'])
 def test_shadow_requires_product_consumers_and_git_recovery(self):
  d=json.loads((HERE/'composed-plan-v1.json').read_text()); a=' '.join(d['acceptance']); self.assertIn('Host protocol-related',a); self.assertIn('Harness protocol-related',a); self.assertIn('Game host-contract',a); self.assertIn('recoverable',a)
if __name__=='__main__':unittest.main()
