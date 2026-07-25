from __future__ import annotations

from collections.abc import Callable

from .identity import IdKind, SemanticId
from .kernel import InvalidTransition, SemanticKernel
from .model import (
    Admission,
    Artifact,
    CapabilityRef,
    Claim,
    CompletionSemantics,
    EffectMode,
    EffectSpec,
    EvidenceKind,
    EvidenceRef,
    Fact,
    IdempotencyKind,
    Observation,
    Verification,
    VerificationDecision,
    VerificationPlan,
    WorldObjectRef,
)
from .state import EffectState, NextAction, next_action


def sid(kind: IdKind, value: str) -> SemanticId:
    return SemanticId(kind, value)


def sample_effect(name: str = "sample") -> EffectSpec:
    principal = sid(IdKind.PRINCIPAL, "agent:reference")
    target = sid(IdKind.WORLD_OBJECT, f"repo:{name}")
    operation = "workspace.read"
    return EffectSpec(
        effect_id=sid(IdKind.EFFECT, f"effect:{name}"),
        target=WorldObjectRef(target, version="rev-1"),
        mode=EffectMode.OBSERVE,
        operation=operation,
        input_digest="sha256:input",
        capability=CapabilityRef(principal, operation, target),
        idempotency=IdempotencyKind.NATURAL,
        completion=CompletionSemantics.VERIFIED,
        verification=VerificationPlan(
            method="digest-and-version",
            required_evidence=(EvidenceKind.OBSERVATION, EvidenceKind.ARTIFACT),
        ),
    )


def run_core_conformance(factory: Callable[[], SemanticKernel]) -> None:
    _successful_verified_effect(factory())
    _unknown_requires_reconciliation(factory())
    _terminal_state_is_immutable(factory())


def _successful_verified_effect(kernel: SemanticKernel) -> None:
    spec = sample_effect("success")
    assert kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, "event:success:0"),
        recorded_at_ms=1,
    ) is Admission.CREATED
    assert kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, "event:success:duplicate-unused"),
        recorded_at_ms=1,
    ) is Admission.EXISTING
    record = kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, "event:success:1"),
        recorded_at_ms=2,
    )
    assert record.state is EffectState.PREPARED
    assert next_action(record.state) is NextAction.DISPATCH
    dispatch_id = sid(IdKind.DISPATCH, "dispatch:success")
    record = kernel.begin_dispatch(
        spec.effect_id,
        expected_revision=1,
        dispatch_id=dispatch_id,
        event_id=sid(IdKind.EVENT, "event:success:2"),
        recorded_at_ms=3,
        request_digest="sha256:dispatch-request",
    )
    assert record.state is EffectState.DISPATCHED
    assert kernel.get_dispatch(dispatch_id).effect_id == spec.effect_id
    observation = Observation(
        observation_id=sid(IdKind.OBSERVATION, "observation:success"),
        effect_id=spec.effect_id,
        dispatch_id=dispatch_id,
        target=spec.target,
        observed_at_ms=4,
        source="reference-adapter",
        payload_digest="sha256:payload",
    )
    assert kernel.record_observation(observation) is Admission.CREATED
    artifact = Artifact(
        artifact_id=sid(IdKind.ARTIFACT, "artifact:success"),
        effect_id=spec.effect_id,
        dispatch_id=dispatch_id,
        kind="execution_result",
        digest="sha256:artifact",
        media_type="application/json",
        byte_length=42,
        created_at_ms=4,
    )
    assert kernel.register_artifact(artifact) is Admission.CREATED
    record = kernel.advance_effect(
        spec.effect_id,
        EffectState.SUCCEEDED,
        expected_revision=2,
        event_id=sid(IdKind.EVENT, "event:success:3"),
        recorded_at_ms=5,
        evidence_digest="sha256:terminal-evidence",
    )
    assert record.state is EffectState.SUCCEEDED
    claim = Claim(
        claim_id=sid(IdKind.CLAIM, "claim:success"),
        origin_effect_id=spec.effect_id,
        subject=spec.target,
        predicate="content_digest_equals",
        value_digest="sha256:payload",
    )
    kernel.admit_claim(claim)
    verification = Verification(
        verification_id=sid(IdKind.VERIFICATION, "verification:success"),
        claim_id=claim.claim_id,
        method="digest-and-version",
        evidence=(
            EvidenceRef(EvidenceKind.OBSERVATION, observation.observation_id),
            EvidenceRef(EvidenceKind.ARTIFACT, artifact.artifact_id),
        ),
        decision=VerificationDecision.ACCEPTED,
        verified_at_ms=6,
    )
    kernel.record_verification(verification)
    fact = Fact(
        fact_id=sid(IdKind.FACT, "fact:success"),
        claim_id=claim.claim_id,
        verification_id=verification.verification_id,
        accepted_at_ms=7,
    )
    kernel.commit_fact(fact)
    kernel.validate_invariants()


