from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
RESEARCH=HERE.parents[1]
class C6CloseoutTests(unittest.TestCase):
 def test_v1_remains_invalid_without_rescore(self):
  d=json.loads((HERE/'evidence/live-v1/apparatus-diagnosis.json').read_text()); self.assertEqual(d['scientificDisposition'],'invalidate_competitive_comparison'); self.assertFalse(d['retrospectiveRescoreAuthorized']); self.assertFalse(d['pressureSelectionAdvantageClaimAuthorized'])
 def test_v2_is_final_and_does_not_promote(self):
  d=json.loads((HERE/'evidence/live-v2/final-diagnosis.json').read_text()); self.assertEqual(d['status'],'final_no_v3'); self.assertFalse(d['promotionRulePassed']); self.assertFalse(d['candidatePromoted']); self.assertEqual(d['scientificDisposition'],'reject_selective_pressure_triage_candidate_not_graduated'); self.assertFalse(d['comparativeSuperiorityClaimAuthorized'])
 def test_selection_failure_and_null_holdout_are_both_retained(self):
  d=json.loads((HERE/'c6-pressure-selection-closeout.json').read_text()); i=d['interpretation']; self.assertTrue(i['selectionFailureObserved']); self.assertTrue(i['contractAdherenceFailureObserved']); self.assertFalse(i['candidateValidDevelopmentTruePressureFound']); self.assertTrue(i['candidateValidHoldoutNullDecision']); self.assertEqual(i['developmentTruePressure'],'harness-rsi-p3')
 def test_c6_does_not_weaken_p2_or_authorize_infrastructure(self):
  d=json.loads((HERE/'c6-pressure-selection-closeout.json').read_text()); c=d['claims']; self.assertTrue(c['boundedRecursiveSelfReformFromP2StillSupported']); self.assertTrue(c['crossEvidenceFamilyTransferFromP2StillSupported']); self.assertFalse(c['autonomousOwnerPressureDiscoveryProven']); self.assertFalse(c['selectiveEvidencePressureTriageProven']); self.assertFalse(c['pressureDiscoveryDaemonAuthorized']); self.assertFalse(c['centralOwnerStateRegistryAuthorized']); self.assertFalse(c['newArchitectureCategoryAuthorized']); self.assertFalse(c['openEndedRSIProven']); self.assertFalse(d['rollback']['required'])
 def test_adaptation_question_is_deferred_m5(self):
  p=json.loads((RESEARCH/'portfolio.json').read_text()); q=next(x for x in p['questions'] if x['id']=='ANC-ADAPT-001'); self.assertEqual((q['status'],q['maturity'],q['priority'],q['disposition']),('deferred','M5','P1','defer')); self.assertIn('owner-pressure-discovery-v0/c6-pressure-selection-closeout.json',q['evidence'][-1]); self.assertIn('Do not build a pressure-discovery daemon',q['nextAction'])
 def test_reform_frontier_stops_after_c6(self):
  d=json.loads((RESEARCH/'computer-responsibility-map-v1.json').read_text()); by={x['step']:x for x in d['reformFrontier']}; self.assertEqual(list(by),['C1','C2','C3','C4','C5','C6']); self.assertTrue(all(x['status']=='completed' for x in d['reformFrontier'])); self.assertFalse(any(x['status']=='next' for x in d['reformFrontier'])); self.assertEqual(d['reformDisposition'],'stopped_waiting_for_new_owner_pressure'); self.assertEqual(by['C6']['record'],'research/experiments/owner-pressure-discovery-v0/c6-pressure-selection-closeout.json')
if __name__=='__main__': unittest.main()
