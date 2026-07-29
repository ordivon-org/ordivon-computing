from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from anc_canonical import (
    JsonValue,
    canonical_bytes,
    canonical_digest,
    validate_digest,
    validate_json_value,
)


class WorkloadValidationError(ValueError):
    pass


class WorkloadAdmissionError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


_CONTEXT_KIND = "ordivon.compiled-context-envelope"
_CONTEXT_PAYLOAD_KIND = "ordivon.compiled-context"
_ALLOWED_CANDIDATE_KINDS = {
    "domain-action",
    "propose-effect",
    "observe-dispatch",
    "request-human",
    "wait",
    "finish",
}
_ALLOWED_OBSERVATION_STATES = {
    "accepted",
    "running",
    "succeeded",
    "failed",
    "rejected",
    "unknown",
}
_ALLOWED_OUTCOME_STATES = {"completed", "failed", "cancelled", "blocked"}


def _fail(message: str) -> None:
    raise WorkloadValidationError(message)


def _exact(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        _fail(f"{label} fields differ: {sorted(set(value) ^ expected)}")


def _string(value: Any, label: str, *, prefix: str | None = None) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        _fail(f"{label} must be a non-empty trimmed string")
    if prefix is not None and not value.startswith(prefix + ":"):
        _fail(f"{label} must start with {prefix}:")
    if len(value.encode("utf-8")) > 512:
        _fail(f"{label} exceeds 512 UTF-8 bytes")
    return value


def _nullable_string(value: Any, label: str, *, prefix: str | None = None) -> str | None:
    if value is None:
        return None
    return _string(value, label, prefix=prefix)


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        _fail(f"{label} must be an integer >= {minimum}")
    return value


def _digest(value: Any, label: str) -> str:
    if not isinstance(value, str):
        _fail(f"{label} must be a digest string")
    try:
        return validate_digest(value)
    except ValueError as error:
        raise WorkloadValidationError(f"{label} is invalid") from error


def _string_list(value: Any, label: str, *, prefix: str | None = None) -> list[str]:
    if not isinstance(value, list):
        _fail(f"{label} must be a list")
    result = [_string(item, f"{label} item", prefix=prefix) for item in value]
    if len(result) != len(set(result)):
        _fail(f"{label} entries must be unique")
    return result


def _state_ref(value: Any) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        _fail("StateRef must be an object")
    _exact(value, {"ref", "digest"}, "StateRef")
    _string(value["ref"], "StateRef ref")
    _digest(value["digest"], "StateRef digest")
    return value


def _state_refs(value: Any, label: str) -> list[dict[str, JsonValue]]:
    if not isinstance(value, list):
        _fail(f"{label} must be a list")
    result = [_state_ref(item) for item in value]
    refs = [item["ref"] for item in result]
    if len(refs) != len(set(refs)):
        _fail(f"{label} refs must be unique")
    return result


def _artifact_ref(value: Any) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        _fail("ArtifactRef must be an object")
    _exact(value, {"ref", "kind", "digest"}, "ArtifactRef")
    _string(value["ref"], "ArtifactRef ref")
    _string(value["kind"], "ArtifactRef kind")
    _digest(value["digest"], "ArtifactRef digest")
    return value


def _artifact_refs(value: Any, label: str) -> list[dict[str, JsonValue]]:
    if not isinstance(value, list):
        _fail(f"{label} must be a list")
    result = [_artifact_ref(item) for item in value]
    refs = [item["ref"] for item in result]
    if len(refs) != len(set(refs)):
        _fail(f"{label} refs must be unique")
    return result


def validate_task_descriptor(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "taskId",
            "goalId",
            "workloadId",
            "assigneeRef",
            "providerPolicyRef",
            "domainRef",
            "configurationDigests",
        },
        "TaskDescriptor",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.host-task-descriptor":
        _fail("TaskDescriptor version or kind is invalid")
    _string(value["taskId"], "TaskDescriptor taskId", prefix="task")
    _string(value["goalId"], "TaskDescriptor goalId", prefix="goal")
    _string(value["workloadId"], "TaskDescriptor workloadId")
    _nullable_string(value["assigneeRef"], "TaskDescriptor assigneeRef")
    _nullable_string(value["providerPolicyRef"], "TaskDescriptor providerPolicyRef")
    _nullable_string(value["domainRef"], "TaskDescriptor domainRef")
    digests = _string_list(value["configurationDigests"], "configurationDigests")
    for digest in digests:
        _digest(digest, "configurationDigests item")
    return value


def validate_context_block(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "blockId",
            "kind",
            "priority",
            "required",
            "freshness",
            "sourceRef",
            "sourceOwner",
            "sourceDigest",
            "trust",
            "validityRefs",
            "payload",
        },
        "ContextBlock",
    )
    _string(value["blockId"], "ContextBlock blockId", prefix="context-block")
    _string(value["kind"], "ContextBlock kind")
    priority = _integer(value["priority"], "ContextBlock priority")
    if priority > 100:
        _fail("ContextBlock priority must be <= 100")
    if type(value["required"]) is not bool:
        _fail("ContextBlock required must be boolean")
    if value["freshness"] not in {"current", "checkpoint", "historical"}:
        _fail("ContextBlock freshness is invalid")
    _string(value["sourceRef"], "ContextBlock sourceRef")
    if value["sourceOwner"] not in {"host", "runtime", "domain", "provider", "human"}:
        _fail("ContextBlock sourceOwner is invalid")
    _digest(value["sourceDigest"], "ContextBlock sourceDigest")
    if value["trust"] not in {"authoritative", "verified", "reported", "inferred"}:
        _fail("ContextBlock trust is invalid")
    _state_refs(value["validityRefs"], "ContextBlock validityRefs")
    validate_json_value(value["payload"])
    return value


