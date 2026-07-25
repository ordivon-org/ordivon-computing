from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .identity import IdKind, SemanticId
from .state import EffectState


class EffectMode(StrEnum):
    OBSERVE = "observe"
    CHANGE = "change"


class IdempotencyKind(StrEnum):
    NONE = "none"
    NATURAL = "natural"
    KEYED = "keyed"


class CompletionSemantics(StrEnum):
    IMMEDIATE = "immediate"
    ACCEPTED = "accepted"
    ASYNCHRONOUS = "asynchronous"
    VERIFIED = "verified"


class EvidenceKind(StrEnum):
    OBSERVATION = "observation"
    ARTIFACT = "artifact"


class VerificationDecision(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class Admission(StrEnum):
    CREATED = "created"
    EXISTING = "existing"


class EventKind(StrEnum):
    EFFECT_ADMITTED = "effect_admitted"
    EFFECT_PREPARED = "effect_prepared"
    DISPATCH_STARTED = "dispatch_started"
    RUNNING_OBSERVED = "running_observed"
    CANCELLATION_REQUESTED = "cancellation_requested"
    OUTCOME_UNKNOWN = "outcome_unknown"
    RECONCILIATION_STARTED = "reconciliation_started"
    EFFECT_SUCCEEDED = "effect_succeeded"
    EFFECT_FAILED = "effect_failed"
    EFFECT_CANCELLED = "effect_cancelled"


@dataclass(frozen=True, slots=True)
class WorldObjectRef:
    object_id: SemanticId
    version: str | None = None

    def __post_init__(self) -> None:
        self.object_id.require(IdKind.WORLD_OBJECT)
        if self.version is not None and not self.version:
            raise ValueError("world object version must be non-empty when present")


@dataclass(frozen=True, slots=True)
class CapabilityRef:
    principal_id: SemanticId
    operation: str
    object_scope: SemanticId
    valid_until_ms: int | None = None

    def __post_init__(self) -> None:
        self.principal_id.require(IdKind.PRINCIPAL)
        self.object_scope.require(IdKind.WORLD_OBJECT)
        if not self.operation:
            raise ValueError("capability operation must not be empty")
        if self.valid_until_ms is not None and self.valid_until_ms < 0:
            raise ValueError("capability expiry must be non-negative")


@dataclass(frozen=True, slots=True)
class Precondition:
    object_ref: WorldObjectRef
    description: str

    def __post_init__(self) -> None:
        if not self.description:
            raise ValueError("precondition description must not be empty")


@dataclass(frozen=True, slots=True)
class VerificationPlan:
    method: str
    required_evidence: tuple[EvidenceKind, ...]

    def __post_init__(self) -> None:
        if not self.method:
            raise ValueError("verification method must not be empty")
        if not self.required_evidence:
            raise ValueError("verification plan must require evidence")
        if len(set(self.required_evidence)) != len(self.required_evidence):
            raise ValueError("verification evidence requirements must be unique")


@dataclass(frozen=True, slots=True)
class EffectSpec:
    effect_id: SemanticId
    target: WorldObjectRef
    mode: EffectMode
    operation: str
    input_digest: str
    capability: CapabilityRef
    idempotency: IdempotencyKind
    completion: CompletionSemantics
    verification: VerificationPlan
    preconditions: tuple[Precondition, ...] = ()
    parent_task_id: SemanticId | None = None
    parent_attempt_id: SemanticId | None = None
    idempotency_key: str | None = None

    def __post_init__(self) -> None:
        self.effect_id.require(IdKind.EFFECT)
        if self.parent_task_id is not None:
            self.parent_task_id.require(IdKind.TASK)
        if self.parent_attempt_id is not None:
            self.parent_attempt_id.require(IdKind.ATTEMPT)
        if not self.operation:
            raise ValueError("effect operation must not be empty")
        if not self.input_digest:
            raise ValueError("effect input digest must not be empty")
        if self.capability.operation != self.operation:
            raise ValueError("capability operation must match effect operation")
        if self.capability.object_scope != self.target.object_id:
            raise ValueError("capability scope must match effect target")
        if self.idempotency is IdempotencyKind.KEYED and not self.idempotency_key:
            raise ValueError("keyed idempotency requires idempotency_key")
        if self.idempotency is not IdempotencyKind.KEYED and self.idempotency_key is not None:
            raise ValueError("idempotency_key is only valid for keyed idempotency")


@dataclass(frozen=True, slots=True)
class EffectRecord:
    spec: EffectSpec
    state: EffectState
    revision: int
    dispatch_id: SemanticId | None = None

    def __post_init__(self) -> None:
        if self.revision < 0:
            raise ValueError("effect revision must be non-negative")
        if self.dispatch_id is not None:
            self.dispatch_id.require(IdKind.DISPATCH)


@dataclass(frozen=True, slots=True)
class DispatchRecord:
    dispatch_id: SemanticId
    effect_id: SemanticId
    request_digest: str
    started_at_ms: int

    def __post_init__(self) -> None:
        self.dispatch_id.require(IdKind.DISPATCH)
        self.effect_id.require(IdKind.EFFECT)
        if not self.request_digest:
            raise ValueError("dispatch request digest must not be empty")
        if self.started_at_ms < 0:
            raise ValueError("dispatch time must be non-negative")


@dataclass(frozen=True, slots=True)
class EffectEvent:
    event_id: SemanticId
    effect_id: SemanticId
    sequence: int
    kind: EventKind
    recorded_at_ms: int
    evidence_digest: str | None = None
    dispatch_id: SemanticId | None = None

    def __post_init__(self) -> None:
        self.event_id.require(IdKind.EVENT)
        self.effect_id.require(IdKind.EFFECT)
        if self.sequence < 0 or self.recorded_at_ms < 0:
            raise ValueError("event sequence and time must be non-negative")
        if self.dispatch_id is not None:
            self.dispatch_id.require(IdKind.DISPATCH)


@dataclass(frozen=True, slots=True)
class Observation:
    observation_id: SemanticId
    effect_id: SemanticId
    dispatch_id: SemanticId
    target: WorldObjectRef
    observed_at_ms: int
    source: str
    payload_digest: str

    def __post_init__(self) -> None:
        self.observation_id.require(IdKind.OBSERVATION)
        self.effect_id.require(IdKind.EFFECT)
        self.dispatch_id.require(IdKind.DISPATCH)
        if self.observed_at_ms < 0:
            raise ValueError("observation time must be non-negative")
        if not self.source or not self.payload_digest:
            raise ValueError("observation source and payload digest must not be empty")


@dataclass(frozen=True, slots=True)
class Artifact:
    artifact_id: SemanticId
    effect_id: SemanticId
    dispatch_id: SemanticId
    kind: str
    digest: str
    media_type: str
    byte_length: int
    created_at_ms: int

    def __post_init__(self) -> None:
        self.artifact_id.require(IdKind.ARTIFACT)
        self.effect_id.require(IdKind.EFFECT)
        self.dispatch_id.require(IdKind.DISPATCH)
        if not self.kind or not self.digest or not self.media_type:
            raise ValueError("artifact kind, digest, and media type must not be empty")
        if self.byte_length < 0 or self.created_at_ms < 0:
            raise ValueError("artifact byte length and time must be non-negative")


@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: SemanticId
    effect_id: SemanticId
    subject: WorldObjectRef
    predicate: str
    value_digest: str

    def __post_init__(self) -> None:
        self.claim_id.require(IdKind.CLAIM)
        self.effect_id.require(IdKind.EFFECT)
        if not self.predicate or not self.value_digest:
            raise ValueError("claim predicate and value digest must not be empty")


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    kind: EvidenceKind
    evidence_id: SemanticId

    def __post_init__(self) -> None:
        expected = {
            EvidenceKind.OBSERVATION: IdKind.OBSERVATION,
            EvidenceKind.ARTIFACT: IdKind.ARTIFACT,
        }[self.kind]
        self.evidence_id.require(expected)


@dataclass(frozen=True, slots=True)
class Verification:
    verification_id: SemanticId
    claim_id: SemanticId
    method: str
    evidence: tuple[EvidenceRef, ...]
    decision: VerificationDecision
    verified_at_ms: int

    def __post_init__(self) -> None:
        self.verification_id.require(IdKind.VERIFICATION)
        self.claim_id.require(IdKind.CLAIM)
        if not self.method:
            raise ValueError("verification method must not be empty")
        if not self.evidence:
            raise ValueError("verification must reference evidence")
        if self.verified_at_ms < 0:
            raise ValueError("verification time must be non-negative")
        if len(set(self.evidence)) != len(self.evidence):
            raise ValueError("verification evidence references must be unique")


@dataclass(frozen=True, slots=True)
class Fact:
    fact_id: SemanticId
    claim_id: SemanticId
    verification_id: SemanticId
    accepted_at_ms: int

    def __post_init__(self) -> None:
        self.fact_id.require(IdKind.FACT)
        self.claim_id.require(IdKind.CLAIM)
        self.verification_id.require(IdKind.VERIFICATION)
        if self.accepted_at_ms < 0:
            raise ValueError("fact acceptance time must be non-negative")
