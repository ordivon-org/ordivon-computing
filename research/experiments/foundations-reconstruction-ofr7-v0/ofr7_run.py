from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import random
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
CONTRACT = ROOT / "experiment-contract-v1.json"
CORPUS = ROOT / "corpus-v1.json"
SURFACES = ROOT / "surfaces-v1.json"
FREEZE = ROOT / "freeze-v1.json"
SECRETS = [Path(f"/root/.config/ordivon/secrets/deepseek{suffix}.json") for suffix in ["", "1", "2", "3", "4", "5"]]

TRUTH_STATES = ["KNOWN_TRUE", "KNOWN_FALSE", "UNKNOWN", "NOT_APPLICABLE"]
IDENTITY_STATES = ["SAME", "DIFFERENT", "UNKNOWN", "NOT_APPLICABLE"]
EVIDENCE_AUTHORITIES = [
    "OWNER_CURRENT_FACT",
    "INSUFFICIENT_CURRENT_EVIDENCE",
    "THEORY_OR_HISTORY_ONLY",
    "DERIVED_OR_HISTORICAL_NONAUTHORITATIVE",
    "NOT_APPLICABLE",
]

GEN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "primaryChoice": {"type": "string", "enum": ["A", "B", "C", "D"]},
        "truthState": {"type": "string", "enum": TRUTH_STATES},
        "identityState": {"type": "string", "enum": IDENTITY_STATES},
        "evidenceAuthority": {"type": "string", "enum": EVIDENCE_AUTHORITIES},
        "seekMoreEvidence": {"type": "boolean"},
        "reason": {"type": "string", "maxLength": 1000},
        "boundary": {"type": "string", "maxLength": 700},
    },
    "required": [
        "primaryChoice",
        "truthState",
        "identityState",
        "evidenceAuthority",
        "seekMoreEvidence",
        "reason",
        "boundary",
    ],
}


def ref(identity: str, kind: str, value: object) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def validate_freeze() -> tuple[dict, dict, dict]:
    freeze = json.loads(FREEZE.read_text())
    for name, digest in freeze["files"].items():
        actual = sha(ROOT / name)
        if actual != digest:
            raise RuntimeError(f"semantic freeze drift {name}: {actual} != {digest}")
    corpus = json.loads(CORPUS.read_text())
    surfaces = json.loads(SURFACES.read_text())
    contract = json.loads(CONTRACT.read_text())
    for name, digest in freeze["surfaceDigests"].items():
        if surfaces["treatments"][name]["digest"] != digest:
            raise RuntimeError(f"surface digest drift: {name}")
    return corpus, surfaces, contract


def secret_for(tag: str) -> Path:
    slot = int(hashlib.sha256(tag.encode()).hexdigest()[:8], 16) % len(SECRETS)
    return SECRETS[slot]


def settings(secret: Path, model: str, max_tokens: int) -> DeepSeekSettings:
    return replace(DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=max_tokens)


def run_structured(*, prompt: str, schema: dict, result_kind: str, model: str, tag: str, max_tokens: int, max_wall_ms: int = 150000) -> dict:
    cfg = settings(secret_for(tag), model, max_tokens)
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:ofr7:{tag}:{uuid.uuid4().hex}"
    completion = {"mode": "structured-result-v1", "resultKind": result_kind, "resultSchema": schema}
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@ofr7",
        caller_id="caller:ordivon-computing-ofr7",
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
            max_wall_time_ms=max_wall_ms,
            max_total_tokens=100000,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(f"system:{tag}", "system-manifest", {"experiment": "OFR7", "resultKind": result_kind, "model": model}),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content", allow_model_content=True, allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-ofr7-") as state_root:
        run = HarnessAgentRun.create(state_root, contract, lambda exact: DeepSeekTurnAdapter(cfg, completion_contract=exact.completion_contract))
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": prompt},))
        elapsed = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        result = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        terminal = execution.terminal_result
        return {
            "valid": isinstance(result, dict),
            "result": result,
            "runId": run_id,
            "model": model,
            "secretSlot": secret_for(tag).name,
            "stopCode": execution.loop_result.stop_code.value,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed,
            "receiptDigest": None if terminal is None else terminal.receipt.digest,
        }


