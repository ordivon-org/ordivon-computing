#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

COMPUTING_ROOT = Path(__file__).resolve().parents[3]
WORLD_ROOT = Path(
    "/var/lib/ordivon/runtime/workspaces/world-wml-a10-presence-source-20260809"
)
HARNESS_ROOT = Path(
    "/var/lib/ordivon/runtime/workspaces/harness-wml-a10-world-equipment-20260809"
)
DEPENDENCY_SITE = Path(
    "/root/projects/ordivon-harness/.venv/lib/python3.12/site-packages"
)
SECRET = Path("/root/.config/ordivon/secrets/deepseek.json")
COMPUTING_BASE = "e4e463eda1f2fa245f56c3e8340389a94f0dd97c"
WORLD_REV = "2f9645113538b15e51ce4546f0942b45d10fda29"
HARNESS_REV = "f09c3795fc811c5a564a5285cf227b2a44283cf5"
TREATMENTS = ("RAW_OWNER_RECORDS", "QUERY_RELATION_INDEX")
REPLICATES = (1, 2)
PROGRESS_PATH = Path(__file__).resolve().parent / ".progress.json"
NO_TOOL_DIGEST = (
    "sha256:" + hashlib.sha256(b"wml-a10-world-presence-no-tool").hexdigest()
)

sys.path.insert(0, str(DEPENDENCY_SITE))
sys.path.insert(0, str(HARNESS_ROOT / "src"))
from ordivon_harness.ordivon.deepseek import DeepSeekSettings, DeepSeekTurnAdapter  # noqa: E402
from ordivon_harness.ordivon.model import AgentTurnRequest  # noqa: E402


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()


def git_dirty(root: Path) -> bool:
    return bool(
        subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain"], text=True
        )
    )


def require_exact_sources() -> None:
    for root, expected in ((WORLD_ROOT, WORLD_REV), (HARNESS_ROOT, HARNESS_REV)):
        actual = git_head(root)
        if actual != expected:
            raise RuntimeError(f"{root.name} revision drift: {actual} != {expected}")
        if git_dirty(root):
            raise RuntimeError(f"{root.name} workspace is dirty")


def rec(
    record_id: str,
    *,
    role: str,
    owner_id: str,
    subject_ref: str,
    body_ref: str,
    scope_id: str,
    logical_time: int,
    **fields: Any,
) -> dict[str, Any]:
    return {
        "recordId": record_id,
        "role": role,
        "ownerId": owner_id,
        "subjectRef": subject_ref,
        "bodyRef": body_ref,
        "scopeId": scope_id,
        "logicalTime": logical_time,
        **fields,
    }


SUBJECT = "continuity-subject:medic-reyes"
GAME_OWNER = "ordivon.game.station-zero-v3"
GAME_BODY = "game-actor:medic-reyes"
SEC_OWNER = "ordivon.security.windows-kvm"
SEC_BODY_A = "security-kvm:body-a"
SEC_BODY_B = "security-kvm:body-b"


