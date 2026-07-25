from __future__ import annotations

from dataclasses import dataclass

from .authority import Attestation, AuthorityRef
from .errors import InvariantViolation
from .identity import SemanticId
from .interfaces import KernelReadView
from .model import (
    Artifact,
    Claim,
    DispatchRecord,
    EffectEvent,
    EffectRecord,
    EvidenceKind,
    EvidenceRef,
    Fact,
    Observation,
    Verification,
)
from .state import DispatchState, EffectState, NextAction, next_action


@dataclass(frozen=True, slots=True)
class ExecutionTraceView:
    effect: EffectRecord
    dispatch: DispatchRecord | None
    events: tuple[EffectEvent, ...]
    observations: tuple[Observation, ...]
    artifacts: tuple[Artifact, ...]
    next_action: NextAction


@dataclass(frozen=True, slots=True)
class RecoveryView:
    effect_id: SemanticId
    effect_state: EffectState
    revision: int
    dispatch_id: SemanticId | None
    dispatch_state: DispatchState | None
    backend_operation_id: str | None
    next_action: NextAction
    latest_evidence_digest: str | None


@dataclass(frozen=True, slots=True)
class EvidenceProvenance:
    reference: EvidenceRef
    evidence: Observation | Artifact
    producing_effect: EffectRecord
    producing_dispatch: DispatchRecord


@dataclass(frozen=True, slots=True)
class FactProvenanceView:
    fact: Fact
    verification: Verification
    claim: Claim
    origin_effect: EffectRecord
    evidence: tuple[EvidenceProvenance, ...]


@dataclass(frozen=True, slots=True)
class AuthorityTraceEntry:
    source_kind: str
    source_id: SemanticId
    authority: AuthorityRef
    attestation_kind: str
    contract_version: str
    subject_digest: str
    issued_at_ms: int


@dataclass(frozen=True, slots=True)
class AuthorityTraceView:
    subject_id: SemanticId
    entries: tuple[AuthorityTraceEntry, ...]


def execution_trace(kernel: KernelReadView, effect_id: SemanticId) -> ExecutionTraceView:
    effect = kernel.get_effect(effect_id)
    dispatch = (
        kernel.get_dispatch(effect.dispatch_id) if effect.dispatch_id is not None else None
    )
    return ExecutionTraceView(
        effect=effect,
        dispatch=dispatch,
        events=kernel.events_for(effect_id),
        observations=kernel.observations_for(effect_id),
        artifacts=kernel.artifacts_for(effect_id),
        next_action=next_action(effect.state),
    )


def recovery_view(kernel: KernelReadView, effect_id: SemanticId) -> RecoveryView:
    trace = execution_trace(kernel, effect_id)
    latest_evidence_digest = next(
        (
            event.evidence_digest
            for event in reversed(trace.events)
            if event.evidence_digest is not None
        ),
        None,
    )
    return RecoveryView(
        effect_id=trace.effect.spec.effect_id,
        effect_state=trace.effect.state,
        revision=trace.effect.revision,
        dispatch_id=trace.effect.dispatch_id,
        dispatch_state=trace.dispatch.state if trace.dispatch is not None else None,
        backend_operation_id=(
            trace.dispatch.backend_operation_id if trace.dispatch is not None else None
        ),
        next_action=trace.next_action,
        latest_evidence_digest=latest_evidence_digest,
    )


def fact_provenance(kernel: KernelReadView, fact_id: SemanticId) -> FactProvenanceView:
    fact = kernel.get_fact(fact_id)
    verification = kernel.get_verification(fact.verification_id)
    claim = kernel.get_claim(fact.claim_id)
    origin_effect = kernel.get_effect(claim.origin_effect_id)
    evidence = tuple(
        _evidence_provenance(kernel, reference) for reference in verification.evidence
    )
    return FactProvenanceView(
        fact=fact,
        verification=verification,
        claim=claim,
        origin_effect=origin_effect,
        evidence=evidence,
    )


def execution_authority_trace(
    kernel: KernelReadView, effect_id: SemanticId
) -> AuthorityTraceView:
    trace = execution_trace(kernel, effect_id)
    entries = [
        _authority_entry("event", event.event_id, event.attestation)
        for event in trace.events
    ]
    entries.extend(
        _authority_entry(
            "observation", observation.observation_id, observation.attestation
        )
        for observation in trace.observations
    )
    entries.extend(
        _authority_entry("artifact", artifact.artifact_id, artifact.attestation)
        for artifact in trace.artifacts
    )
    return AuthorityTraceView(subject_id=effect_id, entries=tuple(entries))


def fact_authority_trace(
    kernel: KernelReadView, fact_id: SemanticId
) -> AuthorityTraceView:
    provenance = fact_provenance(kernel, fact_id)
    entries = list(
        execution_authority_trace(
            kernel, provenance.origin_effect.spec.effect_id
        ).entries
    )
    entries.append(
        _authority_entry(
            "claim", provenance.claim.claim_id, provenance.claim.attestation
        )
    )
    for item in provenance.evidence:
        if isinstance(item.evidence, Observation):
            entries.append(
                _authority_entry(
                    "observation",
                    item.evidence.observation_id,
                    item.evidence.attestation,
                )
            )
        else:
            entries.append(
                _authority_entry(
                    "artifact", item.evidence.artifact_id, item.evidence.attestation
                )
            )
    entries.append(
        _authority_entry(
            "verification",
            provenance.verification.verification_id,
            provenance.verification.attestation,
        )
    )
    entries.append(
        _authority_entry("fact", provenance.fact.fact_id, provenance.fact.attestation)
    )
    return AuthorityTraceView(subject_id=fact_id, entries=tuple(entries))


def _evidence_provenance(
    kernel: KernelReadView, reference: EvidenceRef
) -> EvidenceProvenance:
    if reference.kind is EvidenceKind.OBSERVATION:
        evidence: Observation | Artifact = kernel.get_observation(reference.evidence_id)
        effect_id = evidence.effect_id
        dispatch_id = evidence.dispatch_id
    else:
        evidence = kernel.get_artifact(reference.evidence_id)
        effect_id = evidence.effect_id
        dispatch_id = evidence.dispatch_id
    return EvidenceProvenance(
        reference=reference,
        evidence=evidence,
        producing_effect=kernel.get_effect(effect_id),
        producing_dispatch=kernel.get_dispatch(dispatch_id),
    )


def _authority_entry(
    source_kind: str, source_id: SemanticId, attestation: Attestation | None
) -> AuthorityTraceEntry:
    if attestation is None:
        raise InvariantViolation(f"{source_kind} lacks authority attestation: {source_id}")
    return AuthorityTraceEntry(
        source_kind=source_kind,
        source_id=source_id,
        authority=attestation.authority,
        attestation_kind=attestation.kind.value,
        contract_version=attestation.contract_version,
        subject_digest=attestation.subject_digest,
        issued_at_ms=attestation.issued_at_ms,
    )
