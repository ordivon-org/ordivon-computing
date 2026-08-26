from __future__ import annotations
import argparse, json, random, tempfile, time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings, DeepSeekTurnAdapter, HarnessAgentRun, HarnessBoundReference, HarnessPrivacyPolicy, HarnessRunContract, NO_TOOL_AGENT_GRANT_DIGEST, NO_TOOL_AGENT_SURFACE_DIGEST, RunBudget, decode_structured_completion_result
ROOT=Path(__file__).resolve().parent
SCHEMA={"type":"object","additionalProperties":False,"properties":{"currentCapabilityStanding":{"type":"string","enum":["ESTABLISHED","NOT_ESTABLISHED"]},"preserveNativeSemantics":{"type":"boolean"},"reason":{"type":"string"}},"required":["currentCapabilityStanding","preserveNativeSemantics","reason"]}
def ref(i,k,v): return HarnessBoundReference(i,k,canonical_digest(v))
def oracle(case): return "ESTABLISHED" if case["oracle"]["standing"]=="REALIZED" else "NOT_ESTABLISHED"
def packet(case,treatment):
    base={"targetOperation":case["targetOperation"],"facts":case["rawFacts"]}
    text=("You are a fresh finite Agent with no prior Ordivon memory. Judge ONLY whether the described external resource is a CURRENTLY ESTABLISHED capability for the exact target operation now. "
          "A useful future opportunity, installed resource, reachable endpoint, historical success, or authoritative source may still be NOT_ESTABLISHED for the exact current operation. "
          "Do not reward internal implementation or ownership merely for being internal. Preserve external/native truth and authority. Return only the structured result.\n\nFACTS:\n"+json.dumps(base,ensure_ascii=False,sort_keys=True))
    if treatment=="RELATION_ENVELOPE": text+="\n\nADDITIONAL NON-AUTHORITATIVE RELATION PROJECTION:\nThis projection reorganizes the SAME facts and adds no recommendation or new fact.\n"+json.dumps(case["relations"],ensure_ascii=False,sort_keys=True)
    return text
def score(result,case):
    ok=isinstance(result,dict); expected=oracle(case)
    return {"expected":expected,"standingCorrect":ok and result.get("currentCapabilityStanding")==expected,"nativeSemanticCorrect":ok and result.get("preserveNativeSemantics") is True,"authorityOverclaim":ok and result.get("currentCapabilityStanding")=="ESTABLISHED" and expected!="ESTABLISHED","nativeSemanticErasure":ok and result.get("preserveNativeSemantics") is False}
def run_one(case,treatment,model,rep,secret):
    prompt=packet(case,treatment); now=time.time_ns()//1_000_000; rid=f"harness-run:assimilation-rd0-v2:{case['id']}:{treatment}:{model}:r{rep}:{now}"; completion={"mode":"structured-result-v1","resultKind":"assimilation-relation-deletion-holdout-v2","resultSchema":SCHEMA}; settings=replace(DeepSeekSettings.from_secret_file(secret),model=model,max_output_tokens=600)
    c=HarnessRunContract(harness_run_id=rid,harness_implementation_id="ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f",caller_id="caller:ordivon-computing-assimilation-audit",caller_run_ref=f"holdout-v2|{case['id']}|{treatment}|{model}|r{rep}",objective_ref=ref(f"objective:{case['id']}:holdout-v2","objective",{"target":case["targetOperation"],"axis":"current-capability-standing"}),context_refs=(ref(f"context:{case['id']}:{treatment}:holdout-v2","context",{"prompt":prompt}),),provider_id="provider:deepseek",adapter_id=DeepSeekTurnAdapter.adapter_id,requested_model_id=settings.model,tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,budget=RunBudget(max_model_calls=2,max_tool_calls=0,max_observation_bytes=32768,max_wall_time_ms=120000,max_total_tokens=16384,max_model_retries=1,max_conclusion_corrections=1).to_contract_dict(),completion_contract=completion,system_manifest_ref=ref(f"system:{case['id']}:{treatment}:{model}:holdout-v2","system-manifest",{"experiment":"assimilation-rd0-holdout-v2","treatment":treatment,"model":model}),created_at_ms=now,source_refs=(),privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content",allow_model_content=True,allow_tool_content=False))
    with tempfile.TemporaryDirectory(prefix="assimilation-rd0-v2-") as state:
        run=HarnessAgentRun.create(state,c,lambda exact:DeepSeekTurnAdapter(settings,completion_contract=exact.completion_contract)); started=time.monotonic(); ex=run.run(({"role":"user","content":prompt},)); elapsed=round((time.monotonic()-started)*1000); conclusion=ex.loop_result.conclusion; result=None if conclusion is None else decode_structured_completion_result(c,conclusion); return {"caseId":case["id"],"treatment":treatment,"model":model,"replicate":rep,"result":result,"evaluation":score(result,case),"usage":ex.loop_result.usage,"elapsedMs":elapsed,"stopCode":ex.loop_result.stop_code.value}
def summary(rows):
    o={}
    for r in rows:
        k=f"{r['model']}|{r['treatment']}"; b=o.setdefault(k,{"model":r['model'],"treatment":r['treatment'],"trials":0,"standingCorrect":0,"nativeSemanticCorrect":0,"authorityOverclaim":0,"nativeSemanticErasure":0}) ; b['trials']+=1
        for x in ('standingCorrect','nativeSemanticCorrect','authorityOverclaim','nativeSemanticErasure'): b[x]+=int(bool(r['evaluation'].get(x)))
    return list(o.values())
def main():
    a=argparse.ArgumentParser(); a.add_argument('--output',required=True); a.add_argument('--models',default='deepseek-v4-pro'); a.add_argument('--replicates',type=int,default=1); a.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); a.add_argument('--seed',type=int,default=202608267); z=a.parse_args(); data=json.loads((ROOT/'cases.json').read_text()); sched=[(c,t,m,r) for c in data['cases'] for t in ('RAW_FACTS','RELATION_ENVELOPE') for m in z.models.split(',') if m for r in range(1,z.replicates+1)]; random.Random(z.seed).shuffle(sched); rows=[]; out=Path(z.output)
    for n,(case,t,m,r) in enumerate(sched,1):
        try: row=run_one(case,t,m,r,Path(z.secret))
        except Exception as e: row={"caseId":case['id'],"treatment":t,"model":m,"replicate":r,"result":None,"evaluation":{"expected":oracle(case),"standingCorrect":False,"nativeSemanticCorrect":False,"authorityOverclaim":False,"nativeSemanticErasure":False},"errorType":type(e).__name__,"error":str(e)[:1500]}
        rows.append(row); payload={"schemaVersion":1,"kind":"ordivon.computing.assimilation-relation-deletion-holdout-v2","casesDigest":canonical_digest(data),"seed":z.seed,"plannedTrials":len(sched),"completedTrials":len(rows),"rows":rows,"summary":summary(rows)}; out.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print(json.dumps({"n":n,"total":len(sched),"case":case['id'],"treatment":t,"model":m,"result":row.get('result'),"eval":row.get('evaluation'),"error":row.get('error')},ensure_ascii=False),flush=True)
if __name__=='__main__': main()
