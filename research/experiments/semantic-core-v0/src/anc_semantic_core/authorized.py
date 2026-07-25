from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, replace
from typing import Any, Iterator

from .authority import (
    AttestationKind,
    AuthorityDenied,
    AuthorityPolicy,
    AuthorityRef,
    AuthorityRole,
    AuthoritySigner,
    semantic_digest,
)
from .identity import SemanticId
from .model import Admission, Artifact, Claim, EffectRecord, EffectSpec, Fact, Observation, Verification
from .state import EffectState


@dataclass(frozen=True, slots=True)
class AuthorityGrant:
    authority: AuthorityRef
    signer: AuthoritySigner

    def __post_init__(self) -> None:
        if self.signer.authority != self.authority:
            raise ValueError("authority grant signer does not match its authority")


class AuthorityRoot:
    """Trusted bootstrap that issues role-scoped Kernel views."""

    def __init__(self, kernel: Any, policy: AuthorityPolicy) -> None:
        if kernel.authority_policy_fingerprint != policy.fingerprint:
            raise AuthorityDenied("Kernel and AuthorityPolicy fingerprints differ")
        self._kernel = kernel
        self._policy = policy
        self._seal = object()

    def issue(
        self,
        *,
        authority_id: SemanticId,
        principal_id: SemanticId,
        role: AuthorityRole,
        trust_domain: str,
        contract_version: str,
    ) -> "AuthorizedKernel":
        authority = self._policy.issue(
            authority_id=authority_id,
            principal_id=principal_id,
            role=role,
            trust_domain=trust_domain,
        )
        return AuthorizedKernel._create(
            self._kernel,
            {role: AuthorityGrant(
                authority,
                self._policy.signer(authority, contract_version=contract_version),
            )},
            self._seal,
        )

    def combine(self, *views: "AuthorizedKernel") -> "AuthorizedKernel":
        grants: dict[AuthorityRole, AuthorityGrant] = {}
        for view in views:
            view._require_root(self._kernel, self._seal)
            for role, grant in view._grants.items():
                existing = grants.get(role)
                if existing is not None and existing != grant:
                    raise AuthorityDenied(f"conflicting authority grants for role {role.value}")
                grants[role] = grant
        return AuthorizedKernel._create(
            self._kernel,
            grants,
            self._seal,
        )

    def read_only(self) -> "AuthorizedKernel":
        return AuthorizedKernel._create(self._kernel, {}, self._seal)


