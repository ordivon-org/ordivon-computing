from __future__ import annotations

import argparse
import hashlib
import json
import random
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
CAUSE_IDS = list("ABCDEFGH")
TEST_IDS = [f"T{i}" for i in range(1, 9)]
RESULT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "consideredCauseIds": {
            "type": "array",
            "items": {"type": "string", "enum": CAUSE_IDS},
            "minItems": 1,
            "maxItems": 4,
        },
        "selectedCauseId": {"type": "string", "enum": CAUSE_IDS},
        "selectedTestId": {"type": "string", "enum": TEST_IDS},
        "reason": {"type": "string"},
    },
    "required": [
        "consideredCauseIds",
        "selectedCauseId",
        "selectedTestId",
        "reason",
    ],
}


def ref(identity: str, kind: str, value: Any) -> HarnessBoundReference:
    return HarnessBoundReference(identity, kind, canonical_digest(value))


def permute(case: dict[str, Any], seed_text: str) -> dict[str, Any]:
    rng = random.Random(int(hashlib.sha256(seed_text.encode()).hexdigest()[:16], 16))
    cause_display = CAUSE_IDS.copy()
    test_display = TEST_IDS.copy()
    rng.shuffle(cause_display)
    rng.shuffle(test_display)
    cause_map = dict(zip(CAUSE_IDS, cause_display, strict=True))
    test_map = dict(zip(TEST_IDS, test_display, strict=True))
    return {
        "causeOptions": {cause_map[k]: v for k, v in case["causeOptions"].items()},
        "testOptions": {test_map[k]: v for k, v in case["testOptions"].items()},
        "oracleCauseId": cause_map[case["oracleCauseId"]],
        "acceptedTestIds": [test_map[x] for x in case["acceptedTestIds"]],
        "mappingDigest": canonical_digest({"cause": cause_map, "test": test_map}),
    }


def prompt_for(case: dict[str, Any], visible: dict[str, Any], treatment: str) -> str:
    if treatment == "single":
        instruction = (
            "Choose the single best causal model directly. consideredCauseIds must contain "
            "exactly one ID and it must equal selectedCauseId."
        )
    else:
        instruction = (
            "Before selecting, preserve exactly four distinct plausible competing causal models "
            "in consideredCauseIds. Then select the best one from those four."
        )
    return (
        "You are diagnosing a historical engineering/research incident. The later resolution is hidden. "
        "Use only the packet and options below.\n\n"
        + instruction
        + "\nSelect one discriminating test that would best separate the chosen cause from alternatives. "
        "Return only the structured result.\n\nPACKET:\n"
        + case["packet"]
        + "\n\nCAUSE OPTIONS:\n"
        + json.dumps(visible["causeOptions"], ensure_ascii=False, sort_keys=True)
        + "\n\nTEST OPTIONS:\n"
        + json.dumps(visible["testOptions"], ensure_ascii=False, sort_keys=True)
    )


