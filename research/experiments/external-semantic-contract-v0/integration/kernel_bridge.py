from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from anc_canonical import canonical_digest
from anc_effect_binding import EffectBinding, binding_digest
from anc_effect_ir import CompletionKind, EffectEnvelope, ExecutionKind, SignedEffectEnvelope, effect_digest
from anc_tool_contract import ToolContract, contract_digest
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.model import (
    BindingAdmission,
    CapabilityRef,
    CompletionSemantics,
    EffectMode,
    KernelEffectProjection,
    EvidenceKind,
    IdempotencyKind,
    VerificationPlan,
    WorldObjectRef,
)


def semantic_id(value: str, expected: IdKind) -> SemanticId:
    prefix = expected.value + ":"
    if not value.startswith(prefix):
        raise ValueError(f"identity {value!r} is not a {expected.value} identity")
    return SemanticId(expected, value.removeprefix(prefix))


def internal_effect_projection(
    envelope: EffectEnvelope,
    *,
    backend_target: SemanticId,
) -> KernelEffectProjection:
    mode = EffectMode.OBSERVE if envelope.mode.value == "observe" else EffectMode.CHANGE
    if envelope.result.execution is ExecutionKind.ASYNCHRONOUS:
        completion = CompletionSemantics.ASYNCHRONOUS
    elif envelope.result.completion is CompletionKind.ACCEPTED_VERIFICATION:
        completion = CompletionSemantics.VERIFIED
    else:
        completion = CompletionSemantics.ACCEPTED
    idempotency = (
        IdempotencyKind.NATURAL
        if envelope.delivery.idempotency.value == "natural"
        else IdempotencyKind.NONE
    )
    required_evidence = tuple(
        EvidenceKind(item.value) for item in envelope.verification.required_evidence
    )
    principal = semantic_id(envelope.capability.principal_id, IdKind.PRINCIPAL)
    return KernelEffectProjection(
        effect_id=semantic_id(envelope.effect_id, IdKind.EFFECT),
        target=WorldObjectRef(backend_target, version=envelope.target.version),
        mode=mode,
        input_digest=envelope.input.digest,
        capability=CapabilityRef(
            principal, envelope.action.action_id, backend_target
        ),
        idempotency=idempotency,
        completion=completion,
        verification=VerificationPlan(
            envelope.verification.method, required_evidence
        ),
    )


def admit_bound_effect(
    views: Any,
    signed_effect: SignedEffectEnvelope,
    contract: ToolContract,
    binding: EffectBinding,
    binding_authority: Any,
    *,
    backend_target: SemanticId,
    event_namespace: str,
    admitted_at_ms: int = 1,
) -> tuple[KernelEffectProjection, BindingAdmission]:
    envelope = signed_effect.envelope
    if binding.effect_id != envelope.effect_id:
        raise ValueError("Binding and Envelope Effect identities differ")
    if binding.effect_digest != effect_digest(envelope):
        raise ValueError("Binding does not reference the Envelope digest")
    if binding.contract.contract_id != contract.contract_id:
        raise ValueError("Binding references a different ToolContract")
    if binding.contract.digest != contract_digest(contract):
        raise ValueError("Binding ToolContract digest is stale")
    spec = internal_effect_projection(envelope, backend_target=backend_target)
    views.effects.admit_effect(
        spec,
        event_id=SemanticId(IdKind.EVENT, f"{event_namespace}:effect-admit"),
        recorded_at_ms=admitted_at_ms,
    )
    views.effects.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=SemanticId(IdKind.EVENT, f"{event_namespace}:effect-prepare"),
        recorded_at_ms=admitted_at_ms + 1,
    )
    admission, _ = binding_authority.admit(
        views,
        signed_effect,
        contract,
        binding,
        admitted_at_ms=admitted_at_ms + 2,
    )
    return spec, admission


def project_binding_admission(
    binding: EffectBinding, *, admitted_at_ms: int
) -> BindingAdmission:
    return BindingAdmission(
        binding_id=semantic_id(binding.binding_id, IdKind.BINDING),
        effect_id=semantic_id(binding.effect_id, IdKind.EFFECT),
        effect_digest=binding.effect_digest,
        binding_digest=binding_digest(binding),
        binding_revision=binding.binding_revision,
        admitted_at_ms=admitted_at_ms,
        supersedes_binding_id=(
            None
            if binding.supersedes_binding_id is None
            else semantic_id(binding.supersedes_binding_id, IdKind.BINDING)
        ),
    )


@dataclass(slots=True)
class BoundExecutionView:
    """Inject and enforce one immutable complete Binding at the Kernel edge."""

    execution: Any
    admission: BindingAdmission
    complete_binding: EffectBinding

    def __post_init__(self) -> None:
        if binding_digest(self.complete_binding) != self.admission.binding_digest:
            raise ValueError("complete Binding does not match Kernel admission")
        if self.complete_binding.effect_id != str(self.admission.effect_id):
            raise ValueError("complete Binding belongs to another Effect")

    def begin_dispatch(self, effect_id: SemanticId, **kwargs: Any):
        if effect_id != self.admission.effect_id:
            raise ValueError("Bound execution view cannot dispatch another Effect")
        request_digest = kwargs.get("request_digest")
        if request_digest != canonical_digest(self.complete_binding.arguments):
            raise ValueError("actual Tool request differs from admitted Binding arguments")
        return self.execution.begin_dispatch(
            effect_id,
            **kwargs,
            binding_id=self.admission.binding_id,
            binding_digest=self.admission.binding_digest,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self.execution, name)