def _unknown_requires_reconciliation(kernel: SemanticKernel) -> None:
    spec = sample_effect("unknown")
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, "event:unknown:0"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, "event:unknown:1"),
        recorded_at_ms=2,
    )
    kernel.begin_dispatch(
        spec.effect_id,
        expected_revision=1,
        dispatch_id=sid(IdKind.DISPATCH, "dispatch:unknown"),
        event_id=sid(IdKind.EVENT, "event:unknown:2"),
        recorded_at_ms=3,
        request_digest="sha256:dispatch-request",
    )
    record = kernel.advance_effect(
        spec.effect_id,
        EffectState.UNKNOWN,
        expected_revision=2,
        event_id=sid(IdKind.EVENT, "event:unknown:3"),
        recorded_at_ms=4,
        evidence_digest="sha256:response-lost",
    )
    assert record.state is EffectState.UNKNOWN
    assert next_action(record.state) is NextAction.RECONCILE
    try:
        kernel.begin_dispatch(
            spec.effect_id,
            expected_revision=3,
            dispatch_id=sid(IdKind.DISPATCH, "dispatch:unsafe-repeat"),
            event_id=sid(IdKind.EVENT, "event:unknown:unsafe"),
            recorded_at_ms=5,
            request_digest="sha256:repeat",
        )
    except InvalidTransition:
        pass
    else:
        raise AssertionError("unknown outcome was unsafely redispatched")
    kernel.advance_effect(
        spec.effect_id,
        EffectState.RECONCILING,
        expected_revision=3,
        event_id=sid(IdKind.EVENT, "event:unknown:4"),
        recorded_at_ms=6,
        evidence_digest="sha256:reconciliation-start",
    )
    kernel.advance_effect(
        spec.effect_id,
        EffectState.SUCCEEDED,
        expected_revision=4,
        event_id=sid(IdKind.EVENT, "event:unknown:5"),
        recorded_at_ms=7,
        evidence_digest="sha256:correlated-world-result",
    )
    kernel.validate_invariants()


def _terminal_state_is_immutable(kernel: SemanticKernel) -> None:
    spec = sample_effect("terminal")
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, "event:terminal:0"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, "event:terminal:1"),
        recorded_at_ms=2,
    )
    kernel.advance_effect(
        spec.effect_id,
        EffectState.CANCELLED,
        expected_revision=1,
        event_id=sid(IdKind.EVENT, "event:terminal:2"),
        recorded_at_ms=3,
        evidence_digest="sha256:cancelled-before-dispatch",
    )
    try:
        kernel.advance_effect(
            spec.effect_id,
            EffectState.SUCCEEDED,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:terminal:3"),
            recorded_at_ms=4,
            evidence_digest="sha256:contradiction",
        )
    except InvalidTransition:
        pass
    else:
        raise AssertionError("terminal effect accepted a contradictory outcome")
    kernel.validate_invariants()
