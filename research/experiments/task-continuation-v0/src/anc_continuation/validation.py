from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from anc_canonical import JsonValue, loads_strict
from anc_effect_binding import (
    SignedEffectBinding,
    binding_digest,
    signed_effect_binding_from_dict,
)
from anc_effect_ir import (
    EffectEnvelope,
    ProtocolAttestation,
    ProtocolAuthorityError,
    SignedEffectEnvelope,
    effect_digest,
)
from anc_tool_contract import (
    CancellationKind,
    CompletionKind,
    CorrelationKind,
    EffectClass,
    ExecutionKind,
    IdempotencySupport,
    ToolContract,
    contract_digest,
)

from .model import ReadyAction, SemanticRef, TaskCapsule
from .store import FileObjectStore, ObjectStoreError
from .workload import DECISION, protocol_authorities, sha256_text




def tool_contract_from_dict(value: dict[str, Any]) -> ToolContract:
    expected = {
        "schemaVersion",
        "kind",
        "contractId",
        "revision",
        "providerId",
        "operation",
        "semanticAction",
        "inputSchema",
        "outputSchema",
        "execution",
        "completion",
        "effectClass",
        "idempotencySupport",
        "correlation",
        "cancellation",
        "evidence",
        "capabilityClass",
    }
    if set(value) != expected:
        raise ValueError("normalized ToolContract fields differ")
    evidence = value["evidence"]
    if not isinstance(evidence, list) or any(not isinstance(item, str) for item in evidence):
        raise ValueError("ToolContract evidence must be strings")
    return ToolContract(
        contract_id=str(value["contractId"]),
        revision=str(value["revision"]),
        provider_id=str(value["providerId"]),
        operation=str(value["operation"]),
        semantic_action=str(value["semanticAction"]),
        input_schema=value["inputSchema"],
        output_schema=value["outputSchema"],
        execution=ExecutionKind(str(value["execution"])),
        completion=CompletionKind(str(value["completion"])),
        effect_class=EffectClass(str(value["effectClass"])),
        idempotency_support=IdempotencySupport(str(value["idempotencySupport"])),
        correlation=CorrelationKind(str(value["correlation"])),
        cancellation=CancellationKind(str(value["cancellation"])),
        evidence=tuple(evidence),
        capability_class=str(value["capabilityClass"]),
        schema_version=int(value["schemaVersion"]),
        kind=str(value["kind"]),
    )

class CapsuleValidationError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ResolvedAction:
    action: ReadyAction
    signed_effect: SignedEffectEnvelope
    contract: ToolContract
    signed_binding: SignedEffectBinding


@dataclass(frozen=True, slots=True)
class ValidationReport:
    current_world_digest: str
    world_status: str
    completed_effect_ids: tuple[str, ...]
    fact_ids: tuple[str, ...]
    artifact_ids: tuple[str, ...]
    decisions: tuple[dict[str, JsonValue], ...]
    unresolved_dispatch_ids: tuple[str, ...]
    resolved_actions: tuple[ResolvedAction, ...]


