from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .identity import IdKind, SemanticId
from .kernel import InvalidTransition, SemanticKernel
from .transport import ToolCallError, ToolProtocolError, ToolRejected
from .model import Admission, Artifact, Observation
from .state import EffectState


class ToolCaller(Protocol):
    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class OrdivonExecution:
    workspace_id: str
    executable: str
    args: tuple[str, ...] = ()
    cwd_relative: str = "."
    env: dict[str, str] = field(default_factory=dict)
    timeout_ms: int = 30_000
    stdout_limit_bytes: int = 65_536
    stderr_limit_bytes: int = 65_536

    def __post_init__(self) -> None:
        if not self.workspace_id:
            raise ValueError("workspace identity must not be empty")
        if not self.executable.startswith("/"):
            raise ValueError("Ordivon executable must be absolute")
        if not self.cwd_relative or self.cwd_relative.startswith("/"):
            raise ValueError("Ordivon cwd must be relative")
        if min(self.timeout_ms, self.stdout_limit_bytes, self.stderr_limit_bytes) <= 0:
            raise ValueError("Ordivon execution bounds must be positive")

    def as_tool_arguments(
        self,
        client_request_id: str,
        *,
        wait_ms: int,
        stdout_tail_bytes: int,
        stderr_tail_bytes: int,
    ) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "clientRequestId": client_request_id,
            "execution": {
                "workspaceId": self.workspace_id,
                "executable": self.executable,
                "args": list(self.args),
                "cwdRelative": self.cwd_relative,
                "env": dict(self.env),
                "timeoutMs": self.timeout_ms,
                "stdoutLimitBytes": self.stdout_limit_bytes,
                "stderrLimitBytes": self.stderr_limit_bytes,
            },
            "waitMs": wait_ms,
            "stdoutTailBytes": stdout_tail_bytes,
            "stderrTailBytes": stderr_tail_bytes,
        }


@dataclass(frozen=True, slots=True)
class OrdivonBinding:
    effect_id: SemanticId
    dispatch_id: SemanticId
    client_request_id: str
    workspace_id: str
    job_id: str
    attempt_id: str | None


@dataclass(frozen=True, slots=True)
class AdapterProjection:
    state: EffectState
    binding: OrdivonBinding | None
    observation: Observation | None
    artifacts: tuple[Artifact, ...]
    payload: dict[str, Any] | None
    error_code: str | None = None
    error_message: str | None = None


@dataclass(frozen=True, slots=True)
class _PendingDispatch:
    effect_id: SemanticId
    dispatch_id: SemanticId
    client_request_id: str
    workspace_id: str
    request_digest: str
    dispatched_at_ms: int


def ordivon_workspace_object_id(workspace_id: str) -> SemanticId:
    if not workspace_id:
        raise ValueError("workspace identity must not be empty")
    return SemanticId(IdKind.WORLD_OBJECT, f"ordivon-workspace:{workspace_id}")


def _workspace_id_from_object(object_id: SemanticId) -> str:
    object_id.require(IdKind.WORLD_OBJECT)
    prefix = "ordivon-workspace:"
    if not object_id.value.startswith(prefix):
        raise ValueError("Effect target is not an Ordivon Workspace object")
    workspace_id = object_id.value.removeprefix(prefix)
    if not workspace_id:
        raise ValueError("Ordivon Workspace object has no identity")
    return workspace_id


def semantic_state_from_status(status: str) -> EffectState:
    mapping = {
        "queued": EffectState.DISPATCHED,
        "working": EffectState.RUNNING,
        "succeeded": EffectState.SUCCEEDED,
        "failed": EffectState.FAILED,
        "timed_out": EffectState.FAILED,
        "cancelled": EffectState.CANCELLED,
        "lost": EffectState.UNKNOWN,
        "orphaned": EffectState.UNKNOWN,
        "unknown": EffectState.UNKNOWN,
    }
    try:
        return mapping[status]
    except KeyError as error:
        raise ValueError(f"unknown Ordivon public status: {status}") from error


