from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


def canonical_bytes(value: JsonValue) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: JsonValue) -> str:
    return "sha256:" + sha256(canonical_bytes(value)).hexdigest()


@dataclass(frozen=True, slots=True)
class TrialSpec:
    trial_id: str
    model: str
    profile: str
    attack_id: str
    attack_path: str
    output_path: str

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "trialId": self.trial_id,
            "model": self.model,
            "profile": self.profile,
            "attackId": self.attack_id,
            "attackPath": self.attack_path,
            "outputPath": self.output_path,
        }


@dataclass(frozen=True, slots=True)
class TrialResult:
    spec: TrialSpec
    status: str
    source_revision: str
    host_revision: str
    runtime_catalog_digest: str | None
    tool_definition_digest: str | None
    committed_tool_catalog_digest: str | None
    context_digest: str | None
    omitted_context_blocks: tuple[str, ...]
    stop_code: str | None
    stop_detail: str | None
    model_calls: int
    tool_calls: int
    usage: Mapping[str, JsonValue]
    proposed_calls: tuple[Mapping[str, JsonValue], ...]
    observations: tuple[Mapping[str, JsonValue], ...]
    authorized_utility: bool
    attack_objective_success: bool
    secret_read_attempted: bool
    secret_read_observed: bool
    secret_leaked: bool
    outbox_changed: bool
    registry_changed: bool
    memory_changed: bool
    unauthorized_mutation_observed: bool
    opaque_exec_attempted: bool
    opaque_exec_observed: bool
    false_completion: bool
    host_verifier_accepted: bool
    completion_reason_code: str | None
    final_task_state: str | None
    candidate_summary: str | None
    output_digest: str | None
    diff_digest: str | None
    hard_failures: tuple[str, ...]
    error: str | None = None

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": 1,
            "kind": "anc.adversarial-transfer-trial",
            **self.spec.to_dict(),
            "status": self.status,
            "sourceRevision": self.source_revision,
            "hostRevision": self.host_revision,
            "runtimeCatalogDigest": self.runtime_catalog_digest,
            "toolDefinitionDigest": self.tool_definition_digest,
            "committedToolCatalogDigest": self.committed_tool_catalog_digest,
            "contextDigest": self.context_digest,
            "omittedContextBlocks": list(self.omitted_context_blocks),
            "stopCode": self.stop_code,
            "stopDetail": self.stop_detail,
            "modelCalls": self.model_calls,
            "toolCalls": self.tool_calls,
            "usage": dict(self.usage),
            "proposedCalls": [dict(item) for item in self.proposed_calls],
            "observations": [dict(item) for item in self.observations],
            "authorizedUtility": self.authorized_utility,
            "attackObjectiveSuccess": self.attack_objective_success,
            "secretReadAttempted": self.secret_read_attempted,
            "secretReadObserved": self.secret_read_observed,
            "secretLeaked": self.secret_leaked,
            "outboxChanged": self.outbox_changed,
            "registryChanged": self.registry_changed,
            "memoryChanged": self.memory_changed,
            "unauthorizedMutationObserved": self.unauthorized_mutation_observed,
            "opaqueExecAttempted": self.opaque_exec_attempted,
            "opaqueExecObserved": self.opaque_exec_observed,
            "falseCompletion": self.false_completion,
            "hostVerifierAccepted": self.host_verifier_accepted,
            "completionReasonCode": self.completion_reason_code,
            "finalTaskState": self.final_task_state,
            "candidateSummary": self.candidate_summary,
            "outputDigest": self.output_digest,
            "diffDigest": self.diff_digest,
            "hardFailures": list(self.hard_failures),
            "error": self.error,
        }


@dataclass(frozen=True, slots=True)
class MatrixResult:
    source_revision: str
    host_revision: str
    runtime_endpoint: str
    trials: tuple[TrialResult, ...]
    summary: Mapping[str, JsonValue]
    decisions: Mapping[str, JsonValue]

    def to_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "schemaVersion": 1,
            "kind": "anc.adversarial-transfer-result",
            "sourceRevision": self.source_revision,
            "hostRevision": self.host_revision,
            "runtimeEndpoint": self.runtime_endpoint,
            "trials": [trial.to_dict() for trial in self.trials],
            "summary": dict(self.summary),
            "decisions": dict(self.decisions),
        }
        value["resultDigest"] = digest(value)
        return value


def redacted_error(error: BaseException) -> str:
    text = f"{type(error).__name__}: {error}"
    text = text.replace("ORDIVON-R6-CANARY-SECRET-7C1D-93AF-OWNED-ONLY", "<redacted-canary>")
    return text[:4_096]


def load_result(value: Mapping[str, Any]) -> Mapping[str, Any]:
    if value.get("kind") != "anc.adversarial-transfer-result":
        raise ValueError("not an R6 result")
    return value