def base_records() -> dict[str, dict[str, Any]]:
    return {
        "game_r0_occurrence": rec(
            "record:game:r0:bounded-occurrence",
            role="bounded-embodiment-occurrence",
            owner_id=GAME_OWNER,
            subject_ref=SUBJECT,
            body_ref=GAME_BODY,
            scope_id="planning:r0",
            logical_time=10,
            occurrence="actor-moved",
            nativeEffectVerified=True,
        ),
        "game_r1_body": rec(
            "record:game:r1:body-observation",
            role="native-body-observation",
            owner_id=GAME_OWNER,
            subject_ref=SUBJECT,
            body_ref=GAME_BODY,
            scope_id="planning:r1",
            logical_time=20,
            bodyCurrent=True,
            lifeState="active",
        ),
        "game_r0_binding_rejected_r1": rec(
            "record:game:r1:old-binding-rejection",
            role="destination-admission-rejection",
            owner_id=GAME_OWNER,
            subject_ref=SUBJECT,
            body_ref=GAME_BODY,
            scope_id="planning:r1",
            logical_time=21,
            presentedBindingScopeId="planning:r0",
            admitted=False,
            reason="old binding does not authorize new planning scope",
        ),
        "game_r1_binding": rec(
            "record:game:r1:current-binding",
            role="destination-subject-binding",
            owner_id=GAME_OWNER,
            subject_ref=SUBJECT,
            body_ref=GAME_BODY,
            scope_id="planning:r1",
            logical_time=22,
            admitted=True,
            exactScopeBinding=True,
        ),
        "game_r1_occurrence": rec(
            "record:game:r1:bounded-occurrence",
            role="bounded-embodiment-occurrence",
            owner_id=GAME_OWNER,
            subject_ref=SUBJECT,
            body_ref=GAME_BODY,
            scope_id="planning:r1",
            logical_time=23,
            occurrence="guard-command-deck",
            nativeEffectVerified=True,
        ),
        "sec_materialization": rec(
            "record:security:body-a:materialization",
            role="entity-materialization-receipt",
            owner_id=SEC_OWNER,
            subject_ref=SUBJECT,
            body_ref=SEC_BODY_A,
            scope_id="migration:a",
            logical_time=10,
            migrationStatus="materialized",
            historicalTerminalReceipt=True,
        ),
        "sec_body_current": rec(
            "record:security:body-a:native-body-current",
            role="native-body-observation",
            owner_id=SEC_OWNER,
            subject_ref=SUBJECT,
            body_ref=SEC_BODY_A,
            scope_id="activation:a",
            logical_time=20,
            bodyCurrent=True,
            qemuAlive=True,
        ),
        "sec_subject_unproven": rec(
            "record:security:body-a:subject-activation-unproven",
            role="subject-binding-status",
            owner_id=SEC_OWNER,
            subject_ref=SUBJECT,
            body_ref=SEC_BODY_A,
            scope_id="activation:a",
            logical_time=21,
            subjectActivationProven=False,
        ),
        "sec_destroyed": rec(
            "record:security:body-a:destroyed",
            role="native-body-observation",
            owner_id=SEC_OWNER,
            subject_ref=SUBJECT,
            body_ref=SEC_BODY_A,
            scope_id="post-destroy:a",
            logical_time=30,
            bodyCurrent=False,
            qemuAlive=False,
            ledgerExists=False,
            runPathExists=False,
        ),
        "sec_observation_timeout": rec(
            "record:security:body-a:observation-timeout",
            role="current-owner-observation-attempt",
            owner_id=SEC_OWNER,
            subject_ref=SUBJECT,
            body_ref=SEC_BODY_A,
            scope_id="query:timeout:a",
            logical_time=25,
            status="timeout",
            bodyCurrentnessEstablished=False,
            bindingCurrentnessEstablished=False,
        ),
        "sec_body_b_materialization": rec(
            "record:security:body-b:materialization",
            role="entity-materialization-receipt",
            owner_id=SEC_OWNER,
            subject_ref=SUBJECT,
            body_ref=SEC_BODY_B,
            scope_id="migration:b",
            logical_time=40,
            migrationStatus="materialized",
            historicalTerminalReceipt=True,
        ),
        "sec_body_b_observation_failed": rec(
            "record:security:body-b:observation-failed",
            role="current-owner-observation-attempt",
            owner_id=SEC_OWNER,
            subject_ref=SUBJECT,
            body_ref=SEC_BODY_B,
            scope_id="query:b",
            logical_time=41,
            status="holder-expired-before-valid-owner-observation",
            currentPresenceClaimRetained=False,
        ),
    }


