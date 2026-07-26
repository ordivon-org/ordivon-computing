from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum, StrEnum
from typing import Any

from .identity import IdKind, SemanticId


class AuthorityError(RuntimeError):
    pass


class AuthorityDenied(AuthorityError):
    pass


class AttestationError(AuthorityError):
    pass


class AuthorityRole(StrEnum):
    EFFECT = "effect"
    BINDING = "binding"
    DISPATCH = "dispatch"
    OBSERVATION = "observation"
    VERIFICATION = "verification"
    FACT = "fact"


class AttestationKind(StrEnum):
    EFFECT_PROPOSAL = "effect_proposal"
    EFFECT_PREPARATION = "effect_preparation"
    EFFECT_BINDING = "effect_binding"
    DISPATCH_INTENT = "dispatch_intent"
    BACKEND_ADMISSION = "backend_admission"
    OUTCOME_UNCERTAINTY = "outcome_uncertainty"
    DISPATCH_REJECTION = "dispatch_rejection"
    EFFECT_TRANSITION = "effect_transition"
    OBSERVATION = "observation"
    ARTIFACT = "artifact"
    CLAIM = "claim"
    VERIFICATION = "verification"
    FACT_ACCEPTANCE = "fact_acceptance"


@dataclass(frozen=True, slots=True)
class AuthorityRef:
    authority_id: SemanticId
    issuer_id: SemanticId
    principal_id: SemanticId
    role: AuthorityRole
    trust_domain: str
    policy_version: str
    key_id: str
    signature: str

    def __post_init__(self) -> None:
        self.authority_id.require(IdKind.AUTHORITY)
        self.issuer_id.require(IdKind.PRINCIPAL)
        self.principal_id.require(IdKind.PRINCIPAL)
        if not self.trust_domain or not self.policy_version or not self.key_id:
            raise ValueError("authority trust domain, policy version, and key id are required")
        if not self.signature.startswith("hmac-sha256:"):
            raise ValueError("authority signature must use hmac-sha256")


@dataclass(frozen=True, slots=True)
class Attestation:
    authority: AuthorityRef
    kind: AttestationKind
    contract_version: str
    subject_digest: str
    issued_at_ms: int
    signature: str

    def __post_init__(self) -> None:
        if not self.contract_version:
            raise ValueError("attestation contract version is required")
        if not self.subject_digest.startswith("sha256:"):
            raise ValueError("attestation subject digest must use sha256")
        if self.issued_at_ms < 0:
            raise ValueError("attestation time must be non-negative")
        if not self.signature.startswith("hmac-sha256:"):
            raise ValueError("attestation signature must use hmac-sha256")


class AuthoritySigner:
    """Signer scoped to one issued AuthorityRef and one contract version."""

    def __init__(
        self,
        *,
        authority: AuthorityRef,
        contract_version: str,
        key: bytes,
    ) -> None:
        if not contract_version:
            raise ValueError("authority signer contract version is required")
        self.authority = authority
        self.contract_version = contract_version
        self.__key = bytes(key)

    def attest(
        self,
        *,
        kind: AttestationKind,
        subject_digest: str,
        issued_at_ms: int,
    ) -> Attestation:
        unsigned = _attestation_unsigned(
            self.authority,
            kind=kind,
            contract_version=self.contract_version,
            subject_digest=subject_digest,
            issued_at_ms=issued_at_ms,
        )
        return Attestation(
            authority=self.authority,
            kind=kind,
            contract_version=self.contract_version,
            subject_digest=subject_digest,
            issued_at_ms=issued_at_ms,
            signature=_sign_with_key(self.__key, unsigned),
        )


