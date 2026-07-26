from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from anc_effect_binding import (
    BindingStore,
    EffectBinding,
    SignedEffectBinding,
    binding_digest,
)
from anc_effect_ir import (
    ProtocolAuthority,
    SignedEffectEnvelope,
    effect_digest,
)
from anc_tool_contract import ToolContract, contract_digest
from anc_semantic_core.model import BindingAdmission

from .kernel_bridge import project_binding_admission


@dataclass(frozen=True, slots=True)
class AuthorizedBindingArtifact:
    signed_binding: SignedEffectBinding
    artifact_digest: str


class BindingAuthorityService:
    """Verify public Effect/contract content, sign the Binding, and retain it outside Kernel state."""

    def __init__(
        self,
        *,
        effect_authority: ProtocolAuthority,
        binding_authority: ProtocolAuthority,
        store: BindingStore,
    ) -> None:
        if effect_authority.role != "effect":
            raise ValueError("effect authority must have role effect")
        if binding_authority.role != "binding":
            raise ValueError("binding authority must have role binding")
        self.effect_authority = effect_authority
        self.binding_authority = binding_authority
        self.store = store

    def authorize(
        self,
        signed_effect: SignedEffectEnvelope,
        contract: ToolContract,
        binding: EffectBinding,
        *,
        issued_at_ms: int,
    ) -> AuthorizedBindingArtifact:
        envelope = signed_effect.envelope
        envelope_digest = effect_digest(envelope)
        self.effect_authority.verify(
            signed_effect.attestation,
            expected_kind="effect_proposal",
            expected_contract_version="effect-envelope-v1",
            expected_subject_digest=envelope_digest,
        )
        if binding.effect_id != envelope.effect_id:
            raise ValueError("Binding and signed Effect identities differ")
        if binding.effect_digest != envelope_digest:
            raise ValueError("Binding Effect digest differs from signed Effect content")
        if binding.contract.contract_id != contract.contract_id:
            raise ValueError("Binding references another ToolContract")
        if binding.contract.revision != contract.revision:
            raise ValueError("Binding references another ToolContract revision")
        if binding.contract.digest != contract_digest(contract):
            raise ValueError("Binding ToolContract digest is stale")
        if contract.semantic_action != envelope.action.action_id:
            raise ValueError("ToolContract does not implement the signed Effect action")
        digest = binding_digest(binding)
        attestation = self.binding_authority.attest(
            kind="effect_binding",
            contract_version="effect-binding-v1",
            subject_digest=digest,
            issued_at_ms=issued_at_ms,
        )
        signed_binding = SignedEffectBinding(binding, attestation)
        stored_digest = self.store.put(signed_binding)
        if stored_digest != digest:
            raise RuntimeError("Binding store changed the content address")
        return AuthorizedBindingArtifact(signed_binding, stored_digest)

    def admit(
        self,
        views: Any,
        signed_effect: SignedEffectEnvelope,
        contract: ToolContract,
        binding: EffectBinding,
        *,
        admitted_at_ms: int,
    ) -> tuple[BindingAdmission, AuthorizedBindingArtifact]:
        artifact = self.authorize(
            signed_effect,
            contract,
            binding,
            issued_at_ms=admitted_at_ms,
        )
        admission = project_binding_admission(
            artifact.signed_binding.binding,
            admitted_at_ms=admitted_at_ms,
        )
        views.bindings.admit_binding(admission)
        stored = views.read.get_binding(admission.binding_id)
        self.resolve(stored)
        return stored, artifact

    def resolve(self, admission: BindingAdmission) -> SignedEffectBinding:
        signed = self.store.get(admission.binding_digest)
        digest = binding_digest(signed.binding)
        self.binding_authority.verify(
            signed.attestation,
            expected_kind="effect_binding",
            expected_contract_version="effect-binding-v1",
            expected_subject_digest=digest,
        )
        if signed.binding.binding_id != str(admission.binding_id):
            raise ValueError("stored Binding identity differs from Kernel admission")
        if signed.binding.effect_id != str(admission.effect_id):
            raise ValueError("stored Binding Effect differs from Kernel admission")
        if signed.binding.effect_digest != admission.effect_digest:
            raise ValueError("stored Binding Effect digest differs from Kernel admission")
        if digest != admission.binding_digest:
            raise ValueError("stored Binding digest differs from Kernel admission")
        if signed.binding.binding_revision != admission.binding_revision:
            raise ValueError("stored Binding revision differs from Kernel admission")
        expected_supersedes = (
            None
            if admission.supersedes_binding_id is None
            else str(admission.supersedes_binding_id)
        )
        if signed.binding.supersedes_binding_id != expected_supersedes:
            raise ValueError("stored Binding supersedes edge differs from Kernel admission")
        return signed