class OrdivonSemanticAdapter:
    """Bind semantic Effects to Ordivon's public MCP contract without reading private state."""

    def __init__(
        self,
        kernel: SemanticKernel,
        client: ToolCaller,
        *,
        clock_ms: Callable[[], int] | None = None,
    ) -> None:
        self._kernel = kernel
        self._client = client
        self._clock_ms = clock_ms or (lambda: time.time_ns() // 1_000_000)
        self._pending: dict[SemanticId, _PendingDispatch] = {}
        self._bindings: dict[SemanticId, OrdivonBinding] = {}

    def dispatch_exec(
        self,
        effect_id: SemanticId,
        execution: OrdivonExecution,
        *,
        wait_ms: int = 0,
        stdout_tail_bytes: int = 4096,
        stderr_tail_bytes: int = 4096,
    ) -> AdapterProjection:
        record = self._kernel.get_effect(effect_id)
        if record.spec.operation != "workspace.exec":
            raise ValueError("Ordivon exec adapter requires operation workspace.exec")
        expected_target = ordivon_workspace_object_id(execution.workspace_id)
        if record.spec.target.object_id != expected_target:
            raise ValueError("Effect target does not match the Ordivon Workspace")
        if record.state is not EffectState.PREPARED:
            raise InvalidTransition("only a prepared Effect may cross the Ordivon boundary")
        client_request_id = _client_request_id(effect_id)
        dispatch_id = SemanticId(
            IdKind.DISPATCH,
            f"ordivon:{client_request_id}:r{record.revision + 1}",
        )
        arguments = execution.as_tool_arguments(
            client_request_id,
            wait_ms=wait_ms,
            stdout_tail_bytes=stdout_tail_bytes,
            stderr_tail_bytes=stderr_tail_bytes,
        )
        request_digest = _digest(arguments)
        dispatched_at_ms = self._clock_ms()
        self._kernel.begin_dispatch(
            effect_id,
            expected_revision=record.revision,
            dispatch_id=dispatch_id,
            event_id=self._event_id(effect_id, "dispatch"),
            recorded_at_ms=dispatched_at_ms,
            request_digest=request_digest,
        )
        self._pending[effect_id] = _PendingDispatch(
            effect_id=effect_id,
            dispatch_id=dispatch_id,
            client_request_id=client_request_id,
            workspace_id=execution.workspace_id,
            request_digest=request_digest,
            dispatched_at_ms=dispatched_at_ms,
        )
        try:
            payload = self._client.call_tool("workspace.exec", arguments)
        except ToolRejected as error:
            try:
                binding = self._find_binding(effect_id)
            except ToolCallError as lookup_error:
                return self._mark_unknown(effect_id, lookup_error)
            if binding is not None:
                try:
                    return self._observe_binding(
                        effect_id,
                        binding,
                        wait_ms=wait_ms,
                        stdout_tail_bytes=stdout_tail_bytes,
                        stderr_tail_bytes=stderr_tail_bytes,
                    )
                except ToolCallError as observe_error:
                    return self._mark_unknown(effect_id, observe_error)
            return self._mark_rejected(effect_id, error)
        except ToolCallError as error:
            return self._mark_unknown(effect_id, error)
        return self._apply_payload(effect_id, payload, source="workspace.exec")

    def cancel(
        self,
        effect_id: SemanticId,
        *,
        wait_ms: int = 0,
        stdout_tail_bytes: int = 4096,
        stderr_tail_bytes: int = 4096,
    ) -> AdapterProjection:
        record = self._kernel.get_effect(effect_id)
        if record.state.terminal:
            raise InvalidTransition("terminal Effect cannot accept cancellation intent")
        if record.state not in {
            EffectState.DISPATCHED,
            EffectState.RUNNING,
            EffectState.CANCEL_REQUESTED,
        }:
            raise InvalidTransition(
                "cancellation requires a dispatched or running Effect"
            )
        try:
            binding = self._bindings.get(effect_id)
            if binding is None:
                binding = self._find_binding(effect_id)
            if binding is None:
                return self._mark_unknown(
                    effect_id,
                    ToolProtocolError(
                        "no Ordivon Job matched the cancellation target"
                    ),
                )
            if record.state is not EffectState.CANCEL_REQUESTED:
                record = self._kernel.advance_effect(
                    effect_id,
                    EffectState.CANCEL_REQUESTED,
                    expected_revision=record.revision,
                    event_id=self._event_id(effect_id, "cancel-requested"),
                    recorded_at_ms=self._clock_ms(),
                    evidence_digest=_digest(
                        {
                            "jobId": binding.job_id,
                            "intent": "cancel",
                        }
                    ),
                )
            try:
                payload = self._client.call_tool(
                    "task.cancel",
                    {
                        "schemaVersion": 1,
                        "jobId": binding.job_id,
                    },
                )
            except ToolRejected:
                # A natural terminal outcome may win before cancellation is applied.
                return self._observe_binding(
                    effect_id,
                    binding,
                    wait_ms=wait_ms,
                    stdout_tail_bytes=stdout_tail_bytes,
                    stderr_tail_bytes=stderr_tail_bytes,
                )
            return self._apply_payload(
                effect_id,
                payload,
                source="task.cancel",
            )
        except ToolCallError as error:
            return self._mark_unknown(effect_id, error)

    def observe(
        self,
        effect_id: SemanticId,
        *,
        wait_ms: int = 0,
        stdout_tail_bytes: int = 4096,
        stderr_tail_bytes: int = 4096,
    ) -> AdapterProjection:
        record = self._kernel.get_effect(effect_id)
        if record.state not in {
            EffectState.DISPATCHED,
            EffectState.RUNNING,
            EffectState.CANCEL_REQUESTED,
        }:
            raise InvalidTransition(
                "observation requires a dispatched, running, or cancel-requested Effect"
            )
        try:
            binding = self._bindings.get(effect_id)
            if binding is None:
                binding = self._find_binding(effect_id)
            if binding is None:
                return self._mark_unknown(
                    effect_id,
                    ToolProtocolError(
                        "no Ordivon Job matched the committed request identity"
                    ),
                )
            return self._observe_binding(
                effect_id,
                binding,
                wait_ms=wait_ms,
                stdout_tail_bytes=stdout_tail_bytes,
                stderr_tail_bytes=stderr_tail_bytes,
            )
        except ToolCallError as error:
            return self._mark_unknown(effect_id, error)

    def _observe_binding(
        self,
        effect_id: SemanticId,
        binding: OrdivonBinding,
        *,
        wait_ms: int,
        stdout_tail_bytes: int,
        stderr_tail_bytes: int,
    ) -> AdapterProjection:
        payload = self._client.call_tool(
            "task.observe",
            {
                "schemaVersion": 1,
                "jobId": binding.job_id,
                "waitMs": wait_ms,
                "stdoutTailBytes": stdout_tail_bytes,
                "stderrTailBytes": stderr_tail_bytes,
            },
        )
        return self._apply_payload(effect_id, payload, source="task.observe")

    def _mark_unknown(self, effect_id: SemanticId, error: ToolCallError) -> AdapterProjection:
        record = self._kernel.get_effect(effect_id)
        if record.dispatch_id is None:
            raise InvalidTransition("Effect has no committed Ordivon Dispatch")
        if record.state is not EffectState.UNKNOWN:
            record = self._kernel.mark_dispatch_unknown(
                effect_id,
                record.dispatch_id,
                expected_revision=record.revision,
                event_id=self._event_id(effect_id, "outcome-unknown"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=_digest(
                    {"errorType": type(error).__name__, "message": str(error)}
                ),
            )
        return AdapterProjection(
            state=record.state,
            binding=self._bindings.get(effect_id),
            observation=None,
            artifacts=(),
            payload=None,
            error_code=type(error).__name__,
            error_message=str(error),
        )

    def _mark_rejected(
        self,
        effect_id: SemanticId,
        error: ToolRejected,
    ) -> AdapterProjection:
        record = self._kernel.get_effect(effect_id)
        if record.dispatch_id is None:
            raise InvalidTransition("Effect has no committed Ordivon Dispatch")
        rejected_dispatch_id = record.dispatch_id
        record = self._kernel.reject_dispatch(
            effect_id,
            rejected_dispatch_id,
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
        return AdapterProjection(
            state=record.state,
            binding=None,
            observation=None,
            artifacts=(),
            payload=None,
            error_code=error.code,
            error_message=error.message,
        )

    def reconcile(
        self,
        effect_id: SemanticId,
        *,
        wait_ms: int = 0,
        stdout_tail_bytes: int = 4096,
        stderr_tail_bytes: int = 4096,
    ) -> AdapterProjection:
        record = self._kernel.get_effect(effect_id)
        if record.state is EffectState.UNKNOWN:
            record = self._kernel.advance_effect(
                effect_id,
                EffectState.RECONCILING,
                expected_revision=record.revision,
                event_id=self._event_id(effect_id, "reconcile"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=_digest({"method": "task.list+task.observe"}),
            )
        elif record.state is not EffectState.RECONCILING:
            raise InvalidTransition("reconciliation requires unknown or reconciling state")
        try:
            binding = self._bindings.get(effect_id)
            if binding is None:
                binding = self._find_binding(effect_id)
        except ToolCallError as error:
            return self._mark_unknown(effect_id, error)
        if binding is None:
            current = self._kernel.get_effect(effect_id)
            if current.dispatch_id is None:
                raise InvalidTransition("Effect has no committed Ordivon Dispatch")
            current = self._kernel.mark_dispatch_unknown(
                effect_id,
                current.dispatch_id,
                expected_revision=current.revision,
                event_id=self._event_id(effect_id, "not-found"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=_digest({"result": "no-correlated-job"}),
            )
            return AdapterProjection(
                state=current.state,
                binding=None,
                observation=None,
                artifacts=(),
                payload=None,
                error_code="JOB_NOT_CORRELATED",
                error_message="no Ordivon Job matched the committed request identity",
            )
        try:
            return self._observe_binding(
                effect_id,
                binding,
                wait_ms=wait_ms,
                stdout_tail_bytes=stdout_tail_bytes,
                stderr_tail_bytes=stderr_tail_bytes,
            )
        except ToolCallError as error:
            return self._mark_unknown(effect_id, error)

    def binding_for(self, effect_id: SemanticId) -> OrdivonBinding | None:
        return self._bindings.get(effect_id)

    def _pending_for(
        self,
        effect_id: SemanticId,
    ) -> _PendingDispatch | None:
        pending = self._pending.get(effect_id)
        if pending is not None:
            return pending
        record = self._kernel.get_effect(effect_id)
        if record.dispatch_id is None:
            return None
        dispatch = self._kernel.get_dispatch(record.dispatch_id)
        workspace_id = _workspace_id_from_object(record.spec.target.object_id)
        pending = _PendingDispatch(
            effect_id=effect_id,
            dispatch_id=record.dispatch_id,
            client_request_id=_client_request_id(effect_id),
            workspace_id=workspace_id,
            request_digest=dispatch.request_digest,
            dispatched_at_ms=dispatch.started_at_ms,
        )
        self._pending[effect_id] = pending
        return pending

    def _find_binding(self, effect_id: SemanticId) -> OrdivonBinding | None:
        pending = self._pending_for(effect_id)
        if pending is None:
            raise InvalidTransition("Effect has no committed Ordivon dispatch")
        cursor: dict[str, Any] | None = None
        matches: list[dict[str, Any]] = []
        earliest_relevant_ms = max(0, pending.dispatched_at_ms - 5_000)
        for _ in range(100):
            arguments: dict[str, Any] = {"limit": 100}
            if cursor is not None:
                arguments["cursor"] = cursor
            page = self._client.call_tool("task.list", arguments)
            jobs = page.get("jobs")
            if not isinstance(jobs, list):
                raise ValueError("Ordivon task.list returned no jobs array")
            typed_jobs = [job for job in jobs if isinstance(job, dict)]
            matches.extend(
                job
                for job in typed_jobs
                if job.get("clientRequestId") == pending.client_request_id
            )
            if matches:
                break
            created_times = [
                job.get("createdAtMs")
                for job in typed_jobs
                if isinstance(job.get("createdAtMs"), int)
            ]
            if created_times and min(created_times) < earliest_relevant_ms:
                break
            next_cursor = page.get("nextCursor")
            if not isinstance(next_cursor, dict):
                break
            cursor = next_cursor
        if not matches:
            return None
        job_ids = {job.get("jobId") for job in matches}
        if len(job_ids) != 1 or None in job_ids:
            raise ValueError("client request identity resolved to conflicting Ordivon Jobs")
        return self._bind(effect_id, matches[0])

    def _apply_payload(
        self,
        effect_id: SemanticId,
        payload: dict[str, Any],
        *,
        source: str,
    ) -> AdapterProjection:
        binding = self._bind(effect_id, payload)
        status = payload.get("status")
        if not isinstance(status, str):
            raise ValueError("Ordivon observation has no status")
        projected = semantic_state_from_status(status)
        payload_digest = _digest(payload)
        observation = Observation(
            observation_id=_observation_id(
                effect_id,
                binding.dispatch_id,
                source,
                payload_digest,
            ),
            effect_id=effect_id,
            dispatch_id=binding.dispatch_id,
            target=self._kernel.get_effect(effect_id).spec.target,
            observed_at_ms=self._clock_ms(),
            source=f"ordivon:mcp/{source}",
            payload_digest=payload_digest,
        )
        self._kernel.record_observation(observation)
        artifacts = tuple(self._artifacts(binding, payload))
        for artifact in artifacts:
            self._kernel.register_artifact(artifact)
        current = self._kernel.get_effect(effect_id)
        target = projected
        if current.state is EffectState.RECONCILING and target is EffectState.DISPATCHED:
            target = EffectState.RUNNING
        if target is EffectState.UNKNOWN:
            if current.dispatch_id is None:
                raise InvalidTransition("observed Effect has no committed Dispatch")
            if current.state is not EffectState.UNKNOWN:
                current = self._kernel.mark_dispatch_unknown(
                    effect_id,
                    current.dispatch_id,
                    expected_revision=current.revision,
                    event_id=self._event_id(effect_id, "observe-unknown"),
                    recorded_at_ms=self._clock_ms(),
                    evidence_digest=payload_digest,
                )
        elif (
            current.state is EffectState.CANCEL_REQUESTED
            and target is EffectState.RUNNING
        ):
            target = EffectState.CANCEL_REQUESTED
        elif target is not current.state:
            current = self._kernel.advance_effect(
                effect_id,
                target,
                expected_revision=current.revision,
                event_id=self._event_id(effect_id, f"observe-{target.value}"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=payload_digest,
            )
        self._kernel.validate_invariants()
        return AdapterProjection(
            state=current.state,
            binding=binding,
            observation=observation,
            artifacts=artifacts,
            payload=dict(payload),
        )

    def _bind(self, effect_id: SemanticId, payload: dict[str, Any]) -> OrdivonBinding:
        pending = self._pending_for(effect_id)
        if pending is None:
            raise InvalidTransition("Effect has no committed Ordivon dispatch")
        job_id = payload.get("jobId")
        if not isinstance(job_id, str) or not job_id:
            raise ValueError("Ordivon payload has no Job identity")
        attempt_id = payload.get("attemptId")
        if attempt_id is not None and not isinstance(attempt_id, str):
            raise ValueError("Ordivon Attempt identity is invalid")
        workspace_id = payload.get("workspaceId", pending.workspace_id)
        if workspace_id != pending.workspace_id:
            raise ValueError("Ordivon payload belongs to a different Workspace")
        binding = OrdivonBinding(
            effect_id=effect_id,
            dispatch_id=pending.dispatch_id,
            client_request_id=pending.client_request_id,
            workspace_id=pending.workspace_id,
            job_id=job_id,
            attempt_id=attempt_id,
        )
        existing = self._bindings.get(effect_id)
        if existing is not None and existing.job_id != binding.job_id:
            raise ValueError("one Effect resolved to multiple Ordivon Jobs")
        current = self._kernel.get_effect(effect_id)
        self._kernel.admit_dispatch(
            effect_id,
            pending.dispatch_id,
            expected_revision=current.revision,
            event_id=self._event_id(effect_id, "backend-admitted"),
            recorded_at_ms=self._clock_ms(),
            backend_operation_id=job_id,
            evidence_digest=_digest(
                {
                    "jobId": job_id,
                    "attemptId": attempt_id,
                    "clientRequestId": pending.client_request_id,
                }
            ),
        )
        self._bindings[effect_id] = binding
        return binding

    def _artifacts(
        self,
        binding: OrdivonBinding,
        payload: dict[str, Any],
    ) -> list[Artifact]:
        raw = payload.get("artifacts", [])
        if not isinstance(raw, list):
            raise ValueError("Ordivon artifacts must be an array")
        artifacts: list[Artifact] = []
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError("Ordivon Artifact descriptor must be an object")
            artifact_id = item.get("artifactId")
            kind = item.get("kind")
            digest = item.get("digest")
            retained_bytes = item.get("retainedBytes")
            if not isinstance(artifact_id, str) or not artifact_id:
                raise ValueError("Ordivon Artifact identity is missing")
            if not isinstance(kind, str) or not isinstance(digest, str):
                raise ValueError("Ordivon Artifact descriptor is incomplete")
            if not isinstance(retained_bytes, int) or retained_bytes < 0:
                raise ValueError("Ordivon Artifact byte length is invalid")
            artifacts.append(
                Artifact(
                    artifact_id=SemanticId(
                        IdKind.ARTIFACT,
                        f"ordivon:{binding.job_id}:{artifact_id}",
                    ),
                    effect_id=binding.effect_id,
                    dispatch_id=binding.dispatch_id,
                    kind=kind,
                    digest=digest,
                    media_type="application/octet-stream",
                    byte_length=retained_bytes,
                    created_at_ms=self._clock_ms(),
                )
            )
        return artifacts

    def _event_id(self, effect_id: SemanticId, label: str) -> SemanticId:
        revision = self._kernel.get_effect(effect_id).revision + 1
        digest = hashlib.sha256(str(effect_id).encode("utf-8")).hexdigest()[:16]
        return SemanticId(IdKind.EVENT, f"ordivon:{digest}:{revision}:{label}")


def _observation_id(
    effect_id: SemanticId,
    dispatch_id: SemanticId,
    source: str,
    payload_digest: str,
) -> SemanticId:
    digest = hashlib.sha256(
        f"{effect_id}|{dispatch_id}|{source}|{payload_digest}".encode("utf-8")
    ).hexdigest()[:32]
    return SemanticId(IdKind.OBSERVATION, f"ordivon:{digest}")


def _client_request_id(effect_id: SemanticId) -> str:
    digest = hashlib.sha256(str(effect_id).encode("utf-8")).hexdigest()[:32]
    return f"anc-effect-{digest}"


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"