class CapsuleValidator:
    def __init__(self, store: FileObjectStore) -> None:
        self.store = store
        self.effect_authority, self.binding_authority = protocol_authorities()

    def validate(self, capsule: TaskCapsule, *, world_root: str | Path) -> ValidationReport:
        world_path = Path(world_root) / capsule.world.relative_path
        if not world_path.is_file():
            raise CapsuleValidationError(
                f"world object is missing: {capsule.world.relative_path}"
            )
        current_world_digest = sha256_text(world_path.read_text())
        world_status = (
            "current"
            if current_world_digest == capsule.world.observed_digest
            else "drifted"
        )

        completed: list[str] = []
        for ref in capsule.completed_effects:
            payload = self._payload(ref)
            signed = self._signed_effect(payload)
            if signed.envelope.effect_id != ref.semantic_id:
                raise CapsuleValidationError("completed Effect identity differs")
            if payload.get("state") != "succeeded":
                raise CapsuleValidationError("completed Effect reference is not succeeded")
            if payload.get("effectDigest") != effect_digest(signed.envelope):
                raise CapsuleValidationError("completed Effect digest differs")
            completed.append(ref.semantic_id)

        facts: list[str] = []
        verified_checkpoint_digest = False
        for ref in capsule.facts:
            payload = self._payload(ref)
            if not isinstance(payload, dict):
                raise CapsuleValidationError("Fact payload must be an object")
            if payload.get("factId") != ref.semantic_id:
                raise CapsuleValidationError("Fact identity differs")
            if payload.get("decision") != "accepted":
                raise CapsuleValidationError("TaskCapsule references a rejected Fact")
            if payload.get("predicate") == "content_digest_equals":
                if payload.get("valueDigest") == capsule.world.observed_digest:
                    verified_checkpoint_digest = True
            facts.append(ref.semantic_id)
        if not verified_checkpoint_digest:
            raise CapsuleValidationError(
                "TaskCapsule has no accepted Fact for the checkpoint world digest"
            )

        decisions: list[dict[str, JsonValue]] = []
        artifacts: list[str] = []
        for ref in capsule.artifacts:
            payload = self._payload(ref)
            if not isinstance(payload, dict):
                raise CapsuleValidationError("Artifact payload must be an object")
            if payload.get("artifactKind") != "decision":
                raise CapsuleValidationError("v0 Capsule retains only decision Artifacts")
            content = payload.get("content")
            if not isinstance(content, str):
                raise CapsuleValidationError("decision Artifact content must be UTF-8 text")
            calculated = "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()
            if payload.get("digest") != calculated:
                raise CapsuleValidationError("decision Artifact digest differs from content")
            try:
                decision = loads_strict(content)
            except ValueError as error:
                raise CapsuleValidationError("decision Artifact is not canonical JSON") from error
            if not isinstance(decision, dict) or decision.get("decisionId") != DECISION["decisionId"]:
                raise CapsuleValidationError("required continuation decision is missing")
            decisions.append(decision)
            artifacts.append(ref.semantic_id)
        if not decisions:
            raise CapsuleValidationError("TaskCapsule has no retained decision Artifact")

        unresolved: list[str] = []
        for ref in capsule.unresolved_dispatches:
            payload = self._payload(ref)
            if not isinstance(payload, dict):
                raise CapsuleValidationError("Dispatch payload must be an object")
            if payload.get("dispatchId") != ref.semantic_id:
                raise CapsuleValidationError("Dispatch identity differs")
            if payload.get("state") not in {"unknown", "reconciling"}:
                raise CapsuleValidationError(
                    "unresolved Dispatch reference is not unknown or reconciling"
                )
            unresolved.append(ref.semantic_id)

        binding_by_id: dict[str, SignedEffectBinding] = {}
        for ref in capsule.current_bindings:
            payload = self._payload(ref)
            signed_binding = self._signed_binding(payload)
            if signed_binding.binding.binding_id != ref.semantic_id:
                raise CapsuleValidationError("current Binding identity differs")
            binding_by_id[ref.semantic_id] = signed_binding

        actions: list[ResolvedAction] = []
        for action in capsule.next_ready:
            effect_payload = self._payload(action.effect)
            signed_effect = self._signed_effect(effect_payload)
            if signed_effect.envelope.effect_id in completed:
                raise CapsuleValidationError("next-ready work repeats a completed Effect")
            if effect_payload.get("state") != "proposed":
                raise CapsuleValidationError("next-ready Effect is not proposed")
            contract_value = effect_payload.get("contract")
            if not isinstance(contract_value, dict):
                raise CapsuleValidationError("next-ready Effect has no ToolContract")
            try:
                contract = tool_contract_from_dict(contract_value)
            except ValueError as error:
                raise CapsuleValidationError("next-ready ToolContract is invalid") from error
            signed_binding = binding_by_id.get(action.binding.semantic_id)
            if signed_binding is None:
                raise CapsuleValidationError("next-ready Binding is not current")
            binding = signed_binding.binding
            if binding.effect_id != signed_effect.envelope.effect_id:
                raise CapsuleValidationError("next-ready Binding belongs to another Effect")
            if binding.effect_digest != effect_digest(signed_effect.envelope):
                raise CapsuleValidationError("next-ready Binding has another Effect digest")
            if binding.contract.contract_id != contract.contract_id:
                raise CapsuleValidationError("next-ready Binding has another ToolContract")
            if binding.contract.digest != contract_digest(contract):
                raise CapsuleValidationError("next-ready Binding ToolContract digest differs")
            if signed_effect.envelope.target.version != action.required_world_digest:
                raise CapsuleValidationError("next-ready Effect targets another world version")
            if action.required_world_digest != capsule.world.observed_digest:
                raise CapsuleValidationError("next-ready action ignores checkpoint world version")
            actions.append(ResolvedAction(action, signed_effect, contract, signed_binding))

        return ValidationReport(
            current_world_digest=current_world_digest,
            world_status=world_status,
            completed_effect_ids=tuple(completed),
            fact_ids=tuple(facts),
            artifact_ids=tuple(artifacts),
            decisions=tuple(decisions),
            unresolved_dispatch_ids=tuple(unresolved),
            resolved_actions=tuple(actions),
        )

    def _payload(self, ref: SemanticRef) -> Any:
        try:
            return self.store.resolve_semantic(ref)
        except ObjectStoreError as error:
            raise CapsuleValidationError(str(error)) from error

    def _signed_effect(self, payload: Any) -> SignedEffectEnvelope:
        if not isinstance(payload, dict):
            raise CapsuleValidationError("Effect payload must be an object")
        signed = payload.get("signedEffect")
        if not isinstance(signed, dict) or set(signed) != {"envelope", "attestation"}:
            raise CapsuleValidationError("Effect payload has no signed Effect")
        envelope = signed["envelope"]
        attestation = signed["attestation"]
        if not isinstance(envelope, dict) or not isinstance(attestation, dict):
            raise CapsuleValidationError("signed Effect records must be objects")
        try:
            value = SignedEffectEnvelope(
                EffectEnvelope.from_dict(envelope),
                ProtocolAttestation.from_dict(attestation),
            )
            self.effect_authority.verify(
                value.attestation,
                expected_kind="effect_proposal",
                expected_contract_version="effect-envelope-v1",
                expected_subject_digest=effect_digest(value.envelope),
            )
        except (ValueError, ProtocolAuthorityError) as error:
            raise CapsuleValidationError("signed Effect verification failed") from error
        return value

    def _signed_binding(self, payload: Any) -> SignedEffectBinding:
        if not isinstance(payload, dict):
            raise CapsuleValidationError("Binding payload must be an object")
        signed = payload.get("signedBinding")
        if not isinstance(signed, dict):
            raise CapsuleValidationError("Binding payload has no signed Binding")
        try:
            value = signed_effect_binding_from_dict(signed)
            digest = binding_digest(value.binding)
            if payload.get("bindingDigest") != digest:
                raise ValueError("stored Binding digest differs")
            self.binding_authority.verify(
                value.attestation,
                expected_kind="effect_binding",
                expected_contract_version="effect-binding-v1",
                expected_subject_digest=digest,
            )
        except (ValueError, ProtocolAuthorityError) as error:
            raise CapsuleValidationError("signed Binding verification failed") from error
        return value
