from __future__ import annotations

import ast
import hashlib
import tempfile
import unittest
from collections import defaultdict, deque
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from anc_semantic_core.backend_conformance import (
    BackendPortabilityReport,
    PortableJobPhase,
    PortableProjection,
    run_backend_portability_conformance,
)
from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.model import (
    CapabilityRef,
    CompletionSemantics,
    EffectMode,
    EvidenceKind,
    IdempotencyKind,
    VerificationPlan,
    WorldObjectRef,
)
from anc_semantic_core.ordivon import (
    OrdivonExecution,
    OrdivonSemanticAdapter,
    ordivon_workspace_object_id,
)
from anc_semantic_core.ordivon_io import (
    MutationMode,
    OrdivonIoAdapter,
    OrdivonMutation,
    OrdivonRead,
    ordivon_file_object_id,
)
from anc_semantic_core.simulator import (
    DeterministicBackend,
    DeterministicBackendAdapter,
    SimulatorArtifact,
    SimulatorJobRequest,
    SimulatorMutation,
    SimulatorRead,
    SimulatorStatus,
    simulator_object_id,
)
from anc_semantic_core.state import EffectState
from anc_semantic_core.testing import journal_authority_views, reference_authority_views
from anc_semantic_core.transport import ToolRejected, ToolTransportError


class ScriptedClient:
    def __init__(self) -> None:
        self.responses: dict[str, deque[dict[str, Any] | Exception]] = defaultdict(deque)
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def add(self, name: str, response: dict[str, Any] | Exception) -> None:
        self.responses[name].append(response)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((name, arguments))
        if not self.responses[name]:
            raise AssertionError(f"unexpected Tool call: {name}")
        response = self.responses[name].popleft()
        if isinstance(response, Exception):
            raise response
        return response


@dataclass(slots=True)
class _OrdivonJobScenario:
    phases: deque[PortableJobPhase]
    artifact: bool
    inspection_failures: int
    job_id: str
    client_request_id: str | None = None


