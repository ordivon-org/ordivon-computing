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
UNIVERSE = ROOT / "candidate-universe-v1.json"
CONTRACT = ROOT / "promotion-contract-v1.json"
FREEZE = ROOT / "freeze-v1.json"
CORE = ROOT.parents[2] / "core" / "foundations.md"
PRIMITIVES = ROOT.parents[2] / "core" / "primitives.md"
SECRETS = [Path(f"/root/.config/ordivon/secrets/deepseek{suffix}.json") for suffix in ["", "1", "2", "3", "4", "5"]]
DESTINATIONS = ["CORE_EXISTING", "CORE_REFINE", "KNOWLEDGE", "RESEARCH", "OWNER_LOCAL", "DELETE_CONTRACT"]
REVIEWERS = {
    "minimal-core-architect": "Prefer the smallest generative Core. Detect when a candidate is already covered, when a Knowledge explanation is enough, and when a new Core sentence genuinely changes reusable architecture. Do not reward elegance or recurrence by itself.",
    "deletion-falsification-skeptic": "Assume shared promotion is guilty until evidence clears it. Search for pseudoreplication, owner-specific leakage, treatment/model specificity, duplicate wording, invalid authority transfer, and failed controls that should be contracted or left Research-only.",
    "knowledge-curator": "Optimize reconstructability without Core bloat. Distinguish compact generative foundations from reusable explanatory Knowledge and owner-local causal history. Preserve falsifiers, negative-transfer boundaries, and exact evidence escape hatches.",
}
GROUPS = {
    "G1A": ["C1", "C2", "C3"],
    "G1B": ["C4", "C5", "C6"],
    "G2A": ["C7", "C8", "C9"],
    "G2B": ["C10", "C11", "C12"],
    "G3A": ["M13", "M14", "M15"],
    "G3B": ["M16", "M17", "M18"],
}


def bref(identity: str, kind: str, value: object) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def slot_for(tag: str) -> Path:
    n = int(hashlib.sha256(tag.encode()).hexdigest()[:8], 16)
    return SECRETS[n % len(SECRETS)]


def settings(secret: Path) -> DeepSeekSettings:
    return replace(DeepSeekSettings.from_secret_file(secret), model="deepseek-v4-pro", max_output_tokens=5000)


def result_schema(ids: list[str]) -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "decisions": {
                "type": "array",
                "minItems": len(ids),
                "maxItems": len(ids),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "candidateId": {"type": "string", "enum": ids},
                        "destination": {"type": "string", "enum": DESTINATIONS},
                        "strongestReason": {"type": "string", "maxLength": 900},
                        "strongestCounterargument": {"type": "string", "maxLength": 700},
                        "redundancyOrMutation": {"type": "string", "maxLength": 900},
                        "mechanismPromotionForbidden": {"type": "boolean"},
                    },
                    "required": ["candidateId", "destination", "strongestReason", "strongestCounterargument", "redundancyOrMutation", "mechanismPromotionForbidden"],
                },
            },
            "groupDiagnosis": {"type": "string", "maxLength": 1000},
        },
        "required": ["decisions", "groupDiagnosis"],
    }


def run_structured(prompt: str, schema: dict, tag: str) -> dict:
    secret = slot_for(tag)
    cfg = settings(secret)
    completion = {"mode": "structured-result-v1", "resultKind": "ofr6-advisory-panel", "resultSchema": schema}
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:ofr6:{tag}:{uuid.uuid4().hex}"
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@ofr6",
        caller_id="caller:ordivon-computing-ofr6",
        caller_run_ref=tag,
        objective_ref=bref(f"objective:{tag}", "objective", {"kind": "ofr6-advisory"}),
        context_refs=(bref(f"context:{tag}", "context", {"prompt": prompt}),),
        provider_id="provider:deepseek",
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=cfg.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(max_model_calls=2, max_tool_calls=0, max_observation_bytes=65536, max_wall_time_ms=180000, max_total_tokens=64000, max_model_retries=1, max_conclusion_corrections=1).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=bref(f"system:{tag}", "system-manifest", {"experiment": "OFR6", "reviewer": tag}),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content", allow_model_content=True, allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-ofr6-") as state_root:
        run = HarnessAgentRun.create(state_root, contract, lambda exact: DeepSeekTurnAdapter(cfg, completion_contract=exact.completion_contract))
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": prompt},))
        elapsed = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        result = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        return {
            "valid": isinstance(result, dict),
            "result": result,
            "runId": run_id,
            "model": cfg.model,
            "secretSlot": secret.name,
            "stopCode": execution.loop_result.stop_code.value,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed,
        }