def generation_prompt(case: dict, surface: dict) -> str:
    public_case = {
        "title": case["title"],
        "facts": case["facts"],
        "options": case["options"],
    }
    return (
        "You are a fresh Agent making one bounded decision. You have no repository, prior conversation, search, or hidden evidence. "
        "Treat CASE FACTS as the exact facts available for this decision. A supplied THEORY SURFACE is non-authoritative guidance only: "
        "it may help you reason, but it cannot create current owner facts, permissions, occurrence, or evidence that the case did not provide. "
        "Choose the best option A-D. Preserve UNKNOWN when evidence cannot distinguish action-relevant states; do not invent missing authority. "
        "For truthState, report the case's relevant proposition as KNOWN_TRUE/KNOWN_FALSE/UNKNOWN, or NOT_APPLICABLE if the case is not asking a truth-state distinction. "
        "For identityState, use SAME/DIFFERENT/UNKNOWN only when identity continuity is materially at issue. "
        "For evidenceAuthority, classify the decisive evidence role using the exact enum; this is about the current decision, not which document is longer. "
        "seekMoreEvidence=true only when additional current evidence is required before the selected decision can be completed safely/correctly. "
        "Keep reason and boundary concise; do not quote the theory surface at length.\n\n"
        f"THEORY SURFACE ROLE: {surface['role']}\n"
        f"THEORY SURFACE (non-authoritative):\n{surface['text']}\n\n"
        f"CASE:\n{json.dumps(public_case, ensure_ascii=False, sort_keys=True)}"
    )


def judge_schema(answer_ids: list[str]) -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "grades": {
                "type": "array",
                "minItems": len(answer_ids),
                "maxItems": len(answer_ids),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "answerId": {"type": "string", "enum": answer_ids},
                        "causalGrade": {"type": "string", "enum": ["PASS", "PARTIAL", "FAIL"]},
                        "unsupportedInference": {"type": "boolean"},
                        "overgeneralized": {"type": "boolean"},
                        "authorityConfusion": {"type": "boolean"},
                        "reason": {"type": "string", "maxLength": 350},
                    },
                    "required": ["answerId", "causalGrade", "unsupportedInference", "overgeneralized", "authorityConfusion", "reason"],
                },
            },
        },
        "required": ["grades"],
    }


def anonymize(case_id: str, treatment: str, model: str) -> str:
    return "ans-" + hashlib.sha256(f"{case_id}|{treatment}|{model}|ofr7-blind".encode()).hexdigest()[:12]


def judge_prompt(case: dict, anonymized_answers: list[dict]) -> str:
    gold = case["gold"]
    public_case = {"title": case["title"], "facts": case["facts"], "options": case["options"]}
    judge_gold = {
        "causalGold": gold["causalGold"],
        "forbiddenClaims": gold["forbiddenClaims"],
        "goldPrimaryChoice": gold["primaryChoice"],
    }
    return (
        "You are a treatment-blind evaluator. The answers below were produced by fresh Agents under hidden conditions. "
        "Do not infer or reward treatment/model identity. Grade only the reasoning in `reason` and `boundary` against CASE FACTS and GOLD CAUSAL BOUNDARY. "
        "PASS = preserves the decision-relevant causal mechanism and boundary; PARTIAL = directionally right but loses a material qualifier; FAIL = wrong mechanism, circular restatement, or material boundary loss. "
        "unsupportedInference=true when the reasoning asserts a material fact/authority/occurrence not supplied by the case. "
        "overgeneralized=true when it turns a local conditional result into a broader rule than the gold permits. "
        "authorityConfusion=true when it makes theory/projection/capability/credential/local execution substitute for the current owner/evidence/commitment authority relevant to this case. "
        "Primary option correctness is scored mechanically elsewhere; use it only as context, not as a substitute for causal grading.\n\n"
        f"CASE:\n{json.dumps(public_case, ensure_ascii=False, sort_keys=True)}\n\n"
        f"GOLD CAUSAL BOUNDARY:\n{json.dumps(judge_gold, ensure_ascii=False, sort_keys=True)}\n\n"
        f"ANONYMIZED ANSWERS:\n{json.dumps(anonymized_answers, ensure_ascii=False, sort_keys=True)}"
    )


def provider_prompt_tokens(call: dict) -> int:
    usage = call.get("usage") or {}
    rows = usage.get("providerUsage") or []
    return sum(int(row.get("prompt_tokens", 0)) for row in rows if isinstance(row, dict))


