from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
import time
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterator

from .authority import (
    Attestation,
    AttestationKind,
    AuthorityPolicy,
    AuthorityRef,
    AuthorityRole,
)
from .identity import IdKind, SemanticId
from .reducer import ReferenceReducer
from .model import (
    Admission,
    Artifact,
    BindingAdmission,
    CapabilityRef,
    Claim,
    CompletionSemantics,
    DispatchRecord,
    DispatchState,
    EffectEvent,
    EffectMode,
    EffectRecord,
    EffectSpec,
    EventKind,
    EvidenceKind,
    EvidenceRef,
    Fact,
    IdempotencyKind,
    Observation,
    Precondition,
    Verification,
    VerificationDecision,
    VerificationPlan,
    WorldObjectRef,
)
from .state import EffectState


JOURNAL_SCHEMA_VERSION = 4
SEMANTIC_MODEL_VERSION = "semantic-core-v4-binding-edge"
REDUCER_VERSION = "incremental-reducer-v4-binding-edge"
_LEGACY_SCHEMA_VERSIONS = {2, 3}
_LEGACY_METADATA = {
    2: ("semantic-core-v2-authority", "reference-reducer-v2"),
    3: ("semantic-core-v3-slim", "incremental-reducer-v3"),
}
_GENESIS_DIGEST = "sha256:" + ("0" * 64)


class JournalError(RuntimeError):
    pass


class JournalCorruption(JournalError):
    pass


class JournalConflict(JournalError):
    pass


class JournalSchemaError(JournalError):
    pass


_ALLOWED_TYPES: dict[str, type[Any]] = {
    cls.__name__: cls
    for cls in (
        IdKind,
        SemanticId,
        AuthorityRole,
        AttestationKind,
        AuthorityRef,
        Attestation,
        EffectState,
        EffectMode,
        IdempotencyKind,
        CompletionSemantics,
        EvidenceKind,
        VerificationDecision,
        Admission,
        DispatchState,
        EventKind,
        WorldObjectRef,
        CapabilityRef,
        Precondition,
        VerificationPlan,
        EffectSpec,
        EffectRecord,
        DispatchRecord,
        EffectEvent,
        Observation,
        Artifact,
        BindingAdmission,
        Claim,
        EvidenceRef,
        Verification,
        Fact,
    )
}


def _encode(value: Any) -> Any:
    if isinstance(value, Enum):
        return {"$enum": type(value).__name__, "value": value.value}
    if is_dataclass(value) and not isinstance(value, type):
        return {
            "$dataclass": type(value).__name__,
            "fields": {field.name: _encode(getattr(value, field.name)) for field in fields(value)},
        }
    if isinstance(value, tuple):
        return {"$tuple": [_encode(item) for item in value]}
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("journal dictionaries require string keys")
        return {key: _encode(item) for key, item in value.items()}
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    raise TypeError(f"unsupported journal value: {type(value).__name__}")


def _decode(value: Any, *, schema_version: int) -> Any:
    if isinstance(value, list):
        return [_decode(item, schema_version=schema_version) for item in value]
    if not isinstance(value, dict):
        return value
    markers = {"$enum", "$dataclass", "$tuple"}.intersection(value)
    if len(markers) > 1:
        raise JournalSchemaError("journal value has conflicting type markers")
    if "$enum" in value:
        if set(value) != {"$enum", "value"}:
            raise JournalSchemaError("journal enum has unexpected fields")
        name = value.get("$enum")
        enum_type = _ALLOWED_TYPES.get(name)
        if enum_type is None or not issubclass(enum_type, Enum):
            raise JournalSchemaError(f"unknown journal enum: {name}")
        return enum_type(value.get("value"))
    if "$dataclass" in value:
        if set(value) != {"$dataclass", "fields"}:
            raise JournalSchemaError("journal dataclass has unexpected fields")
        name = value.get("$dataclass")
        data_type = _ALLOWED_TYPES.get(name)
        if data_type is None or not is_dataclass(data_type):
            raise JournalSchemaError(f"unknown journal dataclass: {name}")
        encoded_fields = value.get("fields")
        if not isinstance(encoded_fields, dict):
            raise JournalSchemaError(f"invalid journal dataclass fields: {name}")
        expected = {field.name for field in fields(data_type)}
        actual = set(encoded_fields)
        legacy_dispatch = (
            schema_version in _LEGACY_SCHEMA_VERSIONS
            and data_type is DispatchRecord
            and actual == expected - {"binding_id", "binding_digest"}
        )
        if actual != expected and not legacy_dispatch:
            raise JournalSchemaError(f"journal field mismatch for {name}")
        decoded_fields = {
            key: _decode(item, schema_version=schema_version)
            for key, item in encoded_fields.items()
        }
        if legacy_dispatch:
            decoded_fields["binding_id"] = None
            decoded_fields["binding_digest"] = None
        if schema_version == 2 and data_type in {
            CapabilityRef, Precondition, EffectSpec
        }:
            instance = object.__new__(data_type)
            for field in fields(data_type):
                object.__setattr__(instance, field.name, decoded_fields[field.name])
            return instance
        return data_type(**decoded_fields)
    if "$tuple" in value:
        if set(value) != {"$tuple"}:
            raise JournalSchemaError("journal tuple has unexpected fields")
        items = value.get("$tuple")
        if not isinstance(items, list):
            raise JournalSchemaError("invalid tuple payload")
        return tuple(_decode(item, schema_version=schema_version) for item in items)
    return {key: _decode(item, schema_version=schema_version) for key, item in value.items()}


