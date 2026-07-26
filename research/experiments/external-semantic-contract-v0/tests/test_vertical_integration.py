from __future__ import annotations

import hashlib
import json
import sys
import unittest
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KERNEL_SRC = ROOT.parent / "semantic-core-v0" / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(KERNEL_SRC) not in sys.path:
    sys.path.insert(0, str(KERNEL_SRC))

from anc_effect_binding import (  # noqa: E402
    BindingDecision,
    assess_binding,
    lower_to_ordivon,
    lower_to_simulator,
)
from anc_effect_ir import (  # noqa: E402
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
    effect_digest,
)
from anc_tool_contract import (  # noqa: E402
    ContractChange,
    classify_contract_change,
    normalize_tool_contract,
)
from integration import (  # noqa: E402
    BoundExecutionView,
    admit_bound_effect,
    project_binding_admission,
)
from anc_semantic_core.identity import SemanticId  # noqa: E402
from anc_semantic_core.ordivon import (  # noqa: E402
    OrdivonExecution,
    OrdivonSemanticAdapter,
    ordivon_workspace_object_id,
)
from anc_semantic_core.ordivon_io import (  # noqa: E402
    MutationMode,
    OrdivonIoAdapter,
    OrdivonMutation,
    ordivon_file_object_id,
)
from anc_semantic_core.simulator import (  # noqa: E402
    DeterministicBackend,
    DeterministicBackendAdapter,
    SimulatorJobRequest,
    SimulatorMutation,
    SimulatorRead,
    SimulatorStatus,
    simulator_object_id,
)
from anc_semantic_core.state import EffectState  # noqa: E402
from anc_semantic_core.testing import reference_authority_views  # noqa: E402
from anc_semantic_core.transport import ToolTransportError  # noqa: E402
from anc_semantic_core.verification import verify_digest_fact  # noqa: E402


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


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def load_contract(name: str):
    return normalize_tool_contract(
        json.loads((ROOT / "fixtures/contracts" / name).read_text())
    )


def envelope(
    name: str,
    action: str,
    *,
    version: str | None = None,
    content: str | None = None,
) -> EffectEnvelope:
    mode = EffectMode.OBSERVE if action == "anc.object.read.v1" else EffectMode.CHANGE
    if action == "anc.execution.launch.v1":
        value: Any = {"executable": "/usr/bin/true", "args": []}
        result = ResultSemantics(
            ExecutionKind.ASYNCHRONOUS, CompletionKind.TERMINAL_OBSERVATION
        )
        target_id = "world_object:execution-scope:portable"
    elif action == "anc.object.replace-if-version.v1":
        value = {"content": content}
        result = ResultSemantics(ExecutionKind.SYNCHRONOUS, CompletionKind.RESPONSE)
        target_id = "world_object:workspace-file:config.toml"
    else:
        value = {}
        result = ResultSemantics(
            ExecutionKind.SYNCHRONOUS, CompletionKind.ACCEPTED_VERIFICATION
        )
        target_id = "world_object:workspace-file:config.toml"
    target = TargetRef(target_id, version)
    return EffectEnvelope(
        effect_id=f"effect:{name}",
        target=target,
        mode=mode,
        action=SemanticAction(action, "anc.portable-input.v1"),
        input=CanonicalInput(value),
        capability=CapabilityRequirement("principal:portable-agent", action, target_id),
        delivery=DeliverySemantics(IdempotencyKind.NATURAL),
        result=result,
        verification=VerificationPlan(
            "independent-reread-digest.v1", (EvidenceKind.OBSERVATION,)
        ),
    )


def bound_dispatch(views, effect_id: SemanticId):
    dispatch_id = views.read.get_effect(effect_id).dispatch_id
    if dispatch_id is None:
        raise AssertionError("Effect has no Dispatch")
    return views.read.get_dispatch(dispatch_id)


