from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import tempfile
import time
import uuid
from collections import defaultdict
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
SOURCE = ROOT.parent / "foundations-reconstruction-ofr3-v0" / "causal-reconstruction-v1.json"
CONTRACT = ROOT / "experiment-contract-v1.json"
CORPUS = ROOT / "corpus-v1.json"
PACKETS = ROOT / "packets-v1.json"
SECRETS = [Path(f"/root/.config/ordivon/secrets/deepseek{suffix}.json") for suffix in ["", "1", "2", "3", "4", "5"]]
ROLE_FIELDS = [
    "invariantScope",
    "strongestRival",
    "whyAttractive",
    "decisiveFalsifier",
    "retainedConsequence",
    "counterfactualBreakage",
    "negativeTransferBoundary",
    "reopenCondition",
]
CRITICAL = ["strongestRival", "decisiveFalsifier", "counterfactualBreakage", "negativeTransferBoundary", "reopenCondition"]

GEN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        **{name: {"type": "string"} for name in ROLE_FIELDS},
        "reopenDecision": {"type": "string", "enum": ["REOPEN", "KEEP_CLOSED"]},
        "reopenDecisionReason": {"type": "string"},
        "uncertainty": {"type": "string"},
    },
    "required": ROLE_FIELDS + ["reopenDecision", "reopenDecisionReason", "uncertainty"],
}

JUDGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        **{f"{name}Grade": {"type": "string", "enum": ["PASS", "PARTIAL", "FAIL"]} for name in ROLE_FIELDS},
        "unsupportedInference": {"type": "boolean"},
        "overgeneralized": {"type": "boolean"},
        "judgeReason": {"type": "string"},
    },
    "required": [f"{name}Grade" for name in ROLE_FIELDS] + ["unsupportedInference", "overgeneralized", "judgeReason"],
}


def ref(identity: str, kind: str, value: object) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def load() -> tuple[dict, dict, dict, dict]:
    source = json.loads(SOURCE.read_text())
    contract = json.loads(CONTRACT.read_text())
    corpus = json.loads(CORPUS.read_text())
    packets = json.loads(PACKETS.read_text())
    expected = contract["source"]["digest"]
    actual = "sha256:" + hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if expected != actual or packets["sourceDigest"] != actual:
        raise RuntimeError(f"source digest drift: expected {expected}, actual {actual}")
    return source, contract, corpus, packets


def settings(secret: Path, model: str, max_tokens: int) -> DeepSeekSettings:
    return replace(DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=max_tokens)


def run_structured(*, prompt: str, schema: dict, result_kind: str, model: str, secret: Path, tag: str, max_tokens: int) -> dict:
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:ofr4:{tag}:{uuid.uuid4().hex}"
    completion = {"mode": "structured-result-v1", "resultKind": result_kind, "resultSchema": schema}
    cfg = settings(secret, model, max_tokens)
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@ofr4",
        caller_id="caller:ordivon-computing-ofr4",
        caller_run_ref=tag,
        objective_ref=ref(f"objective:{tag}", "objective", {"kind": result_kind}),
        context_refs=(ref(f"context:{tag}", "context", {"prompt": prompt}),),
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
            max_total_tokens=24000,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(f"system:{tag}", "system-manifest", {"experiment": "OFR4", "resultKind": result_kind, "model": model}),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content", allow_model_content=True, allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-ofr4-") as state_root:
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


def generation_prompt(packet: str, scenario: str) -> str:
    return (
        "You are a fresh Agent evaluating one bounded Ordivon theory packet. Use ONLY the supplied packet. "
        "You have no repository, search, prior conversation, or hidden evidence. Reconstruct the causal knowledge the packet supports. "
        "Causal inference from stated relations is allowed; unsupported invention is not. If a requested role cannot be recovered, write exactly UNKNOWN. "
        "Do not universalize a local result. Distinguish the historical discriminator from the failure predicted if the rival returns now. "
        "Then decide whether the reopen probe meets the packet's current burden for reconsidering the rejected alternative.\n\n"
        f"THEORY PACKET:\n{packet}\n\nREOPEN PROBE:\n{scenario}"
    )


def gold_for(case: dict) -> dict:
    return {
        "invariantScope": case["currentInvariant"],
        "strongestRival": case["strongestRival"]["model"],
        "whyAttractive": case["strongestRival"]["whyAttractive"],
        "decisiveFalsifier": case["decisiveFalsifier"],
        "retainedConsequence": case["retainedConsequence"],
        "counterfactualBreakage": case["counterfactualRestoration"],
        "negativeTransferBoundary": case["boundary"],
        "reopenCondition": case["reopenCondition"],
    }


