from __future__ import annotations
import json,pathlib,unittest,collections
HERE=pathlib.Path(__file__).resolve().parents[1]
class FinalCloseoutTests(unittest.TestCase):
 def setUp(self): self.d=json.loads((HERE/'existence-gauntlet-v1-closeout.json').read_text())
 def test_all_47_features_receive_exact_verdict(self):
  self.assertEqual(len(self.d['rows']),47); self.assertEqual(len({x['featureId'] for x in self.d['rows']}),47); self.assertEqual(set(x['verdict'] for x in self.d['rows']),{'retain','narrow','localize','archive','delete','inconclusive'})
 def test_composed_contraction_passed_and_is_not_applied_in_audit(self):
  h=self.d['headline']; self.assertTrue(h['composedAllChecksPassed']); self.assertTrue(h['composedAllHistoryRecoveryPassed']); self.assertGreater(h['composedRemovedLines'],50000); self.assertTrue(self.d['implementationBoundary']['auditDidNotApplyMassDeletionToSource'])
 def test_rsi_claim_remains_bounded(self):
  r=self.d['rsiInterpretation']; self.assertTrue(r['boundedRecursiveSelfReformStillSupported']); self.assertFalse(r['openEndedRSIProven']); self.assertFalse(r['autonomousPressureSelectionProven'])
 def test_core_is_not_deleted_without_direct_ablation(self):
  row=next(x for x in self.d['rows'] if x['featureId']=='CTRL-01'); self.assertEqual(row['verdict'],'inconclusive')
if __name__=='__main__':unittest.main()
