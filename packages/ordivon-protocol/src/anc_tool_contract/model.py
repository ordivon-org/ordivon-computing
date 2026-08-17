from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from anc_canonical import JsonValue, canonical_digest, validate_json_value
from anc_protocol_types import CompletionKind, ExecutionKind

_ALLOWED_SCHEMA = {
    "type",
    "properties",
    "required",
    "additionalProperties",
    "patternProperties",
    "const",
    "enum",
    "minimum",
    "maximum",
    "minLength",
    "maxLength",
    "minItems",
    "maxItems",
    "pattern",
    "format",
    "default",
    "$defs",
    "$ref",
    "oneOf",
    "anyOf",
    "allOf",
    "items",
}
_PRESENTATION = {"title", "description", "examples", "$comment", "$schema"}


class EffectClass(StrEnum):
    OBSERVE = "observe"
    CHANGE = "change"
    OPAQUE = "opaque"


class IdempotencySupport(StrEnum):
    NONE = "none"
    NATURAL = "natural"
    KEYED = "keyed"


class CorrelationKind(StrEnum):
    RECEIPT = "receipt"
    STABLE_KEY = "stable-key"
    NONE = "none"


class CancellationKind(StrEnum):
    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"


class ContractChange(StrEnum):
    IDENTICAL = "identical"
    COMPATIBLE_EXTENSION = "compatible-extension"
    CALLER_ADAPTATION = "caller-adaptation"
    SEMANTIC_BREAK = "semantic-break"
    CAPABILITY_CHANGE = "capability-change"
    COMPLETION_CHANGE = "completion-change"
    UNKNOWN = "unknown"


def _nonempty(value: str, label: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{label} must be non-empty and trimmed")
    return value


def _strip_schema(value: Any, *, path: str = "$") -> JsonValue:
    if isinstance(value, list):
        return [_strip_schema(item, path=f"{path}[]") for item in value]
    if not isinstance(value, dict):
        validate_json_value(value)
        return value
    result: dict[str, JsonValue] = {}
    for key, item in value.items():
        if key in _PRESENTATION:
            continue
        if (
            path.endswith(".properties")
            or path.endswith(".$defs")
            or path.endswith(".patternProperties")
        ):
            result[key] = _strip_schema(item, path=f"{path}.{key}")
            continue
        if key not in _ALLOWED_SCHEMA:
            raise ValueError(f"unsupported JSON Schema keyword {key} at {path}")
        if key in {"properties", "$defs", "patternProperties"}:
            if not isinstance(item, dict):
                raise ValueError(f"{key} must be an object")
            result[key] = {
                name: _strip_schema(schema, path=f"{path}.{key}")
                for name, schema in item.items()
            }
        elif key in {"oneOf", "anyOf", "allOf"}:
            if not isinstance(item, list):
                raise ValueError(f"{key} must be an array")
            result[key] = [
                _strip_schema(schema, path=f"{path}.{key}") for schema in item
            ]
        elif key == "items":
            result[key] = _strip_schema(item, path=f"{path}.items")
        else:
            validate_json_value(item)
            result[key] = item
    return result


@dataclass(frozen=True, slots=True)
class ToolContract:
    contract_id: str
    revision: str
    provider_id: str
    operation: str
    semantic_action: str
    input_schema: JsonValue
    output_schema: JsonValue
    execution: ExecutionKind
    completion: CompletionKind
    effect_class: EffectClass
    idempotency_support: IdempotencySupport
    correlation: CorrelationKind
    cancellation: CancellationKind
    evidence: tuple[str, ...]
    capability_class: str
    schema_version: int = 1
    kind: str = "anc.tool-contract"

    def __post_init__(self) -> None:
        for value, label in (
            (self.contract_id, "contract id"),
            (self.revision, "revision"),
            (self.provider_id, "provider id"),
            (self.operation, "operation"),
            (self.semantic_action, "semantic action"),
            (self.capability_class, "capability class"),
        ):
            _nonempty(value, label)
        if self.schema_version != 1 or self.kind != "anc.tool-contract":
            raise ValueError("unsupported ToolContract version or kind")
        object.__setattr__(
            self, "input_schema", _strip_schema(self.input_schema, path="$.inputSchema")
        )
        object.__setattr__(
            self, "output_schema", _strip_schema(self.output_schema, path="$.outputSchema")
        )
        if not self.evidence or len(set(self.evidence)) != len(self.evidence):
            raise ValueError("evidence affordances must be non-empty and unique")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": self.schema_version,
            "kind": self.kind,
            "contractId": self.contract_id,
            "revision": self.revision,
            "providerId": self.provider_id,
            "operation": self.operation,
            "semanticAction": self.semantic_action,
            "inputSchema": self.input_schema,
            "outputSchema": self.output_schema,
            "execution": self.execution.value,
            "completion": self.completion.value,
            "effectClass": self.effect_class.value,
            "idempotencySupport": self.idempotency_support.value,
            "correlation": self.correlation.value,
            "cancellation": self.cancellation.value,
            "evidence": list(self.evidence),
            "capabilityClass": self.capability_class,
        }


