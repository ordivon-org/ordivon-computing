from __future__ import annotations

import concurrent.futures
import hashlib
import json
import time
import uuid
from dataclasses import replace
from pathlib import Path

from anc_canonical import canonical_digest
from ordivon_harness.api import DeepSeekSettings, DeepSeekTurnAdapter, RunBudget
from ordivon_harness.domain_tools import (
    AgentToolCall,
    AgentToolDefinition,
    DomainToolCatalog,
    DomainToolLoopPlan,
    DomainToolLoopRunner,
    ToolObservation,
)

import ofr5_run as r

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "single-loop-tool-hydration-diagnostic-v1.json"
TOOL_NAME = "hydrate_foundation_case"

TOOL = AgentToolDefinition(
    name=TOOL_NAME,
    description=(
        "Read-only frozen Foundations Atlas hydration. Choose one exact OFR3 case and only the causal roles needed for the question. "
        "The result mechanically declares truthRole/currentness/authority metadata. It is not current owner truth and grants no evidence, research, mechanism, or action authority."
    ),
    input_schema={
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "caseId": {"type": "string", "enum": [
                "OFR3-RUNTIME-01", "OFR3-HOST-01", "OFR3-HARNESS-01", "OFR3-WORLD-01", "OFR3-HUMAN-01",
                "OFR3-FINANCE-01", "OFR3-WORKSTATION-01", "OFR3-SECURITY-01", "OFR3-GAME-01", "OFR3-WEB-01"
            ]},
            "roles": {"type": "array", "items": {"type": "string", "enum": r.ROLES}, "uniqueItems": True, "minItems": 1, "maxItems": 9},
        },
        "required": ["caseId", "roles"],
    },
)

COMPLETION = {
    "mode": "structured-result-v1",
    "resultKind": "ofr5-single-loop-tool-hydration-answer",
    "resultSchema": r.ANSWER_SCHEMA,
}


class AtlasBridge:
    catalog = DomainToolCatalog(
        domain_id="domain:ordivon-computing-foundations-atlas-diagnostic",
        revision="ofr5-tool-hydration-diagnostic-v1",
        tools=(TOOL,),
    )
    bridge_identity = {
        "schemaVersion": 1,
        "kind": "ordivon.ofr5-frozen-atlas-tool-bridge.v1",
        "truthRole": "non-authoritative-frozen-theory-navigation",
    }

    def __init__(self, atlas: dict) -> None:
        self.atlas = atlas
        self.executions: list[dict] = []

    def execute(self, call: AgentToolCall, *, step_id: str) -> ToolObservation:
        case_id = str(call.arguments["caseId"])
        roles = [str(x) for x in call.arguments["roles"]]
        card = next(c for c in self.atlas["cards"] if c["caseId"] == case_id)
        payload = {
            "schemaVersion": 1,
            "kind": "ordivon.ofr5-frozen-theory-hydration.v1",
            "caseId": case_id,
            "owner": card["owner"],
            "title": card["title"],
            "theoryRef": card["theoryRef"],
            "frozenOwnerRevision": card["frozenOwnerRevision"],
            "roles": {role: self.atlas["hydration"][case_id][role] for role in roles},
            "truthRole": "non-authoritative-frozen-theory-navigation",
            "currentness": "not-revalidated-after-ofr3-freeze",
            "currentnessAuthority": card["owner"],
            "evidenceSufficiencyAuthority": False,
            "researchReopenAuthority": False,
            "mechanismAdmissionAuthority": False,
            "actionAuthority": False,
        }
        self.executions.append({"stepId": step_id, "caseId": case_id, "roles": roles, "payloadDigest": canonical_digest(payload)})
        return ToolObservation(call.tool_call_id, call.name, "observed", payload)


def prompt(index_text: str, q: dict) -> str:
    return (
        "Use the compact frozen Foundations Atlas below to answer the theory-navigation question. You MUST call hydrate_foundation_case exactly once before concluding. "
        "Select one exact case and only the minimum causal roles needed. Treat the Tool observation's truthRole/currentness/authority fields as mechanical facts; do not override them. "
        "Fill roles not asked by the question as NOT_REQUESTED. If a requested fact is absent, use UNKNOWN. refs must contain exact owner+revision+path/commit when supplied. "
        "epistemicBoundary must faithfully state the Tool metadata: frozen navigation is not automatically current owner truth and grants no evidence-sufficiency, research-reopen, mechanism-admission, or action authority.\n"
        + r.role_definition_text()
        + "\n\nATLAS INDEX:\n" + index_text
        + "\n\nQUESTION:\n" + q["text"]
    )


