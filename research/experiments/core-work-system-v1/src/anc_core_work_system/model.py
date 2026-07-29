from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
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


def canonical_digest(value: JsonValue) -> str:
    return "sha256:" + sha256(canonical_bytes(value)).hexdigest()


def require_digest(value: str) -> str:
    if (
        len(value) != 71
        or not value.startswith("sha256:")
        or any(ch not in "0123456789abcdef" for ch in value[7:])
    ):
        raise ValueError("digest must be sha256:<64 lowercase hex>")
    return value


def require_identity(value: str, prefix: str) -> str:
    if (
        not value.startswith(prefix + ":")
        or value != value.strip()
        or len(value.encode("utf-8")) > 300
    ):
        raise ValueError(f"identity must start with {prefix}: and be bounded")
    return value


def require_revision(value: str) -> str:
    if len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError("revision must be a 40-character lowercase Git object id")
    return value


class Fault(StrEnum):
    NONE = "none"
    ATTEMPT_FAILURE = "attempt-failure"
    GOAL_CLARIFICATION = "goal-clarification"
    REPOSITORY_DRIFT = "repository-drift"
    TOOL_CONTRACT_DRIFT = "tool-contract-drift"
    RESPONSE_LOSS_AFTER_COMMIT = "response-loss-after-commit"
    HOST_RESTART = "host-restart"
    PROVIDER_REPLACEMENT = "provider-replacement"
    POISONED_SOURCE = "poisoned-source"
    REVOKED_DECISION = "revoked-decision"


class DecisionDisposition(StrEnum):
    RETAIN = "retain"
    SHRINK = "shrink"
    LOCALIZE = "localize"
    DEFER = "defer"
    DELETE = "delete"
    INCOMPLETE = "incomplete"


class TrialStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class ExperimentSpec:
    experiment_id: str
    work_package: str
    variant: str
    fixture_digest: str
    faults: tuple[Fault, ...]
    model_budget: int = 2
    tool_budget: int = 16
    wall_clock_ms: int = 120_000
    schema_version: int = 1

    def __post_init__(self) -> None:
        require_identity(self.experiment_id, "experiment")
        if self.work_package not in {"continuity", "context", "effect", "attention", "gauntlet"}:
            raise ValueError("unsupported work package")
        if not self.variant or self.variant != self.variant.strip():
            raise ValueError("variant is required")
        require_digest(self.fixture_digest)
        if len(self.faults) != len(set(self.faults)):
            raise ValueError("fault schedule contains duplicates")
        if self.model_budget < 0 or self.tool_budget < 0 or self.wall_clock_ms < 1:
            raise ValueError("experiment budgets are invalid")
        if self.schema_version != 1:
            raise ValueError("unsupported ExperimentSpec version")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": self.schema_version,
            "kind": "anc.core-work-system-experiment-spec",
            "experimentId": self.experiment_id,
            "workPackage": self.work_package,
            "variant": self.variant,
            "fixtureDigest": self.fixture_digest,
            "faults": [fault.value for fault in self.faults],
            "modelBudget": self.model_budget,
            "toolBudget": self.tool_budget,
            "wallClockMs": self.wall_clock_ms,
        }


@dataclass(frozen=True, slots=True)
class SourceRecord:
    source_ref: str
    revision: str
    digest: str
    trust_class: str
    claim_status: str
    invalidation_keys: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_identity(self.source_ref, "source")
        if not self.revision or self.revision != self.revision.strip():
            raise ValueError("source revision is required")
        require_digest(self.digest)
        if self.trust_class not in {"authoritative", "trusted", "untrusted", "adversarial"}:
            raise ValueError("unsupported source trust class")
        if self.claim_status not in {"fact", "claim", "instruction", "observation"}:
            raise ValueError("unsupported claim status")
        if len(self.invalidation_keys) != len(set(self.invalidation_keys)):
            raise ValueError("invalidation keys must be unique")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "sourceRef": self.source_ref,
            "revision": self.revision,
            "digest": self.digest,
            "trustClass": self.trust_class,
            "claimStatus": self.claim_status,
            "invalidationKeys": list(self.invalidation_keys),
        }