def _canonical_command(
    operation: str,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    schema_version: int = JOURNAL_SCHEMA_VERSION,
) -> str:
    payload = {
        "schemaVersion": schema_version,
        "operation": operation,
        "args": _encode(args),
        "kwargs": _encode(kwargs),
    }
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _decode_command(payload_json: str) -> tuple[str, tuple[Any, ...], dict[str, Any]]:
    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError as error:
        raise JournalCorruption("journal entry is not valid JSON") from error
    if not isinstance(payload, dict):
        raise JournalSchemaError("journal command must be a JSON object")
    if set(payload) != {"schemaVersion", "operation", "args", "kwargs"}:
        raise JournalSchemaError("journal command has unexpected fields")
    schema_version = payload.get("schemaVersion")
    if schema_version not in _LEGACY_SCHEMA_VERSIONS | {JOURNAL_SCHEMA_VERSION}:
        raise JournalSchemaError("unsupported journal command schema")
    operation = payload.get("operation")
    if not isinstance(operation, str) or not operation:
        raise JournalSchemaError("journal command has no operation")
    args = _decode(payload.get("args"), schema_version=schema_version)
    kwargs = _decode(payload.get("kwargs"), schema_version=schema_version)
    if not isinstance(args, tuple) or not isinstance(kwargs, dict):
        raise JournalSchemaError("journal command arguments are invalid")
    return operation, args, kwargs


def _entry_digest(previous_digest: str, payload_json: str) -> str:
    material = f"{previous_digest}\n{payload_json}".encode("utf-8")
    return "sha256:" + hashlib.sha256(material).hexdigest()