def cases() -> list[dict[str, Any]]:
    r = base_records()
    return [
        {
            "caseId": "game-new-scope-old-occurrence",
            "query": {
                "queryId": "query:game:r1:before-binding",
                "subjectRef": SUBJECT,
                "bodyRef": GAME_BODY,
                "ownerId": GAME_OWNER,
                "scopeId": "planning:r1",
                "question": "What current Presence relation is established for this exact Game body and planning scope?",
            },
            "records": [
                r["game_r0_occurrence"],
                r["game_r1_body"],
                r["game_r0_binding_rejected_r1"],
            ],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "unknown",
        },
        {
            "caseId": "game-new-scope-current-binding",
            "query": {
                "queryId": "query:game:r1:after-binding",
                "subjectRef": SUBJECT,
                "bodyRef": GAME_BODY,
                "ownerId": GAME_OWNER,
                "scopeId": "planning:r1",
                "question": "What current Presence relation is established for this exact Game body and planning scope?",
            },
            "records": [
                r["game_r0_occurrence"],
                r["game_r1_body"],
                r["game_r1_binding"],
                r["game_r1_occurrence"],
            ],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "present-within-scope",
        },
        {
            "caseId": "security-current-body-subject-unproven",
            "query": {
                "queryId": "query:security:a:before-destroy",
                "subjectRef": SUBJECT,
                "bodyRef": SEC_BODY_A,
                "ownerId": SEC_OWNER,
                "scopeId": "activation:a",
                "question": "What current Presence relation is established through Security body A?",
            },
            "records": [
                r["sec_materialization"],
                r["sec_body_current"],
                r["sec_subject_unproven"],
            ],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "unknown",
        },
        {
            "caseId": "security-destroyed-body-history-survives",
            "query": {
                "queryId": "query:security:a:after-destroy",
                "subjectRef": SUBJECT,
                "bodyRef": SEC_BODY_A,
                "ownerId": SEC_OWNER,
                "scopeId": "post-destroy:a",
                "question": "What current Presence relation is established through Security body A?",
            },
            "records": [r["sec_materialization"], r["sec_destroyed"]],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "absent-through-body",
        },
        {
            "caseId": "security-current-observation-timeout",
            "query": {
                "queryId": "query:security:a:timeout",
                "subjectRef": SUBJECT,
                "bodyRef": SEC_BODY_A,
                "ownerId": SEC_OWNER,
                "scopeId": "query:timeout:a",
                "question": "What current Presence relation is established through Security body A after the current owner observation attempt?",
            },
            "records": [r["sec_materialization"], r["sec_observation_timeout"]],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "unknown",
        },
        {
            "caseId": "multi-body-query-game-body",
            "query": {
                "queryId": "query:multi:game",
                "subjectRef": SUBJECT,
                "bodyRef": GAME_BODY,
                "ownerId": GAME_OWNER,
                "scopeId": "planning:r1",
                "question": "Given evidence about two different bodies of the same Subject, what relation is established for the queried Game body?",
            },
            "records": [
                r["game_r1_body"],
                r["game_r1_binding"],
                r["game_r1_occurrence"],
                r["sec_materialization"],
                r["sec_destroyed"],
            ],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "present-within-scope",
        },
        {
            "caseId": "multi-body-query-security-body-a",
            "query": {
                "queryId": "query:multi:security-a",
                "subjectRef": SUBJECT,
                "bodyRef": SEC_BODY_A,
                "ownerId": SEC_OWNER,
                "scopeId": "post-destroy:a",
                "question": "Given evidence about two different bodies of the same Subject, what relation is established for the queried Security body A?",
            },
            "records": [
                r["game_r1_body"],
                r["game_r1_binding"],
                r["game_r1_occurrence"],
                r["sec_materialization"],
                r["sec_destroyed"],
            ],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "absent-through-body",
        },
        {
            "caseId": "replacement-body-b-old-body-a-evidence",
            "query": {
                "queryId": "query:security:b",
                "subjectRef": SUBJECT,
                "bodyRef": SEC_BODY_B,
                "ownerId": SEC_OWNER,
                "scopeId": "query:b",
                "question": "What current Presence relation is established through replacement Security body B?",
            },
            "records": [
                r["sec_materialization"],
                r["sec_destroyed"],
                r["sec_body_b_materialization"],
                r["sec_body_b_observation_failed"],
            ],
            "allowedAnswers": [
                "present-within-scope",
                "absent-through-body",
                "unknown",
            ],
            "expected": "unknown",
        },
    ]


