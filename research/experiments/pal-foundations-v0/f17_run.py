from __future__ import annotations

import argparse
import json
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

DIRECT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "decision": {"type": "string", "enum": ["PRESSURE", "NO_OP"]},
        "pressureTitle": {"type": "string"},
        "decisiveProbe": {"type": "string"},
        "expectedDecisionChange": {"type": "string"},
        "ownerBoundary": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": [
        "decision",
        "pressureTitle",
        "decisiveProbe",
        "expectedDecisionChange",
        "ownerBoundary",
        "reason",
    ],
}

CERT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "decision": {"type": "string", "enum": ["PRESSURE", "NO_OP"]},
        "pressureTitle": {"type": "string"},
        "affectedMandate": {"type": "string"},
        "observedMismatchOrOpportunity": {"type": "string"},
        "mechanismHypothesis": {"type": "string"},
        "uncertainty": {"type": "string"},
        "decisiveProbe": {"type": "string"},
        "expectedDecisionChange": {"type": "string"},
        "costAndReversibility": {"type": "string"},
        "failureUpdate": {"type": "string"},
        "ownerBoundary": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": [
        "decision",
        "pressureTitle",
        "affectedMandate",
        "observedMismatchOrOpportunity",
        "mechanismHypothesis",
        "uncertainty",
        "decisiveProbe",
        "expectedDecisionChange",
        "costAndReversibility",
        "failureUpdate",
        "ownerBoundary",
        "reason",
    ],
}


def bound_ref(identity: str, kind: str, value: object) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def prompt(event: dict, context: dict, treatment: str) -> str:
    base = (
        "You are reviewing ONE exact post-cutoff reality event for Ordivon Computing PAL research. "
        "The owner has already done its own local work. Your task is not to praise the change or invent work "
        "because it is complex. Decide whether this event exposes ONE unresolved shared research pressure that "
        "deserves a bounded decisive probe, or whether Computing should NO_OP. A valid PRESSURE must identify a "
        "real unresolved mismatch/opportunity/contradiction whose resolution can change a research/design decision. "
        "Owner-local implementation, already-closed debt, or confirmation of an existing boundary is not automatically "
        "shared pressure. Preserve owner authority. Do not propose product mutation as the probe unless independently justified.\n"
    )
    if treatment == "PRESSURE_CERTIFICATE":
        method = (
            "Before deciding, explicitly reconstruct a pressure certificate: affected mandate; observed mismatch/opportunity; "
            "causal mechanism hypothesis; uncertainty; decisive probe that distinguishes alternatives; expected decision change "
            "if resolved; cost/reversibility; failure update; owner boundary. If the event does not support a genuine unresolved "
            "pressure, return NO_OP and use these fields to explain why no shared probe is justified.\n"
        )
    else:
        method = (
            "Use strong direct full-evidence review. Select one bounded pressure or NO_OP. If PRESSURE, decisiveProbe must "
            "distinguish competing explanations and expectedDecisionChange must say what would actually change.\n"
        )
    return (
        base
        + method
        + "\nT0 RESEARCH CONTEXT:\n"
        + json.dumps(context, ensure_ascii=False, sort_keys=True)
        + "\n\nEVENT PACKET:\n"
        + json.dumps(event, ensure_ascii=False, sort_keys=True)
    )


def run_one(event: dict, context: dict, treatment: str, model: str, secret: Path) -> dict:
    schema = CERT_SCHEMA if treatment == "PRESSURE_CERTIFICATE" else DIRECT_SCHEMA
    text = prompt(event, context, treatment)
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:pal-f17:{event['eventId']}:{treatment}:{model}:{now}"
    completion = {
        "mode": "structured-result-v1",
        "resultKind": "pal-f17-pressure-review",
        "resultSchema": schema,
    }
    settings = replace(
        DeepSeekSettings.from_secret_file(secret),
        model=model,
        max_output_tokens=1200,
    )
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@pal-f17",
        caller_id="caller:ordivon-computing-pal",
        caller_run_ref=f"{event['eventId']}|{treatment}|{model}",
        objective_ref=bound_ref(f"objective:{event['eventId']}", "objective", context),
        context_refs=(bound_ref(f"context:{event['eventId']}:{treatment}", "context", {"prompt": text}),),
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
            max_total_tokens=18000,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=bound_ref(
            f"system:{event['eventId']}:{treatment}:{model}",
            "system-manifest",
            {"experiment": "PAL-F17", "treatment": treatment, "model": model},
        ),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(
            content_policy="bounded-private-content",
            allow_model_content=True,
            allow_tool_content=False,
        ),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-pal-f17-") as state_root:
        run = HarnessAgentRun.create(
            state_root,
            contract,
            lambda exact: DeepSeekTurnAdapter(settings, completion_contract=exact.completion_contract),
        )
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": text},))
        elapsed_ms = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        result = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        valid = isinstance(result, dict) and result.get("decision") in {"PRESSURE", "NO_OP"}
        terminal = execution.terminal_result
        return {
            "eventId": event["eventId"],
            "treatment": treatment,
            "model": model,
            "runId": run_id,
            "valid": valid,
            "decision": result.get("decision") if valid else None,
            "result": result,
            "stopCode": execution.loop_result.stop_code.value,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed_ms,
            "receiptDigest": None if terminal is None else terminal.receipt.digest,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--event", default="f17-event-001-v0.json")
    parser.add_argument("--secret", default="/root/.config/ordivon/secrets/deepseek.json")
    args = parser.parse_args()
    event = json.load(open(ROOT / args.event))
    context = json.load(open(ROOT / "f17-t0-research-context-v0.json"))
    rows: list[dict] = []
    order = [
        ("deepseek-v4-flash", "DIRECT_FULL_REVIEW"),
        ("deepseek-v4-flash", "PRESSURE_CERTIFICATE"),
        ("deepseek-v4-pro", "PRESSURE_CERTIFICATE"),
        ("deepseek-v4-pro", "DIRECT_FULL_REVIEW"),
    ]
    output = Path(args.output)
    for model, treatment in order:
        try:
            row = run_one(event, context, treatment, model, Path(args.secret))
        except Exception as error:
            row = {
                "eventId": event["eventId"],
                "treatment": treatment,
                "model": model,
                "valid": False,
                "decision": None,
                "result": None,
                "stopCode": "exception",
                "errorType": type(error).__name__,
                "error": str(error)[:500],
            }
        rows.append(row)
        output.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "kind": "ordivon.computing.pal-f17-event-campaign",
                    "eventDigest": canonical_digest(event),
                    "contextDigest": canonical_digest(context),
                    "rows": rows,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        print(
            json.dumps(
                {
                    "model": model,
                    "treatment": treatment,
                    "valid": row["valid"],
                    "decision": row["decision"],
                    "result": row.get("result"),
                    "error": row.get("error"),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
