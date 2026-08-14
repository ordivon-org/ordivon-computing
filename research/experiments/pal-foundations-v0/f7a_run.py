from __future__ import annotations
import argparse, json, tempfile, time
from dataclasses import replace
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_harness.api import (
    DeepSeekSettings, DeepSeekTurnAdapter, HarnessAgentRun, HarnessBoundReference,
    HarnessPrivacyPolicy, HarnessRunContract, NO_TOOL_AGENT_GRANT_DIGEST,
    NO_TOOL_AGENT_SURFACE_DIGEST, RunBudget, decode_structured_completion_result,
)

ROOT = Path(__file__).resolve().parent
DECISIONS = ["CAPITALIZE", "HOLD_CANDIDATE"]
TREATMENTS = ["local", "sham", "independent"]
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "decision": {"type": "string", "enum": DECISIONS},
        "keyEvidence": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 5},
        "reason": {"type": "string"},
    },
    "required": ["decision", "keyEvidence", "reason"],
}


def ref(identity, kind, value):
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def prompt(doc, case, treatment):
    packet = case["localPacket"]
    if treatment == "sham":
        packet += "\n\nADDITIONAL EVIDENCE:\n" + case["shamAddendum"]
    elif treatment == "independent":
        packet += "\n\nADDITIONAL EVIDENCE:\n" + case["independentAddendum"]
    return (
        "You are deciding whether a locally promising adaptive change should become reusable capital for future rounds. "
        "CAPITALIZE only when the available evidence supports treating the change as an accepted reusable mechanism/prior/capability at its evidenced scope. "
        "Choose HOLD_CANDIDATE when the evidence supports keeping it candidate-only, research-local, narrowly provisional, or awaiting more evidence. "
        "Do not reward implementation effort, architectural elegance, novelty, or mere behavioral activity. Do not assume more evidence is automatically better; use its relevance and independence.\n\n"
        "DECISIONS:\n" + json.dumps(doc["decisionOptions"], ensure_ascii=False, sort_keys=True) +
        "\n\nEVIDENCE PACKET:\n" + packet
    )