def relation_index(case: dict[str, Any]) -> dict[str, Any]:
    q = case["query"]
    idx: dict[str, list[str]] = {
        "exactBodyOwnerRecords": [],
        "differentBodyOrOwnerRecords": [],
        "exactScopeRecords": [],
        "differentScopeRecords": [],
        "boundedHistoricalOccurrenceOrMaterialization": [],
        "currentOwnerObservationRecords": [],
        "currentScopedBindingOrAdmissionRecords": [],
        "failedCurrentObservationRecords": [],
    }
    for item in case["records"]:
        rid = item["recordId"]
        exact_body_owner = (
            item["bodyRef"] == q["bodyRef"] and item["ownerId"] == q["ownerId"]
        )
        (
            idx["exactBodyOwnerRecords"]
            if exact_body_owner
            else idx["differentBodyOrOwnerRecords"]
        ).append(rid)
        (
            idx["exactScopeRecords"]
            if item["scopeId"] == q["scopeId"]
            else idx["differentScopeRecords"]
        ).append(rid)
        if item["role"] in {
            "bounded-embodiment-occurrence",
            "entity-materialization-receipt",
        }:
            idx["boundedHistoricalOccurrenceOrMaterialization"].append(rid)
        if item["role"] == "native-body-observation" and exact_body_owner:
            idx["currentOwnerObservationRecords"].append(rid)
        if (
            item["role"]
            in {
                "destination-subject-binding",
                "destination-admission-rejection",
                "subject-binding-status",
            }
            and exact_body_owner
            and item["scopeId"] == q["scopeId"]
        ):
            idx["currentScopedBindingOrAdmissionRecords"].append(rid)
        if (
            item["role"] == "current-owner-observation-attempt"
            and exact_body_owner
            and item.get("status") != "completed"
        ):
            idx["failedCurrentObservationRecords"].append(rid)
    return {
        "queryCoordinates": {
            k: q[k] for k in ("queryId", "subjectRef", "bodyRef", "ownerId", "scopeId")
        },
        "recordRelations": idx,
    }


def visible_case(case: dict[str, Any], treatment: str) -> dict[str, Any]:
    value = {
        "caseId": case["caseId"],
        "query": case["query"],
        "records": case["records"],
        "allowedAnswers": case["allowedAnswers"],
    }
    if treatment == "QUERY_RELATION_INDEX":
        value["queryRelationIndex"] = relation_index(case)
    return value


def completion_schema(case: dict[str, Any]) -> dict[str, Any]:
    ids = [r["recordId"] for r in case["records"]]
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "answer": {"type": "string", "enum": case["allowedAnswers"]},
            "basisRecordIds": {
                "type": "array",
                "items": {"type": "string", "enum": ids},
                "minItems": 1,
                "uniqueItems": True,
            },
            "reason": {"type": "string", "minLength": 1},
        },
        "required": ["answer", "basisRecordIds", "reason"],
    }


def prompt(case: dict[str, Any], treatment: str) -> str:
    return canonical(
        {
            "experiment": "WML-A10-WORLD-PRESENCE-v0",
            "treatment": treatment,
            "ownerLaw": [
                "Presence is an owner-observed scope-bound current relation, not a durable boolean property of Subject or Body.",
                "Historical bounded embodiment occurrence or materialization does not by itself establish current Presence.",
                "A current Body plus an exact current scoped Subject binding can establish present-within-scope for that query scope.",
                "Exact current Body absence establishes absent-through-body for that Body only, not global Subject absence.",
                "Current owner observation failure or current Body with missing/unproven current Subject binding yields unknown.",
                "Evidence for a different Body or different scope must not be promoted into the queried current relation.",
                "Presence observation is informational evidence and does not authorize an action.",
            ],
            "instruction": "Use only the supplied owner records and owner law. Determine the Presence relation established for the exact query coordinates. Do not infer persistent Presence from historical success and do not globalize one Body state to another Body.",
            "case": visible_case(case, treatment),
        }
    )


def structured_call(
    *, run_id: str, prompt_text: str, schema: dict[str, Any], settings: DeepSeekSettings
) -> tuple[dict[str, Any], dict[str, Any]]:
    adapter = DeepSeekTurnAdapter(
        settings,
        completion_contract={
            "mode": "structured-result-v1",
            "resultKind": "world-presence-decision-v0",
            "resultSchema": schema,
        },
    )
    request = AgentTurnRequest(
        harness_run_id=run_id,
        turn_id=f"turn:{run_id}",
        sequence=1,
        assignment_id=f"assignment:{run_id}",
        context_digest="sha256:" + hashlib.sha256(prompt_text.encode()).hexdigest(),
        tool_catalog_digest=NO_TOOL_DIGEST,
        messages=({"role": "user", "content": prompt_text},),
        tools=(),
        remaining_budget={"modelCalls": 1, "toolCalls": 0, "totalTokens": 32768},
    )
    result = adapter.invoke(request)
    if result.conclusion is None:
        raise RuntimeError("Provider did not submit structured conclusion")
    value = json.loads(result.conclusion.summary)
    return value, {
        "requestDigest": request.digest,
        "resultDigest": result.digest,
        "modelCallId": result.model_call_id,
        "modelId": result.model_id,
        "effectiveModelId": result.effective_model,
        "usage": result.usage,
        "rawResponseDigest": result.raw_response_digest,
    }


