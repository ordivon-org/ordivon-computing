#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any
import uuid

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parent
COMPUTING_ROOT = ROOT.parents[2]
OBSERVATION_ROOT = COMPUTING_ROOT / "research" / "experiments" / "observation-plane-v0"
DEFAULT_HOST_REPO = Path("/root/projects/ordivon-host")
DEFAULT_HARNESS_REPO = Path("/root/projects/ordivon-harness")
DEFAULT_RUNTIME_REPO = Path("/root/projects/ordivon-runtime")

for source in (
    OBSERVATION_ROOT / "implementation",
    COMPUTING_ROOT / "packages" / "ordivon-protocol" / "src",
    DEFAULT_HOST_REPO / "src",
    DEFAULT_HARNESS_REPO / "src",
):
    sys.path.insert(0, str(source))

from anc_canonical import JsonValue, canonical_digest  # noqa: E402
from ordivon_host import EventKind, HostKernel, HostStorage, TaskState  # noqa: E402
from ordivon_host.external_executor import (  # noqa: E402
    ExternalExecutionRequest,
    ExternalExecutorCoordinator,
)
from ordivon_host.extensions import HostExtensionPort  # noqa: E402
from ordivon_host.observation_export import (  # noqa: E402
    COMPONENT_ID as HOST_COMPONENT_ID,
    MAPPING_VERSION as HOST_MAPPING_VERSION,
    PROJECT_ID as HOST_PROJECT_ID,
    export_host_observations,
)
from ordivon_host.runtime import (  # noqa: E402
    McpRuntimeClient,
    RuntimeProtocolError,
    RuntimeToolRejected,
    RuntimeTransportError,
)
from ordivon_host.testing import workspace_absent  # noqa: E402
from ordivon_harness.core_contracts import (  # noqa: E402
    HarnessBoundReference,
    HarnessRunContract,
)
from ordivon_harness.execution_binding import (  # noqa: E402
    HarnessExecutionBinding,
    HarnessRuntimeReference,
)
from ordivon_harness.host_external_adapter import (  # noqa: E402
    OrdivonHarnessExternalExecutorAdapter,
)
from ordivon_harness.observation_export import (  # noqa: E402
    COMPONENT_ID as HARNESS_COMPONENT_ID,
    MAPPING_VERSION as HARNESS_MAPPING_VERSION,
    PROJECT_ID as HARNESS_PROJECT_ID,
    export_harness_observations,
)
from ordivon_harness.ordivon.loop import RunBudget  # noqa: E402
from ordivon_harness.ordivon.model import (  # noqa: E402
    AgentRunConclusion,
    AgentToolCall,
    AgentTurnResult,
    ScriptedTurnAdapter,
)
from ordivon_harness.ordivon.sqlite_run_store import (  # noqa: E402
    SQLiteHarnessRunContinuityStore,
)
from ordivon_harness.ordivon.sqlite_runtime_bridge import (  # noqa: E402
    INDEPENDENT_SEARCH_TOOL_GRANT_DIGEST,
    INDEPENDENT_SEARCH_TOOL_SURFACE_DIGEST,
    SQLiteHarnessRuntimeBridge,
)
from ordivon_harness.runtime_port import (  # noqa: E402
    HarnessRuntimeClientError,
    HarnessRuntimeErrorDetail,
    HarnessRuntimeToolRejected,
)
from ordivon_harness.standalone import (  # noqa: E402
    StandaloneHarnessExecution,
    StandaloneHarnessRunner,
)
from ordivon_observation_core import (  # noqa: E402
    ObservationExportBundle,
    ObservationProducerIdentity,
    SQLiteObservationGateway,
    TrajectoryQuerySpec,
    select_cross_owner_trajectory,
)


class O1Error(RuntimeError):
    pass