class AuthorityPolicy:
    """One issuer-backed HMAC policy for role grants and semantic attestations."""

    def __init__(
        self,
        *,
        issuer_id: SemanticId,
        policy_version: str,
        key_id: str,
        secret: bytes,
    ) -> None:
        issuer_id.require(IdKind.PRINCIPAL)
        if not policy_version or not key_id:
            raise ValueError("authority policy version and key id are required")
        if len(secret) < 32:
            raise ValueError("authority secret must contain at least 32 bytes")
        self.issuer_id = issuer_id
        self.policy_version = policy_version
        self.key_id = key_id
        self._secret = bytes(secret)

    @property
    def fingerprint(self) -> str:
        material = f"{self.issuer_id}|{self.policy_version}|{self.key_id}".encode("utf-8")
        return "sha256:" + hashlib.sha256(material).hexdigest()

    def issue(
        self,
        *,
        authority_id: SemanticId,
        principal_id: SemanticId,
        role: AuthorityRole,
        trust_domain: str,
    ) -> AuthorityRef:
        authority_id.require(IdKind.AUTHORITY)
        principal_id.require(IdKind.PRINCIPAL)
        unsigned = {
            "authorityId": str(authority_id),
            "issuerId": str(self.issuer_id),
            "principalId": str(principal_id),
            "role": role.value,
            "trustDomain": trust_domain,
            "policyVersion": self.policy_version,
            "keyId": self.key_id,
        }
        return AuthorityRef(
            authority_id=authority_id,
            issuer_id=self.issuer_id,
            principal_id=principal_id,
            role=role,
            trust_domain=trust_domain,
            policy_version=self.policy_version,
            key_id=self.key_id,
            signature=self._sign(unsigned),
        )

    def signer(
        self, authority: AuthorityRef, *, contract_version: str
    ) -> AuthoritySigner:
        self.verify_authority(authority)
        return AuthoritySigner(
            authority=authority,
            contract_version=contract_version,
            key=self._attestation_key(authority),
        )

    def verify_authority(
        self,
        authority: AuthorityRef,
        *,
        expected_role: AuthorityRole | None = None,
    ) -> None:
        if authority.issuer_id != self.issuer_id:
            raise AuthorityDenied("authority issuer is not trusted by this policy")
        if authority.policy_version != self.policy_version or authority.key_id != self.key_id:
            raise AuthorityDenied("authority policy version or key id does not match")
        if expected_role is not None and authority.role is not expected_role:
            raise AuthorityDenied(
                f"authority role {authority.role.value} cannot perform {expected_role.value} work"
            )
        unsigned = {
            "authorityId": str(authority.authority_id),
            "issuerId": str(authority.issuer_id),
            "principalId": str(authority.principal_id),
            "role": authority.role.value,
            "trustDomain": authority.trust_domain,
            "policyVersion": authority.policy_version,
            "keyId": authority.key_id,
        }
        self._require_signature(unsigned, authority.signature, "authority grant")

    def verify_attestation(
        self,
        attestation: Attestation,
        *,
        expected_role: AuthorityRole,
        expected_kind: AttestationKind,
        expected_subject_digest: str,
        expected_issued_at_ms: int,
    ) -> None:
        self.verify_authority(attestation.authority, expected_role=expected_role)
        if attestation.kind is not expected_kind:
            raise AttestationError(
                f"attestation kind {attestation.kind.value} does not match {expected_kind.value}"
            )
        if attestation.subject_digest != expected_subject_digest:
            raise AttestationError("attestation subject digest does not match semantic content")
        if attestation.issued_at_ms != expected_issued_at_ms:
            raise AttestationError("attestation time does not match semantic record time")
        self.verify_attestation_signature(attestation)

    def verify_attestation_signature(self, attestation: Attestation) -> None:
        self.verify_authority(attestation.authority)
        unsigned = _attestation_unsigned(
            attestation.authority,
            kind=attestation.kind,
            contract_version=attestation.contract_version,
            subject_digest=attestation.subject_digest,
            issued_at_ms=attestation.issued_at_ms,
        )
        expected = _sign_with_key(self._attestation_key(attestation.authority), unsigned)
        if not hmac.compare_digest(expected, attestation.signature):
            raise AttestationError("semantic attestation signature is invalid")

    def _attestation_key(self, authority: AuthorityRef) -> bytes:
        context = (
            "semantic-attestation-key|"
            + authority.signature
            + "|"
            + str(authority.authority_id)
        ).encode("utf-8")
        return hmac.new(self._secret, context, hashlib.sha256).digest()

    def _sign(self, value: Any) -> str:
        return _sign_with_key(self._secret, value)

    def _require_signature(self, unsigned: Any, signature: str, label: str) -> None:
        expected = self._sign(unsigned)
        if not hmac.compare_digest(expected, signature):
            raise AttestationError(f"{label} signature is invalid")


def _attestation_unsigned(
    authority: AuthorityRef,
    *,
    kind: AttestationKind,
    contract_version: str,
    subject_digest: str,
    issued_at_ms: int,
) -> dict[str, Any]:
    return {
        "authority": _canonical_value(authority),
        "kind": kind.value,
        "contractVersion": contract_version,
        "subjectDigest": subject_digest,
        "issuedAtMs": issued_at_ms,
    }


def _sign_with_key(key: bytes, value: Any) -> str:
    material = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "hmac-sha256:" + hmac.new(key, material, hashlib.sha256).hexdigest()


def semantic_digest(operation: str, *args: Any, **kwargs: Any) -> str:
    payload = {
        "operation": operation,
        "args": _canonical_value(args),
        "kwargs": _canonical_value(kwargs),
    }
    material = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(material).hexdigest()


def _canonical_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return {"$enum": type(value).__name__, "value": value.value}
    if is_dataclass(value) and not isinstance(value, type):
        return {
            "$dataclass": type(value).__name__,
            "fields": {
                field.name: _canonical_value(getattr(value, field.name)) for field in fields(value)
            },
        }
    if isinstance(value, tuple):
        return {"$tuple": [_canonical_value(item) for item in value]}
    if isinstance(value, list):
        return [_canonical_value(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("semantic digest dictionaries require string keys")
        return {key: _canonical_value(item) for key, item in value.items()}
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    raise TypeError(f"unsupported semantic digest value: {type(value).__name__}")
