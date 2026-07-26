from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from anc_canonical import JsonValue, canonical_digest
from anc_effect_ir import EffectEnvelope, ProtocolAttestation, effect_digest
from anc_tool_contract import ContractChange, ToolContract, contract_digest


class BindingChangeClass(StrEnum):
    INITIAL = "initial"
    CALLER_ADAPTATION = "caller-adaptation"
    COMPATIBLE_EXTENSION = "compatible-extension"


class BindingDecision(StrEnum):
    KEEP = "keep"
    REBIND = "rebind"
    REAUTHORIZE = "reauthorize"
    NEW_EFFECT = "new-effect"
    OBSERVE_ORIGINAL = "observe-original"
    FAIL_CLOSED = "fail-closed"


def _identity(value: str, prefix: str) -> str:
    if not value.startswith(prefix + ":") or value != value.strip():
        raise ValueError(f"identity must start with {prefix}:")
    return value


def _digest(value: str) -> str:
    if (
        len(value) != 71
        or not value.startswith("sha256:")
        or any(ch not in "0123456789abcdef" for ch in value[7:])
    ):
        raise ValueError("invalid sha256 digest")
    return value


@dataclass(frozen=True, slots=True)
class ContractRef:
    contract_id: str
    revision: str
    digest: str

    def __post_init__(self) -> None:
        _identity(self.contract_id, "tool-contract")
        _digest(self.digest)
        if not self.revision:
            raise ValueError("contract revision is required")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "contractId": self.contract_id,
            "revision": self.revision,
            "digest": self.digest,
        }


@dataclass(frozen=True, slots=True)
class EncoderRef:
    encoder_id: str
    version: int

    def __post_init__(self) -> None:
        if not self.encoder_id.startswith("anc.binding.") or self.version < 1:
            raise ValueError("invalid encoder identity")

    def to_dict(self) -> dict[str, JsonValue]:
        return {"encoderId": self.encoder_id, "version": self.version}


@dataclass(frozen=True, slots=True)
class EffectBinding:
    binding_id: str
    binding_revision: int
    effect_id: str
    effect_digest: str
    contract: ContractRef
    encoder: EncoderRef
    arguments: JsonValue
    argument_digest: str | None = None
    supersedes_binding_id: str | None = None
    change_class: BindingChangeClass = BindingChangeClass.INITIAL
    schema_version: int = 1
    kind: str = "anc.effect-binding"

    def __post_init__(self) -> None:
        _identity(self.binding_id, "binding")
        _identity(self.effect_id, "effect")
        _digest(self.effect_digest)
        if (
            self.binding_revision < 1
            or self.schema_version != 1
            or self.kind != "anc.effect-binding"
        ):
            raise ValueError("invalid Binding version")
        calculated = canonical_digest(self.arguments)
        if self.argument_digest is None:
            object.__setattr__(self, "argument_digest", calculated)
        elif _digest(self.argument_digest) != calculated:
            raise ValueError("argument digest mismatch")
        if self.supersedes_binding_id is not None:
            _identity(self.supersedes_binding_id, "binding")
            if self.binding_revision < 2 or self.supersedes_binding_id == self.binding_id:
                raise ValueError("invalid supersedes relation")
        elif self.binding_revision != 1:
            raise ValueError("later Binding revisions must supersede an earlier Binding")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": self.schema_version,
            "kind": self.kind,
            "bindingId": self.binding_id,
            "bindingRevision": self.binding_revision,
            "effectId": self.effect_id,
            "effectDigest": self.effect_digest,
            "contract": self.contract.to_dict(),
            "encoder": self.encoder.to_dict(),
            "arguments": {
                "encoding": "anc-canonical-json-v1",
                "digest": self.argument_digest,
                "value": self.arguments,
            },
            "supersedesBindingId": self.supersedes_binding_id,
            "changeClass": self.change_class.value,
        }


@dataclass(frozen=True, slots=True)
class SignedEffectBinding:
    binding: EffectBinding
    attestation: ProtocolAttestation

    def __post_init__(self) -> None:
        if self.attestation.role != "binding" or self.attestation.kind != "effect_binding":
            raise ValueError("Binding requires Binding Authority")
        if self.attestation.subject_digest != binding_digest(self.binding):
            raise ValueError("Binding attestation digest mismatch")


def binding_digest(binding: EffectBinding) -> str:
    return canonical_digest(binding.to_dict())


