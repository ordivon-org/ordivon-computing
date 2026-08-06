from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from typing import Any, Iterable
import uuid

from .canonical import (
    JsonValue,
    bounded_text,
    canonical_bytes,
    canonical_digest,
    digest,
    exact_object,
)
from .contract import (
    ObservationBatch,
    ObservationContractError,
    ObservationProducerIdentity,
)

CHECKPOINT_KIND = "ordivon.observation-export-checkpoint"
BUNDLE_KIND = "ordivon.observation-export-bundle"
_EXPORT_SCHEMA_VERSION = 1
_REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


class ObservationExportError(RuntimeError):
    pass


class ObservationCheckpointConflict(ObservationExportError):
    pass


class ObservationCheckpointCorrupt(ObservationExportError):
    pass


class ObservationBundleConflict(ObservationExportError):
    pass


def _revision(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or _REVISION_RE.fullmatch(value) is None:
        raise ObservationContractError(f"{label} must be an exact 40-character Git revision")
    return value


def _non_negative_int(value: Any, *, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ObservationContractError(f"{label} must be a non-negative integer")
    return value


def _streams(value: Any) -> dict[str, int]:
    if not isinstance(value, dict) or len(value) > 1_000_000:
        raise ObservationContractError("checkpoint streams must be a bounded object")
    result: dict[str, int] = {}
    for key, sequence in value.items():
        stream_id = bounded_text(key, label="checkpoint streamId", max_bytes=1_024)
        result[stream_id] = _non_negative_int(
            sequence, label=f"checkpoint sequence for {stream_id}"
        )
    return result


@dataclass(frozen=True, slots=True)
class ObservationExportCheckpoint:
    producer_identity: ObservationProducerIdentity
    mapping_version: str
    streams: dict[str, int]
    updated_at_ms: int
    integrity_digest: str

    def __post_init__(self) -> None:
        try:
            bounded_text(
                self.mapping_version,
                label="checkpoint mappingVersion",
                max_bytes=128,
            )
            checked_streams = _streams(self.streams)
            _non_negative_int(self.updated_at_ms, label="checkpoint updatedAtMs")
            digest(self.integrity_digest, label="checkpoint payloadDigest")
        except ValueError as error:
            if isinstance(error, ObservationContractError):
                raise
            raise ObservationContractError(str(error)) from error
        if checked_streams != self.streams:
            raise ObservationContractError("checkpoint streams differ after validation")
        if self.integrity_digest != canonical_digest(self._payload_dict()):
            raise ObservationCheckpointCorrupt("checkpoint integrity differs")

    @classmethod
    def build(
        cls,
        *,
        producer_identity: ObservationProducerIdentity,
        mapping_version: str,
        streams: dict[str, int],
        updated_at_ms: int,
    ) -> "ObservationExportCheckpoint":
        provisional = cls.__new__(cls)
        values = {
            "producer_identity": producer_identity,
            "mapping_version": mapping_version,
            "streams": dict(streams),
            "updated_at_ms": updated_at_ms,
            "integrity_digest": "sha256:" + "0" * 64,
        }
        for key, value in values.items():
            object.__setattr__(provisional, key, value)
        values["integrity_digest"] = canonical_digest(provisional._payload_dict())
        return cls(**values)

    @classmethod
    def empty(
        cls,
        *,
        producer_identity: ObservationProducerIdentity,
        mapping_version: str,
    ) -> "ObservationExportCheckpoint":
        return cls.build(
            producer_identity=producer_identity,
            mapping_version=mapping_version,
            streams={},
            updated_at_ms=0,
        )

    def sequence(self, stream_id: str) -> int:
        return self.streams.get(stream_id, 0)

    def advance(
        self,
        updates: dict[str, int],
        *,
        updated_at_ms: int,
    ) -> "ObservationExportCheckpoint":
        next_streams = dict(self.streams)
        for stream_id, sequence in _streams(updates).items():
            previous = next_streams.get(stream_id, 0)
            if sequence < previous:
                raise ObservationCheckpointConflict(
                    f"checkpoint stream {stream_id} cannot move backward"
                )
            next_streams[stream_id] = sequence
        return ObservationExportCheckpoint.build(
            producer_identity=self.producer_identity,
            mapping_version=self.mapping_version,
            streams=next_streams,
            updated_at_ms=updated_at_ms,
        )

    def _payload_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": _EXPORT_SCHEMA_VERSION,
            "kind": CHECKPOINT_KIND,
            "producerIdentity": self.producer_identity.to_dict(),
            "mappingVersion": self.mapping_version,
            "streams": dict(sorted(self.streams.items())),
            "updatedAtMs": self.updated_at_ms,
        }

    def to_dict(self) -> dict[str, JsonValue]:
        value = self._payload_dict()
        value["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": self.integrity_digest,
        }
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationExportCheckpoint":
        try:
            item = exact_object(
                value,
                required={
                    "schemaVersion",
                    "kind",
                    "producerIdentity",
                    "mappingVersion",
                    "streams",
                    "updatedAtMs",
                    "integrity",
                },
                label="ObservationExportCheckpoint",
            )
            if item["schemaVersion"] != _EXPORT_SCHEMA_VERSION or item["kind"] != CHECKPOINT_KIND:
                raise ObservationCheckpointCorrupt(
                    "unsupported Observation checkpoint version or kind"
                )
            integrity = exact_object(
                item["integrity"],
                required={"algorithm", "canonicalization", "payloadDigest"},
                label="ObservationExportCheckpoint integrity",
            )
            if (
                integrity["algorithm"] != "sha256"
                or integrity["canonicalization"] != "ordivon-evidence-json-v1"
            ):
                raise ObservationCheckpointCorrupt(
                    "unsupported Observation checkpoint integrity"
                )
            return cls(
                producer_identity=ObservationProducerIdentity.from_dict(
                    item["producerIdentity"]
                ),
                mapping_version=item["mappingVersion"],
                streams=_streams(item["streams"]),
                updated_at_ms=item["updatedAtMs"],
                integrity_digest=integrity["payloadDigest"],
            )
        except ObservationExportError:
            raise
        except ValueError as error:
            raise ObservationCheckpointCorrupt(str(error)) from error


@dataclass(frozen=True, slots=True)
class ObservationExportBundle:
    producer_identity: ObservationProducerIdentity
    mapping_version: str
    owner_revision: str
    exporter_revision: str
    exported_at_ms: int
    checkpoint_before_digest: str
    checkpoint_after_digest: str
    batches: tuple[ObservationBatch, ...]
    integrity_digest: str

    def __post_init__(self) -> None:
        try:
            bounded_text(
                self.mapping_version,
                label="bundle mappingVersion",
                max_bytes=128,
            )
            _revision(self.owner_revision, label="ownerRevision")
            _revision(self.exporter_revision, label="exporterRevision")
            _non_negative_int(self.exported_at_ms, label="exportedAtMs")
            digest(self.checkpoint_before_digest, label="checkpointBeforeDigest")
            digest(self.checkpoint_after_digest, label="checkpointAfterDigest")
            digest(self.integrity_digest, label="bundle payloadDigest")
        except ValueError as error:
            if isinstance(error, ObservationContractError):
                raise
            raise ObservationContractError(str(error)) from error
        for batch in self.batches:
            if batch.producer_identity != self.producer_identity:
                raise ObservationContractError("export bundle mixes producer identities")
            for event in batch.events:
                if event.source.mapping_version != self.mapping_version:
                    raise ObservationContractError("export bundle mixes mapping versions")
        if self.integrity_digest != canonical_digest(self._payload_dict()):
            raise ObservationContractError("export bundle integrity differs")

    @classmethod
    def build(
        cls,
        *,
        producer_identity: ObservationProducerIdentity,
        mapping_version: str,
        owner_revision: str,
        exporter_revision: str,
        exported_at_ms: int,
        checkpoint_before: ObservationExportCheckpoint,
        checkpoint_after: ObservationExportCheckpoint,
        batches: Iterable[ObservationBatch],
    ) -> "ObservationExportBundle":
        if checkpoint_before.producer_identity != producer_identity:
            raise ObservationContractError("before checkpoint producer differs")
        if checkpoint_after.producer_identity != producer_identity:
            raise ObservationContractError("after checkpoint producer differs")
        if checkpoint_before.mapping_version != mapping_version:
            raise ObservationContractError("before checkpoint mapping differs")
        if checkpoint_after.mapping_version != mapping_version:
            raise ObservationContractError("after checkpoint mapping differs")
        if checkpoint_after.updated_at_ms < checkpoint_before.updated_at_ms:
            raise ObservationCheckpointConflict(
                "after checkpoint time cannot precede before checkpoint time"
            )
        for stream_id, sequence in checkpoint_before.streams.items():
            if checkpoint_after.sequence(stream_id) < sequence:
                raise ObservationCheckpointConflict(
                    f"after checkpoint stream {stream_id} moved backward"
                )
        provisional = cls.__new__(cls)
        values = {
            "producer_identity": producer_identity,
            "mapping_version": mapping_version,
            "owner_revision": owner_revision,
            "exporter_revision": exporter_revision,
            "exported_at_ms": exported_at_ms,
            "checkpoint_before_digest": checkpoint_before.integrity_digest,
            "checkpoint_after_digest": checkpoint_after.integrity_digest,
            "batches": tuple(batches),
            "integrity_digest": "sha256:" + "0" * 64,
        }
        for key, value in values.items():
            object.__setattr__(provisional, key, value)
        values["integrity_digest"] = canonical_digest(provisional._payload_dict())
        return cls(**values)

    def _payload_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": _EXPORT_SCHEMA_VERSION,
            "kind": BUNDLE_KIND,
            "producerIdentity": self.producer_identity.to_dict(),
            "mappingVersion": self.mapping_version,
            "ownerRevision": self.owner_revision,
            "exporterRevision": self.exporter_revision,
            "exportedAtMs": self.exported_at_ms,
            "checkpointBeforeDigest": self.checkpoint_before_digest,
            "checkpointAfterDigest": self.checkpoint_after_digest,
            "batches": [batch.to_dict() for batch in self.batches],
        }

    def to_dict(self) -> dict[str, JsonValue]:
        value = self._payload_dict()
        value["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": self.integrity_digest,
        }
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationExportBundle":
        try:
            item = exact_object(
                value,
                required={
                    "schemaVersion",
                    "kind",
                    "producerIdentity",
                    "mappingVersion",
                    "ownerRevision",
                    "exporterRevision",
                    "exportedAtMs",
                    "checkpointBeforeDigest",
                    "checkpointAfterDigest",
                    "batches",
                    "integrity",
                },
                label="ObservationExportBundle",
            )
            if item["schemaVersion"] != _EXPORT_SCHEMA_VERSION or item["kind"] != BUNDLE_KIND:
                raise ObservationContractError(
                    "unsupported Observation export bundle version or kind"
                )
            batches = item["batches"]
            if not isinstance(batches, list):
                raise ObservationContractError("export bundle batches must be an array")
            integrity = exact_object(
                item["integrity"],
                required={"algorithm", "canonicalization", "payloadDigest"},
                label="ObservationExportBundle integrity",
            )
            if (
                integrity["algorithm"] != "sha256"
                or integrity["canonicalization"] != "ordivon-evidence-json-v1"
            ):
                raise ObservationContractError(
                    "unsupported Observation export bundle integrity"
                )
            return cls(
                producer_identity=ObservationProducerIdentity.from_dict(
                    item["producerIdentity"]
                ),
                mapping_version=item["mappingVersion"],
                owner_revision=item["ownerRevision"],
                exporter_revision=item["exporterRevision"],
                exported_at_ms=item["exportedAtMs"],
                checkpoint_before_digest=item["checkpointBeforeDigest"],
                checkpoint_after_digest=item["checkpointAfterDigest"],
                batches=tuple(
                    ObservationBatch.from_dict(batch) for batch in batches
                ),
                integrity_digest=integrity["payloadDigest"],
            )
        except ObservationContractError:
            raise
        except ValueError as error:
            raise ObservationContractError(str(error)) from error