def owner_evidence() -> list[dict[str, Any]]:
    refs = [
        "evidence/acceptance/w5a-a4-presence-888ca4e.json",
        "evidence/acceptance/w5b-b0-agent-current-relation-e40842d.json",
        "evidence/acceptance/w5b-b1-security-active-destination-e40842d.json",
    ]
    out = []
    for ref in refs:
        p = WORLD_ROOT / ref
        if not p.is_file():
            raise FileNotFoundError(p)
        value = json.loads(p.read_text())
        if value.get("status") not in {"passed", "accepted"}:
            raise RuntimeError(f"owner evidence not accepted: {ref}")
        out.append({"ref": ref, "sha256": file_sha256(p), "kind": value.get("kind")})
    return out


def identity(settings: DeepSeekSettings) -> dict[str, Any]:
    return {
        "experimentId": "WML-A10-WORLD-PRESENCE-v0",
        "computingBaseRevision": COMPUTING_BASE,
        "worldRevision": WORLD_REV,
        "harnessRevision": HARNESS_REV,
        "model": settings.model,
        "credentialScopeId": settings.credential_scope_id,
        "casesDigest": digest(cases()),
        "treatments": list(TREATMENTS),
        "replicates": list(REPLICATES),
        "ownerEvidence": owner_evidence(),
    }


def empty_progress(exp_id: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world-model-a10-world-presence-progress",
        "identity": exp_id,
        "identityDigest": digest(exp_id),
        "records": {},
    }


def load_progress(exp_id: dict[str, Any]) -> dict[str, Any]:
    expected = empty_progress(exp_id)
    if not PROGRESS_PATH.exists():
        return expected
    value = json.loads(PROGRESS_PATH.read_text())
    if (
        value.get("identityDigest") != expected["identityDigest"]
        or value.get("identity") != exp_id
    ):
        raise RuntimeError("progress identity differs")
    return value


def save_progress(progress: dict[str, Any]) -> None:
    tmp = PROGRESS_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(PROGRESS_PATH)


def error_class(expected: str, answer: str) -> str | None:
    if answer == expected:
        return None
    if expected == "unknown" and answer != "unknown":
        return "false-current-certainty"
    if expected == "present-within-scope" and answer == "absent-through-body":
        return "false-absence"
    if expected == "absent-through-body" and answer == "present-within-scope":
        return "false-presence"
    if expected != "unknown" and answer == "unknown":
        return "false-abstention"
    return "wrong-relation"


def number(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) else 0


def run_one(
    *,
    case: dict[str, Any],
    treatment: str,
    replicate: int,
    settings: DeepSeekSettings,
    progress: dict[str, Any],
) -> dict[str, Any]:
    key = f"{case['caseId']}:{treatment}:r{replicate}"
    if key in progress["records"]:
        row = progress["records"][key]
        print(
            f"{case['caseId']:44} {treatment:22} r{replicate} REPLAY answer={row['answer']:22} expected={case['expected']:22} ok={row['correct']}",
            flush=True,
        )
        return row
    text = prompt(case, treatment)
    result, evidence = structured_call(
        run_id=f"wml-a10-world:{case['caseId']}:{treatment.lower()}:r{replicate}",
        prompt_text=text,
        schema=completion_schema(case),
        settings=settings,
    )
    answer = result["answer"]
    basis = list(result["basisRecordIds"])
    ids = {r["recordId"] for r in case["records"]}
    row = {
        "caseId": case["caseId"],
        "treatment": treatment,
        "replicate": replicate,
        "expected": case["expected"],
        "answer": answer,
        "correct": answer == case["expected"],
        "errorClass": error_class(case["expected"], answer),
        "basisRecordIds": basis,
        "basisValid": bool(basis) and set(basis).issubset(ids),
        "result": result,
        "promptDigest": "sha256:" + hashlib.sha256(text.encode()).hexdigest(),
        "modelEvidence": evidence,
    }
    progress["records"][key] = row
    save_progress(progress)
    print(
        f"{case['caseId']:44} {treatment:22} r{replicate} answer={answer:22} expected={case['expected']:22} ok={row['correct']}",
        flush=True,
    )
    return row


