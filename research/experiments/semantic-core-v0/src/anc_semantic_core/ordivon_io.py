from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Any, Callable, Protocol

from .identity import IdKind, SemanticId
from .errors import InvalidTransition
from .interfaces import ExecutionView
from .model import EffectMode, Observation, WorldObjectRef
from .state import EffectState
from .transport import ToolCallError, ToolRejected


class ToolCaller(Protocol):
    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]: ...


class ReadMode(StrEnum):
    FULL = "FULL"
    SLICE = "SLICE"


class MutationMode(StrEnum):
    WRITE = "WRITE"
    APPEND = "APPEND"
    REPLACE_EXACT = "REPLACE_EXACT"


@dataclass(frozen=True, slots=True)
class OrdivonRead:
    workspace_id: str
    relative_path: str
    mode: ReadMode = ReadMode.FULL
    max_bytes: int = 4_194_304
    offset: int = 0

    def __post_init__(self) -> None:
        _validate_workspace_id(self.workspace_id)
        _validate_relative_path(self.relative_path)
        if not 1 <= self.max_bytes <= 4_194_304:
            raise ValueError("read max_bytes is outside the Ordivon contract")
        if self.offset < 0:
            raise ValueError("read offset must be non-negative")
        if self.mode is ReadMode.FULL and self.offset != 0:
            raise ValueError("FULL read must begin at offset zero")

    def as_tool_arguments(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "workspaceId": self.workspace_id,
            "relativePath": self.relative_path,
            "mode": self.mode.value,
            "offset": self.offset,
            "maxBytes": self.max_bytes,
        }


@dataclass(frozen=True, slots=True)
class OrdivonMutation:
    workspace_id: str
    relative_path: str
    mode: MutationMode
    content: str
    expected_digest: str
    expected_text: str | None = None

    def __post_init__(self) -> None:
        _validate_workspace_id(self.workspace_id)
        _validate_relative_path(self.relative_path)
        if not self.expected_digest.startswith("sha256:"):
            raise ValueError("mutation requires a sha256 expected_digest")
        if self.mode is MutationMode.REPLACE_EXACT:
            if not self.expected_text:
                raise ValueError("REPLACE_EXACT requires non-empty expected_text")
        elif self.expected_text is not None:
            raise ValueError("expected_text is only valid for REPLACE_EXACT")

    def as_tool_arguments(self) -> dict[str, Any]:
        mutation: dict[str, Any] = {
            "relativePath": self.relative_path,
            "mode": self.mode.value,
            "content": self.content,
            "expectedDigest": self.expected_digest,
        }
        if self.expected_text is not None:
            mutation["expectedText"] = self.expected_text
        return {
            "schemaVersion": 1,
            "workspaceId": self.workspace_id,
            "mutations": [mutation],
        }


@dataclass(frozen=True, slots=True)
class IoProjection:
    state: EffectState
    dispatch_id: SemanticId
    observation: Observation | None
    payload: dict[str, Any] | None
    receipt_id: str | None = None
    error_code: str | None = None
    error_message: str | None = None


