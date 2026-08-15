from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import tempfile
import time
import uuid
from dataclasses import replace
from pathlib import Path

from anc_canonical import canonical_digest
from ordivon_harness.api import (
    DeepSeekSettings,
    DeepSeekTurnAdapter,
    HarnessAgentRun,
    HarnessBoundReference,
    HarnessPrivacyPolicy,
    HarnessRunContract,
    NO_TOOL_AGENT_GRANT_DIGEST,
    NO_TOOL_AGENT_SURFACE_DIGEST,
    RunBudget,
    decode_structured_completion_result,
)

ROOT = Path(__file__).resolve().parent
OFR3 = ROOT.parent / "foundations-reconstruction-ofr3-v0" / "causal-reconstruction-v1.json"
ATLAS = ROOT / "atlas-v1.json"
QUERIES = ROOT / "queries-v1.json"
SURFACES = ROOT / "surfaces-v1.json"
CONTRACT = ROOT / "experiment-contract-v1.json"
SECRETS = [Path(f"/root/.config/ordivon/secrets/deepseek{suffix}.json") for suffix in ["", "1", "2", "3", "4", "5"]]
ROLES = ["invariant", "strongestRival", "whyAttractive", "decisiveFalsifier", "retainedConsequence", "counterfactualBreakage", "boundary", "reopenCondition", "refs"]
TEXT_FIELDS = ROLES
GRADE_VALUES = {"PASS": 1.0, "PARTIAL": 0.5, "FAIL": 0.0}

NAV_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "selectedCaseId": {"type": "string", "enum": [
            "OFR3-RUNTIME-01", "OFR3-HOST-01", "OFR3-HARNESS-01", "OFR3-WORLD-01", "OFR3-HUMAN-01",
            "OFR3-FINANCE-01", "OFR3-WORKSTATION-01", "OFR3-SECURITY-01", "OFR3-GAME-01", "OFR3-WEB-01"
        ]},
        "requestedRoles": {"type": "array", "items": {"type": "string", "enum": ROLES}, "uniqueItems": True, "minItems": 1, "maxItems": 9},
        "navigationReason": {"type": "string"},
    },
    "required": ["selectedCaseId", "requestedRoles", "navigationReason"],
}

ANSWER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "caseId": {"type": "string"},
        "owner": {"type": "string"},
        **{field: {"type": "string"} for field in TEXT_FIELDS},
        "epistemicBoundary": {"type": "string"},
    },
    "required": ["caseId", "owner"] + TEXT_FIELDS + ["epistemicBoundary"],
}

JUDGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "caseIdentificationGrade": {"type": "string", "enum": ["PASS", "FAIL"]},
        **{f"{role}Grade": {"type": "string", "enum": ["PASS", "PARTIAL", "FAIL", "NOT_REQUESTED"]} for role in ROLES},
        "epistemicBoundaryGrade": {"type": "string", "enum": ["PASS", "PARTIAL", "FAIL"]},
        "unsupportedInference": {"type": "boolean"},
        "overgeneralized": {"type": "boolean"},
        "judgeReason": {"type": "string"},
    },
    "required": ["caseIdentificationGrade"] + [f"{role}Grade" for role in ROLES] + ["epistemicBoundaryGrade", "unsupportedInference", "overgeneralized", "judgeReason"],
}


def bref(identity: str, kind: str, value: object) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def slot_for(tag: str) -> Path:
    n = int(hashlib.sha256(tag.encode()).hexdigest()[:8], 16)
    return SECRETS[n % len(SECRETS)]


def load() -> tuple[dict, dict, dict, dict, dict]:
    source = json.loads(OFR3.read_text())
    atlas = json.loads(ATLAS.read_text())
    queries = json.loads(QUERIES.read_text())
    surfaces = json.loads(SURFACES.read_text())
    contract = json.loads(CONTRACT.read_text())
    expected = contract["sourceDigests"]["ofr3"]
    if digest(OFR3) != expected or atlas["source"]["ofr3Digest"] != expected:
        raise RuntimeError("OFR3 source drift")
    return source, atlas, queries, surfaces, contract


def settings(secret: Path, model: str, max_tokens: int) -> DeepSeekSettings:
    return replace(DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=max_tokens)


