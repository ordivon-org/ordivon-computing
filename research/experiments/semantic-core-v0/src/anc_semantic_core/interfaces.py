from __future__ import annotations

from typing import Any, ContextManager, Protocol

from .identity import SemanticId
from .model import (
    Admission,
    Artifact,
    BindingAdmission,
    Claim,
    DispatchRecord,
    EffectEvent,
    EffectRecord,
    KernelEffectProjection,
    Fact,
    Observation,
    Verification,
)
from .state import EffectState


class KernelReadView(Protocol):
    """Read-only projection surface shared by all role-scoped Kernel views."""

    def get_effect(self, effect_id: SemanticId) -> EffectRecord: ...

    def get_dispatch(self, dispatch_id: SemanticId) -> DispatchRecord: ...

    def get_binding(self, binding_id: SemanticId) -> BindingAdmission: ...

    def bindings_for(self, effect_id: SemanticId) -> tuple[BindingAdmission, ...]: ...

    def current_binding_for(self, effect_id: SemanticId) -> BindingAdmission | None: ...

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

    def verify_from_genesis(self) -> None: ...

    def close(self) -> None: ...


class RootBoundView(Protocol):
    """A view issued by one AuthorityRoot."""

    def require_same_root(self, other: RootBoundView) -> None: ...


class TransactionalView(Protocol):
    def transaction(self) -> ContextManager[Any]: ...


class EffectView(KernelReadView, RootBoundView, TransactionalView, Protocol):
    def admit_effect(
        self, spec: KernelEffectProjection, *, event_id: SemanticId, recorded_at_ms: int
    ) -> Admission: ...

    def prepare_effect(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
    ) -> EffectRecord: ...


class BindingView(KernelReadView, RootBoundView, TransactionalView, Protocol):
    def admit_binding(self, binding: BindingAdmission) -> Admission: ...


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
        binding_id: SemanticId | None = None,
        binding_digest: str | None = None,
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


class SemanticKernel(
    EffectView, BindingView, ExecutionView, VerificationView, FactView, Protocol
):
    """Compatibility aggregate for tests that intentionally exercise all public roles."""
