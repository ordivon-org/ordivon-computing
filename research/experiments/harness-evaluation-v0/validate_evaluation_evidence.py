#!/usr/bin/env python3
"""Validate Track R evaluation records without external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

DIGEST_PREFIX = "sha256:"
KINDS = {
    "ordivon.evaluation-task",
    "ordivon.evaluation-trial",
    "ordivon.evaluation-result",
    "ordivon.evaluation-failure",
}
BUDGET_FIELDS = {
    "maxModelCalls",
    "maxToolCalls",
    "maxRuntimeJobs",
    "maxObservationBytes",
    "maxWallTimeMs",
    "maxInputTokens",
    "maxOutputTokens",
}
METRIC_FIELDS = {
    "modelCalls",
    "toolCalls",
    "runtimeJobs",
    "observationBytes",
    "inputTokens",
    "outputTokens",
    "cachedInputTokens",
    "reasoningTokens",
    "totalTokens",
    "wallTimeMs",
    "estimatedCostUsd",
    "repeatedReads",
    "repeatedCommands",
    "invalidToolCalls",
    "humanInterventionCount",
}
FAILURE_CODES = {
    "CONTEXT": {"stale_source", "stale_assignment", "missing_fact", "provenance_lost", "goal_drift"},
    "MODEL": {"invalid_output", "false_completion", "premature_stop", "repeated_plan"},
    "TOOL": {"invalid_arguments", "unsupported_capability", "partial_observation", "schema_drift"},
    "EFFECT": {"unknown_delivery", "duplicate_effect", "reconciliation_failed"},
    "HARNESS": {"result_misrouting", "budget_error", "loop_nontermination", "state_loss"},
    "VERIFIER": {"false_accept", "false_reject", "flaky_assertion", "hidden_requirement"},
    "ENVIRONMENT": {"nondeterminism", "resource_exhaustion", "leaked_state"},
}


def canonical_payload(document: dict[str, Any]) -> bytes:
    payload = dict(document)
    payload.pop("integrity", None)
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def payload_digest(document: dict[str, Any]) -> str:
    return DIGEST_PREFIX + hashlib.sha256(canonical_payload(document)).hexdigest()


def _exact(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{label} fields differ; missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _nullable_nonnegative_integer(value: Any, label: str) -> None:
    if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 0):
        raise ValueError(f"{label} must be null or a non-negative integer")


def _nullable_nonnegative_number(value: Any, label: str) -> None:
    if value is not None and (
        isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
    ):
        raise ValueError(f"{label} must be null or a non-negative number")


def _digest(value: Any, label: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or len(value) != 71 or not value.startswith(DIGEST_PREFIX):
        raise ValueError(f"{label} must be sha256:<64 lowercase hex>")
    suffix = value.removeprefix(DIGEST_PREFIX)
    if any(character not in "0123456789abcdef" for character in suffix):
        raise ValueError(f"{label} must be sha256:<64 lowercase hex>")


def _revision(value: Any, label: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or len(value) != 40:
        raise ValueError(f"{label} must be a 40-character lowercase Git revision")
    if any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{label} must be a 40-character lowercase Git revision")


def _string_list(value: Any, label: str, *, minimum: int = 0, unique: bool = False) -> None:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{label} must be a list containing at least {minimum} entries")
    for index, item in enumerate(value):
        _nonempty(item, f"{label}[{index}]")
    if unique and len(value) != len(set(value)):
        raise ValueError(f"{label} entries must be unique")


def _validate_integrity(document: dict[str, Any]) -> None:
    integrity = document.get("integrity")
    if not isinstance(integrity, dict):
        raise ValueError("integrity must be an object")
    _exact(integrity, {"algorithm", "canonicalization", "payloadDigest"}, "integrity")
    if integrity["algorithm"] != "sha256":
        raise ValueError("integrity algorithm differs")
    if integrity["canonicalization"] != "ordivon-canonical-json-v1":
        raise ValueError("integrity canonicalization differs")
    _digest(integrity["payloadDigest"], "integrity payloadDigest")
    expected = payload_digest(document)
    if integrity["payloadDigest"] != expected:
        raise ValueError(
            f"integrity payloadDigest differs; expected={expected}, "
            f"observed={integrity['payloadDigest']}"
        )


def _validate_budget(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    _exact(value, BUDGET_FIELDS, label)
    for field, amount in value.items():
        _nullable_nonnegative_integer(amount, f"{label}.{field}")


def _validate_task_ref(value: Any, label: str = "taskRef") -> tuple[str, int]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    _exact(value, {"taskId", "taskVersion"}, label)
    task_id = _nonempty(value["taskId"], f"{label}.taskId")
    task_version = value["taskVersion"]
    if isinstance(task_version, bool) or not isinstance(task_version, int) or task_version < 1:
        raise ValueError(f"{label}.taskVersion must be a positive integer")
    return task_id, task_version


def validate_task(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "taskId",
        "taskVersion",
        "family",
        "objective",
        "initialState",
        "allowedCapabilities",
        "budgetProfile",
        "acceptanceContract",
        "oracle",
        "expertTimeEstimateMinutes",
        "reproducibility",
        "knownLimitations",
        "labels",
        "integrity",
    }
    _exact(document, expected, "Task Definition")
    if document["schemaVersion"] != 1 or document["kind"] != "ordivon.evaluation-task":
        raise ValueError("unsupported Task Definition identity")
    _nonempty(document["taskId"], "taskId")
    if isinstance(document["taskVersion"], bool) or not isinstance(document["taskVersion"], int) or document["taskVersion"] < 1:
        raise ValueError("taskVersion must be a positive integer")
    _nonempty(document["family"], "family")
    _nonempty(document["objective"], "objective")

    initial = document["initialState"]
    if not isinstance(initial, dict):
        raise ValueError("initialState must be an object")
    _exact(initial, {"sourceRepositoryId", "sourceRevision", "fixturePath", "environmentDigest"}, "initialState")
    _nonempty(initial["sourceRepositoryId"], "initialState.sourceRepositoryId")
    _revision(initial["sourceRevision"], "initialState.sourceRevision", nullable=True)
    _nonempty(initial["fixturePath"], "initialState.fixturePath")
    _digest(initial["environmentDigest"], "initialState.environmentDigest", nullable=True)

    _string_list(document["allowedCapabilities"], "allowedCapabilities", unique=True)
    _validate_budget(document["budgetProfile"], "budgetProfile")

    acceptance = document["acceptanceContract"]
    if not isinstance(acceptance, dict):
        raise ValueError("acceptanceContract must be an object")
    _exact(acceptance, {"verifierId", "verifierRevision", "assertions", "requiredArtifacts"}, "acceptanceContract")
    _nonempty(acceptance["verifierId"], "acceptanceContract.verifierId")
    _nonempty(acceptance["verifierRevision"], "acceptanceContract.verifierRevision")
    _string_list(acceptance["assertions"], "acceptanceContract.assertions", minimum=1, unique=True)
    _string_list(acceptance["requiredArtifacts"], "acceptanceContract.requiredArtifacts", unique=True)

    oracle = document["oracle"]
    if oracle is not None:
        if not isinstance(oracle, dict):
            raise ValueError("oracle must be null or an object")
        _exact(oracle, {"kind", "path", "digest"}, "oracle")
        _nonempty(oracle["kind"], "oracle.kind")
        _nonempty(oracle["path"], "oracle.path")
        _digest(oracle["digest"], "oracle.digest")

    _nullable_nonnegative_number(document["expertTimeEstimateMinutes"], "expertTimeEstimateMinutes")
    if document["expertTimeEstimateMinutes"] == 0:
        raise ValueError("expertTimeEstimateMinutes must be positive when known")

    reproducibility = document["reproducibility"]
    if not isinstance(reproducibility, dict):
        raise ValueError("reproducibility must be an object")
    _exact(reproducibility, {"cleanRebuildTrials", "requiredAgreement"}, "reproducibility")
    trials = reproducibility["cleanRebuildTrials"]
    agreement = reproducibility["requiredAgreement"]
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 1 for value in (trials, agreement)):
        raise ValueError("reproducibility values must be positive integers")
    if agreement > trials:
        raise ValueError("requiredAgreement cannot exceed cleanRebuildTrials")
    _string_list(document["knownLimitations"], "knownLimitations")
    _string_list(document["labels"], "labels", unique=True)
    _validate_integrity(document)


def validate_trial(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "trialId",
        "taskRef",
        "executionPath",
        "model",
        "harness",
        "bindings",
        "sampling",
        "budget",
        "startedAtMs",
        "completedAtMs",
        "sourceEvidenceRefs",
        "limitations",
        "integrity",
    }
    _exact(document, expected, "Trial Manifest")
    if document["schemaVersion"] != 1 or document["kind"] != "ordivon.evaluation-trial":
        raise ValueError("unsupported Trial Manifest identity")
    _nonempty(document["trialId"], "trialId")
    _validate_task_ref(document["taskRef"])
    if document["executionPath"] not in {
        "one_shot",
        "ordivon_harness",
        "provider_harness",
        "replay",
        "historical_projection",
    }:
        raise ValueError("unsupported executionPath")

    model = document["model"]
    if not isinstance(model, dict):
        raise ValueError("model must be an object")
    _exact(model, {"providerId", "modelId", "modelRevision", "adapterRevision"}, "model")
    _nonempty(model["providerId"], "model.providerId")
    _nonempty(model["modelId"], "model.modelId")
    if model["modelRevision"] is not None:
        _nonempty(model["modelRevision"], "model.modelRevision")
    if model["adapterRevision"] is not None:
        _nonempty(model["adapterRevision"], "model.adapterRevision")

    harness = document["harness"]
    if not isinstance(harness, dict):
        raise ValueError("harness must be an object")
    _exact(harness, {"harnessId", "harnessRevision", "manifestDigest"}, "harness")
    _nonempty(harness["harnessId"], "harness.harnessId")
    if harness["harnessRevision"] is not None:
        _nonempty(harness["harnessRevision"], "harness.harnessRevision")
    _digest(harness["manifestDigest"], "harness.manifestDigest", nullable=True)

    bindings = document["bindings"]
    if not isinstance(bindings, dict):
        raise ValueError("bindings must be an object")
    _exact(
        bindings,
        {"sourceRevision", "environmentDigest", "contextDigest", "toolCatalogDigest", "systemSnapshotRef"},
        "bindings",
    )
    _revision(bindings["sourceRevision"], "bindings.sourceRevision", nullable=True)
    _digest(bindings["environmentDigest"], "bindings.environmentDigest", nullable=True)
    _digest(bindings["contextDigest"], "bindings.contextDigest", nullable=True)
    _digest(bindings["toolCatalogDigest"], "bindings.toolCatalogDigest", nullable=True)
    if bindings["systemSnapshotRef"] is not None:
        _nonempty(bindings["systemSnapshotRef"], "bindings.systemSnapshotRef")

    sampling = document["sampling"]
    if not isinstance(sampling, dict):
        raise ValueError("sampling must be an object")
    _exact(sampling, {"seed", "temperature", "topP", "reasoningEffort"}, "sampling")
    if sampling["seed"] is not None and (isinstance(sampling["seed"], bool) or not isinstance(sampling["seed"], int)):
        raise ValueError("sampling.seed must be null or an integer")
    _nullable_nonnegative_number(sampling["temperature"], "sampling.temperature")
    _nullable_nonnegative_number(sampling["topP"], "sampling.topP")
    if sampling["topP"] is not None and sampling["topP"] > 1:
        raise ValueError("sampling.topP cannot exceed 1")
    if sampling["reasoningEffort"] is not None:
        _nonempty(sampling["reasoningEffort"], "sampling.reasoningEffort")

    _validate_budget(document["budget"], "budget")
    _nullable_nonnegative_integer(document["startedAtMs"], "startedAtMs")
    _nullable_nonnegative_integer(document["completedAtMs"], "completedAtMs")
    if document["startedAtMs"] is not None and document["completedAtMs"] is not None and document["completedAtMs"] < document["startedAtMs"]:
        raise ValueError("completedAtMs precedes startedAtMs")

    evidence = document["sourceEvidenceRefs"]
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("sourceEvidenceRefs must be a non-empty list")
    for index, reference in enumerate(evidence):
        if not isinstance(reference, dict):
            raise ValueError(f"sourceEvidenceRefs[{index}] must be an object")
        _exact(reference, {"repositoryId", "path", "digest"}, f"sourceEvidenceRefs[{index}]")
        _nonempty(reference["repositoryId"], f"sourceEvidenceRefs[{index}].repositoryId")
        _nonempty(reference["path"], f"sourceEvidenceRefs[{index}].path")
        _digest(reference["digest"], f"sourceEvidenceRefs[{index}].digest")
    _string_list(document["limitations"], "limitations")
    _validate_integrity(document)


def validate_result(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "trialId",
        "taskRef",
        "stopCode",
        "acceptance",
        "metrics",
        "artifacts",
        "trace",
        "failureRefs",
        "limitations",
        "integrity",
    }
    _exact(document, expected, "Trial Result")
    if document["schemaVersion"] != 1 or document["kind"] != "ordivon.evaluation-result":
        raise ValueError("unsupported Trial Result identity")
    _nonempty(document["trialId"], "trialId")
    _validate_task_ref(document["taskRef"])
    _nonempty(document["stopCode"], "stopCode")

    acceptance = document["acceptance"]
    if not isinstance(acceptance, dict):
        raise ValueError("acceptance must be an object")
    _exact(acceptance, {"status", "decisionRef", "falseCompletion", "verifier"}, "acceptance")
    if acceptance["status"] not in {"accepted", "rejected", "not_adjudicated"}:
        raise ValueError("unsupported acceptance status")
    if acceptance["decisionRef"] is not None:
        _nonempty(acceptance["decisionRef"], "acceptance.decisionRef")
    if not isinstance(acceptance["falseCompletion"], bool):
        raise ValueError("acceptance.falseCompletion must be boolean")

    verifier = acceptance["verifier"]
    if not isinstance(verifier, dict):
        raise ValueError("acceptance.verifier must be an object")
    _exact(verifier, {"verifierId", "verifierRevision", "status", "assertions"}, "acceptance.verifier")
    if verifier["status"] not in {"passed", "failed", "not_run"}:
        raise ValueError("unsupported verifier status")
    for field in ("verifierId", "verifierRevision"):
        if verifier[field] is not None:
            _nonempty(verifier[field], f"acceptance.verifier.{field}")
    if not isinstance(verifier["assertions"], list):
        raise ValueError("acceptance.verifier.assertions must be a list")
    for index, assertion in enumerate(verifier["assertions"]):
        if not isinstance(assertion, dict):
            raise ValueError(f"assertion[{index}] must be an object")
        _exact(assertion, {"assertionId", "status", "evidenceRefs"}, f"assertion[{index}]")
        _nonempty(assertion["assertionId"], f"assertion[{index}].assertionId")
        if assertion["status"] not in {"passed", "failed", "unknown"}:
            raise ValueError(f"assertion[{index}] has unsupported status")
        _string_list(assertion["evidenceRefs"], f"assertion[{index}].evidenceRefs")

    if acceptance["status"] == "accepted":
        if verifier["status"] != "passed":
            raise ValueError("accepted Trial requires a passed verifier")
        if acceptance["falseCompletion"]:
            raise ValueError("accepted Trial cannot be marked falseCompletion")
    if verifier["status"] == "passed" and any(item["status"] != "passed" for item in verifier["assertions"]):
        raise ValueError("passed verifier contains a non-passing assertion")

    metrics = document["metrics"]
    if not isinstance(metrics, dict):
        raise ValueError("metrics must be an object")
    _exact(metrics, METRIC_FIELDS, "metrics")
    for field, amount in metrics.items():
        if field == "estimatedCostUsd":
            _nullable_nonnegative_number(amount, f"metrics.{field}")
        else:
            _nullable_nonnegative_integer(amount, f"metrics.{field}")

    if not isinstance(document["artifacts"], list):
        raise ValueError("artifacts must be a list")
    for index, artifact in enumerate(document["artifacts"]):
        if not isinstance(artifact, dict):
            raise ValueError(f"artifacts[{index}] must be an object")
        _exact(artifact, {"ref", "kind", "digest", "valid"}, f"artifacts[{index}]")
        _nonempty(artifact["ref"], f"artifacts[{index}].ref")
        _nonempty(artifact["kind"], f"artifacts[{index}].kind")
        _digest(artifact["digest"], f"artifacts[{index}].digest")
        if artifact["valid"] is not None and not isinstance(artifact["valid"], bool):
            raise ValueError(f"artifacts[{index}].valid must be null or boolean")

    trace = document["trace"]
    if not isinstance(trace, dict):
        raise ValueError("trace must be an object")
    _exact(trace, {"digest", "eventCount", "ref"}, "trace")
    _digest(trace["digest"], "trace.digest", nullable=True)
    _nullable_nonnegative_integer(trace["eventCount"], "trace.eventCount")
    if trace["ref"] is not None:
        _nonempty(trace["ref"], "trace.ref")
    _string_list(document["failureRefs"], "failureRefs", unique=True)
    _string_list(document["limitations"], "limitations")
    _validate_integrity(document)


def validate_failure(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "failureId",
        "trialId",
        "failureClass",
        "failureCode",
        "firstObservableEvent",
        "responsibleBoundary",
        "recoverable",
        "recovered",
        "duplicateEffect",
        "humanIntervention",
        "description",
        "minimalCorrection",
        "correctionCost",
        "evidenceRefs",
        "integrity",
    }
    _exact(document, expected, "Failure Record")
    if document["schemaVersion"] != 1 or document["kind"] != "ordivon.evaluation-failure":
        raise ValueError("unsupported Failure Record identity")
    _nonempty(document["failureId"], "failureId")
    _nonempty(document["trialId"], "trialId")
    failure_class = document["failureClass"]
    if failure_class not in FAILURE_CODES:
        raise ValueError("unsupported failureClass")
    if document["failureCode"] not in FAILURE_CODES[failure_class]:
        raise ValueError("failureCode is not admitted by failureClass")

    event = document["firstObservableEvent"]
    if not isinstance(event, dict):
        raise ValueError("firstObservableEvent must be an object")
    _exact(event, {"sequence", "eventKind", "evidenceRef"}, "firstObservableEvent")
    if event["sequence"] is not None and (
        isinstance(event["sequence"], bool) or not isinstance(event["sequence"], int) or event["sequence"] < 1
    ):
        raise ValueError("firstObservableEvent.sequence must be null or positive")
    _nonempty(event["eventKind"], "firstObservableEvent.eventKind")
    _nonempty(event["evidenceRef"], "firstObservableEvent.evidenceRef")

    if document["responsibleBoundary"] not in {
        "context",
        "model",
        "tool",
        "effect",
        "harness",
        "verifier",
        "environment",
        "host",
        "runtime",
        "provider",
        "operator",
    }:
        raise ValueError("unsupported responsibleBoundary")
    for field in ("recoverable", "recovered", "duplicateEffect", "humanIntervention"):
        if not isinstance(document[field], bool):
            raise ValueError(f"{field} must be boolean")
    if document["recovered"] and not document["recoverable"]:
        raise ValueError("a recovered failure must be recoverable")
    _nonempty(document["description"], "description")
    _nonempty(document["minimalCorrection"], "minimalCorrection")
    if document["correctionCost"] is not None:
        _nonempty(document["correctionCost"], "correctionCost")
    _string_list(document["evidenceRefs"], "evidenceRefs", minimum=1)
    _validate_integrity(document)


def validate_document(document: dict[str, Any]) -> None:
    kind = document.get("kind")
    if kind == "ordivon.evaluation-task":
        validate_task(document)
    elif kind == "ordivon.evaluation-trial":
        validate_trial(document)
    elif kind == "ordivon.evaluation-result":
        validate_result(document)
    elif kind == "ordivon.evaluation-failure":
        validate_failure(document)
    else:
        raise ValueError(f"unsupported evaluation record kind: {kind!r}")


def validate_collection(documents: Iterable[dict[str, Any]]) -> None:
    items = list(documents)
    for document in items:
        validate_document(document)

    tasks: dict[tuple[str, int], dict[str, Any]] = {}
    trials: dict[str, dict[str, Any]] = {}
    results: dict[str, dict[str, Any]] = {}
    failures: dict[str, dict[str, Any]] = {}

    for document in items:
        kind = document["kind"]
        if kind == "ordivon.evaluation-task":
            identity = (document["taskId"], document["taskVersion"])
            if identity in tasks:
                raise ValueError(f"duplicate Task Definition: {identity}")
            tasks[identity] = document
        elif kind == "ordivon.evaluation-trial":
            identity = document["trialId"]
            if identity in trials:
                raise ValueError(f"duplicate Trial Manifest: {identity}")
            trials[identity] = document
        elif kind == "ordivon.evaluation-result":
            identity = document["trialId"]
            if identity in results:
                raise ValueError(f"duplicate Trial Result: {identity}")
            results[identity] = document
        elif kind == "ordivon.evaluation-failure":
            identity = document["failureId"]
            if identity in failures:
                raise ValueError(f"duplicate Failure Record: {identity}")
            failures[identity] = document

    for trial_id, trial in trials.items():
        task_identity = _validate_task_ref(trial["taskRef"])
        if tasks and task_identity not in tasks:
            raise ValueError(f"Trial references missing Task Definition: {trial_id} -> {task_identity}")

    for trial_id, result in results.items():
        trial = trials.get(trial_id)
        if trial is None:
            raise ValueError(f"Trial Result references missing Trial Manifest: {trial_id}")
        if result["taskRef"] != trial["taskRef"]:
            raise ValueError(f"Trial Result taskRef differs from Trial Manifest: {trial_id}")
        missing_failures = sorted(set(result["failureRefs"]) - set(failures))
        if missing_failures:
            raise ValueError(f"Trial Result references missing Failure Records: {trial_id} -> {missing_failures}")

    for failure_id, failure in failures.items():
        if failure["trialId"] not in trials:
            raise ValueError(f"Failure Record references missing Trial Manifest: {failure_id}")


def discover(paths: Iterable[Path]) -> list[Path]:
    discovered: list[Path] = []
    for path in paths:
        if path.is_dir():
            discovered.extend(sorted(path.rglob("*.json")))
        else:
            discovered.append(path)
    return sorted(set(discovered))


def load_documents(paths: Iterable[Path]) -> list[tuple[Path, dict[str, Any]]]:
    loaded: list[tuple[Path, dict[str, Any]]] = []
    for path in discover(paths):
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"{path} must contain one JSON object")
        if value.get("kind") not in KINDS:
            continue
        loaded.append((path, value))
    if not loaded:
        raise ValueError("no evaluation records found")
    return loaded


def write_digests(loaded: list[tuple[Path, dict[str, Any]]]) -> None:
    for path, document in loaded:
        document["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": "ordivon-canonical-json-v1",
            "payloadDigest": payload_digest(document),
        }
        path.write_text(
            json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--write-digests", action="store_true")
    args = parser.parse_args()

    loaded = load_documents(args.paths)
    if args.write_digests:
        write_digests(loaded)
        loaded = load_documents(args.paths)
    validate_collection(document for _, document in loaded)
    output = {
        "schemaVersion": 1,
        "kind": "ordivon.evaluation-validation-result",
        "ok": True,
        "records": len(loaded),
        "paths": [str(path) for path, _ in loaded],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