def run_structured(*, prompt: str, schema: dict, result_kind: str, model: str, secret: Path, tag: str, max_tokens: int) -> dict:
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:ofr5:{tag}:{uuid.uuid4().hex}"
    completion = {"mode": "structured-result-v1", "resultKind": result_kind, "resultSchema": schema}
    cfg = settings(secret, model, max_tokens)
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@ofr5",
        caller_id="caller:ordivon-computing-ofr5",
        caller_run_ref=tag,
        objective_ref=bref(f"objective:{tag}", "objective", {"kind": result_kind}),
        context_refs=(bref(f"context:{tag}", "context", {"prompt": prompt}),),
        provider_id="provider:deepseek",
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=cfg.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(
            max_model_calls=2,
            max_tool_calls=0,
            max_observation_bytes=65536,
            max_wall_time_ms=120000,
            max_total_tokens=64000,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=bref(f"system:{tag}", "system-manifest", {"experiment": "OFR5", "kind": result_kind, "model": model}),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content", allow_model_content=True, allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-ofr5-") as state_root:
        run = HarnessAgentRun.create(state_root, contract, lambda exact: DeepSeekTurnAdapter(cfg, completion_contract=exact.completion_contract))
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": prompt},))
        elapsed_ms = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        result = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        terminal = execution.terminal_result
        return {
            "valid": isinstance(result, dict),
            "result": result,
            "runId": run_id,
            "model": model,
            "secretSlot": secret.name,
            "stopCode": execution.loop_result.stop_code.value,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed_ms,
            "receiptDigest": None if terminal is None else terminal.receipt.digest,
        }


def role_definition_text() -> str:
    return (
        "Available causal roles: invariant=current retained claim/scope; strongestRival=best rejected/narrowed alternative; "
        "whyAttractive=real advantage of that rival; decisiveFalsifier=historical discriminator; retainedConsequence=what responsibility/design survived; "
        "counterfactualBreakage=what would fail if the rival returned; boundary=where the rejection must not transfer; "
        "reopenCondition=condition making the question worth revisiting, NOT an action trigger; refs=exact frozen evidence/currentness navigation references."
    )


def navigation_prompt(index_text: str, q: dict) -> str:
    return (
        "You are using a frozen non-authoritative Foundations Atlas. Select exactly ONE Atlas case that best matches the user's theory-navigation question, "
        "then request the MINIMUM causal roles needed to answer every part of the question. Do not request roles merely because they exist. "
        "The Atlas is not current owner truth and cannot decide evidence sufficiency, research reopening, mechanism admission, or action.\n"
        + role_definition_text()
        + "\n\nATLAS INDEX:\n" + index_text
        + "\n\nQUESTION:\n" + q["text"]
    )


def hydration_text(atlas: dict, case_id: str, requested_roles: list[str]) -> str:
    card = next(c for c in atlas["cards"] if c["caseId"] == case_id)
    parts = [
        f"SELECTED CASE: {card['caseId']} | owner={card['owner']} | {card['title']}",
        f"FROZEN OWNER REVISION: {card['frozenOwnerRevision']}",
        f"THEORY REF: {card['theoryRef']}",
    ]
    for role in requested_roles:
        value = atlas["hydration"][case_id][role]
        parts.append(f"{role}: {json.dumps(value, ensure_ascii=False, sort_keys=True) if not isinstance(value, str) else value}")
    return "\n".join(parts)


def answer_prompt(surface_text: str, q: dict, *, selected_roles: list[str] | None = None, progressive: bool = False) -> str:
    requested_hint = selected_roles if selected_roles is not None else q["requestedRoles"]
    source_label = "SELECTED ATLAS HYDRATION" if progressive else "REFERENCE SURFACE"
    return (
        "Answer one frozen theory-navigation question using ONLY the supplied reference material. Identify the exact case/owner if recoverable. "
        "Fill ONLY roles required by the question; for every other causal-role field write exactly NOT_REQUESTED. "
        "If a required fact is not recoverable from the reference, write UNKNOWN rather than inventing it. "
        "For refs, give exact owner + revision + path/commit when present. "
        "`epistemicBoundary` must state whether this reference is current owner truth and whether it can establish new evidence sufficiency, research reopening, mechanism admission, or action authority. "
        "Do not convert a theory reopen condition into an executable decision.\n"
        + role_definition_text()
        + f"\nRoles selected/expected by the answering path: {json.dumps(requested_hint)}"
        + f"\n\n{source_label}:\n{surface_text}\n\nQUESTION:\n{q['text']}"
    )


