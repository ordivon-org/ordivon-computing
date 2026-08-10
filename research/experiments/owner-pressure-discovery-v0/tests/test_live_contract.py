from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
from run_live_pressure_discovery import SelectiveBridge,instruction,validate_assessment,FALSIFIER_ENUMS
from ordivon_harness.domain_tools import AgentToolCall
class ContractTests(unittest.TestCase):
 def setUp(self):
  self.cards=json.loads((HERE/'fixtures/cards.json').read_text())['cards']
 def test_candidate_initial_context_has_metadata_not_evidence_body(self):
  cards=[x for x in self.cards if x['split']=='development']; text=instruction('development',cards,include_evidence=False)
  self.assertIn('harness-rsi-p3',text); self.assertIn(cards[0]['evidenceDigest'],text); self.assertNotIn(cards[0]['evidence'][:500],text); self.assertNotIn('hidden-oracle',text); self.assertNotIn('requiresComputerExperiment": true',text)
 def test_inspection_limit_fails_closed(self):
  cards=[x for x in self.cards if x['split']=='holdout']; bridge=SelectiveBridge(cards,2)
  for i in range(2):
   bridge.execute(AgentToolCall(tool_call_id=f'call:{i}',name='inspect_owner_evidence',arguments={'cardId':cards[i]['cardId']}),step_id=f'step:{i}')
  with self.assertRaisesRegex(ValueError,'limit exceeded'):
   bridge.execute(AgentToolCall(tool_call_id='call:3',name='inspect_owner_evidence',arguments={'cardId':cards[2]['cardId']}),step_id='step:3')
 def test_null_selection_cannot_hide_falsifier(self):
  cards=[x for x in self.cards if x['split']=='holdout']; assessment={'cards':[{'cardId':c['cardId'],'pressureClass':'churn','requiresComputerExperiment':False,'targetResponsibilityId':'none','reason':'bounded'} for c in cards],'selection':{'selectedCardId':'none','action':'no_new_computer_experiment','targetResponsibilityId':'none','falsifier':{'hypothesis':'secret experiment',**FALSIFIER_ENUMS}},'summary':'x'}
  with self.assertRaisesRegex(ValueError,'null selection'):
   validate_assessment(assessment,cards)
if __name__=='__main__':unittest.main()