def summarize(records: list[dict[str, Any]], treatment: str) -> dict[str, Any]:
    rows = [r for r in records if r["treatment"] == treatment]
    return {
        "decisions": len(rows),
        "correct": sum(int(r["correct"]) for r in rows),
        "accuracy": sum(int(r["correct"]) for r in rows) / len(rows),
        "falseCurrentCertainty": sum(
            int(r["errorClass"] == "false-current-certainty") for r in rows
        ),
        "falseAbsence": sum(int(r["errorClass"] == "false-absence") for r in rows),
        "falsePresence": sum(int(r["errorClass"] == "false-presence") for r in rows),
        "falseAbstention": sum(
            int(r["errorClass"] == "false-abstention") for r in rows
        ),
        "basisValid": sum(int(r["basisValid"]) for r in rows),
        "providerPromptTokens": sum(
            number(r["modelEvidence"]["usage"].get("prompt_tokens")) for r in rows
        ),
        "providerTotalTokens": sum(
            number(r["modelEvidence"]["usage"].get("total_tokens")) for r in rows
        ),
    }


def main() -> None:
    require_exact_sources()
    settings = DeepSeekSettings.from_secret_file(
        SECRET, max_output_tokens=640, timeout_seconds=90.0
    )
    exp_id = identity(settings)
    progress = load_progress(exp_id)
    save_progress(progress)
    all_cases = cases()
    records = []
    for replicate in REPLICATES:
        order = TREATMENTS if replicate == 1 else tuple(reversed(TREATMENTS))
        for case in all_cases:
            for treatment in order:
                records.append(
                    run_one(
                        case=case,
                        treatment=treatment,
                        replicate=replicate,
                        settings=settings,
                        progress=progress,
                    )
                )
    summaries = {t: summarize(records, t) for t in TREATMENTS}
    pairs = []
    for case in all_cases:
        for replicate in REPLICATES:
            raw = next(
                r
                for r in records
                if r["caseId"] == case["caseId"]
                and r["replicate"] == replicate
                and r["treatment"] == "RAW_OWNER_RECORDS"
            )
            idx = next(
                r
                for r in records
                if r["caseId"] == case["caseId"]
                and r["replicate"] == replicate
                and r["treatment"] == "QUERY_RELATION_INDEX"
            )
            pairs.append(
                {
                    "caseId": case["caseId"],
                    "replicate": replicate,
                    "rawCorrect": raw["correct"],
                    "indexCorrect": idx["correct"],
                    "answerChanged": raw["answer"] != idx["answer"],
                    "indexFixedRawError": (not raw["correct"]) and idx["correct"],
                    "indexHarmedRawCorrect": raw["correct"] and (not idx["correct"]),
                }
            )
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.world-model-a10-world-presence-experiment",
        "status": "completed",
        "identity": exp_id,
        "cases": all_cases,
        "records": records,
        "summary": summaries,
        "pairedComparison": {
            "pairs": len(pairs),
            "answerChanged": sum(int(p["answerChanged"]) for p in pairs),
            "indexFixedRawError": sum(int(p["indexFixedRawError"]) for p in pairs),
            "indexHarmedRawCorrect": sum(
                int(p["indexHarmedRawCorrect"]) for p in pairs
            ),
            "details": pairs,
        },
        "externalWorldEffectAttempted": False,
        "interpretationBoundary": "Second-domain A10 falsifier over owner-defined World Presence laws. QUERY_RELATION_INDEX is deterministic experiment-local evidence organization, not a Presence registry, truth service, or action authority.",
    }
    payload = digest(receipt)
    receipt["integrity"] = {"algorithm": "sha256", "payloadDigest": payload}
    out = (
        COMPUTING_ROOT
        / "research/evidence"
        / f"wml-a10-world-presence-{payload[7:19]}.json"
    )
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    PROGRESS_PATH.unlink(missing_ok=True)
    print("RECEIPT", out.relative_to(COMPUTING_ROOT), payload, flush=True)
    print("SUMMARY", json.dumps(summaries, sort_keys=True), flush=True)
    print("PAIRED", json.dumps(receipt["pairedComparison"], sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