class LiveClock:
    def __init__(self) -> None:
        self.value = int(time.time_ns() // 1_000_000)

    def __call__(self) -> int:
        observed = int(time.time_ns() // 1_000_000)
        self.value = max(self.value + 1, observed)
        return self.value


class HarnessRuntimeAdapter:
    """Translate Host MCP transport errors into the caller-neutral Harness port."""

    def __init__(self, delegate: McpRuntimeClient) -> None:
        self.delegate = delegate

    def call_tool(
        self,
        name: str,
        arguments: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        try:
            return self.delegate.call_tool(name, arguments)
        except RuntimeToolRejected as error:
            detail = error.detail
            raise HarnessRuntimeToolRejected(
                name,
                HarnessRuntimeErrorDetail(
                    code=detail.code,
                    message=detail.message,
                    commit_state=detail.commit_state or "unknown",
                    retryable=detail.retryable,
                    field=detail.field,
                ),
            ) from error
        except (RuntimeTransportError, RuntimeProtocolError) as error:
            raise HarnessRuntimeClientError(str(error)) from error


@dataclass
class Driver:
    runner: StandaloneHarnessRunner
    holder: dict[str, Any]
    initial_messages: tuple[dict[str, JsonValue], ...]

    def execute(self) -> StandaloneHarnessExecution:
        execution = self.runner.run(self.initial_messages)
        self.holder["execution"] = execution
        observations = execution.loop_result.observations
        runtime_jobs = tuple(
            sorted(
                {
                    item.runtime_job_ref
                    for item in observations
                    if item.runtime_job_ref is not None
                }
            )
        )
        self.holder["runtimeJobIds"] = runtime_jobs
        return execution


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one fresh current Host→Harness→Runtime Observation dogfood trajectory"
    )
    parser.add_argument("--host-repo", type=Path, default=DEFAULT_HOST_REPO)
    parser.add_argument("--harness-repo", type=Path, default=DEFAULT_HARNESS_REPO)
    parser.add_argument("--runtime-repo", type=Path, default=DEFAULT_RUNTIME_REPO)
    parser.add_argument(
        "--runtime-exporter-repo",
        type=Path,
        default=DEFAULT_RUNTIME_REPO,
        help="Runtime checkout containing the exact-job Observation exporter",
    )
    parser.add_argument(
        "--runtime-endpoint",
        default="http://127.0.0.1:8897/mcp",
    )
    parser.add_argument(
        "--registry-root",
        type=Path,
        default=Path("/var/lib/ordivon/registry"),
    )
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--keep-owner-state", action="store_true")
    parser.add_argument("--allow-dirty-computing", action="store_true")
    return parser


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _repo_state(repo: Path, *, allow_dirty: bool = False) -> tuple[str, bool]:
    revision = _git(repo, "rev-parse", "HEAD")
    dirty = bool(_git(repo, "status", "--porcelain"))
    if dirty and not allow_dirty:
        raise O1Error(f"repository is dirty: {repo}")
    return revision, dirty


def _runtime_export_module(repo: Path) -> Any:
    path = repo / "scripts" / "observation_export.py"
    spec = importlib.util.spec_from_file_location("a0_o1_runtime_observation_export", path)
    if spec is None or spec.loader is None:
        raise O1Error(f"cannot load Runtime Observation exporter: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_bundle(path: str) -> ObservationExportBundle:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    return ObservationExportBundle.from_dict(value)


def _bound_reference(ref: str, kind: str, value: Any) -> HarnessBoundReference:
    digest = value if isinstance(value, str) and value.startswith("sha256:") else canonical_digest(value)
    return HarnessBoundReference(ref, kind, digest)


def _tool_turn(token: str) -> AgentTurnResult:
    return AgentTurnResult(
        model_call_id=f"model-call:{token}:search",
        model_id=ScriptedTurnAdapter.model_id,
        content=None,
        tool_calls=(
            AgentToolCall(
                tool_call_id=f"tool-call:{token}:search",
                name="search_workspace",
                arguments={
                    "query": "class HarnessExecutionBinding",
                    "relativePath": "src",
                    "maxMatches": 20,
                },
            ),
        ),
        conclusion=None,
        usage={"inputTokens": 16, "outputTokens": 8},
        finish_reason="tool_calls",
        raw_response_digest=canonical_digest({"token": token, "turn": "search"}),
    )


def _completion_turn(token: str) -> AgentTurnResult:
    return AgentTurnResult(
        model_call_id=f"model-call:{token}:complete",
        model_id=ScriptedTurnAdapter.model_id,
        content="Located the current Harness execution binding through Runtime.",
        tool_calls=(),
        conclusion=AgentRunConclusion(
            status="candidate_completed",
            summary="Observation-only Runtime search completed; Host still owns acceptance.",
        ),
        usage={"inputTokens": 24, "outputTokens": 10},
        finish_reason="stop",
        raw_response_digest=canonical_digest({"token": token, "turn": "complete"}),
    )


def _execution_binding(
    contract: HarnessRunContract,
    continuity: SQLiteHarnessRunContinuityStore,
    *,
    workspace_id: str,
    runtime_revision: str,
) -> HarnessExecutionBinding:
    binding = continuity.binding
    references = tuple(
        sorted(
            (
                HarnessRuntimeReference(
                    namespace="ordivon.harness",
                    reference_type="harness_run",
                    reference_id=contract.harness_run_id,
                    generation=str(binding.assignment_generation),
                    digest=binding.digest,
                ),
                HarnessRuntimeReference(
                    namespace="ordivon.harness",
                    reference_type="run_contract",
                    reference_id=f"harness-run-contract:{contract.digest[7:31]}",
                    generation="1",
                    digest=contract.digest,
                ),
                HarnessRuntimeReference(
                    namespace="ordivon.harness",
                    reference_type="tool_grant",
                    reference_id=f"tool-grant:{contract.tool_grant_digest[7:31]}",
                    generation="1",
                    digest=contract.tool_grant_digest,
                ),
            ),
            key=lambda item: item.sort_key,
        )
    )
    return HarnessExecutionBinding(
        harness_run_id=contract.harness_run_id,
        workspace_ref=workspace_id,
        assignment_id=binding.assignment_id,
        assignment_generation=binding.assignment_generation,
        assignment_digest=binding.assignment_digest,
        runtime_binding_digest=canonical_digest(
            {
                "harnessRunId": contract.harness_run_id,
                "workspaceId": workspace_id,
                "runtimeRevision": runtime_revision,
            }
        ),
        tool_catalog_digest=contract.tool_catalog_digest,
        tool_grant_digest=contract.tool_grant_digest,
        deadline_ms=contract.deadline_ms,
        runtime_references=references,
    )


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.chmod(path, 0o600)


def _copy_bundle(source: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    os.chmod(destination, 0o600)


def _with_integrity(value: dict[str, Any]) -> dict[str, Any]:
    return {
        **value,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": canonical_digest(value),
        },
    }


def run(args: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    computing_revision, computing_dirty = _repo_state(
        COMPUTING_ROOT,
        allow_dirty=args.allow_dirty_computing,
    )
    host_revision, host_dirty = _repo_state(args.host_repo)
    harness_revision, harness_dirty = _repo_state(args.harness_repo)
    runtime_revision, runtime_dirty = _repo_state(args.runtime_repo)
    runtime_exporter_revision, runtime_exporter_dirty = _repo_state(
        args.runtime_exporter_repo
    )
    runtime_export = _runtime_export_module(args.runtime_exporter_repo)
    if "job_ids" not in runtime_export.export_runtime_observations.__annotations__:
        # Python annotations may be incomplete on older versions; inspect the function instead.
        import inspect

        if "job_ids" not in inspect.signature(runtime_export.export_runtime_observations).parameters:
            raise O1Error("Runtime exporter does not support exact job selection")

    token = f"a0-o1-{int(time.time_ns() // 1_000_000)}-{uuid.uuid4().hex[:10]}"
    task_id = f"task:{token}"
    goal_id = f"goal:{token}"
    external_request_id = f"external-request:{token}"
    task_attempt_ref = f"task-attempt:{token}"
    harness_run_id = f"harness-run:{token}"
    host_instance = f"host:{token}"
    harness_instance = f"harness:{token}"
    runtime_instance = f"runtime:{token}"

    token_value = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token_value:
        raise O1Error("ORDIVON_BEARER_TOKEN is required for the live Runtime trajectory")
    runtime_client = McpRuntimeClient(
        args.runtime_endpoint,
        token_value,
        client_name="ordivon-a0-o1-current-trajectory",
        client_version="1.0.0",
    )
    runtime_client.initialize()
    runtime_port = HarnessRuntimeAdapter(runtime_client)

    temp_root = Path(tempfile.mkdtemp(prefix=f"ordivon-{token}-"))
    os.chmod(temp_root, 0o700)
    host_root = temp_root / "owners" / "host"
    harness_root = temp_root / "owners" / "harness"
    workspace_id: str | None = None
    workspace_closed = False
    output_root = (
        args.output_root.resolve()
        if args.output_root is not None
        else (ROOT / "evidence" / f"o1-current-{token}").resolve()
    )
    holder: dict[str, Any] = {}
    host_clock = LiveClock()
    harness_clock = LiveClock()

    system_identity = {
        "computingRevision": computing_revision,
        "hostRevision": host_revision,
        "harnessRevision": harness_revision,
        "runtimeRevision": runtime_revision,
    }
    contract = HarnessRunContract(
        harness_run_id=harness_run_id,
        harness_implementation_id=f"ordivon-harness@{harness_revision}",
        caller_id="caller:ordivon-host",
        caller_run_ref=external_request_id,
        objective_ref=_bound_reference(
            f"objective:{token}",
            "objective",
            {"purpose": "prove fresh current three-owner Observation reconstruction"},
        ),
        context_refs=(
            _bound_reference(
                f"context:{token}",
                "context",
                {"searchTarget": "HarnessExecutionBinding", "path": "src"},
            ),
        ),
        provider_id="provider:scripted",
        adapter_id=ScriptedTurnAdapter.adapter_id,
        requested_model_id=ScriptedTurnAdapter.model_id,
        tool_catalog_digest=INDEPENDENT_SEARCH_TOOL_SURFACE_DIGEST,
        tool_grant_digest=INDEPENDENT_SEARCH_TOOL_GRANT_DIGEST,
        budget={
            "maxModelCalls": 2,
            "maxToolCalls": 1,
            "maxWallTimeMs": 30_000,
        },
        completion_contract={"mode": "propose"},
        system_manifest_ref=_bound_reference(
            f"system-manifest:{token}",
            "system-manifest",
            system_identity,
        ),
        created_at_ms=harness_clock(),
    )
    budget = RunBudget(
        max_model_calls=2,
        max_tool_calls=1,
        max_observation_bytes=65_536,
        max_wall_time_ms=30_000,
        max_total_tokens=10_000,
        max_model_retries=0,
    )

    def resolve(request: Any) -> HarnessRunContract:
        if request.request_id != external_request_id:
            raise O1Error("unexpected Host external request identity")
        return contract

    def driver_factory(
        run_contract: HarnessRunContract,
        continuity: SQLiteHarnessRunContinuityStore,
    ) -> Driver:
        if workspace_id is None:
            raise O1Error("Runtime Workspace was not opened")
        bridge = SQLiteHarnessRuntimeBridge(
            run_contract,
            continuity,
            _execution_binding(
                run_contract,
                continuity,
                workspace_id=workspace_id,
                runtime_revision=runtime_revision,
            ),
            runtime_port,
        )
        runner = StandaloneHarnessRunner(
            run_contract,
            continuity,
            ScriptedTurnAdapter((_tool_turn(token), _completion_turn(token))),
            bridge,
            budget=budget,
            clock_ms=harness_clock,
            monotonic_ms=harness_clock,
        )
        return Driver(
            runner,
            holder,
            ({"role": "user", "content": "Search the current Harness source and report candidate completion."},),
        )

    external_adapter = OrdivonHarnessExternalExecutorAdapter(
        harness_root,
        contract_resolver=resolve,
        driver_factory=driver_factory,
        clock_ms=harness_clock,
    )

    try:
        opened = runtime_client.call_tool(
            "workspace.open",
            {
                "schemaVersion": 1,
                "sourceRepo": str(args.harness_repo.resolve()),
                "sourceRevision": harness_revision,
            },
        )
        observed_workspace = opened.get("workspaceId")
        if not isinstance(observed_workspace, str) or not observed_workspace:
            raise O1Error("Runtime workspace.open omitted Workspace identity")
        workspace_id = observed_workspace

        with HostStorage(host_root) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=host_clock,
                owner_id=f"host:{token}",
            )
            created = kernel.create_task(
                event_id=f"event:{token}:task-created",
                kind=EventKind.TASK_CREATED,
                task_id=task_id,
                goal_id=goal_id,
                payload={"workloadId": "crosscut-a0-o1-current-trajectory"},
                frontier=(f"node:{token}:run",),
            ).projection
            request = ExternalExecutionRequest(
                request_id=external_request_id,
                adapter_id=external_adapter.adapter_id,
                task_id=task_id,
                task_revision=created.revision,
                task_attempt_ref=task_attempt_ref,
                contract_digest=contract.digest,
                correlation_context={"trajectoryId": token},
                created_at_ms=host_clock(),
            )
            coordinator = ExternalExecutorCoordinator(HostExtensionPort(storage, kernel))
            started = coordinator.start(request, external_adapter)
            completed = coordinator.collect_completion(task_id, external_adapter)
            if started.binding is None or completed.binding is None:
                raise O1Error("Host did not bind the foreign Harness Run")
            if completed.completion_proposal is None:
                raise O1Error("Host did not collect the Harness CompletionProposal")
            if completed.projection.state is not TaskState.READY:
                raise O1Error("Harness candidate completion changed Host Task meaning")
            retained = tuple(
                item
                for item in (
                    completed.request_object,
                    completed.binding_object,
                    completed.completion_proposal_object,
                )
                if item is not None
            )
            current_data = storage.read_task_event(task_id).data
            with kernel.locked_task(
                task_id,
                expected_revision=completed.projection.revision,
            ) as locked:
                verification = locked.commit(
                    event_id=f"event:{token}:verification",
                    kind=EventKind.VERIFICATION_RECORDED,
                    payload={
                        **current_data,
                        "verificationStatus": "passed",
                        "verificationRule": "scripted search produced one observed Runtime Job and one CompletionProposal",
                    },
                    referenced_objects=retained,
                )
            with kernel.locked_task(
                task_id,
                expected_revision=verification.projection.revision,
            ) as locked:
                outcome = locked.commit(
                    event_id=f"event:{token}:outcome",
                    kind=EventKind.TASK_OUTCOME_RECORDED,
                    payload={**current_data, "taskOutcome": "accepted"},
                    state=TaskState.COMPLETED,
                    frontier=(),
                    referenced_objects=retained,
                )
            if outcome.projection.state is not TaskState.COMPLETED:
                raise O1Error("Host deterministic verifier did not close the Task")

        execution = holder.get("execution")
        if not isinstance(execution, StandaloneHarnessExecution):
            raise O1Error("Harness Driver did not retain its execution result")
        runtime_job_ids = holder.get("runtimeJobIds")
        if not isinstance(runtime_job_ids, tuple) or len(runtime_job_ids) != 1:
            raise O1Error(f"O1 expected exactly one Runtime Job, observed {runtime_job_ids!r}")
        runtime_job_id = runtime_job_ids[0]
        if not isinstance(runtime_job_id, str):
            raise O1Error("Runtime Job identity is invalid")
        if not execution.loop_result.candidate_completed:
            raise O1Error("Harness did not reach candidate completion")
        if execution.loop_result.tool_calls != 1 or execution.loop_result.model_calls != 2:
            raise O1Error("Harness O1 call counts differ from the frozen workload")

        exported_at_ms = max(host_clock(), harness_clock())
        host_result = export_host_observations(
            state_root=host_root,
            instance_id=host_instance,
            checkpoint_path=temp_root / "sidecars" / "host.json",
            outbox_root=temp_root / "outboxes" / "host",
            owner_revision=host_revision,
            exporter_revision=host_revision,
            exported_at_ms=exported_at_ms,
            limit=256,
        )
        harness_result = export_harness_observations(
            state_root=harness_root,
            instance_id=harness_instance,
            checkpoint_path=temp_root / "sidecars" / "harness.json",
            outbox_root=temp_root / "outboxes" / "harness",
            owner_revision=harness_revision,
            exporter_revision=harness_revision,
            exported_at_ms=exported_at_ms + 1,
            limit=256,
        )
        runtime_result = runtime_export.export_runtime_observations(
            registry_root=args.registry_root,
            instance_id=runtime_instance,
            checkpoint_path=temp_root / "sidecars" / "runtime.json",
            outbox_root=temp_root / "outboxes" / "runtime",
            owner_revision=runtime_revision,
            exporter_revision=runtime_exporter_revision,
            exported_at_ms=exported_at_ms + 2,
            job_limit=1,
            event_limit_per_job=256,
            job_ids=(runtime_job_id,),
        )
        export_results = {
            "host": host_result,
            "harness": harness_result,
            "runtime": runtime_result,
        }
        for owner, result in export_results.items():
            if result.get("status") != "exported" or not isinstance(result.get("bundlePath"), str):
                raise O1Error(f"{owner} Observation exporter did not produce a Bundle: {result}")
        bundles = {
            owner: _load_bundle(str(result["bundlePath"]))
            for owner, result in export_results.items()
        }

        producers = (
            ObservationProducerIdentity(HOST_PROJECT_ID, HOST_COMPONENT_ID, host_instance),
            ObservationProducerIdentity(HARNESS_PROJECT_ID, HARNESS_COMPONENT_ID, harness_instance),
            ObservationProducerIdentity(
                runtime_export.PROJECT_ID,
                runtime_export.COMPONENT_ID,
                runtime_instance,
            ),
        )
        mappings = (
            (HOST_PROJECT_ID, HOST_COMPONENT_ID, HOST_MAPPING_VERSION),
            (HARNESS_PROJECT_ID, HARNESS_COMPONENT_ID, HARNESS_MAPPING_VERSION),
            (
                runtime_export.PROJECT_ID,
                runtime_export.COMPONENT_ID,
                runtime_export.MAPPING_VERSION,
            ),
        )
        with SQLiteObservationGateway.initialize(
            temp_root / "gateway",
            gateway_instance_id=f"observation-gateway:{token}",
            producer_allowlist=producers,
            mapping_versions=mappings,
            created_at_ms=exported_at_ms + 10,
        ) as gateway:
            ingested_at_ms = exported_at_ms + 20
            for owner in ("host", "harness", "runtime"):
                for batch in bundles[owner].batches:
                    gateway.ingest(batch, ingested_at_ms=ingested_at_ms)
                    ingested_at_ms += 1
            doctor = gateway.doctor(full=True)
            if doctor.get("healthy") is not True:
                raise O1Error("Observation Gateway full Doctor failed")
            selection = select_cross_owner_trajectory(
                gateway,
                TrajectoryQuerySpec(
                    query_id=f"trajectory-query:{token}",
                    anchor_kind="ordivon.host.task",
                    anchor_id=task_id,
                    artifact_coverage="owner_native_only",
                ),
            )
        if selection.completeness.get("complete") is not True:
            raise O1Error(f"fresh cross-owner Selection is incomplete: {selection.completeness}")
        if selection.privacy.get("metadataOnly") is not True:
            raise O1Error("fresh Selection retained inline private content")
        if selection.privacy.get("payloadBytesCopied") is not False:
            raise O1Error("fresh Selection copied owner payload bytes")

        if workspace_id is None:
            raise O1Error("Runtime Workspace identity disappeared before cleanup")
        runtime_client.call_tool(
            "workspace.close",
            {
                "schemaVersion": 1,
                "workspaceId": workspace_id,
                "force": True,
            },
        )
        workspace_closed = workspace_absent(runtime_client, workspace_id)
        if not workspace_closed:
            raise O1Error(f"Runtime Workspace remained open: {workspace_id}")

        output_root.mkdir(parents=True, exist_ok=True)
        os.chmod(output_root, 0o700)
        for owner, result in export_results.items():
            _copy_bundle(
                str(result["bundlePath"]),
                output_root / f"{owner}-observation-bundle.json",
            )
        _write_json(output_root / "selection.json", selection.to_dict())

        claims = {
            str(item["claimId"]): str(item["status"])
            for item in selection.completeness["claims"]
        }
        receipt = _with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.crosscut-a0-o1-current-trajectory",
                "status": "accepted_fresh_current_trajectory",
                "capturedAtMs": int(time.time_ns() // 1_000_000),
                "source": {
                    "computingImplementationRevision": computing_revision,
                    "hostRevision": host_revision,
                    "harnessRevision": harness_revision,
                    "runtimeOwnerRevision": runtime_revision,
                    "runtimeExporterRevision": runtime_exporter_revision,
                    "computingDirtyAtStart": computing_dirty,
                    "hostDirtyAtStart": host_dirty,
                    "harnessDirtyAtStart": harness_dirty,
                    "runtimeDirtyAtStart": runtime_dirty,
                    "runtimeExporterDirtyAtStart": runtime_exporter_dirty,
                },
                "identities": {
                    "trajectoryId": token,
                    "taskId": task_id,
                    "goalId": goal_id,
                    "externalRequestId": external_request_id,
                    "harnessRunId": harness_run_id,
                    "runtimeWorkspaceId": workspace_id,
                    "runtimeJobId": runtime_job_id,
                },
                "run": {
                    "modelCalls": execution.loop_result.model_calls,
                    "toolCalls": execution.loop_result.tool_calls,
                    "observationBytes": execution.loop_result.observation_bytes,
                    "usage": dict(execution.loop_result.usage),
                    "stopCode": execution.loop_result.stop_code.value,
                    "candidateCompleted": execution.loop_result.candidate_completed,
                },
                "observation": {
                    "hostEventCount": host_result["eventCount"],
                    "harnessEventCount": harness_result["eventCount"],
                    "runtimeEventCount": runtime_result["eventCount"],
                    "runtimeRegistryJobCount": runtime_result["registryJobCount"],
                    "runtimeExportJobCount": runtime_result["jobCount"],
                    "exactRuntimeJobSelection": True,
                    "hostBundleDigest": host_result["bundleDigest"],
                    "harnessBundleDigest": harness_result["bundleDigest"],
                    "runtimeBundleDigest": runtime_result["bundleDigest"],
                    "selectionDigest": selection.selection_digest,
                    "selectedEventCount": len(selection.selected_events),
                    "claims": claims,
                    "privacy": selection.privacy,
                    "trialValidityInferred": selection.completeness["trialValidityInferred"],
                },
                "checks": {
                    "onePhysicalRuntimeJobLinked": len(runtime_job_ids) == 1,
                    "hostRemainedSemanticAuthority": True,
                    "threeOwnerSelectionComplete": selection.completeness["complete"] is True,
                    "threeOwnerCoverage": claims.get("three_owner_coverage") == "satisfied",
                    "runtimeJobLinked": claims.get("runtime_job_linked") == "satisfied",
                    "harnessRunLinked": claims.get("harness_run_linked") == "satisfied",
                    "hostVerificationRecorded": claims.get("host_verification_recorded") == "satisfied",
                    "hostOutcomeRecorded": claims.get("host_task_outcome_recorded") == "satisfied",
                    "metadataOnly": selection.privacy["metadataOnly"] is True,
                    "payloadBytesCopied": selection.privacy["payloadBytesCopied"] is False,
                    "exactRuntimeExportSurvivedLargeRegistry": (
                        runtime_result["registryJobCount"] > runtime_result["jobCount"] == 1
                    ),
                    "runtimeWorkspaceClosed": workspace_closed,
                },
                "limitations": [
                    "The Provider is scripted; O1 proves fresh current infrastructure composition, not model capability.",
                    "Runtime Artifact traversal remains owner-native only.",
                    "Host and Harness temporary owner payload stores are removed unless --keep-owner-state is requested; retained Bundles are metadata-only evidence.",
                    "Observation remains rebuildable evidence and is not production authority.",
                ],
                "productionObservationActivated": False,
            }
        )
        if not all(receipt["checks"].values()):
            raise O1Error(f"O1 receipt checks failed: {receipt['checks']}")
        _write_json(output_root / "receipt.json", receipt)
        return receipt, output_root
    finally:
        if workspace_id is not None and not workspace_closed:
            try:
                runtime_client.call_tool(
                    "workspace.close",
                    {
                        "schemaVersion": 1,
                        "workspaceId": workspace_id,
                        "force": True,
                    },
                )
                workspace_closed = workspace_absent(runtime_client, workspace_id)
            except Exception:
                workspace_closed = False
        if args.keep_owner_state:
            retained = output_root / "owner-state-location.txt"
            retained.parent.mkdir(parents=True, exist_ok=True)
            retained.write_text(str(temp_root) + "\n", encoding="utf-8")
            os.chmod(retained, 0o600)
        else:
            shutil.rmtree(temp_root, ignore_errors=True)
        if workspace_id is not None and not workspace_closed:
            raise O1Error(f"Runtime Workspace cleanup could not be confirmed: {workspace_id}")


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        receipt, output_root = run(args)
    except Exception as error:
        print(f"A0 O1 current trajectory: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "taskId": receipt["identities"]["taskId"],
                "harnessRunId": receipt["identities"]["harnessRunId"],
                "runtimeJobId": receipt["identities"]["runtimeJobId"],
                "runtimeRegistryJobCount": receipt["observation"]["runtimeRegistryJobCount"],
                "selectedEventCount": receipt["observation"]["selectedEventCount"],
                "selectionDigest": receipt["observation"]["selectionDigest"],
                "outputRoot": str(output_root),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