def provider_cache_hit_tokens(call: dict) -> int:
    usage = call.get("usage") or {}
    rows = usage.get("providerUsage") or []
    return sum(int(row.get("prompt_cache_hit_tokens", 0)) for row in rows if isinstance(row, dict))


def total_tokens(call: dict) -> int:
    return int((call.get("usage") or {}).get("totalTokens", 0))


def deterministic_scores(case: dict, answer: dict | None, valid: bool) -> dict:
    gold = case["gold"]
    if not valid or not isinstance(answer, dict):
        return {
            "primaryCorrect": False,
            "applicableFieldCorrect": 0,
            "applicableFieldTotal": sum(gold[field] != "NOT_APPLICABLE" for field in ["truthState", "identityState", "evidenceAuthority"]) + 1,
            "seekMoreEvidenceCorrect": False,
        }
    fields = ["truthState", "identityState", "evidenceAuthority"]
    applicable = [field for field in fields if gold[field] != "NOT_APPLICABLE"]
    correct = sum(answer.get(field) == gold[field] for field in applicable)
    return {
        "primaryCorrect": answer.get("primaryChoice") == gold["primaryChoice"],
        "applicableFieldCorrect": correct,
        "applicableFieldTotal": len(applicable),
        "seekMoreEvidenceCorrect": answer.get("seekMoreEvidence") == gold["seekMoreEvidence"],
    }


def mean(values: list[float]) -> float | None:
    return None if not values else sum(values) / len(values)


def bootstrap_diff(a: list[float], b: list[float], *, seed: int = 7717, reps: int = 10000) -> dict:
    if len(a) != len(b) or not a:
        return {"n": len(a), "meanDiff": None, "ci95": None}
    diffs = [x - y for x, y in zip(a, b)]
    rng = random.Random(seed)
    samples = []
    n = len(diffs)
    for _ in range(reps):
        samples.append(sum(diffs[rng.randrange(n)] for _ in range(n)) / n)
    samples.sort()
    lo = samples[math.floor(0.025 * (reps - 1))]
    hi = samples[math.floor(0.975 * (reps - 1))]
    return {"n": n, "meanDiff": round(sum(diffs) / n, 4), "ci95": [round(lo, 4), round(hi, 4)]}