def write_export_bundle(
    root: str | Path,
    bundle: ObservationExportBundle,
) -> Path:
    destination = Path(root).expanduser()
    if destination.is_symlink():
        raise ObservationBundleConflict("bundle outbox cannot be a symlink")
    if destination.exists():
        if not destination.is_dir():
            raise ObservationBundleConflict("bundle outbox is not a directory")
        if os.stat(destination).st_mode & 0o077:
            raise ObservationBundleConflict("bundle outbox permissions are not private")
    else:
        destination.mkdir(parents=True, mode=0o700)
        os.chmod(destination, 0o700)
    name = f"bundle-{bundle.integrity_digest.removeprefix('sha256:')}.json"
    target = destination / name
    encoded = canonical_bytes(bundle.to_dict()) + b"\n"
    if target.is_symlink():
        raise ObservationBundleConflict("bundle target cannot be a symlink")
    if target.exists():
        if not target.is_file():
            raise ObservationBundleConflict("bundle target is not a regular file")
        if os.stat(target).st_mode & 0o077:
            raise ObservationBundleConflict("bundle target permissions are not private")
        if target.read_bytes() != encoded:
            raise ObservationBundleConflict("bundle target bytes differ")
        return target
    temporary = target.with_name(
        f".{target.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}"
    )
    directory_fd: int | None = None
    try:
        with temporary.open("xb") as handle:
            os.chmod(temporary, 0o600)
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
        os.chmod(target, 0o600)
        directory_fd = os.open(
            destination, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        )
        os.fsync(directory_fd)
    finally:
        if directory_fd is not None:
            os.close(directory_fd)
        temporary.unlink(missing_ok=True)
    return target


