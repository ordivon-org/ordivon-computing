"""Parse the deliberately small YAML subset used by Ordivon content manifests.

The subset supports a flat mapping, scalar values, inline lists, and indented
block lists. It intentionally rejects nested mappings, anchors, tags, and other
features that would make the P0 contract depend on a general YAML runtime.
"""

from __future__ import annotations

import ast
import json
import re
from typing import Any


_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


def _scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value):
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            body = value[1:-1].strip()
            if not body:
                return []
            parsed = [_scalar(part) for part in body.split(",")]
        if not isinstance(parsed, list):
            raise ValueError("inline YAML value must be a list")
        return parsed
    if value[0:1] in {"'", '"'}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as error:
            raise ValueError(f"invalid quoted YAML scalar: {value}") from error
        if not isinstance(parsed, str):
            raise ValueError("quoted YAML scalar must be text")
        return parsed
    return value


def loads(text: str) -> dict[str, Any]:
    document: dict[str, Any] = {}
    list_key: str | None = None
    for number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if line.startswith("- "):
            if list_key is None or indent == 0:
                raise ValueError(f"line {number}: list item has no parent key")
            document[list_key].append(_scalar(line[2:]))
            continue
        if indent:
            raise ValueError(f"line {number}: nested mappings are not supported")
        key, separator, raw_value = line.partition(":")
        if not separator or not _KEY.fullmatch(key):
            raise ValueError(f"line {number}: invalid mapping entry")
        if key in document:
            raise ValueError(f"line {number}: duplicate key {key}")
        if raw_value.strip():
            document[key] = _scalar(raw_value)
            list_key = None
        else:
            document[key] = []
            list_key = key
    return document
