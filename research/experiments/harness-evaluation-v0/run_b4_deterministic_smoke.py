#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from typing import Any

SCRIPT = Path(__file__).resolve()
EXPERIMENT = SCRIPT.parent
COMPUTING_ROOT = EXPERIMENT.parents[2]
OBSERVATION_ROOT = EXPERIMENT.parent / "observation-plane-v0"
HOST_ROOT = Path("/root/projects/ordivon-host")
HARNESS_ROOT = Path("/root/projects/ordivon-harness")
RUNTIME_ROOT = Path("/root/projects/ordivon-runtime")
PROTOCOL_SRC = COMPUTING_ROOT / "packages" / "ordivon-protocol" / "src"

for source in (
    EXPERIMENT,
    OBSERVATION_ROOT / "implementation",
    PROTOCOL_SRC,
    HOST_ROOT / "src",
    HARNESS_ROOT / "src",
):
    sys.path.insert(0, str(source))

from b4_fault_cells import run_b4_fault_cells  # noqa: E402
from formal_runner import (  # noqa: E402
    TrialDisposition,
    TrialRecordStore,
    canonical_digest,
    validate_completion_artifact,
    with_integrity,
)
from ordivon_host import EventKind, HostKernel, HostStorage, TaskState  # noqa: E402
from ordivon_host.external_executor import (  # noqa: E402
    ExternalCompletionProposal,
    ExternalExecutionRequest,
    ExternalExecutorCoordinator,
    ExternalRunObservation,
    ExternalRunStatus,
)
from ordivon_host.extensions import HostExtensionPort  # noqa: E402
from ordivon_host.observation_export import export_host_observations  # noqa: E402
from ordivon_host.runtime import McpRuntimeClient  # noqa: E402
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
    export_harness_observations,
)
from ordivon_harness.ordivon.loop import RunBudget  # noqa: E402
from ordivon_harness.ordivon.model import (  # noqa: E402
    AgentRunConclusion,
    AgentToolCall,
    AgentTurnResult,
    ScriptedTurnAdapter,
)
from ordivon_harness.ordivon.sqlite_repository_repair_bridge import (  # noqa: E402
    INDEPENDENT_REPOSITORY_REPAIR_TOOL_GRANT_DIGEST,
    INDEPENDENT_REPOSITORY_REPAIR_TOOL_SURFACE_DIGEST,
    SQLiteHarnessRepositoryRepairRuntimeBridge,
)
from ordivon_harness.ordivon.sqlite_run_store import (  # noqa: E402
    SQLiteHarnessRunContinuityStore,
)
from ordivon_harness.runtime_port import HarnessRuntimeClientError  # noqa: E402
from ordivon_harness.sqlite_store import SQLiteHarnessStore  # noqa: E402
from ordivon_harness.standalone import StandaloneHarnessRunner  # noqa: E402
from ordivon_observation_core import (  # noqa: E402
    ObservationExportBundle,
    ObservationProducerIdentity,
    SQLiteObservationGateway,
    TrajectoryQuerySpec,
    select_cross_owner_trajectory,
)

TASK_ID = "HARNESS-REPO-REPAIR-001"
TASK_VERSION = 1
TRIAL_ID = "trial:b4-scripted-integrated-smoke"
CONFIGURATION_ID = "scripted-integrated-control"
HOST_TASK_ID = "task:b4-scripted-integrated-smoke"
HOST_GOAL_ID = "goal:b4-scripted-integrated-smoke"
HOST_ATTEMPT_REF = "task-attempt:b4-scripted-integrated-smoke"
EXTERNAL_REQUEST_ID = "external-request:b4-scripted-integrated-smoke"
HARNESS_RUN_ID = "harness-run:b4-scripted-integrated-smoke"
HISTORICAL_HOST_REVISION = "b4bc43a4ea7eb1e7771644d507bc4a3a39b4e741"
HISTORICAL_FIXTURE = "fixtures/harness-replacement-repository-repair-v1"
HOST_REVISION = "a76a620160b28d870670696e04c39e539296fe00"
HOST_EXPORTER_REVISION = "e1c134f330a90c15495126a67021b06c56245156"
HARNESS_REVISION = "ac10497f1b6e681899cfe98c347ed6d48941ba23"
HARNESS_IMPLEMENTATION_REVISION = "7664240791dfb984338aa72e4c74ce8459ec7c98"
HARNESS_EXPORTER_REVISION = "e3cb34b4991b5f52e1c0ed0151ea17b067e88e16"
RUNTIME_REVISION = "a455fd01ce0dea25684956e5e5da899d41832a1b"
RUNTIME_EXPORTER_REVISION = "a455fd01ce0dea25684956e5e5da899d41832a1b"
PROTOCOL_REVISION = "420dc356cb664d75db0f34f356156baebe5843db"
B3_IMPLEMENTATION_REVISION = "e9bc8b49941fb332f9f1f5774588bddca72a5b49"
B3_RECEIPT_REVISION = "e6e480b03a7db336b950b73d8a837ef1799bde12"
SHARED_CONTRACT_REVISION = "b0973311d84b0debe30ca002e15e02401e16ee36"
DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
DIGEST_C = "sha256:" + "c" * 64
HOST_INSTANCE = "host:b4-scripted-smoke"
HARNESS_INSTANCE = "harness:b4-scripted-smoke"
RUNTIME_INSTANCE = "runtime:b4-scripted-smoke"


class SmokeError(RuntimeError):
    pass


class Clock:
    def __init__(self, value: int) -> None:
        self.value = value

    def __call__(self) -> int:
        self.value += 1
        return self.value


@dataclass
class ExecutionCapture:
    loop_result: Any | None = None
    driver_creations: int = 0


class Driver:
    def __init__(
        self,
        runner: StandaloneHarnessRunner,
        capture: ExecutionCapture,
        initial_messages: tuple[dict[str, Any], ...],
    ) -> None:
        self.runner = runner
        self.capture = capture
        self.initial_messages = initial_messages

    def execute(self) -> None:
        execution = self.runner.run(self.initial_messages)
        self.capture.loop_result = execution.loop_result


class LossyExternalAdapter:
    adapter_id = OrdivonHarnessExternalExecutorAdapter.adapter_id

    def __init__(self, delegate: OrdivonHarnessExternalExecutorAdapter) -> None:
        self.delegate = delegate
        self.start_calls = 0
        self.lost = False

    def start(self, request):
        self.start_calls += 1
        result = self.delegate.start(request)
        if not self.lost:
            self.lost = True
            raise RuntimeError("injected Host external Run response delivery loss")
        return result

    def observe(self, foreign_run_ref: str):
        return self.delegate.observe(foreign_run_ref)

    def cancel(self, foreign_run_ref: str, request_id: str):
        return self.delegate.cancel(foreign_run_ref, request_id)

    def recover(self, request, foreign_run_ref: str | None):
        return self.delegate.recover(request, foreign_run_ref)

    def collect_completion(self, foreign_run_ref: str):
        return self.delegate.collect_completion(foreign_run_ref)