class OrdivonIoAdapter:
    """Bind versioned file reads and one-file atomic mutations to Ordivon Tools."""

    def __init__(
        self,
        kernel: ExecutionView,
        client: ToolCaller,
        *,
        clock_ms: Callable[[], int] | None = None,
    ) -> None:
        self._kernel = kernel
        self._client = client
        self._clock_ms = clock_ms or (lambda: time.time_ns() // 1_000_000)

    def dispatch_read(self, effect_id: SemanticId, request: OrdivonRead) -> IoProjection:
        record = self._validate_effect(
            effect_id,
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            target=ordivon_file_object_id(request.workspace_id, request.relative_path),
        )
        arguments = request.as_tool_arguments()
        dispatch_id = self._begin(effect_id, record.revision, "workspace.read", arguments)
        try:
            payload = self._client.call_tool("workspace.read", arguments)
        except ToolRejected as error:
            return self._reject(effect_id, dispatch_id, error)
        except ToolCallError as error:
            return self._unknown(effect_id, dispatch_id, error)
        try:
            content, content_digest = _validate_read_payload(payload)
        except (TypeError, ValueError) as error:
            return self._unknown(effect_id, dispatch_id, error)
        payload_digest = _digest(payload)
        receipt_id = (
            f"ordivon-receipt:workspace.read:{dispatch_id.value}:"
            f"{payload_digest.removeprefix('sha256:')}"
        )
        return self._commit_read_projection(
            effect_id=effect_id,
            dispatch_id=dispatch_id,
            request=request,
            payload=payload,
            content=content,
            content_digest=content_digest,
            payload_digest=payload_digest,
            receipt_id=receipt_id,
        )

    def _commit_read_projection(
        self,
        *,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        request: OrdivonRead,
        payload: dict[str, Any],
        content: str,
        content_digest: str,
        payload_digest: str,
        receipt_id: str,
    ) -> IoProjection:
        with self._kernel.transaction():
            self._admit(effect_id, dispatch_id, receipt_id, payload_digest)
            observation = Observation(
                observation_id=_observation_id(dispatch_id, payload_digest),
                effect_id=effect_id,
                dispatch_id=dispatch_id,
                target=WorldObjectRef(
                    ordivon_file_object_id(request.workspace_id, request.relative_path),
                    version=content_digest,
                ),
                observed_at_ms=self._clock_ms(),
                source="ordivon:mcp/workspace.read",
                payload_digest=payload_digest,
            )
            self._kernel.record_observation(observation)
            observation = self._kernel.get_observation(observation.observation_id)
            current = self._kernel.get_effect(effect_id)
            expected_version = current.spec.target.version
            if expected_version is not None and content_digest != expected_version:
                current = self._kernel.advance_effect(
                    effect_id,
                    EffectState.FAILED,
                    expected_revision=current.revision,
                    event_id=self._event_id(effect_id, "version-mismatch"),
                    recorded_at_ms=self._clock_ms(),
                    evidence_digest=_digest(
                        {
                            "expectedDigest": expected_version,
                            "observedDigest": content_digest,
                        }
                    ),
                )
                return IoProjection(
                    state=current.state,
                    dispatch_id=dispatch_id,
                    observation=observation,
                    payload=dict(payload),
                    receipt_id=receipt_id,
                    error_code="VERSION_MISMATCH",
                    error_message="observed file digest does not match the requested version",
                )
            current = self._kernel.advance_effect(
                effect_id,
                EffectState.SUCCEEDED,
                expected_revision=current.revision,
                event_id=self._event_id(effect_id, "read-succeeded"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=payload_digest,
            )
            self._kernel.validate_invariants()
            return IoProjection(
                state=current.state,
                dispatch_id=dispatch_id,
                observation=observation,
                payload={"content": content, "digest": content_digest},
                receipt_id=receipt_id,
            )

    def dispatch_mutation(
        self,
        effect_id: SemanticId,
        request: OrdivonMutation,
    ) -> IoProjection:
        record = self._validate_effect(
            effect_id,
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            target=ordivon_file_object_id(request.workspace_id, request.relative_path),
        )
        if record.spec.target.version != request.expected_digest:
            raise ValueError("Effect target version must equal mutation expected_digest")
        arguments = request.as_tool_arguments()
        dispatch_id = self._begin(effect_id, record.revision, "workspace.mutate", arguments)
        try:
            payload = self._client.call_tool("workspace.mutate", arguments)
        except ToolRejected as error:
            if _proves_mutation_not_admitted(error):
                return self._reject(effect_id, dispatch_id, error)
            return self._unknown(effect_id, dispatch_id, error)
        except ToolCallError as error:
            return self._unknown(effect_id, dispatch_id, error)
        try:
            after_digest = _validate_mutation_payload(payload, request.relative_path)
        except (TypeError, ValueError) as error:
            return self._unknown(effect_id, dispatch_id, error)
        payload_digest = _digest(payload)
        receipt_id = (
            f"ordivon-receipt:workspace.mutate:{dispatch_id.value}:"
            f"{payload_digest.removeprefix('sha256:')}"
        )
        return self._commit_mutation_projection(
            effect_id=effect_id,
            dispatch_id=dispatch_id,
            request=request,
            payload=payload,
            after_digest=after_digest,
            payload_digest=payload_digest,
            receipt_id=receipt_id,
        )

    def _commit_mutation_projection(
        self,
        *,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        request: OrdivonMutation,
        payload: dict[str, Any],
        after_digest: str,
        payload_digest: str,
        receipt_id: str,
    ) -> IoProjection:
        with self._kernel.transaction():
            self._admit(effect_id, dispatch_id, receipt_id, payload_digest)
            observation = Observation(
                observation_id=_observation_id(dispatch_id, payload_digest),
                effect_id=effect_id,
                dispatch_id=dispatch_id,
                target=WorldObjectRef(
                    ordivon_file_object_id(request.workspace_id, request.relative_path),
                    version=after_digest,
                ),
                observed_at_ms=self._clock_ms(),
                source="ordivon:mcp/workspace.mutate",
                payload_digest=payload_digest,
            )
            self._kernel.record_observation(observation)
            observation = self._kernel.get_observation(observation.observation_id)
            current = self._kernel.get_effect(effect_id)
            current = self._kernel.advance_effect(
                effect_id,
                EffectState.SUCCEEDED,
                expected_revision=current.revision,
                event_id=self._event_id(effect_id, "mutation-accepted"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=payload_digest,
            )
            self._kernel.validate_invariants()
            return IoProjection(
                state=current.state,
                dispatch_id=dispatch_id,
                observation=observation,
                payload=dict(payload),
                receipt_id=receipt_id,
            )

    def _validate_effect(
        self,
        effect_id: SemanticId,
        *,
        operation: str,
        mode: EffectMode,
        target: SemanticId,
    ):
        record = self._kernel.get_effect(effect_id)
        if record.state is not EffectState.PREPARED:
            raise InvalidTransition("only a prepared Effect may cross the Tool boundary")
        semantic_action = {
            "workspace.read": "anc.object.read.v1",
            "workspace.mutate": "anc.object.replace-if-version.v1",
        }[operation]
        if record.spec.capability.operation not in {semantic_action, operation}:
            raise ValueError(f"Effect semantic action must be {semantic_action}")
        if record.spec.mode is not mode:
            raise ValueError(f"Effect mode must be {mode.value}")
        if record.spec.target.object_id != target:
            raise ValueError("Effect target does not match the Ordivon file")
        return record

    def _begin(
        self,
        effect_id: SemanticId,
        revision: int,
        operation: str,
        arguments: dict[str, Any],
    ) -> SemanticId:
        request_digest = _digest(arguments)
        digest = hashlib.sha256(str(effect_id).encode("utf-8")).hexdigest()[:16]
        dispatch_id = SemanticId(
            IdKind.DISPATCH,
            f"ordivon-io:{digest}:r{revision + 1}",
        )
        self._kernel.begin_dispatch(
            effect_id,
            expected_revision=revision,
            dispatch_id=dispatch_id,
            event_id=self._event_id(effect_id, f"{operation}-dispatch"),
            recorded_at_ms=self._clock_ms(),
            request_digest=request_digest,
        )
        return dispatch_id

    def _admit(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        receipt_id: str,
        evidence_digest: str,
    ) -> None:
        record = self._kernel.get_effect(effect_id)
        self._kernel.admit_dispatch(
            effect_id,
            dispatch_id,
            expected_revision=record.revision,
            event_id=self._event_id(effect_id, "sync-receipt"),
            recorded_at_ms=self._clock_ms(),
            backend_operation_id=receipt_id,
            evidence_digest=evidence_digest,
        )

    def _reject(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        error: ToolRejected,
    ) -> IoProjection:
        record = self._kernel.get_effect(effect_id)
        record = self._kernel.reject_dispatch(
            effect_id,
            dispatch_id,
            expected_revision=record.revision,
            event_id=self._event_id(effect_id, "tool-rejected"),
            recorded_at_ms=self._clock_ms(),
            reason_code=error.code,
            retryable=error.retryable,
            evidence_digest=_digest(
                {
                    "code": error.code,
                    "message": error.message,
                    "field": error.field,
                    "retryable": error.retryable,
                }
            ),
        )
        self._kernel.validate_invariants()
        return IoProjection(
            state=record.state,
            dispatch_id=dispatch_id,
            observation=None,
            payload=None,
            error_code=error.code,
            error_message=error.message,
        )

    def _unknown(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        error: Exception,
    ) -> IoProjection:
        record = self._kernel.get_effect(effect_id)
        record = self._kernel.mark_dispatch_unknown(
            effect_id,
            dispatch_id,
            expected_revision=record.revision,
            event_id=self._event_id(effect_id, "outcome-unknown"),
            recorded_at_ms=self._clock_ms(),
            evidence_digest=_digest(
                {"errorType": type(error).__name__, "message": str(error)}
            ),
        )
        self._kernel.validate_invariants()
        return IoProjection(
            state=record.state,
            dispatch_id=dispatch_id,
            observation=None,
            payload=None,
            error_code=type(error).__name__,
            error_message=str(error),
        )

    def _event_id(self, effect_id: SemanticId, label: str) -> SemanticId:
        revision = self._kernel.get_effect(effect_id).revision + 1
        digest = hashlib.sha256(str(effect_id).encode("utf-8")).hexdigest()[:16]
        return SemanticId(IdKind.EVENT, f"ordivon-io:{digest}:{revision}:{label}")


def ordivon_file_object_id(workspace_id: str, relative_path: str) -> SemanticId:
    _validate_workspace_id(workspace_id)
    normalized = _validate_relative_path(relative_path)
    return SemanticId(
        IdKind.WORLD_OBJECT,
        f"ordivon-file:{workspace_id}:{normalized}",
    )


def _validate_workspace_id(workspace_id: str) -> None:
    if not workspace_id or workspace_id.strip() != workspace_id:
        raise ValueError("workspace identity must be non-empty and trimmed")


def _validate_relative_path(relative_path: str) -> str:
    if not relative_path or relative_path.startswith("/") or "\\" in relative_path:
        raise ValueError("file path must be a non-empty POSIX relative path")
    path = PurePosixPath(relative_path)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("file path must not contain empty, dot, or parent segments")
    normalized = str(path)
    if normalized != relative_path:
        raise ValueError("file path must already be normalized")
    return normalized


def _validate_read_payload(payload: dict[str, Any]) -> tuple[str, str]:
    content = payload.get("content")
    digest = payload.get("digest")
    if not isinstance(content, str) or not isinstance(digest, str):
        raise TypeError("workspace.read returned incomplete structured content")
    calculated = f"sha256:{hashlib.sha256(content.encode('utf-8')).hexdigest()}"
    if calculated != digest:
        raise ValueError("workspace.read content does not match its reported digest")
    return content, digest


def _validate_mutation_payload(payload: dict[str, Any], relative_path: str) -> str:
    mutations = payload.get("mutations")
    if not isinstance(mutations, list) or len(mutations) != 1:
        raise TypeError("workspace.mutate returned an invalid receipt array")
    receipt = mutations[0]
    if not isinstance(receipt, dict) or receipt.get("relativePath") != relative_path:
        raise ValueError("workspace.mutate receipt targets the wrong file")
    after_digest = receipt.get("afterDigest")
    byte_length = receipt.get("byteLength")
    if not isinstance(after_digest, str) or not after_digest.startswith("sha256:"):
        raise TypeError("workspace.mutate receipt lacks afterDigest")
    if not isinstance(byte_length, int) or byte_length < 0:
        raise TypeError("workspace.mutate receipt has invalid byteLength")
    return after_digest


def _proves_mutation_not_admitted(error: ToolRejected) -> bool:
    return error.code == "INVALID_REQUEST" and (
        error.field is None or error.field.startswith("mutations[")
    )


def _observation_id(dispatch_id: SemanticId, payload_digest: str) -> SemanticId:
    suffix = payload_digest.removeprefix("sha256:")[:24]
    return SemanticId(IdKind.OBSERVATION, f"{dispatch_id.value}:{suffix}")


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"
