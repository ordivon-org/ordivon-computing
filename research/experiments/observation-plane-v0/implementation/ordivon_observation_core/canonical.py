from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any, TypeAlias

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]

_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,127}$")
_NAMESPACED_KIND_RE = re.compile(
    r"^[a-z][a-z0-9]*(?:[.-][a-z0-9][a-z0-9_-]*)+$"
)
_FORBIDDEN_EXACT_KEYS = {
    "authorization",
    "api_key",
    "apikey",
    "access_token",
    "accesstoken",
    "refresh_token",
    "refreshtoken",
    "credential",
    "credentials",
    "password",
    "passwd",
    "secret",
    "private_reasoning",
    "chain_of_thought",
    "raw_prompt",
    "model_output",
    "tool_payload",
    "stdout",
    "stderr",
}
_FORBIDDEN_SUFFIXES = (
    "_api_key",
    "_access_token",
    "_refresh_token",
    "_password",
    "_passwd",
    "_secret",
    "_credential",
)


class CanonicalValueError(ValueError):
    pass


def validate_json(value: Any, *, label: str = "JSON value", depth: int = 0) -> None:
    if depth > 24:
        raise CanonicalValueError(f"{label} exceeds the maximum nesting depth")
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalValueError(f"{label} contains a non-finite number")
        return
    if isinstance(value, list):
        if len(value) > 1_024:
            raise CanonicalValueError(f"{label} contains too many array items")
        for item in value:
            validate_json(item, label=label, depth=depth + 1)
        return
    if isinstance(value, dict):
        if len(value) > 1_024:
            raise CanonicalValueError(f"{label} contains too many object fields")
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalValueError(f"{label} object keys must be strings")
            validate_json(item, label=label, depth=depth + 1)
        return
    raise CanonicalValueError(f"{label} contains unsupported type {type(value).__name__}")


def canonical_bytes(value: JsonValue) -> bytes:
    validate_json(value)
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CanonicalValueError("value is not canonical JSON") from error


def canonical_digest(value: JsonValue) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def exact_object(
    value: Any,
    *,
    required: set[str],
    optional: set[str] = frozenset(),
    label: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CanonicalValueError(f"{label} must be an object")
    fields = set(value)
    missing = required - fields
    unknown = fields - required - optional
    if missing or unknown:
        raise CanonicalValueError(
            f"{label} fields differ: missing={sorted(missing)} unknown={sorted(unknown)}"
        )
    return value


def bounded_text(
    value: Any,
    *,
    label: str,
    max_bytes: int = 1_024,
    allow_empty: bool = False,
) -> str:
    if not isinstance(value, str) or value != value.strip():
        raise CanonicalValueError(f"{label} must be a trimmed string")
    if not value and not allow_empty:
        raise CanonicalValueError(f"{label} must be non-empty")
    if len(value.encode("utf-8")) > max_bytes:
        raise CanonicalValueError(f"{label} exceeds {max_bytes} UTF-8 bytes")
    return value


def digest(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or _DIGEST_RE.fullmatch(value) is None:
        raise CanonicalValueError(f"{label} must be sha256:<64 lowercase hex>")
    return value


def namespaced_kind(value: Any, *, label: str) -> str:
    text = bounded_text(value, label=label, max_bytes=256)
    if _NAMESPACED_KIND_RE.fullmatch(text) is None:
        raise CanonicalValueError(f"{label} must be a bounded namespaced kind")
    return text


def attribute_key(value: Any, *, label: str) -> str:
    text = bounded_text(value, label=label, max_bytes=128)
    if _KEY_RE.fullmatch(text) is None:
        raise CanonicalValueError(f"{label} is not a supported attribute key")
    normalized = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    if normalized in _FORBIDDEN_EXACT_KEYS or normalized.endswith(_FORBIDDEN_SUFFIXES):
        raise CanonicalValueError(f"{label} is forbidden by the metadata-only policy")
    return text


def scalar(value: Any, *, label: str, max_string_bytes: int = 2_048) -> JsonScalar:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalValueError(f"{label} must be finite")
        return value
    if isinstance(value, str):
        return bounded_text(
            value,
            label=label,
            max_bytes=max_string_bytes,
            allow_empty=True,
        )
    raise CanonicalValueError(f"{label} must be a JSON scalar")


def scalar_map(
    value: Any,
    *,
    label: str,
    max_fields: int = 128,
    max_bytes: int = 16_384,
) -> dict[str, JsonScalar | list[JsonScalar]]:
    if not isinstance(value, dict) or len(value) > max_fields:
        raise CanonicalValueError(f"{label} must be a bounded object")
    result: dict[str, JsonScalar | list[JsonScalar]] = {}
    for key, item in value.items():
        checked_key = attribute_key(key, label=f"{label} key")
        if isinstance(item, list):
            if len(item) > 32:
                raise CanonicalValueError(f"{label}.{checked_key} contains too many values")
            result[checked_key] = [
                scalar(entry, label=f"{label}.{checked_key}") for entry in item
            ]
        else:
            result[checked_key] = scalar(item, label=f"{label}.{checked_key}")
    if len(canonical_bytes(result)) > max_bytes:
        raise CanonicalValueError(f"{label} exceeds {max_bytes} canonical bytes")
    return result


__all__ = [
    "CanonicalValueError",
    "JsonScalar",
    "JsonValue",
    "attribute_key",
    "bounded_text",
    "canonical_bytes",
    "canonical_digest",
    "digest",
    "exact_object",
    "namespaced_kind",
    "scalar",
    "scalar_map",
    "sha256_bytes",
    "validate_json",
]
