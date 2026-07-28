from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from anc_canonical import JsonValue, digest_text, validate_digest

from .model import (
    CanonicalInput,
    CapabilityRequirement,
    CompletionKind,
    DeliverySemantics,
    EffectEnvelope,
    EffectMode,
    EvidenceKind,
    ExecutionKind,
    IdempotencyKind,
    ResultSemantics,
    SemanticAction,
    TargetRef,
    VerificationPlan,
)


@dataclass(frozen=True, slots=True)
class SourceFileChange:
    relative_path: str
    expected_digest: str
    result_digest: str
    content: str

    def __post_init__(self) -> None:
        path = PurePosixPath(self.relative_path)
        if (
            not self.relative_path
            or path.is_absolute()
            or ".." in path.parts
            or self.relative_path != self.relative_path.strip()
        ):
            raise ValueError("source change path must be a safe relative path")
        validate_digest(self.expected_digest)
        if validate_digest(self.result_digest) != digest_text(self.content):
            raise ValueError("source change result digest does not match content")
        if len(self.content.encode("utf-8")) > 524_288:
            raise ValueError("source change content exceeds 512 KiB")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "relativePath": self.relative_path,
            "expectedDigest": self.expected_digest,
            "resultDigest": self.result_digest,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SourceFileChange:
        if set(value) != {
            "relativePath",
            "expectedDigest",
            "resultDigest",
            "content",
        } or any(not isinstance(item, str) for item in value.values()):
            raise ValueError("SourceFileChange fields differ")
        return cls(
            relative_path=value["relativePath"],
            expected_digest=value["expectedDigest"],
            result_digest=value["resultDigest"],
            content=value["content"],
        )


@dataclass(frozen=True, slots=True)
class SourceChangeSpec:
    repository_id: str
    base_revision: str
    files: tuple[SourceFileChange, ...]
    verification_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not self.repository_id.startswith("repository:")
            or self.repository_id != self.repository_id.strip()
        ):
            raise ValueError("source repository identity must start with repository:")
        if (
            len(self.base_revision) != 40
            or any(character not in "0123456789abcdef" for character in self.base_revision)
        ):
            raise ValueError("source base revision must be a lowercase Git object id")
        if not 1 <= len(self.files) <= 8:
            raise ValueError("source change requires 1 to 8 files")
        if len({item.relative_path for item in self.files}) != len(self.files):
            raise ValueError("source change file paths must be unique")
        if not 1 <= len(self.verification_ids) <= 8:
            raise ValueError("source change requires 1 to 8 verification identities")
        if len(set(self.verification_ids)) != len(self.verification_ids):
            raise ValueError("source verification identities must be unique")
        if any(not item or item != item.strip() for item in self.verification_ids):
            raise ValueError("source verification identities must be non-empty")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "repositoryId": self.repository_id,
            "baseRevision": self.base_revision,
            "files": [item.to_dict() for item in self.files],
            "verificationIds": list(self.verification_ids),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SourceChangeSpec:
        if set(value) != {
            "repositoryId",
            "baseRevision",
            "files",
            "verificationIds",
        }:
            raise ValueError("SourceChangeSpec fields differ")
        files = value["files"]
        verification_ids = value["verificationIds"]
        if (
            not isinstance(value["repositoryId"], str)
            or not isinstance(value["baseRevision"], str)
            or not isinstance(files, list)
            or any(not isinstance(item, dict) for item in files)
            or not isinstance(verification_ids, list)
            or any(not isinstance(item, str) for item in verification_ids)
        ):
            raise ValueError("SourceChangeSpec field types are invalid")
        return cls(
            repository_id=value["repositoryId"],
            base_revision=value["baseRevision"],
            files=tuple(SourceFileChange.from_dict(item) for item in files),
            verification_ids=tuple(verification_ids),
        )


def source_change_effect(
    *,
    effect_id: str,
    principal_id: str,
    spec: SourceChangeSpec,
) -> EffectEnvelope:
    action = "anc.source.change.v1"
    target = TargetRef(f"world_object:{spec.repository_id}")
    return EffectEnvelope(
        effect_id=effect_id,
        target=target,
        mode=EffectMode.CHANGE,
        action=SemanticAction(action, "anc.source-change-input.v1"),
        input=CanonicalInput(spec.to_dict()),
        capability=CapabilityRequirement(principal_id, action, target.object_id),
        delivery=DeliverySemantics(IdempotencyKind.NONE),
        result=ResultSemantics(
            ExecutionKind.ASYNCHRONOUS,
            CompletionKind.ACCEPTED_VERIFICATION,
        ),
        verification=VerificationPlan(
            "source-files-structured-diff-and-checks.v1",
            (EvidenceKind.OBSERVATION, EvidenceKind.ARTIFACT),
        ),
    )
