from __future__ import annotations

import unittest
from anc_semantic_core.testing import reference_kernel
from dataclasses import replace
from typing import Any

from anc_semantic_core.conformance import run_core_conformance, sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.kernel import (
    IdentityConflict,
    InvalidTransition,
    InvariantViolation,
    NotFound,
    SemanticKernel,
    RevisionConflict,
)
from anc_semantic_core.model import (
    Admission,
    Artifact,
    Claim,
    EvidenceKind,
    EvidenceRef,
    Fact,
    Observation,
    Verification,
    VerificationDecision,
)
from anc_semantic_core.state import EffectState


def start_effect(
    kernel: SemanticKernel,
    name: str,
) -> tuple[Any, Any]:
    spec = sample_effect(name)
    dispatch = sid(IdKind.DISPATCH, f"dispatch:{name}")
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"event:{name}:0"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"event:{name}:1"),
        recorded_at_ms=2,
    )
    kernel.begin_dispatch(
        spec.effect_id,
        expected_revision=1,
        dispatch_id=dispatch,
        event_id=sid(IdKind.EVENT, f"event:{name}:2"),
        recorded_at_ms=3,
        request_digest=f"sha256:request:{name}",
    )
    kernel.admit_dispatch(
        spec.effect_id,
        dispatch,
        expected_revision=2,
        event_id=sid(IdKind.EVENT, f"event:{name}:admitted"),
        recorded_at_ms=3,
        backend_operation_id=f"backend:{name}",
        evidence_digest=f"sha256:admission:{name}",
    )
    return spec, dispatch


def add_evidence(
    kernel: SemanticKernel,
    spec: Any,
    dispatch: Any,
    name: str,
) -> tuple[Observation, Artifact]:
    observation = Observation(
        observation_id=sid(IdKind.OBSERVATION, f"observation:{name}"),
        effect_id=spec.effect_id,
        dispatch_id=dispatch,
        target=spec.target,
        observed_at_ms=4,
        source="test-adapter",
        payload_digest=f"sha256:payload:{name}",
    )
    artifact = Artifact(
        artifact_id=sid(IdKind.ARTIFACT, f"artifact:{name}"),
        effect_id=spec.effect_id,
        dispatch_id=dispatch,
        kind="execution_result",
        digest=f"sha256:artifact:{name}",
        media_type="application/json",
        byte_length=42,
        created_at_ms=4,
    )
    kernel.record_observation(observation)
    kernel.register_artifact(artifact)
    return observation, artifact