def validate_decision_candidate(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "candidateId",
            "kind",
            "summary",
            "proposalDigest",
            "effectId",
            "dispatchId",
            "requiredStateRefs",
        },
        "DecisionCandidate",
    )
    _string(value["candidateId"], "DecisionCandidate candidateId", prefix="candidate")
    kind = _string(value["kind"], "DecisionCandidate kind")
    if kind not in _ALLOWED_CANDIDATE_KINDS:
        _fail("DecisionCandidate kind is invalid")
    _string(value["summary"], "DecisionCandidate summary")
    proposal_digest = value["proposalDigest"]
    if proposal_digest is not None:
        _digest(proposal_digest, "DecisionCandidate proposalDigest")
    effect_id = _nullable_string(value["effectId"], "DecisionCandidate effectId", prefix="effect")
    dispatch_id = _nullable_string(
        value["dispatchId"], "DecisionCandidate dispatchId", prefix="dispatch"
    )
    _state_refs(value["requiredStateRefs"], "DecisionCandidate requiredStateRefs")
    if kind == "domain-action":
        if proposal_digest is None or effect_id is not None or dispatch_id is not None:
            _fail("domain-action requires proposalDigest only")
    elif kind == "propose-effect":
        if effect_id is None or dispatch_id is not None:
            _fail("propose-effect requires effectId and no dispatchId")
    elif kind == "observe-dispatch":
        if dispatch_id is None or effect_id is not None or proposal_digest is not None:
            _fail("observe-dispatch requires dispatchId only")
    elif any(item is not None for item in (proposal_digest, effect_id, dispatch_id)):
        _fail(f"{kind} cannot carry proposal, Effect, or Dispatch identities")
    return value


