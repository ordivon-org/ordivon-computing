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
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "choice": {"type": "string", "enum": ["A", "B", "C", "D"]},
        "reason": {"type": "string"},
    },
    "required": ["choice", "reason"],
}


def ref(identity: str, kind: str, value):
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def packet(case: dict, treatment: str) -> str:
    visible = {
        "caseId": case["id"],
        "historicalOutcome": case["terminal"],
        "question": case["question"],
        "candidateActions": case["actions"],
    }
    if treatment == "CAUSAL_LINEAGE":
        visible["sourceFencedCausalLineage"] = case["lineage"]
    return (
        "You are a fresh finite research Agent with no prior Ordivon memory. "
        "Choose exactly one NEXT reachability/research action A-D. "
        "The historical material is evidence about a past trajectory, not current authority and not a guarantee that the same path transfers. "
        "Do not invent missing current capabilities, authority, resources, or causal facts. "
        "Prefer the action that best preserves the distinction between terminal outcome and load-bearing capability transition. "
        "Return only the structured result.\n\nPACKET:\n"
        + json.dumps(visible, ensure_ascii=False, sort_keys=True)
    )


def evaluate(result: dict | None, case: dict) -> dict:
    choice = result.get("choice") if isinstance(result, dict) else None
    return {
        "exactNextAction": choice == case["oracle"],
        "prematureClosure": choice == "C" and case["oracle"] != "C",
        "terminalOutcomeCollapse": choice in {"A", "D"} and case["oracle"] == "B",
        "currentCapabilityLifting": case["id"] == "NIF-STAGED-REALIZATION" and choice in {"A", "D"},
        "historyAsAuthority": case["id"] == "OSI-STANDARD-LOCKIN" and choice == "A",
        "unsupportedGeneralization": choice in {"A", "D"} and case["id"] in {"MRNA-DORMANT-PLATFORM", "GREAT-EASTERN-OPTION-VALUE"},
    }


def run_one(case, treatment, model, replicate, secret):
    prompt = packet(case, treatment)
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:historical-reachability-hr1:{case['id']}:{treatment}:{model}:r{replicate}:{now}"
    completion = {
        "mode": "structured-result-v1",
        "resultKind": "historical-reachability-hr1-v0",
        "resultSchema": SCHEMA,
    }
    settings = replace(
        DeepSeekSettings.from_secret_file(secret),
        model=model,
        max_output_tokens=700,
    )
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@684333be5146d4f705a91edb396e83c6a1150e1f",
        caller_id="caller:ordivon-computing-historical-reachability-hr1",
        caller_run_ref=f"{case['id']}|{treatment}|{model}|r{replicate}",
        objective_ref=ref(
            f"objective:{case['id']}:hr1:v1",
            "objective",
            {"question": "choose next reachability action", "caseId": case["id"]},
        ),
        context_refs=(
            ref(
                f"context:{case['id']}:{treatment}:hr1:v1",
                "context",
                {"prompt": prompt, "sourceRef": case["sourceRef"]},
            ),
        ),
        provider_id="provider:deepseek",
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=settings.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(
            max_model_calls=2,
            max_tool_calls=0,
            max_observation_bytes=32768,
            max_wall_time_ms=120000,
            max_total_tokens=16384,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(
            f"system:{case['id']}:{treatment}:{model}:r{replicate}:hr1:v1",
            "system-manifest",
            {"experiment": "historical-reachability-hr1-v0", "treatment": treatment, "model": model},
        ),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(
            content_policy="bounded-private-content",
            allow_model_content=True,
            allow_tool_content=False,
        ),
    )
    with tempfile.TemporaryDirectory(prefix="historical-reachability-hr1-") as state:
        run = HarnessAgentRun.create(
            state,
            contract,
            lambda exact: DeepSeekTurnAdapter(settings, completion_contract=exact.completion_contract),
        )
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": prompt},))
        elapsed = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        result = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        return {
            "caseId": case["id"],
            "sourceRef": case["sourceRef"],
            "treatment": treatment,
            "model": model,
            "replicate": replicate,
            "result": result,
            "evaluation": evaluate(result, case),
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed,
            "stopCode": execution.loop_result.stop_code.value,
        }


def summarize(rows):
    out = {}
    for row in rows:
        key = f"{row['model']}|{row['treatment']}"
        bucket = out.setdefault(
            key,
            {
                "model": row["model"],
                "treatment": row["treatment"],
                "trials": 0,
                "exactNextAction": 0,
                "prematureClosure": 0,
                "terminalOutcomeCollapse": 0,
                "currentCapabilityLifting": 0,
                "historyAsAuthority": 0,
                "unsupportedGeneralization": 0,
                "tokens": 0,
            },
        )
        bucket["trials"] += 1
        for name in (
            "exactNextAction",
            "prematureClosure",
            "terminalOutcomeCollapse",
            "currentCapabilityLifting",
            "historyAsAuthority",
            "unsupportedGeneralization",
        ):
            bucket[name] += int(bool(row["evaluation"].get(name)))
        bucket["tokens"] += int((row.get("usage") or {}).get("totalTokens", 0) or 0)
    return list(out.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--models", default="deepseek-v4-flash")
    parser.add_argument("--replicates", type=int, default=2)
    parser.add_argument("--secret", default="/root/.config/ordivon/secrets/deepseek.json")
    parser.add_argument("--seed", type=int, default=202608269)
    args = parser.parse_args()

    cases_payload = json.loads((ROOT / "cases.json").read_text())
    contract_payload = json.loads((ROOT / "contract.json").read_text())
    models = [item for item in args.models.split(",") if item]
    schedule = [
        (case, treatment, model, replicate)
        for case in cases_payload["cases"]
        for treatment in ("TERMINAL_ONLY", "CAUSAL_LINEAGE")
        for model in models
        for replicate in range(1, args.replicates + 1)
    ]
    random.Random(args.seed).shuffle(schedule)

    rows = []
    output = Path(args.output)
    for index, (case, treatment, model, replicate) in enumerate(schedule, 1):
        try:
            row = run_one(case, treatment, model, replicate, Path(args.secret))
        except Exception as exc:
            row = {
                "caseId": case["id"],
                "sourceRef": case["sourceRef"],
                "treatment": treatment,
                "model": model,
                "replicate": replicate,
                "result": None,
                "evaluation": {"exactNextAction": False},
                "errorType": type(exc).__name__,
                "error": str(exc)[:1600],
            }
        rows.append(row)
        payload = {
            "schemaVersion": 1,
            "kind": "ordivon.computing.historical-reachability-hr1-live-v0",
            "contractDigest": canonical_digest(contract_payload),
            "casesDigest": canonical_digest(cases_payload),
            "seed": args.seed,
            "plannedTrials": len(schedule),
            "completedTrials": len(rows),
            "rows": rows,
            "summary": summarize(rows),
        }
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print(
            json.dumps(
                {
                    "n": index,
                    "total": len(schedule),
                    "case": case["id"],
                    "treatment": treatment,
                    "model": model,
                    "result": row.get("result"),
                    "evaluation": row.get("evaluation"),
                    "error": row.get("error"),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