class SemanticKernelTests(unittest.TestCase):
    def test_reference_kernel_passes_reusable_conformance(self) -> None:
        run_core_conformance(reference_kernel)

    def test_effect_identity_is_idempotent_but_not_ambiguous(self) -> None:
        kernel = reference_kernel()
        spec = sample_effect("identity")
        self.assertIs(
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "event:identity:0"),
                recorded_at_ms=1,
            ),
            Admission.CREATED,
        )
        self.assertIs(
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "event:identity:ignored"),
                recorded_at_ms=1,
            ),
            Admission.EXISTING,
        )
        conflicting = replace(spec, input_digest="sha256:different")
        with self.assertRaises(IdentityConflict):
            kernel.admit_effect(
                conflicting,
                event_id=sid(IdKind.EVENT, "event:identity:conflict"),
                recorded_at_ms=2,
            )

    def test_revision_conflict_prevents_lost_update(self) -> None:
        kernel = reference_kernel()
        spec = sample_effect("revision")
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "event:revision:0"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:revision:1"),
            recorded_at_ms=2,
        )
        with self.assertRaises(RevisionConflict):
            kernel.prepare_effect(
                spec.effect_id,
                expected_revision=0,
                event_id=sid(IdKind.EVENT, "event:revision:stale"),
                recorded_at_ms=3,
            )

    def test_dispatch_is_a_separate_durable_semantic_object(self) -> None:
        kernel = reference_kernel()
        spec, dispatch_id = start_effect(kernel, "dispatch-record")
        dispatch = kernel.get_dispatch(dispatch_id)
        self.assertEqual(dispatch.effect_id, spec.effect_id)
        self.assertEqual(dispatch.request_digest, "sha256:request:dispatch-record")
        self.assertEqual(dispatch.started_at_ms, 3)
        kernel.validate_invariants()

    def test_effect_event_time_cannot_regress(self) -> None:
        kernel = reference_kernel()
        spec = sample_effect("time")
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "event:time:0"),
            recorded_at_ms=10,
        )
        with self.assertRaises(InvariantViolation):
            kernel.prepare_effect(
                spec.effect_id,
                expected_revision=0,
                event_id=sid(IdKind.EVENT, "event:time:1"),
                recorded_at_ms=9,
            )

    def test_rejected_verification_cannot_become_fact(self) -> None:
        kernel = reference_kernel()
        spec, dispatch = start_effect(kernel, "rejected-fact")
        observation, _ = add_evidence(kernel, spec, dispatch, "rejected-fact")
        kernel.advance_effect(
            spec.effect_id,
            EffectState.SUCCEEDED,
            expected_revision=3,
            event_id=sid(IdKind.EVENT, "event:rejected-fact:3"),
            recorded_at_ms=5,
            evidence_digest="sha256:terminal",
        )
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:rejected"),
            origin_effect_id=spec.effect_id,
            subject=spec.target,
            predicate="content_digest_equals",
            value_digest="sha256:different",
        )
        kernel.admit_claim(claim)
        verification = Verification(
            verification_id=sid(IdKind.VERIFICATION, "verification:rejected"),
            claim_id=claim.claim_id,
            method="digest-and-version",
            evidence=(EvidenceRef(EvidenceKind.OBSERVATION, observation.observation_id),),
            decision=VerificationDecision.REJECTED,
            verified_at_ms=6,
        )
        kernel.record_verification(verification)
        with self.assertRaises(InvariantViolation):
            kernel.commit_fact(
                Fact(
                    fact_id=sid(IdKind.FACT, "fact:rejected"),
                    claim_id=claim.claim_id,
                    verification_id=verification.verification_id,
                    accepted_at_ms=7,
                )
            )

    def test_accepted_verification_requires_the_effect_plan_evidence(self) -> None:
        kernel = reference_kernel()
        spec, dispatch = start_effect(kernel, "missing-evidence")
        observation, _ = add_evidence(kernel, spec, dispatch, "missing-evidence")
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:missing-evidence"),
            origin_effect_id=spec.effect_id,
            subject=spec.target,
            predicate="content_digest_equals",
            value_digest=observation.payload_digest,
        )
        kernel.admit_claim(claim)
        with self.assertRaises(InvariantViolation):
            kernel.record_verification(
                Verification(
                    verification_id=sid(
                        IdKind.VERIFICATION,
                        "verification:missing-evidence",
                    ),
                    claim_id=claim.claim_id,
                    method="digest-and-version",
                    evidence=(
                        EvidenceRef(
                            EvidenceKind.OBSERVATION,
                            observation.observation_id,
                        ),
                    ),
                    decision=VerificationDecision.ACCEPTED,
                    verified_at_ms=6,
                )
            )

    def test_verification_accepts_independent_same_subject_evidence(self) -> None:
        kernel = reference_kernel()
        origin, _ = start_effect(kernel, "origin")
        independent_base = sample_effect("independent")
        independent = replace(
            independent_base,
            target=origin.target,
            capability=replace(
                independent_base.capability,
                object_scope=origin.target.object_id,
            ),
        )
        independent_dispatch = sid(IdKind.DISPATCH, "dispatch:independent")
        kernel.admit_effect(
            independent,
            event_id=sid(IdKind.EVENT, "event:independent:0"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            independent.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:independent:1"),
            recorded_at_ms=2,
        )
        kernel.begin_dispatch(
            independent.effect_id,
            expected_revision=1,
            dispatch_id=independent_dispatch,
            event_id=sid(IdKind.EVENT, "event:independent:2"),
            recorded_at_ms=3,
            request_digest="sha256:request:independent",
        )
        kernel.admit_dispatch(
            independent.effect_id,
            independent_dispatch,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:independent:admitted"),
            recorded_at_ms=3,
            backend_operation_id="backend:independent",
            evidence_digest="sha256:admission:independent",
        )
        observation, artifact = add_evidence(
            kernel,
            independent,
            independent_dispatch,
            "independent",
        )
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:origin"),
            origin_effect_id=origin.effect_id,
            subject=origin.target,
            predicate="content_digest_equals",
            value_digest=observation.payload_digest,
        )
        kernel.admit_claim(claim)
        kernel.record_verification(
            Verification(
                verification_id=sid(
                    IdKind.VERIFICATION,
                    "verification:independent",
                ),
                claim_id=claim.claim_id,
                method="digest-and-version",
                evidence=(
                    EvidenceRef(
                        EvidenceKind.OBSERVATION,
                        observation.observation_id,
                    ),
                    EvidenceRef(EvidenceKind.ARTIFACT, artifact.artifact_id),
                ),
                decision=VerificationDecision.ACCEPTED,
                verified_at_ms=6,
            )
        )
        kernel.validate_invariants()

    def test_verification_rejects_evidence_for_wrong_version(self) -> None:
        kernel = reference_kernel()
        origin, _ = start_effect(kernel, "version-origin")
        independent_base = sample_effect("version-independent")
        wrong_version_target = replace(origin.target, version="rev-2")
        independent = replace(
            independent_base,
            target=wrong_version_target,
            capability=replace(
                independent_base.capability,
                object_scope=origin.target.object_id,
            ),
        )
        dispatch = sid(IdKind.DISPATCH, "dispatch:version-independent")
        kernel.admit_effect(
            independent,
            event_id=sid(IdKind.EVENT, "event:version-independent:0"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            independent.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:version-independent:1"),
            recorded_at_ms=2,
        )
        kernel.begin_dispatch(
            independent.effect_id,
            expected_revision=1,
            dispatch_id=dispatch,
            event_id=sid(IdKind.EVENT, "event:version-independent:2"),
            recorded_at_ms=3,
            request_digest="sha256:request:version-independent",
        )
        kernel.admit_dispatch(
            independent.effect_id,
            dispatch,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:version-independent:admitted"),
            recorded_at_ms=3,
            backend_operation_id="backend:version-independent",
            evidence_digest="sha256:admission:version-independent",
        )
        observation, artifact = add_evidence(
            kernel,
            independent,
            dispatch,
            "version-independent",
        )
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:version-origin"),
            origin_effect_id=origin.effect_id,
            subject=origin.target,
            predicate="content_digest_equals",
            value_digest=observation.payload_digest,
        )
        kernel.admit_claim(claim)
        with self.assertRaises(InvariantViolation):
            kernel.record_verification(
                Verification(
                    verification_id=sid(
                        IdKind.VERIFICATION,
                        "verification:wrong-version",
                    ),
                    claim_id=claim.claim_id,
                    method="digest-and-version",
                    evidence=(
                        EvidenceRef(
                            EvidenceKind.OBSERVATION,
                            observation.observation_id,
                        ),
                        EvidenceRef(EvidenceKind.ARTIFACT, artifact.artifact_id),
                    ),
                    decision=VerificationDecision.ACCEPTED,
                    verified_at_ms=6,
                )
            )

    def test_verification_rejects_evidence_for_different_subject(self) -> None:
        kernel = reference_kernel()
        first, _ = start_effect(kernel, "first")
        second, second_dispatch = start_effect(kernel, "second")
        observation, artifact = add_evidence(
            kernel,
            second,
            second_dispatch,
            "second",
        )
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:first"),
            origin_effect_id=first.effect_id,
            subject=first.target,
            predicate="content_digest_equals",
            value_digest="sha256:payload:first",
        )
        kernel.admit_claim(claim)
        with self.assertRaises(InvariantViolation):
            kernel.record_verification(
                Verification(
                    verification_id=sid(
                        IdKind.VERIFICATION,
                        "verification:wrong-subject",
                    ),
                    claim_id=claim.claim_id,
                    method="digest-and-version",
                    evidence=(
                        EvidenceRef(
                            EvidenceKind.OBSERVATION,
                            observation.observation_id,
                        ),
                        EvidenceRef(EvidenceKind.ARTIFACT, artifact.artifact_id),
                    ),
                    decision=VerificationDecision.ACCEPTED,
                    verified_at_ms=6,
                )
            )

    def test_verification_cannot_predate_cross_effect_evidence(self) -> None:
        kernel = reference_kernel()
        spec, dispatch = start_effect(kernel, "evidence-time")
        observation, artifact = add_evidence(
            kernel,
            spec,
            dispatch,
            "evidence-time",
        )
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:evidence-time"),
            origin_effect_id=spec.effect_id,
            subject=spec.target,
            predicate="content_digest_equals",
            value_digest=observation.payload_digest,
        )
        kernel.admit_claim(claim)
        with self.assertRaises(InvariantViolation):
            kernel.record_verification(
                Verification(
                    verification_id=sid(
                        IdKind.VERIFICATION,
                        "verification:evidence-time",
                    ),
                    claim_id=claim.claim_id,
                    method="digest-and-version",
                    evidence=(
                        EvidenceRef(
                            EvidenceKind.OBSERVATION,
                            observation.observation_id,
                        ),
                        EvidenceRef(EvidenceKind.ARTIFACT, artifact.artifact_id),
                    ),
                    decision=VerificationDecision.ACCEPTED,
                    verified_at_ms=3,
                )
            )

    def test_admitted_unknown_dispatch_cannot_be_reclassified_rejected(self) -> None:
        kernel = reference_kernel()
        spec = sample_effect("admitted-unknown")
        dispatch = sid(IdKind.DISPATCH, "dispatch:admitted-unknown")
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "event:admitted-unknown:0"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:admitted-unknown:1"),
            recorded_at_ms=2,
        )
        kernel.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=dispatch,
            event_id=sid(IdKind.EVENT, "event:admitted-unknown:2"),
            recorded_at_ms=3,
            request_digest="sha256:request",
        )
        kernel.admit_dispatch(
            spec.effect_id,
            dispatch,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:admitted-unknown:3"),
            recorded_at_ms=4,
            backend_operation_id="backend-job:admitted-unknown",
            evidence_digest="sha256:admitted",
        )
        kernel.mark_dispatch_unknown(
            spec.effect_id,
            dispatch,
            expected_revision=3,
            event_id=sid(IdKind.EVENT, "event:admitted-unknown:4"),
            recorded_at_ms=5,
            evidence_digest="sha256:ownership-lost",
        )
        with self.assertRaises(InvalidTransition):
            kernel.reject_dispatch(
                spec.effect_id,
                dispatch,
                expected_revision=4,
                event_id=sid(IdKind.EVENT, "event:admitted-unknown:5"),
                recorded_at_ms=6,
                reason_code="NOT_FOUND",
                retryable=True,
                evidence_digest="sha256:not-found",
            )
        kernel.validate_invariants()

    def test_fact_requires_existing_claim_and_verification(self) -> None:
        kernel = reference_kernel()
        fact = Fact(
            fact_id=sid(IdKind.FACT, "fact:missing"),
            claim_id=sid(IdKind.CLAIM, "claim:missing"),
            verification_id=sid(IdKind.VERIFICATION, "verification:missing"),
            accepted_at_ms=1,
        )
        with self.assertRaises(NotFound):
            kernel.commit_fact(fact)

    def test_fact_cannot_predate_accepted_verification(self) -> None:
        kernel = reference_kernel()
        spec, dispatch = start_effect(kernel, "fact-time")
        observation, artifact = add_evidence(kernel, spec, dispatch, "fact-time")
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:fact-time"),
            origin_effect_id=spec.effect_id,
            subject=spec.target,
            predicate="content_digest_equals",
            value_digest=observation.payload_digest,
        )
        kernel.admit_claim(claim)
        verification = Verification(
            verification_id=sid(IdKind.VERIFICATION, "verification:fact-time"),
            claim_id=claim.claim_id,
            method="digest-and-version",
            evidence=(
                EvidenceRef(EvidenceKind.OBSERVATION, observation.observation_id),
                EvidenceRef(EvidenceKind.ARTIFACT, artifact.artifact_id),
            ),
            decision=VerificationDecision.ACCEPTED,
            verified_at_ms=8,
        )
        kernel.record_verification(verification)
        with self.assertRaises(InvariantViolation):
            kernel.commit_fact(
                Fact(
                    fact_id=sid(IdKind.FACT, "fact:too-early"),
                    claim_id=claim.claim_id,
                    verification_id=verification.verification_id,
                    accepted_at_ms=7,
                )
            )

    def test_observation_must_match_bound_dispatch(self) -> None:
        kernel = reference_kernel()
        spec, _ = start_effect(kernel, "dispatch-binding")
        with self.assertRaises(InvariantViolation):
            kernel.record_observation(
                Observation(
                    observation_id=sid(
                        IdKind.OBSERVATION,
                        "observation:wrong-dispatch",
                    ),
                    effect_id=spec.effect_id,
                    dispatch_id=sid(IdKind.DISPATCH, "dispatch:wrong"),
                    target=spec.target,
                    observed_at_ms=4,
                    source="reference-adapter",
                    payload_digest="sha256:payload",
                )
            )


if __name__ == "__main__":
    unittest.main()