def load_checkpoint(
    path: str | Path,
    *,
    producer_identity: ObservationProducerIdentity,
    mapping_version: str,
) -> ObservationExportCheckpoint:
    target = Path(path).expanduser()
    if target.is_symlink():
        raise ObservationCheckpointCorrupt("checkpoint path cannot be a symlink")
    if target.parent.is_symlink():
        raise ObservationCheckpointCorrupt("checkpoint parent cannot be a symlink")
    if target.parent.exists() and os.stat(target.parent).st_mode & 0o077:
        raise ObservationCheckpointCorrupt(
            "checkpoint parent permissions are not private"
        )
    if not target.exists():
        return ObservationExportCheckpoint.empty(
            producer_identity=producer_identity,
            mapping_version=mapping_version,
        )
    if not target.is_file():
        raise ObservationCheckpointCorrupt("checkpoint path is not a regular file")
    if os.stat(target).st_mode & 0o077:
        raise ObservationCheckpointCorrupt("checkpoint file permissions are not private")
    try:
        value = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ObservationCheckpointCorrupt("checkpoint cannot be decoded") from error
    checkpoint = ObservationExportCheckpoint.from_dict(value)
    if checkpoint.producer_identity != producer_identity:
        raise ObservationCheckpointCorrupt("checkpoint producer differs")
    if checkpoint.mapping_version != mapping_version:
        raise ObservationCheckpointCorrupt("checkpoint mapping version differs")
    return checkpoint


