from __future__ import annotations
import json, re, tempfile, time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import (
    DeepSeekSettings, DeepSeekTurnAdapter, HarnessAgentRun, HarnessBoundReference,
    HarnessPrivacyPolicy, HarnessRunContract, NO_TOOL_AGENT_GRANT_DIGEST,
    NO_TOOL_AGENT_SURFACE_DIGEST, RunBudget, decode_structured_completion_result,
)

ROOT=Path(__file__).resolve().parent
PACKET=json.loads((ROOT/'owner-source-packet-v2.json').read_text())
OWNER_ROWS={x['ownerId']:x for x in PACKET['owners']}
BATCHES=[
    ['ordivon-computing','ordivon-runtime','ordivon-host','ordivon-harness','ordivon-world'],
    ['ordivon-game','ordivon-security','ordivon-finance','ordivon-human','ordivon-media'],
    ['ordivon-web','ordivon-scd','ordivon-computational-possibility','ordivon-interlocus','ordivon-normative'],
]

def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))

def schema_for(owners):
    item={
      'type':'object','additionalProperties':False,
      'properties':{
        'ownerId':{'type':'string','enum':owners},
        'targetKey':{'type':'string'},
        'sourcePath':{'type':'string'},
        'sourceAnchorQuote':{'type':'string'},
        'targetStanding':{'type':'string'},
        'qkOwnerKnown':{'type':'string'},
        'quEnglish':{'type':'string'},
        'quChinese':{'type':'string'},
      },
      'required':['ownerId','targetKey','sourcePath','sourceAnchorQuote','targetStanding','qkOwnerKnown','quEnglish','quChinese']
    }
    return {'type':'object','additionalProperties':False,'properties':{'targets':{'type':'array','minItems':len(owners),'maxItems':len(owners),'items':item}},'required':['targets']}

def run_batch(index, owners):
    sources=[OWNER_ROWS[o] for o in owners]
    prompt='''You are forming PRE-REGISTERED retrieval targets for a discoverability audit. You have ONLY committed current owner-source excerpts; you have not seen Atlas retrieval results.

For EACH owner, choose exactly one materially distinctive current research standing, responsibility boundary, or research conclusion supported by the supplied source. Do not choose a generic project description if a more discriminating current claim is available.

Return:
- sourcePath: one supplied path for that owner.
- sourceAnchorQuote: an EXACT contiguous quote from that supplied source, 5-24 words, enough to verify the target mechanically. Do not alter punctuation or words.
- targetStanding: concise faithful paraphrase of what that quote/source establishes; do not strengthen it.
- qkOwnerKnown: an English search query allowed to include the owner/project name and source-near vocabulary. This is a lexical-rich positive control.
- quEnglish: a natural English question a caller might ask WITHOUT knowing the owner/project/repository. Do not use any `ordivon-*` id, project name, repository name, or copy a source sentence. Prefer different everyday/causal vocabulary while preserving the same intended problem.
- quChinese: a natural Chinese question expressing the same intended problem WITHOUT project/owner/repository names and WITHOUT inserting English answer-key terms. Use Chinese prose; ordinary ASCII punctuation/numbers are fine, but no Latin alphabetic words.

Important constraints:
1. Each owner appears exactly once.
2. The target must be current-source-supported, not invented from general knowledge.
3. qk is intentionally easy/lexical. QU queries are intentionally owner-unknown and representation-shifted, not adversarial nonsense.
4. Do not mention Atlas, retrieval, this audit, or 'which project' in the user queries.
5. Do not turn an implementation detail into a broader theory claim.
6. For historical/currentness-sensitive owners, target a CURRENT bounded claim, not a historical statement unless the current source itself makes the historical/current distinction load-bearing.

SOURCE PACKET:
'''+json.dumps({'owners':sources},ensure_ascii=False,sort_keys=True)
    completion={'mode':'structured-result-v1','resultKind':f'discoverability-targets-b{index}','resultSchema':schema_for(owners)}
    settings=replace(DeepSeekSettings.from_secret_file('/root/.config/ordivon/secrets/deepseek.json'),model='deepseek-v4-flash',max_output_tokens=6000)
    now=time.time_ns()//1_000_000
    c=HarnessRunContract(
        harness_run_id=f'harness-run:discoverability-targets:b{index}:{now}',
        harness_implementation_id='ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f',
        caller_id='caller:ordivon-computing-discoverability-audit',
        caller_run_ref=f'discoverability-target-generation|batch-{index}',
        objective_ref=ref(f'objective:discoverability-targets:b{index}','objective',{'target':'form pre-retrieval owner-unknown queries'}),
        context_refs=(ref(f'context:discoverability-targets:b{index}','context',{'prompt':prompt}),),
        provider_id='provider:deepseek',adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=180000,max_total_tokens=160000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(f'system:discoverability-targets:b{index}','system-manifest',{'experiment':'discoverability-currentness-v0','role':'query-formation-before-retrieval'}),
        created_at_ms=now,source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy='bounded-private-content',allow_model_content=True,allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix=f'discovery-target-b{index}-') as state:
        ex=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)).run(({'role':'user','content':prompt},))
        result=decode_structured_completion_result(c,ex.loop_result.conclusion) if ex.loop_result.conclusion else None
    if not result:
        raise RuntimeError(f'batch {index} failed: {ex.loop_result.stop_code.value}')
    return {'batch':index,'owners':owners,'result':result,'usage':ex.loop_result.usage,'stopCode':ex.loop_result.stop_code.value}

