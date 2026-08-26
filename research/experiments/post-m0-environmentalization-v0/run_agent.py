from __future__ import annotations
import argparse,json,random,tempfile,time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings,DeepSeekTurnAdapter,HarnessAgentRun,HarnessBoundReference,HarnessPrivacyPolicy,HarnessRunContract,NO_TOOL_AGENT_GRANT_DIGEST,NO_TOOL_AGENT_SURFACE_DIGEST,RunBudget,decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
SCHEMA={"type":"object","additionalProperties":False,"properties":{"choice":{"type":"string","enum":["A","B","C","D"]},"reason":{"type":"string"}},"required":["choice","reason"]}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def packet(case,treatment,m0,cand):
    base={"caseId":case['id'],"facts":case['facts'],"candidateActions":case['actions']}
    txt=("You are a fresh finite research-method consumer with no prior Ordivon memory. Use the supplied non-authoritative methodology observation to choose exactly one bounded next disposition A-D. Judge only from the facts given. Do not invent missing authority, consumer burden, benefit, currentness, or universal infrastructure. Return only the structured result.\n\nCURRENT M0:\n"+m0+"\n\nCASE:\n"+json.dumps(base,ensure_ascii=False,sort_keys=True))
    if treatment=='M0_PLUS_CANDIDATE_A': txt+="\n\nADDITIONAL CANDIDATE METHODOLOGY OBSERVATION:\n"+cand
    return txt
def score(result,case):
    ch=result.get('choice') if isinstance(result,dict) else None; hz=set(case.get('hazards',{}).get(ch,[]))
    return {"exactDecision":ch==case['oracle'],"overDefault":"overDefault" in hz,"underDefault":"underDefault" in hz,"authorityMint":"authorityMint" in hz,"stalePersistence":"stalePersistence" in hz}
def one(case,treatment,model,rep,secret,m0,cand):
    prompt=packet(case,treatment,m0,cand); now=time.time_ns()//1_000_000; rid=f"harness-run:post-m0-env-v0:{case['id']}:{treatment}:{model}:r{rep}:{now}"; completion={"mode":"structured-result-v1","resultKind":"post-m0-environmentalization-v0","resultSchema":SCHEMA}; settings=replace(DeepSeekSettings.from_secret_file(secret),model=model,max_output_tokens=600)
    c=HarnessRunContract(harness_run_id=rid,harness_implementation_id="ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f",caller_id="caller:ordivon-computing-post-m0-audit",caller_run_ref=f"{case['id']}|{treatment}|{model}|r{rep}",objective_ref=ref(f"objective:{case['id']}:post-m0-v0","objective",{"target":"environmentalization placement judgment","case":case['id']}),context_refs=(ref(f"context:{case['id']}:{treatment}:post-m0-v0","context",{"prompt":prompt}),),provider_id="provider:deepseek",adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=120000,max_total_tokens=20000,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f"system:{case['id']}:{treatment}:{model}:r{rep}:post-m0-v0","system-manifest",{"experiment":"post-m0-environmentalization-v0","treatment":treatment,"model":model}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content",allow_model_content=True,allow_tool_content=False))
    with tempfile.TemporaryDirectory(prefix='post-m0-env-v0-') as state:
        run=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); st=time.monotonic(); ex=run.run(({"role":"user","content":prompt},)); elapsed=round((time.monotonic()-st)*1000); concl=ex.loop_result.conclusion; result=None if concl is None else decode_structured_completion_result(c,concl); return {"caseId":case['id'],"treatment":treatment,"model":model,"replicate":rep,"result":result,"evaluation":score(result,case),"usage":ex.loop_result.usage,"elapsedMs":elapsed,"stopCode":ex.loop_result.stop_code.value}
def summary(rows):
    out={}
    for r in rows:
        k=f"{r['model']}|{r['treatment']}"; b=out.setdefault(k,{"model":r['model'],"treatment":r['treatment'],"trials":0,"exactDecision":0,"overDefault":0,"underDefault":0,"authorityMint":0,"stalePersistence":0,"tokens":0}); b['trials']+=1
        for x in ('exactDecision','overDefault','underDefault','authorityMint','stalePersistence'): b[x]+=int(bool(r['evaluation'].get(x)))
        b['tokens']+=int((r.get('usage') or {}).get('totalTokens',0) or 0)
    return list(out.values())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--models',default='deepseek-v4-flash'); ap.add_argument('--replicates',type=int,default=2); ap.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); ap.add_argument('--seed',type=int,default=202608269); a=ap.parse_args(); data=json.loads((ROOT/'cases.json').read_text()); m0=(ROOT/'m0-base.md').read_text(); cand=(ROOT/'candidate-a.md').read_text(); models=[x for x in a.models.split(',') if x]; sched=[(c,t,m,r) for c in data['cases'] for t in ('M0_ONLY','M0_PLUS_CANDIDATE_A') for m in models for r in range(1,a.replicates+1)]; random.Random(a.seed).shuffle(sched); rows=[]; out=Path(a.output)
    for n,(case,t,m,r) in enumerate(sched,1):
        try: row=one(case,t,m,r,Path(a.secret),m0,cand)
        except Exception as e: row={"caseId":case['id'],"treatment":t,"model":m,"replicate":r,"result":None,"evaluation":{"exactDecision":False,"overDefault":False,"underDefault":False,"authorityMint":False,"stalePersistence":False},"errorType":type(e).__name__,"error":str(e)[:1500]}
        rows.append(row); payload={"schemaVersion":1,"kind":"ordivon.computing.post-m0-environmentalization-live-v0","contractDigest":canonical_digest(json.loads((ROOT/'contract.json').read_text())),"casesDigest":canonical_digest(data),"m0Digest":canonical_digest(m0),"candidateDigest":canonical_digest(cand),"seed":a.seed,"plannedTrials":len(sched),"completedTrials":len(rows),"rows":rows,"summary":summary(rows)}; out.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({"n":n,"total":len(sched),"case":case['id'],"treatment":t,"result":row.get('result'),"eval":row.get('evaluation'),"error":row.get('error')},ensure_ascii=False),flush=True)
if __name__=='__main__': main()
