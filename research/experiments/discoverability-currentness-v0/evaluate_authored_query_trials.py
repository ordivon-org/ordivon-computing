from __future__ import annotations
import json,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'authored-query-inspection-trials-v1.json').read_text())
CONTRACT=json.loads((ROOT/'candidate-evaluation-contract.json').read_text())
OWNERS=['ordivon-computing','ordivon-runtime','ordivon-host','ordivon-harness','ordivon-world','ordivon-game','ordivon-security','ordivon-finance','ordivon-human','ordivon-media','ordivon-web','ordivon-scd','ordivon-computational-possibility','ordivon-interlocus','ordivon-normative']
Q=['AQ_EN','AQ_ZH']; S=['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def schema(owner):
 item={'type':'object','additionalProperties':False,'properties':{'ownerId':{'type':'string','enum':[owner]},'queryKind':{'type':'string','enum':Q},'surface':{'type':'string','enum':S},'semanticRecall':{'type':'boolean'},'targetRank':{'type':'integer','minimum':0,'maximum':8},'matchClass':{'type':'string','enum':['TARGET','CORRECT_SUCCESSOR','RELATED_ONLY','NONE']},'falsePositiveDominated':{'type':'boolean'},'shortReason':{'type':'string'}},'required':['ownerId','queryKind','surface','semanticRecall','targetRank','matchClass','falsePositiveDominated','shortReason']}
 return {'type':'object','additionalProperties':False,'properties':{'evaluations':{'type':'array','minItems':4,'maxItems':4,'items':item}},'required':['evaluations']}
def compact(r):
 return {'ownerId':r['ownerId'],'targetStanding':r['targetStanding'],'sourceAnchorQuote':r['sourceAnchorQuote'],'queryKind':r['queryKind'],'rawQuery':r['rawQuery'],'authoredVariants':r['authoredVariants'],'surface':r['surface'],'candidates':[{'rank':c['rank'],'sourceClass':c['candidate'].get('sourceClass'),'path':c['candidate'].get('path'),'currentness':c['candidate'].get('currentness'),'bestVariantQuery':c['bestVariantQuery'],'inspectionText':c['inspectionText']} for c in r['inspectedCandidates']]}
def run(idx,owner):
 rows=[compact(r) for r in DATA['rows'] if r['ownerId']==owner]
 prompt='''You are a bounded second-stage semantic comparator in a preregistered query-authoring ablation. The retrieval candidates were produced from caller-authored lexical variants generated WITHOUT the target owner, target standing, source anchor, or retrieval result. Judge whether the inspected candidates actually recover the FROZEN target.

For each of 4 rows: TARGET or CORRECT_SUCCESSOR => semanticRecall=true and targetRank is earliest genuine target-bearing candidate. RELATED_ONLY or NONE => semanticRecall=false and targetRank=0. Do not reward a candidate merely for broad domain words, owner/project names, or because an authored variant sounds plausible. A synthesis can recover semantics while still being non-authoritative/currentness-unknown. Do not infer currentness, owner truth, novelty, or admission. falsePositiveDominated=true if attractive wrong candidates consume the bounded top-8 before a target or in place of one.

Do all four rows exactly once. Enforce semanticRecall=true iff targetRank in 1..8 and matchClass in {TARGET,CORRECT_SUCCESSOR}.

CONTRACT:\n'''+json.dumps(CONTRACT,ensure_ascii=False,sort_keys=True)+'\n\nROWS:\n'+json.dumps(rows,ensure_ascii=False,sort_keys=True)
 completion={'mode':'structured-result-v1','resultKind':f'discoverability-authored-eval-{idx}','resultSchema':schema(owner)}
 settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=5000)
 now=time.time_ns()//1_000_000
 c=HarnessRunContract(harness_run_id=f'harness-run:discoverability-authored-eval:{idx}:{now}',harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:ordivon-computing-discoverability-audit',caller_run_ref=f'discoverability-authored-eval|{owner}',objective_ref=ref(f'objective:discoverability-authored-eval:{idx}','objective',{'target':'evaluate query-authoring ablation target recall'}),context_refs=(ref(f'context:discoverability-authored-eval:{idx}','context',{'prompt':prompt}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=180000,max_total_tokens=180000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f'system:discoverability-authored-eval:{idx}','system-manifest',{'experiment':'discoverability-currentness-v0','role':'authored-query-semantic-comparator'}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix=f'discovery-authored-eval-{idx}-') as state:
  ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({'role':'user','content':prompt},)); result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
 if not result: raise RuntimeError(f'{owner} failed {ex.loop_result.stop_code.value}')
 expected={(owner,q,s) for q in Q for s in S}; got={(e['ownerId'],e['queryKind'],e['surface']) for e in result['evaluations']}
 if got!=expected: raise RuntimeError(f'{owner} coverage mismatch')
 for e in result['evaluations']:
  valid=((e['semanticRecall'] and 1<=e['targetRank']<=8 and e['matchClass'] in ('TARGET','CORRECT_SUCCESSOR')) or ((not e['semanticRecall']) and e['targetRank']==0 and e['matchClass'] in ('RELATED_ONLY','NONE')))
  if not valid: raise RuntimeError(f'{owner} contract inconsistency {e}')
 return {'owner':owner,'evaluations':result['evaluations'],'usage':ex.loop_result.usage,'stopCode':ex.loop_result.stop_code.value}
def main():
 partial=ROOT/'authored-query-eval-partials-v2'; partial.mkdir(exist_ok=True)
 bs=[]; apparatus=[]
 for i,o in enumerate(OWNERS):
  path=partial/f'{i+1:02d}-{o}.json'
  if path.exists():
   b=json.loads(path.read_text()); bs.append(b); print('reuse',o,flush=True); continue
  last=None
  for attempt in (1,2):
   try:
    b=run(i+1,o); b['apparatusAttempt']=attempt; path.write_text(json.dumps(b,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); bs.append(b); print('done',o,'attempt',attempt,flush=True); last=None; break
   except Exception as exc:
    last=f'{type(exc).__name__}: {exc}'; apparatus.append({'owner':o,'attempt':attempt,'error':last}); print('retryable-failure',o,'attempt',attempt,last,flush=True)
  if last is not None: raise RuntimeError(f'{o} exhausted apparatus retries: {last}')
 es=[e for b in bs for e in b['evaluations']]
 out={'schemaVersion':2,'kind':'ordivon.computing.discoverability-authored-query-semantic-evaluations','contractDigest':canonical_digest(CONTRACT),'trialDigest':canonical_digest(DATA),'evaluations':es,'batches':[{k:v for k,v in b.items() if k!='evaluations'} for b in bs],'apparatusEvents':apparatus,'reliabilityRepair':'per-owner durable partial; at most one identical-contract retry after evaluation apparatus/model-format failure'}
 (ROOT/'authored-query-semantic-evaluations-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 print('evaluations',len(es))
 for s in S:
  print('\n'+s)
  for q in Q:
   rr=[e for e in es if e['surface']==s and e['queryKind']==q]; ranks=[e['targetRank'] for e in rr if e['semanticRecall']]; print(q,'recall',sum(e['semanticRecall'] for e in rr),'/',len(rr),'FPdom',sum(e['falsePositiveDominated'] for e in rr),'avgRank',round(sum(ranks)/len(ranks),2) if ranks else None)
 print('tokens',[b['usage'].get('totalTokens') for b in bs])
 print('apparatusEvents',apparatus)
if __name__=='__main__': main()