def validate_compiled_context(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {"schemaVersion", "kind", "digest", "byteLength", "manifest", "payload"},
        "CompiledContextEnvelope",
    )
    if value["schemaVersion"] != 1 or value["kind"] != _CONTEXT_KIND:
        _fail("CompiledContextEnvelope version or kind is invalid")
    _digest(value["digest"], "CompiledContextEnvelope digest")
    _integer(value["byteLength"], "CompiledContextEnvelope byteLength", minimum=1)
    manifest = value["manifest"]
    if not isinstance(manifest, dict):
        _fail("Context manifest must be an object")
    _exact(
        manifest,
        {"tokenBudget", "estimatedTokens", "selectedBlockIds", "omittedBlockIds"},
        "ContextManifest",
    )
    budget = _integer(manifest["tokenBudget"], "ContextManifest tokenBudget", minimum=1)
    estimate = _integer(
        manifest["estimatedTokens"], "ContextManifest estimatedTokens", minimum=1
    )
    if estimate > budget:
        _fail("ContextManifest estimatedTokens exceeds tokenBudget")
    selected = _string_list(
        manifest["selectedBlockIds"], "ContextManifest selectedBlockIds", prefix="context-block"
    )
    omitted = _string_list(
        manifest["omittedBlockIds"], "ContextManifest omittedBlockIds", prefix="context-block"
    )
    if set(selected) & set(omitted):
        _fail("ContextManifest selected and omitted blocks overlap")
    payload = value["payload"]
    if not isinstance(payload, dict):
        _fail("CompiledContext payload must be an object")
    _exact(
        payload,
        {
            "schemaVersion",
            "kind",
            "taskId",
            "workloadId",
            "stateRefs",
            "blocks",
            "candidates",
            "completedEffectIds",
            "unresolvedDispatchIds",
            "instruction",
        },
        "CompiledContext",
    )
    if payload["schemaVersion"] != 1 or payload["kind"] != _CONTEXT_PAYLOAD_KIND:
        _fail("CompiledContext version or kind is invalid")
    _string(payload["taskId"], "CompiledContext taskId", prefix="task")
    _string(payload["workloadId"], "CompiledContext workloadId")
    _state_refs(payload["stateRefs"], "CompiledContext stateRefs")
    if not isinstance(payload["blocks"], list):
        _fail("CompiledContext blocks must be a list")
    blocks = [validate_context_block(item) if isinstance(item, dict) else _fail("ContextBlock must be an object") for item in payload["blocks"]]
    block_ids = [item["blockId"] for item in blocks]
    if len(block_ids) != len(set(block_ids)):
        _fail("CompiledContext block identities must be unique")
    if block_ids != selected:
        _fail("CompiledContext selected blocks differ from manifest")
    if not isinstance(payload["candidates"], list) or not 1 <= len(payload["candidates"]) <= 16:
        _fail("CompiledContext requires between 1 and 16 candidates")
    candidates = [validate_decision_candidate(item) if isinstance(item, dict) else _fail("DecisionCandidate must be an object") for item in payload["candidates"]]
    candidate_ids = [item["candidateId"] for item in candidates]
    if len(candidate_ids) != len(set(candidate_ids)):
        _fail("CompiledContext candidate identities must be unique")
    _string_list(payload["completedEffectIds"], "completedEffectIds", prefix="effect")
    _string_list(payload["unresolvedDispatchIds"], "unresolvedDispatchIds", prefix="dispatch")
    _string(payload["instruction"], "CompiledContext instruction")
    expected_digest = canonical_digest(payload)
    expected_bytes = len(canonical_bytes(payload))
    if value["digest"] != expected_digest or value["byteLength"] != expected_bytes:
        _fail("CompiledContext digest or byteLength differs from payload")
    return value


def validate_model_invocation_intent(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "invocationId",
            "taskId",
            "contextDigest",
            "contextObjectDigest",
            "providerPolicyRef",
        },
        "ModelInvocationIntent",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.model-invocation-intent":
        _fail("ModelInvocationIntent version or kind is invalid")
    _string(value["invocationId"], "ModelInvocationIntent invocationId", prefix="invocation")
    _string(value["taskId"], "ModelInvocationIntent taskId", prefix="task")
    _digest(value["contextDigest"], "ModelInvocationIntent contextDigest")
    _digest(value["contextObjectDigest"], "ModelInvocationIntent contextObjectDigest")
    _string(value["providerPolicyRef"], "ModelInvocationIntent providerPolicyRef")
    return value


def validate_model_decision(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "invocationId",
            "contextDigest",
            "candidateId",
            "providerId",
            "confidencePermille",
            "rationale",
        },
        "ModelDecision",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.model-decision":
        _fail("ModelDecision version or kind is invalid")
    _string(value["invocationId"], "ModelDecision invocationId", prefix="invocation")
    _digest(value["contextDigest"], "ModelDecision contextDigest")
    _nullable_string(value["candidateId"], "ModelDecision candidateId", prefix="candidate")
    _string(value["providerId"], "ModelDecision providerId")
    confidence = _integer(value["confidencePermille"], "ModelDecision confidencePermille")
    if confidence > 1000:
        _fail("ModelDecision confidencePermille must be <= 1000")
    _string(value["rationale"], "ModelDecision rationale")
    return value


