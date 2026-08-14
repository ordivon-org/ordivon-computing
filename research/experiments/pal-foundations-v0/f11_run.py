from __future__ import annotations
import argparse,json,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
ACTIONS=['PRESERVE_OPTION','DO_NOT_CARRY']
SCHEMA={'type':'object','additionalProperties':False,'properties':{'decision':{'type':'string','enum':ACTIONS},'currentGoalStatus':{'type':'string'},'optionCarrier':{'type':'string'},'reopenTrigger':{'type':'string'},'reason':{'type':'string'}},'required':['decision','currentGoalStatus','optionCarrier','reopenTrigger','reason']}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def lens(t):
 if t=='greedy_current': return 'POLICY: Optimize only current declared-objective/current-consumer value. If no current justified use remains, choose DO_NOT_CARRY. Ordinary documentary/Git archival is always available and does not count as preserving an option.'
 return 'POLICY: Separate current success from future option value. Choose PRESERVE_OPTION only when a SPECIFIC reusable capability/method/asset can be kept dormant or cheaply reacquirable at bounded carrying cost, losing it would make plausible adjacent future work materially harder, and visible evidence supports such adjacency. Do not preserve invalid, high-carry, authority-confused, or easily reacquired candidates merely because future value can be imagined. Ordinary archival alone is not PRESERVE_OPTION.'
def prompt(c,t): return 'You are making a retention decision at the stated historical/current decision point. You do NOT know later outcomes. Do not treat future historical success as known. '+lens(t)+'\n\nCASE:\n'+c['packet']+'\n\nReturn exactly one structured decision.'
def one(c,t,model,rep,secret):
 pr=prompt(c,t); settings=replace(DeepSeekSettings.from_secret_file(secret),model=model,max_output_tokens=700); now=time.time_ns()//1_000_000; rid=f"harness-run:pal-f11:{c['caseId']}:{t}:{model}:{rep}:{now}"; comp={'mode':'structured-result-v1','resultKind':'pal-f11-option-retention','resultSchema':SCHEMA}; contract=HarnessRunContract(harness_run_id=rid,harness_implementation_id='ordivon-harness@pal-f11',caller_id='caller:ordivon-computing-pal',caller_run_ref=f"{c['caseId']}|{t}|{model}|{rep}",objective_ref=ref(f"objective:{c['caseId']}",'objective',{'case':c['caseId']}),context_refs=(ref(f"context:{c['caseId']}:{t}:{rep}",'context',{'prompt':pr}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=65536,max_wall_time_ms=90000,max_total_tokens=16000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=comp,system_manifest_ref=ref(f"system:{c['caseId']}:{t}:{model}",'system-manifest',{'experiment':'PAL-F11','model':model,'treatment':t}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix='ordivon-pal-f11-') as sr:
  run=HarnessAgentRun.create(sr,contract,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); st=time.monotonic(); ex=run.run(({'role':'user','content':pr},)); elapsed=round((time.monotonic()-st)*1000); conc=ex.loop_result.conclusion; dec=None if conc is None else decode_structured_completion_result(contract,conc); valid=isinstance(dec,dict) and dec.get('decision') in ACTIONS and all(isinstance(dec.get(k),str) for k in ['currentGoalStatus','optionCarrier','reopenTrigger','reason']); term=ex.terminal_result
  return {'caseId':c['caseId'],'split':c['split'],'treatment':t,'model':model,'replica':rep,'runId':rid,'stopCode':ex.loop_result.stop_code.value,'modelCalls':ex.loop_result.model_calls,'usage':ex.loop_result.usage,'elapsedMs':elapsed,'result':dec,'valid':valid,'decision':dec.get('decision') if valid else None,'oracle':c['oracle'],'exactCorrect':bool(valid and dec.get('decision')==c['oracle']),'receiptDigest':None if term is None else term.receipt.digest}
def validate():
 d=json.load(open(ROOT/'f11-cases-v0.json')); assert len(d['cases'])==14; assert sum(c['oracle']=='PRESERVE_OPTION' for c in d['cases'])==7; assert sum(c['oracle']=='DO_NOT_CARRY' for c in d['cases'])==7; assert sum(c['split']=='development' for c in d['cases'])==7; assert sum(c['split']=='holdout' for c in d['cases'])==7; return {'caseCount':14,'caseDigest':canonical_digest(d),'schemaDigest':canonical_digest(SCHEMA)}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--model',choices=['deepseek-v4-flash','deepseek-v4-pro']); ap.add_argument('--replicas',type=int,default=2); ap.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); ap.add_argument('--output'); ap.add_argument('--validate-only',action='store_true'); a=ap.parse_args(); v=validate()
 if a.validate_only: print(json.dumps(v,indent=2)); return
 if not a.model or not a.output: ap.error('--model and --output required')
 doc=json.load(open(ROOT/'f11-cases-v0.json')); rows=[]; out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
 def persist():
  e={'schemaVersion':1,'kind':'ordivon.computing.pal-f11-provider-campaign','model':a.model,'replicas':a.replicas,'caseDigest':canonical_digest(doc),'schemaDigest':canonical_digest(SCHEMA),'rows':rows}; out.write_text(json.dumps(e,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); return e
 persist(); orders={1:['greedy_current','option_aware'],2:['option_aware','greedy_current']}
 for c in doc['cases']:
  for rep in range(1,a.replicas+1):
   for t in orders[rep]:
    try:r=one(c,t,a.model,rep,Path(a.secret))
    except Exception as exc:r={'caseId':c['caseId'],'split':c['split'],'treatment':t,'model':a.model,'replica':rep,'runId':None,'stopCode':'provider_or_recovery_exception','modelCalls':None,'usage':None,'elapsedMs':None,'result':None,'valid':False,'decision':None,'oracle':c['oracle'],'exactCorrect':False,'receiptDigest':None,'errorType':type(exc).__name__,'error':str(exc)[:500]}
    rows.append(r); persist(); print(json.dumps({'case':r['caseId'],'model':a.model,'replica':rep,'treatment':t,'valid':r['valid'],'decision':r['decision'],'oracle':r['oracle'],'correct':r['exactCorrect'],'errorType':r.get('errorType')},ensure_ascii=False),flush=True)
 e=persist(); print(json.dumps({'output':str(out),'rows':len(rows),'digest':canonical_digest(e)},indent=2))
if __name__=='__main__': main()
