from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Callable

from .errors import InvalidTransition
from .identity import IdKind, SemanticId
from .interfaces import ExecutionView
from .model import Artifact, EffectMode, Observation, WorldObjectRef
from .state import EffectState


class SimulatorStatus(StrEnum):
    ACCEPTED = "accepted"
    ACTIVE = "active"
    COMPLETE = "complete"
    ERROR = "error"
    ABORTED = "aborted"
    INDETERMINATE = "indeterminate"


class SimulatorError(RuntimeError):
    pass


class SimulatorResponseLost(SimulatorError):
    """The backend accepted a request but its response was not delivered."""


class SimulatorInspectionError(SimulatorError):
    """The backend cannot currently return a trustworthy Job observation."""


class SimulatorRejected(SimulatorError):
    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.retryable = retryable


@dataclass(frozen=True, slots=True)
class SimulatorArtifact:
    name: str
    kind: str
    content: bytes
    media_type: str = "application/octet-stream"

    def __post_init__(self) -> None:
        if not self.name or not self.kind or not self.media_type:
            raise ValueError("simulator Artifact metadata must not be empty")

    @property
    def digest(self) -> str:
        return _sha256_bytes(self.content)


@dataclass(frozen=True, slots=True)
class SimulatorJobRequest:
    object_key: str
    action: str
    status_plan: tuple[SimulatorStatus, ...]
    artifacts: tuple[SimulatorArtifact, ...] = ()
    inspection_failures: int = 0

    def __post_init__(self) -> None:
        _validate_object_key(self.object_key)
        if not self.action:
            raise ValueError("simulator Job action must not be empty")
        if not self.status_plan:
            raise ValueError("simulator Job requires a status plan")
        if self.inspection_failures < 0:
            raise ValueError("simulator inspection failure count must be non-negative")


@dataclass(frozen=True, slots=True)
class SimulatorRead:
    object_key: str

    def __post_init__(self) -> None:
        _validate_object_key(self.object_key)


@dataclass(frozen=True, slots=True)
class SimulatorMutation:
    object_key: str
    expected_version: str
    content: str

    def __post_init__(self) -> None:
        _validate_object_key(self.object_key)
        if not self.expected_version.startswith("sha256:"):
            raise ValueError("simulator mutation requires a sha256 expected version")


@dataclass(frozen=True, slots=True)
class SimulatorReadReceipt:
    receipt_id: str
    object_key: str
    content: str
    version: str


@dataclass(frozen=True, slots=True)
class SimulatorMutationReceipt:
    receipt_id: str
    object_key: str
    before_version: str
    after_version: str
    byte_length: int


@dataclass(frozen=True, slots=True)
class SimulatorJobSnapshot:
    operation_id: str
    correlation_key: str
    object_key: str
    status: SimulatorStatus
    artifacts: tuple[SimulatorArtifact, ...]
    cancellation_requested: bool


@dataclass(slots=True)
class _SimulatorJob:
    operation_id: str
    correlation_key: str
    object_key: str
    status_plan: tuple[SimulatorStatus, ...]
    artifacts: tuple[SimulatorArtifact, ...]
    inspection_failures: int
    position: int = 0
    cancellation_requested: bool = False

    def snapshot(self) -> SimulatorJobSnapshot:
        status = (
            SimulatorStatus.ABORTED
            if self.cancellation_requested
            else self.status_plan[self.position]
        )
        artifacts = self.artifacts if status is SimulatorStatus.COMPLETE else ()
        return SimulatorJobSnapshot(
            operation_id=self.operation_id,
            correlation_key=self.correlation_key,
            object_key=self.object_key,
            status=status,
            artifacts=artifacts,
            cancellation_requested=self.cancellation_requested,
        )


