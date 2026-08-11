from __future__ import annotations

from contextlib import contextmanager
import json
import os
from pathlib import Path
import sqlite3
import stat
from typing import Any, Iterable, Iterator

from .canonical import canonical_bytes, canonical_digest, sha256_bytes
from .contract import (
    ObservationBatch,
    ObservationContractError,
    ObservationEnvelope,
    ObservationIngestAcknowledgement,
    ObservationPrivacyError,
    ObservationProducerIdentity,
)

_GATEWAY_SCHEMA_VERSION = 1
_GATEWAY_KIND = "ordivon.observation-gateway"
_CATALOG_KIND = "ordivon.observation-catalog-snapshot"
_COMPLETENESS_STATES = {"empty", "complete", "gap", "quarantined"}


class ObservationGatewayError(RuntimeError):
    pass


class ObservationRejected(ObservationGatewayError):
    def __init__(
        self,
        reason: str,
        *,
        acknowledgement: ObservationIngestAcknowledgement | None = None,
    ) -> None:
        super().__init__(reason)
        self.reason = reason
        self.acknowledgement = acknowledgement


class ObservationContractRejected(ObservationRejected):
    pass


class ObservationPolicyRejected(ObservationRejected):
    pass


class ObservationMappingRejected(ObservationRejected):
    pass


class ObservationSequenceGap(ObservationRejected):
    pass


class ObservationCorruption(ObservationRejected):
    pass


class ObservationGatewayCorrupt(ObservationGatewayError):
    pass