def run_one(
    case: dict[str, Any], treatment: str, model: str, replica: int, secret: Path
) -> dict[str, Any]:
    seed = f"{case['caseId']}|{treatment}|{model}|{replica}"
    visible = permute(case, seed)
    prompt = prompt_for(case, visible, treatment)
    settings = replace(
        DeepSeekSettings.from_secret_file(secret), model=model, max_output_tokens=700
    )
    now = time.time_ns() // 1_000_000
    run_id = f"harness-run:pal-f4:{case['caseId']}:{treatment}:{model}:{replica}:{now}"
    completion = {
        "mode": "structured-result-v1",
        "resultKind": "pal-f4-causal-diagnosis",
        "resultSchema": RESULT_SCHEMA,
    }
    contract = HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@pal-f4",
        caller_id="caller:ordivon-computing-pal",
        caller_run_ref=seed,
        objective_ref=ref(
            f"objective:{case['caseId']}",
            "objective",
            {"case": case["caseId"], "treatment": treatment},
        ),
        context_refs=(
            ref(
                f"context:{case['caseId']}:{treatment}:{replica}",
                "context",
                {"prompt": prompt},
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
            {
                "experiment": "PAL-F4",
                "model": model,
                "treatment": treatment,
                "maxOutputTokens": 700,
            },
        ),
        created_at_ms=now,
        source_refs=(),
        privacy=HarnessPrivacyPolicy(
            content_policy="bounded-private-content",
            allow_model_content=True,
            allow_tool_content=False,
        ),
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-pal-f4-") as state_root:
        run = HarnessAgentRun.create(
            state_root,
            contract,
            lambda exact: DeepSeekTurnAdapter(
                settings, completion_contract=exact.completion_contract
            ),
        )
        started = time.monotonic()
        execution = run.run(({"role": "user", "content": prompt},))
        elapsed_ms = round((time.monotonic() - started) * 1000)
        conclusion = execution.loop_result.conclusion
        decoded = (
            None
            if conclusion is None
            else decode_structured_completion_result(contract, conclusion)
        )
        considered = (
            [] if not isinstance(decoded, dict) else decoded.get("consideredCauseIds", [])
        )
        shape_valid = (
            isinstance(decoded, dict)
            and isinstance(considered, list)
            and len(considered) == len(set(considered))
            and decoded.get("selectedCauseId") in CAUSE_IDS
            and decoded.get("selectedTestId") in TEST_IDS
        )
        treatment_shape_valid = bool(
            shape_valid
            and (
                (
                    treatment == "single"
                    and len(considered) == 1
                    and considered[0] == decoded.get("selectedCauseId")
                )
                or (
                    treatment == "variation"
                    and len(considered) == 4
                    and decoded.get("selectedCauseId") in considered
                )
            )
        )
        cause_ok = bool(
            treatment_shape_valid
            and decoded["selectedCauseId"] == visible["oracleCauseId"]
        )
        test_ok = bool(
            treatment_shape_valid
            and decoded["selectedTestId"] in visible["acceptedTestIds"]
        )
        coverage = bool(
            treatment_shape_valid and visible["oracleCauseId"] in considered
        )
        terminal = execution.terminal_result
        return {
            "caseId": case["caseId"],
            "split": case["split"],
            "treatment": treatment,
            "model": model,
            "replica": replica,
            "runId": run_id,
            "mappingDigest": visible["mappingDigest"],
            "stopCode": execution.loop_result.stop_code.value,
            "modelCalls": execution.loop_result.model_calls,
            "usage": execution.loop_result.usage,
            "elapsedMs": elapsed_ms,
            "result": decoded,
            "shapeValid": shape_valid,
            "treatmentShapeValid": treatment_shape_valid,
            "causeCorrect": cause_ok,
            "testCorrect": test_ok,
            "jointCorrect": cause_ok and test_ok,
            "oracleCoveredByConsidered": coverage,
            "receiptDigest": None if terminal is None else terminal.receipt.digest,
        }


def validate_fixture() -> dict[str, Any]:
    doc = json.loads((ROOT / "f4-cases-v0.json").read_text())
    assert len(doc["cases"]) == 6
    for case in doc["cases"]:
        assert set(case["causeOptions"]) == set(CAUSE_IDS)
        assert set(case["testOptions"]) == set(TEST_IDS)
        assert case["oracleCauseId"] in CAUSE_IDS
        assert case["acceptedTestIds"]
        for test_id in case["acceptedTestIds"]:
            assert test_id in TEST_IDS
        # Ensure permutation preserves hidden truth but changes labels by trial seed.
        for treatment in ("single", "variation"):
            visible = permute(case, f"{case['caseId']}|{treatment}|dry|1")
            assert visible["oracleCauseId"] in CAUSE_IDS
            assert set(visible["causeOptions"]) == set(CAUSE_IDS)
            assert set(visible["testOptions"]) == set(TEST_IDS)
    return {"caseCount": len(doc["cases"]), "caseDigest": canonical_digest(doc)}


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

    doc = json.loads((ROOT / "f4-cases-v0.json").read_text())
    rows: list[dict[str, Any]] = []
    for case in doc["cases"]:
        for replica in range(1, args.replicas + 1):
            order = ["single", "variation"] if replica % 2 else ["variation", "single"]
            for treatment in order:
                row = run_one(case, treatment, args.model, replica, Path(args.secret))
                rows.append(row)
                print(
                    json.dumps(
                        {
                            "case": row["caseId"],
                            "model": args.model,
                            "replica": replica,
                            "treatment": treatment,
                            "valid": row["treatmentShapeValid"],
                            "joint": row["jointCorrect"],
                            "cause": row["causeCorrect"],
                            "test": row["testCorrect"],
                            "coverage": row["oracleCoveredByConsidered"],
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
    evidence = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.pal-f4-provider-campaign",
        "model": args.model,
        "replicas": args.replicas,
        "caseDigest": canonical_digest(doc),
        "rows": rows,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {"output": str(out), "rows": len(rows), "digest": canonical_digest(evidence)},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
