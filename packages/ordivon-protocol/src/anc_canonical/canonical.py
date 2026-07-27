from __future__ import annotations

import hashlib
import json
from typing import TypeAlias

JsonScalar: TypeAlias = None | bool | int | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


class CanonicalError(ValueError):
    pass


def _reject_number(value: str):
    raise CanonicalError(f"non-integer JSON number is forbidden: {value}")


def _pairs(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def loads_strict(data: str | bytes) -> JsonValue:
    try:
        value = json.loads(
            data,
            object_pairs_hook=_pairs,
            parse_float=_reject_number,
            parse_constant=_reject_number,
        )
    except json.JSONDecodeError as error:
        raise CanonicalError("invalid JSON") from error
    validate_json_value(value)
    return value


def validate_json_value(value: object, *, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, int, str)):
        if isinstance(value, str) and any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
            raise CanonicalError(f"unpaired Unicode surrogate at {path}")
        return
    if isinstance(value, float):
        raise CanonicalError(f"floating-point values are forbidden at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            validate_json_value(item, path=f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalError(f"JSON object key is not a string at {path}")
            validate_json_value(key, path=f"{path}.<key>")
            validate_json_value(item, path=f"{path}.{key}")
        return
    raise CanonicalError(f"unsupported JSON value {type(value).__name__} at {path}")


def canonical_bytes(value: JsonValue) -> bytes:
    validate_json_value(value)
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_text(value: JsonValue) -> str:
    return canonical_bytes(value).decode("utf-8")


def canonical_digest(value: JsonValue) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()
