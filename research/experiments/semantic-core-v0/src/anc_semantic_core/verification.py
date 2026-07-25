from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .identity import IdKind, SemanticId
from .authorized import AuthorizedKernel
from .model import (
    Claim,
    EvidenceKind,
    EvidenceRef,
    Fact,
    Observation,
    Verification,
    VerificationDecision,
    WorldObjectRef,
)
from .state import EffectState


@dataclass(frozen=True, slots=True)
class DigestFactResult:
    claim: Claim
    verification: Verification
    fact: Fact | None


def verify_digest_fact(
    verification_kernel: AuthorizedKernel,
    fact_kernel: AuthorizedKernel,
    *,
    claim_effect_id: SemanticId,
    observation: Observation,
    expected_digest: str,
    verified_at_ms: int,
    accepted_at_ms: int | None = None,
) -> DigestFactResult:
    """Verify one Effect's digest claim using an independently produced Observation."""

    verification_kernel.require_same_root(fact_kernel)
    if not expected_digest.startswith("sha256:"):
        raise ValueError("expected digest must use sha256 identity")
    origin = verification_kernel.get_effect(claim_effect_id)
    if origin.state is not EffectState.SUCCEEDED:
        raise ValueError("claim origin Effect must be succeeded")
    if origin.spec.target.object_id != observation.target.object_id:
        raise ValueError("verification Observation targets a different world object")
    if observation.effect_id == claim_effect_id:
        raise ValueError("digest Fact requires an independent Observation Effect")
    token = hashlib.sha256(
        f"{claim_effect_id}|{observation.observation_id}|{expected_digest}".encode("utf-8")
    ).hexdigest()[:24]
    claim = Claim(
        claim_id=SemanticId(IdKind.CLAIM, f"digest:{token}"),
        origin_effect_id=claim_effect_id,
        subject=WorldObjectRef(origin.spec.target.object_id, version=expected_digest),
        predicate="content_digest_equals",
        value_digest=expected_digest,
    )
    with verification_kernel.transaction():
        verification_kernel.admit_claim(claim, proposed_at_ms=verified_at_ms)
        decision = (
            VerificationDecision.ACCEPTED
            if observation.target.version == expected_digest
            else VerificationDecision.REJECTED
        )
        verification = Verification(
            verification_id=SemanticId(IdKind.VERIFICATION, f"digest:{token}"),
            claim_id=claim.claim_id,
            method=origin.spec.verification.method,
            evidence=(
                EvidenceRef(
                    kind=EvidenceKind.OBSERVATION,
                    evidence_id=observation.observation_id,
                ),
            ),
            decision=decision,
            verified_at_ms=verified_at_ms,
        )
        verification_kernel.record_verification(verification)
        fact: Fact | None = None
        if decision is VerificationDecision.ACCEPTED:
            accepted = verified_at_ms if accepted_at_ms is None else accepted_at_ms
            fact = Fact(
                fact_id=SemanticId(IdKind.FACT, f"digest:{token}"),
                claim_id=claim.claim_id,
                verification_id=verification.verification_id,
                accepted_at_ms=accepted,
            )
            fact_kernel.commit_fact(fact)
        verification_kernel.validate_invariants()
        claim = verification_kernel.get_claim(claim.claim_id)
        verification = verification_kernel.get_verification(verification.verification_id)
        if fact is not None:
            fact = fact_kernel.get_fact(fact.fact_id)
    return DigestFactResult(claim=claim, verification=verification, fact=fact)
