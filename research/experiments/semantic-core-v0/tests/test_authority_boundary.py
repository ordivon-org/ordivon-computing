from __future__ import annotations

import secrets
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from anc_semantic_core.authority import (
    AttestationError,
    AttestationKind,
    AuthorityDenied,
    AuthorityPolicy,
    AuthorityRole,
    semantic_digest,
)
from anc_semantic_core.authorized import AuthorityRoot, AuthorizedKernel
from anc_semantic_core.bootstrap import authorized_reference_views
from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.journal import (
    JournalCorruption,
    JournalReducer,
    JournalSchemaError,
)
from anc_semantic_core.kernel import NotFound, ReferenceReducer
from anc_semantic_core.model import (
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
from anc_semantic_core.testing import (
    authorize_reducer,
    reference_kernel,
    test_authority_policy,
)


def issue_view(
    reducer,
    policy: AuthorityPolicy,
    role: AuthorityRole,
    *,
    namespace: str,
) -> AuthorizedKernel:
    return AuthorityRoot(reducer, policy).issue(
        authority_id=SemanticId(IdKind.AUTHORITY, f"{namespace}:{role.value}"),
        principal_id=SemanticId(IdKind.PRINCIPAL, f"{namespace}:{role.value}"),
        role=role,
        trust_domain=f"trust:{namespace}:{role.value}",
        contract_version=f"{role.value}-contract-v1",
    )


def admitted_effect(kernel: AuthorizedKernel, name: str):
    spec = sample_effect(name)
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"{name}:admit"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"{name}:prepare"),
        recorded_at_ms=2,
    )
    dispatch_id = sid(IdKind.DISPATCH, f"{name}:dispatch")
    kernel.begin_dispatch(
        spec.effect_id,
        expected_revision=1,
        dispatch_id=dispatch_id,
        event_id=sid(IdKind.EVENT, f"{name}:dispatch-start"),
        recorded_at_ms=3,
        request_digest=f"sha256:{name}:request",
    )
    kernel.admit_dispatch(
        spec.effect_id,
        dispatch_id,
        expected_revision=2,
        event_id=sid(IdKind.EVENT, f"{name}:dispatch-admitted"),
        recorded_at_ms=4,
        backend_operation_id=f"backend:{name}",
        evidence_digest=f"sha256:{name}:admission",
    )
    return spec, dispatch_id


