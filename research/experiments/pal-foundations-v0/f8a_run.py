from __future__ import annotations
import argparse,json,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
SCHEMA={'type':'object','additionalProperties':False,'properties':{'diagnosis':{'type':'string'},'discriminatingTest':{'type':'string'},'consideredAlternatives':{'type':'array','items':{'type':'string'},'minItems':1,'maxItems':4},'reason':{'type':'string'}},'required':['diagnosis','discriminatingTest','consideredAlternatives','reason']}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def norm(s): return ' '.join(str(s).lower().replace('_',' ').replace('-',' ').split())
def matches(text,groups):
 s=norm(text); return all(any(norm(term) in s for term in group) for group in groups)
def prompt(c,t):
 if t=='direct': mode='Reason toward ONE best root-cause diagnosis. Do not enumerate alternative causal mechanisms. In consideredAlternatives include exactly one item: your final diagnosis.'
 else: mode='Before finalizing, generate FOUR materially distinct plausible causal mechanisms. Put exactly four distinct items in consideredAlternatives, then select the best final diagnosis and one discriminating test.'
 return 'Diagnose one real system incident from evidence available before resolution. The correct cause is not supplied as a menu. '+mode+' Prefer a test that would distinguish your diagnosis from plausible alternatives.\n\nINCIDENT:\n'+c['packet']
def one(doc,c,t,model,rep,secret):
 pr=prompt(c,t); settings=replace(DeepSeekSettings.from_secret_file(secret),model=model,max_output_tokens=900); now=time.time_ns()//1_000_000; rid=f"harness-run:pal-f8a:{c['caseId']}:{t}:{model}:{rep}:{now}"; comp={'mode':'structured-result-v1','resultKind':'pal-f8a-open-diagnosis','resultSchema':SCHEMA}; contract=HarnessRunContract(harness_run_id=rid,harness_implementation_id='ordivon-harness@pal-f8a',caller_id='caller:ordivon-computing-pal',caller_run_ref=f"{c['caseId']}|{t}|{model}|{rep}",objective_ref=ref(f"objective:{c['caseId']}",'objective',{'case':c['caseId']}),context_refs=(ref(f"context:{c['caseId']}:{t}:{rep}",'context',{'prompt':pr}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=65536,max_wall_time_ms=90000,max_total_tokens=18000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=comp,system_manifest_ref=ref(f"system:{c['caseId']}:{t}:{model}",'system-manifest',{'experiment':'PAL-F8A','model':model,'treatment':t,'maxOutputTokens':900}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix='ordivon-pal-f8a-') as sr:
  run=HarnessAgentRun.create(sr,contract,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); st=time.monotonic(); ex=run.run(({'role':'user','content':pr},)); elapsed=round((time.monotonic()-st)*1000); conc=ex.loop_result.conclusion; dec=None if conc is None else decode_structured_completion_result(contract,conc); valid=isinstance(dec,dict) and all(isinstance(dec.get(k),str) for k in ['diagnosis','discriminatingTest','reason']) and isinstance(dec.get('consideredAlternatives'),list); diag=False if not valid else matches(dec['diagnosis'],c['diagnosisGroups']); test=False if not valid else matches(dec['discriminatingTest'],c['testGroups']); alts=[] if not valid else [norm(x) for x in dec['consideredAlternatives'] if isinstance(x,str)]; compliance=valid and ((t=='direct' and len(alts)==1) or (t=='variation' and len(alts)==4 and len(set(alts))==4)); term=ex.terminal_result
  return {'caseId':c['caseId'],'split':c['split'],'treatment':t,'model':model,'replica':rep,'runId':rid,'stopCode':ex.loop_result.stop_code.value,'modelCalls':ex.loop_result.model_calls,'usage':ex.loop_result.usage,'elapsedMs':elapsed,'result':dec,'valid':valid,'variationCompliant':compliance,'diagnosisCorrect':diag,'testCorrect':test,'jointCorrect':bool(diag and test),'receiptDigest':None if term is None else term.receipt.digest}
def validate():
 d=json.load(open(ROOT/'f8a-cases-v0.json')); assert len(d['cases'])==8; assert sum(c['split']=='development' for c in d['cases'])==4; assert sum(c['split']=='holdout' for c in d['cases'])==4
 for c in d['cases']: assert c['diagnosisGroups'] and c['testGroups'] and c['packet']
 return {'caseCount':8,'caseDigest':canonical_digest(d),'schemaDigest':canonical_digest(SCHEMA)}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--model',choices=['deepseek-v4-flash','deepseek-v4-pro']); ap.add_argument('--replicas',type=int,default=2); ap.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); ap.add_argument('--output'); ap.add_argument('--validate-only',action='store_true'); a=ap.parse_args(); v=validate()
 if a.validate_only: print(json.dumps(v,indent=2)); return
 if not a.model or not a.output: ap.error('--model and --output required')
 doc=json.load(open(ROOT/'f8a-cases-v0.json')); rows=[]; out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
 def persist():
  e={'schemaVersion':1,'kind':'ordivon.computing.pal-f8a-provider-campaign','model':a.model,'replicas':a.replicas,'caseDigest':canonical_digest(doc),'schemaDigest':canonical_digest(SCHEMA),'rows':rows}; out.write_text(json.dumps(e,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); return e
 persist(); orders={1:['direct','variation'],2:['variation','direct']}
 for c in doc['cases']:
  for rep in range(1,a.replicas+1):
   for t in orders[rep]:
    try:r=one(doc,c,t,a.model,rep,Path(a.secret))
    except Exception as exc:r={'caseId':c['caseId'],'split':c['split'],'treatment':t,'model':a.model,'replica':rep,'runId':None,'stopCode':'provider_or_recovery_exception','modelCalls':None,'usage':None,'elapsedMs':None,'result':None,'valid':False,'variationCompliant':False,'diagnosisCorrect':False,'testCorrect':False,'jointCorrect':False,'receiptDigest':None,'errorType':type(exc).__name__,'error':str(exc)[:500]}
    rows.append(r); e=persist(); print(json.dumps({'case':r['caseId'],'model':a.model,'replica':rep,'treatment':t,'valid':r['valid'],'compliant':r['variationCompliant'],'diagnosis':r['diagnosisCorrect'],'test':r['testCorrect'],'joint':r['jointCorrect'],'errorType':r.get('errorType')},ensure_ascii=False),flush=True)
 e=persist(); print(json.dumps({'output':str(out),'rows':len(rows),'digest':canonical_digest(e)},indent=2))
if __name__=='__main__':main()
