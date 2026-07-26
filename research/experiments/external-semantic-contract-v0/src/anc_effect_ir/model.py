from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from anc_canonical import JsonValue, canonical_bytes, canonical_digest, loads_strict, validate_json_value

_EFFECT_KIND = "anc.effect-envelope"
_SCHEMA_VERSION = 1
_ACTIONS = {
    "anc.object.read.v1",
    "anc.object.replace-if-version.v1",
    "anc.execution.launch.v1",
}


class EffectMode(StrEnum):
    OBSERVE = "observe"
    CHANGE = "change"


class ExecutionKind(StrEnum):
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"


class CompletionKind(StrEnum):
    RESPONSE = "response"
    TERMINAL_OBSERVATION = "terminal-observation"
    ACCEPTED_VERIFICATION = "accepted-verification"


class EvidenceKind(StrEnum):
    OBSERVATION = "observation"
    ARTIFACT = "artifact"


class IdempotencyKind(StrEnum):
    NONE = "none"
    NATURAL = "natural"


def _identifier(value: str, prefix: str) -> str:
    if not isinstance(value, str) or not value.startswith(prefix + ":"):
        raise ValueError(f"identity must start with {prefix}:")
    if value != value.strip() or len(value.encode("utf-8")) > 300:
        raise ValueError("identity is empty, padded, or too long")
    return value


def _digest(value: str) -> str:
    if not isinstance(value, str) or len(value) != 71 or not value.startswith("sha256:"):
        raise ValueError("digest must be sha256:<64 lowercase hex>")
    if any(ch not in "0123456789abcdef" for ch in value[7:]):
        raise ValueError("digest must use lowercase hexadecimal")
    return value


def _exact(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{label} fields differ: {sorted(set(value) ^ expected)}")


@dataclass(frozen=True, slots=True)
class TargetRef:
    object_id: str
    version: str | None = None

    def __post_init__(self) -> None:
        _identifier(self.object_id, "world_object")
        if self.version is not None:
            _digest(self.version)

    def to_dict(self) -> dict[str, JsonValue]:
        return {"objectId": self.object_id, "version": self.version}


@dataclass(frozen=True, slots=True)
class SemanticAction:
    action_id: str
    input_type: str

    def __post_init__(self) -> None:
        if self.action_id not in _ACTIONS:
            raise ValueError(f"unfrozen semantic action: {self.action_id}")
        if not self.input_type or not self.input_type.endswith(".v1"):
            raise ValueError("input type must be a versioned semantic identity")

    def to_dict(self) -> dict[str, JsonValue]:
        return {"actionId": self.action_id, "inputType": self.input_type}


@dataclass(frozen=True, slots=True)
class CanonicalInput:
    value: JsonValue
    digest: str | None = None
    encoding: str = "anc-canonical-json-v1"

    def __post_init__(self) -> None:
        if self.encoding != "anc-canonical-json-v1":
            raise ValueError("unsupported input encoding")
        validate_json_value(self.value)
        calculated = canonical_digest(self.value)
        if self.digest is None:
            object.__setattr__(self, "digest", calculated)
        elif _digest(self.digest) != calculated:
            raise ValueError("input digest does not match canonical value")

    def to_dict(self) -> dict[str, JsonValue]:
        return {"encoding": self.encoding, "digest": self.digest, "value": self.value}


@dataclass(frozen=True, slots=True)
class CapabilityRequirement:
    principal_id: str
    action_id: str
    object_scope: str

    def __post_init__(self) -> None:
        _identifier(self.principal_id, "principal")
        if self.action_id not in _ACTIONS:
            raise ValueError("capability action is not a frozen semantic action")
        _identifier(self.object_scope, "world_object")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "principalId": self.principal_id,
            "actionId": self.action_id,
            "objectScope": self.object_scope,
        }


@dataclass(frozen=True, slots=True)
class DeliverySemantics:
    idempotency: IdempotencyKind

    def to_dict(self) -> dict[str, JsonValue]:
        return {"idempotency": self.idempotency.value}


@dataclass(frozen=True, slots=True)
class ResultSemantics:
    execution: ExecutionKind
    completion: CompletionKind

    def __post_init__(self) -> None:
        if (
            self.execution is ExecutionKind.SYNCHRONOUS
            and self.completion is CompletionKind.TERMINAL_OBSERVATION
        ):
            raise ValueError(
                "synchronous execution cannot require asynchronous terminal observation"
            )

    def to_dict(self) -> dict[str, JsonValue]:
        return {"execution": self.execution.value, "completion": self.completion.value}


@dataclass(frozen=True, slots=True)
class VerificationPlan:
    method: str
    required_evidence: tuple[EvidenceKind, ...]

    def __post_init__(self) -> None:
        if not self.method.endswith(".v1"):
            raise ValueError("verification method must be versioned")
        if not self.required_evidence or len(set(self.required_evidence)) != len(
            self.required_evidence
        ):
            raise ValueError("verification evidence must be non-empty and unique")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "method": self.method,
            "requiredEvidence": [item.value for item in self.required_evidence],
        }


