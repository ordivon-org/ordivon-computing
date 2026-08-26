from __future__ import annotations
import argparse, json, random, tempfile, time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings, DeepSeekTurnAdapter, HarnessAgentRun, HarnessBoundReference, HarnessPrivacyPolicy, HarnessRunContract, NO_TOOL_AGENT_GRANT_DIGEST, NO_TOOL_AGENT_SURFACE_DIGEST, RunBudget, decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
SCHEMA={"type":"object","additionalProperties":False,"properties":{"standing":{"type":"string","enum":["REALIZED","POTENTIAL","NOT_ESTABLISHED"]},"decision":{"type":"string","enum":["USE_BOUND_EXTERNAL","QUALIFY_OR_BIND","HOLD","PREFER_REMOTE_SHARED","LOCALIZE"]},"preserveNativeSemantics":{"type":"boolean"},"reason":{"type":"string"}},"required":["standing","decision","preserveNativeSemantics","reason"]}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def packet(case,treatment):
    base={"targetOperation":case["targetOperation"],"facts":case["rawFacts"]}
    text="You are a fresh finite Agent with no prior Ordivon memory. Decide whether the described external resource is a current capability for the exact target operation. Do not reward internal implementation or ownership merely for being internal; do not assume external resources are usable merely because they exist, are installed, or are reachable. Preserve external/native truth and authority when the facts require it. Return only the structured result.\n\nFACTS:\n"+json.dumps(base,ensure_ascii=False,sort_keys=True)
    if treatment=="RELATION_ENVELOPE":
        text+="\n\nADDITIONAL NON-AUTHORITATIVE RELATION PROJECTION:\nThis projection reorganizes the SAME facts and adds no recommendation or new fact.\n"+json.dumps(case["relations"],ensure_ascii=False,sort_keys=True)
    return text
def score(result,case):
    o=case["oracle"]
    valid=isinstance(result,dict)
    standing=valid and result.get("standing")==o["standing"]
    decision=valid and result.get("decision")==o["decision"]
    native=valid and result.get("preserveNativeSemantics")==o["preserveNativeSemantics"]
    false_internalization=valid and result.get("decision")=="LOCALIZE" and o["decision"]!="LOCALIZE"
    authority_overclaim=valid and result.get("standing")=="REALIZED" and o["standing"]!="REALIZED"
    native_erasure=valid and result.get("preserveNativeSemantics") is False and o["preserveNativeSemantics"] is True
    return {"standingCorrect":standing,"relationDecisionCorrect":decision,"nativeSemanticCorrect":native,"strictAccepted":standing and decision and native,"falseInternalization":false_internalization,"authorityOverclaim":authority_overclaim,"nativeSemanticErasure":native_erasure}
def run_one(case,treatment,model,rep,secret):
    prompt=packet(case,treatment); now=time.time_ns()//1_000_000
    run_id=f"harness-run:assimilation-rd0:{case['id']}:{treatment}:{model}:r{rep}:{now}"
    completion={"mode":"structured-result-v1","resultKind":"assimilation-relation-deletion-v0","resultSchema":SCHEMA}
    settings=replace(DeepSeekSettings.from_secret_file(secret),model=model,max_output_tokens=700)
    contract=HarnessRunContract(harness_run_id=run_id,harness_implementation_id="ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f",caller_id="caller:ordivon-computing-assimilation-audit",caller_run_ref=f"{case['id']}|{treatment}|{model}|r{rep}",objective_ref=ref(f"objective:{case['id']}:v1","objective",{"target":case["targetOperation"]}),context_refs=(ref(f"context:{case['id']}:{treatment}:v1","context",{"prompt":prompt}),),provider_id="provider:deepseek",adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=120000,max_total_tokens=16384,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f"system:{case['id']}:{treatment}:{model}:r{rep}:v1","system-manifest",{"experiment":"assimilation-relation-deletion-v0","treatment":treatment,"model":model}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content",allow_model_content=True,allow_tool_content=False))
    with tempfile.TemporaryDirectory(prefix="assimilation-rd0-") as state:
        run=HarnessAgentRun.create(state,contract,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract))
        started=time.monotonic(); ex=run.run(({"role":"user","content":prompt},)); elapsed=round((time.monotonic()-started)*1000)
        c=ex.loop_result.conclusion; result=None if c is None else decode_structured_completion_result(contract,c)
        return {"caseId":case["id"],"treatment":treatment,"model":model,"replicate":rep,"result":result,"evaluation":score(result,case),"usage":ex.loop_result.usage,"elapsedMs":elapsed,"stopCode":ex.loop_result.stop_code.value}
def summarize(rows):
    out={}
    for r in rows:
        k=f"{r['model']}|{r['treatment']}"; b=out.setdefault(k,{"model":r['model'],"treatment":r['treatment'],"trials":0,"strictAccepted":0,"standingCorrect":0,"relationDecisionCorrect":0,"falseInternalization":0,"authorityOverclaim":0,"nativeSemanticErasure":0,"tokens":0})
        b["trials"]+=1
        for x in ("strictAccepted","standingCorrect","relationDecisionCorrect","falseInternalization","authorityOverclaim","nativeSemanticErasure"): b[x]+=int(bool(r["evaluation"].get(x)))
        b["tokens"]+=int((r.get("usage") or {}).get("totalTokens",0) or 0)
    return list(out.values())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--models',default='deepseek-v4-flash'); ap.add_argument('--replicates',type=int,default=1); ap.add_argument('--cases',default='all'); ap.add_argument('--treatments',default='RAW_FACTS,RELATION_ENVELOPE'); ap.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); ap.add_argument('--seed',type=int,default=202608266); a=ap.parse_args()
    data=json.loads((ROOT/'cases.json').read_text()); by={c['id']:c for c in data['cases']}; ids=list(by) if a.cases=='all' else [x for x in a.cases.split(',') if x]; models=[x for x in a.models.split(',') if x]; treatments=[x for x in a.treatments.split(',') if x]
    sched=[(i,t,m,r) for i in ids for t in treatments for m in models for r in range(1,a.replicates+1)]; random.Random(a.seed).shuffle(sched); rows=[]; out=Path(a.output)
    for n,(i,t,m,r) in enumerate(sched,1):
        try: row=run_one(by[i],t,m,r,Path(a.secret))
        except Exception as e: row={"caseId":i,"treatment":t,"model":m,"replicate":r,"result":None,"evaluation":{"strictAccepted":False,"standingCorrect":False,"relationDecisionCorrect":False,"falseInternalization":False,"authorityOverclaim":False,"nativeSemanticErasure":False},"errorType":type(e).__name__,"error":str(e)[:1500]}
        rows.append(row); payload={"schemaVersion":1,"kind":"ordivon.computing.assimilation-relation-deletion-live-v0","contractDigest":canonical_digest(json.loads((ROOT/'contract.json').read_text())),"casesDigest":canonical_digest(data),"seed":a.seed,"plannedTrials":len(sched),"completedTrials":len(rows),"rows":rows,"summary":summarize(rows)}; out.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({"n":n,"total":len(sched),"case":i,"treatment":t,"model":m,"result":row.get('result'),"eval":row.get('evaluation'),"error":row.get('error')},ensure_ascii=False),flush=True)
if __name__=='__main__': main()