def analyze(rows: list[dict], cases: dict[str, dict], contract: dict, split: str, judge_calls: list[dict]) -> dict:
    grade_value = contract["scoring"]["causalGradeValues"]
    by_treatment: dict[str, dict] = {}
    for treatment in contract["treatments"]:
        group = [row for row in rows if row["treatment"] == treatment]
        valid = [row for row in group if row["generation"].get("valid")]
        applicable_correct = sum(row["scores"]["applicableFieldCorrect"] for row in group)
        applicable_total = sum(row["scores"]["applicableFieldTotal"] for row in group)
        by_treatment[treatment] = {
            "trials": len(group),
            "physicalValidRate": round(len(valid) / len(group), 4) if group else None,
            "primaryAccuracy": round(sum(row["scores"]["primaryCorrect"] for row in group) / len(group), 4) if group else None,
            "applicableFieldAccuracy": round(applicable_correct / applicable_total, 4) if applicable_total else None,
            "seekMoreEvidenceAccuracy": round(sum(row["scores"]["seekMoreEvidenceCorrect"] for row in group) / len(group), 4) if group else None,
            "causalScore": round(sum(grade_value.get((row.get("judge") or {}).get("causalGrade"), 0.0) for row in group) / len(group), 4) if group else None,
            "unsupportedInferenceRate": round(sum(bool((row.get("judge") or {}).get("unsupportedInference", False)) for row in group) / len(group), 4) if group else None,
            "overgeneralizationRate": round(sum(bool((row.get("judge") or {}).get("overgeneralized", False)) for row in group) / len(group), 4) if group else None,
            "authorityConfusionRate": round(sum(bool((row.get("judge") or {}).get("authorityConfusion", False)) for row in group) / len(group), 4) if group else None,
            "meanPromptTokens": round(mean([provider_prompt_tokens(row["generation"]) for row in group]) or 0, 1),
            "meanCacheHitTokens": round(mean([provider_cache_hit_tokens(row["generation"]) for row in group]) or 0, 1),
            "meanGenerationTokens": round(mean([total_tokens(row["generation"]) for row in group]) or 0, 1),
            "meanElapsedMs": round(mean([float(row["generation"].get("elapsedMs", 0)) for row in group]) or 0, 1),
        }
    by_model: dict[str, dict] = {}
    for model in contract["models"]:
        by_model[model] = {}
        for treatment in contract["treatments"]:
            group = [row for row in rows if row["model"] == model and row["treatment"] == treatment]
            by_model[model][treatment] = {
                "n": len(group),
                "primaryAccuracy": round(sum(row["scores"]["primaryCorrect"] for row in group) / len(group), 4) if group else None,
                "causalScore": round(sum(grade_value.get((row.get("judge") or {}).get("causalGrade"), 0.0) for row in group) / len(group), 4) if group else None,
                "physicalValidRate": round(sum(bool(row["generation"].get("valid")) for row in group) / len(group), 4) if group else None,
            }
    families = sorted({case["family"] for case in cases.values() if case["split"] == split})
    by_family: dict[str, dict] = {}
    for family in families:
        by_family[family] = {}
        ids = {case_id for case_id, case in cases.items() if case["split"] == split and case["family"] == family}
        for treatment in contract["treatments"]:
            group = [row for row in rows if row["caseId"] in ids and row["treatment"] == treatment]
            by_family[family][treatment] = {
                "n": len(group),
                "primaryAccuracy": round(sum(row["scores"]["primaryCorrect"] for row in group) / len(group), 4) if group else None,
                "causalScore": round(sum(grade_value.get((row.get("judge") or {}).get("causalGrade"), 0.0) for row in group) / len(group), 4) if group else None,
                "unsupportedInferenceRate": round(sum(bool((row.get("judge") or {}).get("unsupportedInference", False)) for row in group) / len(group), 4) if group else None,
                "overgeneralizationRate": round(sum(bool((row.get("judge") or {}).get("overgeneralized", False)) for row in group) / len(group), 4) if group else None,
                "authorityConfusionRate": round(sum(bool((row.get("judge") or {}).get("authorityConfusion", False)) for row in group) / len(group), 4) if group else None,
            }
    pair_index = {(row["caseId"], row["model"], row["treatment"]): row for row in rows}
    comparisons: dict[str, dict] = {}
    for left, right, label in [
        ("POST_OFR6_FULL", "PRE_OFR6_FULL", "post_vs_pre"),
        ("PRE_OFR6_FULL", "DIRECT", "pre_vs_direct"),
        ("POST_OFR6_FOCUSED", "POST_OFR6_FULL", "focused_vs_full"),
    ]:
        pairs = []
        for case_id, case in cases.items():
            if case["split"] != split:
                continue
            for model in contract["models"]:
                a = pair_index[(case_id, model, left)]
                b = pair_index[(case_id, model, right)]
                pairs.append((case, a, b))
        targeted = [(case, a, b) for case, a, b in pairs if case["family"] != "NEUTRAL_EXISTING_CORE"]
        def summarize(ps: list[tuple[dict, dict, dict]]) -> dict:
            primary_a = [1.0 if a["scores"]["primaryCorrect"] else 0.0 for _, a, _ in ps]
            primary_b = [1.0 if b["scores"]["primaryCorrect"] else 0.0 for _, _, b in ps]
            causal_a = [grade_value.get((a.get("judge") or {}).get("causalGrade"), 0.0) for _, a, _ in ps]
            causal_b = [grade_value.get((b.get("judge") or {}).get("causalGrade"), 0.0) for _, _, b in ps]
            return {
                "n": len(ps),
                "primaryDiff": bootstrap_diff(primary_a, primary_b),
                "causalDiff": bootstrap_diff(causal_a, causal_b, seed=8811),
                "pairedCorrections": sum((not b["scores"]["primaryCorrect"]) and a["scores"]["primaryCorrect"] for _, a, b in ps),
                "pairedRegressions": sum(b["scores"]["primaryCorrect"] and (not a["scores"]["primaryCorrect"]) for _, a, b in ps),
            }
        comparisons[label] = {"all": summarize(pairs), "targeted": summarize(targeted)}
    judge_usage = {
        "calls": len(judge_calls),
        "validCalls": sum(bool(call.get("valid")) for call in judge_calls),
        "promptTokens": sum(provider_prompt_tokens(call) for call in judge_calls),
        "totalTokens": sum(total_tokens(call) for call in judge_calls),
    }
    return {
        "byTreatment": by_treatment,
        "byModel": by_model,
        "byFamily": by_family,
        "comparisons": comparisons,
        "judgeUsage": judge_usage,
    }