@dataclass(frozen=True, slots=True)
class PendingOperation:
    operation_id: str
    request_id: str
    backend_correlation: str
    state: str
    target_revision: str
    catalog_digest: str

    def __post_init__(self) -> None:
        require_identity(self.operation_id, "operation")
        require_identity(self.request_id, "request")
        if not self.backend_correlation or self.backend_correlation != self.backend_correlation.strip():
            raise ValueError("backend correlation is required")
        if self.state not in {"prepared", "running", "unknown", "succeeded", "failed"}:
            raise ValueError("unsupported operation state")
        require_revision(self.target_revision)
        require_digest(self.catalog_digest)

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "operationId": self.operation_id,
            "requestId": self.request_id,
            "backendCorrelation": self.backend_correlation,
            "state": self.state,
            "targetRevision": self.target_revision,
            "catalogDigest": self.catalog_digest,
        }


@dataclass(frozen=True, slots=True)
class WorkState:
    task_id: str
    goal_revision: int
    goal_statement: str
    repository_revision: str
    catalog_digest: str
    frontier: tuple[str, ...]
    completed_effects: tuple[str, ...] = ()
    pending_operations: tuple[PendingOperation, ...] = ()
    facts: tuple[str, ...] = ()
    sources: tuple[SourceRecord, ...] = ()
    pending_decision_id: str | None = None
    provider_id: str = "provider:scripted-a"
    revision: int = 1

    def __post_init__(self) -> None:
        require_identity(self.task_id, "task")
        if self.goal_revision < 1 or self.revision < 1:
            raise ValueError("state revisions must be positive")
        if not self.goal_statement or self.goal_statement != self.goal_statement.strip():
            raise ValueError("Goal statement is required")
        require_revision(self.repository_revision)
        require_digest(self.catalog_digest)
        if not self.frontier or len(self.frontier) != len(set(self.frontier)):
            raise ValueError("frontier must be non-empty and unique")
        for effect_id in self.completed_effects:
            require_identity(effect_id, "effect")
        for fact_id in self.facts:
            require_identity(fact_id, "fact")
        if len(self.completed_effects) != len(set(self.completed_effects)):
            raise ValueError("completed Effect identities must be unique")
        if len(self.facts) != len(set(self.facts)):
            raise ValueError("Fact identities must be unique")
        operation_ids = [item.operation_id for item in self.pending_operations]
        if len(operation_ids) != len(set(operation_ids)):
            raise ValueError("pending operation identities must be unique")
        source_refs = [item.source_ref for item in self.sources]
        if len(source_refs) != len(set(source_refs)):
            raise ValueError("source identities must be unique")
        if self.pending_decision_id is not None:
            require_identity(self.pending_decision_id, "decision-request")
        require_identity(self.provider_id, "provider")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": 1,
            "kind": "anc.core-work-state",
            "taskId": self.task_id,
            "goalRevision": self.goal_revision,
            "goalStatement": self.goal_statement,
            "repositoryRevision": self.repository_revision,
            "catalogDigest": self.catalog_digest,
            "frontier": list(self.frontier),
            "completedEffects": list(self.completed_effects),
            "pendingOperations": [item.to_dict() for item in self.pending_operations],
            "facts": list(self.facts),
            "sources": [item.to_dict() for item in self.sources],
            "pendingDecisionId": self.pending_decision_id,
            "providerId": self.provider_id,
            "revision": self.revision,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "WorkState":
        expected = {
            "schemaVersion", "kind", "taskId", "goalRevision", "goalStatement",
            "repositoryRevision", "catalogDigest", "frontier", "completedEffects",
            "pendingOperations", "facts", "sources", "pendingDecisionId", "providerId",
            "revision",
        }
        if set(value) != expected or value["schemaVersion"] != 1 or value["kind"] != "anc.core-work-state":
            raise ValueError("WorkState fields, version, or kind differ")
        pending = value["pendingOperations"]
        sources = value["sources"]
        if not isinstance(pending, list) or any(not isinstance(item, dict) for item in pending):
            raise ValueError("pending operations must be objects")
        if not isinstance(sources, list) or any(not isinstance(item, dict) for item in sources):
            raise ValueError("sources must be objects")
        return cls(
            task_id=str(value["taskId"]),
            goal_revision=int(value["goalRevision"]),
            goal_statement=str(value["goalStatement"]),
            repository_revision=str(value["repositoryRevision"]),
            catalog_digest=str(value["catalogDigest"]),
            frontier=tuple(str(item) for item in value["frontier"]),
            completed_effects=tuple(str(item) for item in value["completedEffects"]),
            pending_operations=tuple(
                PendingOperation(
                    operation_id=str(item["operationId"]),
                    request_id=str(item["requestId"]),
                    backend_correlation=str(item["backendCorrelation"]),
                    state=str(item["state"]),
                    target_revision=str(item["targetRevision"]),
                    catalog_digest=str(item["catalogDigest"]),
                ) for item in pending
            ),
            facts=tuple(str(item) for item in value["facts"]),
            sources=tuple(
                SourceRecord(
                    source_ref=str(item["sourceRef"]),
                    revision=str(item["revision"]),
                    digest=str(item["digest"]),
                    trust_class=str(item["trustClass"]),
                    claim_status=str(item["claimStatus"]),
                    invalidation_keys=tuple(str(key) for key in item["invalidationKeys"]),
                ) for item in sources
            ),
            pending_decision_id=None if value["pendingDecisionId"] is None else str(value["pendingDecisionId"]),
            provider_id=str(value["providerId"]),
            revision=int(value["revision"]),
        )