def write_checkpoint(
    path: str | Path,
    checkpoint: ObservationExportCheckpoint,
    *,
    expected_digest: str | None,
) -> None:
    target = Path(path).expanduser()
    if target.is_symlink():
        raise ObservationCheckpointCorrupt("checkpoint path cannot be a symlink")
    parent = target.parent
    if parent.is_symlink():
        raise ObservationCheckpointCorrupt("checkpoint parent cannot be a symlink")
    if parent.exists():
        if os.stat(parent).st_mode & 0o077:
            raise ObservationCheckpointCorrupt(
                "checkpoint parent permissions are not private"
            )
    else:
        parent.mkdir(parents=True, mode=0o700)
        os.chmod(parent, 0o700)
    if target.exists():
        current = load_checkpoint(
            target,
            producer_identity=checkpoint.producer_identity,
            mapping_version=checkpoint.mapping_version,
        )
        if expected_digest is None or current.integrity_digest != expected_digest:
            raise ObservationCheckpointConflict("checkpoint changed before commit")
    elif expected_digest is not None:
        raise ObservationCheckpointConflict("expected checkpoint is absent")
    temporary = target.with_name(f".{target.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}")
    directory_fd: int | None = None
    try:
        with temporary.open("xb") as handle:
            os.chmod(temporary, 0o600)
            handle.write(canonical_bytes(checkpoint.to_dict()))
            handle.write(b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
        os.chmod(target, 0o600)
        directory_fd = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        os.fsync(directory_fd)
    finally:
        if directory_fd is not None:
            os.close(directory_fd)
        temporary.unlink(missing_ok=True)


__all__ = [
    "BUNDLE_KIND",
    "CHECKPOINT_KIND",
    "ObservationCheckpointConflict",
    "ObservationCheckpointCorrupt",
    "ObservationBundleConflict",
    "ObservationExportBundle",
    "ObservationExportCheckpoint",
    "ObservationExportError",
    "load_checkpoint",
    "write_checkpoint",
    "write_export_bundle",
]