class DeterministicBackend:
    """A deterministic non-Ordivon execution substrate used for portability tests."""

    def __init__(self) -> None:
        self._objects: dict[str, str] = {}
        self._jobs: dict[str, _SimulatorJob] = {}
        self._operation_by_correlation: dict[str, str] = {}
        self._launch_counts: dict[str, int] = {}
        self._next_operation = 1
        self._next_receipt = 1
        self.lose_next_launch_response = False

    def seed_object(self, object_key: str, content: str) -> None:
        _validate_object_key(object_key)
        self._objects[object_key] = content

    def object_content(self, object_key: str) -> str:
        try:
            return self._objects[object_key]
        except KeyError as error:
            raise SimulatorRejected("NOT_FOUND", "object does not exist") from error

    def object_version(self, object_key: str) -> str:
        return _sha256_text(self.object_content(object_key))

    def read(self, request: SimulatorRead) -> SimulatorReadReceipt:
        content = self.object_content(request.object_key)
        return SimulatorReadReceipt(
            receipt_id=self._receipt_id("read"),
            object_key=request.object_key,
            content=content,
            version=_sha256_text(content),
        )

    def mutate(self, request: SimulatorMutation) -> SimulatorMutationReceipt:
        before_content = self.object_content(request.object_key)
        before_version = _sha256_text(before_content)
        if before_version != request.expected_version:
            raise SimulatorRejected(
                "VERSION_CONFLICT",
                "object version does not match the guarded mutation",
                retryable=False,
            )
        self._objects[request.object_key] = request.content
        return SimulatorMutationReceipt(
            receipt_id=self._receipt_id("mutation"),
            object_key=request.object_key,
            before_version=before_version,
            after_version=_sha256_text(request.content),
            byte_length=len(request.content.encode("utf-8")),
        )

    def launch(
        self, correlation_key: str, request: SimulatorJobRequest
    ) -> SimulatorJobSnapshot:
        if correlation_key in self._operation_by_correlation:
            raise SimulatorRejected(
                "DUPLICATE_CORRELATION",
                "correlation key already identifies one backend operation",
            )
        operation_id = f"sim-operation-{self._next_operation:06d}"
        self._next_operation += 1
        job = _SimulatorJob(
            operation_id=operation_id,
            correlation_key=correlation_key,
            object_key=request.object_key,
            status_plan=request.status_plan,
            artifacts=request.artifacts,
            inspection_failures=request.inspection_failures,
        )
        self._jobs[operation_id] = job
        self._operation_by_correlation[correlation_key] = operation_id
        self._launch_counts[correlation_key] = self._launch_counts.get(correlation_key, 0) + 1
        snapshot = job.snapshot()
        if self.lose_next_launch_response:
            self.lose_next_launch_response = False
            raise SimulatorResponseLost("launch response lost after backend admission")
        return snapshot

    def lookup(self, correlation_key: str) -> SimulatorJobSnapshot | None:
        operation_id = self._operation_by_correlation.get(correlation_key)
        if operation_id is None:
            return None
        return self._jobs[operation_id].snapshot()

    def inspect(self, operation_id: str) -> SimulatorJobSnapshot:
        try:
            job = self._jobs[operation_id]
        except KeyError as error:
            raise SimulatorRejected("NOT_FOUND", "backend operation does not exist") from error
        if job.inspection_failures:
            job.inspection_failures -= 1
            raise SimulatorInspectionError("deterministic inspection fault")
        if not job.cancellation_requested and job.position + 1 < len(job.status_plan):
            job.position += 1
        return job.snapshot()

    def request_cancel(self, operation_id: str) -> None:
        try:
            job = self._jobs[operation_id]
        except KeyError as error:
            raise SimulatorRejected("NOT_FOUND", "backend operation does not exist") from error
        job.cancellation_requested = True

    def launch_count(self, correlation_key: str) -> int:
        return self._launch_counts.get(correlation_key, 0)

    def _receipt_id(self, kind: str) -> str:
        receipt_id = f"sim-receipt-{kind}-{self._next_receipt:06d}"
        self._next_receipt += 1
        return receipt_id


@dataclass(frozen=True, slots=True)
class SimulatorBinding:
    effect_id: SemanticId
    dispatch_id: SemanticId
    correlation_key: str
    operation_id: str
    object_key: str


@dataclass(frozen=True, slots=True)
class SimulatorProjection:
    state: EffectState
    dispatch_id: SemanticId
    binding: SimulatorBinding | None
    observation: Observation | None
    artifacts: tuple[Artifact, ...]
    receipt_id: str | None = None
    error_code: str | None = None
    error_message: str | None = None