class OrdivonPortabilityDriver:
    name = "ordivon"

    def __init__(self) -> None:
        self.views = reference_authority_views(namespace="p2e-ordivon")
        self.client = ScriptedClient()
        self._clock_values = iter(range(1_000, 200_000))
        self._exec_adapter = self._new_exec_adapter()
        self._io_adapter = OrdivonIoAdapter(
            self.views.execution,
            self.client,
            clock_ms=self._clock_values.__next__,
        )
        self._objects: dict[str, str] = {}
        self._jobs: dict[SemanticId, _OrdivonJobScenario] = {}
        self._request_ids: dict[SemanticId, str] = {}
        self._next_job = 1

    def _new_exec_adapter(self) -> OrdivonSemanticAdapter:
        return OrdivonSemanticAdapter(
            self.views.execution,
            self.client,
            clock_ms=self._clock_values.__next__,
        )

    def seed_object(self, object_key: str, content: str) -> None:
        self._objects[object_key] = content

    def object_content(self, object_key: str) -> str:
        return self._objects[object_key]

    def object_version(self, object_key: str) -> str:
        return _sha256_text(self.object_content(object_key))

    def prepare_read(
        self, name: str, object_key: str, *, version: str | None
    ) -> SemanticId:
        return self._prepare_effect(
            name,
            target=ordivon_file_object_id("p2e-workspace", object_key),
            version=version,
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            completion=CompletionSemantics.VERIFIED,
            verification=VerificationPlan(
                method="independent-reread-digest",
                required_evidence=(EvidenceKind.OBSERVATION,),
            ),
        )

    def prepare_mutation(
        self, name: str, object_key: str, *, expected_version: str
    ) -> SemanticId:
        return self._prepare_effect(
            name,
            target=ordivon_file_object_id("p2e-workspace", object_key),
            version=expected_version,
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            completion=CompletionSemantics.ACCEPTED,
            verification=VerificationPlan(
                method="independent-reread-digest",
                required_evidence=(EvidenceKind.OBSERVATION,),
            ),
        )

    def prepare_job(self, name: str, object_key: str) -> SemanticId:
        return self._prepare_effect(
            name,
            target=ordivon_workspace_object_id(object_key),
            version=None,
            operation="workspace.exec",
            mode=EffectMode.CHANGE,
            completion=CompletionSemantics.ASYNCHRONOUS,
            verification=VerificationPlan(
                method="backend-observation",
                required_evidence=(EvidenceKind.OBSERVATION,),
            ),
        )

    def dispatch_read(
        self, effect_id: SemanticId, object_key: str
    ) -> PortableProjection:
        content = self.object_content(object_key)
        digest = _sha256_text(content)
        self.client.add("workspace.read", {"content": content, "digest": digest})
        result = self._io_adapter.dispatch_read(
            effect_id,
            OrdivonRead("p2e-workspace", object_key),
        )
        return PortableProjection(
            state=result.state,
            dispatch_id=result.dispatch_id,
            observation=result.observation,
            artifacts=(),
            error_code=result.error_code,
        )

    def dispatch_mutation(
        self,
        effect_id: SemanticId,
        object_key: str,
        *,
        expected_version: str,
        content: str,
    ) -> PortableProjection:
        current = self.object_version(object_key)
        if current != expected_version:
            self.client.add(
                "workspace.mutate",
                ToolRejected(
                    "workspace.mutate",
                    code="INVALID_REQUEST",
                    message="object does not match expectedDigest",
                    field="mutations[0].expectedDigest",
                    retryable=False,
                ),
            )
        else:
            after = _sha256_text(content)
            self.client.add(
                "workspace.mutate",
                {
                    "mutations": [
                        {
                            "relativePath": object_key,
                            "afterDigest": after,
                            "byteLength": len(content.encode("utf-8")),
                        }
                    ]
                },
            )
        result = self._io_adapter.dispatch_mutation(
            effect_id,
            OrdivonMutation(
                "p2e-workspace",
                object_key,
                MutationMode.WRITE,
                content,
                expected_version,
            ),
        )
        if result.state is EffectState.SUCCEEDED:
            self._objects[object_key] = content
        return PortableProjection(
            state=result.state,
            dispatch_id=result.dispatch_id,
            observation=result.observation,
            artifacts=(),
            error_code=result.error_code,
        )

    def dispatch_job(
        self,
        effect_id: SemanticId,
        object_key: str,
        *,
        phases: tuple[PortableJobPhase, ...],
        lose_response: bool = False,
        artifact: bool = False,
        inspection_failures: int = 0,
    ) -> PortableProjection:
        job_id = f"ordivon-job-{self._next_job:04d}"
        self._next_job += 1
        scenario = _OrdivonJobScenario(
            phases=deque(phases),
            artifact=artifact,
            inspection_failures=inspection_failures,
            job_id=job_id,
        )
        self._jobs[effect_id] = scenario
        if lose_response:
            self.client.add(
                "workspace.exec",
                ToolTransportError("response lost after backend admission"),
            )
        else:
            phase = scenario.phases.popleft()
            self.client.add("workspace.exec", self._job_payload(scenario, phase, object_key))
        result = self._exec_adapter.dispatch_exec(
            effect_id,
            OrdivonExecution(object_key, "/usr/bin/true"),
        )
        request = self.client.calls[-1][1]
        client_request_id = request["clientRequestId"]
        scenario.client_request_id = client_request_id
        self._request_ids[effect_id] = client_request_id
        return self._portable_job_projection(effect_id, result)

    def observe_job(self, effect_id: SemanticId) -> PortableProjection:
        scenario = self._jobs[effect_id]
        phase = scenario.phases.popleft() if scenario.phases else PortableJobPhase.CANCELLED
        self.client.add(
            "task.observe",
            self._job_payload(scenario, phase, self._job_object(effect_id)),
        )
        result = self._exec_adapter.observe(effect_id)
        return self._portable_job_projection(effect_id, result)

    def reconcile_job(
        self, effect_id: SemanticId, *, restart_adapter: bool
    ) -> PortableProjection:
        if restart_adapter:
            self._exec_adapter = self._new_exec_adapter()
        scenario = self._jobs[effect_id]
        current = scenario.phases[0]
        self.client.add(
            "task.list",
            {
                "jobs": [
                    {
                        **self._job_payload(
                            scenario,
                            current,
                            self._job_object(effect_id),
                        ),
                        "clientRequestId": scenario.client_request_id,
                        "createdAtMs": 1_000,
                    }
                ]
            },
        )
        if scenario.inspection_failures:
            scenario.inspection_failures -= 1
            self.client.add(
                "task.observe",
                ToolTransportError("scripted observation failure"),
            )
        else:
            scenario.phases.popleft()
            observed = (
                scenario.phases.popleft() if scenario.phases else current
            )
            self.client.add(
                "task.observe",
                self._job_payload(
                    scenario,
                    observed,
                    self._job_object(effect_id),
                ),
            )
        result = self._exec_adapter.reconcile(effect_id)
        return self._portable_job_projection(effect_id, result)

    def cancel_job(self, effect_id: SemanticId) -> PortableProjection:
        scenario = self._jobs[effect_id]
        object_key = self._job_object(effect_id)
        self.client.add(
            "task.cancel",
            ToolRejected(
                "task.cancel",
                code="TEMPORARY_CONFLICT",
                message="cancellation accepted but not yet observed",
                retryable=True,
            ),
        )
        self.client.add(
            "task.observe",
            self._job_payload(scenario, PortableJobPhase.RUNNING, object_key),
        )
        result = self._exec_adapter.cancel(effect_id)
        scenario.phases = deque((PortableJobPhase.CANCELLED,))
        return self._portable_job_projection(effect_id, result)

    def delivery_count(self, effect_id: SemanticId) -> int:
        request_id = self._request_ids[effect_id]
        return sum(
            1
            for name, arguments in self.client.calls
            if name == "workspace.exec" and arguments.get("clientRequestId") == request_id
        )

    def _prepare_effect(
        self,
        name: str,
        *,
        target: SemanticId,
        version: str | None,
        operation: str,
        mode: EffectMode,
        completion: CompletionSemantics,
        verification: VerificationPlan,
    ) -> SemanticId:
        base = sample_effect(name)
        spec = replace(
            base,
            target=WorldObjectRef(target, version=version),
            mode=mode,
            operation=operation,
            capability=CapabilityRef(base.capability.principal_id, operation, target),
            idempotency=IdempotencyKind.NATURAL,
            completion=completion,
            verification=verification,
        )
        self.views.effects.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"event:{name}:admit"),
            recorded_at_ms=10,
        )
        self.views.effects.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"event:{name}:prepare"),
            recorded_at_ms=11,
        )
        return spec.effect_id

    def _job_payload(
        self,
        scenario: _OrdivonJobScenario,
        phase: PortableJobPhase,
        object_key: str,
    ) -> dict[str, Any]:
        status = {
            PortableJobPhase.RUNNING: "working",
            PortableJobPhase.SUCCEEDED: "succeeded",
            PortableJobPhase.FAILED: "failed",
            PortableJobPhase.CANCELLED: "cancelled",
            PortableJobPhase.UNKNOWN: "orphaned",
        }[phase]
        artifacts = []
        if phase is PortableJobPhase.SUCCEEDED and scenario.artifact:
            artifacts = [
                {
                    "artifactId": "portable-result",
                    "kind": "execution_result",
                    "digest": _sha256_text("portable-result\n"),
                    "retainedBytes": len("portable-result\n".encode("utf-8")),
                    "truncated": False,
                }
            ]
        return {
            "jobId": scenario.job_id,
            "attemptId": f"attempt-{scenario.job_id}",
            "workspaceId": object_key,
            "status": status,
            "exitCode": 0 if phase is PortableJobPhase.SUCCEEDED else None,
            "artifacts": artifacts,
        }

    def _job_object(self, effect_id: SemanticId) -> str:
        value = self.views.read.get_effect(effect_id).spec.target.object_id.value
        return value.removeprefix("ordivon-workspace:")

    def _portable_job_projection(
        self, effect_id: SemanticId, result: Any
    ) -> PortableProjection:
        dispatch_id = self.views.read.get_effect(effect_id).dispatch_id
        if dispatch_id is None:
            dispatch_id = result.binding.dispatch_id
        return PortableProjection(
            state=result.state,
            dispatch_id=dispatch_id,
            observation=result.observation,
            artifacts=result.artifacts,
            error_code=result.error_code,
        )