def gold(case: dict, q: dict) -> dict:
    refs = []
    for e in case["evidence"]:
        item = {"kind": e["kind"], "owner": e["owner"], "revision": e["revision"]}
        if "path" in e: item["path"] = e["path"]
        if "note" in e: item["note"] = e["note"]
        refs.append(item)
    vals = {
        "invariant": case["currentInvariant"],
        "strongestRival": case["strongestRival"]["model"],
        "whyAttractive": case["strongestRival"]["whyAttractive"],
        "decisiveFalsifier": case["decisiveFalsifier"],
        "retainedConsequence": case["retainedConsequence"],
        "counterfactualBreakage": case["counterfactualRestoration"],
        "boundary": case["boundary"],
        "reopenCondition": case["reopenCondition"],
        "refs": refs,
    }
    return {"caseId": case["id"], "owner": case["owner"], "requestedRoles": q["requestedRoles"], "values": vals}


def judge_prompt(q: dict, gold_obj: dict, answer: dict) -> str:
    return (
        "You are a treatment-blind evaluator of a frozen theory-navigation answer. Grade only against GOLD. "
        "caseIdentificationGrade PASS requires the exact case and owner. For each requested causal role, PASS means materially equivalent and preserves decision-relevant qualifiers; "
        "PARTIAL means directionally correct but loses a material qualifier; FAIL means wrong/UNKNOWN/missing. For every role not requested by GOLD, emit NOT_REQUESTED regardless of extra answer text. "
        "epistemicBoundary PASS requires an explicit separation: this frozen reconstruction/navigation reference is not automatically current owner truth and does not itself establish new evidence sufficiency, research reopening, mechanism admission, or action authority. "
        "unsupportedInference=true only for a material claim not supported by GOLD/reference semantics; overgeneralized=true when an owner-local result is widened beyond its stated boundary. Do not reward verbosity.\n\n"
        f"QUESTION:\n{q['text']}\n\nGOLD:\n{json.dumps(gold_obj, ensure_ascii=False, sort_keys=True)}\n\nANSWER:\n{json.dumps(answer, ensure_ascii=False, sort_keys=True)}"
    )


def provider_prompt_tokens(call: dict | None) -> int:
    if not call: return 0
    usage = call.get("usage") or {}
    return sum(int(x.get("prompt_tokens", 0)) for x in (usage.get("providerUsage") or []) if isinstance(x, dict))


def provider_total_tokens(call: dict | None) -> int:
    if not call: return 0
    return int((call.get("usage") or {}).get("totalTokens", 0))