class DeterministicBackendAdapter:
    """Translate the deterministic backend contract into Semantic Core records."""

    READ_OPERATION = "simulator.object.read"
    MUTATION_OPERATION = "simulator.object.mutate"
    JOB_OPERATION = "simulator.job.launch"

    def __init__(
        self,
        kernel: ExecutionView,
        backend: DeterministicBackend,
        *,
        clock_ms: Callable[[], int] | None = None,
    ) -> None:
        self._kernel = kernel
        self._backend = backend
        self._clock_ms = clock_ms or (lambda: time.time_ns() // 1_000_000)
        self._bindings: dict[SemanticId, SimulatorBinding] = {}

    def dispatch_read(
        self, effect_id: SemanticId, request: SimulatorRead
    ) -> SimulatorProjection:
        record = self._validate_effect(
            effect_id,
            operation=self.READ_OPERATION,
            mode=EffectMode.OBSERVE,
            object_key=request.object_key,
        )
        dispatch_id = self._begin(
            effect_id,
            record.revision,
            {"method": "fetch", "object": request.object_key},
        )
        try:
            receipt = self._backend.read(request)
        except SimulatorRejected as error:
            return self._reject(effect_id, dispatch_id, error)
        except SimulatorError as error:
            return self._unknown(effect_id, dispatch_id, error)
        calculated = _sha256_text(receipt.content)
        if calculated != receipt.version:
            return self._unknown(
                effect_id,
                dispatch_id,
                SimulatorInspectionError("read receipt content/version mismatch"),
            )
        payload = {
            "receipt": receipt.receipt_id,
            "object": receipt.object_key,
            "version": receipt.version,
            "content": receipt.content,
        }
        payload_digest = _digest(payload)
        with self._kernel.transaction():
            self._admit(
                effect_id,
                dispatch_id,
                backend_operation_id=receipt.receipt_id,
                evidence_digest=payload_digest,
            )
            observation = self._record_observation(
                effect_id,
                dispatch_id,
                request.object_key,
                version=receipt.version,
                source="simulator:fetch",
                payload_digest=payload_digest,
            )
            current = self._kernel.get_effect(effect_id)
            expected_version = current.spec.target.version
            if expected_version is not None and expected_version != receipt.version:
                current = self._kernel.advance_effect(
                    effect_id,
                    EffectState.FAILED,
                    expected_revision=current.revision,
                    event_id=self._event_id(effect_id, "version-mismatch"),
                    recorded_at_ms=self._clock_ms(),
                    evidence_digest=_digest(
                        {"expected": expected_version, "observed": receipt.version}
                    ),
                )
                return SimulatorProjection(
                    state=current.state,
                    dispatch_id=dispatch_id,
                    binding=None,
                    observation=observation,
                    artifacts=(),
                    receipt_id=receipt.receipt_id,
                    error_code="VERSION_MISMATCH",
                    error_message="observed object version differs from requested version",
                )
            current = self._kernel.advance_effect(
                effect_id,
                EffectState.SUCCEEDED,
                expected_revision=current.revision,
                event_id=self._event_id(effect_id, "read-succeeded"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=payload_digest,
            )
            return SimulatorProjection(
                state=current.state,
                dispatch_id=dispatch_id,
                binding=None,
                observation=observation,
                artifacts=(),
                receipt_id=receipt.receipt_id,
            )

    def dispatch_mutation(
        self, effect_id: SemanticId, request: SimulatorMutation
    ) -> SimulatorProjection:
        record = self._validate_effect(
            effect_id,
            operation=self.MUTATION_OPERATION,
            mode=EffectMode.CHANGE,
            object_key=request.object_key,
        )
        if record.spec.target.version != request.expected_version:
            raise ValueError("Effect target version must equal mutation expected version")
        dispatch_id = self._begin(
            effect_id,
            record.revision,
            {
                "method": "replace_if_version",
                "object": request.object_key,
                "expected": request.expected_version,
                "contentDigest": _sha256_text(request.content),
            },
        )
        try:
            receipt = self._backend.mutate(request)
        except SimulatorRejected as error:
            return self._reject(effect_id, dispatch_id, error)
        except SimulatorError as error:
            return self._unknown(effect_id, dispatch_id, error)
        expected_after = _sha256_text(request.content)
        if receipt.after_version != expected_after:
            return self._unknown(
                effect_id,
                dispatch_id,
                SimulatorInspectionError("mutation receipt has the wrong resulting version"),
            )
        payload = {
            "receipt": receipt.receipt_id,
            "object": receipt.object_key,
            "before": receipt.before_version,
            "after": receipt.after_version,
            "bytes": receipt.byte_length,
        }
        payload_digest = _digest(payload)
        with self._kernel.transaction():
            self._admit(
                effect_id,
                dispatch_id,
                backend_operation_id=receipt.receipt_id,
                evidence_digest=payload_digest,
            )
            observation = self._record_observation(
                effect_id,
                dispatch_id,
                request.object_key,
                version=receipt.after_version,
                source="simulator:replace_if_version",
                payload_digest=payload_digest,
            )
            current = self._kernel.get_effect(effect_id)
            current = self._kernel.advance_effect(
                effect_id,
                EffectState.SUCCEEDED,
                expected_revision=current.revision,
                event_id=self._event_id(effect_id, "mutation-succeeded"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=payload_digest,
            )
            return SimulatorProjection(
                state=current.state,
                dispatch_id=dispatch_id,
                binding=None,
                observation=observation,
                artifacts=(),
                receipt_id=receipt.receipt_id,
            )

    def dispatch_job(
        self, effect_id: SemanticId, request: SimulatorJobRequest
    ) -> SimulatorProjection:
        record = self._validate_effect(
            effect_id,
            operation=self.JOB_OPERATION,
            mode=EffectMode.CHANGE,
            object_key=request.object_key,
        )
        correlation_key = _correlation_key(effect_id)
        dispatch_id = self._begin(
            effect_id,
            record.revision,
            {
                "method": "launch",
                "correlation": correlation_key,
                "object": request.object_key,
                "action": request.action,
                "statusPlan": [status.value for status in request.status_plan],
                "artifacts": [
                    {
                        "name": artifact.name,
                        "kind": artifact.kind,
                        "digest": artifact.digest,
                        "bytes": len(artifact.content),
                    }
                    for artifact in request.artifacts
                ],
            },
        )
        try:
            snapshot = self._backend.launch(correlation_key, request)
        except SimulatorRejected as error:
            return self._reject(effect_id, dispatch_id, error)
        except SimulatorError as error:
            return self._unknown(effect_id, dispatch_id, error)
        return self._apply_snapshot(effect_id, snapshot, source="launch")

    def observe(self, effect_id: SemanticId) -> SimulatorProjection:
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
            binding = self._binding_for(effect_id)
            if binding is None:
                return self._unknown(
                    effect_id,
                    self._require_dispatch_id(effect_id),
                    SimulatorInspectionError("no operation matched the Effect correlation"),
                )
            snapshot = self._backend.inspect(binding.operation_id)
        except SimulatorError as error:
            return self._unknown(
                effect_id,
                self._require_dispatch_id(effect_id),
                error,
            )
        return self._apply_snapshot(effect_id, snapshot, source="inspect")

    def reconcile(self, effect_id: SemanticId) -> SimulatorProjection:
        record = self._kernel.get_effect(effect_id)
        if record.state is EffectState.UNKNOWN:
            record = self._kernel.advance_effect(
                effect_id,
                EffectState.RECONCILING,
                expected_revision=record.revision,
                event_id=self._event_id(effect_id, "reconcile"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=_digest({"method": "lookup+inspect"}),
            )
        elif record.state is not EffectState.RECONCILING:
            raise InvalidTransition("reconciliation requires unknown or reconciling state")
        try:
            binding = self._binding_for(effect_id)
            if binding is None:
                return self._unknown(
                    effect_id,
                    self._require_dispatch_id(effect_id),
                    SimulatorInspectionError("no operation matched the Effect correlation"),
                )
            snapshot = self._backend.inspect(binding.operation_id)
        except SimulatorError as error:
            return self._unknown(
                effect_id,
                self._require_dispatch_id(effect_id),
                error,
            )
        return self._apply_snapshot(effect_id, snapshot, source="reconcile")

    def cancel(self, effect_id: SemanticId) -> SimulatorProjection:
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
        binding = self._binding_for(effect_id)
        if binding is None:
            return self._unknown(
                effect_id,
                self._require_dispatch_id(effect_id),
                SimulatorInspectionError("no operation matched the cancellation target"),
            )
        if record.state is not EffectState.CANCEL_REQUESTED:
            record = self._kernel.advance_effect(
                effect_id,
                EffectState.CANCEL_REQUESTED,
                expected_revision=record.revision,
                event_id=self._event_id(effect_id, "cancel-requested"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=_digest(
                    {"operation": binding.operation_id, "intent": "cancel"}
                ),
            )
        try:
            self._backend.request_cancel(binding.operation_id)
        except SimulatorError as error:
            return SimulatorProjection(
                state=record.state,
                dispatch_id=binding.dispatch_id,
                binding=binding,
                observation=None,
                artifacts=(),
                error_code=type(error).__name__,
                error_message=str(error),
            )
        return SimulatorProjection(
            state=record.state,
            dispatch_id=binding.dispatch_id,
            binding=binding,
            observation=None,
            artifacts=(),
        )

    def binding_for(self, effect_id: SemanticId) -> SimulatorBinding | None:
        return self._binding_for(effect_id)

    def delivery_count(self, effect_id: SemanticId) -> int:
        return self._backend.launch_count(_correlation_key(effect_id))

    def _validate_effect(
        self,
        effect_id: SemanticId,
        *,
        operation: str,
        mode: EffectMode,
        object_key: str,
    ):
        record = self._kernel.get_effect(effect_id)
        if record.state is not EffectState.PREPARED:
            raise InvalidTransition("only a prepared Effect may cross the simulator boundary")
        if record.spec.operation != operation:
            raise ValueError(f"Effect operation must be {operation}")
        if record.spec.mode is not mode:
            raise ValueError(f"Effect mode must be {mode.value}")
        if record.spec.target.object_id != simulator_object_id(object_key):
            raise ValueError("Effect target does not match the simulator object")
        return record

    def _begin(
        self,
        effect_id: SemanticId,
        revision: int,
        request_payload: dict[str, Any],
    ) -> SemanticId:
        digest = hashlib.sha256(str(effect_id).encode("utf-8")).hexdigest()[:16]
        dispatch_id = SemanticId(
            IdKind.DISPATCH, f"simulator:{digest}:r{revision + 1}"
        )
        self._kernel.begin_dispatch(
            effect_id,
            expected_revision=revision,
            dispatch_id=dispatch_id,
            event_id=self._event_id(effect_id, "dispatch"),
            recorded_at_ms=self._clock_ms(),
            request_digest=_digest(request_payload),
        )
        return dispatch_id

    def _admit(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        backend_operation_id: str,
        evidence_digest: str,
    ) -> None:
        current = self._kernel.get_effect(effect_id)
        self._kernel.admit_dispatch(
            effect_id,
            dispatch_id,
            expected_revision=current.revision,
            event_id=self._event_id(effect_id, "backend-admitted"),
            recorded_at_ms=self._clock_ms(),
            backend_operation_id=backend_operation_id,
            evidence_digest=evidence_digest,
        )

    def _apply_snapshot(
        self,
        effect_id: SemanticId,
        snapshot: SimulatorJobSnapshot,
        *,
        source: str,
    ) -> SimulatorProjection:
        with self._kernel.transaction():
            binding = self._bind(effect_id, snapshot)
            payload = {
                "operation": snapshot.operation_id,
                "correlation": snapshot.correlation_key,
                "object": snapshot.object_key,
                "phase": snapshot.status.value,
                "cancelRequested": snapshot.cancellation_requested,
                "artifacts": [
                    {
                        "name": artifact.name,
                        "kind": artifact.kind,
                        "digest": artifact.digest,
                        "bytes": len(artifact.content),
                    }
                    for artifact in snapshot.artifacts
                ],
            }
            payload_digest = _digest(payload)
            observation = self._record_observation(
                effect_id,
                binding.dispatch_id,
                snapshot.object_key,
                version=None,
                source=f"simulator:{source}",
                payload_digest=payload_digest,
            )
            artifact_drafts = tuple(
                Artifact(
                    artifact_id=SemanticId(
                        IdKind.ARTIFACT,
                        f"simulator:{snapshot.operation_id}:{artifact.name}",
                    ),
                    effect_id=effect_id,
                    dispatch_id=binding.dispatch_id,
                    kind=artifact.kind,
                    digest=artifact.digest,
                    media_type=artifact.media_type,
                    byte_length=len(artifact.content),
                    created_at_ms=self._clock_ms(),
                )
                for artifact in snapshot.artifacts
            )
            for artifact in artifact_drafts:
                self._kernel.register_artifact(artifact)
            artifacts = tuple(
                self._kernel.get_artifact(artifact.artifact_id)
                for artifact in artifact_drafts
            )
            current = self._kernel.get_effect(effect_id)
            target = simulator_state(snapshot.status)
            if current.state is EffectState.RECONCILING and target is EffectState.DISPATCHED:
                target = EffectState.RUNNING
            if target is EffectState.UNKNOWN:
                if current.state is not EffectState.UNKNOWN:
                    current = self._kernel.mark_dispatch_unknown(
                        effect_id,
                        binding.dispatch_id,
                        expected_revision=current.revision,
                        event_id=self._event_id(effect_id, "observed-unknown"),
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
                    event_id=self._event_id(effect_id, f"observed-{target.value}"),
                    recorded_at_ms=self._clock_ms(),
                    evidence_digest=payload_digest,
                )
            return SimulatorProjection(
                state=current.state,
                dispatch_id=binding.dispatch_id,
                binding=binding,
                observation=observation,
                artifacts=artifacts,
            )

    def _bind(
        self, effect_id: SemanticId, snapshot: SimulatorJobSnapshot
    ) -> SimulatorBinding:
        dispatch_id = self._require_dispatch_id(effect_id)
        expected_correlation = _correlation_key(effect_id)
        if snapshot.correlation_key != expected_correlation:
            raise SimulatorInspectionError("backend snapshot has the wrong correlation")
        expected_object = _object_key_from_id(
            self._kernel.get_effect(effect_id).spec.target.object_id
        )
        if snapshot.object_key != expected_object:
            raise SimulatorInspectionError("backend snapshot has the wrong object")
        binding = SimulatorBinding(
            effect_id=effect_id,
            dispatch_id=dispatch_id,
            correlation_key=snapshot.correlation_key,
            operation_id=snapshot.operation_id,
            object_key=snapshot.object_key,
        )
        existing = self._bindings.get(effect_id)
        if existing is not None and existing.operation_id != binding.operation_id:
            raise SimulatorInspectionError("one Effect resolved to multiple operations")
        self._admit(
            effect_id,
            dispatch_id,
            backend_operation_id=snapshot.operation_id,
            evidence_digest=_digest(
                {
                    "operation": snapshot.operation_id,
                    "correlation": snapshot.correlation_key,
                }
            ),
        )
        self._bindings[effect_id] = binding
        return binding

    def _binding_for(self, effect_id: SemanticId) -> SimulatorBinding | None:
        existing = self._bindings.get(effect_id)
        if existing is not None:
            return existing
        snapshot = self._backend.lookup(_correlation_key(effect_id))
        if snapshot is None:
            return None
        return self._bind(effect_id, snapshot)

    def _record_observation(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        object_key: str,
        *,
        version: str | None,
        source: str,
        payload_digest: str,
    ) -> Observation:
        token = hashlib.sha256(
            f"{effect_id}|{dispatch_id}|{source}|{payload_digest}".encode("utf-8")
        ).hexdigest()[:32]
        observation = Observation(
            observation_id=SemanticId(IdKind.OBSERVATION, f"simulator:{token}"),
            effect_id=effect_id,
            dispatch_id=dispatch_id,
            target=WorldObjectRef(simulator_object_id(object_key), version=version),
            observed_at_ms=self._clock_ms(),
            source=source,
            payload_digest=payload_digest,
        )
        self._kernel.record_observation(observation)
        return self._kernel.get_observation(observation.observation_id)

    def _reject(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        error: SimulatorRejected,
    ) -> SimulatorProjection:
        current = self._kernel.get_effect(effect_id)
        current = self._kernel.reject_dispatch(
            effect_id,
            dispatch_id,
            expected_revision=current.revision,
            event_id=self._event_id(effect_id, "backend-rejected"),
            recorded_at_ms=self._clock_ms(),
            reason_code=error.code,
            retryable=error.retryable,
            evidence_digest=_digest(
                {
                    "code": error.code,
                    "message": error.message,
                    "retryable": error.retryable,
                }
            ),
        )
        return SimulatorProjection(
            state=current.state,
            dispatch_id=dispatch_id,
            binding=None,
            observation=None,
            artifacts=(),
            error_code=error.code,
            error_message=error.message,
        )

    def _unknown(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        error: Exception,
    ) -> SimulatorProjection:
        current = self._kernel.get_effect(effect_id)
        if current.state is not EffectState.UNKNOWN:
            current = self._kernel.mark_dispatch_unknown(
                effect_id,
                dispatch_id,
                expected_revision=current.revision,
                event_id=self._event_id(effect_id, "outcome-unknown"),
                recorded_at_ms=self._clock_ms(),
                evidence_digest=_digest(
                    {"errorType": type(error).__name__, "message": str(error)}
                ),
            )
        return SimulatorProjection(
            state=current.state,
            dispatch_id=dispatch_id,
            binding=self._bindings.get(effect_id),
            observation=None,
            artifacts=(),
            error_code=type(error).__name__,
            error_message=str(error),
        )

    def _require_dispatch_id(self, effect_id: SemanticId) -> SemanticId:
        dispatch_id = self._kernel.get_effect(effect_id).dispatch_id
        if dispatch_id is None:
            raise InvalidTransition("Effect has no committed simulator Dispatch")
        return dispatch_id

    def _event_id(self, effect_id: SemanticId, label: str) -> SemanticId:
        revision = self._kernel.get_effect(effect_id).revision + 1
        digest = hashlib.sha256(str(effect_id).encode("utf-8")).hexdigest()[:16]
        return SemanticId(IdKind.EVENT, f"simulator:{digest}:{revision}:{label}")


def simulator_object_id(object_key: str) -> SemanticId:
    _validate_object_key(object_key)
    return SemanticId(IdKind.WORLD_OBJECT, f"simulator-object:{object_key}")


def simulator_state(status: SimulatorStatus) -> EffectState:
    return {
        SimulatorStatus.ACCEPTED: EffectState.DISPATCHED,
        SimulatorStatus.ACTIVE: EffectState.RUNNING,
        SimulatorStatus.COMPLETE: EffectState.SUCCEEDED,
        SimulatorStatus.ERROR: EffectState.FAILED,
        SimulatorStatus.ABORTED: EffectState.CANCELLED,
        SimulatorStatus.INDETERMINATE: EffectState.UNKNOWN,
    }[status]


def _object_key_from_id(object_id: SemanticId) -> str:
    object_id.require(IdKind.WORLD_OBJECT)
    prefix = "simulator-object:"
    if not object_id.value.startswith(prefix):
        raise ValueError("Effect target is not a simulator object")
    object_key = object_id.value.removeprefix(prefix)
    _validate_object_key(object_key)
    return object_key


def _validate_object_key(object_key: str) -> None:
    if not object_key or object_key.strip() != object_key:
        raise ValueError("simulator object key must be non-empty and trimmed")


def _correlation_key(effect_id: SemanticId) -> str:
    token = hashlib.sha256(str(effect_id).encode("utf-8")).hexdigest()[:32]
    return f"sim-correlation-{token}"


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return _sha256_bytes(encoded)


def _sha256_text(content: str) -> str:
    return _sha256_bytes(content.encode("utf-8"))


def _sha256_bytes(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"