def validate_admitted_decision(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "contextDigest",
            "candidate",
            "providerId",
            "confidencePermille",
            "rationale",
        },
        "AdmittedDecision",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.admitted-decision":
        _fail("AdmittedDecision version or kind is invalid")
    _digest(value["contextDigest"], "AdmittedDecision contextDigest")
    if value["candidate"] is not None:
        if not isinstance(value["candidate"], dict):
            _fail("AdmittedDecision candidate must be an object or null")
        validate_decision_candidate(value["candidate"])
    _string(value["providerId"], "AdmittedDecision providerId")
    confidence = _integer(value["confidencePermille"], "AdmittedDecision confidencePermille")
    if confidence > 1000:
        _fail("AdmittedDecision confidencePermille must be <= 1000")
    _string(value["rationale"], "AdmittedDecision rationale")
    return value


def validate_dispatch_envelope(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "dispatchId",
            "effectId",
            "executorId",
            "requestDigest",
            "idempotencyKey",
            "requiredStateRefs",
            "expectedObservationKind",
        },
        "DispatchEnvelope",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.dispatch-envelope":
        _fail("DispatchEnvelope version or kind is invalid")
    _string(value["dispatchId"], "DispatchEnvelope dispatchId", prefix="dispatch")
    _string(value["effectId"], "DispatchEnvelope effectId", prefix="effect")
    _string(value["executorId"], "DispatchEnvelope executorId")
    _digest(value["requestDigest"], "DispatchEnvelope requestDigest")
    _string(value["idempotencyKey"], "DispatchEnvelope idempotencyKey")
    _state_refs(value["requiredStateRefs"], "DispatchEnvelope requiredStateRefs")
    _string(value["expectedObservationKind"], "DispatchEnvelope expectedObservationKind")
    return value


def validate_observation_envelope(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "dispatchId",
            "executorId",
            "status",
            "payloadDigest",
            "evidenceRefs",
        },
        "ObservationEnvelope",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.observation-envelope":
        _fail("ObservationEnvelope version or kind is invalid")
    _string(value["dispatchId"], "ObservationEnvelope dispatchId", prefix="dispatch")
    _string(value["executorId"], "ObservationEnvelope executorId")
    if value["status"] not in _ALLOWED_OBSERVATION_STATES:
        _fail("ObservationEnvelope status is invalid")
    _digest(value["payloadDigest"], "ObservationEnvelope payloadDigest")
    _artifact_refs(value["evidenceRefs"], "ObservationEnvelope evidenceRefs")
    return value


def validate_verification_receipt(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "dispatchId",
            "method",
            "accepted",
            "observationDigest",
            "resultItems",
        },
        "VerificationReceipt",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.verification-receipt":
        _fail("VerificationReceipt version or kind is invalid")
    _string(value["dispatchId"], "VerificationReceipt dispatchId", prefix="dispatch")
    _string(value["method"], "VerificationReceipt method")
    if type(value["accepted"]) is not bool:
        _fail("VerificationReceipt accepted must be boolean")
    _digest(value["observationDigest"], "VerificationReceipt observationDigest")
    if not isinstance(value["resultItems"], list):
        _fail("VerificationReceipt resultItems must be a list")
    subjects: list[str] = []
    for item in value["resultItems"]:
        if not isinstance(item, dict):
            _fail("Verification result item must be an object")
        _exact(
            item,
            {"subjectRef", "decisionDigest", "status", "reason", "evidenceDigest"},
            "VerificationResultItem",
        )
        subjects.append(_string(item["subjectRef"], "VerificationResultItem subjectRef"))
        _digest(item["decisionDigest"], "VerificationResultItem decisionDigest")
        if item["status"] not in {"succeeded", "failed", "rejected", "not-selected"}:
            _fail("VerificationResultItem status is invalid")
        _nullable_string(item["reason"], "VerificationResultItem reason")
        _digest(item["evidenceDigest"], "VerificationResultItem evidenceDigest")
    if len(subjects) != len(set(subjects)):
        _fail("VerificationReceipt result item subjects must be unique")
    return value


def validate_task_outcome(value: dict[str, Any]) -> dict[str, Any]:
    _exact(
        value,
        {
            "schemaVersion",
            "kind",
            "taskId",
            "goalId",
            "status",
            "verificationDigest",
            "artifactRefs",
        },
        "TaskOutcome",
    )
    if value["schemaVersion"] != 1 or value["kind"] != "ordivon.task-outcome":
        _fail("TaskOutcome version or kind is invalid")
    _string(value["taskId"], "TaskOutcome taskId", prefix="task")
    _string(value["goalId"], "TaskOutcome goalId", prefix="goal")
    if value["status"] not in _ALLOWED_OUTCOME_STATES:
        _fail("TaskOutcome status is invalid")
    if value["verificationDigest"] is not None:
        _digest(value["verificationDigest"], "TaskOutcome verificationDigest")
    _artifact_refs(value["artifactRefs"], "TaskOutcome artifactRefs")
    return value