class _BatchReject(Exception):
    def __init__(self, reason: str, *, event_id: str | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.event_id = event_id


def _producer_key(identity: ObservationProducerIdentity) -> tuple[str, str, str]:
    return identity.project_id, identity.component_id, identity.instance_id


def _stream_key(batch: ObservationBatch) -> tuple[str, str, str, str]:
    return (*_producer_key(batch.producer_identity), batch.stream_id)


def _exception_for_reason(
    reason: str,
    *,
    acknowledgement: ObservationIngestAcknowledgement | None,
) -> ObservationRejected:
    if reason in {
        "event_identity_conflict",
        "stream_sequence_conflict",
        "request_identity_conflict",
        "stored_event_index_drift",
        "stream_projection_drift",
    }:
        return ObservationCorruption(reason, acknowledgement=acknowledgement)
    if reason == "sequence_gap":
        return ObservationSequenceGap(reason, acknowledgement=acknowledgement)
    if reason in {"producer_not_allowlisted", "mapping_version_not_allowlisted"}:
        return ObservationMappingRejected(reason, acknowledgement=acknowledgement)
    if reason in {"privacy_rejected", "secret_like_metadata"}:
        return ObservationPolicyRejected(reason, acknowledgement=acknowledgement)
    return ObservationRejected(reason, acknowledgement=acknowledgement)


class SQLiteObservationGateway:
    """In-process, observation-only SQLite ingest and query core."""

    def __init__(self, root: str | Path) -> None:
        requested_root = Path(root).expanduser()
        if requested_root.is_symlink():
            raise ValueError("Observation Gateway state root cannot be a symlink")
        self.root = requested_root.resolve(strict=False)
        database = self.root / "observation.sqlite3"
        if not database.is_file():
            raise FileNotFoundError(database)
        if database.is_symlink():
            raise ValueError("Observation Gateway database cannot be a symlink")
        os.chmod(self.root, 0o700)
        os.chmod(database, 0o600)
        self.database = database
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA synchronous = FULL")
        self._harden_sqlite_files()
        self.gateway_instance_id = self._read_instance_identity()

    @classmethod
    def initialize(
        cls,
        root: str | Path,
        *,
        gateway_instance_id: str,
        producer_allowlist: Iterable[ObservationProducerIdentity],
        mapping_versions: Iterable[tuple[str, str, str]],
        created_at_ms: int,
    ) -> "SQLiteObservationGateway":
        requested_state = Path(root).expanduser()
        if requested_state.is_symlink():
            raise ValueError("Observation Gateway state root cannot be a symlink")
        state = requested_state.resolve(strict=False)
        if state.exists():
            raise FileExistsError(state)
        if state.parent.exists() and state.parent.is_symlink():
            raise ValueError("Observation Gateway parent cannot be a symlink")
        state.mkdir(parents=True, mode=0o700)
        os.chmod(state, 0o700)
        database = state / "observation.sqlite3"
        connection = sqlite3.connect(database)
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA synchronous = FULL")
            connection.executescript(_SCHEMA)
            connection.execute(
                "INSERT INTO schema_info(schema_version, kind, gateway_instance_id, "
                "created_at_ms) VALUES (?, ?, ?, ?)",
                (
                    _GATEWAY_SCHEMA_VERSION,
                    _GATEWAY_KIND,
                    gateway_instance_id,
                    created_at_ms,
                ),
            )
            connection.execute(
                "INSERT INTO schema_migrations(version, applied_at_ms, migration_digest) "
                "VALUES (?, ?, ?)",
                (
                    _GATEWAY_SCHEMA_VERSION,
                    created_at_ms,
                    canonical_digest(
                        {
                            "kind": "ordivon.observation-gateway-schema",
                            "version": _GATEWAY_SCHEMA_VERSION,
                        }
                    ),
                ),
            )
            producers = tuple(producer_allowlist)
            if not producers:
                raise ValueError("Observation Gateway requires an explicit producer allowlist")
            for producer in producers:
                connection.execute(
                    "INSERT INTO producer_instances(project_id, component_id, instance_id, "
                    "allowlisted, first_seen_ms, last_seen_ms) VALUES (?, ?, ?, 1, NULL, NULL)",
                    _producer_key(producer),
                )
            mappings = tuple(mapping_versions)
            if not mappings:
                raise ValueError("Observation Gateway requires mapping versions")
            for project_id, component_id, mapping_version in mappings:
                connection.execute(
                    "INSERT INTO mapping_versions(project_id, component_id, mapping_version, "
                    "admitted_at_ms) VALUES (?, ?, ?, ?)",
                    (project_id, component_id, mapping_version, created_at_ms),
                )
            connection.commit()
        except BaseException:
            connection.close()
            import shutil

            shutil.rmtree(state, ignore_errors=True)
            raise
        else:
            connection.close()
        os.chmod(database, 0o600)
        for path in (database.with_name(database.name + "-wal"), database.with_name(database.name + "-shm")):
            if path.exists():
                os.chmod(path, 0o600)
        return cls(state)

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteObservationGateway":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    @contextmanager
    def _transaction(self) -> Iterator[None]:
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self.connection.rollback()
            raise
        else:
            self.connection.commit()
            self._harden_sqlite_files()

    def _harden_sqlite_files(self) -> None:
        for path in (
            self.database,
            self.database.with_name(self.database.name + "-wal"),
            self.database.with_name(self.database.name + "-shm"),
        ):
            if path.exists():
                if path.is_symlink():
                    raise ValueError("Observation Gateway SQLite file cannot be a symlink")
                os.chmod(path, 0o600)

    def _read_instance_identity(self) -> str:
        row = self.connection.execute(
            "SELECT schema_version, kind, gateway_instance_id FROM schema_info"
        ).fetchone()
        if row is None:
            raise ObservationGatewayCorrupt("Observation Gateway schema_info is missing")
        if row["schema_version"] != _GATEWAY_SCHEMA_VERSION or row["kind"] != _GATEWAY_KIND:
            raise ObservationGatewayCorrupt("unsupported Observation Gateway schema")
        return str(row["gateway_instance_id"])

    def ingest_dict(
        self,
        value: Any,
        *,
        ingested_at_ms: int,
    ) -> ObservationIngestAcknowledgement:
        try:
            batch = ObservationBatch.from_dict(value)
        except ObservationPrivacyError as error:
            self._record_unparsed_rejection(
                value,
                observed_at_ms=ingested_at_ms,
                reason="privacy_rejected",
                detail=type(error).__name__,
            )
            raise ObservationPolicyRejected("privacy_rejected") from error
        except (ObservationContractError, ValueError) as error:
            self._record_unparsed_rejection(
                value,
                observed_at_ms=ingested_at_ms,
                reason="contract_rejected",
                detail=type(error).__name__,
            )
            raise ObservationContractRejected("contract_rejected") from error
        return self.ingest(batch, ingested_at_ms=ingested_at_ms)

    def ingest(
        self,
        batch: ObservationBatch,
        *,
        ingested_at_ms: int,
    ) -> ObservationIngestAcknowledgement:
        if ingested_at_ms < 0:
            raise ValueError("Observation ingest time must be non-negative")
        producer = _producer_key(batch.producer_identity)
        if not self._producer_is_allowlisted(producer):
            return self._reject_and_raise(
                batch,
                observed_at_ms=ingested_at_ms,
                reason="producer_not_allowlisted",
            )
        unsupported = [
            event.source.mapping_version
            for event in batch.events
            if not self._mapping_is_allowlisted(
                event.source.project_id,
                event.source.component_id,
                event.source.mapping_version,
            )
        ]
        if unsupported:
            return self._reject_and_raise(
                batch,
                observed_at_ms=ingested_at_ms,
                reason="mapping_version_not_allowlisted",
            )

        try:
            with self._transaction():
                replay = self._request_replay(batch)
                if replay is not None:
                    if replay.status == "committed":
                        return replay
                    raise _BatchReject("previous_request_rejected")
                acknowledgement = self._ingest_transaction(
                    batch, ingested_at_ms=ingested_at_ms
                )
                return acknowledgement
        except _BatchReject as error:
            return self._reject_and_raise(
                batch,
                observed_at_ms=ingested_at_ms,
                reason=error.reason,
                event_id=error.event_id,
            )
        except sqlite3.IntegrityError:
            return self._reject_and_raise(
                batch,
                observed_at_ms=ingested_at_ms,
                reason="stream_sequence_conflict",
            )

    def _request_replay(
        self, batch: ObservationBatch
    ) -> ObservationIngestAcknowledgement | None:
        producer = _producer_key(batch.producer_identity)
        row = self.connection.execute(
            "SELECT batch_digest, status, acknowledgement_json, rejection_reason "
            "FROM ingest_receipts WHERE project_id = ? AND component_id = ? "
            "AND instance_id = ? AND request_id = ?",
            (*producer, batch.request_id),
        ).fetchone()
        if row is None:
            return None
        if row["batch_digest"] != batch.batch_digest:
            raise _BatchReject("request_identity_conflict")
        acknowledgement = ObservationIngestAcknowledgement.from_dict(
            json.loads(bytes(row["acknowledgement_json"]).decode("utf-8"))
        )
        if row["status"] == "rejected":
            raise _BatchReject(str(row["rejection_reason"]))
        return acknowledgement

    def _ingest_transaction(
        self,
        batch: ObservationBatch,
        *,
        ingested_at_ms: int,
    ) -> ObservationIngestAcknowledgement:
        key = _stream_key(batch)
        row = self.connection.execute(
            "SELECT last_contiguous_sequence, highest_seen_sequence, completeness_state "
            "FROM source_streams WHERE project_id = ? AND component_id = ? "
            "AND instance_id = ? AND stream_id = ?",
            key,
        ).fetchone()
        last_contiguous = 0 if row is None else int(row["last_contiguous_sequence"])
        highest_seen = 0 if row is None else int(row["highest_seen_sequence"])
        if batch.first_sequence > last_contiguous + 1:
            raise _BatchReject("sequence_gap")

        expected_new = last_contiguous + 1
        accepted = 0
        duplicates = 0
        for event in batch.events:
            canonical = event.canonical_bytes
            existing = self.connection.execute(
                "SELECT envelope_digest, canonical_json, project_id, component_id, "
                "instance_id, stream_id, sequence FROM events WHERE event_id = ?",
                (event.event_id,),
            ).fetchone()
            by_sequence = self.connection.execute(
                "SELECT event_id FROM events WHERE project_id = ? AND component_id = ? "
                "AND instance_id = ? AND stream_id = ? AND sequence = ?",
                (*key, event.source.sequence),
            ).fetchone()
            if existing is not None:
                if (
                    existing["envelope_digest"] != event.canonical_digest
                    or bytes(existing["canonical_json"]) != canonical
                    or tuple(existing[field] for field in ("project_id", "component_id", "instance_id", "stream_id"))
                    != key
                    or int(existing["sequence"]) != event.source.sequence
                ):
                    raise _BatchReject(
                        "event_identity_conflict", event_id=event.event_id
                    )
                if by_sequence is None or by_sequence["event_id"] != event.event_id:
                    raise _BatchReject(
                        "stored_event_index_drift", event_id=event.event_id
                    )
                if event.source.sequence > last_contiguous:
                    raise _BatchReject(
                        "stream_projection_drift", event_id=event.event_id
                    )
                duplicates += 1
                continue
            if by_sequence is not None:
                raise _BatchReject(
                    "stream_sequence_conflict", event_id=event.event_id
                )
            if event.source.sequence != expected_new:
                reason = (
                    "stream_projection_drift"
                    if event.source.sequence <= last_contiguous
                    else "sequence_gap"
                )
                raise _BatchReject(reason, event_id=event.event_id)
            self.connection.execute(
                "INSERT INTO events(event_id, envelope_digest, canonical_json, project_id, "
                "component_id, instance_id, stream_id, sequence, native_kind, native_id, "
                "native_revision, native_digest, mapping_version, occurred_at_ms, "
                "privacy_class) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event.event_id,
                    event.canonical_digest,
                    canonical,
                    event.source.project_id,
                    event.source.component_id,
                    event.source.instance_id,
                    event.source.stream_id,
                    event.source.sequence,
                    event.source.native_kind,
                    event.source.native_id,
                    None
                    if event.source.native_revision is None
                    else str(event.source.native_revision),
                    event.source.native_digest,
                    event.source.mapping_version,
                    event.occurred_at_ms,
                    event.privacy.privacy_class,
                ),
            )
            for ordinal, relation in enumerate(event.relations):
                self.connection.execute(
                    "INSERT INTO relations(event_id, ordinal, relation_type, target_kind, "
                    "target_id, target_digest) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        event.event_id,
                        ordinal,
                        relation.relation_type,
                        relation.target_kind,
                        relation.target_id,
                        relation.target_digest,
                    ),
                )
            accepted += 1
            expected_new += 1

        new_last = expected_new - 1
        new_highest = max(highest_seen, batch.last_sequence)
        state = "complete" if new_last >= new_highest else "gap"
        self._upsert_stream(
            key,
            last_contiguous_sequence=new_last,
            highest_seen_sequence=new_highest,
            completeness_state=state,
            updated_at_ms=ingested_at_ms,
        )
        self.connection.execute(
            "UPDATE producer_instances SET first_seen_ms = COALESCE(first_seen_ms, ?), "
            "last_seen_ms = ? WHERE project_id = ? AND component_id = ? AND instance_id = ?",
            (ingested_at_ms, ingested_at_ms, *key[:3]),
        )
        acknowledgement = ObservationIngestAcknowledgement.build(
            batch=batch,
            accepted=accepted,
            duplicates=duplicates,
            rejected=0,
            last_contiguous_sequence=new_last,
            status="committed",
            ingested_at_ms=ingested_at_ms,
        )
        self._insert_receipt(
            batch,
            acknowledgement,
            status="committed",
            rejection_reason=None,
        )
        return acknowledgement

    def _reject_and_raise(
        self,
        batch: ObservationBatch,
        *,
        observed_at_ms: int,
        reason: str,
        event_id: str | None = None,
    ) -> ObservationIngestAcknowledgement:
        producer = _producer_key(batch.producer_identity)
        existing = self.connection.execute(
            "SELECT batch_digest, acknowledgement_json, rejection_reason, status "
            "FROM ingest_receipts WHERE project_id = ? AND component_id = ? "
            "AND instance_id = ? AND request_id = ?",
            (*producer, batch.request_id),
        ).fetchone()
        if existing is not None and existing["batch_digest"] == batch.batch_digest:
            acknowledgement = ObservationIngestAcknowledgement.from_dict(
                json.loads(bytes(existing["acknowledgement_json"]).decode("utf-8"))
            )
            stored_reason = str(existing["rejection_reason"] or reason)
            raise _exception_for_reason(
                stored_reason, acknowledgement=acknowledgement
            )

        key = _stream_key(batch)
        with self._transaction():
            row = self.connection.execute(
                "SELECT last_contiguous_sequence, highest_seen_sequence FROM source_streams "
                "WHERE project_id = ? AND component_id = ? AND instance_id = ? AND stream_id = ?",
                key,
            ).fetchone()
            last_contiguous = 0 if row is None else int(row["last_contiguous_sequence"])
            highest_seen = 0 if row is None else int(row["highest_seen_sequence"])
            new_highest = max(highest_seen, batch.last_sequence)
            state = "gap" if reason == "sequence_gap" else "quarantined"
            self._upsert_stream(
                key,
                last_contiguous_sequence=last_contiguous,
                highest_seen_sequence=new_highest,
                completeness_state=state,
                updated_at_ms=observed_at_ms,
            )
            acknowledgement = ObservationIngestAcknowledgement.build(
                batch=batch,
                accepted=0,
                duplicates=0,
                rejected=len(batch.events),
                last_contiguous_sequence=last_contiguous,
                status="rejected",
                ingested_at_ms=observed_at_ms,
            )
            if existing is None:
                self._insert_receipt(
                    batch,
                    acknowledgement,
                    status="rejected",
                    rejection_reason=reason,
                )
            self._insert_quarantine(
                observed_at_ms=observed_at_ms,
                reason=reason,
                request_id=batch.request_id,
                event_id=event_id,
                producer=producer,
                stream_id=batch.stream_id,
                first_sequence=batch.first_sequence,
                last_sequence=batch.last_sequence,
                incoming_digest=batch.batch_digest,
                detail="batch rejected before completeness advancement",
            )
        raise _exception_for_reason(reason, acknowledgement=acknowledgement)

    def _record_unparsed_rejection(
        self,
        value: Any,
        *,
        observed_at_ms: int,
        reason: str,
        detail: str,
    ) -> None:
        request_id: str | None = None
        event_id: str | None = None
        producer: tuple[str, str, str] | None = None
        stream_id: str | None = None
        first_sequence: int | None = None
        last_sequence: int | None = None
        if isinstance(value, dict):
            request_id = value.get("requestId") if isinstance(value.get("requestId"), str) else None
            stream_id = value.get("streamId") if isinstance(value.get("streamId"), str) else None
            first_sequence = value.get("firstSequence") if type(value.get("firstSequence")) is int else None
            last_sequence = value.get("lastSequence") if type(value.get("lastSequence")) is int else None
            identity = value.get("producerIdentity")
            if isinstance(identity, dict) and all(
                isinstance(identity.get(field), str)
                for field in ("projectId", "componentId", "instanceId")
            ):
                producer = (
                    identity["projectId"],
                    identity["componentId"],
                    identity["instanceId"],
                )
            events = value.get("events")
            if isinstance(events, list) and events and isinstance(events[0], dict):
                candidate = events[0].get("eventId")
                event_id = candidate if isinstance(candidate, str) else None
        try:
            incoming_digest = canonical_digest(value)
        except ValueError:
            incoming_digest = sha256_bytes(type(value).__name__.encode("utf-8"))
        with self._transaction():
            self._insert_quarantine(
                observed_at_ms=observed_at_ms,
                reason=reason,
                request_id=request_id,
                event_id=event_id,
                producer=producer,
                stream_id=stream_id,
                first_sequence=first_sequence,
                last_sequence=last_sequence,
                incoming_digest=incoming_digest,
                detail=detail,
            )

    def _producer_is_allowlisted(self, producer: tuple[str, str, str]) -> bool:
        row = self.connection.execute(
            "SELECT allowlisted FROM producer_instances WHERE project_id = ? "
            "AND component_id = ? AND instance_id = ?",
            producer,
        ).fetchone()
        return row is not None and row["allowlisted"] == 1

    def _mapping_is_allowlisted(
        self, project_id: str, component_id: str, mapping_version: str
    ) -> bool:
        return (
            self.connection.execute(
                "SELECT 1 FROM mapping_versions WHERE project_id = ? AND component_id = ? "
                "AND mapping_version = ?",
                (project_id, component_id, mapping_version),
            ).fetchone()
            is not None
        )

    def _upsert_stream(
        self,
        key: tuple[str, str, str, str],
        *,
        last_contiguous_sequence: int,
        highest_seen_sequence: int,
        completeness_state: str,
        updated_at_ms: int,
    ) -> None:
        if completeness_state not in _COMPLETENESS_STATES:
            raise ValueError("unsupported completeness state")
        self.connection.execute(
            "INSERT INTO source_streams(project_id, component_id, instance_id, stream_id, "
            "last_contiguous_sequence, highest_seen_sequence, completeness_state, updated_at_ms) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(project_id, component_id, "
            "instance_id, stream_id) DO UPDATE SET last_contiguous_sequence = excluded.last_contiguous_sequence, "
            "highest_seen_sequence = excluded.highest_seen_sequence, completeness_state = excluded.completeness_state, "
            "updated_at_ms = excluded.updated_at_ms",
            (*key, last_contiguous_sequence, highest_seen_sequence, completeness_state, updated_at_ms),
        )

    def _insert_receipt(
        self,
        batch: ObservationBatch,
        acknowledgement: ObservationIngestAcknowledgement,
        *,
        status: str,
        rejection_reason: str | None,
    ) -> None:
        self.connection.execute(
            "INSERT INTO ingest_receipts(gateway_receipt_digest, request_id, project_id, "
            "component_id, instance_id, stream_id, batch_digest, status, acknowledgement_json, "
            "rejection_reason, created_at_ms) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                acknowledgement.gateway_receipt_digest,
                batch.request_id,
                batch.producer_identity.project_id,
                batch.producer_identity.component_id,
                batch.producer_identity.instance_id,
                batch.stream_id,
                batch.batch_digest,
                status,
                canonical_bytes(acknowledgement.to_dict()),
                rejection_reason,
                acknowledgement.ingested_at_ms,
            ),
        )

    def _insert_quarantine(
        self,
        *,
        observed_at_ms: int,
        reason: str,
        request_id: str | None,
        event_id: str | None,
        producer: tuple[str, str, str] | None,
        stream_id: str | None,
        first_sequence: int | None,
        last_sequence: int | None,
        incoming_digest: str,
        detail: str,
    ) -> None:
        project_id, component_id, instance_id = (
            (None, None, None) if producer is None else producer
        )
        self.connection.execute(
            "INSERT INTO quarantine(observed_at_ms, reason, request_id, event_id, project_id, "
            "component_id, instance_id, stream_id, first_sequence, last_sequence, incoming_digest, detail) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                observed_at_ms,
                reason,
                request_id,
                event_id,
                project_id,
                component_id,
                instance_id,
                stream_id,
                first_sequence,
                last_sequence,
                incoming_digest,
                detail,
            ),
        )

    def event(self, event_id: str) -> ObservationEnvelope:
        row = self.connection.execute(
            "SELECT canonical_json FROM events WHERE event_id = ?", (event_id,)
        ).fetchone()
        if row is None:
            raise KeyError(event_id)
        return ObservationEnvelope.from_dict(
            json.loads(bytes(row["canonical_json"]).decode("utf-8"))
        )

    def stream_status(
        self,
        *,
        project_id: str,
        component_id: str,
        instance_id: str,
        stream_id: str,
    ) -> dict[str, Any]:
        row = self.connection.execute(
            "SELECT last_contiguous_sequence, highest_seen_sequence, completeness_state, "
            "updated_at_ms FROM source_streams WHERE project_id = ? AND component_id = ? "
            "AND instance_id = ? AND stream_id = ?",
            (project_id, component_id, instance_id, stream_id),
        ).fetchone()
        if row is None:
            return {
                "lastContiguousSequence": 0,
                "highestSeenSequence": 0,
                "completenessState": "empty",
                "updatedAtMs": None,
            }
        return {
            "lastContiguousSequence": int(row["last_contiguous_sequence"]),
            "highestSeenSequence": int(row["highest_seen_sequence"]),
            "completenessState": row["completeness_state"],
            "updatedAtMs": int(row["updated_at_ms"]),
        }

    def quarantine(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT observed_at_ms, reason, request_id, event_id, project_id, component_id, "
            "instance_id, stream_id, first_sequence, last_sequence, incoming_digest, detail "
            "FROM quarantine ORDER BY quarantine_id"
        ).fetchall()
        return [dict(row) for row in rows]

    def status(self) -> dict[str, Any]:
        event_count = int(self.connection.execute("SELECT COUNT(*) FROM events").fetchone()[0])
        receipt_count = int(
            self.connection.execute("SELECT COUNT(*) FROM ingest_receipts").fetchone()[0]
        )
        quarantine_count = int(
            self.connection.execute("SELECT COUNT(*) FROM quarantine").fetchone()[0]
        )
        stream_counts = {
            row["completeness_state"]: int(row["count"])
            for row in self.connection.execute(
                "SELECT completeness_state, COUNT(*) AS count FROM source_streams "
                "GROUP BY completeness_state"
            )
        }
        return {
            "schemaVersion": _GATEWAY_SCHEMA_VERSION,
            "gatewayInstanceId": self.gateway_instance_id,
            "events": event_count,
            "receipts": receipt_count,
            "quarantine": quarantine_count,
            "streams": stream_counts,
        }

    def catalog_snapshot(self) -> dict[str, Any]:
        event_rows = self.connection.execute(
            "SELECT event_id, envelope_digest, project_id, component_id, instance_id, "
            "stream_id, sequence, native_kind, native_id, mapping_version FROM events "
            "ORDER BY project_id, component_id, instance_id, stream_id, sequence"
        ).fetchall()
        events: list[dict[str, Any]] = []
        for row in event_rows:
            relations = [
                {
                    "relationType": relation["relation_type"],
                    "targetKind": relation["target_kind"],
                    "targetId": relation["target_id"],
                    **(
                        {}
                        if relation["target_digest"] is None
                        else {"targetDigest": relation["target_digest"]}
                    ),
                }
                for relation in self.connection.execute(
                    "SELECT relation_type, target_kind, target_id, target_digest FROM relations "
                    "WHERE event_id = ? ORDER BY ordinal",
                    (row["event_id"],),
                )
            ]
            events.append(
                {
                    "eventId": row["event_id"],
                    "envelopeDigest": row["envelope_digest"],
                    "source": {
                        "projectId": row["project_id"],
                        "componentId": row["component_id"],
                        "instanceId": row["instance_id"],
                        "streamId": row["stream_id"],
                        "sequence": int(row["sequence"]),
                        "nativeKind": row["native_kind"],
                        "nativeId": row["native_id"],
                        "mappingVersion": row["mapping_version"],
                    },
                    "relations": relations,
                }
            )
        streams = [
            {
                "projectId": row["project_id"],
                "componentId": row["component_id"],
                "instanceId": row["instance_id"],
                "streamId": row["stream_id"],
                "lastContiguousSequence": int(row["last_contiguous_sequence"]),
                "highestSeenSequence": int(row["highest_seen_sequence"]),
                "completenessState": row["completeness_state"],
            }
            for row in self.connection.execute(
                "SELECT project_id, component_id, instance_id, stream_id, "
                "last_contiguous_sequence, highest_seen_sequence, completeness_state "
                "FROM source_streams ORDER BY project_id, component_id, instance_id, stream_id"
            )
        ]
        return {
            "schemaVersion": 1,
            "kind": _CATALOG_KIND,
            "events": events,
            "streams": streams,
        }

    @property
    def catalog_digest(self) -> str:
        return canonical_digest(self.catalog_snapshot())

    def doctor(self, *, full: bool = False) -> dict[str, Any]:
        checks: list[dict[str, str]] = []
        quick = tuple(
            row[0] for row in self.connection.execute("PRAGMA quick_check").fetchall()
        )
        checks.append(
            {
                "name": "sqlite.quick_check",
                "status": "ok" if quick == ("ok",) else "error",
                "detail": repr(quick),
            }
        )
        paths = [
            (self.root, 0o700),
            (self.database, 0o600),
        ]
        paths.extend(
            (path, 0o600)
            for path in (
                self.database.with_name(self.database.name + "-wal"),
                self.database.with_name(self.database.name + "-shm"),
            )
            if path.exists()
        )
        insecure = [
            f"{path.name}:{stat.S_IMODE(path.stat().st_mode):04o}"
            for path, expected in paths
            if stat.S_IMODE(path.stat().st_mode) != expected
        ]
        checks.append(
            {
                "name": "state.permissions",
                "status": "error" if insecure else "ok",
                "detail": ",".join(insecure) if insecure else "private",
            }
        )
        if full:
            try:
                self._validate_full_history()
            except BaseException as error:
                checks.append(
                    {
                        "name": "catalog.history",
                        "status": "error",
                        "detail": f"{type(error).__name__}: {error}",
                    }
                )
            else:
                checks.append(
                    {
                        "name": "catalog.history",
                        "status": "ok",
                        "detail": self.catalog_digest,
                    }
                )
        return {
            "schemaVersion": 1,
            "kind": "ordivon.observation-gateway-doctor",
            "healthy": not any(check["status"] == "error" for check in checks),
            "checks": checks,
            "status": self.status(),
        }

    def _validate_full_history(self) -> None:
        for row in self.connection.execute(
            "SELECT event_id, envelope_digest, canonical_json, project_id, component_id, "
            "instance_id, stream_id, sequence FROM events"
        ):
            raw = bytes(row["canonical_json"])
            envelope = ObservationEnvelope.from_dict(json.loads(raw.decode("utf-8")))
            if envelope.canonical_bytes != raw:
                raise ObservationGatewayCorrupt(
                    f"canonical Event bytes differ: {row['event_id']}"
                )
            if envelope.event_id != row["event_id"] or envelope.canonical_digest != row["envelope_digest"]:
                raise ObservationGatewayCorrupt(
                    f"Event identity or digest differs: {row['event_id']}"
                )
            if (
                envelope.source.project_id,
                envelope.source.component_id,
                envelope.source.instance_id,
                envelope.source.stream_id,
                envelope.source.sequence,
            ) != (
                row["project_id"],
                row["component_id"],
                row["instance_id"],
                row["stream_id"],
                row["sequence"],
            ):
                raise ObservationGatewayCorrupt(
                    f"Event source index differs: {row['event_id']}"
                )
            indexed = self.connection.execute(
                "SELECT relation_type, target_kind, target_id, target_digest FROM relations "
                "WHERE event_id = ? ORDER BY ordinal",
                (row["event_id"],),
            ).fetchall()
            expected_relations = [
                (
                    relation.relation_type,
                    relation.target_kind,
                    relation.target_id,
                    relation.target_digest,
                )
                for relation in envelope.relations
            ]
            actual_relations = [tuple(item) for item in indexed]
            if actual_relations != expected_relations:
                raise ObservationGatewayCorrupt(
                    f"Event relation index differs: {row['event_id']}"
                )
        for stream in self.connection.execute(
            "SELECT project_id, component_id, instance_id, stream_id, "
            "last_contiguous_sequence, highest_seen_sequence, completeness_state "
            "FROM source_streams"
        ):
            last = int(stream["last_contiguous_sequence"])
            highest = int(stream["highest_seen_sequence"])
            sequences = [
                int(row[0])
                for row in self.connection.execute(
                    "SELECT sequence FROM events WHERE project_id = ? AND component_id = ? "
                    "AND instance_id = ? AND stream_id = ? ORDER BY sequence",
                    tuple(stream[field] for field in ("project_id", "component_id", "instance_id", "stream_id")),
                )
            ]
            if sequences[:last] != list(range(1, last + 1)):
                raise ObservationGatewayCorrupt("source stream contiguous prefix differs")
            state = stream["completeness_state"]
            if state not in _COMPLETENESS_STATES:
                raise ObservationGatewayCorrupt("source stream completeness state differs")
            if state == "complete" and last < highest:
                raise ObservationGatewayCorrupt("complete stream has an unresolved gap")