@dataclass(frozen=True, slots=True)
class EffectEnvelope:
    effect_id: str
    target: TargetRef
    mode: EffectMode
    action: SemanticAction
    input: CanonicalInput
    capability: CapabilityRequirement
    delivery: DeliverySemantics
    result: ResultSemantics
    verification: VerificationPlan
    schema_version: int = _SCHEMA_VERSION
    kind: str = _EFFECT_KIND

    def __post_init__(self) -> None:
        if self.schema_version != _SCHEMA_VERSION or self.kind != _EFFECT_KIND:
            raise ValueError("unsupported EffectEnvelope version or kind")
        _identifier(self.effect_id, "effect")
        if self.capability.action_id != self.action.action_id:
            raise ValueError("capability action must match Effect action")
        if self.capability.object_scope != self.target.object_id:
            raise ValueError("capability scope must match Effect target")
        expected_mode = (
            EffectMode.OBSERVE
            if self.action.action_id == "anc.object.read.v1"
            else EffectMode.CHANGE
        )
        if self.mode is not expected_mode:
            raise ValueError("Effect mode does not match semantic action")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": self.schema_version,
            "kind": self.kind,
            "effectId": self.effect_id,
            "target": self.target.to_dict(),
            "mode": self.mode.value,
            "action": self.action.to_dict(),
            "input": self.input.to_dict(),
            "capability": self.capability.to_dict(),
            "delivery": self.delivery.to_dict(),
            "result": self.result.to_dict(),
            "verification": self.verification.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "EffectEnvelope":
        _exact(
            value,
            {
                "schemaVersion",
                "kind",
                "effectId",
                "target",
                "mode",
                "action",
                "input",
                "capability",
                "delivery",
                "result",
                "verification",
            },
            "EffectEnvelope",
        )
        target = value["target"]
        action = value["action"]
        inp = value["input"]
        cap = value["capability"]
        delivery = value["delivery"]
        result = value["result"]
        verification = value["verification"]
        for item, label, keys in (
            (target, "target", {"objectId", "version"}),
            (action, "action", {"actionId", "inputType"}),
            (inp, "input", {"encoding", "digest", "value"}),
            (cap, "capability", {"principalId", "actionId", "objectScope"}),
            (delivery, "delivery", {"idempotency"}),
            (result, "result", {"execution", "completion"}),
            (verification, "verification", {"method", "requiredEvidence"}),
        ):
            if not isinstance(item, dict):
                raise ValueError(f"{label} must be an object")
            _exact(item, keys, label)
        return cls(
            schema_version=value["schemaVersion"],
            kind=value["kind"],
            effect_id=value["effectId"],
            target=TargetRef(target["objectId"], target["version"]),
            mode=EffectMode(value["mode"]),
            action=SemanticAction(action["actionId"], action["inputType"]),
            input=CanonicalInput(inp["value"], inp["digest"], inp["encoding"]),
            capability=CapabilityRequirement(
                cap["principalId"], cap["actionId"], cap["objectScope"]
            ),
            delivery=DeliverySemantics(IdempotencyKind(delivery["idempotency"])),
            result=ResultSemantics(
                ExecutionKind(result["execution"]),
                CompletionKind(result["completion"]),
            ),
            verification=VerificationPlan(
                verification["method"],
                tuple(EvidenceKind(item) for item in verification["requiredEvidence"]),
            ),
        )


@dataclass(frozen=True, slots=True)
class ProtocolAttestation:
    authority_id: str
    issuer_id: str
    principal_id: str
    role: str
    trust_domain: str
    policy_version: str
    key_id: str
    authority_signature: str
    kind: str
    contract_version: str
    subject_digest: str
    issued_at_ms: int
    signature: str

    def __post_init__(self) -> None:
        _identifier(self.authority_id, "authority")
        _identifier(self.issuer_id, "principal")
        _identifier(self.principal_id, "principal")
        _digest(self.subject_digest)
        if self.issued_at_ms < 0 or not self.role or not self.kind or not self.contract_version:
            raise ValueError("invalid protocol attestation")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "authorityId": self.authority_id,
            "issuerId": self.issuer_id,
            "principalId": self.principal_id,
            "role": self.role,
            "trustDomain": self.trust_domain,
            "policyVersion": self.policy_version,
            "keyId": self.key_id,
            "authoritySignature": self.authority_signature,
            "kind": self.kind,
            "contractVersion": self.contract_version,
            "subjectDigest": self.subject_digest,
            "issuedAtMs": self.issued_at_ms,
            "signature": self.signature,
        }


@dataclass(frozen=True, slots=True)
class SignedEffectEnvelope:
    envelope: EffectEnvelope
    attestation: ProtocolAttestation

    def __post_init__(self) -> None:
        if self.attestation.role != "effect" or self.attestation.kind != "effect_proposal":
            raise ValueError("EffectEnvelope requires Effect proposal authority")
        if self.attestation.subject_digest != effect_digest(self.envelope):
            raise ValueError("Effect attestation does not bind the envelope")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "envelope": self.envelope.to_dict(),
            "attestation": self.attestation.to_dict(),
        }


def effect_digest(effect: EffectEnvelope) -> str:
    return canonical_digest(effect.to_dict())


def encode_effect_envelope(effect: EffectEnvelope) -> bytes:
    return canonical_bytes(effect.to_dict())


def decode_effect_envelope(data: str | bytes) -> EffectEnvelope:
    value = loads_strict(data)
    if not isinstance(value, dict):
        raise ValueError("EffectEnvelope must be an object")
    return EffectEnvelope.from_dict(value)