_VALIDATORS = {
    "ordivon.host-task-descriptor": validate_task_descriptor,
    _CONTEXT_KIND: validate_compiled_context,
    "ordivon.model-invocation-intent": validate_model_invocation_intent,
    "ordivon.model-decision": validate_model_decision,
    "ordivon.admitted-decision": validate_admitted_decision,
    "ordivon.dispatch-envelope": validate_dispatch_envelope,
    "ordivon.observation-envelope": validate_observation_envelope,
    "ordivon.verification-receipt": validate_verification_receipt,
    "ordivon.task-outcome": validate_task_outcome,
}


def validate_host_workload_object(value: JsonValue) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("Host workload wire object must be an object")
    validate_json_value(value)
    kind = value.get("kind")
    if not isinstance(kind, str) or kind not in _VALIDATORS:
        _fail(f"unsupported Host workload object kind: {kind}")
    return _VALIDATORS[kind](value)


def _current_state_map(value: Mapping[str, str] | list[dict[str, JsonValue]]) -> dict[str, str]:
    if isinstance(value, Mapping):
        result = dict(value)
        for ref, digest in result.items():
            _string(ref, "current state ref")
            _digest(digest, "current state digest")
        return result
    return {str(item["ref"]): str(item["digest"]) for item in _state_refs(value, "currentStateRefs")}


def admit_model_decision(
    context: dict[str, Any],
    decision: dict[str, Any],
    *,
    current_state_refs: Mapping[str, str] | list[dict[str, JsonValue]],
    completed_effect_ids: tuple[str, ...] = (),
    unresolved_dispatch_ids: tuple[str, ...] = (),
) -> dict[str, JsonValue]:
    validate_compiled_context(context)
    validate_model_decision(decision)
    if decision["contextDigest"] != context["digest"]:
        raise WorkloadAdmissionError("wrong_context", "Decision targets another Context")
    current = _current_state_map(current_state_refs)
    payload = context["payload"]
    for state_ref in payload["stateRefs"]:
        if current.get(state_ref["ref"]) != state_ref["digest"]:
            raise WorkloadAdmissionError("stale_state", "Context state reference is stale")
    candidate_id = decision["candidateId"]
    candidates = payload["candidates"]
    candidate = None
    if candidate_id is not None:
        exact = [item for item in candidates if item["candidateId"] == candidate_id]
        if len(exact) != 1:
            raise WorkloadAdmissionError("invented_candidate", "Decision selected an unknown candidate")
        candidate = exact[0]
        for state_ref in candidate["requiredStateRefs"]:
            if current.get(state_ref["ref"]) != state_ref["digest"]:
                raise WorkloadAdmissionError("stale_state", "Candidate state reference is stale")
        completed = set(completed_effect_ids) | set(payload["completedEffectIds"])
        if candidate["effectId"] is not None and candidate["effectId"] in completed:
            raise WorkloadAdmissionError("completed_effect", "Decision repeats a completed Effect")
        unresolved = set(unresolved_dispatch_ids) | set(payload["unresolvedDispatchIds"])
        if candidate["kind"] == "observe-dispatch":
            if candidate["dispatchId"] not in unresolved:
                raise WorkloadAdmissionError(
                    "wrong_dispatch", "Decision observes another Dispatch"
                )
        elif unresolved and candidate["kind"] in {"domain-action", "propose-effect", "finish"}:
            raise WorkloadAdmissionError(
                "unresolved_dispatch", "Unresolved Dispatch forbids new progress"
            )
    admitted: dict[str, JsonValue] = {
        "schemaVersion": 1,
        "kind": "ordivon.admitted-decision",
        "contextDigest": context["digest"],
        "candidate": candidate,
        "providerId": decision["providerId"],
        "confidencePermille": decision["confidencePermille"],
        "rationale": decision["rationale"],
    }
    validate_admitted_decision(admitted)
    return admitted


__all__ = [
    "WorkloadAdmissionError",
    "WorkloadValidationError",
    "admit_model_decision",
    "validate_host_workload_object",
]
