from __future__ import annotations

import argparse
import json
import random
import tempfile
import time
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
CLASSES = [
    "T1_POTENTIATE",
    "T2_COMPLEMENT",
    "T3_INSTRUMENT",
    "T4_REPRESENT_STANDARDIZE",
    "T5_RECONFIGURE_RECOMBINE",
    "T6_EXTERNALIZE_ACCESS",
    "T7_VALIDATE_REALIZE_STAGE",
    "T8_CONSTRAIN_PRUNE",
    "T9_SCALE_MOVE_BOUNDARY",
    "T10_LOSS_LOCKIN_DECAY",
    "OTHER",
    "NONE",
]
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "transitionClasses": {
            "type": "array",
            "items": {"type": "string", "enum": CLASSES},
            "minItems": 1,
            "maxItems": 3,
            "uniqueItems": True,
        },
        "beforeBlocker": {"type": "string"},
        "basisChange": {"type": "string"},
        "openedOrClosedPath": {"type": "string"},
        "remainingBoundary": {"type": "string"},
        "terminalOnlyLikelySufficient": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": [
        "transitionClasses",
        "beforeBlocker",
        "basisChange",
        "openedOrClosedPath",
        "remainingBoundary",
        "terminalOnlyLikelySufficient",
        "reason",
    ],
}


def ref(identity: str, kind: str, value):
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def prompt_for(item: dict, contract: dict) -> str:
    record = item["record"]
    instructions = {
        "task": "Code the source-fenced historical trajectory using the Historical Reachability transition lens.",
        "classes": contract["classes"],
        "codingRules": contract["codingRules"],
        "important": [
            "This is not a success score and not a current capability claim.",
            "Use only the supplied source-native record.",
            "If the lens does not fit, use OTHER or NONE rather than forcing a category.",
            "A mention of infrastructure/standards/instruments is insufficient unless it materially changes reachability/search/realization in the supplied trajectory.",
        ],
    }
    return (
        "You are an independent skeptical historical research coder. Return only the structured result.\n\n"
        "CODING CONTRACT:\n"
        + json.dumps(instructions, ensure_ascii=False, sort_keys=True)
        + "\n\nSOURCE-NATIVE TRAJECTORY:\n"
        + json.dumps(record, ensure_ascii=False, sort_keys=True)
    )


def run_one(item, contract_payload, model, replicate, secret):
    prompt = prompt_for(item, contract_payload)
    tid = item["trajectoryId"]
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:historical-reachability-hr0:{tid}:{model}:r{replicate}:{now}"
    completion = {
        "mode": "structured-result-v1",
        "resultKind": "historical-reachability-hr0-coding-v0",
        "resultSchema": SCHEMA,
    }
    settings = replace(DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=1100)
    hcontract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f",
        caller_id="caller:ordivon-computing-historical-reachability-hr0",
        caller_run_ref=f"{tid}|{model}|r{replicate}",
        objective_ref=ref(f"objective:{tid}:hr0:v1", "objective", {"trajectoryId": tid, "task": "independent transition coding"}),
        context_refs=(ref(f"context:{tid}:hr0:v1", "context", {"prompt": prompt, "recordDigest": item["recordDigest"]}),),
        provider_id="provider:deepseek",
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=settings.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(
            max_model_calls=2,
            max_tool_calls=0,
            max_observation_bytes=65536,
            max_wall_time_ms=120000,
            max_total_tokens=24576,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(
            f"system:{tid}:{model}:r{replicate}:hr0:v1",
            "system-manifest",
            {"experiment": "historical-reachability-hr0-coding-v0", "model": model},
        ),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content", allow_model_content=True, allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix="historical-reachability-hr0-") as state:
        run = HarnessAgentRun.create(state, hcontract, lambda exact: DeepSeekTurnAdapter(settings, completion_contract=exact.completion_contract))
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": prompt},))
        elapsed = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        result = None if conclusion is None else decode_structured_completion_result(hcontract, conclusion)
        return {
            "trajectoryId": tid,
            "recordDigest": item["recordDigest"],
            "model": model,
            "replicate": replicate,
            "result": result,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed,
            "stopCode": execution.loop_result.stop_code.value,
        }


def analysis(rows):
    class_counts = {}
    by_key = {}
    errors = 0
    for row in rows:
        result = row.get("result")
        if not isinstance(result, dict):
            errors += 1
            continue
        classes = result.get("transitionClasses") or []
        for cls in classes:
            class_counts[cls] = class_counts.get(cls, 0) + 1
        by_key.setdefault(row["trajectoryId"], []).append(set(classes))
    exact = 0
    jaccards = []
    comparable = 0
    for tid, sets in by_key.items():
        if len(sets) != 2:
            continue
        comparable += 1
        a, b = sets
        exact += int(a == b)
        union = a | b
        jaccards.append(1.0 if not union else len(a & b) / len(union))
    return {
        "classCounts": dict(sorted(class_counts.items())),
        "providerErrors": errors,
        "replicateComparableRecords": comparable,
        "replicateExactSetAgreement": exact,
        "replicateMeanJaccard": None if not jaccards else sum(jaccards) / len(jaccards),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--models", default="deepseek-v4-flash")
    parser.add_argument("--replicates", type=int, default=2)
    parser.add_argument("--secret", default="/root/.config/ordivon/secrets/deepseek.json")
    parser.add_argument("--seed", type=int, default=2026082610)
    args = parser.parse_args()

    source = json.loads((ROOT / "hr0-source-freeze-v0.json").read_text())
    contract = json.loads((ROOT / "hr0-coding-contract.json").read_text())
    models = [m for m in args.models.split(",") if m]
    full_schedule = [(item, model, rep) for item in source["records"] for model in models for rep in range(1, args.replicates + 1)]
    random.Random(args.seed).shuffle(full_schedule)
    output = Path(args.output)
    rows = []
    if output.exists():
        prior = json.loads(output.read_text())
        if prior.get("sourceFreezeDigest") != canonical_digest(source) or prior.get("contractDigest") != canonical_digest(contract):
            raise RuntimeError("refusing resume: source/contract digest mismatch")
        rows = list(prior.get("rows", []))
    completed = {(row.get("trajectoryId"), row.get("model"), row.get("replicate")) for row in rows}
    schedule = [(item, model, rep) for item, model, rep in full_schedule if (item["trajectoryId"], model, rep) not in completed]
    for index, (item, model, rep) in enumerate(schedule, 1):
        try:
            row = run_one(item, contract, model, rep, Path(args.secret))
        except Exception as exc:
            row = {
                "trajectoryId": item["trajectoryId"],
                "recordDigest": item["recordDigest"],
                "model": model,
                "replicate": rep,
                "result": None,
                "errorType": type(exc).__name__,
                "error": str(exc)[:1600],
            }
        rows.append(row)
        payload = {
            "schemaVersion": 1,
            "kind": "ordivon.computing.historical-reachability-hr0-live-v0",
            "sourceFreezeDigest": canonical_digest(source),
            "contractDigest": canonical_digest(contract),
            "seed": args.seed,
            "plannedTrials": len(full_schedule),
            "completedTrials": len(rows),
            "rows": rows,
            "analysis": analysis(rows),
        }
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print(json.dumps({"n": index, "total": len(schedule), "trajectoryId": item["trajectoryId"], "replicate": rep, "result": row.get("result"), "error": row.get("error")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
