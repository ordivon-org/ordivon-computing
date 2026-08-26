from __future__ import annotations
import json,re,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
TARGETS=json.loads((ROOT/'prefrozen-targets-v2.json').read_text())
CTX=json.loads((ROOT/'retrieval-authoring-context-v1.json').read_text())
CONTRACT=json.loads((ROOT/'query-authoring-ablation-contract.json').read_text())
items=[]
for i,t in enumerate(TARGETS['targets'],1):
    items.append({'queryId':f'q{i:02d}-en','language':'en','rawQuery':t['quEnglish']})
    items.append({'queryId':f'q{i:02d}-zh','language':'zh','rawQuery':t['quChinese']})
BATCHES=[items[i:i+10] for i in range(0,len(items),10)]
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def schema(qids):
    item={'type':'object','additionalProperties':False,'properties':{'queryId':{'type':'string','enum':qids},'variants':{'type':'array','minItems':1,'maxItems':4,'uniqueItems':True,'items':{'type':'string','minLength':2}}},'required':['queryId','variants']}
    return {'type':'object','additionalProperties':False,'properties':{'queries':{'type':'array','minItems':len(qids),'maxItems':len(qids),'items':item}},'required':['queries']}
def run(idx,batch):
    qids=[x['queryId'] for x in batch]
    prompt='''You are a bounded QUERY AUTHORING aid for a lexical research retrieval surface. You are not a semantic owner, currentness oracle, novelty judge, or retrieval evaluator.

For each opaque queryId, convert the raw user question into 1-4 DISTINCT concise ENGLISH lexical search variants likely to match research documents. Preserve the user's question, but diversify terminology/synonyms and compress prose into useful concept handles. For Chinese input, translate the intended meaning into English lexical variants. Do not answer the question. Do not guess or invent project/owner/repository names. Do not mention Atlas or Ordivon. Do not use information not present in the raw question or the generic retrieval-authoring context. Return every queryId exactly once.

The retrieval system does lexical substring/path matching, no semantic similarity and no built-in translation. Caller-authored variants are allowed. The generic retrieval-authoring context below may suggest how to express abstract research questions, but it is NOT an answer key and no coordinate is guaranteed relevant.

CONTRACT:\n'''+json.dumps(CONTRACT,ensure_ascii=False,sort_keys=True)+'\n\nRETRIEVAL AUTHORING CONTEXT:\n'+json.dumps(CTX,ensure_ascii=False,sort_keys=True)+'\n\nRAW QUERIES:\n'+json.dumps(batch,ensure_ascii=False,sort_keys=True)
    completion={'mode':'structured-result-v1','resultKind':f'discoverability-query-variants-b{idx}','resultSchema':schema(qids)}
    settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=4500)
    now=time.time_ns()//1_000_000
    c=HarnessRunContract(harness_run_id=f'harness-run:discoverability-query-authoring:b{idx}:{now}',harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',caller_id='caller:ordivon-computing-discoverability-audit',caller_run_ref=f'discoverability-query-authoring|b{idx}',objective_ref=ref(f'objective:discoverability-query-authoring:b{idx}','objective',{'target':'author lexical query variants without owner or answer key'}),context_refs=(ref(f'context:discoverability-query-authoring:b{idx}','context',{'prompt':prompt}),),provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=180000,max_total_tokens=100000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f'system:discoverability-query-authoring:b{idx}','system-manifest',{'experiment':'discoverability-currentness-v0','role':'query-authoring-only'}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False))
    with tempfile.TemporaryDirectory(prefix=f'discovery-query-author-b{idx}-') as state:
        ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({'role':'user','content':prompt},)); result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
    if not result: raise RuntimeError(f'batch {idx} failed {ex.loop_result.stop_code.value}')
    got={x['queryId'] for x in result['queries']}
    if got!=set(qids): raise RuntimeError(f'batch {idx} coverage mismatch')
    return {'batch':idx,'queries':result['queries'],'usage':ex.loop_result.usage,'stopCode':ex.loop_result.stop_code.value}
def main():
    bs=[run(i+1,b) for i,b in enumerate(BATCHES)]; qs=[q for b in bs for q in b['queries']]
    lookup={x['queryId']:x for x in items}; problems=[]
    for q in qs:
        for v in q['variants']:
            if not re.search(r'[A-Za-z]',v): problems.append(f"{q['queryId']}: non-English/no-Latin variant {v!r}")
            if 'ordivon' in v.lower(): problems.append(f"{q['queryId']}: guessed forbidden product namespace {v!r}")
        if len(set(v.strip().lower() for v in q['variants']))!=len(q['variants']): problems.append(f"{q['queryId']}: duplicate normalized variants")
    out={'schemaVersion':1,'kind':'ordivon.computing.discoverability-prefrozen-authored-query-variants','generatedBeforeAuthoredRetrieval':True,'contractDigest':canonical_digest(CONTRACT),'retrievalAuthoringContextDigest':canonical_digest(CTX),'queries':[lookup[q['queryId']]|{'variants':q['variants']} for q in qs],'validationProblems':problems,'batches':[{k:v for k,v in b.items() if k!='queries'} for b in bs],'nonClaims':['No target owner, target standing, source anchor or Atlas result was supplied to the query-authoring model.','Authored variants are experimental caller-side representations, not Atlas truth or owner inference.']}
    (ROOT/'prefrozen-authored-query-variants-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'queries':len(qs),'problems':problems,'tokens':[b['usage'].get('totalTokens') for b in bs]},ensure_ascii=False,indent=2))
    if problems: raise SystemExit(2)
if __name__=='__main__': main()
