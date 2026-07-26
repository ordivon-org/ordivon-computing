from __future__ import annotations

import os
import secrets
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = ROOT.parent / "semantic-core-v0"
for path in (ROOT, ROOT / "src", CORE_ROOT / "src", CORE_ROOT / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from anc_effect_binding import FileBindingStore  # noqa: E402
from anc_effect_ir import (  # noqa: E402
    EffectEnvelope,
    ProtocolAuthority,
    SignedEffectEnvelope,
    effect_digest,
)
from integration import BindingAuthorityService  # noqa: E402


EFFECT_SECRET_ENV = "ANC_EXTERNAL_EFFECT_SECRET_HEX"
BINDING_SECRET_ENV = "ANC_EXTERNAL_BINDING_SECRET_HEX"


def secret_from_environment(name: str, *, create: bool) -> bytes:
    encoded = os.environ.get(name)
    if encoded:
        try:
            secret = bytes.fromhex(encoded)
        except ValueError as error:
            raise SystemExit(f"{name} must contain hexadecimal bytes") from error
        if len(secret) < 32:
            raise SystemExit(f"{name} must contain at least 32 bytes")
        return secret
    if create:
        return secrets.token_bytes(32)
    raise SystemExit(f"{name} is required to resume the signed Binding store")


@dataclass(slots=True)
class LiveBindingContext:
    effect_authority: ProtocolAuthority
    binding_authority: ProtocolAuthority
    service: BindingAuthorityService
    effect_secret: bytes
    binding_secret: bytes

    @classmethod
    def open(cls, store_path: str | Path, *, create_secrets: bool) -> "LiveBindingContext":
        effect_secret = secret_from_environment(EFFECT_SECRET_ENV, create=create_secrets)
        binding_secret = secret_from_environment(BINDING_SECRET_ENV, create=create_secrets)
        effect_authority = ProtocolAuthority(
            authority_id="authority:ordivon-live-effect",
            issuer_id="principal:ordivon-live-protocol-issuer",
            principal_id="principal:ordivon-live-agent",
            role="effect",
            trust_domain="ordivon-live",
            policy_version="external-contract-v1",
            key_id="ordivon-live-effect-key",
            secret=effect_secret,
        )
        binding_authority = ProtocolAuthority(
            authority_id="authority:ordivon-live-binding",
            issuer_id="principal:ordivon-live-protocol-issuer",
            principal_id="principal:ordivon-live-binding-service",
            role="binding",
            trust_domain="ordivon-live",
            policy_version="external-contract-v1",
            key_id="ordivon-live-binding-key",
            secret=binding_secret,
        )
        service = BindingAuthorityService(
            effect_authority=effect_authority,
            binding_authority=binding_authority,
            store=FileBindingStore(store_path),
        )
        return cls(
            effect_authority,
            binding_authority,
            service,
            effect_secret,
            binding_secret,
        )

    def sign(self, envelope: EffectEnvelope, *, issued_at_ms: int) -> SignedEffectEnvelope:
        return SignedEffectEnvelope(
            envelope,
            self.effect_authority.attest(
                kind="effect_proposal",
                contract_version="effect-envelope-v1",
                subject_digest=effect_digest(envelope),
                issued_at_ms=issued_at_ms,
            ),
        )

    def child_environment(self) -> dict[str, str]:
        return {
            EFFECT_SECRET_ENV: self.effect_secret.hex(),
            BINDING_SECRET_ENV: self.binding_secret.hex(),
        }
