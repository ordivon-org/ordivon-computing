from __future__ import annotations
import json,re,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'prefrozen-authored-query-variants-v1.json').read_text())
ctx=json.loads((ROOT/'retrieval-authoring-context-v1.json').read_text())
contract=json.loads((ROOT/'query-authoring-ablation-contract.json').read_text())
BAD=['q11-zh','q12-zh','q13-zh','q14-zh','q15-zh']
rows=[{'queryId':q['queryId'],'language':q['language'],'rawQuery':q['rawQuery']} for q in src['queries'] if q['queryId'] in BAD]

def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
item={'type':'object','additionalProperties':False,'properties':{'queryId':{'type':'string','enum':BAD},'variants':{'type':'array','minItems':1,'maxItems':4,'uniqueItems':True,'items':{'type':'string','minLength':2}}},'required':['queryId','variants']}
schema={'type':'object','additionalProperties':False,'properties':{'queries':{'type':'array','minItems':5,'maxItems':5,'items':item}},'required':['queries']}
prompt='''This is a PRE-RETRIEVAL apparatus repair for five query-authoring outputs that violated the frozen ENGLISH-output contract by staying Chinese. You have not seen any retrieval result, target owner, target standing or answer key.

For each opaque queryId, produce 1-4 concise ENGLISH lexical search variants that faithfully translate/rephrase the Chinese raw question. EVERY variant must contain Latin-alphabet English words; do not output Chinese characters. Do not answer the question. Do not guess project/owner/repository names. Do not mention Ordivon or Atlas. Use only the raw query and generic retrieval-authoring context.

RAW QUERIES:\n'''+json.dumps(rows,ensure_ascii=False,sort_keys=True)+'\n\nGENERIC CONTEXT:\n'+json.dumps(ctx,ensure_ascii=False,sort_keys=True)
completion={'mode':'structured-result-v1','resultKind':'discoverability-query-variant-repair-v2','resultSchema':schema}
settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=2500)
now=time.time_ns()//1_000_000
c=HarnessRunContract(harness_run_id=f'harness-run:discoverability-query-authoring-repair:{now}',harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:ordivon-computing-discoverability-audit',caller_run_ref='discoverability-query-authoring|repair-v2',objective_ref=ref('objective:discoverability-query-authoring-repair','objective',{'target':'repair English-output constraint before retrieval'}),context_refs=(ref('context:discoverability-query-authoring-repair','context',{'prompt':prompt}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=120000,max_total_tokens=70000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref('system:discoverability-query-authoring-repair','system-manifest',{'experiment':'discoverability-currentness-v0','role':'pre-retrieval-apparatus-repair'}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
with tempfile.TemporaryDirectory(prefix='discovery-query-repair-') as state:
    ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({'role':'user','content':prompt},)); result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
if not result: raise RuntimeError(ex.loop_result.stop_code.value)
rep={q['queryId']:q['variants'] for q in result['queries']}
if set(rep)!=set(BAD): raise RuntimeError('coverage mismatch')
out_queries=[]; problems=[]
for q in src['queries']:
    row=dict(q)
    if row['queryId'] in rep: row['variants']=rep[row['queryId']]
    for v in row['variants']:
        if not re.search(r'[A-Za-z]',v): problems.append(f"{row['queryId']}: no Latin English {v!r}")
        if re.search(r'[\u3400-\u9fff]',v): problems.append(f"{row['queryId']}: still contains CJK {v!r}")
        if 'ordivon' in v.lower(): problems.append(f"{row['queryId']}: forbidden namespace {v!r}")
    out_queries.append(row)
out={'schemaVersion':2,'kind':'ordivon.computing.discoverability-prefrozen-authored-query-variants','generatedBeforeAuthoredRetrieval':True,'contractDigest':src['contractDigest'],'retrievalAuthoringContextDigest':src['retrievalAuthoringContextDigest'],'queries':out_queries,'validationProblems':problems,'apparatusRepair':{'from':'prefrozen-authored-query-variants-v1.json','beforeAnyAuthoredRetrieval':True,'repairedQueryIds':BAD,'reason':'v1 variants violated pre-frozen English-output treatment; no retrieval result or target answer was observed'},'v1BatchEvidence':src['batches'],'repairUsage':ex.loop_result.usage,'nonClaims':src['nonClaims']}
(ROOT/'prefrozen-authored-query-variants-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print(json.dumps({'repaired':BAD,'problems':problems,'tokens':ex.loop_result.usage.get('totalTokens'),'variants':rep},ensure_ascii=False,indent=2))
if problems: raise SystemExit(2)