class VerticalIntegrationTests(unittest.TestCase):
    def test_same_mutation_envelope_executes_through_two_bound_backends(self) -> None:
        before = sha256_text("alpha\n")
        after = sha256_text("beta\n")
        shared = envelope(
            "shared-mutation",
            "anc.object.replace-if-version.v1",
            version=before,
            content="beta\n",
        )

        ordivon_contract = load_contract("ordivon-workspace-mutate-current.json")
        ordivon_binding = lower_to_ordivon(
            shared,
            ordivon_contract,
            binding_id="binding:shared-mutation-ordivon",
        )
        ordivon_views = reference_authority_views(namespace="vertical-ordivon")
        ordivon_spec, ordivon_admission = admit_bound_effect(
            ordivon_views,
            shared,
            ordivon_contract,
            ordivon_binding,
            backend_target=ordivon_file_object_id("workspace-001", "config.toml"),
            event_namespace="vertical-ordivon",
        )
        client = ScriptedClient()
        client.add(
            "workspace.mutate",
            {
                "mutations": [
                    {
                        "relativePath": "config.toml",
                        "afterDigest": after,
                        "byteLength": len("beta\n".encode()),
                    }
                ]
            },
        )
        ordivon_adapter = OrdivonIoAdapter(
            BoundExecutionView(ordivon_views.execution, ordivon_admission),
            client,
            clock_ms=iter(range(10, 100)).__next__,
        )
        ordivon_result = ordivon_adapter.dispatch_mutation(
            ordivon_spec.effect_id,
            OrdivonMutation(
                "workspace-001",
                "config.toml",
                MutationMode.WRITE,
                "beta\n",
                before,
            ),
        )

        simulator_contract = load_contract("simulator-object-mutate.json")
        simulator_binding = lower_to_simulator(
            shared,
            simulator_contract,
            binding_id="binding:shared-mutation-simulator",
        )
        simulator_views = reference_authority_views(namespace="vertical-simulator")
        simulator_spec, simulator_admission = admit_bound_effect(
            simulator_views,
            shared,
            simulator_contract,
            simulator_binding,
            backend_target=simulator_object_id("config.toml"),
            event_namespace="vertical-simulator",
        )
        backend = DeterministicBackend()
        backend.seed_object("config.toml", "alpha\n")
        simulator_adapter = DeterministicBackendAdapter(
            BoundExecutionView(simulator_views.execution, simulator_admission),
            backend,
            clock_ms=iter(range(10, 100)).__next__,
        )
        simulator_result = simulator_adapter.dispatch_mutation(
            simulator_spec.effect_id,
            SimulatorMutation("config.toml", before, "beta\n"),
        )

        self.assertIs(ordivon_result.state, EffectState.SUCCEEDED)
        self.assertIs(simulator_result.state, EffectState.SUCCEEDED)
        self.assertEqual(ordivon_result.observation.target.version, after)
        self.assertEqual(simulator_result.observation.target.version, after)
        self.assertEqual(ordivon_binding.effect_digest, simulator_binding.effect_digest)
        self.assertEqual(ordivon_binding.effect_digest, effect_digest(shared))
        self.assertNotEqual(ordivon_binding.contract.digest, simulator_binding.contract.digest)
        self.assertEqual(bound_dispatch(ordivon_views, ordivon_spec.effect_id).binding_id, ordivon_admission.binding_id)
        self.assertEqual(bound_dispatch(simulator_views, simulator_spec.effect_id).binding_id, simulator_admission.binding_id)

    def test_external_read_completes_verification_and_fact(self) -> None:
        before = sha256_text("alpha\n")
        after = sha256_text("beta\n")
        views = reference_authority_views(namespace="vertical-fact")
        backend = DeterministicBackend()
        backend.seed_object("config.toml", "alpha\n")

        mutation = envelope(
            "fact-mutation",
            "anc.object.replace-if-version.v1",
            version=before,
            content="beta\n",
        )
        mutation_contract = load_contract("simulator-object-mutate.json")
        mutation_binding = lower_to_simulator(
            mutation, mutation_contract, binding_id="binding:fact-mutation"
        )
        mutation_spec, mutation_admission = admit_bound_effect(
            views,
            mutation,
            mutation_contract,
            mutation_binding,
            backend_target=simulator_object_id("config.toml"),
            event_namespace="vertical-fact-mutation",
        )
        DeterministicBackendAdapter(
            BoundExecutionView(views.execution, mutation_admission),
            backend,
            clock_ms=iter(range(10, 100)).__next__,
        ).dispatch_mutation(
            mutation_spec.effect_id,
            SimulatorMutation("config.toml", before, "beta\n"),
        )

        read = envelope(
            "fact-read", "anc.object.read.v1", version=after
        )
        read_contract = load_contract("simulator-object-read.json")
        read_binding = lower_to_simulator(
            read, read_contract, binding_id="binding:fact-read"
        )
        read_spec, read_admission = admit_bound_effect(
            views,
            read,
            read_contract,
            read_binding,
            backend_target=simulator_object_id("config.toml"),
            event_namespace="vertical-fact-read",
            admitted_at_ms=100,
        )
        read_result = DeterministicBackendAdapter(
            BoundExecutionView(views.execution, read_admission),
            backend,
            clock_ms=iter(range(110, 200)).__next__,
        ).dispatch_read(read_spec.effect_id, SimulatorRead("config.toml"))
        fact = verify_digest_fact(
            views.verification,
            views.facts,
            claim_effect_id=mutation_spec.effect_id,
            observation=read_result.observation,
            expected_digest=after,
            verified_at_ms=200,
            accepted_at_ms=201,
        )
        self.assertIsNotNone(fact.fact)
        self.assertEqual(fact.fact.claim_id, fact.claim.claim_id)

    def test_same_launch_envelope_recovers_original_binding_on_two_backends(self) -> None:
        shared = envelope("shared-launch", "anc.execution.launch.v1")

        simulator_contract = load_contract("simulator-job-launch.json")
        simulator_binding = lower_to_simulator(
            shared,
            simulator_contract,
            binding_id="binding:shared-launch-simulator",
        )
        simulator_views = reference_authority_views(namespace="launch-simulator")
        simulator_spec, simulator_admission = admit_bound_effect(
            simulator_views,
            shared,
            simulator_contract,
            simulator_binding,
            backend_target=simulator_object_id("portable"),
            event_namespace="launch-simulator",
        )
        backend = DeterministicBackend()
        backend.lose_next_launch_response = True
        simulator_adapter = DeterministicBackendAdapter(
            BoundExecutionView(simulator_views.execution, simulator_admission),
            backend,
            clock_ms=iter(range(10, 100)).__next__,
        )
        lost = simulator_adapter.dispatch_job(
            simulator_spec.effect_id,
            SimulatorJobRequest(
                "portable",
                "run",
                (SimulatorStatus.ACTIVE, SimulatorStatus.COMPLETE),
            ),
        )
        simulator_dispatch = bound_dispatch(simulator_views, simulator_spec.effect_id)
        recovered = DeterministicBackendAdapter(
            BoundExecutionView(simulator_views.execution, simulator_admission),
            backend,
            clock_ms=iter(range(100, 200)).__next__,
        ).reconcile(simulator_spec.effect_id)
        self.assertIs(lost.state, EffectState.UNKNOWN)
        self.assertIs(recovered.state, EffectState.SUCCEEDED)
        self.assertEqual(backend.launch_count(recovered.binding.correlation_key), 1)
        self.assertEqual(bound_dispatch(simulator_views, simulator_spec.effect_id).binding_id, simulator_dispatch.binding_id)

        ordivon_contract = load_contract("ordivon-workspace-exec-current.json")
        ordivon_binding = lower_to_ordivon(
            shared,
            ordivon_contract,
            binding_id="binding:shared-launch-ordivon",
        )
        ordivon_views = reference_authority_views(namespace="launch-ordivon")
        ordivon_spec, ordivon_admission = admit_bound_effect(
            ordivon_views,
            shared,
            ordivon_contract,
            ordivon_binding,
            backend_target=ordivon_workspace_object_id("workspace-001"),
            event_namespace="launch-ordivon",
        )
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            ToolTransportError("response lost after backend admission"),
        )
        first_adapter = OrdivonSemanticAdapter(
            BoundExecutionView(ordivon_views.execution, ordivon_admission),
            client,
            clock_ms=iter(range(10, 100)).__next__,
        )
        ordivon_lost = first_adapter.dispatch_exec(
            ordivon_spec.effect_id,
            OrdivonExecution("workspace-001", "/usr/bin/true"),
        )
        request_id = next(
            arguments["clientRequestId"]
            for name, arguments in client.calls
            if name == "workspace.exec"
        )
        ordivon_dispatch = bound_dispatch(ordivon_views, ordivon_spec.effect_id)
        job = {
            "jobId": "job-portable-001",
            "attemptId": "attempt-portable-001",
            "workspaceId": "workspace-001",
            "status": "working",
            "exitCode": None,
            "artifacts": [],
        }
        client.add(
            "task.list",
            {
                "jobs": [
                    {
                        **job,
                        "clientRequestId": request_id,
                        "createdAtMs": 10,
                    }
                ]
            },
        )
        client.add("task.observe", {**job, "status": "succeeded", "exitCode": 0})
        restarted = OrdivonSemanticAdapter(
            BoundExecutionView(ordivon_views.execution, ordivon_admission),
            client,
            clock_ms=iter(range(100, 200)).__next__,
        )
        ordivon_recovered = restarted.reconcile(ordivon_spec.effect_id)
        deliveries = sum(1 for name, _ in client.calls if name == "workspace.exec")
        self.assertIs(ordivon_lost.state, EffectState.UNKNOWN)
        self.assertIs(ordivon_recovered.state, EffectState.SUCCEEDED)
        self.assertEqual(deliveries, 1)
        self.assertEqual(bound_dispatch(ordivon_views, ordivon_spec.effect_id).binding_id, ordivon_dispatch.binding_id)

    def test_contract_drift_rebinds_only_pending_effect(self) -> None:
        old_contract = load_contract("ordivon-workspace-exec-old.json")
        new_contract = load_contract("ordivon-workspace-exec-current.json")
        self.assertIs(
            classify_contract_change(old_contract, new_contract),
            ContractChange.CALLER_ADAPTATION,
        )
        shared = envelope("drift-launch", "anc.execution.launch.v1")
        old_binding = lower_to_ordivon(
            shared, old_contract, binding_id="binding:drift-r1"
        )
        new_binding = lower_to_ordivon(
            shared,
            new_contract,
            binding_id="binding:drift-r2",
            revision=2,
            supersedes=old_binding.binding_id,
        )
        self.assertEqual(old_binding.effect_digest, new_binding.effect_digest)
        self.assertIs(
            assess_binding("prepared", ContractChange.CALLER_ADAPTATION),
            BindingDecision.REBIND,
        )
        views = reference_authority_views(namespace="drift-pending")
        _, old_admission = admit_bound_effect(
            views,
            shared,
            old_contract,
            old_binding,
            backend_target=ordivon_workspace_object_id("workspace-001"),
            event_namespace="drift-pending",
        )
        views.bindings.admit_binding(
            project_binding_admission(new_binding, admitted_at_ms=10)
        )
        current = views.read.current_binding_for(old_admission.effect_id)
        self.assertEqual(current.binding_revision, 2)
        self.assertEqual(current.effect_digest, old_admission.effect_digest)

        client = ScriptedClient()
        client.add("workspace.exec", ToolTransportError("ambiguous response"))
        adapter = OrdivonSemanticAdapter(
            BoundExecutionView(views.execution, current),
            client,
            clock_ms=iter(range(20, 100)).__next__,
        )
        adapter.dispatch_exec(
            old_admission.effect_id,
            OrdivonExecution("workspace-001", "/usr/bin/true"),
        )
        from anc_semantic_core.errors import InvalidTransition

        with self.assertRaisesRegex(InvalidTransition, "cannot admit Binding"):
            views.bindings.admit_binding(
                replace_binding_revision(new_binding, 3, "binding:drift-r3")
            )
        self.assertIs(
            assess_binding("unknown", ContractChange.CALLER_ADAPTATION),
            BindingDecision.OBSERVE_ORIGINAL,
        )


def replace_binding_revision(binding, revision: int, binding_id: str):
    previous = binding.binding_id
    return project_binding_admission(
        type(binding)(
            binding_id=binding_id,
            binding_revision=revision,
            effect_id=binding.effect_id,
            effect_digest=binding.effect_digest,
            contract=binding.contract,
            encoder=binding.encoder,
            arguments=binding.arguments,
            supersedes_binding_id=previous,
            change_class=binding.change_class,
        ),
        admitted_at_ms=30,
    )


if __name__ == "__main__":
    unittest.main()
