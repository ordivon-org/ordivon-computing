from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
from evaluator import evaluate
class ApparatusTests(unittest.TestCase):
 def setUp(self):
  self.cards=json.loads((HERE/'fixtures/cards.json').read_text())['cards']; self.oracle=json.loads((HERE/'fixtures/oracle.json').read_text())
 def test_split_is_disjoint_and_holdout_is_null(self):
  d={x['cardId'] for x in self.cards if x['split']=='development'}; h={x['cardId'] for x in self.cards if x['split']=='holdout'}; self.assertFalse(d&h); self.assertEqual(len(d),6); self.assertEqual(len(h),4); self.assertEqual(self.oracle['selection']['holdout']['selectedCardId'],'none')
 def test_only_development_harness_requires_new_computer_experiment(self):
  positives=[k for k,v in self.oracle['classes'].items() if v['requiresComputerExperiment']]; self.assertEqual(positives,['harness-rsi-p3'])
 def test_perfect_assessment_scores_perfect(self):
  for split in ('development','holdout'):
   cards=[x for x in self.cards if x['split']==split]; rows=[]
   for c in cards:
    o=self.oracle['classes'][c['cardId']]; rows.append({'cardId':c['cardId'],**o,'reason':'oracle fixture'})
   s=self.oracle['selection'][split]; f={'hypothesis':'bounded pressure selection'}
   if split=='development':f.update(self.oracle['developmentFalsifierContract'])
   else:f.update({k:'none' for k in ('baseline','oracle','holdout','promotionBoundary','deletionOutcome')}); f['hypothesis']='none'
   a={'cards':rows,'selection':{**s,'falsifier':f},'summary':'x'}; ev=evaluate(a,cards,self.oracle,split); self.assertTrue(ev['decisionCorrect']); self.assertEqual(ev['classificationAccuracy'],1.0); self.assertEqual(ev['falsePromotions'],0)
if __name__=='__main__':unittest.main()