class SimulatorPortabilityDriver:
    name = "simulator"

    def __init__(
        self,
        *,
        views: Any | None = None,
        backend: DeterministicBackend | None = None,
        clock_start: int = 1_000,
    ) -> None:
        self.views = views or reference_authority_views(namespace="p2e-simulator")
        self.backend = backend or DeterministicBackend()
        self._clock_values = iter(range(clock_start, clock_start + 200_000))
        self._adapter = self._new_adapter()

    def _new_adapter(self) -> DeterministicBackendAdapter:
        return DeterministicBackendAdapter(
            self.views.execution,
            self.backend,
            clock_ms=self._clock_values.__next__,
        )

    def seed_object(self, object_key: str, content: str) -> None:
        self.backend.seed_object(object_key, content)

    def object_content(self, object_key: str) -> str:
        return self.backend.object_content(object_key)

    def object_version(self, object_key: str) -> str:
        return self.backend.object_version(object_key)

    def prepare_read(
        self, name: str, object_key: str, *, version: str | None
    ) -> SemanticId:
        return self._prepare_effect(
            name,
            object_key=object_key,
            version=version,
            operation=DeterministicBackendAdapter.READ_OPERATION,
            mode=EffectMode.OBSERVE,
            completion=CompletionSemantics.VERIFIED,
            verification=VerificationPlan(
                method="independent-reread-digest",
                required_evidence=(EvidenceKind.OBSERVATION,),
            ),
        )

    def prepare_mutation(
        self, name: str, object_key: str, *, expected_version: str
    ) -> SemanticId:
        return self._prepare_effect(
            name,
            object_key=object_key,
            version=expected_version,
            operation=DeterministicBackendAdapter.MUTATION_OPERATION,
            mode=EffectMode.CHANGE,
            completion=CompletionSemantics.ACCEPTED,
            verification=VerificationPlan(
                method="independent-reread-digest",
                required_evidence=(EvidenceKind.OBSERVATION,),
            ),
        )

    def prepare_job(self, name: str, object_key: str) -> SemanticId:
        return self._prepare_effect(
            name,
            object_key=object_key,
            version=None,
            operation=DeterministicBackendAdapter.JOB_OPERATION,
            mode=EffectMode.CHANGE,
            completion=CompletionSemantics.ASYNCHRONOUS,
            verification=VerificationPlan(
                method="backend-observation",
                required_evidence=(EvidenceKind.OBSERVATION,),
            ),
        )

    def dispatch_read(
        self, effect_id: SemanticId, object_key: str
    ) -> PortableProjection:
        return _simulator_projection(
            self._adapter.dispatch_read(effect_id, SimulatorRead(object_key))
        )

    def dispatch_mutation(
        self,
        effect_id: SemanticId,
        object_key: str,
        *,
        expected_version: str,
        content: str,
    ) -> PortableProjection:
        return _simulator_projection(
            self._adapter.dispatch_mutation(
                effect_id,
                SimulatorMutation(object_key, expected_version, content),
            )
        )

    def dispatch_job(
        self,
        effect_id: SemanticId,
        object_key: str,
        *,
        phases: tuple[PortableJobPhase, ...],
        lose_response: bool = False,
        artifact: bool = False,
        inspection_failures: int = 0,
    ) -> PortableProjection:
        self.backend.lose_next_launch_response = lose_response
        artifacts = (
            (
                SimulatorArtifact(
                    "portable-result",
                    "execution_result",
                    b"portable-result\n",
                ),
            )
            if artifact
            else ()
        )
        request = SimulatorJobRequest(
            object_key=object_key,
            action="portable-action",
            status_plan=tuple(_simulator_status(phase) for phase in phases),
            artifacts=artifacts,
            inspection_failures=inspection_failures,
        )
        return _simulator_projection(self._adapter.dispatch_job(effect_id, request))

    def observe_job(self, effect_id: SemanticId) -> PortableProjection:
        return _simulator_projection(self._adapter.observe(effect_id))

    def reconcile_job(
        self, effect_id: SemanticId, *, restart_adapter: bool
    ) -> PortableProjection:
        if restart_adapter:
            self._adapter = self._new_adapter()
        return _simulator_projection(self._adapter.reconcile(effect_id))

    def cancel_job(self, effect_id: SemanticId) -> PortableProjection:
        return _simulator_projection(self._adapter.cancel(effect_id))

    def delivery_count(self, effect_id: SemanticId) -> int:
        return self._adapter.delivery_count(effect_id)

    def _prepare_effect(
        self,
        name: str,
        *,
        object_key: str,
        version: str | None,
        operation: str,
        mode: EffectMode,
        completion: CompletionSemantics,
        verification: VerificationPlan,
    ) -> SemanticId:
        base = sample_effect(name)
        target = simulator_object_id(object_key)
        spec = replace(
            base,
            target=WorldObjectRef(target, version=version),
            mode=mode,
            operation=operation,
            capability=CapabilityRef(base.capability.principal_id, operation, target),
            idempotency=IdempotencyKind.NATURAL,
            completion=completion,
            verification=verification,
        )
        self.views.effects.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"event:{name}:admit"),
            recorded_at_ms=10,
        )
        self.views.effects.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"event:{name}:prepare"),
            recorded_at_ms=11,
        )
        return spec.effect_id