def normalize_tool_contract(raw: dict[str, Any]) -> ToolContract:
    expected = {
        "schemaVersion",
        "providerId",
        "revision",
        "name",
        "inputSchema",
        "outputSchema",
        "semantics",
    }
    optional = {"description", "title"}
    if not set(raw).issubset(expected | optional) or not expected.issubset(raw):
        raise ValueError("raw Tool descriptor fields are unsupported or incomplete")
    if raw["schemaVersion"] != 1:
        raise ValueError("unsupported raw descriptor version")
    semantics = raw["semantics"]
    semantic_keys = {
        "semanticAction",
        "execution",
        "completion",
        "effectClass",
        "idempotencySupport",
        "correlation",
        "cancellation",
        "evidence",
        "capabilityClass",
    }
    if not isinstance(semantics, dict) or set(semantics) != semantic_keys:
        raise ValueError("Tool semantic profile is incomplete")
    provider = _nonempty(raw["providerId"], "provider id")
    name = _nonempty(raw["name"], "operation")
    return ToolContract(
        contract_id=f"tool-contract:{provider}/{name}",
        revision=raw["revision"],
        provider_id=provider,
        operation=name,
        semantic_action=semantics["semanticAction"],
        input_schema=raw["inputSchema"],
        output_schema=raw["outputSchema"],
        execution=ExecutionKind(semantics["execution"]),
        completion=CompletionKind(semantics["completion"]),
        effect_class=EffectClass(semantics["effectClass"]),
        idempotency_support=IdempotencySupport(semantics["idempotencySupport"]),
        correlation=CorrelationKind(semantics["correlation"]),
        cancellation=CancellationKind(semantics["cancellation"]),
        evidence=tuple(semantics["evidence"]),
        capability_class=semantics["capabilityClass"],
    )


def normalize_mcp_tool_contract(
    tool: dict[str, Any],
    *,
    provider_id: str,
    revision: str,
    semantics: dict[str, Any],
) -> ToolContract:
    if not isinstance(tool, dict):
        raise ValueError("MCP Tool descriptor must be an object")
    allowed = {
        "name",
        "description",
        "title",
        "inputSchema",
        "outputSchema",
        "annotations",
        "execution",
    }
    if not set(tool).issubset(allowed):
        raise ValueError("MCP Tool descriptor contains unsupported fields")
    name = tool.get("name")
    input_schema = tool.get("inputSchema")
    if not isinstance(name, str) or not name:
        raise ValueError("MCP Tool descriptor has no operation name")
    if not isinstance(input_schema, dict):
        raise ValueError("MCP Tool descriptor has no input schema")
    execution = tool.get("execution")
    if execution is not None:
        if not isinstance(execution, dict) or set(execution) != {"taskSupport"}:
            raise ValueError("MCP Tool execution metadata is unsupported")
        if execution["taskSupport"] not in {"forbidden", "optional", "required"}:
            raise ValueError("MCP Tool taskSupport value is unsupported")
    return normalize_tool_contract(
        {
            "schemaVersion": 1,
            "providerId": provider_id,
            "revision": revision,
            "name": name,
            "description": tool.get("description", ""),
            "inputSchema": input_schema,
            "outputSchema": tool.get("outputSchema"),
            "semantics": semantics,
        }
    )


def contract_digest(contract: ToolContract) -> str:
    return canonical_digest(contract.to_dict())


def _properties(schema: JsonValue) -> tuple[dict[str, Any], set[str]] | None:
    if not isinstance(schema, dict) or schema.get("type") != "object":
        return None
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    if not isinstance(properties, dict):
        return None
    return properties, required


def _optional_extension(old: JsonValue, new: JsonValue) -> bool:
    left = _properties(old)
    right = _properties(new)
    if left is None or right is None:
        return False
    old_properties, old_required = left
    new_properties, new_required = right
    if old_required != new_required or not set(old_properties).issubset(new_properties):
        return False
    return all(old_properties[key] == new_properties[key] for key in old_properties) and all(
        key not in new_required for key in set(new_properties) - set(old_properties)
    )


def _schema_version_adaptation(old: JsonValue, new: JsonValue) -> bool:
    left = _properties(old)
    right = _properties(new)
    if left is None or right is None:
        return False
    old_properties, old_required = left
    new_properties, new_required = right
    if (
        set(old_properties) != set(new_properties)
        or old_required != new_required
        or "schemaVersion" not in old_properties
    ):
        return False
    for key in old_properties:
        if key != "schemaVersion" and old_properties[key] != new_properties[key]:
            return False
    before = old_properties["schemaVersion"]
    after = new_properties["schemaVersion"]
    return (
        before != after
        and isinstance(before, dict)
        and isinstance(after, dict)
        and before.get("type") == "integer"
        and after.get("const") == 1
        and after.get("default", 1) == 1
    )


def classify_contract_change(old: ToolContract, new: ToolContract) -> ContractChange:
    if contract_digest(old) == contract_digest(new):
        return ContractChange.IDENTICAL
    if old.semantic_action != new.semantic_action or old.effect_class != new.effect_class:
        return ContractChange.SEMANTIC_BREAK
    if old.capability_class != new.capability_class:
        return ContractChange.CAPABILITY_CHANGE
    if (
        old.execution,
        old.completion,
        old.correlation,
        old.cancellation,
    ) != (
        new.execution,
        new.completion,
        new.correlation,
        new.cancellation,
    ):
        return ContractChange.COMPLETION_CHANGE
    if old.idempotency_support != new.idempotency_support:
        return ContractChange.CAPABILITY_CHANGE
    if _schema_version_adaptation(old.input_schema, new.input_schema):
        return ContractChange.CALLER_ADAPTATION
    if _optional_extension(old.input_schema, new.input_schema) and (
        old.output_schema == new.output_schema
        or _optional_extension(old.output_schema, new.output_schema)
    ):
        return ContractChange.COMPATIBLE_EXTENSION
    if old.input_schema == new.input_schema and _optional_extension(
        old.output_schema, new.output_schema
    ):
        return ContractChange.COMPATIBLE_EXTENSION
    return ContractChange.UNKNOWN
