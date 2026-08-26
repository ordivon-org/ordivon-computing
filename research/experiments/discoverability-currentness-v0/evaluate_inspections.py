from __future__ import annotations
import json,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'atlas-inspection-trials-v1.json').read_text())
CONTRACT=json.loads((ROOT/'candidate-evaluation-contract.json').read_text())
OWNERS=['ordivon-computing','ordivon-runtime','ordivon-host','ordivon-harness','ordivon-world','ordivon-game','ordivon-security','ordivon-finance','ordivon-human','ordivon-media','ordivon-web','ordivon-scd','ordivon-computational-possibility','ordivon-interlocus','ordivon-normative']
BATCHES=[[owner] for owner in OWNERS]
Q=['QK','QU_E','QU_ZH']; S=['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def schema(owners):
 item={'type':'object','additionalProperties':False,'properties':{'ownerId':{'type':'string','enum':owners},'queryKind':{'type':'string','enum':Q},'surface':{'type':'string','enum':S},'semanticRecall':{'type':'boolean'},'targetRank':{'type':'integer','minimum':0,'maximum':8},'matchClass':{'type':'string','enum':['TARGET','CORRECT_SUCCESSOR','RELATED_ONLY','NONE']},'falsePositiveDominated':{'type':'boolean'},'shortReason':{'type':'string'}},'required':['ownerId','queryKind','surface','semanticRecall','targetRank','matchClass','falsePositiveDominated','shortReason']}
 return {'type':'object','additionalProperties':False,'properties':{'evaluations':{'type':'array','minItems':len(owners)*6,'maxItems':len(owners)*6,'items':item}},'required':['evaluations']}
def compact(r):
 return {'ownerId':r['ownerId'],'targetStanding':r['targetStanding'],'sourceAnchorQuote':r['sourceAnchorQuote'],'queryKind':r['queryKind'],'query':r['query'],'surface':r['surface'],'candidates':[{'rank':c['rank'],'sourceClass':c['candidate'].get('sourceClass'),'path':c['candidate'].get('path'),'currentness':c['candidate'].get('currentness'),'inspectionText':c['inspectionText']} for c in r['inspectedCandidates']]}
def run(idx,owners):
 rows=[compact(r) for r in DATA['rows'] if r['ownerId'] in owners]
 prompt='''You are the second-stage semantic comparator in a preregistered Atlas discoverability audit. The caller has already used first-look and then the official bounded inspect-candidate operation. Judge the INSPECTED candidate content, not only its original excerpt.

For each row, compare the frozen owner-source target against ranked inspected candidate content. TARGET or CORRECT_SUCCESSOR => semanticRecall=true and targetRank is the earliest genuine target-bearing inspected candidate. RELATED_ONLY/NONE => semanticRecall=false, targetRank=0. Do not award recall for broad thematic overlap or owner name alone. A synthesis may recover semantics even though it does not own currentness; currentness is adjudicated separately. falsePositiveDominated means the bounded journey returns attractive but wrong material in a way likely to consume finite attention before any target-bearing candidate.

Do every row exactly once. Do not infer currentness, novelty or owner truth.

CONTRACT:\n'''+json.dumps(CONTRACT,ensure_ascii=False,sort_keys=True)+'\n\nINSPECTED ROWS:\n'+json.dumps(rows,ensure_ascii=False,sort_keys=True)
 completion={'mode':'structured-result-v1','resultKind':f'discoverability-inspection-eval-b{idx}','resultSchema':schema(owners)}
 settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=7000)
 now=time.time_ns()//1_000_000
 c=HarnessRunContract(harness_run_id=f'harness-run:discoverability-inspect-eval:b{idx}:{now}',harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:ordivon-computing-discoverability-audit',caller_run_ref=f'discoverability-inspection-eval|b{idx}',objective_ref=ref(f'objective:discoverability-inspection-eval:b{idx}','objective',{'target':'evaluate bounded inspected candidate semantic recall'}),context_refs=(ref(f'context:discoverability-inspection-eval:b{idx}','context',{'prompt':prompt}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=180000,max_total_tokens=190000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f'system:discoverability-inspection-eval:b{idx}','system-manifest',{'experiment':'discoverability-currentness-v0','role':'second-stage-semantic-comparator'}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix=f'discovery-inspect-eval-b{idx}-') as state:
  ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({'role':'user','content':prompt},)); result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
 if not result: raise RuntimeError(f'batch {idx} failed {ex.loop_result.stop_code.value}')
 expected={(o,q,s) for o in owners for q in Q for s in S}; got={(e['ownerId'],e['queryKind'],e['surface']) for e in result['evaluations']}
 if got!=expected: raise RuntimeError(f'batch {idx} coverage mismatch')
 return {'batch':idx,'owners':owners,'evaluations':result['evaluations'],'usage':ex.loop_result.usage,'stopCode':ex.loop_result.stop_code.value}
def main():
 bs=[run(i+1,b) for i,b in enumerate(BATCHES)]; es=[e for b in bs for e in b['evaluations']]
 out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-inspection-semantic-evaluations','contractDigest':canonical_digest(CONTRACT),'inspectionTrialsDigest':canonical_digest(DATA),'evaluations':es,'batches':[{k:v for k,v in b.items() if k!='evaluations'} for b in bs]}
 (ROOT/'inspection-semantic-evaluations-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 print('evaluations',len(es))
 for s in S:
  print('\n'+s)
  for q in Q:
   rr=[e for e in es if e['surface']==s and e['queryKind']==q]; ranks=[e['targetRank'] for e in rr if e['semanticRecall']]; print(q,'recall',sum(e['semanticRecall'] for e in rr),'/',len(rr),'FPdom',sum(e['falsePositiveDominated'] for e in rr),'avgRank',round(sum(ranks)/len(ranks),2) if ranks else None)
 print('tokens',[b['usage'].get('totalTokens') for b in bs])
if __name__=='__main__': main()
