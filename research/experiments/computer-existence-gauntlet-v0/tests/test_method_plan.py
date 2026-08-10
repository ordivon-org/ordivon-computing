from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class MethodPlanTests(unittest.TestCase):
 def setUp(self):
  self.corpus=json.loads((HERE/'fixtures/method-scenarios.json').read_text())
  self.oracle=json.loads((HERE/'fixtures/method-oracle.json').read_text())
  self.plan=json.loads((HERE/'method-plan-v1.json').read_text())
 def test_oracle_is_separate_from_candidate_visible_corpus(self):
  self.assertEqual(len(self.corpus['scenarios']),12); self.assertFalse(any('expected' in x for x in self.corpus['scenarios'])); self.assertEqual({x['id'] for x in self.corpus['scenarios']},set(self.oracle['labels']))
 def test_split_and_null_cases_are_frozen(self):
  self.assertEqual(sum(x['split']=='development' for x in self.corpus['scenarios']),8); self.assertEqual(sum(x['split']=='holdout' for x in self.corpus['scenarios']),4); self.assertEqual(self.oracle['labels']['null-pressure'],'no_new_experiment'); self.assertEqual(self.oracle['labels']['safe-observation'],'continue_experiment')
 def test_global_method_must_add_incremental_value(self):
  rule=self.plan['promotionRule']; self.assertIn('improves decision correctness on development',rule); self.assertIn('does not regress holdout',rule); self.assertIn('<=1.25 token ratio',rule); self.assertIn('tie in correctness with higher context cost',rule)
 def test_no_retention_tuning_after_valid_campaign(self):
  self.assertIn('no prompt/evaluator V2 tuning solely to retain the method',self.plan['stopRule'])
if __name__=='__main__':unittest.main()