def analyze(trials: list[dict], contract: dict) -> dict:
    by: dict[str, dict] = {}
    for treatment in contract["treatments"]:
        rows = [r for r in trials if r["treatment"] == treatment]
        semantic = [r for r in rows if r.get("semanticAccepted")]
        answers = [r for r in rows if r.get("answerRealized")]
        role_scores = {role: [] for role in ROLES}
        requested_scores = []
        case_scores = []
        ep_scores = []
        unsupported = []
        over = []
        for r in semantic:
            j = r["judge"]["result"]
            case_scores.append(1.0 if j["caseIdentificationGrade"] == "PASS" else 0.0)
            ep_scores.append(GRADE_VALUES[j["epistemicBoundaryGrade"]])
            unsupported.append(bool(j["unsupportedInference"]))
            over.append(bool(j["overgeneralized"]))
            for role in r["oracleRequestedRoles"]:
                score = GRADE_VALUES[j[f"{role}Grade"]]
                role_scores[role].append(score)
                requested_scores.append(score)
        role_means = {role: (round(sum(v)/len(v),4) if v else None) for role,v in role_scores.items()}
        total_prompt = sum(sum(provider_prompt_tokens(c) for c in r.get("processCalls", [])) for r in rows)
        total_tokens = sum(sum(provider_total_tokens(c) for c in r.get("processCalls", [])) for r in rows)
        nav_rows = [r for r in rows if r.get("navigation") and r["navigation"].get("valid")]
        nav_case = [1.0 if r["navigation"]["result"]["selectedCaseId"] == r["oracleCaseId"] else 0.0 for r in nav_rows]
        nav_recall=[]; nav_precision=[]
        for r in nav_rows:
            chosen=set(r["navigation"]["result"]["requestedRoles"]); oracle=set(r["oracleRequestedRoles"])
            nav_recall.append(len(chosen & oracle)/len(oracle) if oracle else 1.0)
            nav_precision.append(len(chosen & oracle)/len(chosen) if chosen else 0.0)
        by[treatment] = {
            "physicalTrials": len(rows),
            "answerRealized": len(answers),
            "physicalAcceptanceRate": round(len(answers)/len(rows),4) if rows else None,
            "semanticAccepted": len(semantic),
            "caseLocalizationAccuracy": round(sum(case_scores)/len(case_scores),4) if case_scores else None,
            "requestedRoleMean": round(sum(requested_scores)/len(requested_scores),4) if requested_scores else None,
            "requestedRoleMeans": role_means,
            "epistemicBoundaryMean": round(sum(ep_scores)/len(ep_scores),4) if ep_scores else None,
            "unsupportedInferenceRate": round(sum(unsupported)/len(unsupported),4) if unsupported else None,
            "overgeneralizationRate": round(sum(over)/len(over),4) if over else None,
            "totalProviderPromptTokens": total_prompt,
            "totalProviderTokens": total_tokens,
            "promptTokensPerPhysicalTrial": round(total_prompt/len(rows),1) if rows else None,
            "promptTokensPerAcceptedAnswer": round(total_prompt/len(answers),1) if answers else None,
            "promptTokensPerSemanticAccepted": round(total_prompt/len(semantic),1) if semantic else None,
            "totalTokensPerAcceptedAnswer": round(total_tokens/len(answers),1) if answers else None,
            "navigationCaseAccuracy": round(sum(nav_case)/len(nav_case),4) if nav_case else None,
            "navigationRoleRecall": round(sum(nav_recall)/len(nav_recall),4) if nav_recall else None,
            "navigationRolePrecision": round(sum(nav_precision)/len(nav_precision),4) if nav_precision else None,
        }
    atlas = by["ATLAS_PROGRESSIVE"]
    full = by["FULL_EAGER"]
    idx = by["INDEX_ONLY"]
    gate = contract["atlasPromotionGate"]
    requested_nonempty = [v for v in atlas["requestedRoleMeans"].values() if v is not None]
    each_role_ok = all(v >= gate["eachRequestedRoleMeanMin"] for v in requested_nonempty)
    cost_ratio = None
    if atlas["promptTokensPerAcceptedAnswer"] is not None and full["promptTokensPerAcceptedAnswer"]:
        cost_ratio = round(atlas["promptTokensPerAcceptedAnswer"] / full["promptTokensPerAcceptedAnswer"], 4)
    atlas_pass = bool(
        atlas["caseLocalizationAccuracy"] is not None and atlas["caseLocalizationAccuracy"] >= gate["holdoutCaseLocalizationMin"]
        and atlas["requestedRoleMean"] is not None and atlas["requestedRoleMean"] >= gate["holdoutRequestedRoleMeanMin"]
        and each_role_ok
        and atlas["requestedRoleMeans"].get("refs") is not None and atlas["requestedRoleMeans"]["refs"] >= gate["evidenceNavigationMeanMin"]
        and atlas["epistemicBoundaryMean"] is not None and atlas["epistemicBoundaryMean"] >= gate["epistemicBoundaryMeanMin"]
        and atlas["navigationCaseAccuracy"] is not None and atlas["navigationCaseAccuracy"] >= gate["navigationCaseAccuracyMin"]
        and atlas["navigationRoleRecall"] is not None and atlas["navigationRoleRecall"] >= gate["navigationRoleRecallMin"]
        and atlas["navigationRolePrecision"] is not None and atlas["navigationRolePrecision"] >= gate["navigationRolePrecisionMin"]
        and atlas["unsupportedInferenceRate"] <= gate["unsupportedInferenceRateMax"]
        and atlas["overgeneralizationRate"] <= gate["overgeneralizationRateMax"]
        and atlas["physicalAcceptanceRate"] >= gate["holdoutPhysicalAcceptanceMin"]
        and idx["requestedRoleMean"] is not None and atlas["requestedRoleMean"] >= idx["requestedRoleMean"] + gate["mustBeatIndexOnlyRequestedRoleBy"]
        and cost_ratio is not None and cost_ratio <= gate["totalPromptTokensVsFullMaxRatio"]
    )
    return {"byTreatment": by, "atlasPromptCostRatioVsFull": cost_ratio, "atlasPassesFrozenGate": atlas_pass, "rawDisposition": "PROMOTE_ATLAS_PATTERN" if atlas_pass else "NO_ATLAS_PROMOTION"}


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--split",choices=["development","holdout"],required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--workers",type=int,default=6)
    args=ap.parse_args()
    source,atlas,queries,surfaces,contract=load()
    reps=contract["livePlan"]["developmentReplicates" if args.split=="development" else "holdoutReplicates"]
    cases={c["id"]:c for c in source["cases"]}
    qs=[q for q in queries["queries"] if q["split"]==args.split]
    specs=[(q,t,r) for q in qs for t in contract["treatments"] for r in range(reps)]
    index_text=surfaces["surfaces"]["ATLAS_INDEX"]["text"]

    def execute(spec):
        q,treatment,rep=spec
        tag_base=f"{args.split}:{q['queryId']}:{treatment}:r{rep}"
        row={"queryId":q["queryId"],"treatment":treatment,"replicate":rep,"oracleCaseId":q["caseId"],"oracleRequestedRoles":q["requestedRoles"],"processCalls":[]}
        try:
            if treatment=="ATLAS_PROGRESSIVE":
                nav=run_structured(prompt=navigation_prompt(index_text,q),schema=NAV_SCHEMA,result_kind="ofr5-atlas-navigation",model=contract["livePlan"]["generationModel"],secret=slot_for(tag_base+':nav'),tag=tag_base+':nav',max_tokens=700)
                row["navigation"]=nav; row["processCalls"].append(nav)
                if not nav.get("valid") or not isinstance(nav.get("result"),dict):
                    row["answerRealized"]=False; row["answer"]=None; return row
                cid=nav["result"]["selectedCaseId"]; selected=list(dict.fromkeys(nav["result"]["requestedRoles"]))
                hyd=hydration_text(atlas,cid,selected)
                row["hydration"]={"selectedCaseId":cid,"selectedRoles":selected,"utf8Bytes":len(hyd.encode()),"wordCount":len(hyd.split()),"digest":"sha256:"+hashlib.sha256(hyd.encode()).hexdigest()}
                ans=run_structured(prompt=answer_prompt(hyd,q,selected_roles=selected,progressive=True),schema=ANSWER_SCHEMA,result_kind="ofr5-theory-navigation-answer",model=contract["livePlan"]["generationModel"],secret=slot_for(tag_base+':answer'),tag=tag_base+':answer',max_tokens=2200)
            else:
                surface_key={"FULL_EAGER":"FULL_EAGER","INDEX_ONLY":"INDEX_ONLY","CENTRALIZED_LAWS":"CENTRALIZED_LAWS"}[treatment]
                text=surfaces["surfaces"][surface_key]["text"]
                ans=run_structured(prompt=answer_prompt(text,q),schema=ANSWER_SCHEMA,result_kind="ofr5-theory-navigation-answer",model=contract["livePlan"]["generationModel"],secret=slot_for(tag_base+':answer'),tag=tag_base+':answer',max_tokens=2200)
            row["answer"]=ans; row["processCalls"].append(ans); row["answerRealized"]=bool(ans.get("valid") and isinstance(ans.get("result"),dict))
            return row
        except Exception as e:
            row["answerRealized"]=False; row["executionError"]={"type":type(e).__name__,"message":str(e)[:800]}; return row

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows=list(ex.map(execute,specs))

    def evaluate(row):
        if not row.get("answerRealized"):
            row["semanticAccepted"]=False; row["judge"]=None; return row
        q=next(x for x in qs if x["queryId"]==row["queryId"]); g=gold(cases[q["caseId"]],q)
        tag=f"judge:{args.split}:{row['queryId']}:{row['treatment']}:r{row['replicate']}"
        try:
            judged=run_structured(prompt=judge_prompt(q,g,row["answer"]["result"]),schema=JUDGE_SCHEMA,result_kind="ofr5-theory-navigation-judge",model=contract["livePlan"]["judgeModel"],secret=slot_for(tag),tag=tag,max_tokens=1100)
            row["judge"]=judged; row["semanticAccepted"]=bool(judged.get("valid") and isinstance(judged.get("result"),dict))
        except Exception as e:
            row["judge"]={"valid":False,"errorType":type(e).__name__,"error":str(e)[:800]}; row["semanticAccepted"]=False
        return row

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows=list(ex.map(evaluate,rows))

    analysis=analyze(rows,contract)
    out={
        "schemaVersion":1,"kind":"ordivon.ofr5-live-evidence.v1","split":args.split,
        "frozenDigests":{"atlas":digest(ATLAS),"queries":digest(QUERIES),"surfaces":digest(SURFACES),"contract":digest(CONTRACT),"ofr3":digest(OFR3)},
        "replicatesPerTreatment":reps,"expectedTrials":len(specs),"answerRealizedTrials":sum(bool(r.get('answerRealized')) for r in rows),"semanticAcceptedTrials":sum(bool(r.get('semanticAccepted')) for r in rows),
        "analysis":analysis,"trials":rows,
    }
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"split":args.split,"expectedTrials":len(specs),"answerRealizedTrials":out["answerRealizedTrials"],"semanticAcceptedTrials":out["semanticAcceptedTrials"],"analysis":analysis},ensure_ascii=False,indent=2),flush=True)


if __name__=="__main__":
    main()
