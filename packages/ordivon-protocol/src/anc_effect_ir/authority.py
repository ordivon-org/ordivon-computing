from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

from anc_canonical import JsonValue, canonical_bytes, canonical_digest

from .model import ProtocolAttestation


class ProtocolAuthorityError(RuntimeError):
    pass


class ProtocolAuthorityDenied(ProtocolAuthorityError):
    pass


class ProtocolAttestationError(ProtocolAuthorityError):
    pass


def _identity(value: str, prefix: str) -> str:
    if not value.startswith(prefix + ":") or value != value.strip():
        raise ValueError(f"identity must start with {prefix}:")
    return value


def _signature(key: bytes, value: JsonValue) -> str:
    return "hmac-sha256:" + hmac.new(key, canonical_bytes(value), hashlib.sha256).hexdigest()


@dataclass(frozen=True, slots=True)
class ProtocolAuthority:
    authority_id: str
    issuer_id: str
    principal_id: str
    role: str
    trust_domain: str
    policy_version: str
    key_id: str
    secret: bytes

    def __post_init__(self) -> None:
        _identity(self.authority_id, "authority")
        _identity(self.issuer_id, "principal")
        _identity(self.principal_id, "principal")
        if not self.role or not self.trust_domain or not self.policy_version or not self.key_id:
            raise ValueError("protocol authority metadata is incomplete")
        if len(self.secret) < 32:
            raise ValueError("protocol authority secret must contain at least 32 bytes")
        object.__setattr__(self, "secret", bytes(self.secret))

    @property
    def authority_signature(self) -> str:
        return _signature(self.secret, self._grant_payload())

    @property
    def fingerprint(self) -> str:
        return canonical_digest(self._grant_payload())

    def attest(
        self,
        *,
        kind: str,
        contract_version: str,
        subject_digest: str,
        issued_at_ms: int,
    ) -> ProtocolAttestation:
        if not kind or not contract_version:
            raise ValueError("attestation kind and contract version are required")
        unsigned = self._attestation_payload(
            kind=kind,
            contract_version=contract_version,
            subject_digest=subject_digest,
            issued_at_ms=issued_at_ms,
        )
        return ProtocolAttestation(
            authority_id=self.authority_id,
            issuer_id=self.issuer_id,
            principal_id=self.principal_id,
            role=self.role,
            trust_domain=self.trust_domain,
            policy_version=self.policy_version,
            key_id=self.key_id,
            authority_signature=self.authority_signature,
            kind=kind,
            contract_version=contract_version,
            subject_digest=subject_digest,
            issued_at_ms=issued_at_ms,
            signature=_signature(self._attestation_key(), unsigned),
        )

    def verify(
        self,
        attestation: ProtocolAttestation,
        *,
        expected_kind: str,
        expected_contract_version: str,
        expected_subject_digest: str,
    ) -> None:
        expected_fields = {
            "authority_id": self.authority_id,
            "issuer_id": self.issuer_id,
            "principal_id": self.principal_id,
            "role": self.role,
            "trust_domain": self.trust_domain,
            "policy_version": self.policy_version,
            "key_id": self.key_id,
        }
        for field, expected in expected_fields.items():
            if getattr(attestation, field) != expected:
                raise ProtocolAuthorityDenied(f"protocol authority {field} is not trusted")
        if not hmac.compare_digest(attestation.authority_signature, self.authority_signature):
            raise ProtocolAttestationError("protocol authority grant signature is invalid")
        if attestation.kind != expected_kind:
            raise ProtocolAttestationError("protocol attestation kind does not match")
        if attestation.contract_version != expected_contract_version:
            raise ProtocolAttestationError("protocol contract version does not match")
        if attestation.subject_digest != expected_subject_digest:
            raise ProtocolAttestationError("protocol subject digest does not match")
        unsigned = self._attestation_payload(
            kind=attestation.kind,
            contract_version=attestation.contract_version,
            subject_digest=attestation.subject_digest,
            issued_at_ms=attestation.issued_at_ms,
        )
        expected_signature = _signature(self._attestation_key(), unsigned)
        if not hmac.compare_digest(attestation.signature, expected_signature):
            raise ProtocolAttestationError("protocol attestation signature is invalid")

    def _grant_payload(self) -> dict[str, JsonValue]:
        return {
            "authorityId": self.authority_id,
            "issuerId": self.issuer_id,
            "principalId": self.principal_id,
            "role": self.role,
            "trustDomain": self.trust_domain,
            "policyVersion": self.policy_version,
            "keyId": self.key_id,
        }

    def _attestation_key(self) -> bytes:
        context = (
            "external-protocol-attestation|"
            + self.authority_signature
            + "|"
            + self.authority_id
        ).encode("utf-8")
        return hmac.new(self.secret, context, hashlib.sha256).digest()

    def _attestation_payload(
        self,
        *,
        kind: str,
        contract_version: str,
        subject_digest: str,
        issued_at_ms: int,
    ) -> dict[str, JsonValue]:
        return {
            "authority": self._grant_payload(),
            "authoritySignature": self.authority_signature,
            "kind": kind,
            "contractVersion": contract_version,
            "subjectDigest": subject_digest,
            "issuedAtMs": issued_at_ms,
        }
