from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import re

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ContentIdentityError(ValueError):
    pass


def _value(record: Any, *names: str) -> Any:
    if isinstance(record, dict):
        for name in names:
            if name in record:
                return record[name]
    for name in names:
        if hasattr(record, name):
            return getattr(record, name)
    raise ContentIdentityError(f"missing content field: {'/'.join(names)}")


def canonical_sha256(value: str, *, bare_allowed: bool) -> str:
    if not isinstance(value, str):
        raise ContentIdentityError("content digest must be a string")
    if value.startswith("sha256:"):
        hexadecimal = value.removeprefix("sha256:")
    elif bare_allowed:
        hexadecimal = value
    else:
        raise ContentIdentityError("content digest must use sha256:<lowercase-hex>")
    if not _SHA256.fullmatch(hexadecimal):
        raise ContentIdentityError("content digest must contain 64 lowercase SHA-256 hex characters")
    return "sha256:" + hexadecimal


def byte_length(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ContentIdentityError("content byte length must be a non-negative integer")
    return value


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Identity of one exact byte sequence, with no owner or storage semantics."""

    digest: str
    byte_length: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "digest", canonical_sha256(self.digest, bare_allowed=False))
        object.__setattr__(self, "byte_length", byte_length(self.byte_length))

    def to_dict(self) -> dict[str, object]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.content-identity",
            "digest": self.digest,
            "byteLength": self.byte_length,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ContentIdentity":
        expected = {"schemaVersion", "kind", "digest", "byteLength"}
        if set(value) != expected:
            raise ContentIdentityError("ContentIdentity fields differ")
        if value["schemaVersion"] != 1 or value["kind"] != "ordivon.content-identity":
            raise ContentIdentityError("ContentIdentity version or kind is unsupported")
        return cls(digest=value["digest"], byte_length=value["byteLength"])


def from_runtime_artifact(record: Any) -> ContentIdentity:
    return ContentIdentity(
        digest=canonical_sha256(_value(record, "digest"), bare_allowed=False),
        byte_length=byte_length(_value(record, "retainedBytes", "retained_bytes")),
    )


def from_finance_evidence(record: Any) -> ContentIdentity:
    algorithm = _value(record, "algorithm")
    if algorithm != "sha256":
        raise ContentIdentityError("Finance EvidenceArtifact algorithm must be sha256")
    return ContentIdentity(
        digest=canonical_sha256(_value(record, "digest"), bare_allowed=True),
        byte_length=byte_length(_value(record, "byteLength", "byte_length")),
    )


def from_security_sample(record: Any) -> ContentIdentity:
    return ContentIdentity(
        digest=canonical_sha256(_value(record, "sha256"), bare_allowed=False),
        byte_length=byte_length(_value(record, "byteLength", "byte_length")),
    )


def from_studio_blob(record: Any) -> ContentIdentity:
    return ContentIdentity(
        digest=canonical_sha256(_value(record, "digest"), bare_allowed=False),
        byte_length=byte_length(_value(record, "sizeBytes", "size_bytes")),
    )


def from_world_artifact(record: Any) -> ContentIdentity:
    return ContentIdentity(
        digest=canonical_sha256(_value(record, "sha256"), bare_allowed=True),
        byte_length=byte_length(_value(record, "bytes")),
    )


_OWNER_PROJECTORS = {
    "runtime": from_runtime_artifact,
    "finance": from_finance_evidence,
    "security": from_security_sample,
    "studio": from_studio_blob,
    "world": from_world_artifact,
}


def project_owner_content(owner: str, record: Any) -> ContentIdentity:
    try:
        projector = _OWNER_PROJECTORS[owner]
    except KeyError as error:
        raise ContentIdentityError(f"unsupported content owner: {owner}") from error
    return projector(record)


def require_same_content(records: dict[str, Any]) -> ContentIdentity:
    if not records:
        raise ContentIdentityError("at least one owner record is required")
    projected = {owner: project_owner_content(owner, record) for owner, record in records.items()}
    identities = set(projected.values())
    if len(identities) != 1:
        detail = ", ".join(
            f"{owner}={identity.digest}@{identity.byte_length}" for owner, identity in sorted(projected.items())
        )
        raise ContentIdentityError(f"owner content identities differ: {detail}")
    return next(iter(identities))