class SQLiteSemanticJournal:
    """Append-only SQLite command journal with a verified hash chain."""

    def __init__(self, path: str | Path, authority_policy: AuthorityPolicy) -> None:
        self.path = Path(path)
        self._authority_policy = authority_policy
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.path)
        try:
            self._connection.execute("PRAGMA journal_mode=WAL")
            self._connection.execute("PRAGMA synchronous=FULL")
            self._connection.execute("PRAGMA foreign_keys=ON")
            self._connection.execute("PRAGMA busy_timeout=5000")
            self._initialize()
        except BaseException:
            self._connection.close()
            raise

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS journal_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS journal_entries (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                previous_digest TEXT NOT NULL,
                entry_digest TEXT NOT NULL UNIQUE,
                committed_at_ms INTEGER NOT NULL CHECK (committed_at_ms >= 0)
            );
            CREATE TRIGGER IF NOT EXISTS journal_entries_no_update
            BEFORE UPDATE ON journal_entries
            BEGIN
                SELECT RAISE(ABORT, 'journal entries are append-only');
            END;
            CREATE TRIGGER IF NOT EXISTS journal_entries_no_delete
            BEFORE DELETE ON journal_entries
            BEGIN
                SELECT RAISE(ABORT, 'journal entries are append-only');
            END;
            """
        )
        metadata = dict(
            self._connection.execute(
                "SELECT key, value FROM journal_metadata"
            ).fetchall()
        )
        stored_schema = metadata.get("schema_version")
        if stored_schema is None:
            metadata = {
                "schema_version": str(JOURNAL_SCHEMA_VERSION),
                "semantic_model_version": SEMANTIC_MODEL_VERSION,
                "reducer_version": REDUCER_VERSION,
                "authority_policy_fingerprint": self._authority_policy.fingerprint,
            }
            self._connection.executemany(
                "INSERT INTO journal_metadata(key, value) VALUES(?, ?)",
                tuple(metadata.items()),
            )
        else:
            try:
                stored_version = int(stored_schema)
            except ValueError as error:
                raise JournalSchemaError("journal schema version is not an integer") from error
            if stored_version in _LEGACY_SCHEMA_VERSIONS:
                legacy_model, legacy_reducer = _LEGACY_METADATA[stored_version]
                expected_legacy = {
                    "semantic_model_version": legacy_model,
                    "reducer_version": legacy_reducer,
                    "authority_policy_fingerprint": self._authority_policy.fingerprint,
                }
                for key, expected in expected_legacy.items():
                    if metadata.get(key) != expected:
                        raise JournalSchemaError(
                            f"legacy journal metadata {key} does not match runtime"
                        )
                self._connection.executemany(
                    "UPDATE journal_metadata SET value = ? WHERE key = ?",
                    (
                        (str(JOURNAL_SCHEMA_VERSION), "schema_version"),
                        (SEMANTIC_MODEL_VERSION, "semantic_model_version"),
                        (REDUCER_VERSION, "reducer_version"),
                    ),
                )
            elif stored_version == JOURNAL_SCHEMA_VERSION:
                expected_current = {
                    "semantic_model_version": SEMANTIC_MODEL_VERSION,
                    "reducer_version": REDUCER_VERSION,
                    "authority_policy_fingerprint": self._authority_policy.fingerprint,
                }
                for key, expected in expected_current.items():
                    if metadata.get(key) != expected:
                        raise JournalSchemaError(
                            f"journal metadata {key} does not match runtime"
                        )
            else:
                raise JournalSchemaError(
                    f"journal schema {stored_schema} is not supported by {JOURNAL_SCHEMA_VERSION}"
                )
        self._connection.commit()
        actual_head = self._actual_head()
        head_rows = dict(
            self._connection.execute(
                "SELECT key, value FROM journal_metadata "
                "WHERE key IN ('head_sequence', 'head_digest')"
            ).fetchall()
        )
        if not head_rows:
            if actual_head[0] != 0:
                raise JournalCorruption(
                    "non-empty journal has no durable head metadata"
                )
            self._connection.executemany(
                "INSERT INTO journal_metadata(key, value) VALUES(?, ?)",
                (
                    ("head_sequence", str(actual_head[0])),
                    ("head_digest", actual_head[1]),
                ),
            )
            self._connection.commit()
        elif set(head_rows) != {"head_sequence", "head_digest"}:
            raise JournalCorruption("journal head metadata is incomplete")
        elif (int(head_rows["head_sequence"]), head_rows["head_digest"]) != actual_head:
            raise JournalCorruption("journal durable head does not match stored tail")
        check = self._connection.execute("PRAGMA quick_check").fetchone()
        if check is None or check[0] != "ok":
            raise JournalCorruption(f"SQLite quick_check failed: {check}")

    def _actual_head(self) -> tuple[int, str]:
        row = self._connection.execute(
            "SELECT sequence, entry_digest FROM journal_entries ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return (0, _GENESIS_DIGEST)
        return (int(row[0]), str(row[1]))

    def _metadata_head(self) -> tuple[int, str]:
        rows = dict(
            self._connection.execute(
                "SELECT key, value FROM journal_metadata "
                "WHERE key IN ('head_sequence', 'head_digest')"
            ).fetchall()
        )
        if set(rows) != {"head_sequence", "head_digest"}:
            raise JournalCorruption("journal head metadata is incomplete")
        return (int(rows["head_sequence"]), str(rows["head_digest"]))

    @property
    def head(self) -> tuple[int, str]:
        actual = self._actual_head()
        marked = self._metadata_head()
        if actual != marked:
            raise JournalCorruption("journal durable head does not match stored tail")
        return actual

    def append(
        self,
        operation: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        *,
        expected_head: tuple[int, str] | None = None,
    ) -> int:
        return self.append_many(
            ((operation, args, kwargs),), expected_head=expected_head
        )[0]

    def append_many(
        self,
        commands: tuple[tuple[str, tuple[Any, ...], dict[str, Any]], ...],
        *,
        expected_head: tuple[int, str] | None = None,
    ) -> tuple[int, ...]:
        if not commands:
            return ()
        committed_at_ms = time.time_ns() // 1_000_000
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            row = self._connection.execute(
                "SELECT sequence, entry_digest FROM journal_entries ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            current_head = (
                (int(row[0]), str(row[1]))
                if row is not None
                else (0, _GENESIS_DIGEST)
            )
            if expected_head is not None and current_head != expected_head:
                raise JournalConflict(
                    f"journal head changed: expected {expected_head[0]}, found {current_head[0]}"
                )
            previous_digest = current_head[1]
            sequences: list[int] = []
            for operation, args, kwargs in commands:
                payload_json = _canonical_command(operation, args, kwargs)
                digest = _entry_digest(previous_digest, payload_json)
                cursor = self._connection.execute(
                    """
                    INSERT INTO journal_entries(
                        operation, payload_json, previous_digest, entry_digest, committed_at_ms
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (operation, payload_json, previous_digest, digest, committed_at_ms),
                )
                sequences.append(int(cursor.lastrowid))
                previous_digest = digest
            self._connection.execute(
                "UPDATE journal_metadata SET value = ? WHERE key = 'head_sequence'",
                (str(sequences[-1]),),
            )
            self._connection.execute(
                "UPDATE journal_metadata SET value = ? WHERE key = 'head_digest'",
                (previous_digest,),
            )
            self._connection.commit()
            return tuple(sequences)
        except BaseException:
            self._connection.rollback()
            raise

    def commands(
        self, *, after_sequence: int = 0
    ) -> tuple[tuple[int, str, tuple[Any, ...], dict[str, Any]], ...]:
        if after_sequence < 0:
            raise ValueError("after_sequence must be non-negative")
        rows = self._connection.execute(
            """
            SELECT sequence, operation, payload_json, previous_digest, entry_digest
            FROM journal_entries ORDER BY sequence
            """
        ).fetchall()
        expected_sequence = 1
        previous_digest = _GENESIS_DIGEST
        commands: list[tuple[int, str, tuple[Any, ...], dict[str, Any]]] = []
        for sequence, stored_operation, payload_json, stored_previous, stored_digest in rows:
            if sequence != expected_sequence:
                raise JournalCorruption(
                    f"journal sequence gap: expected {expected_sequence}, found {sequence}"
                )
            if stored_previous != previous_digest:
                raise JournalCorruption(f"journal hash predecessor mismatch at {sequence}")
            computed = _entry_digest(previous_digest, payload_json)
            if stored_digest != computed:
                raise JournalCorruption(f"journal entry digest mismatch at {sequence}")
            if sequence > after_sequence:
                operation, args, kwargs = _decode_command(payload_json)
                if operation != stored_operation:
                    raise JournalCorruption(f"journal operation mismatch at {sequence}")
                commands.append((sequence, operation, args, kwargs))
            previous_digest = stored_digest
            expected_sequence += 1
        reconstructed_head = (expected_sequence - 1, previous_digest)
        if reconstructed_head != self._metadata_head():
            raise JournalCorruption("journal command chain does not match durable head")
        if after_sequence > reconstructed_head[0]:
            raise JournalCorruption("checkpoint sequence exceeds journal head")
        return tuple(commands)

    @property
    def entry_count(self) -> int:
        row = self._connection.execute("SELECT COUNT(*) FROM journal_entries").fetchone()
        return int(row[0])

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "SQLiteSemanticJournal":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()