def assess_binding(effect_state: str, change: ContractChange) -> BindingDecision:
    if effect_state in {
        "dispatched",
        "running",
        "cancel_requested",
        "unknown",
        "reconciling",
    }:
        return BindingDecision.OBSERVE_ORIGINAL
    if effect_state in {"succeeded", "failed", "cancelled"}:
        return BindingDecision.KEEP
    if effect_state not in {"proposed", "prepared"}:
        return BindingDecision.FAIL_CLOSED
    return {
        ContractChange.IDENTICAL: BindingDecision.KEEP,
        ContractChange.COMPATIBLE_EXTENSION: BindingDecision.KEEP,
        ContractChange.CALLER_ADAPTATION: BindingDecision.REBIND,
        ContractChange.CAPABILITY_CHANGE: BindingDecision.REAUTHORIZE,
        ContractChange.SEMANTIC_BREAK: BindingDecision.NEW_EFFECT,
        ContractChange.COMPLETION_CHANGE: BindingDecision.FAIL_CLOSED,
        ContractChange.UNKNOWN: BindingDecision.FAIL_CLOSED,
    }[change]


def _binding(
    effect: EffectEnvelope,
    contract: ToolContract,
    *,
    backend: str,
    binding_id: str,
    revision: int,
    arguments: JsonValue,
    supersedes: str | None = None,
    change_class: BindingChangeClass = BindingChangeClass.INITIAL,
) -> EffectBinding:
    if contract.semantic_action != effect.action.action_id:
        raise ValueError("ToolContract does not implement Effect semantic action")
    return EffectBinding(
        binding_id=binding_id,
        binding_revision=revision,
        effect_id=effect.effect_id,
        effect_digest=effect_digest(effect),
        contract=ContractRef(
            contract.contract_id,
            contract.revision,
            contract_digest(contract),
        ),
        encoder=EncoderRef(
            f"anc.binding.{backend}.{contract.operation.replace('.', '-')}", 1
        ),
        arguments=arguments,
        supersedes_binding_id=supersedes,
        change_class=change_class,
    )


def lower_to_ordivon(
    effect: EffectEnvelope,
    contract: ToolContract,
    *,
    binding_id: str,
    revision: int = 1,
    supersedes: str | None = None,
    workspace_id: str = "workspace-001",
) -> EffectBinding:
    action = effect.action.action_id
    value = effect.input.value
    if action == "anc.object.read.v1":
        arguments: JsonValue = {
            "schemaVersion": 1,
            "workspaceId": workspace_id,
            "relativePath": _target_path(effect),
        }
    elif action == "anc.object.replace-if-version.v1":
        if (
            not isinstance(value, dict)
            or set(value) != {"content"}
            or effect.target.version is None
        ):
            raise ValueError("replace input requires content and target version")
        arguments = {
            "schemaVersion": 1,
            "workspaceId": workspace_id,
            "mutations": [
                {
                    "relativePath": _target_path(effect),
                    "mode": "WRITE",
                    "content": value["content"],
                    "expectedDigest": effect.target.version,
                }
            ],
        }
    elif action == "anc.execution.launch.v1":
        if not isinstance(value, dict) or not {"executable", "args"}.issubset(value):
            raise ValueError("launch input requires executable and args")
        arguments = {
            "schemaVersion": 1,
            "workspaceId": workspace_id,
            "executable": value["executable"],
            "args": value["args"],
        }
    else:
        raise ValueError("unsupported Ordivon semantic action")
    return _binding(
        effect,
        contract,
        backend="ordivon",
        binding_id=binding_id,
        revision=revision,
        arguments=arguments,
        supersedes=supersedes,
        change_class=(
            BindingChangeClass.CALLER_ADAPTATION
            if revision > 1
            else BindingChangeClass.INITIAL
        ),
    )


def lower_to_simulator(
    effect: EffectEnvelope,
    contract: ToolContract,
    *,
    binding_id: str,
    revision: int = 1,
    supersedes: str | None = None,
) -> EffectBinding:
    action = effect.action.action_id
    value = effect.input.value
    key = _target_key(effect)
    if action == "anc.object.read.v1":
        arguments: JsonValue = {"objectKey": key}
    elif action == "anc.object.replace-if-version.v1":
        if (
            not isinstance(value, dict)
            or set(value) != {"content"}
            or effect.target.version is None
        ):
            raise ValueError("replace input requires content and target version")
        arguments = {
            "objectKey": key,
            "expectedVersion": effect.target.version,
            "content": value["content"],
        }
    elif action == "anc.execution.launch.v1":
        if not isinstance(value, dict) or not {"executable", "args"}.issubset(value):
            raise ValueError("launch input requires executable and args")
        arguments = {
            "objectKey": key,
            "action": {"executable": value["executable"], "args": value["args"]},
        }
    else:
        raise ValueError("unsupported simulator semantic action")
    return _binding(
        effect,
        contract,
        backend="simulator",
        binding_id=binding_id,
        revision=revision,
        arguments=arguments,
        supersedes=supersedes,
        change_class=(
            BindingChangeClass.CALLER_ADAPTATION
            if revision > 1
            else BindingChangeClass.INITIAL
        ),
    )


def _target_path(effect: EffectEnvelope) -> str:
    value = effect.target.object_id.split(":", 2)[-1]
    return value.split("/", 1)[-1]


def _target_key(effect: EffectEnvelope) -> str:
    return effect.target.object_id.split(":", 2)[-1]
