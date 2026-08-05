from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_text(value: Any) -> str:
    return canonical_bytes(value).decode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def file_digest(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def with_integrity(document: dict[str, Any]) -> dict[str, Any]:
    result = dict(document)
    result["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evaluation-data-json-v1",
        "payloadDigest": sha256_value(document),
    }
    return result


def validate_integrity(document: dict[str, Any]) -> None:
    integrity = document.get("integrity")
    if not isinstance(integrity, dict):
        raise ValueError("projection manifest integrity must be an object")
    if set(integrity) != {"algorithm", "canonicalization", "payloadDigest"}:
        raise ValueError("projection manifest integrity fields differ")
    if integrity["algorithm"] != "sha256":
        raise ValueError("unsupported projection manifest integrity algorithm")
    if integrity["canonicalization"] != "ordivon-evaluation-data-json-v1":
        raise ValueError("unsupported projection manifest canonicalization")
    payload = {key: value for key, value in document.items() if key != "integrity"}
    expected = sha256_value(payload)
    if integrity["payloadDigest"] != expected:
        raise ValueError(
            "projection manifest payload digest differs; "
            f"expected={expected}, observed={integrity['payloadDigest']}"
        )


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
