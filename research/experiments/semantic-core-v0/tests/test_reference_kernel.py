from __future__ import annotations

import unittest
from dataclasses import replace

from anc_semantic_core.conformance import run_core_conformance, sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.kernel import (
    IdentityConflict,
    InvalidTransition,
    InvariantViolation,
    NotFound,
    ReferenceKernel,
    RevisionConflict,
)
from anc_semantic_core.model import (
    Admission,
    Claim,
    EvidenceKind,
    EvidenceRef,
    Fact,
    Observation,
    Verification,
    VerificationDecision,
)
from anc_semantic_core.state import EffectState


class ReferenceKernelTests(unittest.TestCase):
    def test_reference_kernel_passes_reusable_conformance(self) -> None:
        run_core_conformance(ReferenceKernel)

    def test_effect_identity_is_idempotent_but_not_ambiguous(self) -> None:
        kernel = ReferenceKernel()
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
        kernel = ReferenceKernel()
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

    def test_rejected_verification_cannot_become_fact(self) -> None:
        kernel = ReferenceKernel()
        spec = sample_effect("rejected-fact")
        dispatch = sid(IdKind.DISPATCH, "dispatch:rejected-fact")
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "event:rejected-fact:0"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:rejected-fact:1"),
            recorded_at_ms=2,
        )
        kernel.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=dispatch,
            event_id=sid(IdKind.EVENT, "event:rejected-fact:2"),
            recorded_at_ms=3,
            request_digest="sha256:dispatch",
        )
        kernel.admit_dispatch(
            spec.effect_id,
            dispatch,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:rejected-fact:3"),
            recorded_at_ms=4,
            backend_operation_id="backend-job:rejected-fact",
            evidence_digest="sha256:backend-admission",
        )
        observation = Observation(
            observation_id=sid(IdKind.OBSERVATION, "observation:rejected-fact"),
            effect_id=spec.effect_id,
            dispatch_id=dispatch,
            target=spec.target,
            observed_at_ms=5,
            source="reference-adapter",
            payload_digest="sha256:payload",
        )
        kernel.record_observation(observation)
        kernel.advance_effect(
            spec.effect_id,
            EffectState.SUCCEEDED,
            expected_revision=3,
            event_id=sid(IdKind.EVENT, "event:rejected-fact:4"),
            recorded_at_ms=6,
            evidence_digest="sha256:terminal",
        )
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "claim:rejected"),
            effect_id=spec.effect_id,
            subject=spec.target,
            predicate="content_digest_equals",
            value_digest="sha256:different",
        )
        kernel.admit_claim(claim)
        verification = Verification(
            verification_id=sid(IdKind.VERIFICATION, "verification:rejected"),
            claim_id=claim.claim_id,
            method="digest-and-version",
            evidence=(
                EvidenceRef(EvidenceKind.OBSERVATION, observation.observation_id),
            ),
            decision=VerificationDecision.REJECTED,
            verified_at_ms=7,
        )
        kernel.record_verification(verification)
        with self.assertRaises(InvariantViolation):
            kernel.commit_fact(
                Fact(
                    fact_id=sid(IdKind.FACT, "fact:rejected"),
                    claim_id=claim.claim_id,
                    verification_id=verification.verification_id,
                    accepted_at_ms=8,
                )
            )

    def test_admitted_unknown_dispatch_cannot_be_reclassified_rejected(self) -> None:
        kernel = ReferenceKernel()
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
        kernel = ReferenceKernel()
        fact = Fact(
            fact_id=sid(IdKind.FACT, "fact:missing"),
            claim_id=sid(IdKind.CLAIM, "claim:missing"),
            verification_id=sid(IdKind.VERIFICATION, "verification:missing"),
            accepted_at_ms=1,
        )
        with self.assertRaises(NotFound):
            kernel.commit_fact(fact)

    def test_observation_must_match_bound_dispatch(self) -> None:
        kernel = ReferenceKernel()
        spec = sample_effect("dispatch-binding")
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "event:dispatch-binding:0"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:dispatch-binding:1"),
            recorded_at_ms=2,
        )
        correct_dispatch = sid(IdKind.DISPATCH, "dispatch:correct")
        kernel.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=correct_dispatch,
            event_id=sid(IdKind.EVENT, "event:dispatch-binding:2"),
            recorded_at_ms=3,
            request_digest="sha256:dispatch",
        )
        kernel.admit_dispatch(
            spec.effect_id,
            correct_dispatch,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:dispatch-binding:3"),
            recorded_at_ms=4,
            backend_operation_id="backend-job:dispatch-binding",
            evidence_digest="sha256:backend-admission",
        )
        with self.assertRaises(InvariantViolation):
            kernel.record_observation(
                Observation(
                    observation_id=sid(
                        IdKind.OBSERVATION, "observation:wrong-dispatch"
                    ),
                    effect_id=spec.effect_id,
                    dispatch_id=sid(IdKind.DISPATCH, "dispatch:wrong"),
                    target=spec.target,
                    observed_at_ms=5,
                    source="reference-adapter",
                    payload_digest="sha256:payload",
                )
            )


if __name__ == "__main__":
    unittest.main()