def make_prompt(reviewer: str, group: str, cards: list[dict], contract: dict) -> str:
    core_text = CORE.read_text()
    primitive_text = PRIMITIVES.read_text()
    return f"""You are one advisory reviewer in OFR6, a frozen promotion/localization/deletion court for Ordivon's reconstructed foundations.

REVIEWER ROLE: {reviewer}
ROLE DISCIPLINE: {REVIEWERS[reviewer]}

Your output is challenge evidence only. You have NO authority to mutate Core/Knowledge or owner truth. Apply the frozen categorical contract; do not invent a scalar maturity score. A strong candidate may belong in Knowledge rather than Core. A candidate already materially represented in Core should normally be CORE_EXISTING or CORE_REFINE, not a duplicate new law. OWNER_LOCAL is appropriate when the proposed shared claim still smuggles product-specific meaning. DELETE_CONTRACT means contract/delete the active shared representation while preserving historical evidence.

FROZEN PROMOTION CONTRACT:
{json.dumps(contract, ensure_ascii=False, indent=2)}

CURRENT CORE FOUNDATIONS (exact frozen text):
{core_text}

CURRENT CORE PRIMITIVES (exact frozen text):
{primitive_text}

CANDIDATES IN {group}:
{json.dumps(cards, ensure_ascii=False, indent=2)}

For every candidate, choose exactly one destination and give only the strongest reason, strongest counterargument, and exact redundancy/mutation target. Keep each concise. `mechanismPromotionForbidden=true` whenever the semantic promotion would NOT justify a daemon/database/schema/service/automatic authority mechanism. Be conservative and explicit about duplication.
"""


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--output", required=True); ap.add_argument("--workers", type=int, default=6); args=ap.parse_args()
    universe = json.loads(UNIVERSE.read_text()); contract = json.loads(CONTRACT.read_text()); freeze = json.loads(FREEZE.read_text())
    for n,d in freeze["files"].items():
        if digest(ROOT/n) != d: raise RuntimeError(f"freeze drift: {n}")
    by_id = {c["id"]: c for c in universe["candidates"]}
    specs=[]
    for group,ids in GROUPS.items():
        cards=[by_id[i] for i in ids]
        for reviewer in REVIEWERS: specs.append((group,ids,cards,reviewer))
    def one(spec):
        group,ids,cards,reviewer=spec
        tag=f"{group}:{reviewer}"
        try:
            call=run_structured(make_prompt(reviewer,group,cards,contract),result_schema(ids),tag)
            if call.get('valid'):
                got=[x['candidateId'] for x in call['result']['decisions']]
                call['candidateSetExact']=(len(got)==len(ids) and set(got)==set(ids) and len(got)==len(set(got)))
            else: call['candidateSetExact']=False
            return {'group':group,'reviewer':reviewer,'candidateIds':ids,'call':call}
        except Exception as e:
            return {'group':group,'reviewer':reviewer,'candidateIds':ids,'call':{'valid':False,'candidateSetExact':False,'errorType':type(e).__name__,'error':str(e)[:1000]}}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex: rows=list(ex.map(one,specs))
    counts={}
    disagreements={}
    for cid in by_id:
        votes=[]
        for row in rows:
            if row['call'].get('valid') and row['call'].get('candidateSetExact'):
                for d in row['call']['result']['decisions']:
                    if d['candidateId']==cid: votes.append(d['destination'])
        counts[cid]={x:votes.count(x) for x in DESTINATIONS if votes.count(x)}
        disagreements[cid]=len(set(votes))>1
    out={'schemaVersion':1,'kind':'ordivon.ofr6-advisory-panel.v1','promotionAuthority':False,'freezeDigests':freeze['files'],'expectedCalls':len(specs),'validCalls':sum(bool(r['call'].get('valid') and r['call'].get('candidateSetExact')) for r in rows),'voteCounts':counts,'hasReviewerDisagreement':disagreements,'reviews':rows}
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'expectedCalls':len(specs),'validCalls':out['validCalls'],'voteCounts':counts,'disagreements':[k for k,v in disagreements.items() if v]},ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