_SCHEMA = """
CREATE TABLE schema_info(
    schema_version INTEGER NOT NULL,
    kind TEXT NOT NULL,
    gateway_instance_id TEXT NOT NULL,
    created_at_ms INTEGER NOT NULL
) STRICT;

CREATE TABLE schema_migrations(
    version INTEGER PRIMARY KEY,
    applied_at_ms INTEGER NOT NULL,
    migration_digest TEXT NOT NULL
) STRICT;

CREATE TABLE producer_instances(
    project_id TEXT NOT NULL,
    component_id TEXT NOT NULL,
    instance_id TEXT NOT NULL,
    allowlisted INTEGER NOT NULL CHECK(allowlisted IN (0, 1)),
    first_seen_ms INTEGER,
    last_seen_ms INTEGER,
    PRIMARY KEY(project_id, component_id, instance_id)
) STRICT;

CREATE TABLE mapping_versions(
    project_id TEXT NOT NULL,
    component_id TEXT NOT NULL,
    mapping_version TEXT NOT NULL,
    admitted_at_ms INTEGER NOT NULL,
    PRIMARY KEY(project_id, component_id, mapping_version)
) STRICT;

CREATE TABLE events(
    event_id TEXT PRIMARY KEY,
    envelope_digest TEXT NOT NULL,
    canonical_json BLOB NOT NULL,
    project_id TEXT NOT NULL,
    component_id TEXT NOT NULL,
    instance_id TEXT NOT NULL,
    stream_id TEXT NOT NULL,
    sequence INTEGER NOT NULL CHECK(sequence >= 1),
    native_kind TEXT NOT NULL,
    native_id TEXT NOT NULL,
    native_revision TEXT,
    native_digest TEXT NOT NULL,
    mapping_version TEXT NOT NULL,
    occurred_at_ms INTEGER NOT NULL CHECK(occurred_at_ms >= 0),
    privacy_class TEXT NOT NULL,
    UNIQUE(project_id, component_id, instance_id, stream_id, sequence)
) STRICT;

CREATE TABLE source_streams(
    project_id TEXT NOT NULL,
    component_id TEXT NOT NULL,
    instance_id TEXT NOT NULL,
    stream_id TEXT NOT NULL,
    last_contiguous_sequence INTEGER NOT NULL CHECK(last_contiguous_sequence >= 0),
    highest_seen_sequence INTEGER NOT NULL CHECK(highest_seen_sequence >= 0),
    completeness_state TEXT NOT NULL,
    updated_at_ms INTEGER NOT NULL,
    PRIMARY KEY(project_id, component_id, instance_id, stream_id)
) STRICT;

CREATE TABLE relations(
    event_id TEXT NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    ordinal INTEGER NOT NULL CHECK(ordinal >= 0),
    relation_type TEXT NOT NULL,
    target_kind TEXT NOT NULL,
    target_id TEXT NOT NULL,
    target_digest TEXT,
    PRIMARY KEY(event_id, ordinal)
) STRICT;

CREATE INDEX relations_target_idx ON relations(target_kind, target_id, event_id);

CREATE TABLE ingest_receipts(
    gateway_receipt_digest TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    component_id TEXT NOT NULL,
    instance_id TEXT NOT NULL,
    stream_id TEXT NOT NULL,
    batch_digest TEXT NOT NULL,
    status TEXT NOT NULL,
    acknowledgement_json BLOB NOT NULL,
    rejection_reason TEXT,
    created_at_ms INTEGER NOT NULL,
    UNIQUE(project_id, component_id, instance_id, request_id)
) STRICT;

CREATE TABLE quarantine(
    quarantine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    observed_at_ms INTEGER NOT NULL,
    reason TEXT NOT NULL,
    request_id TEXT,
    event_id TEXT,
    project_id TEXT,
    component_id TEXT,
    instance_id TEXT,
    stream_id TEXT,
    first_sequence INTEGER,
    last_sequence INTEGER,
    incoming_digest TEXT NOT NULL,
    detail TEXT NOT NULL
) STRICT;
"""


__all__ = [
    "ObservationContractRejected",
    "ObservationCorruption",
    "ObservationGatewayCorrupt",
    "ObservationGatewayError",
    "ObservationMappingRejected",
    "ObservationPolicyRejected",
    "ObservationRejected",
    "ObservationSequenceGap",
    "SQLiteObservationGateway",
]