class AuthorizedKernel:
    """Role-scoped facade that signs every semantic mutation before reduction."""

    def __init__(self, *_: Any, **__: Any) -> None:
        raise TypeError("AuthorizedKernel views are issued by AuthorityRoot")

    @classmethod
    def _create(
        cls,
        kernel: Any,
        grants: dict[AuthorityRole, AuthorityGrant],
        root_seal: object,
    ) -> "AuthorizedKernel":
        self = object.__new__(cls)
        self._kernel = kernel
        self._grants = dict(grants)
        self._root_seal = root_seal
        return self

    def _require_root(self, kernel: Any, seal: object) -> None:
        if self._kernel is not kernel or self._root_seal is not seal:
            raise AuthorityDenied("authority views belong to different roots")

    def authority_for(self, role: AuthorityRole) -> AuthorityRef:
        return self._grant(role).authority

    def require_same_root(self, other: "AuthorizedKernel") -> None:
        if not isinstance(other, AuthorizedKernel):
            raise AuthorityDenied("authority operation requires another AuthorizedKernel view")
        other._require_root(self._kernel, self._root_seal)

    def _grant(self, role: AuthorityRole) -> AuthorityGrant:
        grant = self._grants.get(role)
        if grant is None:
            raise AuthorityDenied(f"Kernel view has no {role.value} authority")
        if grant.authority.role is not role:
            raise AuthorityDenied("authority grant role does not match its Kernel slot")
        return grant

    def _attest(
        self,
        role: AuthorityRole,
        kind: AttestationKind,
        operation: str,
        issued_at_ms: int,
        *args: Any,
        **kwargs: Any,
    ):
        grant = self._grant(role)
        return grant.signer.attest(
            kind=kind,
            subject_digest=semantic_digest(operation, *args, **kwargs),
            issued_at_ms=issued_at_ms,
        )

    def admit_effect(
        self, spec: EffectSpec, *, event_id: SemanticId, recorded_at_ms: int
    ) -> Admission:
        attestation = self._attest(
            AuthorityRole.EFFECT,
            AttestationKind.EFFECT_PROPOSAL,
            "admit_effect",
            recorded_at_ms,
            spec,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
        )
        return self._kernel.admit_effect(
            spec,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            attestation=attestation,
        )

    def prepare_effect(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
    ) -> EffectRecord:
        attestation = self._attest(
            AuthorityRole.EFFECT,
            AttestationKind.EFFECT_PREPARATION,
            "prepare_effect",
            recorded_at_ms,
            effect_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
        )
        return self._kernel.prepare_effect(
            effect_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            attestation=attestation,
        )

    def begin_dispatch(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        dispatch_id: SemanticId,
        event_id: SemanticId,
        recorded_at_ms: int,
        request_digest: str,
    ) -> EffectRecord:
        attestation = self._attest(
            AuthorityRole.DISPATCH,
            AttestationKind.DISPATCH_INTENT,
            "begin_dispatch",
            recorded_at_ms,
            effect_id,
            expected_revision=expected_revision,
            dispatch_id=dispatch_id,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            request_digest=request_digest,
        )
        return self._kernel.begin_dispatch(
            effect_id,
            expected_revision=expected_revision,
            dispatch_id=dispatch_id,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            request_digest=request_digest,
            attestation=attestation,
        )

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
    ) -> EffectRecord:
        attestation = self._attest(
            AuthorityRole.DISPATCH,
            AttestationKind.BACKEND_ADMISSION,
            "admit_dispatch",
            recorded_at_ms,
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            backend_operation_id=backend_operation_id,
            evidence_digest=evidence_digest,
        )
        return self._kernel.admit_dispatch(
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            backend_operation_id=backend_operation_id,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

    def mark_dispatch_unknown(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str,
    ) -> EffectRecord:
        attestation = self._attest(
            AuthorityRole.DISPATCH,
            AttestationKind.OUTCOME_UNCERTAINTY,
            "mark_dispatch_unknown",
            recorded_at_ms,
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
        )
        return self._kernel.mark_dispatch_unknown(
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

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
    ) -> EffectRecord:
        attestation = self._attest(
            AuthorityRole.DISPATCH,
            AttestationKind.DISPATCH_REJECTION,
            "reject_dispatch",
            recorded_at_ms,
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            reason_code=reason_code,
            retryable=retryable,
            evidence_digest=evidence_digest,
        )
        return self._kernel.reject_dispatch(
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            reason_code=reason_code,
            retryable=retryable,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

    def advance_effect(
        self,
        effect_id: SemanticId,
        target: EffectState,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str | None = None,
    ) -> EffectRecord:
        attestation = self._attest(
            AuthorityRole.DISPATCH,
            AttestationKind.EFFECT_TRANSITION,
            "advance_effect",
            recorded_at_ms,
            effect_id,
            target,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
        )
        return self._kernel.advance_effect(
            effect_id,
            target,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

    def record_observation(self, observation: Observation) -> Admission:
        if observation.attestation is not None:
            raise AuthorityDenied("Observation attestation is assigned by the authority view")
        grant = self._grant(AuthorityRole.OBSERVATION)
        attestation = grant.signer.attest(
            kind=AttestationKind.OBSERVATION,
            subject_digest=semantic_digest("record_observation", observation),
            issued_at_ms=observation.observed_at_ms,
        )
        return self._kernel.record_observation(replace(observation, attestation=attestation))

    def register_artifact(self, artifact: Artifact) -> Admission:
        if artifact.attestation is not None:
            raise AuthorityDenied("Artifact attestation is assigned by the authority view")
        grant = self._grant(AuthorityRole.OBSERVATION)
        attestation = grant.signer.attest(
            kind=AttestationKind.ARTIFACT,
            subject_digest=semantic_digest("register_artifact", artifact),
            issued_at_ms=artifact.created_at_ms,
        )
        return self._kernel.register_artifact(replace(artifact, attestation=attestation))

    def admit_claim(self, claim: Claim, *, proposed_at_ms: int = 0) -> Admission:
        if claim.attestation is not None:
            raise AuthorityDenied("Claim attestation is assigned by the authority view")
        grant = self._grant(AuthorityRole.VERIFICATION)
        attestation = grant.signer.attest(
            kind=AttestationKind.CLAIM,
            subject_digest=semantic_digest(
                "admit_claim", claim, proposed_at_ms=proposed_at_ms
            ),
            issued_at_ms=proposed_at_ms,
        )
        return self._kernel.admit_claim(
            replace(claim, attestation=attestation), proposed_at_ms=proposed_at_ms
        )

    def record_verification(self, verification: Verification) -> Admission:
        if verification.attestation is not None:
            raise AuthorityDenied("Verification attestation is assigned by the authority view")
        grant = self._grant(AuthorityRole.VERIFICATION)
        attestation = grant.signer.attest(
            kind=AttestationKind.VERIFICATION,
            subject_digest=semantic_digest("record_verification", verification),
            issued_at_ms=verification.verified_at_ms,
        )
        return self._kernel.record_verification(
            replace(verification, attestation=attestation)
        )

    def commit_fact(self, fact: Fact) -> Admission:
        if fact.attestation is not None:
            raise AuthorityDenied("Fact attestation is assigned by the authority view")
        grant = self._grant(AuthorityRole.FACT)
        attestation = grant.signer.attest(
            kind=AttestationKind.FACT_ACCEPTANCE,
            subject_digest=semantic_digest("commit_fact", fact),
            issued_at_ms=fact.accepted_at_ms,
        )
        return self._kernel.commit_fact(replace(fact, attestation=attestation))

    def get_effect(self, effect_id: SemanticId):
        return self._kernel.get_effect(effect_id)

    def get_dispatch(self, dispatch_id: SemanticId):
        return self._kernel.get_dispatch(dispatch_id)

    def events_for(self, effect_id: SemanticId):
        return self._kernel.events_for(effect_id)

    def get_observation(self, observation_id: SemanticId):
        return self._kernel.get_observation(observation_id)

    def get_artifact(self, artifact_id: SemanticId):
        return self._kernel.get_artifact(artifact_id)

    def get_claim(self, claim_id: SemanticId):
        return self._kernel.get_claim(claim_id)

    def get_verification(self, verification_id: SemanticId):
        return self._kernel.get_verification(verification_id)

    def get_fact(self, fact_id: SemanticId):
        return self._kernel.get_fact(fact_id)

    def validate_invariants(self) -> None:
        self._kernel.validate_invariants()

    def state_snapshot(self):
        return self._kernel.state_snapshot()

    @property
    def journal_entry_count(self) -> int:
        return self._kernel.journal_entry_count

    @contextmanager
    def transaction(self) -> Iterator["AuthorizedKernel"]:
        with self._kernel.transaction():
            yield self

    def close(self) -> None:
        self._kernel.close()

    def __enter__(self) -> "AuthorizedKernel":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()
