from __future__ import annotations

import argparse
import json
import tempfile
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

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
DECISIONS = [
    "NO_CHANGE",
    "OWNER_LOCAL",
    "SHARED_BOUNDARY",
    "RESEARCH_ONLY",
    "INDEPENDENT_PLATFORM",
]
PRIOR = """Reusable infrastructure-promotion prior:
1. If a mature lower/classical mechanism already owns the operation semantics, inherit it directly.
2. If repeated mechanical Agent burden remains, add only the smallest owner-local adapter/projection/manifest; it must not become a new authority.
3. Promote a shared Ordivon semantic boundary only after repeated materially different workloads expose the same unowned stable responsibility, a strong simpler baseline fails, ownership/recovery consequences are explicit, and deletion would recreate material loss.
4. Even after a shared boundary is earned, an independent service/repository/platform is a separate later decision requiring independent deployment/versioning/persistence/security or consumer pressure.
5. Useful cross-project code, symmetry, implementation effort, or convenience alone are not promotion evidence."""

RESULT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "decision": {"type": "string", "enum": DECISIONS},
        "keyEvidence": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 4},
        "reason": {"type": "string"},
    },
    "required": ["decision", "keyEvidence", "reason"],
}


def ref(identity: str, kind: str, value: Any) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def make_prompt(doc: dict[str, Any], case: dict[str, Any], treatment: str) -> str:
    base = (
        "You are making one architecture/consumption disposition from evidence available at that time. "
        "Prefer evidence over naming symmetry, minimize unnecessary durable complexity, and do not infer authority that is not stated. "
        "Choose exactly one admitted disposition.\n\n"
    )
    if treatment == "prior":
        base += PRIOR + "\n\n"
    base += "DISPOSITIONS:\n" + json.dumps(doc["decisionOptions"], ensure_ascii=False, sort_keys=True)
    base += "\n\nEVIDENCE PACKET:\n" + case["packet"]
    return base


def run_one(doc: dict[str, Any], case: dict[str, Any], treatment: str, model: str, replica: int, secret: Path) -> dict[str, Any]:
    prompt = make_prompt(doc, case, treatment)
    settings = replace(DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=700)
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:pal-f5:{case['caseId']}:{treatment}:{model}:{replica}:{now}"
    completion = {"mode": "structured-result-v1", "resultKind": "pal-f5-meta-selection", "resultSchema": RESULT_SCHEMA}
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@pal-f5",
        caller_id="caller:ordivon-computing-pal",
        caller_run_ref=f"{case['caseId']}|{treatment}|{model}|{replica}",
        objective_ref=ref(f"objective:{case['caseId']}", "objective", {"case": case["caseId"]}),
        context_refs=(ref(f"context:{case['caseId']}:{treatment}:{replica}", "context", {"prompt": prompt}),),
        provider_id="provider:deepseek",
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=settings.model,
        tool_catalog_digest=NO_TOOL_AGENT_SURFACE_DIGEST,
        tool_grant_digest=NO_TOOL_AGENT_GRANT_DIGEST,
        budget=RunBudget(
            max_model_calls=2,
            max_tool_calls=0,
            max_observation_bytes=65_536,
            max_wall_time_ms=90_000,
            max_total_tokens=16_000,
            max_model_retries=1,
            max_conclusion_corrections=1,
        ).to_contract_dict(),
        completion_contract=completion,
        system_manifest_ref=ref(
            f"system:{case['caseId']}:{treatment}:{model}",
            "system-manifest",
            {"experiment": "PAL-F5", "model": model, "treatment": treatment, "maxOutputTokens": 700},
        ),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(content_policy="bounded-private-content", allow_model_content=True, allow_tool_content=False),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-pal-f5-") as state_root:
        run = HarnessAgentRun.create(
            state_root,
            contract,
            lambda exact: DeepSeekTurnAdapter(settings, completion_contract=exact.completion_contract),
        )
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": prompt},))
        elapsed_ms = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        decoded = None if conclusion is None else decode_structured_completion_result(contract, conclusion)
        valid = isinstance(decoded, dict) and decoded.get("decision") in DECISIONS
        decision = decoded.get("decision") if valid else None
        oracle = case["oracleDecision"]
        terminal = execution.terminal_result
        return {
            "caseId": case["caseId"],
            "split": case["split"],
            "treatment": treatment,
            "model": model,
            "replica": replica,
            "runId": run_id,
            "stopCode": execution.loop_result.stop_code.value,
            "modelCalls": execution.loop_result.model_calls,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed_ms,
            "result": decoded,
            "valid": valid,
            "decision": decision,
            "exactCorrect": bool(valid and decision == oracle),
            "falseIndependentPlatform": bool(valid and decision == "INDEPENDENT_PLATFORM" and oracle != "INDEPENDENT_PLATFORM"),
            "missedEarnedChange": bool(valid and oracle in {"OWNER_LOCAL", "SHARED_BOUNDARY"} and decision in {"NO_CHANGE", "RESEARCH_ONLY"}),
            "oracleDecision": oracle,
            "receiptDigest": None if terminal is None else terminal.receipt.digest,
        }


