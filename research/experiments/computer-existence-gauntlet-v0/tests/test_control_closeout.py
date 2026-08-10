from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class ControlCloseoutTests(unittest.TestCase):
 def test_semantic_self_defense_failed(self):
  d=json.loads((HERE/'control-wave-v1-closeout.json').read_text()); self.assertEqual(d['headline']['semanticMutantsKilled'],0); self.assertEqual(d['headline']['semanticMutantsTotal'],5); self.assertTrue(d['headline']['positiveControlKilled'])
 def test_map_relations_did_not_earn_current_mechanical_authority(self):
  d=json.loads((HERE/'evidence/control-deletion-v1.json').read_text()); a=next(x for x in d['attacks'] if x['attackId']=='D01-map-relations-delete'); self.assertEqual(a['removedLines'],248); self.assertIn('check_research_portfolio',a['checksPassed'])
 def test_no_blanket_checker_deletion_claim(self):
  d=json.loads((HERE/'control-wave-v1-closeout.json').read_text()); self.assertTrue(any('Do not delete every checker' in x for x in d['forbiddenConclusions']))
if __name__=='__main__':unittest.main()