def one(doc, case, treatment, model, replica, secret):
    pr = prompt(doc, case, treatment)
    settings = replace(DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=800)
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:pal-f7a:{case['caseId']}:{treatment}:{model}:{replica}:{now}"
    completion = {
        "mode": "structured-result-v1",
        "resultKind": "pal-f7a-capitalization-decision",
        "resultSchema": SCHEMA,
    }
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@pal-f7a",
        caller_id="caller:ordivon-computing-pal",
        caller_run_ref=f"{case['caseId']}|{treatment}|{model}|{replica}",
        objective_ref=ref(f"objective:{case['caseId']}", "objective", {"case": case["caseId"]}),
        context_refs=(ref(f"context:{case['caseId']}:{treatment}:{replica}", "context", {"prompt": pr}),),
        provider_id="provider:deepseek",
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=settings.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(
            max_model_calls=2, max_tool_calls=0, max_observation_bytes=65536,
            max_wall_time_ms=90000, max_total_tokens=18000, max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(
            f"system:{case['caseId']}:{treatment}:{model}", "system-manifest",
            {"experiment": "PAL-F7A", "model": model, "treatment": treatment, "maxOutputTokens": 800},
        ),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(
            content_policy="bounded-private-content", allow_model_content=True, allow_tool_content=False
        ),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-pal-f7a-") as state_root:
        run = HarnessAgentRun.create(
            state_root, contract,
            lambda exact: DeepSeekTurnAdapter(settings, completion_contract=exact.completion_contract),
        )
        start = time.monotonic()
        execution = run.run(({"role": "user", "content": pr},))
        elapsed_ms = round((time.monotonic() - start) * 1000)
        conclusion = execution.loop_result.conclusion
        decoded = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        valid = isinstance(decoded, dict) and decoded.get("decision") in DECISIONS
        choice = decoded.get("decision") if valid else None
        terminal = execution.terminal_result
        return {
            "caseId": case["caseId"], "split": case["split"], "caseClass": case["class"],
            "treatment": treatment, "model": model, "replica": replica, "runId": run_id,
            "stopCode": execution.loop_result.stop_code.value,
            "modelCalls": execution.loop_result.model_calls,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed_ms, "result": decoded, "valid": valid, "decision": choice,
            "exactCorrect": bool(valid and choice == case["oracleDecision"]),
            "oracleDecision": case["oracleDecision"],
            "receiptDigest": None if terminal is None else terminal.receipt.digest,
        }


def validate():
    doc = json.loads((ROOT / "f7a-cases-v0.json").read_text())
    assert len(doc["cases"]) == 8
    assert Counter(c["class"] for c in doc["cases"]) == Counter({"trap": 4, "positive": 4})
    assert Counter(c["split"] for c in doc["cases"]) == Counter({"development": 4, "holdout": 4})
    for split in ("development", "holdout"):
        subset = [c for c in doc["cases"] if c["split"] == split]
        assert Counter(c["class"] for c in subset) == Counter({"trap": 2, "positive": 2})
    for c in doc["cases"]:
        assert c["oracleDecision"] in DECISIONS
        ratio = len(c["shamAddendum"]) / len(c["independentAddendum"])
        assert 0.8 <= ratio <= 1.25, (c["caseId"], ratio)
    return {
        "caseCount": 8,
        "caseDigest": canonical_digest(doc),
        "treatments": TREATMENTS,
        "balancedClasses": True,
        "balancedSplits": True,
        "shamIndependentLengthRatio": "0.8..1.25",
    }

# local import after definition keeps the runner compact and validation deterministic
from collections import Counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["deepseek-v4-flash", "deepseek-v4-pro"])
    parser.add_argument("--replicas", type=int, default=2)
    parser.add_argument("--secret", default="/root/.config/ordivon/secrets/deepseek.json")
    parser.add_argument("--output")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    validation = validate()
    if args.validate_only:
        print(json.dumps(validation, indent=2))
        return
    if not args.model or not args.output:
        parser.error("--model and --output required")
    doc = json.loads((ROOT / "f7a-cases-v0.json").read_text())
    rows = []
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    def persist():
        evidence = {
            "schemaVersion": 1,
            "kind": "ordivon.computing.pal-f7a-provider-campaign",
            "model": args.model,
            "replicas": args.replicas,
            "caseDigest": canonical_digest(doc),
            "rows": rows,
        }
        output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        return evidence

    persist()
    orders = {
        1: ["local", "sham", "independent"],
        2: ["independent", "sham", "local"],
    }
    for case in doc["cases"]:
        for replica in range(1, args.replicas + 1):
            for treatment in orders[replica]:
                try:
                    row = one(doc, case, treatment, args.model, replica, Path(args.secret))
                except Exception as exc:
                    row = {
                        "caseId": case["caseId"], "split": case["split"], "caseClass": case["class"],
                        "treatment": treatment, "model": args.model, "replica": replica,
                        "runId": None, "stopCode": "provider_or_recovery_exception", "modelCalls": None,
                        "usage": None, "elapsedMs": None, "result": None, "valid": False,
                        "decision": None, "exactCorrect": False, "oracleDecision": case["oracleDecision"],
                        "receiptDigest": None, "errorType": type(exc).__name__, "error": str(exc)[:500],
                    }
                rows.append(row)
                evidence = persist()
                print(json.dumps({
                    "case": row["caseId"], "class": row["caseClass"], "model": args.model,
                    "replica": replica, "treatment": treatment, "valid": row["valid"],
                    "decision": row["decision"], "oracle": row["oracleDecision"],
                    "correct": row["exactCorrect"], "errorType": row.get("errorType"),
                }, ensure_ascii=False), flush=True)
    evidence = persist()
    print(json.dumps({"output": str(output), "rows": len(rows), "digest": canonical_digest(evidence)}, indent=2))


if __name__ == "__main__":
    main()