def judge_prompt(packet: str, gold: dict, scenario: str, answer: dict) -> str:
    return (
        "You are an independent treatment-blind evaluator. Grade whether a fresh Agent reconstructed the GOLD causal roles from the exact PACKET it received. "
        "For each role: PASS = materially equivalent and preserves the important distinction; PARTIAL = directionally correct but loses a decision-relevant qualifier; FAIL = wrong, contradictory, UNKNOWN, or misses the role. "
        "unsupportedInference=true only when the answer asserts a material claim not supported by the packet and not a valid causal inference from it. "
        "overgeneralized=true when a local/conditional result is turned into a broader prohibition/law than GOLD permits. Do not reward verbosity. Treatment identity is intentionally absent.\n\n"
        f"PACKET:\n{packet}\n\nGOLD:\n{json.dumps(gold, ensure_ascii=False, sort_keys=True)}\n\nREOPEN PROBE:\n{scenario}\n\nAGENT ANSWER:\n{json.dumps(answer, ensure_ascii=False, sort_keys=True)}"
    )


def analyze(trials: list[dict], contract: dict) -> dict:
    val = contract["scoring"]["roleValues"]
    by = {}
    for treatment in contract["treatments"]:
        rows = [r for r in trials if r.get("treatment") == treatment and r.get("semanticAccepted")]
        role_means = {}
        for role in ROLE_FIELDS:
            grades = [r["judge"]["result"][f"{role}Grade"] for r in rows]
            role_means[role] = round(sum(val[g] for g in grades) / len(grades), 4) if grades else None
        all_scores = [role_means[r] for r in ROLE_FIELDS if role_means[r] is not None]
        critical_scores = [role_means[r] for r in CRITICAL if role_means[r] is not None]
        reopen = [r["reopenDecisionCorrect"] for r in rows]
        unsupported = [r["judge"]["result"]["unsupportedInference"] for r in rows]
        over = [r["judge"]["result"]["overgeneralized"] for r in rows]
        def prompt_token_count(row):
            usage = row["generation"].get("usage") or {}
            provider = usage.get("providerUsage") or []
            return sum(int(item.get("prompt_tokens", 0)) for item in provider if isinstance(item, dict))
        prompt_tokens = [prompt_token_count(r) for r in rows]
        total_tokens = [int((r["generation"].get("usage") or {}).get("totalTokens", 0)) for r in rows]
        by[treatment] = {
            "accepted": len(rows),
            "roleMeans": role_means,
            "overallRoleScore": round(sum(all_scores) / len(all_scores), 4) if all_scores else None,
            "criticalRoleScore": round(sum(critical_scores) / len(critical_scores), 4) if critical_scores else None,
            "reopenDecisionAccuracy": round(sum(reopen) / len(reopen), 4) if reopen else None,
            "unsupportedInferenceRate": round(sum(unsupported) / len(unsupported), 4) if unsupported else None,
            "overgeneralizationRate": round(sum(over) / len(over), 4) if over else None,
            "meanPromptTokens": round(sum(prompt_tokens) / len(prompt_tokens), 1) if prompt_tokens else None,
            "meanGenerationTokens": round(sum(total_tokens) / len(total_tokens), 1) if total_tokens else None,
        }
    scores = [v["overallRoleScore"] for v in by.values() if v["overallRoleScore"] is not None]
    best = max(scores) if scores else None
    q = contract["scoring"]["qualification"]
    qualifying = []
    for name, row in by.items():
        if row["overallRoleScore"] is None or best is None:
            row["qualifies"] = False
            continue
        each_critical = all((row["roleMeans"][role] or 0) >= q["eachCriticalRoleMeanMin"] for role in CRITICAL)
        row["qualifies"] = (
            row["criticalRoleScore"] >= q["criticalRoleMeanMin"]
            and each_critical
            and row["reopenDecisionAccuracy"] >= q["reopenDecisionAccuracyMin"]
            and row["unsupportedInferenceRate"] <= q["unsupportedInferenceRateMax"]
            and row["overgeneralizationRate"] <= q["overgeneralizationRateMax"]
            and row["overallRoleScore"] >= best - q["withinBestOverallRoleScore"]
        )
        if row["qualifies"]:
            qualifying.append((row["meanPromptTokens"], name))
    selected = min(qualifying)[1] if qualifying else "NO_PROMOTION"
    return {"byTreatment": by, "bestOverallRoleScore": best, "selected": selected}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["development", "holdout"], required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    source, contract, corpus, packets = load()
    reps = contract["livePlan"]["developmentReplicates" if args.split == "development" else "holdoutReplicates"]
    cases = {c["id"]: c for c in source["cases"]}
    corpus_cases = {c["caseId"]: c for c in corpus["cases"] if c["split"] == args.split}
    packet_map = {(p["caseId"], p["treatment"]): p for p in packets["packets"] if p["split"] == args.split}
    specs = []
    for case_id, meta in corpus_cases.items():
        for treatment in contract["treatments"]:
            for replicate in range(reps):
                specs.append((case_id, treatment, replicate, meta, packet_map[(case_id, treatment)]))

    def generate(spec):
        case_id, treatment, replicate, meta, packet = spec
        secret = SECRETS[(abs(hash((case_id, treatment, replicate))) % len(SECRETS))]
        tag = f"gen:{args.split}:{case_id}:{treatment}:r{replicate}"
        try:
            out = run_structured(prompt=generation_prompt(packet["text"], meta["reopenProbe"]), schema=GEN_SCHEMA, result_kind="ofr4-causal-reconstruction", model=contract["livePlan"]["generationModel"], secret=secret, tag=tag, max_tokens=1800)
            return {"caseId": case_id, "treatment": treatment, "replicate": replicate, "packetDigest": packet["textDigest"], "generation": out}
        except Exception as e:
            return {"caseId": case_id, "treatment": treatment, "replicate": replicate, "packetDigest": packet["textDigest"], "generation": {"valid": False, "errorType": type(e).__name__, "error": str(e)[:800]}}

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        generated = list(ex.map(generate, specs))

    gen_index = {(r["caseId"], r["treatment"], r["replicate"]): r for r in generated}

    def judge(spec):
        case_id, treatment, replicate, meta, packet = spec
        row = gen_index[(case_id, treatment, replicate)]
        answer = row["generation"].get("result")
        if not row["generation"].get("valid") or not isinstance(answer, dict):
            row["semanticAccepted"] = False
            row["judge"] = None
            row["reopenDecisionCorrect"] = None
            return row
        secret = SECRETS[(abs(hash(("judge", case_id, treatment, replicate))) % len(SECRETS))]
        tag = f"judge:{args.split}:{case_id}:r{replicate}:{uuid.uuid4().hex[:8]}"
        try:
            judged = run_structured(prompt=judge_prompt(packet["text"], gold_for(cases[case_id]), meta["reopenProbe"], answer), schema=JUDGE_SCHEMA, result_kind="ofr4-causal-reconstruction-judge", model=contract["livePlan"]["judgeModel"], secret=secret, tag=tag, max_tokens=1500)
            row["judge"] = judged
            row["semanticAccepted"] = bool(judged.get("valid") and isinstance(judged.get("result"), dict))
            row["reopenDecisionCorrect"] = answer.get("reopenDecision") == meta["reopenOracle"]
        except Exception as e:
            row["semanticAccepted"] = False
            row["judge"] = {"valid": False, "errorType": type(e).__name__, "error": str(e)[:800]}
            row["reopenDecisionCorrect"] = answer.get("reopenDecision") == meta["reopenOracle"]
        return row

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        trials = list(ex.map(judge, specs))

    analysis = analyze(trials, contract)
    failures = [r for r in trials if not r.get("semanticAccepted")]
    out = {
        "schemaVersion": 1,
        "kind": "ordivon.ofr4-live-evidence.v1",
        "split": args.split,
        "sourceDigest": contract["source"]["digest"],
        "contractDigest": "sha256:" + hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "corpusDigest": "sha256:" + hashlib.sha256(CORPUS.read_bytes()).hexdigest(),
        "packetsDigest": "sha256:" + hashlib.sha256(PACKETS.read_bytes()).hexdigest(),
        "replicatesPerTreatment": reps,
        "expectedTrials": len(specs),
        "semanticAcceptedTrials": len(trials) - len(failures),
        "failures": [{k: r.get(k) for k in ["caseId", "treatment", "replicate"]} | {"generation": r.get("generation"), "judge": r.get("judge")} for r in failures],
        "analysis": analysis,
        "trials": trials,
    }
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"split": args.split, "expectedTrials": len(specs), "semanticAcceptedTrials": out["semanticAcceptedTrials"], "failures": len(failures), "analysis": analysis}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