class BackendPortabilityTests(unittest.TestCase):
    def test_same_semantic_contract_runs_against_two_backends(self) -> None:
        ordivon = run_backend_portability_conformance(OrdivonPortabilityDriver())
        simulator = run_backend_portability_conformance(SimulatorPortabilityDriver())
        self.assertIsInstance(ordivon, BackendPortabilityReport)
        self.assertEqual(ordivon, simulator)

    def test_simulator_response_loss_survives_journal_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "p2e-simulator.sqlite3"
            backend = DeterministicBackend()
            views = journal_authority_views(path, namespace="p2e-simulator-journal")
            first = SimulatorPortabilityDriver(views=views, backend=backend)
            first.seed_object("journal-object", "alpha\n")
            effect_id = first.prepare_job("p2e-simulator-journal", "journal-object")
            lost = first.dispatch_job(
                effect_id,
                "journal-object",
                phases=(PortableJobPhase.RUNNING, PortableJobPhase.SUCCEEDED),
                lose_response=True,
            )
            self.assertIs(lost.state, EffectState.UNKNOWN)
            original_dispatch = views.read.get_effect(effect_id).dispatch_id
            entries_before = views.read.journal_entry_count
            views.read.close()

            reopened_views = journal_authority_views(
                path, namespace="p2e-simulator-journal-reopen"
            )
            restarted = SimulatorPortabilityDriver(
                views=reopened_views,
                backend=backend,
                clock_start=50_000,
            )
            recovered = restarted.reconcile_job(effect_id, restart_adapter=True)
            self.assertIs(recovered.state, EffectState.SUCCEEDED)
            self.assertEqual(
                reopened_views.read.get_effect(effect_id).dispatch_id,
                original_dispatch,
            )
            self.assertEqual(restarted.delivery_count(effect_id), 1)
            self.assertGreater(reopened_views.read.journal_entry_count, entries_before)
            reopened_views.read.verify_from_genesis()
            reopened_views.read.close()

    def test_shared_conformance_imports_no_backend_adapter(self) -> None:
        source_path = (
            Path(__file__).resolve().parents[1]
            / "src"
            / "anc_semantic_core"
            / "backend_conformance.py"
        )
        tree = ast.parse(source_path.read_text())
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.add(node.module)
        self.assertFalse(
            any(
                name.endswith("ordivon")
                or name.endswith("ordivon_io")
                or name.endswith("simulator")
                for name in imported_modules
            )
        )
        source = source_path.read_text()
        for backend_term in (
            "workspace.exec",
            "workspace.read",
            "workspace.mutate",
            "task.list",
            "task.observe",
            "task.cancel",
            "jobId",
            "attemptId",
        ):
            self.assertNotIn(backend_term, source)

    def test_backend_contracts_are_structurally_distinct(self) -> None:
        import anc_semantic_core as package_root

        self.assertFalse(hasattr(package_root, "DeterministicBackend"))
        self.assertFalse(hasattr(package_root, "BackendPortabilityDriver"))
        self.assertNotEqual(
            "workspace.exec",
            DeterministicBackendAdapter.JOB_OPERATION,
        )
        self.assertNotEqual(
            "workspace.read",
            DeterministicBackendAdapter.READ_OPERATION,
        )
        self.assertNotEqual(
            "workspace.mutate",
            DeterministicBackendAdapter.MUTATION_OPERATION,
        )
        self.assertEqual(
            _simulator_status(PortableJobPhase.RUNNING),
            SimulatorStatus.ACTIVE,
        )


def _simulator_projection(result: Any) -> PortableProjection:
    return PortableProjection(
        state=result.state,
        dispatch_id=result.dispatch_id,
        observation=result.observation,
        artifacts=result.artifacts,
        error_code=result.error_code,
    )


def _simulator_status(phase: PortableJobPhase) -> SimulatorStatus:
    return {
        PortableJobPhase.RUNNING: SimulatorStatus.ACTIVE,
        PortableJobPhase.SUCCEEDED: SimulatorStatus.COMPLETE,
        PortableJobPhase.FAILED: SimulatorStatus.ERROR,
        PortableJobPhase.CANCELLED: SimulatorStatus.ABORTED,
        PortableJobPhase.UNKNOWN: SimulatorStatus.INDETERMINATE,
    }[phase]


def _sha256_text(content: str) -> str:
    return f"sha256:{hashlib.sha256(content.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    unittest.main()