class JournalReducer:
    """Raw durable reducer backed by an append-only SQLite command journal."""

    _MUTATIONS = {
        "admit_effect",
        "admit_binding",
        "prepare_effect",
        "begin_dispatch",
        "admit_dispatch",
        "mark_dispatch_unknown",
        "reject_dispatch",
        "advance_effect",
        "record_observation",
        "register_artifact",
        "admit_claim",
        "record_verification",
        "commit_fact",
    }

    def __init__(self, path: str | Path, authority_policy: AuthorityPolicy) -> None:
        self._authority_policy = authority_policy
        self._journal = SQLiteSemanticJournal(path, authority_policy)
        self._kernel = ReferenceReducer(authority_policy)
        self._transaction_depth = 0
        self._transaction_commands: list[
            tuple[str, tuple[Any, ...], dict[str, Any]]
        ] = []
        self._head: tuple[int, str] = (0, _GENESIS_DIGEST)
        try:
            self._replay()
            self._head = self._journal.head
        except BaseException:
            self._journal.close()
            raise

    @property
    def authority_policy_fingerprint(self) -> str:
        return self._authority_policy.fingerprint

    def _replay(self) -> None:
        for sequence, operation, args, kwargs in self._journal.commands():
            if operation not in self._MUTATIONS:
                raise JournalCorruption(
                    f"unsupported operation {operation!r} at journal entry {sequence}"
                )
            try:
                getattr(self._kernel, operation)(*args, **kwargs)
            except BaseException as error:
                raise JournalCorruption(
                    f"semantic replay failed at entry {sequence} ({operation})"
                ) from error
        self._kernel.validate_invariants()

    def _commit(self, operation: str, *args: Any, **kwargs: Any) -> Any:
        if self._transaction_depth:
            before = self._kernel.mutation_serial
            result = getattr(self._kernel, operation)(*args, **kwargs)
            if self._kernel.mutation_serial != before:
                self._transaction_commands.append((operation, args, kwargs))
            return result
        with self._kernel.transaction():
            before = self._kernel.mutation_serial
            result = getattr(self._kernel, operation)(*args, **kwargs)
            if self._kernel.mutation_serial == before:
                return result
            self._journal.append(
                operation, args, kwargs, expected_head=self._head
            )
            self._head = self._journal.head
            return result

    @contextmanager
    def transaction(self) -> Iterator["JournalReducer"]:
        outermost = self._transaction_depth == 0
        saved_command_count = len(self._transaction_commands)
        if outermost:
            self._transaction_commands = []
        self._transaction_depth += 1
        try:
            with self._kernel.transaction():
                yield self
                if outermost:
                    commands = tuple(self._transaction_commands)
                    if commands:
                        self._journal.append_many(
                            commands, expected_head=self._head
                        )
                        self._head = self._journal.head
        except BaseException:
            del self._transaction_commands[saved_command_count:]
            raise
        finally:
            self._transaction_depth -= 1
            if outermost:
                self._transaction_commands = []

    def admit_effect(
        self,
        spec: EffectSpec,
        *,
        event_id: SemanticId,
        recorded_at_ms: int,
        attestation: Attestation,
    ) -> Admission:
        return self._commit(
            "admit_effect",
            spec,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            attestation=attestation,
        )

    def admit_binding(self, binding: BindingAdmission) -> Admission:
        return self._commit("admit_binding", binding)

    def prepare_effect(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        attestation: Attestation,
    ) -> EffectRecord:
        return self._commit(
            "prepare_effect",
            effect_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            attestation=attestation,
        )

    def begin_dispatch(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        dispatch_id: SemanticId,
        event_id: SemanticId,
        recorded_at_ms: int,
        request_digest: str,
        attestation: Attestation,
        binding_id: SemanticId | None = None,
        binding_digest: str | None = None,
    ) -> EffectRecord:
        kwargs: dict[str, Any] = {
            "expected_revision": expected_revision,
            "dispatch_id": dispatch_id,
            "event_id": event_id,
            "recorded_at_ms": recorded_at_ms,
            "request_digest": request_digest,
            "attestation": attestation,
        }
        if binding_id is not None or binding_digest is not None:
            kwargs["binding_id"] = binding_id
            kwargs["binding_digest"] = binding_digest
        return self._commit("begin_dispatch", effect_id, **kwargs)

    def admit_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        backend_operation_id: str,
        evidence_digest: str,
        attestation: Attestation,
    ) -> EffectRecord:
        return self._commit(
            "admit_dispatch",
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            backend_operation_id=backend_operation_id,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

    def mark_dispatch_unknown(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str,
        attestation: Attestation,
    ) -> EffectRecord:
        return self._commit(
            "mark_dispatch_unknown",
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

    def reject_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        reason_code: str,
        retryable: bool,
        evidence_digest: str,
        attestation: Attestation,
    ) -> EffectRecord:
        return self._commit(
            "reject_dispatch",
            effect_id,
            dispatch_id,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            reason_code=reason_code,
            retryable=retryable,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

    def advance_effect(
        self,
        effect_id: SemanticId,
        target: EffectState,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str | None = None,
        attestation: Attestation,
    ) -> EffectRecord:
        return self._commit(
            "advance_effect",
            effect_id,
            target,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
            attestation=attestation,
        )

    def _view_kernel(self) -> ReferenceReducer:
        return self._kernel

    def get_effect(self, effect_id: SemanticId) -> EffectRecord:
        return self._view_kernel().get_effect(effect_id)

    def get_dispatch(self, dispatch_id: SemanticId) -> DispatchRecord:
        return self._view_kernel().get_dispatch(dispatch_id)

    def get_binding(self, binding_id: SemanticId) -> BindingAdmission:
        return self._view_kernel().get_binding(binding_id)

    def bindings_for(self, effect_id: SemanticId) -> tuple[BindingAdmission, ...]:
        return self._view_kernel().bindings_for(effect_id)

    def current_binding_for(self, effect_id: SemanticId) -> BindingAdmission | None:
        return self._view_kernel().current_binding_for(effect_id)

    def events_for(self, effect_id: SemanticId) -> tuple[EffectEvent, ...]:
        return self._view_kernel().events_for(effect_id)

    def observations_for(self, effect_id: SemanticId) -> tuple[Observation, ...]:
        return self._view_kernel().observations_for(effect_id)

    def artifacts_for(self, effect_id: SemanticId) -> tuple[Artifact, ...]:
        return self._view_kernel().artifacts_for(effect_id)

    def get_observation(self, observation_id: SemanticId) -> Observation:
        return self._view_kernel().get_observation(observation_id)

    def get_artifact(self, artifact_id: SemanticId) -> Artifact:
        return self._view_kernel().get_artifact(artifact_id)

    def get_claim(self, claim_id: SemanticId) -> Claim:
        return self._view_kernel().get_claim(claim_id)

    def get_verification(self, verification_id: SemanticId) -> Verification:
        return self._view_kernel().get_verification(verification_id)

    def get_fact(self, fact_id: SemanticId) -> Fact:
        return self._view_kernel().get_fact(fact_id)

    def record_observation(self, observation: Observation) -> Admission:
        return self._commit("record_observation", observation)

    def register_artifact(self, artifact: Artifact) -> Admission:
        return self._commit("register_artifact", artifact)

    def admit_claim(
        self, claim: Claim, *, proposed_at_ms: int
    ) -> Admission:
        return self._commit(
            "admit_claim", claim, proposed_at_ms=proposed_at_ms
        )

    def record_verification(self, verification: Verification) -> Admission:
        return self._commit("record_verification", verification)

    def commit_fact(self, fact: Fact) -> Admission:
        return self._commit("commit_fact", fact)

    def validate_invariants(self) -> None:
        self._view_kernel().validate_invariants()
        self._journal.commands()

    def verify_from_genesis(self) -> None:
        candidate = ReferenceReducer(self._authority_policy)
        for sequence, operation, args, kwargs in self._journal.commands():
            if operation not in self._MUTATIONS:
                raise JournalCorruption(
                    f"unsupported operation {operation!r} at journal entry {sequence}"
                )
            try:
                getattr(candidate, operation)(*args, **kwargs)
            except BaseException as error:
                raise JournalCorruption(
                    f"genesis replay failed at entry {sequence} ({operation})"
                ) from error
        candidate.validate_invariants()
        if candidate.state_snapshot() != self._kernel.state_snapshot():
            raise JournalCorruption(
                "checkpoint projection does not match genesis replay"
            )

    @property
    def journal_entry_count(self) -> int:
        return self._journal.entry_count

    def close(self) -> None:
        self._journal.close()

    def __enter__(self) -> "JournalReducer":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()


# Backward-compatible internal name for existing tests and experiments.
JournalKernel = JournalReducer