def final_interpretation(analysis: dict, contract: dict) -> dict:
    bt = analysis["byTreatment"]
    post = bt["POST_OFR6_FULL"]
    pre = bt["PRE_OFR6_FULL"]
    focused = bt["POST_OFR6_FOCUSED"]
    targeted_cmp = analysis["comparisons"]["post_vs_pre"]["targeted"]
    diff = targeted_cmp["primaryDiff"]["meanDiff"] or 0.0
    causal_diff = targeted_cmp["causalDiff"]["meanDiff"] or 0.0
    boundary_ok = all(post[name] <= pre[name] + 0.05 for name in ["unsupportedInferenceRate", "overgeneralizationRate", "authorityConfusionRate"])
    marginal_supported = (
        (diff >= 0.05 or targeted_cmp["pairedCorrections"] >= 2)
        and causal_diff >= -0.05
        and boundary_ok
    )
    focused_qualifies = (
        focused["primaryAccuracy"] >= post["primaryAccuracy"] - 0.03
        and focused["causalScore"] >= post["causalScore"] - 0.05
        and focused["unsupportedInferenceRate"] <= post["unsupportedInferenceRate"] + 0.03
        and focused["overgeneralizationRate"] <= post["overgeneralizationRate"] + 0.03
        and focused["authorityConfusionRate"] <= post["authorityConfusionRate"] + 0.03
        and focused["physicalValidRate"] >= 0.95
        and focused["meanPromptTokens"] <= 0.75 * post["meanPromptTokens"]
    )
    family_status = {}
    for family in ["C2_UNKNOWN", "C4_IDENTITY", "C10_OPTION_VALUE", "M13_CAUSAL_HISTORY", "M16_MECHANICAL_PROJECTION", "M17_COMPRESSION"]:
        f = analysis["byFamily"][family]
        p = f["POST_OFR6_FULL"]
        q = f["PRE_OFR6_FULL"]
        # Paired exact correction/regression for this family.
        family_status[family] = {
            "prePrimary": q["primaryAccuracy"],
            "postPrimary": p["primaryAccuracy"],
            "preCausal": q["causalScore"],
            "postCausal": p["causalScore"],
            "classification": (
                "SUPPORTED" if (p["primaryAccuracy"] > q["primaryAccuracy"] and p["causalScore"] >= q["causalScore"] - 0.05)
                else "NEUTRAL_CEILING" if p["primaryAccuracy"] == q["primaryAccuracy"] == 1.0 and p["causalScore"] >= q["causalScore"] - 0.05
                else "MIXED" if p["primaryAccuracy"] >= q["primaryAccuracy"] and p["causalScore"] >= q["causalScore"] - 0.10
                else "NEGATIVE"
            ),
        }
    return {
        "marginalOfr6PracticalValueEstablished": marginal_supported,
        "postVsPreTargetedPrimaryDiff": diff,
        "postVsPreTargetedCausalDiff": causal_diff,
        "postVsPreTargetedPairedCorrections": targeted_cmp["pairedCorrections"],
        "postVsPreTargetedPairedRegressions": targeted_cmp["pairedRegressions"],
        "focusedProjectionQualifies": focused_qualifies,
        "familyStatus": family_status,
        "neutralControlPostMinusPrePrimary": round(analysis["byFamily"]["NEUTRAL_EXISTING_CORE"]["POST_OFR6_FULL"]["primaryAccuracy"] - analysis["byFamily"]["NEUTRAL_EXISTING_CORE"]["PRE_OFR6_FULL"]["primaryAccuracy"], 4),
        "interpretationBoundary": "These are results on the frozen OFR7 corpus and two DeepSeek capacities. A ceiling result is not proof that doctrine is useless; a marginal win is not a universal cognition law."
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["development", "holdout"], required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    corpus, surfaces, contract = validate_freeze()
    cases = {case["caseId"]: case for case in corpus["cases"]}
    split_cases = [case for case in corpus["cases"] if case["split"] == args.split]
    if args.split == "holdout" and [case["caseId"] for case in split_cases] != json.loads(FREEZE.read_text())["holdoutCaseIds"]:
        raise RuntimeError("holdout composition drift")
    specs = [(case, treatment, model) for case in split_cases for treatment in contract["treatments"] for model in contract["models"]]

    def generate(spec):
        case, treatment, model = spec
        surface = surfaces["treatments"][treatment]
        tag = f"gen:{args.split}:{case['caseId']}:{treatment}:{model}"
        try:
            call = run_structured(
                prompt=generation_prompt(case, surface),
                schema=GEN_SCHEMA,
                result_kind="ofr7-decision",
                model=model,
                tag=tag,
                max_tokens=1100,
            )
        except Exception as exc:
            call = {"valid": False, "errorType": type(exc).__name__, "error": str(exc)[:1000]}
        answer = call.get("result") if call.get("valid") else None
        return {
            "caseId": case["caseId"],
            "family": case["family"],
            "treatment": treatment,
            "model": model,
            "surfaceDigest": surface["digest"],
            "generation": call,
            "scores": deterministic_scores(case, answer, bool(call.get("valid"))),
            "answer": answer,
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(generate, specs))

    by_case: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_case[row["caseId"]].append(row)

    def judge_case(case: dict) -> dict:
        case_rows = by_case[case["caseId"]]
        anonymized = []
        mapping = {}
        for row in case_rows:
            aid = anonymize(case["caseId"], row["treatment"], row["model"])
            mapping[aid] = (row["treatment"], row["model"])
            anonymized.append({
                "answerId": aid,
                "answer": row["answer"] if row["generation"].get("valid") else {"invalidGeneration": True, "stopCode": row["generation"].get("stopCode")},
            })
        # Stable but non-treatment-ordered presentation.
        anonymized.sort(key=lambda item: item["answerId"])
        answer_ids = [item["answerId"] for item in anonymized]
        tag = f"judge:{args.split}:{case['caseId']}"
        try:
            call = run_structured(
                prompt=judge_prompt(case, anonymized),
                schema=judge_schema(answer_ids),
                result_kind="ofr7-treatment-blind-judge",
                model=contract["judgeModel"],
                tag=tag,
                max_tokens=2600,
                max_wall_ms=180000,
            )
            exact = False
            if call.get("valid") and isinstance(call.get("result"), dict):
                grades = call["result"].get("grades") or []
                got = [grade.get("answerId") for grade in grades if isinstance(grade, dict)]
                exact = len(got) == len(answer_ids) and len(set(got)) == len(got) and set(got) == set(answer_ids)
            call["answerSetExact"] = exact
        except Exception as exc:
            call = {"valid": False, "answerSetExact": False, "errorType": type(exc).__name__, "error": str(exc)[:1000]}
        return {"caseId": case["caseId"], "mapping": mapping, "call": call}

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.workers, len(split_cases))) as ex:
        judge_results = list(ex.map(judge_case, split_cases))

    judge_calls = [item["call"] for item in judge_results]
    judge_index = {}
    for item in judge_results:
        call = item["call"]
        if not (call.get("valid") and call.get("answerSetExact")):
            continue
        for grade in call["result"]["grades"]:
            treatment, model = item["mapping"][grade["answerId"]]
            judge_index[(item["caseId"], treatment, model)] = grade
    for row in rows:
        row["judge"] = judge_index.get((row["caseId"], row["treatment"], row["model"]))

    analysis = analyze(rows, cases, contract, args.split, judge_calls)
    interpretation = final_interpretation(analysis, contract) if args.split == "holdout" else None
    output = {
        "schemaVersion": 1,
        "kind": "ordivon.ofr7-live-evidence.v1",
        "split": args.split,
        "semanticFreezeDigest": sha(FREEZE),
        "contractDigest": sha(CONTRACT),
        "corpusDigest": sha(CORPUS),
        "surfacesDigest": sha(SURFACES),
        "expectedGenerationTrials": len(specs),
        "validGenerationTrials": sum(bool(row["generation"].get("valid")) for row in rows),
        "expectedJudgeCalls": len(split_cases),
        "validJudgeCalls": sum(bool(item["call"].get("valid") and item["call"].get("answerSetExact")) for item in judge_results),
        "analysis": analysis,
        "interpretation": interpretation,
        "judgeCalls": judge_results,
        "trials": rows,
    }
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "split": args.split,
        "expectedGenerationTrials": output["expectedGenerationTrials"],
        "validGenerationTrials": output["validGenerationTrials"],
        "expectedJudgeCalls": output["expectedJudgeCalls"],
        "validJudgeCalls": output["validJudgeCalls"],
        "analysis": analysis,
        "interpretation": interpretation,
    }, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
