from __future__ import annotations

import os
from pathlib import Path

from anc_canonical import JsonValue, canonical_bytes, canonical_digest, loads_strict

from .model import SemanticRef, TaskCapsule, capsule_digest


class ObjectStoreError(RuntimeError):
    pass


class ObjectMissing(ObjectStoreError):
    pass


class ObjectCorrupt(ObjectStoreError):
    pass


class FileObjectStore:
    """Minimal content-addressed JSON store for semantic references and capsules."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, value: JsonValue) -> str:
        digest = canonical_digest(value)
        payload = canonical_bytes(value)
        path = self._path(digest)
        if path.exists():
            if path.read_bytes() != payload:
                raise ObjectCorrupt("content address maps to different bytes")
            return digest
        temporary = path.with_suffix(f".tmp-{os.getpid()}")
        temporary.write_bytes(payload)
        os.replace(temporary, path)
        return digest

    def get(self, digest: str) -> JsonValue:
        path = self._path(digest)
        if not path.exists():
            raise ObjectMissing(f"content-addressed object is missing: {digest}")
        try:
            value = loads_strict(path.read_bytes())
        except (OSError, ValueError) as error:
            raise ObjectCorrupt(f"object cannot be decoded: {digest}") from error
        if canonical_digest(value) != digest:
            raise ObjectCorrupt("object content does not match its address")
        return value

    def put_semantic(self, kind: str, semantic_id: str, payload: JsonValue) -> SemanticRef:
        value: JsonValue = {
            "schemaVersion": 1,
            "kind": kind,
            "semanticId": semantic_id,
            "payload": payload,
        }
        return SemanticRef(kind, semantic_id, self.put(value))

    def resolve_semantic(self, ref: SemanticRef) -> JsonValue:
        value = self.get(ref.digest)
        if not isinstance(value, dict):
            raise ObjectCorrupt("semantic reference does not resolve to an object")
        expected = {"schemaVersion", "kind", "semanticId", "payload"}
        if set(value) != expected:
            raise ObjectCorrupt("semantic reference object fields differ")
        if value["schemaVersion"] != 1:
            raise ObjectCorrupt("semantic reference schema is unsupported")
        if value["kind"] != ref.kind or value["semanticId"] != ref.semantic_id:
            raise ObjectCorrupt("semantic reference identity differs from stored object")
        return value["payload"]

    def put_capsule(self, capsule: TaskCapsule) -> str:
        digest = self.put(capsule.to_dict())
        if digest != capsule_digest(capsule):
            raise ObjectCorrupt("TaskCapsule store changed the capsule digest")
        return digest

    def get_capsule(self, digest: str) -> TaskCapsule:
        value = self.get(digest)
        if not isinstance(value, dict):
            raise ObjectCorrupt("TaskCapsule object must be a JSON object")
        try:
            capsule = TaskCapsule.from_dict(value)
        except ValueError as error:
            raise ObjectCorrupt("TaskCapsule object is invalid") from error
        if capsule_digest(capsule) != digest:
            raise ObjectCorrupt("TaskCapsule digest differs from its content address")
        return capsule

    def _path(self, digest: str) -> Path:
        if (
            len(digest) != 71
            or not digest.startswith("sha256:")
            or any(ch not in "0123456789abcdef" for ch in digest[7:])
        ):
            raise ValueError("object store key must be a sha256 digest")
        return self.root / f"{digest[7:]}.json"
