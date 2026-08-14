from __future__ import annotations
import argparse,json,tempfile,time
from dataclasses import replace
from pathlib import Path
from typing import Any
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
DECISIONS=['RETAIN_METHOD','RETAIN_ON_DEMAND','CONDITIONAL','DEFER','REJECT','PROMOTE_OWNER_UTILITY']
STATIC='''Reusable infrastructure-promotion prior:\n1. Inherit mature mechanisms when they already own the operation semantics.\n2. If repeated Agent burden remains, add the smallest local adapter/equipment surface rather than a new authority.\n3. Promote a durable reusable owner/shared responsibility only after repeated real workloads, strong simpler-baseline failure, explicit ownership/recovery consequences, and a deletion test.\n4. Independent platform/repository status requires separate lifecycle/deployment pressure. Convenience, popularity and implementation effort are not promotion evidence.'''
CAL='''Use an evidence-calibration procedure before deciding. Do not default to either conservatism or retention. Explicitly assess in your reason: CURRENT CONSUMER; INCREMENTAL OUTCOME over current substrate; whether the STRONG BASELINE failed; RECURRING COST/coupling; AUTHORITY FIT; and REOPEN/DELETION evidence. Then choose the disposition whose strength matches the evidence. A repeated measured gain may justify retention or owner-utility promotion; missing consumer/incremental gain should remain deferred/rejected.'''
SCHEMA={'type':'object','additionalProperties':False,'properties':{'decision':{'type':'string','enum':DECISIONS},'keyEvidence':{'type':'array','items':{'type':'string'},'minItems':1,'maxItems':5},'reason':{'type':'string'}},'required':['decision','keyEvidence','reason']}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def prompt(doc,c,t):
 s='You are deciding whether/how to retain one professional equipment candidate from evidence available at that time. Use evidence, not software popularity or naming symmetry. Choose exactly one disposition.\n\n'
 if t=='static': s+=STATIC+'\n\n'
 elif t=='calibrated': s+=CAL+'\n\n'
 return s+'DISPOSITIONS:\n'+json.dumps(doc['decisionOptions'],ensure_ascii=False,sort_keys=True)+'\n\nEVIDENCE PACKET:\n'+c['packet']
def one(doc,c,t,model,rep,secret):
 pr=prompt(doc,c,t); settings=replace(DeepSeekSettings.from_secret_file(secret),model=model,max_output_tokens=900); now=time.time_ns()//1_000_000; rid=f"harness-run:pal-f6:{c['caseId']}:{t}:{model}:{rep}:{now}"; completion={'mode':'structured-result-v1','resultKind':'pal-f6-equipment-selection','resultSchema':SCHEMA}
 contract=HarnessRunContract(harness_run_id=rid,harness_implementation_id='ordivon-harness@pal-f6',caller_id='caller:ordivon-computing-pal',caller_run_ref=f"{c['caseId']}|{t}|{model}|{rep}",objective_ref=ref(f"objective:{c['caseId']}",'objective',{'case':c['caseId']}),context_refs=(ref(f"context:{c['caseId']}:{t}:{rep}",'context',{'prompt':pr}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=65536,max_wall_time_ms=90000,max_total_tokens=18000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f"system:{c['caseId']}:{t}:{model}",'system-manifest',{'experiment':'PAL-F6','model':model,'treatment':t,'maxOutputTokens':900}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix='ordivon-pal-f6-') as sr:
  run=HarnessAgentRun.create(sr,contract,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); st=time.monotonic(); ex=run.run(({'role':'user','content':pr},)); elapsed=round((time.monotonic()-st)*1000); conc=ex.loop_result.conclusion; dec=None if conc is None else decode_structured_completion_result(contract,conc); valid=isinstance(dec,dict) and dec.get('decision') in DECISIONS; choice=dec.get('decision') if valid else None; term=ex.terminal_result
  return {'caseId':c['caseId'],'split':c['split'],'treatment':t,'model':model,'replica':rep,'runId':rid,'stopCode':ex.loop_result.stop_code.value,'modelCalls':ex.loop_result.model_calls,'usage':ex.loop_result.usage,'elapsedMs':elapsed,'result':dec,'valid':valid,'decision':choice,'exactCorrect':bool(valid and choice==c['oracleDecision']),'oracleDecision':c['oracleDecision'],'receiptDigest':None if term is None else term.receipt.digest}
def validate():
 d=json.load(open(ROOT/'f6-cases-v0.json')); assert len(d['cases'])==8; [(_ for _ in ()).throw(AssertionError()) for c in d['cases'] if c['oracleDecision'] not in DECISIONS]; return {'caseCount':8,'caseDigest':canonical_digest(d),'staticPriorDigest':canonical_digest(STATIC),'calibrationDigest':canonical_digest(CAL)}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--model',choices=['deepseek-v4-flash','deepseek-v4-pro']); ap.add_argument('--replicas',type=int,default=2); ap.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); ap.add_argument('--output'); ap.add_argument('--validate-only',action='store_true'); a=ap.parse_args(); v=validate();
 if a.validate_only: print(json.dumps(v,indent=2)); return
 if not a.model or not a.output: ap.error('--model and --output required')
 doc=json.load(open(ROOT/'f6-cases-v0.json')); rows=[]; out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
 def persist():
  e={'schemaVersion':1,'kind':'ordivon.computing.pal-f6-provider-campaign','model':a.model,'replicas':a.replicas,'caseDigest':canonical_digest(doc),'staticPriorDigest':canonical_digest(STATIC),'calibrationDigest':canonical_digest(CAL),'rows':rows}; out.write_text(json.dumps(e,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); return e
 persist(); orders={1:['raw','static','calibrated'],2:['calibrated','static','raw']}
 for c in doc['cases']:
  for rep in range(1,a.replicas+1):
   for t in orders[rep]:
    try: r=one(doc,c,t,a.model,rep,Path(a.secret))
    except Exception as exc: r={'caseId':c['caseId'],'split':c['split'],'treatment':t,'model':a.model,'replica':rep,'runId':None,'stopCode':'provider_or_recovery_exception','modelCalls':None,'usage':None,'elapsedMs':None,'result':None,'valid':False,'decision':None,'exactCorrect':False,'oracleDecision':c['oracleDecision'],'receiptDigest':None,'errorType':type(exc).__name__,'error':str(exc)[:500]}
    rows.append(r); e=persist(); print(json.dumps({'case':r['caseId'],'model':a.model,'replica':rep,'treatment':t,'valid':r['valid'],'decision':r['decision'],'oracle':r['oracleDecision'],'correct':r['exactCorrect'],'errorType':r.get('errorType')},ensure_ascii=False),flush=True)
 e=persist(); print(json.dumps({'output':str(out),'rows':len(rows),'digest':canonical_digest(e)},indent=2))
if __name__=='__main__': main()
