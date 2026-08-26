from __future__ import annotations
import json,tempfile,time
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
RAW=json.loads((ROOT/'atlas-raw-trials-v1.json').read_text())
CONTRACT=json.loads((ROOT/'candidate-evaluation-contract.json').read_text())
BATCHES=[
 ['ordivon-computing','ordivon-runtime','ordivon-host','ordivon-harness','ordivon-world'],
 ['ordivon-game','ordivon-security','ordivon-finance','ordivon-human','ordivon-media'],
 ['ordivon-web','ordivon-scd','ordivon-computational-possibility','ordivon-interlocus','ordivon-normative'],
]
Q=['QK','QU_E','QU_ZH']; S=['A0_SYNTHESIS_ONLY','A1_EXISTING_STALE_GENERATED_PLUS_SYNTHESIS']
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def schema(owners):
 item={'type':'object','additionalProperties':False,'properties':{
  'ownerId':{'type':'string','enum':owners},'queryKind':{'type':'string','enum':Q},'surface':{'type':'string','enum':S},
  'semanticRecall':{'type':'boolean'},'targetRank':{'type':'integer','minimum':0,'maximum':8},
  'matchClass':{'type':'string','enum':['TARGET','CORRECT_SUCCESSOR','RELATED_ONLY','NONE']},
  'falsePositiveDominated':{'type':'boolean'},'shortReason':{'type':'string'}},
  'required':['ownerId','queryKind','surface','semanticRecall','targetRank','matchClass','falsePositiveDominated','shortReason']}
 return {'type':'object','additionalProperties':False,'properties':{'evaluations':{'type':'array','minItems':len(owners)*6,'maxItems':len(owners)*6,'items':item}},'required':['evaluations']}
def compact_row(r):
 return {'ownerId':r['ownerId'],'targetStanding':r['targetStanding'],'sourceAnchorQuote':r['sourceAnchorQuote'],'queryKind':r['queryKind'],'query':r['query'],'surface':r['surface'],'candidates':[{'rank':i+1,'sourceClass':c.get('sourceClass'),'path':c.get('path'),'locator':c.get('locator'),'currentness':c.get('currentness'),'excerpt':c.get('excerpt')} for i,c in enumerate(r['candidates'])]}
def run_batch(idx,owners):
 rows=[compact_row(r) for r in RAW['rows'] if r['ownerId'] in owners]
 prompt='''You are a fresh bounded semantic comparator in a preregistered discoverability audit. You are NOT the owner truth authority and you do NOT adjudicate currentness. For every supplied retrieval instance, compare the frozen target standing/source anchor against the ranked Atlas candidates.

Use the exact contract definitions:
TARGET = candidate directly contains or faithfully states the target standing.
CORRECT_SUCCESSOR = candidate faithfully resolves the same target to its correct semantic successor.
RELATED_ONLY = same domain/theme/keywords but does not recover the target distinction.
NONE = no candidate materially relevant.

semanticRecall is true only for TARGET or CORRECT_SUCCESSOR. targetRank is the earliest true target/successor rank, else 0. falsePositiveDominated=true when ranked results are mainly lexically/thematically attractive but fail the target, especially when top candidates could mislead a finite caller.

Do not award recall because the project/owner name appears. Do not treat Atlas currentness labels as owner truth. Evaluate every row exactly once.

EVALUATION CONTRACT:\n'''+json.dumps(CONTRACT,ensure_ascii=False,sort_keys=True)+'\n\nROWS:\n'+json.dumps(rows,ensure_ascii=False,sort_keys=True)
 completion={'mode':'structured-result-v1','resultKind':f'discoverability-semantic-eval-b{idx}','resultSchema':schema(owners)}
 settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=9000)
 now=time.time_ns()//1_000_000
 c=HarnessRunContract(harness_run_id=f'harness-run:discoverability-eval:b{idx}:{now}',harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:ordivon-computing-discoverability-audit',caller_run_ref=f'discoverability-semantic-eval|b{idx}',objective_ref=ref(f'objective:discoverability-eval:b{idx}','objective',{'target':'semantic recall classification'}),context_refs=(ref(f'context:discoverability-eval:b{idx}','context',{'prompt':prompt}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=180000,max_total_tokens=180000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f'system:discoverability-eval:b{idx}','system-manifest',{'experiment':'discoverability-currentness-v0','role':'semantic-comparator-only'}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
 with tempfile.TemporaryDirectory(prefix=f'discovery-eval-b{idx}-') as state:
  ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({'role':'user','content':prompt},)); result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
 if not result: raise RuntimeError(f'batch {idx} failed {ex.loop_result.stop_code.value}')
 expected={(o,q,s) for o in owners for q in Q for s in S}; got={(e['ownerId'],e['queryKind'],e['surface']) for e in result['evaluations']}
 if got!=expected: raise RuntimeError(f'batch {idx} coverage mismatch missing={sorted(expected-got)} extra={sorted(got-expected)}')
 return {'batch':idx,'owners':owners,'evaluations':result['evaluations'],'usage':ex.loop_result.usage,'stopCode':ex.loop_result.stop_code.value}
def main():
 batches=[run_batch(i+1,b) for i,b in enumerate(BATCHES)]
 evals=[e for b in batches for e in b['evaluations']]
 out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-semantic-evaluations','contractDigest':canonical_digest(CONTRACT),'rawTrialsDigest':canonical_digest(RAW),'evaluations':evals,'batches':[{k:v for k,v in b.items() if k!='evaluations'} for b in batches]}
 (ROOT/'semantic-evaluations-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 print('evaluations',len(evals))
 for surface in S:
  print('\n',surface)
  for q in Q:
   rr=[e for e in evals if e['surface']==surface and e['queryKind']==q]; print(q,'recall',sum(e['semanticRecall'] for e in rr),'/',len(rr),'falsePositiveDominated',sum(e['falsePositiveDominated'] for e in rr),'avgRank',round(sum(e['targetRank'] for e in rr if e['targetRank'])/max(1,sum(bool(e['targetRank']) for e in rr)),2))
 print('tokens',[b['usage'].get('totalTokens') for b in batches])
if __name__=='__main__': main()
