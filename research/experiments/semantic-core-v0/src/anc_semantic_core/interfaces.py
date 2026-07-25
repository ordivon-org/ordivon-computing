from __future__ import annotations

from typing import Any, ContextManager, Protocol

from .identity import SemanticId
from .model import (
    Admission,
    Artifact,
    Claim,
    DispatchRecord,
    EffectEvent,
    EffectRecord,
    EffectSpec,
    Fact,
    Observation,
    Verification,
)
from .state import EffectState


class KernelReadView(Protocol):
    """Read-only projection surface shared by all role-scoped Kernel views."""

    def get_effect(self, effect_id: SemanticId) -> EffectRecord: ...

    def get_dispatch(self, dispatch_id: SemanticId) -> DispatchRecord: ...

    def events_for(self, effect_id: SemanticId) -> tuple[EffectEvent, ...]: ...

    def observations_for(self, effect_id: SemanticId) -> tuple[Observation, ...]: ...

    def artifacts_for(self, effect_id: SemanticId) -> tuple[Artifact, ...]: ...

    def get_observation(self, observation_id: SemanticId) -> Observation: ...

    def get_artifact(self, artifact_id: SemanticId) -> Artifact: ...

    def get_claim(self, claim_id: SemanticId) -> Claim: ...

    def get_verification(self, verification_id: SemanticId) -> Verification: ...

    def get_fact(self, fact_id: SemanticId) -> Fact: ...

    def validate_invariants(self) -> None: ...

    def state_snapshot(self) -> tuple[dict[Any, Any], ...]: ...

    @property
    def journal_entry_count(self) -> int: ...

    def close(self) -> None: ...


class RootBoundView(Protocol):
    """A view issued by one AuthorityRoot."""

    def require_same_root(self, other: RootBoundView) -> None: ...


class TransactionalView(Protocol):
    def transaction(self) -> ContextManager[Any]: ...


class EffectView(KernelReadView, RootBoundView, TransactionalView, Protocol):
    def admit_effect(
        self, spec: EffectSpec, *, event_id: SemanticId, recorded_at_ms: int
    ) -> Admission: ...

    def prepare_effect(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
    ) -> EffectRecord: ...


class ExecutionView(KernelReadView, RootBoundView, TransactionalView, Protocol):
    def begin_dispatch(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        dispatch_id: SemanticId,
        event_id: SemanticId,
        recorded_at_ms: int,
        request_digest: str,
    ) -> EffectRecord: ...

    def admit_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        backend_operation_id: str,
        evidence_digest: str,
    ) -> EffectRecord: ...

    def mark_dispatch_unknown(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str,
    ) -> EffectRecord: ...

    def reject_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        reason_code: str,
        retryable: bool,
        evidence_digest: str,
    ) -> EffectRecord: ...

    def advance_effect(
        self,
        effect_id: SemanticId,
        target: EffectState,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str | None = None,
    ) -> EffectRecord: ...

    def record_observation(self, observation: Observation) -> Admission: ...

    def register_artifact(self, artifact: Artifact) -> Admission: ...


class VerificationView(KernelReadView, RootBoundView, TransactionalView, Protocol):
    def admit_claim(self, claim: Claim, *, proposed_at_ms: int = 0) -> Admission: ...

    def record_verification(self, verification: Verification) -> Admission: ...


class FactView(KernelReadView, RootBoundView, TransactionalView, Protocol):
    def commit_fact(self, fact: Fact) -> Admission: ...


class SemanticKernel(EffectView, ExecutionView, VerificationView, FactView, Protocol):
    """Compatibility aggregate for tests that intentionally exercise all public roles."""