class AuthorityBoundaryTests(unittest.TestCase):
    def test_public_bootstrap_returns_only_scoped_authority_views(self) -> None:
        views = authorized_reference_views(
            secrets.token_bytes(32), namespace="public-scoped"
        )
        self.assertFalse(hasattr(views, "full"))
        self.assertIsNotNone(views.effects.authority_for(AuthorityRole.EFFECT))
        self.assertIsNotNone(
            views.execution.authority_for(AuthorityRole.DISPATCH)
        )
        self.assertIsNotNone(
            views.execution.authority_for(AuthorityRole.OBSERVATION)
        )
        with self.assertRaises(AuthorityDenied):
            views.read.authority_for(AuthorityRole.EFFECT)

    def test_authorized_kernel_can_only_be_issued_by_authority_root(self) -> None:
        with self.assertRaises(TypeError):
            AuthorizedKernel()

    def test_effect_role_cannot_cross_dispatch_boundary(self) -> None:
        policy = test_authority_policy()
        reducer = ReferenceReducer(policy)
        effect_view = issue_view(reducer, policy, AuthorityRole.EFFECT, namespace="effect-only")
        spec = sample_effect("effect-only")
        effect_view.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "effect-only:admit"),
            recorded_at_ms=1,
        )
        effect_view.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "effect-only:prepare"),
            recorded_at_ms=2,
        )
        with self.assertRaises(AuthorityDenied):
            effect_view.begin_dispatch(
                spec.effect_id,
                expected_revision=1,
                dispatch_id=sid(IdKind.DISPATCH, "effect-only:dispatch"),
                event_id=sid(IdKind.EVENT, "effect-only:started"),
                recorded_at_ms=3,
                request_digest="sha256:effect-only-request",
            )
        self.assertIs(reducer.get_effect(spec.effect_id).state, EffectState.PREPARED)

    def test_role_specific_signer_cannot_escalate_to_another_role(self) -> None:
        policy = test_authority_policy()
        reducer = ReferenceReducer(policy)
        effect_view = issue_view(reducer, policy, AuthorityRole.EFFECT, namespace="no-escalation")
        spec = sample_effect("no-escalation")
        effect_view.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "no-escalation:admit"),
            recorded_at_ms=1,
        )
        effect_view.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "no-escalation:prepare"),
            recorded_at_ms=2,
        )
        self.assertFalse(hasattr(effect_view, "_policy"))
        dispatch_id = sid(IdKind.DISPATCH, "no-escalation:dispatch")
        event_id = sid(IdKind.EVENT, "no-escalation:started")
        forged = effect_view._grants[AuthorityRole.EFFECT].signer.attest(
            kind=AttestationKind.DISPATCH_INTENT,
            subject_digest=semantic_digest(
                "begin_dispatch",
                spec.effect_id,
                expected_revision=1,
                dispatch_id=dispatch_id,
                event_id=event_id,
                recorded_at_ms=3,
                request_digest="sha256:no-escalation",
            ),
            issued_at_ms=3,
        )
        with self.assertRaises(AuthorityDenied):
            reducer.begin_dispatch(
                spec.effect_id,
                expected_revision=1,
                dispatch_id=dispatch_id,
                event_id=event_id,
                recorded_at_ms=3,
                request_digest="sha256:no-escalation",
                attestation=forged,
            )
        self.assertIs(reducer.get_effect(spec.effect_id).state, EffectState.PREPARED)

    def test_dispatch_role_cannot_attest_observation(self) -> None:
        policy = test_authority_policy()
        reducer = ReferenceReducer(policy)
        effect_view = issue_view(reducer, policy, AuthorityRole.EFFECT, namespace="dispatch-split")
        dispatch_view = issue_view(
            reducer, policy, AuthorityRole.DISPATCH, namespace="dispatch-split"
        )
        kernel = AuthorityRoot(reducer, policy).read_only()
        # Views from separate roots cannot be combined; use the deterministic helper for setup.
        combined = authorize_reducer(
            reducer,
            policy,
            roles=(AuthorityRole.EFFECT, AuthorityRole.DISPATCH),
            namespace="dispatch-setup",
        )
        spec, dispatch_id = admitted_effect(combined, "dispatch-no-observation")
        observation = Observation(
            observation_id=sid(IdKind.OBSERVATION, "dispatch-no-observation:observation"),
            effect_id=spec.effect_id,
            dispatch_id=dispatch_id,
            target=spec.target,
            observed_at_ms=5,
            source="test",
            payload_digest="sha256:payload",
        )
        with self.assertRaises(AuthorityDenied):
            dispatch_view.record_observation(observation)
        with self.assertRaises(NotFound):
            kernel.get_observation(observation.observation_id)
        self.assertIsNotNone(effect_view.authority_for(AuthorityRole.EFFECT))

    def test_views_from_different_roots_cannot_be_combined(self) -> None:
        policy = test_authority_policy()
        reducer = ReferenceReducer(policy)
        first_root = AuthorityRoot(reducer, policy)
        second_root = AuthorityRoot(reducer, policy)
        effect = first_root.issue(
            authority_id=sid(IdKind.AUTHORITY, "cross-root:effect"),
            principal_id=sid(IdKind.PRINCIPAL, "cross-root:effect"),
            role=AuthorityRole.EFFECT,
            trust_domain="cross-root",
            contract_version="effect-v1",
        )
        dispatch = second_root.issue(
            authority_id=sid(IdKind.AUTHORITY, "cross-root:dispatch"),
            principal_id=sid(IdKind.PRINCIPAL, "cross-root:dispatch"),
            role=AuthorityRole.DISPATCH,
            trust_domain="cross-root",
            contract_version="dispatch-v1",
        )
        with self.assertRaises(AuthorityDenied):
            first_root.combine(effect, dispatch)

    def test_forged_authority_signature_is_rejected(self) -> None:
        policy = test_authority_policy()
        authority = policy.issue(
            authority_id=sid(IdKind.AUTHORITY, "forged:authority"),
            principal_id=sid(IdKind.PRINCIPAL, "forged:principal"),
            role=AuthorityRole.EFFECT,
            trust_domain="forged",
        )
        forged = replace(authority, principal_id=sid(IdKind.PRINCIPAL, "attacker"))
        with self.assertRaises(AttestationError):
            policy.verify_authority(forged, expected_role=AuthorityRole.EFFECT)

    def test_attestation_is_bound_to_exact_observation_content(self) -> None:
        kernel = reference_kernel(namespace="content-binding")
        spec, dispatch_id = admitted_effect(kernel, "content-binding")
        observation = Observation(
            observation_id=sid(IdKind.OBSERVATION, "content-binding:observation"),
            effect_id=spec.effect_id,
            dispatch_id=dispatch_id,
            target=spec.target,
            observed_at_ms=5,
            source="trusted-adapter",
            payload_digest="sha256:original",
        )
        kernel.record_observation(observation)
        stored = kernel.get_observation(observation.observation_id)
        self.assertIsNotNone(stored.attestation)
        tampered = replace(stored, payload_digest="sha256:tampered")
        with self.assertRaises(AttestationError):
            kernel._kernel.record_observation(tampered)
        kernel._kernel._observations[stored.observation_id] = tampered
        with self.assertRaises(AttestationError):
            kernel.validate_invariants()

    def test_caller_supplied_observation_attestation_is_rejected(self) -> None:
        kernel = reference_kernel(namespace="caller-attestation")
        spec, dispatch_id = admitted_effect(kernel, "caller-attestation")
        legitimate = Observation(
            observation_id=sid(IdKind.OBSERVATION, "caller-attestation:legitimate"),
            effect_id=spec.effect_id,
            dispatch_id=dispatch_id,
            target=spec.target,
            observed_at_ms=5,
            source="trusted-adapter",
            payload_digest="sha256:payload",
        )
        kernel.record_observation(legitimate)
        signed = kernel.get_observation(legitimate.observation_id)
        forged_record = replace(
            legitimate,
            observation_id=sid(IdKind.OBSERVATION, "caller-attestation:forged"),
            attestation=signed.attestation,
        )
        with self.assertRaises(AuthorityDenied):
            kernel.record_observation(forged_record)

    def test_attestation_provenance_survives_journal_replay(self) -> None:
        policy = test_authority_policy()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "authority.sqlite3"
            first = authorize_reducer(
                JournalReducer(path, policy),
                policy,
                namespace="journal-authority",
            )
            spec, dispatch_id = admitted_effect(first, "journal-authority")
            observation = Observation(
                observation_id=sid(IdKind.OBSERVATION, "journal-authority:observation"),
                effect_id=spec.effect_id,
                dispatch_id=dispatch_id,
                target=spec.target,
                observed_at_ms=5,
                source="ordivon:mcp/test",
                payload_digest="sha256:journal-payload",
            )
            first.record_observation(observation)
            stored_before = first.get_observation(observation.observation_id)
            first.close()

            reopened = authorize_reducer(
                JournalReducer(path, policy),
                policy,
                namespace="journal-authority",
            )
            stored_after = reopened.get_observation(observation.observation_id)
            self.assertEqual(stored_after.attestation, stored_before.attestation)
            self.assertEqual(
                stored_after.attestation.authority.role,
                AuthorityRole.OBSERVATION,
            )
            self.assertEqual(
                stored_after.attestation.contract_version,
                "observation-contract-v1",
            )
            reopened.validate_invariants()
            reopened.close()

    def test_wrong_secret_cannot_replay_signed_journal(self) -> None:
        policy = test_authority_policy()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong-secret.sqlite3"
            first = authorize_reducer(
                JournalReducer(path, policy), policy, namespace="wrong-secret"
            )
            spec = sample_effect("wrong-secret")
            first.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "wrong-secret:admit"),
                recorded_at_ms=1,
            )
            first.close()
            wrong = AuthorityPolicy(
                issuer_id=policy.issuer_id,
                policy_version=policy.policy_version,
                key_id=policy.key_id,
                secret=b"a-different-authority-secret-material-which-is-long-enough",
            )
            with self.assertRaises(JournalCorruption):
                JournalReducer(path, wrong)

    def test_policy_fingerprint_change_is_rejected_before_replay(self) -> None:
        policy = test_authority_policy()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy-version.sqlite3"
            first = authorize_reducer(
                JournalReducer(path, policy), policy, namespace="policy-version"
            )
            spec = sample_effect("policy-version")
            first.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "policy-version:admit"),
                recorded_at_ms=1,
            )
            first.close()
            changed = AuthorityPolicy(
                issuer_id=policy.issuer_id,
                policy_version="authority-policy-v2",
                key_id=policy.key_id,
                secret=b"agent-native-computing-semantic-core-authority-v2-secret",
            )
            with self.assertRaises(JournalSchemaError):
                JournalReducer(path, changed)

    def test_fact_records_verification_and_acceptance_authorities(self) -> None:
        kernel = reference_kernel(namespace="fact-authority")
        spec, dispatch_id = admitted_effect(kernel, "fact-authority")
        observation = Observation(
            observation_id=sid(IdKind.OBSERVATION, "fact-authority:observation"),
            effect_id=spec.effect_id,
            dispatch_id=dispatch_id,
            target=spec.target,
            observed_at_ms=5,
            source="trusted-adapter",
            payload_digest="sha256:fact-payload",
        )
        kernel.record_observation(observation)
        kernel.advance_effect(
            spec.effect_id,
            EffectState.SUCCEEDED,
            expected_revision=3,
            event_id=sid(IdKind.EVENT, "fact-authority:succeeded"),
            recorded_at_ms=6,
            evidence_digest="sha256:fact-terminal",
        )
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "fact-authority:claim"),
            origin_effect_id=spec.effect_id,
            subject=spec.target,
            predicate="payload_digest_equals",
            value_digest="sha256:fact-payload",
        )
        kernel.admit_claim(claim, proposed_at_ms=7)
        verification = Verification(
            verification_id=sid(IdKind.VERIFICATION, "fact-authority:verification"),
            claim_id=claim.claim_id,
            method=spec.verification.method,
            evidence=(
                EvidenceRef(EvidenceKind.OBSERVATION, observation.observation_id),
            ),
            decision=VerificationDecision.ACCEPTED,
            verified_at_ms=8,
        )
        # The sample plan also requires an Artifact.
        artifact = Artifact(
            artifact_id=sid(IdKind.ARTIFACT, "fact-authority:artifact"),
            effect_id=spec.effect_id,
            dispatch_id=dispatch_id,
            kind="result",
            digest="sha256:artifact",
            media_type="application/json",
            byte_length=1,
            created_at_ms=5,
        )
        kernel.register_artifact(artifact)
        verification = replace(
            verification,
            evidence=verification.evidence
            + (EvidenceRef(EvidenceKind.ARTIFACT, artifact.artifact_id),),
        )
        kernel.record_verification(verification)
        fact = Fact(
            fact_id=sid(IdKind.FACT, "fact-authority:fact"),
            claim_id=claim.claim_id,
            verification_id=verification.verification_id,
            accepted_at_ms=9,
        )
        kernel.commit_fact(fact)
        stored_verification = kernel.get_verification(verification.verification_id)
        stored_fact = kernel.get_fact(fact.fact_id)
        self.assertEqual(
            stored_verification.attestation.authority.role,
            AuthorityRole.VERIFICATION,
        )
        self.assertEqual(stored_fact.attestation.authority.role, AuthorityRole.FACT)
        self.assertNotEqual(
            stored_verification.attestation.authority.authority_id,
            stored_fact.attestation.authority.authority_id,
        )
        kernel.validate_invariants()


if __name__ == "__main__":
    unittest.main()