def loop_one(atlas: dict, contract: dict, index_text: str, q: dict, rep: int) -> dict:
    tag = f"toolloop:{q['queryId']}:r{rep}"
    secret = r.slot_for(tag)
    cfg = replace(DeepSeekSettings.from_secret_file(secret), model=contract["livePlan"]["generationModel"], max_output_tokens=2200)
    adapter = DeepSeekTurnAdapter(cfg, completion_contract=COMPLETION)
    bridge = AtlasBridge(atlas)
    text = prompt(index_text, q)
    run_id = f"harness-run:ofr5:{tag}:{uuid.uuid4().hex}"
    plan = DomainToolLoopPlan(
        harness_run_id=run_id,
        assignment_id=f"assignment:ofr5:{q['queryId']}:{rep}:{uuid.uuid4().hex[:12]}",
        context_digest=canonical_digest({"prompt": text}),
        initial_messages=({"role": "user", "content": text},),
        allowed_tools=(TOOL_NAME,),
        budget=RunBudget(max_model_calls=3, max_tool_calls=2, max_observation_bytes=65536, max_wall_time_ms=120000, max_total_tokens=64000, max_model_retries=1, max_tool_corrections=2, max_conclusion_corrections=1),
    )
    started=time.monotonic()
    result=DomainToolLoopRunner(adapter,bridge).run(plan)
    elapsed=round((time.monotonic()-started)*1000)
    answer=None
    if result.conclusion is not None:
        try: answer=json.loads(result.conclusion.summary)
        except Exception: answer=None
    usage=result.usage if isinstance(result.usage,dict) else dict(result.usage)
    return {
        "queryId":q["queryId"],"replicate":rep,"oracleCaseId":q["caseId"],"oracleRequestedRoles":q["requestedRoles"],
        "runId":run_id,"secretSlot":secret.name,"stopCode":result.stop_code.value,"elapsedMs":elapsed,"usage":usage,
        "toolCalls":result.tool_calls,"toolExecutions":bridge.executions,"answer":answer,"answerRealized":isinstance(answer,dict),
    }


def main() -> None:
    source,atlas,queries,surfaces,contract=r.load()
    cases={c["id"]:c for c in source["cases"]}
    qs=[q for q in queries["queries"] if q["split"]=="holdout"]
    specs=[(q,rep) for q in qs for rep in range(2)]
    index_text=surfaces["surfaces"]["ATLAS_INDEX"]["text"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        rows=list(ex.map(lambda s: loop_one(atlas,contract,index_text,*s),specs))

    def judge(row):
        if not row["answerRealized"]:
            row["semanticAccepted"]=False; row["judge"]=None; return row
        q=next(x for x in qs if x["queryId"]==row["queryId"])
        tag=f"toolloop-judge:{q['queryId']}:r{row['replicate']}"
        try:
            j=r.run_structured(prompt=r.judge_prompt(q,r.gold(cases[q["caseId"]],q),row["answer"]),schema=r.JUDGE_SCHEMA,result_kind="ofr5-single-loop-tool-hydration-judge",model=contract["livePlan"]["judgeModel"],secret=r.slot_for(tag),tag=tag,max_tokens=1100)
            row["judge"]=j; row["semanticAccepted"]=bool(j.get("valid") and isinstance(j.get("result"),dict))
        except Exception as e:
            row["judge"]={"valid":False,"errorType":type(e).__name__,"error":str(e)[:800]}; row["semanticAccepted"]=False
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        rows=list(ex.map(judge,rows))

    sem=[x for x in rows if x.get("semanticAccepted")]
    role_scores=[]; case_scores=[]; ep=[]; unsupported=[]; over=[]
    for x in sem:
        j=x["judge"]["result"]
        case_scores.append(1 if j["caseIdentificationGrade"]=="PASS" else 0)
        ep.append(r.GRADE_VALUES[j["epistemicBoundaryGrade"]]); unsupported.append(j["unsupportedInference"]); over.append(j["overgeneralized"])
        for role in x["oracleRequestedRoles"]: role_scores.append(r.GRADE_VALUES[j[f"{role}Grade"]])
    def prompt_tokens(x):
        return sum(int(u.get("prompt_tokens",0)) for u in (x.get("usage") or {}).get("providerUsage",[]) if isinstance(u,dict))
    realized=sum(x["answerRealized"] for x in rows)
    total_prompt=sum(prompt_tokens(x) for x in rows)
    tool_exact=sum(bool(x["toolExecutions"] and x["toolExecutions"][0]["caseId"]==x["oracleCaseId"]) for x in rows)
    analysis={
        "physicalTrials":len(rows),"answerRealized":realized,"physicalAcceptanceRate":round(realized/len(rows),4),"semanticAccepted":len(sem),
        "toolCaseAccuracy":round(tool_exact/len(rows),4),"meanToolExecutions":round(sum(len(x["toolExecutions"]) for x in rows)/len(rows),4),
        "caseLocalizationAccuracy":round(sum(case_scores)/len(case_scores),4) if case_scores else None,
        "requestedRoleMean":round(sum(role_scores)/len(role_scores),4) if role_scores else None,
        "epistemicBoundaryMean":round(sum(ep)/len(ep),4) if ep else None,
        "unsupportedInferenceRate":round(sum(unsupported)/len(unsupported),4) if unsupported else None,
        "overgeneralizationRate":round(sum(over)/len(over),4) if over else None,
        "totalProviderPromptTokens":total_prompt,"promptTokensPerPhysicalTrial":round(total_prompt/len(rows),1),"promptTokensPerAcceptedAnswer":round(total_prompt/realized,1) if realized else None,
    }
    out={"schemaVersion":1,"kind":"ordivon.ofr5-post-holdout-single-loop-tool-hydration-diagnostic.v1","promotionEligible":False,"reason":"Post-holdout mechanism diagnostic using existing Harness DomainToolLoopRunner; cannot repair/rescore frozen OFR5 promotion decision.","analysis":analysis,"trials":rows}
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps(analysis,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