class LossyRuntimeClient:
    def __init__(self, delegate: McpRuntimeClient) -> None:
        self.delegate = delegate
        self.calls: list[str] = []
        self.job_ids: set[str] = set()
        self.exec_dispatches = 0
        self.lost_exec_response = False

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(name)
        result = self.delegate.call_tool(name, arguments)
        self._capture_jobs(result)
        if name == "workspace.exec":
            self.exec_dispatches += 1
            if not self.lost_exec_response:
                self.lost_exec_response = True
                raise HarnessRuntimeClientError(
                    "injected Runtime response loss after Job admission"
                )
        return result

    def _capture_jobs(self, value: dict[str, Any]) -> None:
        job_id = value.get("jobId")
        if isinstance(job_id, str):
            self.job_ids.add(job_id)
        jobs = value.get("jobs")
        if isinstance(jobs, list):
            for item in jobs:
                if isinstance(item, dict) and isinstance(item.get("jobId"), str):
                    self.job_ids.add(item["jobId"])


class MissingArtifactAdapter:
    adapter_id = "external-executor:b4-missing-artifact"

    def __init__(self, runtime_job_id: str) -> None:
        self.runtime_job_id = runtime_job_id
        self.run_ref = "harness-run:b4-missing-artifact"

    def start(self, request: ExternalExecutionRequest) -> ExternalRunObservation:
        return ExternalRunObservation(
            foreign_run_ref=self.run_ref,
            status=ExternalRunStatus.COMPLETED,
            revision=1,
            evidence_refs=(f"runtime-job:{self.runtime_job_id}",),
            observed_at_ms=request.created_at_ms + 1,
            metadata={},
        )

    def observe(self, foreign_run_ref: str) -> ExternalRunObservation:
        return ExternalRunObservation(
            foreign_run_ref=foreign_run_ref,
            status=ExternalRunStatus.COMPLETED,
            revision=1,
            evidence_refs=(f"runtime-job:{self.runtime_job_id}",),
            observed_at_ms=1,
            metadata={},
        )

    def cancel(self, foreign_run_ref: str, request_id: str) -> ExternalRunObservation:
        raise SmokeError(f"unexpected cancellation: {foreign_run_ref} {request_id}")

    def recover(
        self,
        request: ExternalExecutionRequest,
        foreign_run_ref: str | None,
    ) -> ExternalRunObservation:
        return self.start(request)

    def collect_completion(
        self, foreign_run_ref: str
    ) -> ExternalCompletionProposal | None:
        return ExternalCompletionProposal(
            proposal_id="completion-proposal:b4-missing-artifact",
            foreign_run_ref=foreign_run_ref,
            contract_digest=DIGEST_A,
            summary="Physical Runtime success without the required completion Artifact.",
            evidence_refs=(f"runtime-job:{self.runtime_job_id}",),
            artifact_refs=(),
            created_at_ms=2,
            metadata={},
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the B4 deterministic formal smoke")
    parser.add_argument("--runtime-endpoint", default="http://127.0.0.1:8897/mcp")
    parser.add_argument("--runtime-registry-root", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--allow-dirty-computing", action="store_true")
    return parser.parse_args()


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def text_digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def extract_historical_fixture(root: Path) -> str:
    root.mkdir(parents=True, mode=0o700)
    paths = ("SPEC.md", "allocation.py", "test_allocation.py", "artifacts/.gitkeep")
    for relative in paths:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        value = subprocess.run(
            [
                "git",
                "-C",
                str(HOST_ROOT),
                "show",
                f"{HISTORICAL_HOST_REVISION}:{HISTORICAL_FIXTURE}/{relative}",
            ],
            check=True,
            capture_output=True,
        ).stdout
        target.write_bytes(value)
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(
        ["git", "-C", str(root), "config", "user.email", "b4@ordivon.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "config", "user.name", "Ordivon B4"],
        check=True,
    )
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", "freeze B4 Task source"],
        check=True,
    )
    return git(root, "rev-parse", "HEAD")


def edit_range(source: str, expected: str) -> dict[str, Any]:
    offset = source.index(expected)
    end_offset = offset + len(expected)
    before = source[:offset]
    through = source[:end_offset]
    return {
        "start": {
            "line": before.count("\n") + 1,
            "column": len(before.rsplit("\n", 1)[-1]),
        },
        "end": {
            "line": through.count("\n") + 1,
            "column": len(through.rsplit("\n", 1)[-1]),
        },
    }


def build_completion_artifact(final_source: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.evaluation-completion-artifact",
        "taskId": TASK_ID,
        "taskVersion": TASK_VERSION,
        "sourceRevision": HISTORICAL_HOST_REVISION,
        "changedPaths": ["allocation.py"],
        "visibleCheck": {"checkId": "visible-tests", "status": "passed"},
        "finalSourceDigest": text_digest(final_source),
        "summary": "Implemented deterministic largest-remainder allocation with stable tie-breaking.",
    }


def agent_turn(sequence: int, call: AgentToolCall) -> AgentTurnResult:
    return AgentTurnResult(
        model_call_id=f"model-call:b4-smoke:{sequence}",
        model_id=ScriptedTurnAdapter.model_id,
        content=None,
        tool_calls=(call,),
        conclusion=None,
        usage={"inputTokens": 10, "outputTokens": 5},
        finish_reason="tool_calls",
        raw_response_digest=canonical_digest(
            {"sequence": sequence, "toolCall": call.to_dict()}
        ),
    )


def completion_turn(workspace_id: str) -> AgentTurnResult:
    return AgentTurnResult(
        model_call_id="model-call:b4-smoke:6",
        model_id=ScriptedTurnAdapter.model_id,
        content="candidate complete",
        tool_calls=(),
        conclusion=AgentRunConclusion(
            status="candidate_completed",
            summary="Repository repair candidate completed; Host still owns acceptance.",
            artifact_refs=(
                f"workspace-artifact:{workspace_id}:artifacts/completion.json",
            ),
            evidence_refs=("evidence:b4-scripted-smoke",),
        ),
        usage={"inputTokens": 10, "outputTokens": 5},
        finish_reason="stop",
        raw_response_digest=canonical_digest({"b4": "candidate-completed"}),
    )


def build_contract(created_at_ms: int) -> HarnessRunContract:
    return HarnessRunContract(
        harness_run_id=HARNESS_RUN_ID,
        harness_implementation_id=(
            f"ordivon-harness@{HARNESS_IMPLEMENTATION_REVISION}"
        ),
        caller_id="caller:ordivon-host",
        caller_run_ref=EXTERNAL_REQUEST_ID,
        objective_ref=HarnessBoundReference(
            "objective:b4-scripted-smoke", "objective", DIGEST_A
        ),
        context_refs=(
            HarnessBoundReference("context:b4-scripted-smoke", "context", DIGEST_B),
        ),
        provider_id="provider:scripted",
        adapter_id=ScriptedTurnAdapter.adapter_id,
        requested_model_id=ScriptedTurnAdapter.model_id,
        tool_catalog_digest=INDEPENDENT_REPOSITORY_REPAIR_TOOL_SURFACE_DIGEST,
        tool_grant_digest=INDEPENDENT_REPOSITORY_REPAIR_TOOL_GRANT_DIGEST,
        budget={
            "maxModelCalls": 8,
            "maxToolCalls": 20,
            "maxWallTimeMs": 600_000,
        },
        completion_contract={
            "mode": "propose",
            "requiredArtifact": "artifacts/completion.json",
        },
        system_manifest_ref=HarnessBoundReference(
            "system-manifest:b4-scripted-smoke", "system-manifest", DIGEST_C
        ),
        created_at_ms=created_at_ms,
    )


def build_execution_binding(
    contract: HarnessRunContract,
    continuity: SQLiteHarnessRunContinuityStore,
    workspace_id: str,
) -> HarnessExecutionBinding:
    binding = continuity.binding
    references = (
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
    )
    return HarnessExecutionBinding(
        harness_run_id=contract.harness_run_id,
        workspace_ref=workspace_id,
        assignment_id=binding.assignment_id,
        assignment_generation=binding.assignment_generation,
        assignment_digest=binding.assignment_digest,
        runtime_binding_digest=canonical_digest(
            {"harnessRunId": contract.harness_run_id, "workspaceRef": workspace_id}
        ),
        tool_catalog_digest=contract.tool_catalog_digest,
        tool_grant_digest=contract.tool_grant_digest,
        deadline_ms=contract.deadline_ms,
        runtime_references=references,
    )


def read_workspace(client: McpRuntimeClient, workspace_id: str, path: str) -> str:
    value = client.call_tool(
        "workspace.read",
        {
            "schemaVersion": 1,
            "workspaceId": workspace_id,
            "relativePath": path,
            "mode": "FULL",
            "offset": 0,
            "maxBytes": 1_048_576,
        },
    )
    content = value.get("content")
    if not isinstance(content, str) or value.get("truncated") is True:
        raise SmokeError(f"Workspace read is incomplete: {path}")
    return content


def run_verifier(
    root: Path,
    *,
    candidate_source: str,
    completion_text: str,
    protected: dict[str, str],
) -> dict[str, Any]:
    workspace = root / "verifier-workspace"
    source = root / "source"
    shutil.copytree(source, workspace)
    (workspace / "allocation.py").write_text(candidate_source, encoding="utf-8")
    artifact_path = workspace / "artifacts" / "completion.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(completion_text, encoding="utf-8")
    completion = json.loads(completion_text)
    if not isinstance(completion, dict):
        raise SmokeError("Completion Artifact is not an object")
    validate_completion_artifact(
        completion,
        task_id=TASK_ID,
        task_version=TASK_VERSION,
        source_revision=HISTORICAL_HOST_REVISION,
    )
    if completion["finalSourceDigest"] != text_digest(candidate_source):
        raise SmokeError("Completion Artifact source digest differs from candidate")
    for relative, expected in protected.items():
        if file_digest(workspace / relative) != expected:
            raise SmokeError(f"protected file changed: {relative}")
    visible = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_allocation.py"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=60,
    )
    hidden_path = (
        HARNESS_ROOT
        / "evals"
        / "harness-repository-repair-001"
        / "verifier"
        / "test_outcome.py"
    )
    hidden = subprocess.run(
        [sys.executable, str(hidden_path)],
        cwd=workspace,
        env={**os.environ, "ORDIVON_EVAL_WORKSPACE": str(workspace)},
        capture_output=True,
        text=True,
        timeout=60,
    )
    return {
        "visiblePassed": visible.returncode == 0,
        "visibleDigest": text_digest(visible.stdout + visible.stderr),
        "hiddenPassed": hidden.returncode == 0,
        "hiddenDigest": text_digest(hidden.stdout + hidden.stderr),
        "completionArtifactDigest": text_digest(completion_text),
        "candidateSourceDigest": text_digest(candidate_source),
        "protectedFilesUnchanged": True,
    }


def runtime_export_module() -> Any:
    path = RUNTIME_ROOT / "scripts" / "observation_export.py"
    spec = importlib.util.spec_from_file_location("b4_runtime_exporter", path)
    if spec is None or spec.loader is None:
        raise SmokeError("Runtime exporter cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_runtime_job(
    source_root: Path,
    destination_root: Path,
    job_id: str,
) -> None:
    destination_root.mkdir(parents=True, mode=0o700)
    destination = destination_root / "registry.sqlite3"
    source = source_root / "registry.sqlite3"
    target = sqlite3.connect(destination)
    origin = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
    origin.row_factory = sqlite3.Row
    try:
        migrations = (
            RUNTIME_ROOT
            / "crates"
            / "ordivon-runtime-core"
            / "migrations"
            / "runtime"
        )
        for path in sorted(migrations.glob("*.sql")):
            target.executescript(path.read_text(encoding="utf-8"))
        target.executemany(
            "INSERT INTO schema_migrations(version,name,checksum,applied_at_ms) VALUES(?,?,?,?)",
            [(version, f"migration-{version}", DIGEST_A, version) for version in range(1, 5)],
        )
        target.execute("PRAGMA foreign_keys=OFF")
        for table, query in (
            ("jobs", "SELECT * FROM jobs WHERE job_id=?"),
            ("attempts", "SELECT * FROM attempts WHERE job_id=? ORDER BY attempt_number"),
            ("job_events", "SELECT * FROM job_events WHERE job_id=? ORDER BY event_sequence"),
            ("artifacts", "SELECT * FROM artifacts WHERE job_id=? ORDER BY artifact_id"),
        ):
            rows = origin.execute(query, (job_id,)).fetchall()
            for row in rows:
                columns = list(row.keys())
                target.execute(
                    f"INSERT INTO {table}({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
                    tuple(row[column] for column in columns),
                )
        target.commit()
        target.execute("PRAGMA foreign_keys=ON")
        violations = target.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise SmokeError(f"Runtime Job snapshot violates foreign keys: {violations}")
        count = target.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        if count != 1:
            raise SmokeError("Runtime Job snapshot does not contain exactly one Job")
    finally:
        origin.close()
        target.close()
    os.chmod(destination, 0o600)


def load_bundle(path: str) -> ObservationExportBundle:
    return ObservationExportBundle.from_dict(
        json.loads(Path(path).read_text(encoding="utf-8"))
    )


def build_selection(
    root: Path,
    host_root: Path,
    harness_root: Path,
    runtime_snapshot: Path,
) -> dict[str, Any]:
    sidecars = root / "observation-sidecars"
    outboxes = root / "observation-outboxes"
    host_result = export_host_observations(
        state_root=host_root,
        instance_id=HOST_INSTANCE,
        checkpoint_path=sidecars / "host.json",
        outbox_root=outboxes / "host",
        owner_revision=HOST_REVISION,
        exporter_revision=HOST_EXPORTER_REVISION,
        exported_at_ms=8_000,
        limit=1_000,
    )
    harness_result = export_harness_observations(
        state_root=harness_root,
        instance_id=HARNESS_INSTANCE,
        checkpoint_path=sidecars / "harness.json",
        outbox_root=outboxes / "harness",
        owner_revision=HARNESS_REVISION,
        exporter_revision=HARNESS_EXPORTER_REVISION,
        exported_at_ms=8_001,
        limit=1_000,
    )
    runtime_export = runtime_export_module()
    runtime_result = runtime_export.export_runtime_observations(
        registry_root=runtime_snapshot,
        instance_id=RUNTIME_INSTANCE,
        checkpoint_path=sidecars / "runtime.json",
        outbox_root=outboxes / "runtime",
        owner_revision=RUNTIME_REVISION,
        exporter_revision=RUNTIME_EXPORTER_REVISION,
        exported_at_ms=8_002,
        job_limit=10,
        event_limit_per_job=1_000,
    )
    results = (host_result, harness_result, runtime_result)
    if any(result["status"] != "exported" for result in results):
        raise SmokeError("one B4 owner exporter produced no Bundle")
    bundles = tuple(load_bundle(str(result["bundlePath"])) for result in results)
    producers = (
        ObservationProducerIdentity("ordivon-host", "host-journal", HOST_INSTANCE),
        ObservationProducerIdentity(
            "ordivon-harness", "harness-journal", HARNESS_INSTANCE
        ),
        ObservationProducerIdentity(
            "ordivon-runtime", "runtime-registry", RUNTIME_INSTANCE
        ),
    )
    mappings = (
        ("ordivon-host", "host-journal", "host-observation-v1"),
        ("ordivon-harness", "harness-journal", "harness-observation-v1"),
        ("ordivon-runtime", "runtime-registry", "runtime-observation-v1"),
    )
    gateway_root = root / "gateway"
    with SQLiteObservationGateway.initialize(
        gateway_root,
        gateway_instance_id="observation-gateway:b4-smoke",
        producer_allowlist=producers,
        mapping_versions=mappings,
        created_at_ms=8_100,
    ) as gateway:
        for offset, bundle in enumerate((bundles[2], bundles[0], bundles[1])):
            for batch in bundle.batches:
                gateway.ingest(batch, ingested_at_ms=8_200 + offset)
        if not gateway.doctor(full=True)["healthy"]:
            raise SmokeError("B4 Observation Gateway Doctor failed")
        selection = select_cross_owner_trajectory(
            gateway,
            TrajectoryQuerySpec(
                query_id="trajectory-query:b4-scripted-smoke",
                anchor_kind="ordivon.host.task",
                anchor_id=HOST_TASK_ID,
                artifact_coverage="owner_native_only",
            ),
        )
    if not selection.completeness["complete"]:
        raise SmokeError("B4 cross-owner Selection is incomplete")
    return selection.to_dict()


def event_count(storage: HostStorage, task_id: str, kind: EventKind) -> int:
    row = storage.journal.connection.execute(
        "SELECT COUNT(*) FROM events WHERE stream_id=? AND event_kind=?",
        (task_id, kind.value),
    ).fetchone()
    if row is None:
        raise SmokeError("Host event count query returned no row")
    return int(row[0])


def host_accept(
    host_root: Path,
    host_clock: Clock,
    verification: dict[str, Any],
) -> dict[str, Any]:
    with HostStorage(host_root) as storage:
        kernel = HostKernel(
            storage,
            clock_ms=host_clock,
            owner_id="host:b4-scripted-smoke-reopen",
        )
        coordinator = ExternalExecutorCoordinator(HostExtensionPort(storage, kernel))
        current = coordinator.load(HOST_TASK_ID)
        if current.completion_proposal is None:
            raise SmokeError("Host lost Completion Proposal before verification")
        retained = tuple(
            item
            for item in (
                current.request_object,
                current.binding_object,
                current.completion_proposal_object,
            )
            if item is not None
        )
        snapshot = storage.read_task_event(HOST_TASK_ID)
        if not isinstance(snapshot.data, dict):
            raise SmokeError("Host Task data is not an object")
        with kernel.locked_task(
            HOST_TASK_ID,
            expected_revision=current.projection.revision,
        ) as locked:
            recorded = locked.commit(
                event_id="event:b4-smoke:verification-recorded",
                kind=EventKind.VERIFICATION_RECORDED,
                payload={
                    **snapshot.data,
                    "verificationStatus": "passed",
                    "verifierDigest": canonical_digest(verification),
                },
                referenced_objects=retained,
            )
        snapshot = storage.read_task_event(HOST_TASK_ID)
        with kernel.locked_task(
            HOST_TASK_ID,
            expected_revision=recorded.projection.revision,
        ) as locked:
            accepted = locked.commit(
                event_id="event:b4-smoke:verification-accepted",
                kind=EventKind.VERIFICATION_ACCEPTED,
                payload={**snapshot.data, "verificationStatus": "accepted"},
                referenced_objects=retained,
            )
        snapshot = storage.read_task_event(HOST_TASK_ID)
        with kernel.locked_task(
            HOST_TASK_ID,
            expected_revision=accepted.projection.revision,
        ) as locked:
            outcome = locked.commit(
                event_id="event:b4-smoke:task-outcome",
                kind=EventKind.TASK_OUTCOME_RECORDED,
                payload={**snapshot.data, "taskOutcome": "accepted"},
                state=TaskState.COMPLETED,
                frontier=(),
                referenced_objects=retained,
            )
        if event_count(storage, HOST_TASK_ID, EventKind.TASK_OUTCOME_RECORDED) != 1:
            raise SmokeError("Host committed more than one TaskOutcome")
        return {
            "decisionRef": "host-event:event:b4-smoke:verification-accepted",
            "outcomeRef": "host-event:event:b4-smoke:task-outcome",
            "taskRevision": outcome.projection.revision,
            "taskState": outcome.projection.state.value,
        }


def run_missing_artifact_cell(
    host_root: Path,
    host_clock: Clock,
    runtime_job_id: str,
) -> dict[str, Any]:
    task_id = "task:b4-missing-artifact"
    adapter = MissingArtifactAdapter(runtime_job_id)
    with HostStorage(host_root) as storage:
        kernel = HostKernel(
            storage,
            clock_ms=host_clock,
            owner_id="host:b4-missing-artifact",
        )
        created = kernel.create_task(
            event_id="event:b4-missing-artifact:create",
            kind=EventKind.TASK_CREATED,
            task_id=task_id,
            goal_id="goal:b4-missing-artifact",
            payload={"purpose": "B4 missing Artifact fault cell"},
            frontier=("node:b4-missing-artifact",),
        ).projection
        coordinator = ExternalExecutorCoordinator(HostExtensionPort(storage, kernel))
        request = ExternalExecutionRequest(
            request_id="external-request:b4-missing-artifact",
            adapter_id=adapter.adapter_id,
            task_id=task_id,
            task_revision=created.revision,
            task_attempt_ref="task-attempt:b4-missing-artifact",
            contract_digest=DIGEST_A,
            correlation_context={"cellId": "HOST-MISSING-ARTIFACT"},
            created_at_ms=host_clock(),
        )
        coordinator.start(request, adapter)
        completed = coordinator.collect_completion(task_id, adapter)
        proposal = completed.completion_proposal
        if proposal is None or proposal.artifact_refs:
            raise SmokeError("missing Artifact cell did not produce an empty Artifact set")
        snapshot = storage.read_task_event(task_id)
        retained = tuple(
            item
            for item in (
                completed.request_object,
                completed.binding_object,
                completed.completion_proposal_object,
            )
            if item is not None
        )
        with kernel.locked_task(
            task_id,
            expected_revision=completed.projection.revision,
        ) as locked:
            rejected = locked.commit(
                event_id="event:b4-missing-artifact:verification-rejected",
                kind=EventKind.VERIFICATION_RECORDED,
                payload={
                    **snapshot.data,
                    "verificationStatus": "rejected",
                    "reasonCode": "required_completion_artifact_missing",
                },
                referenced_objects=retained,
            )
        outcomes = event_count(storage, task_id, EventKind.TASK_OUTCOME_RECORDED)
        return {
            "passed": (
                outcomes == 0
                and not rejected.projection.state.terminal
                and rejected.projection.state is TaskState.READY
            ),
            "runtimeJobRef": runtime_job_id,
            "taskOutcomeCount": outcomes,
            "taskState": rejected.projection.state.value,
        }


def validate_system_manifest_record(value: dict[str, Any]) -> None:
    path = EXPERIMENT / "validate_p0_artifacts.py"
    spec = importlib.util.spec_from_file_location("b4_p0_validator", path)
    if spec is None or spec.loader is None:
        raise SmokeError("System Manifest validator cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_system_manifest(value)


def system_manifest(
    *,
    environment_digest: str,
    prompt_digest: str,
    context_digest: str,
    budget_digest: str,
    snapshot_digest: str,
) -> dict[str, Any]:
    def ref(path: str) -> dict[str, str]:
        return {"path": path, "digest": file_digest(COMPUTING_ROOT / path)}

    value = with_integrity(
        {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-system-manifest",
            "manifestId": "b4-scripted-integrated-control-v1",
            "capturedAt": now_iso(),
            "systemSnapshot": {
                "path": "system-snapshot.json",
                "digest": snapshot_digest,
            },
            "configuration": {
                "provider": {
                    "providerId": "scripted",
                    "modelId": "deterministic-oracle-actions",
                    "modelRevision": "1",
                    "adapterRevision": HARNESS_IMPLEMENTATION_REVISION,
                },
                "digests": {
                    "promptSet": prompt_digest,
                    "contextPolicy": context_digest,
                    "toolCatalog": INDEPENDENT_REPOSITORY_REPAIR_TOOL_SURFACE_DIGEST,
                    "toolGrant": INDEPENDENT_REPOSITORY_REPAIR_TOOL_GRANT_DIGEST,
                    "budgetProfile": budget_digest,
                    "environment": environment_digest,
                },
            },
            "evaluationContract": {
                "suite": ref(
                    "research/experiments/harness-evaluation-v0/suite-v1.json"
                ),
                "taskSchema": ref(
                    "research/experiments/harness-evaluation-v0/schemas/task.schema.json"
                ),
                "trialSchema": ref(
                    "research/experiments/harness-evaluation-v0/schemas/trial.schema.json"
                ),
                "resultSchema": ref(
                    "research/experiments/harness-evaluation-v0/schemas/result.schema.json"
                ),
                "failureSchema": ref(
                    "research/experiments/harness-evaluation-v0/schemas/failure-record.schema.json"
                ),
                "failureTaxonomy": ref(
                    "research/experiments/harness-evaluation-v0/failure-taxonomy.yaml"
                ),
                "graderSet": {
                    "path": (
                        "evals/harness-repository-repair-001/"
                        "verifier/test_outcome.py"
                    ),
                    "digest": file_digest(
                        HARNESS_ROOT
                        / "evals"
                        / "harness-repository-repair-001"
                        / "verifier"
                        / "test_outcome.py"
                    ),
                },
            },
            "privacy": {"secretsIncluded": False, "rawReasoningRequired": False},
            "unavailableFields": [],
            "limitations": [
                "The Provider is scripted and competitive=false.",
                "Runtime Artifact traversal in Observation remains owner-native only.",
                "No result from this smoke is a model capability claim.",
            ],
        }
    )
    validate_system_manifest_record(value)
    return value


def validate_track_r_record(value: dict[str, Any]) -> None:
    path = EXPERIMENT / "validate_evaluation_evidence.py"
    spec = importlib.util.spec_from_file_location("b4_track_r_validator", path)
    if spec is None or spec.loader is None:
        raise SmokeError("Track R validator cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_document(value)


def run(args: argparse.Namespace) -> dict[str, Any]:
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SmokeError("ORDIVON_BEARER_TOKEN is not set")
    computing_revision = git(COMPUTING_ROOT, "rev-parse", "HEAD")
    dirty = bool(git(COMPUTING_ROOT, "status", "--porcelain"))
    if dirty and not args.allow_dirty_computing:
        raise SmokeError("Computing repository must be clean")
    for repo, expected in (
        (HOST_ROOT, HOST_REVISION),
        (HARNESS_ROOT, HARNESS_REVISION),
        (RUNTIME_ROOT, RUNTIME_REVISION),
    ):
        if git(repo, "rev-parse", "HEAD") != expected or git(repo, "status", "--porcelain"):
            raise SmokeError(f"owner revision or cleanliness differs: {repo.name}")

    registry_root = args.runtime_registry_root
    if registry_root is None:
        configured = os.environ.get("ORDIVON_REGISTRY_ROOT")
        if not configured:
            raise SmokeError("Runtime Registry root is not configured")
        registry_root = Path(configured)
    client = McpRuntimeClient(
        args.runtime_endpoint,
        token,
        client_name="ordivon-b4-formal-smoke",
        client_version="1.0.0",
    )
    client.initialize()

    temporary = Path(tempfile.mkdtemp(prefix="ordivon-b4-smoke-"))
    output = args.output_root.resolve() if args.output_root else temporary / "trial"
    workspace_id: str | None = None
    workspace_closed = False
    try:
        source_root = temporary / "source"
        extracted_revision = extract_historical_fixture(source_root)
        protected = {
            "SPEC.md": file_digest(source_root / "SPEC.md"),
            "test_allocation.py": file_digest(source_root / "test_allocation.py"),
        }
        initial_source = (source_root / "allocation.py").read_text(encoding="utf-8")
        oracle_source = (
            HARNESS_ROOT
            / "evals"
            / "harness-repository-repair-001"
            / "oracle"
            / "allocation.py"
        ).read_text(encoding="utf-8")
        completion = build_completion_artifact(oracle_source)
        completion_text = json.dumps(
            completion, indent=2, ensure_ascii=False, sort_keys=True
        ) + "\n"
        opened = client.call_tool(
            "workspace.open",
            {
                "schemaVersion": 1,
                "sourceRepo": str(source_root),
                "sourceRevision": extracted_revision,
            },
        )
        observed_workspace = opened.get("workspaceId")
        if not isinstance(observed_workspace, str):
            raise SmokeError("Runtime workspace.open omitted identity")
        workspace_id = observed_workspace

        trial = TrialRecordStore.initialize(
            output,
            trial_id=TRIAL_ID,
            configuration_id=CONFIGURATION_ID,
            task_ref={"taskId": TASK_ID, "taskVersion": TASK_VERSION},
            created_at_ms=int(time.time_ns() // 1_000_000),
        )
        trial.advance(
            expected_stage="planned",
            next_stage="prepared",
            updated_at_ms=int(time.time_ns() // 1_000_000),
        )
        prompt = (
            "Repair allocation.py according to SPEC.md, run visible-tests, inspect the diff, "
            "and create artifacts/completion.json with the required structured claim."
        )
        budget_value = {
            "maxModelCalls": 8,
            "maxToolCalls": 20,
            "maxRuntimeJobs": 8,
            "maxObservationBytes": 1_048_576,
            "maxWallTimeMs": 600_000,
            "maxInputTokens": 1_000_000,
            "maxOutputTokens": 100_000,
        }
        environment = {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "runtimeEndpoint": args.runtime_endpoint,
            "historicalHostRevision": HISTORICAL_HOST_REVISION,
            "extractedSourceRevision": extracted_revision,
        }
        snapshot = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-system-snapshot",
                "computingRevision": computing_revision,
                "hostRevision": HOST_REVISION,
                "harnessRevision": HARNESS_REVISION,
                "harnessImplementationRevision": HARNESS_IMPLEMENTATION_REVISION,
                "runtimeRevision": RUNTIME_REVISION,
                "protocolRevision": PROTOCOL_REVISION,
                "b3ImplementationRevision": B3_IMPLEMENTATION_REVISION,
                "b3ReceiptRevision": B3_RECEIPT_REVISION,
                "sharedObservationContractRevision": SHARED_CONTRACT_REVISION,
                "productionActivated": False,
            }
        )
        snapshot_digest = trial.write_record("system-snapshot.json", snapshot)
        manifest = system_manifest(
            environment_digest=canonical_digest(environment),
            prompt_digest=canonical_digest({"prompt": prompt}),
            context_digest=canonical_digest(
                {
                    "taskId": TASK_ID,
                    "sourceRevision": HISTORICAL_HOST_REVISION,
                    "protectedFiles": protected,
                }
            ),
            budget_digest=canonical_digest(budget_value),
            snapshot_digest=snapshot_digest,
        )
        manifest_digest = trial.write_record("system-manifest.json", manifest)
        trial.advance(
            expected_stage="prepared",
            next_stage="executing",
            updated_at_ms=int(time.time_ns() // 1_000_000),
            records=("system-snapshot.json", "system-manifest.json"),
        )

        host_root = temporary / "host"
        harness_root = temporary / "harness"
        host_clock = Clock(10_000)
        harness_clock = Clock(20_000)
        contract = build_contract(harness_clock())
        runtime = LossyRuntimeClient(client)
        capture = ExecutionCapture()
        patch_old = initial_source[initial_source.index("    weight_total") :]
        patch_new = oracle_source[oracle_source.index("    weight_total") :]
        tool_identity = workspace_id.removeprefix("workspace:").replace(":", "-")
        calls = (
            AgentToolCall(
                f"tool-call:b4:{tool_identity}:read-spec",
                "read_workspace",
                {"relativePath": "SPEC.md", "mode": "FULL"},
            ),
            AgentToolCall(
                f"tool-call:b4:{tool_identity}:read-source",
                "read_workspace",
                {"relativePath": "allocation.py", "mode": "FULL"},
            ),
            AgentToolCall(
                f"tool-call:b4:{tool_identity}:patch",
                "patch_workspace",
                {
                    "files": [
                        {
                            "relativePath": "allocation.py",
                            "expectedDigest": text_digest(initial_source),
                            "edits": [
                                {
                                    "range": edit_range(initial_source, patch_old),
                                    "expectedText": patch_old,
                                    "replacement": patch_new,
                                }
                            ],
                        },
                        {
                            "relativePath": "artifacts/completion.json",
                            "expectedDigest": None,
                            "edits": [
                                {
                                    "range": {
                                        "start": {"line": 1, "column": 0},
                                        "end": {"line": 1, "column": 0},
                                    },
                                    "expectedText": "",
                                    "replacement": completion_text,
                                }
                            ],
                        },
                    ],
                    "maxDiffBytes": 65_536,
                },
            ),
            AgentToolCall(
                f"tool-call:b4:{tool_identity}:visible-check",
                "run_check",
                {
                    "checkId": "visible-tests",
                    "waitMs": 30_000,
                    "stdoutTailBytes": 65_536,
                    "stderrTailBytes": 65_536,
                },
            ),
            AgentToolCall(
                f"tool-call:b4:{tool_identity}:diff",
                "diff_workspace",
                {"maxBytes": 65_536},
            ),
        )
        turns = tuple(
            agent_turn(index, call) for index, call in enumerate(calls, start=1)
        ) + (completion_turn(workspace_id),)

        def resolve(request) -> HarnessRunContract:
            if request.request_id != EXTERNAL_REQUEST_ID:
                raise SmokeError("unexpected external request")
            return contract

        def driver_factory(
            run_contract: HarnessRunContract,
            continuity: SQLiteHarnessRunContinuityStore,
        ) -> Driver:
            capture.driver_creations += 1
            bridge = SQLiteHarnessRepositoryRepairRuntimeBridge(
                run_contract,
                continuity,
                build_execution_binding(run_contract, continuity, workspace_id),
                runtime,
            )
            runner = StandaloneHarnessRunner(
                run_contract,
                continuity,
                ScriptedTurnAdapter(turns),
                bridge,
                budget=RunBudget(
                    max_model_calls=8,
                    max_tool_calls=20,
                    max_observation_bytes=1_048_576,
                    max_wall_time_ms=600_000,
                    max_total_tokens=1_100_000,
                    max_model_retries=1,
                ),
                clock_ms=harness_clock,
                monotonic_ms=harness_clock,
            )
            return Driver(
                runner,
                capture,
                ({"role": "user", "content": prompt},),
            )

        delegate = OrdivonHarnessExternalExecutorAdapter(
            harness_root,
            contract_resolver=resolve,
            driver_factory=driver_factory,
            clock_ms=harness_clock,
        )
        lossy = LossyExternalAdapter(delegate)
        with HostStorage(host_root) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=host_clock,
                owner_id="host:b4-scripted-smoke",
            )
            created = kernel.create_task(
                event_id="event:b4-smoke:task-created",
                kind=EventKind.TASK_CREATED,
                task_id=HOST_TASK_ID,
                goal_id=HOST_GOAL_ID,
                payload={"taskId": TASK_ID, "taskVersion": TASK_VERSION},
                frontier=("node:b4-scripted-smoke",),
            ).projection
            request = ExternalExecutionRequest(
                request_id=EXTERNAL_REQUEST_ID,
                adapter_id=lossy.adapter_id,
                task_id=HOST_TASK_ID,
                task_revision=created.revision,
                task_attempt_ref=HOST_ATTEMPT_REF,
                contract_digest=contract.digest,
                correlation_context={"trialId": TRIAL_ID},
                created_at_ms=host_clock(),
            )
            coordinator = ExternalExecutorCoordinator(HostExtensionPort(storage, kernel))
            try:
                coordinator.start(request, lossy)
            except RuntimeError as error:
                if "delivery loss" not in str(error):
                    raise
            else:
                raise SmokeError("Host response-loss injection did not fire")
            gap = coordinator.load(HOST_TASK_ID)
            if gap.request != request or gap.binding is not None:
                raise SmokeError("Host did not retain request-only delivery gap")
            bound = coordinator.start(request, lossy)
            if bound.binding is None or bound.binding.foreign_run_ref != HARNESS_RUN_ID:
                raise SmokeError("Host did not bind the recovered Harness Run")
            if capture.loop_result is None:
                raise SmokeError("independent Harness produced no loop result")
            if not capture.loop_result.candidate_completed:
                statuses = [
                    {
                        "tool": item.tool_name,
                        "status": item.status,
                        "errorType": item.structured_content.get("type"),
                    }
                    for item in capture.loop_result.observations
                ]
                final_event = (
                    capture.loop_result.trace.events[-1].to_dict()
                    if capture.loop_result.trace.events
                    else None
                )
                raise SmokeError(
                    "independent Harness did not reach candidate completion: "
                    f"stop={capture.loop_result.stop_code.value} "
                    f"observations={statuses} finalEvent={final_event}"
                )
            completed = coordinator.collect_completion(HOST_TASK_ID, lossy)
            if completed.completion_proposal is None:
                raise SmokeError("Host did not collect Completion Proposal")
        if capture.driver_creations != 1 or lossy.start_calls != 2:
            raise SmokeError("Host response loss caused duplicate Harness execution")
        if runtime.exec_dispatches != 1 or len(runtime.job_ids) != 1:
            raise SmokeError("Runtime response loss caused duplicate Job dispatch")
        runtime_job_id = next(iter(runtime.job_ids))

        candidate_source = read_workspace(client, workspace_id, "allocation.py")
        completion_observed = read_workspace(
            client, workspace_id, "artifacts/completion.json"
        )
        spec_observed = read_workspace(client, workspace_id, "SPEC.md")
        tests_observed = read_workspace(client, workspace_id, "test_allocation.py")
        if text_digest(spec_observed) != protected["SPEC.md"] or text_digest(
            tests_observed
        ) != protected["test_allocation.py"]:
            raise SmokeError("protected Workspace files changed")
        verifier = run_verifier(
            temporary,
            candidate_source=candidate_source,
            completion_text=completion_observed,
            protected=protected,
        )
        if not all(
            verifier[key]
            for key in (
                "visiblePassed",
                "hiddenPassed",
                "protectedFilesUnchanged",
            )
        ):
            raise SmokeError(f"independent verifier failed: {verifier}")

        # The decision occurs only after all Host/Harness process objects were closed.
        decision = host_accept(host_root, host_clock, verifier)
        with HostStorage(host_root) as reopened_host:
            if event_count(
                reopened_host, HOST_TASK_ID, EventKind.TASK_OUTCOME_RECORDED
            ) != 1:
                raise SmokeError("Host TaskOutcome count changed after reopen")
        with SQLiteHarnessStore(harness_root) as reopened_harness:
            if not reopened_harness.doctor(full=True)["healthy"]:
                raise SmokeError("Harness Doctor failed after restart")
            harness_event_count = len(
                reopened_harness.list_run_events(HARNESS_RUN_ID)
            )
        missing_artifact = run_missing_artifact_cell(
            host_root, host_clock, runtime_job_id
        )
        if not missing_artifact["passed"]:
            raise SmokeError("Host missing-Artifact fault cell failed")

        runtime_snapshot = temporary / "runtime-snapshot"
        copy_runtime_job(registry_root, runtime_snapshot, runtime_job_id)
        selection = build_selection(
            temporary,
            host_root,
            harness_root,
            runtime_snapshot,
        )
        native_refs = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-native-refs",
                "trialId": TRIAL_ID,
                "hostTaskId": HOST_TASK_ID,
                "hostTaskAttemptRef": HOST_ATTEMPT_REF,
                "externalRequestId": EXTERNAL_REQUEST_ID,
                "harnessRunId": HARNESS_RUN_ID,
                "runtimeWorkspaceId": workspace_id,
                "runtimeJobId": runtime_job_id,
                "completionArtifactRef": (
                    f"workspace-artifact:{workspace_id}:artifacts/completion.json"
                ),
                "decisionRef": decision["decisionRef"],
                "outcomeRef": decision["outcomeRef"],
            }
        )
        grader_bundle = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-grader-bundle",
                "trialId": TRIAL_ID,
                "verifierId": "HARNESS-REPO-REPAIR-001-verifier",
                "verifierRevision": "1",
                "visible": {
                    "status": "passed",
                    "digest": verifier["visibleDigest"],
                },
                "hidden": {
                    "status": "passed",
                    "digest": verifier["hiddenDigest"],
                },
                "protectedFilesUnchanged": True,
                "completionArtifactDigest": verifier["completionArtifactDigest"],
                "candidateSourceDigest": verifier["candidateSourceDigest"],
                "disagreement": False,
            }
        )
        trial.write_record("native-refs.json", native_refs, minimum_stage="executing")
        trial.write_record("grader-bundle.json", grader_bundle, minimum_stage="executing")
        trial.advance(
            expected_stage="executing",
            next_stage="evidence_collected",
            updated_at_ms=int(time.time_ns() // 1_000_000),
            records=("native-refs.json", "grader-bundle.json"),
        )
        trial.admit_selection(selection)

        intent_created_at = trial.intent().get("createdAtMs")
        if not isinstance(intent_created_at, int):
            raise SmokeError("Trial intent omitted createdAtMs")
        started_at_ms = intent_created_at
        completed_at_ms = int(time.time_ns() // 1_000_000)
        task_ref = {"taskId": TASK_ID, "taskVersion": TASK_VERSION}
        trial_manifest = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-trial",
                "trialId": TRIAL_ID,
                "taskRef": task_ref,
                "executionPath": "ordivon_harness",
                "model": {
                    "providerId": "scripted",
                    "modelId": "deterministic-oracle-actions",
                    "modelRevision": "1",
                    "adapterRevision": HARNESS_IMPLEMENTATION_REVISION,
                },
                "harness": {
                    "harnessId": "ordivon-harness",
                    "harnessRevision": HARNESS_REVISION,
                    "manifestDigest": manifest_digest,
                },
                "bindings": {
                    "sourceRevision": HISTORICAL_HOST_REVISION,
                    "environmentDigest": canonical_digest(environment),
                    "contextDigest": canonical_digest(
                        {"prompt": prompt, "protectedFiles": protected}
                    ),
                    "toolCatalogDigest": INDEPENDENT_REPOSITORY_REPAIR_TOOL_SURFACE_DIGEST,
                    "systemSnapshotRef": "system-snapshot.json",
                    "systemManifestRef": {
                        "repositoryId": "ordivon-computing",
                        "path": "system-manifest.json",
                        "digest": manifest_digest,
                    },
                },
                "sampling": {
                    "seed": 0,
                    "temperature": 0,
                    "topP": 1,
                    "reasoningEffort": "none",
                },
                "budget": budget_value,
                "startedAtMs": started_at_ms,
                "completedAtMs": completed_at_ms,
                "sourceEvidenceRefs": [
                    {
                        "repositoryId": "ordivon-computing",
                        "path": "observation-selection.json",
                        "digest": selection["integrity"]["payloadDigest"],
                    },
                    {
                        "repositoryId": "ordivon-harness",
                        "path": "evidence/repository-repair-runtime-bridge-7664240.json",
                        "digest": (
                            "sha256:bf86a6c6c35d03379aa136ed7917a41d563ef9e0f3562f67ca863271d9739514"
                        ),
                    },
                ],
                "limitations": [
                    "Scripted non-competitive smoke.",
                    "Runtime Artifact traversal is owner-native only.",
                ],
            }
        )
        validate_track_r_record(trial_manifest)
        trial.write_record("trial.json", trial_manifest, minimum_stage="evidence_collected")

        loop = capture.loop_result
        metrics = {
            "modelCalls": loop.model_calls,
            "toolCalls": loop.tool_calls,
            "runtimeJobs": len(runtime.job_ids),
            "observationBytes": len(
                json.dumps(
                    [item.to_dict() for item in loop.observations],
                    sort_keys=True,
                ).encode("utf-8")
            ),
            "inputTokens": 60,
            "outputTokens": 30,
            "cachedInputTokens": 0,
            "reasoningTokens": 0,
            "totalTokens": 90,
            "wallTimeMs": max(0, completed_at_ms - started_at_ms),
            "estimatedCostUsd": 0,
            "repeatedReads": 0,
            "repeatedCommands": 0,
            "invalidToolCalls": 0,
            "humanInterventionCount": 0,
        }
        completion_digest = text_digest(completion_observed)
        result = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-result",
                "trialId": TRIAL_ID,
                "taskRef": task_ref,
                "stopCode": loop.stop_code.value,
                "acceptance": {
                    "status": "accepted",
                    "decisionRef": decision["decisionRef"],
                    "falseCompletion": False,
                    "verifier": {
                        "verifierId": "HARNESS-REPO-REPAIR-001-verifier",
                        "verifierRevision": "1",
                        "status": "passed",
                        "assertions": [
                            {
                                "assertionId": "visible-tests-pass",
                                "status": "passed",
                                "evidenceRefs": [verifier["visibleDigest"]],
                            },
                            {
                                "assertionId": "hidden-tests-pass",
                                "status": "passed",
                                "evidenceRefs": [verifier["hiddenDigest"]],
                            },
                            {
                                "assertionId": "protected-files-unchanged",
                                "status": "passed",
                                "evidenceRefs": list(protected.values()),
                            },
                            {
                                "assertionId": "exactly-one-task-outcome",
                                "status": "passed",
                                "evidenceRefs": [decision["outcomeRef"]],
                            },
                        ],
                    },
                },
                "metrics": metrics,
                "artifacts": [
                    {
                        "ref": (
                            f"workspace-artifact:{workspace_id}:artifacts/completion.json"
                        ),
                        "kind": "completion",
                        "digest": completion_digest,
                        "valid": True,
                    }
                ],
                "trace": {
                    "digest": loop.trace.digest,
                    "eventCount": len(loop.trace.events),
                    "ref": f"harness-run:{HARNESS_RUN_ID}",
                },
                "failureRefs": [],
                "limitations": [
                    "The Provider is scripted.",
                    "The result proves runner integrity, not Agent capability.",
                ],
            }
        )
        validate_track_r_record(result)
        trial.write_record("result.json", result, minimum_stage="evidence_collected")
        fault_cells = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-b4-integrated-fault-cells",
                "trialId": TRIAL_ID,
                "runtimeResponseLoss": {
                    "passed": runtime.exec_dispatches == 1
                    and "task.list" in runtime.calls
                    and "task.observe" in runtime.calls,
                    "physicalDispatches": runtime.exec_dispatches,
                    "runtimeJobCount": len(runtime.job_ids),
                },
                "hostExternalResponseLoss": {
                    "passed": capture.driver_creations == 1 and lossy.start_calls == 2,
                    "physicalHarnessExecutions": capture.driver_creations,
                    "adapterStartCalls": lossy.start_calls,
                },
                "crossRestartAfterRun": {
                    "passed": decision["taskState"] == "completed",
                    "taskOutcomeCount": 1,
                    "providerSessionRequired": False,
                },
                "hostMissingArtifact": missing_artifact,
            }
        )
        trial.write_record(
            "integrated-fault-cells.json",
            fault_cells,
            minimum_stage="evidence_collected",
        )
        deterministic_fault_cells = run_b4_fault_cells(
            computing_root=COMPUTING_ROOT,
            harness_root=HARNESS_ROOT,
            harness_revision=HARNESS_REVISION,
        )
        trial.write_record(
            "deterministic-fault-cells.json",
            deterministic_fault_cells,
            minimum_stage="evidence_collected",
        )
        trial.advance(
            expected_stage="evidence_collected",
            next_stage="verified",
            updated_at_ms=int(time.time_ns() // 1_000_000),
            records=(
                "observation-selection.json",
                "trial.json",
                "result.json",
                "integrated-fault-cells.json",
                "deterministic-fault-cells.json",
            ),
        )
        trial.dispose(
            TrialDisposition(
                trial_id=TRIAL_ID,
                validity="valid",
                semantic_outcome="accepted",
                comparative_outcome="not_applicable",
                failure_attribution="none",
                comparison_eligible=False,
                reasons=(
                    "scripted integrated smoke passed",
                    "cross-owner Observation Selection complete",
                    "independent verifier and Host acceptance passed",
                ),
                selection_digest=selection["selectionDigest"],
            ),
            updated_at_ms=int(time.time_ns() // 1_000_000),
        )
        review = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-review",
                "trialId": TRIAL_ID,
                "reviewRequired": True,
                "reviewStatus": "completed",
                "findings": [
                    "Both injected response-loss paths reconciled without duplicate dispatch.",
                    "Fresh Host/Harness reopen produced exactly one semantic TaskOutcome.",
                    "Runtime success without the required Artifact produced no TaskOutcome.",
                ],
                "liveTrialUnlocked": True,
                "b6Implemented": False,
            }
        )
        trial.write_record("review.json", review, minimum_stage="disposed")

        client.call_tool(
            "workspace.close",
            {"schemaVersion": 1, "workspaceId": workspace_id, "force": True},
        )
        workspace_closed = workspace_absent(client, workspace_id)
        if not workspace_closed:
            raise SmokeError("Runtime Workspace remained after close")
        closeout = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-b4-smoke-closeout",
                "workPackage": "B4",
                "implementationRevision": computing_revision,
                "computingClean": not dirty,
                "trialId": TRIAL_ID,
                "systemManifestDigest": manifest_digest,
                "selectionDigest": selection["selectionDigest"],
                "resultDigest": result["integrity"]["payloadDigest"],
                "dispositionDigest": trial.record("disposition.json")["integrity"][
                    "payloadDigest"
                ],
                "runtimeJobId": runtime_job_id,
                "harnessRunId": HARNESS_RUN_ID,
                "hostTaskId": HOST_TASK_ID,
                "harnessEventCount": harness_event_count,
                "workspaceClosed": workspace_closed,
                "integratedFaultCells": {
                    "runtimeResponseLoss": True,
                    "hostExternalResponseLoss": True,
                    "crossRestartAfterRun": True,
                    "hostMissingArtifact": True,
                },
                "deterministicFaultCellsDigest": deterministic_fault_cells[
                    "integrity"
                ]["payloadDigest"],
                "deterministicFaultCells": {
                    item["cellId"]: item["status"] == "passed"
                    for item in deterministic_fault_cells["cells"]
                },
                "pendingDeterministicUnitCells": [],
                "liveTrialUnlocked": True,
                "productionActivated": False,
                "b6Implemented": False,
            }
        )
        trial.write_record("closeout.json", closeout, minimum_stage="disposed")
        trial.advance(
            expected_stage="disposed",
            next_stage="closed",
            updated_at_ms=int(time.time_ns() // 1_000_000),
            records=("review.json", "closeout.json"),
        )
        if not trial.doctor()["healthy"]:
            raise SmokeError("Formal Runner Doctor failed")
        return closeout
    finally:
        if workspace_id is not None and not workspace_closed:
            try:
                client.call_tool(
                    "workspace.close",
                    {
                        "schemaVersion": 1,
                        "workspaceId": workspace_id,
                        "force": True,
                    },
                )
            except Exception:
                pass
        if args.output_root is None:
            shutil.rmtree(temporary, ignore_errors=True)
        else:
            # Trial evidence is retained, disposable owner and verifier roots are removed.
            for child in temporary.iterdir():
                if child.resolve() != output.resolve():
                    if child.is_dir():
                        shutil.rmtree(child, ignore_errors=True)
                    else:
                        child.unlink(missing_ok=True)
            if temporary.exists() and not any(temporary.iterdir()):
                temporary.rmdir()


def main() -> int:
    args = parse_args()
    try:
        result = run(args)
    except Exception as error:
        print(f"B4 deterministic smoke: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