def validate_fixture() -> dict[str, Any]:
    doc = json.loads((ROOT / "f5-cases-v0.json").read_text())
    assert len(doc["cases"]) == 8
    for case in doc["cases"]:
        assert case["oracleDecision"] in DECISIONS
    return {"caseCount": len(doc["cases"]), "caseDigest": canonical_digest(doc), "priorDigest": canonical_digest(PRIOR)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["deepseek-v4-flash", "deepseek-v4-pro"])
    parser.add_argument("--replicas", type=int, default=2)
    parser.add_argument("--secret", default="/root/.config/ordivon/secrets/deepseek.json")
    parser.add_argument("--output")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    validation = validate_fixture()
    if args.validate_only:
        print(json.dumps(validation, indent=2))
        return
    if not args.model or not args.output:
        parser.error("--model and --output are required unless --validate-only")
    doc = json.loads((ROOT / "f5-cases-v0.json").read_text())
    rows = []
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    def persist() -> dict[str, Any]:
        evidence = {
            "schemaVersion": 1,
            "kind": "ordivon.computing.pal-f5-provider-campaign",
            "model": args.model,
            "replicas": args.replicas,
            "caseDigest": canonical_digest(doc),
            "priorDigest": canonical_digest(PRIOR),
            "rows": rows,
        }
        out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        return evidence

    persist()
    for case in doc["cases"]:
        for replica in range(1, args.replicas + 1):
            order = ["raw", "prior"] if replica % 2 else ["prior", "raw"]
            for treatment in order:
                try:
                    row = run_one(doc, case, treatment, args.model, replica, Path(args.secret))
                except Exception as exc:
                    row = {
                        "caseId": case["caseId"], "split": case["split"], "treatment": treatment,
                        "model": args.model, "replica": replica, "runId": None,
                        "stopCode": "provider_or_recovery_exception", "modelCalls": None,
                        "usage": None, "elapsedMs": None, "result": None, "valid": False,
                        "decision": None, "exactCorrect": False, "falseIndependentPlatform": False,
                        "missedEarnedChange": False, "oracleDecision": case["oracleDecision"],
                        "receiptDigest": None, "errorType": type(exc).__name__, "error": str(exc)[:500],
                    }
                rows.append(row)
                evidence = persist()
                print(json.dumps({
                    "case": row["caseId"], "model": args.model, "replica": replica,
                    "treatment": treatment, "valid": row["valid"], "decision": row["decision"],
                    "oracle": row["oracleDecision"], "correct": row["exactCorrect"],
                    "errorType": row.get("errorType"),
                }, ensure_ascii=False), flush=True)
    evidence = persist()
    print(json.dumps({"output": str(out), "rows": len(rows), "digest": canonical_digest(evidence)}, indent=2))


if __name__ == "__main__":
    main()