def validate(targets):
    problems=[]
    seen=[]
    latin=re.compile(r'[A-Za-z]')
    for t in targets:
        owner=t['ownerId']; seen.append(owner); row=OWNER_ROWS[owner]
        src=next((s for s in row['sources'] if s['path']==t['sourcePath']),None)
        if src is None: problems.append(f'{owner}: sourcePath not supplied'); continue
        if t['sourceAnchorQuote'] not in src['text']:
            problems.append(f'{owner}: anchor quote not exact')
        low=(t['quEnglish']+' '+t['quChinese']).lower()
        forbidden={owner.lower(),owner.replace('ordivon-','').lower(),'ordivon'}
        for f in forbidden:
            if len(f)>=3 and f in low: problems.append(f'{owner}: unknown query leaks forbidden token {f}')
        if latin.search(t['quChinese']): problems.append(f'{owner}: Chinese query contains Latin alphabetic text')
        if not t['qkOwnerKnown'].strip() or not t['quEnglish'].strip() or not t['quChinese'].strip(): problems.append(f'{owner}: empty query')
    if sorted(seen)!=sorted(OWNER_ROWS): problems.append('owner coverage mismatch')
    return problems

def main():
    batches=[run_batch(i+1,b) for i,b in enumerate(BATCHES)]
    targets=[t for b in batches for t in b['result']['targets']]
    problems=validate(targets)
    out={
      'schemaVersion':1,
      'kind':'ordivon.computing.discoverability-prefrozen-targets',
      'truthRole':'model-authored-query-formation-bound-to-committed-owner-source',
      'generatedBeforeAtlasRetrieval':True,
      'sourcePacketDigest':canonical_digest(PACKET),
      'targets':targets,
      'validationProblems':problems,
      'batches':[{k:v for k,v in b.items() if k!='result'} for b in batches],
      'nonClaims':['TargetStanding is a bounded paraphrase for the audit; owner-native source remains authority.','Model target generation does not establish discoverability or currentness.']
    }
    (ROOT/'prefrozen-targets-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'targets':len(targets),'validationProblems':problems,'batchStops':[b['stopCode'] for b in batches],'tokens':[b['usage'].get('totalTokens') for b in batches]},ensure_ascii=False,indent=2))
    if problems: raise SystemExit(2)
if __name__=='__main__': main()