@dataclass(frozen=True, slots=True)
class WorldManifest:
    fixture_id: str
    fixture_digest: str
    initial_revision: str
    concurrent_revision: str
    catalog_v1_digest: str
    catalog_v2_digest: str
    authoritative_files: tuple[str, ...]
    untrusted_files: tuple[str, ...]
    schema_version: int = 1

    def __post_init__(self) -> None:
        require_identity(self.fixture_id, "fixture")
        for digest in (self.fixture_digest, self.catalog_v1_digest, self.catalog_v2_digest):
            require_digest(digest)
        require_revision(self.initial_revision)
        require_revision(self.concurrent_revision)
        if not self.authoritative_files:
            raise ValueError("fixture requires authoritative files")
        if set(self.authoritative_files) & set(self.untrusted_files):
            raise ValueError("authoritative and untrusted files overlap")
        if self.schema_version != 1:
            raise ValueError("unsupported WorldManifest version")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": self.schema_version,
            "kind": "anc.core-work-system-world-manifest",
            "fixtureId": self.fixture_id,
            "fixtureDigest": self.fixture_digest,
            "initialRevision": self.initial_revision,
            "concurrentRevision": self.concurrent_revision,
            "catalogV1Digest": self.catalog_v1_digest,
            "catalogV2Digest": self.catalog_v2_digest,
            "authoritativeFiles": list(self.authoritative_files),
            "untrustedFiles": list(self.untrusted_files),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "WorldManifest":
        return cls(
            fixture_id=str(value["fixtureId"]),
            fixture_digest=str(value["fixtureDigest"]),
            initial_revision=str(value["initialRevision"]),
            concurrent_revision=str(value["concurrentRevision"]),
            catalog_v1_digest=str(value["catalogV1Digest"]),
            catalog_v2_digest=str(value["catalogV2Digest"]),
            authoritative_files=tuple(str(item) for item in value["authoritativeFiles"]),
            untrusted_files=tuple(str(item) for item in value["untrustedFiles"]),
            schema_version=int(value["schemaVersion"]),
        )


@dataclass(frozen=True, slots=True)
class TrialRecord:
    spec: ExperimentSpec
    status: TrialStatus
    world_manifest_digest: str
    initial_state_digest: str
    final_state_digest: str | None
    accepted_outcome: bool
    hard_failures: tuple[str, ...]
    observations: dict[str, JsonValue]
    costs: dict[str, JsonValue]
    disposition: DecisionDisposition = DecisionDisposition.INCOMPLETE
    schema_version: int = 1

    def __post_init__(self) -> None:
        for digest in (self.world_manifest_digest, self.initial_state_digest):
            require_digest(digest)
        if self.final_state_digest is not None:
            require_digest(self.final_state_digest)
        if self.status is TrialStatus.PASSED and self.hard_failures:
            raise ValueError("passed Trial cannot retain hard failures")
        if self.accepted_outcome and self.status is not TrialStatus.PASSED:
            raise ValueError("accepted outcome requires passed Trial")
        if self.schema_version != 1:
            raise ValueError("unsupported TrialRecord version")

    def to_dict(self) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "schemaVersion": self.schema_version,
            "kind": "anc.core-work-system-trial-record",
            "spec": self.spec.to_dict(),
            "status": self.status.value,
            "worldManifestDigest": self.world_manifest_digest,
            "initialStateDigest": self.initial_state_digest,
            "finalStateDigest": self.final_state_digest,
            "acceptedOutcome": self.accepted_outcome,
            "hardFailures": list(self.hard_failures),
            "observations": self.observations,
            "costs": self.costs,
            "disposition": self.disposition.value,
        }
        payload["recordDigest"] = canonical_digest(payload)
        return payload
