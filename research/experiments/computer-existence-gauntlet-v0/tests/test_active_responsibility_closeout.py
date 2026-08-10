from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class ActiveResponsibilityTests(unittest.TestCase):
 def test_mass_ablation_removes_large_apparatus_but_keeps_current_checks(self):
  d=json.loads((HERE/'evidence/active-tree-wave-v1.json').read_text()); a=d['massAblation']; self.assertGreater(a['removedLines'],50000); self.assertEqual(a['extractedCurrentUtility']['lines'],143); self.assertIn('freshness-operator',a['currentChecksPassed'])
 def test_all_responsibilities_have_existential_verdicts(self):
  d=json.loads((HERE/'responsibility-wave-v1.json').read_text()); self.assertEqual(len(d['rows']),18); self.assertEqual({x['responsibilityId'] for x in d['rows']},{f'CR-{i:02d}' for i in range(1,19)})
 def test_retained_invariant_does_not_retain_apparatus(self):
  d=json.loads((HERE/'responsibility-wave-v1.json').read_text()); self.assertIn('does not retain',d['summary']['note'])
if __name__=='__main__':unittest.main()
