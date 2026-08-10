from __future__ import annotations
from typing import Any
CLASSES={'shared_method_pressure','shared_knowledge_candidate','confirming_owner_evidence','owner_local_gap','churn'}
def evaluate(assessment:dict[str,Any],cards:list[dict[str,Any]],oracle:dict[str,Any],split:str)->dict[str,Any]:
 expected=oracle['classes']; submitted={x.get('cardId'):x for x in assessment.get('cards',[])}
 card_rows=[]; false_promotions=0; correct=0
 for card in cards:
  cid=card['cardId']; got=submitted.get(cid,{}); exp=expected[cid]
  class_ok=got.get('pressureClass')==exp['pressureClass']; req_ok=got.get('requiresComputerExperiment') is exp['requiresComputerExperiment']; target_ok=got.get('targetResponsibilityId')==exp['targetResponsibilityId']
  row_ok=class_ok and req_ok and target_ok; correct+=int(row_ok)
  if got.get('requiresComputerExperiment') is True and exp['requiresComputerExperiment'] is False:false_promotions+=1
  card_rows.append({'cardId':cid,'correct':row_ok,'classCorrect':class_ok,'experimentFlagCorrect':req_ok,'targetCorrect':target_ok})
 sel=assessment.get('selection',{}); sexp=oracle['selection'][split]
 decision=sel.get('selectedCardId')==sexp['selectedCardId'] and sel.get('action')==sexp['action'] and sel.get('targetResponsibilityId')==sexp['targetResponsibilityId']
 falsifier_ok=True
 if split=='development':
  f=sel.get('falsifier',{}); contract=oracle['developmentFalsifierContract']; falsifier_ok=all(f.get(k)==v for k,v in contract.items()) and isinstance(f.get('hypothesis'),str) and bool(f.get('hypothesis','').strip())
  decision=decision and falsifier_ok
 else:
  f=sel.get('falsifier',{}); falsifier_ok=all(f.get(k)=='none' for k in ('hypothesis','baseline','oracle','holdout','promotionBoundary','deletionOutcome')); decision=decision and falsifier_ok
 return {'cardRows':card_rows,'cardsCorrect':correct,'cardsTotal':len(cards),'classificationAccuracy':correct/len(cards) if cards else 0.0,'falsePromotions':false_promotions,'decisionCorrect':decision,'falsifierCorrect':falsifier_ok}
