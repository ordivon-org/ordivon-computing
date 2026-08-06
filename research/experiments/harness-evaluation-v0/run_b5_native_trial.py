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

import run_b4_deterministic_smoke as b4  # noqa: E402
from formal_runner import (  # noqa: E402
    TrialDisposition,
    TrialRecordStore,
    canonical_digest,
    validate_completion_artifact,
    with_integrity,
)
from ordivon_host import EventKind, HostKernel, HostStorage, TaskState  # noqa: E402
from ordivon_host.external_executor import (  # noqa: E402
    ExternalExecutionRequest,
    ExternalExecutorCoordinator,
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
from ordivon_harness.observation_export import export_harness_observations  # noqa: E402
from ordivon_harness.ordivon.deepseek import (  # noqa: E402
    DeepSeekSettings,
    DeepSeekTurnAdapter,
)
from ordivon_harness.ordivon.loop import RunBudget  # noqa: E402
from ordivon_harness.ordivon.sqlite_repository_repair_bridge import (  # noqa: E402
    INDEPENDENT_REPOSITORY_REPAIR_TOOL_GRANT_DIGEST,
    INDEPENDENT_REPOSITORY_REPAIR_TOOL_SURFACE_DIGEST,
    SQLiteHarnessRepositoryRepairRuntimeBridge,
)
from ordivon_harness.ordivon.sqlite_run_store import (  # noqa: E402
    SQLiteHarnessRunContinuityStore,
)
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
CONFIGURATION_ID = "ordivon-harness-deepseek"
HISTORICAL_HOST_REVISION = "b4bc43a4ea7eb1e7771644d507bc4a3a39b4e741"
HOST_REVISION = "a76a620160b28d870670696e04c39e539296fe00"
HOST_EXPORTER_REVISION = "e1c134f330a90c15495126a67021b06c56245156"
HARNESS_REVISION = "ac10497f1b6e681899cfe98c347ed6d48941ba23"
HARNESS_EXPORTER_REVISION = "e3cb34b4991b5f52e1c0ed0151ea17b067e88e16"
RUNTIME_REVISION = "a455fd01ce0dea25684956e5e5da899d41832a1b"
RUNTIME_EXPORTER_REVISION = "a455fd01ce0dea25684956e5e5da899d41832a1b"
PROTOCOL_REVISION = "420dc356cb664d75db0f34f356156baebe5843db"
B4_IMPLEMENTATION_REVISION = "78de3a6225802ea6eb7d8970eaabc1cca1e25407"
B4_RECEIPT_REVISION = "fe4ba60c56f58017513b00b8b8fc54d0e7ffa57a"
B4_CLOSEOUT_DIGEST = "sha256:51ffa2bc77e474f355e99d07356d515b84718379412c93ab833e5a2c2b2e23f5"
SHARED_CONTRACT_REVISION = "b0973311d84b0debe30ca002e15e02401e16ee36"
DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
DIGEST_C = "sha256:" + "c" * 64


class NativeTrialError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class TrialIds:
    number: int
    suffix: str
    trial_id: str
    host_task_id: str
    host_goal_id: str
    host_attempt_ref: str
    external_request_id: str
    harness_run_id: str
    host_instance: str
    harness_instance: str
    runtime_instance: str

    @classmethod
    def build(cls, number: int) -> "TrialIds":
        if not 1 <= number <= 999:
            raise ValueError("Trial number must be between 1 and 999")
        suffix = f"b5-native-{number:03d}"
        return cls(
            number=number,
            suffix=suffix,
            trial_id=f"trial:{suffix}",
            host_task_id=f"task:{suffix}",
            host_goal_id=f"goal:{suffix}",
            host_attempt_ref=f"task-attempt:{suffix}",
            external_request_id=f"external-request:{suffix}",
            harness_run_id=f"harness-run:{suffix}",
            host_instance=f"host:{suffix}",
            harness_instance=f"harness:{suffix}",
            runtime_instance=f"runtime:{suffix}",
        )


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

    def execute(self):
        execution = self.runner.run(self.initial_messages)
        self.capture.loop_result = execution.loop_result
        return execution


class RuntimeRecorder:
    def __init__(self, delegate: McpRuntimeClient) -> None:
        self.delegate = delegate
        self.calls: list[str] = []
        self.job_ids: set[str] = set()

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(name)
        result = self.delegate.call_tool(name, arguments)
        self._capture(result)
        return result

    def _capture(self, value: dict[str, Any]) -> None:
        job_id = value.get("jobId")
        if isinstance(job_id, str):
            self.job_ids.add(job_id)
        jobs = value.get("jobs")
        if isinstance(jobs, list):
            for item in jobs:
                if isinstance(item, dict) and isinstance(item.get("jobId"), str):
                    self.job_ids.add(item["jobId"])


@dataclass(frozen=True, slots=True)
class CandidateEvaluation:
    accepted: bool
    visible_passed: bool
    hidden_passed: bool
    protected_files_unchanged: bool
    completion_artifact_valid: bool
    candidate_source_digest: str
    completion_artifact_digest: str | None
    visible_digest: str
    hidden_digest: str
    failure_codes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "visiblePassed": self.visible_passed,
            "hiddenPassed": self.hidden_passed,
            "protectedFilesUnchanged": self.protected_files_unchanged,
            "completionArtifactValid": self.completion_artifact_valid,
            "candidateSourceDigest": self.candidate_source_digest,
            "completionArtifactDigest": self.completion_artifact_digest,
            "visibleDigest": self.visible_digest,
            "hiddenDigest": self.hidden_digest,
            "failureCodes": list(self.failure_codes),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one B5 native DeepSeek Trial")
    parser.add_argument("--trial-number", type=int, required=True)
    parser.add_argument(
        "--deepseek-secret",
        type=Path,
        default=Path("/root/.config/ordivon/secrets/deepseek.json"),
    )
    parser.add_argument("--runtime-endpoint", default="http://127.0.0.1:8897/mcp")
    parser.add_argument("--runtime-registry-root", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
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


def build_contract(
    ids: TrialIds,
    *,
    settings: DeepSeekSettings,
    manifest_digest: str,
    prompt_digest: str,
    context_digest: str,
    created_at_ms: int,
) -> HarnessRunContract:
    return HarnessRunContract(
        harness_run_id=ids.harness_run_id,
        harness_implementation_id=f"ordivon-harness@{HARNESS_REVISION}",
        caller_id="caller:ordivon-host",
        caller_run_ref=ids.external_request_id,
        objective_ref=HarnessBoundReference(
            f"objective:{ids.suffix}", "objective", prompt_digest
        ),
        context_refs=(
            HarnessBoundReference(
                f"context:{ids.suffix}", "context", context_digest
            ),
        ),
        provider_id="deepseek",
        adapter_id=DeepSeekTurnAdapter.adapter_id,
        requested_model_id=settings.model,
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
            "hostVerificationRequired": True,
        },
        system_manifest_ref=HarnessBoundReference(
            f"system-manifest:{ids.suffix}", "system-manifest", manifest_digest
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


def system_manifest(
    *,
    settings: DeepSeekSettings,
    computing_revision: str,
    environment_digest: str,
    prompt_digest: str,
    context_digest: str,
    budget_digest: str,
    snapshot_digest: str,
) -> dict[str, Any]:
    return with_integrity(
        {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-system-manifest",
            "configurationId": CONFIGURATION_ID,
            "competitive": False,
            "createdAt": now_iso(),
            "systemSnapshot": {
                "path": "system-snapshot.json",
                "digest": snapshot_digest,
            },
            "configuration": {
                "provider": {
                    "providerId": "deepseek",
                    "modelId": settings.model,
                    "modelRevision": None,
                    "adapterRevision": HARNESS_REVISION,
                    "adapterId": DeepSeekTurnAdapter.adapter_id,
                    "credentialScopeId": settings.credential_scope_id,
                    "thinkingMode": "disabled",
                    "maxOutputTokens": settings.max_output_tokens,
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
                "suite": {
                    "path": "research/experiments/harness-evaluation-v0/suite-v1.json",
                    "digest": file_digest(EXPERIMENT / "suite-v1.json"),
                },
                "task": {
                    "path": (
                        "/root/projects/ordivon-harness/evals/"
                        "harness-repository-repair-001/task.json"
                    ),
                    "digest": file_digest(
                        HARNESS_ROOT
                        / "evals"
                        / "harness-repository-repair-001"
                        / "task.json"
                    ),
                },
                "graderSet": {
                    "path": (
                        "/root/projects/ordivon-harness/evals/"
                        "harness-repository-repair-001/verifier/test_outcome.py"
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
            "privacy": {
                "secretsIncluded": False,
                "secretPathIncluded": False,
                "rawReasoningRequired": False,
            },
            "revisionAuthority": {
                "computing": computing_revision,
                "host": HOST_REVISION,
                "harness": HARNESS_REVISION,
                "runtime": RUNTIME_REVISION,
                "protocol": PROTOCOL_REVISION,
                "b4Implementation": B4_IMPLEMENTATION_REVISION,
                "b4Receipt": B4_RECEIPT_REVISION,
            },
            "limitations": [
                "This is a development baseline with three sequential valid Trials, not a model ranking.",
                "Runtime Artifact traversal in Observation remains owner-native only.",
                "Credential material and raw reasoning are excluded from evidence.",
            ],
        }
    )


def initial_messages(ids: TrialIds, workspace_id: str) -> tuple[dict[str, Any], ...]:
    artifact_ref = f"workspace-artifact:{workspace_id}:artifacts/completion.json"
    system = (
        "You are operating one bounded repository-repair Trial. Host owns acceptance; "
        "your conclusion is only a candidate proposal. Use the available tools rather "
        "than guessing. Only allocation.py and artifacts/completion.json may be changed. "
        "Read SPEC.md, allocation.py, and test_allocation.py. Implement the specified "
        "largest-remainder method, run the named visible-tests Check, inspect the final "
        "diff, and re-read allocation.py after the patch. Before submitting a candidate "
        "conclusion, create artifacts/completion.json with exactly these fields: "
        "schemaVersion=1, kind=ordivon.evaluation-completion-artifact, "
        f"taskId={TASK_ID}, taskVersion=1, sourceRevision={HISTORICAL_HOST_REVISION}, "
        "changedPaths=[\"allocation.py\"], visibleCheck={checkId:\"visible-tests\","
        "status:\"passed\"}, finalSourceDigest equal to the digest returned by the final "
        "read of allocation.py, and a concise summary. Then submit candidate_completed "
        f"with artifact_refs containing exactly {artifact_ref}. Hidden verification is "
        "independent. Do not modify protected files and do not claim Host acceptance."
    )
    user = (
        f"Execute Trial {ids.trial_id}. Repair allocate_units according to SPEC.md. "
        "Use deterministic stable tie-breaking, preserve the public API, pass the visible "
        "Check, create the required completion Artifact, and submit the bounded conclusion."
    )
    return ({"role": "system", "content": system}, {"role": "user", "content": user})


def evaluate_candidate(
    root: Path,
    *,
    candidate_source: str,
    completion_text: str | None,
    protected_observed: dict[str, str],
    protected_expected: dict[str, str],
) -> CandidateEvaluation:
    workspace = root / "verifier-workspace"
    source = root / "source"
    shutil.copytree(source, workspace)
    (workspace / "allocation.py").write_text(candidate_source, encoding="utf-8")
    failures: list[str] = []
    protected_ok = protected_observed == protected_expected
    if not protected_ok:
        failures.append("protected_files_changed")
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
    visible_ok = visible.returncode == 0
    hidden_ok = hidden.returncode == 0
    if not visible_ok:
        failures.append("visible_check_failed")
    if not hidden_ok:
        failures.append("hidden_check_failed")
    artifact_ok = False
    artifact_digest: str | None = None
    if completion_text is None:
        failures.append("completion_artifact_missing")
    else:
        artifact_digest = text_digest(completion_text)
        try:
            value = json.loads(completion_text)
            if not isinstance(value, dict):
                raise ValueError("Completion Artifact is not an object")
            validate_completion_artifact(
                value,
                task_id=TASK_ID,
                task_version=TASK_VERSION,
                source_revision=HISTORICAL_HOST_REVISION,
            )
            if value["finalSourceDigest"] != text_digest(candidate_source):
                raise ValueError("Completion Artifact source digest differs")
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            failures.append("completion_artifact_invalid")
        else:
            artifact_ok = True
    return CandidateEvaluation(
        accepted=visible_ok and hidden_ok and protected_ok and artifact_ok,
        visible_passed=visible_ok,
        hidden_passed=hidden_ok,
        protected_files_unchanged=protected_ok,
        completion_artifact_valid=artifact_ok,
        candidate_source_digest=text_digest(candidate_source),
        completion_artifact_digest=artifact_digest,
        visible_digest=text_digest(visible.stdout + visible.stderr),
        hidden_digest=text_digest(hidden.stdout + hidden.stderr),
        failure_codes=tuple(sorted(set(failures))),
    )


def host_finalize(
    ids: TrialIds,
    *,
    host_root: Path,
    host_clock: Clock,
    evaluation: CandidateEvaluation,
) -> dict[str, Any]:
    with HostStorage(host_root) as storage:
        kernel = HostKernel(
            storage,
            clock_ms=host_clock,
            owner_id=f"host:{ids.suffix}:verifier",
        )
        coordinator = ExternalExecutorCoordinator(HostExtensionPort(storage, kernel))
        current = coordinator.load(ids.host_task_id)
        retained = tuple(
            item
            for item in (
                current.request_object,
                current.binding_object,
                current.completion_proposal_object,
            )
            if item is not None
        )
        snapshot = storage.read_task_event(ids.host_task_id)
        if not isinstance(snapshot.data, dict):
            raise NativeTrialError("Host Task data is not an object")
        verification_event_id = f"event:{ids.suffix}:verification-recorded"
        with kernel.locked_task(
            ids.host_task_id,
            expected_revision=current.projection.revision,
        ) as locked:
            recorded = locked.commit(
                event_id=verification_event_id,
                kind=EventKind.VERIFICATION_RECORDED,
                payload={
                    **snapshot.data,
                    "verificationStatus": (
                        "passed" if evaluation.accepted else "failed"
                    ),
                    "verifierDigest": canonical_digest(evaluation.to_dict()),
                    "failureCodes": list(evaluation.failure_codes),
                },
                referenced_objects=retained,
            )
        decision_event_id = verification_event_id
        decision_revision = recorded.projection.revision
        if evaluation.accepted:
            snapshot = storage.read_task_event(ids.host_task_id)
            decision_event_id = f"event:{ids.suffix}:verification-accepted"
            with kernel.locked_task(
                ids.host_task_id,
                expected_revision=recorded.projection.revision,
            ) as locked:
                accepted = locked.commit(
                    event_id=decision_event_id,
                    kind=EventKind.VERIFICATION_ACCEPTED,
                    payload={**snapshot.data, "verificationStatus": "accepted"},
                    referenced_objects=retained,
                )
            decision_revision = accepted.projection.revision
        snapshot = storage.read_task_event(ids.host_task_id)
        outcome_event_id = f"event:{ids.suffix}:task-outcome"
        with kernel.locked_task(
            ids.host_task_id,
            expected_revision=decision_revision,
        ) as locked:
            outcome = locked.commit(
                event_id=outcome_event_id,
                kind=EventKind.TASK_OUTCOME_RECORDED,
                payload={
                    **snapshot.data,
                    "taskOutcome": "accepted" if evaluation.accepted else "rejected",
                    "failureCodes": list(evaluation.failure_codes),
                },
                state=TaskState.COMPLETED if evaluation.accepted else TaskState.FAILED,
                frontier=(),
                referenced_objects=retained,
            )
        if b4.event_count(
            storage, ids.host_task_id, EventKind.TASK_OUTCOME_RECORDED
        ) != 1:
            raise NativeTrialError("Host committed more than one TaskOutcome")
        return {
            "decisionRef": f"host-event:{decision_event_id}",
            "outcomeRef": f"host-event:{outcome_event_id}",
            "taskRevision": outcome.projection.revision,
            "taskState": outcome.projection.state.value,
            "semanticOutcome": "accepted" if evaluation.accepted else "rejected",
        }


def copy_runtime_jobs(
    source_root: Path,
    destination_root: Path,
    job_ids: tuple[str, ...],
) -> None:
    if not job_ids:
        raise NativeTrialError("Trial has no Runtime Job to snapshot")
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
            "INSERT INTO schema_migrations(version,name,checksum,applied_at_ms) "
            "VALUES(?,?,?,?)",
            [(version, f"migration-{version}", DIGEST_A, version) for version in range(1, 5)],
        )
        target.execute("PRAGMA foreign_keys=OFF")
        for job_id in job_ids:
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
                        f"INSERT INTO {table}({','.join(columns)}) "
                        f"VALUES({','.join('?' for _ in columns)})",
                        tuple(row[column] for column in columns),
                    )
        target.commit()
        target.execute("PRAGMA foreign_keys=ON")
        violations = target.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise NativeTrialError(
                f"Runtime Job snapshot violates foreign keys: {violations}"
            )
        count = int(target.execute("SELECT COUNT(*) FROM jobs").fetchone()[0])
        if count != len(job_ids):
            raise NativeTrialError(
                f"Runtime Job snapshot count differs: {count} != {len(job_ids)}"
            )
    finally:
        origin.close()
        target.close()
    os.chmod(destination, 0o600)


def runtime_export_module() -> Any:
    path = RUNTIME_ROOT / "scripts" / "observation_export.py"
    spec = importlib.util.spec_from_file_location("b5_runtime_exporter", path)
    if spec is None or spec.loader is None:
        raise NativeTrialError("Runtime exporter cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_bundle(path: str) -> ObservationExportBundle:
    return ObservationExportBundle.from_dict(
        json.loads(Path(path).read_text(encoding="utf-8"))
    )


def build_selection(
    ids: TrialIds,
    *,
    root: Path,
    host_root: Path,
    harness_root: Path,
    runtime_snapshot: Path,
) -> dict[str, Any]:
    sidecars = root / "observation-sidecars"
    outboxes = root / "observation-outboxes"
    host_result = export_host_observations(
        state_root=host_root,
        instance_id=ids.host_instance,
        checkpoint_path=sidecars / "host.json",
        outbox_root=outboxes / "host",
        owner_revision=HOST_REVISION,
        exporter_revision=HOST_EXPORTER_REVISION,
        exported_at_ms=8_000 + ids.number * 10,
        limit=2_000,
    )
    harness_result = export_harness_observations(
        state_root=harness_root,
        instance_id=ids.harness_instance,
        checkpoint_path=sidecars / "harness.json",
        outbox_root=outboxes / "harness",
        owner_revision=HARNESS_REVISION,
        exporter_revision=HARNESS_EXPORTER_REVISION,
        exported_at_ms=8_001 + ids.number * 10,
        limit=2_000,
    )
    runtime_result = runtime_export_module().export_runtime_observations(
        registry_root=runtime_snapshot,
        instance_id=ids.runtime_instance,
        checkpoint_path=sidecars / "runtime.json",
        outbox_root=outboxes / "runtime",
        owner_revision=RUNTIME_REVISION,
        exporter_revision=RUNTIME_EXPORTER_REVISION,
        exported_at_ms=8_002 + ids.number * 10,
        job_limit=20,
        event_limit_per_job=2_000,
    )
    results = (host_result, harness_result, runtime_result)
    if any(result["status"] != "exported" for result in results):
        raise NativeTrialError("one B5 owner exporter produced no Bundle")
    bundles = tuple(load_bundle(str(result["bundlePath"])) for result in results)
    producers = (
        ObservationProducerIdentity("ordivon-host", "host-journal", ids.host_instance),
        ObservationProducerIdentity(
            "ordivon-harness", "harness-journal", ids.harness_instance
        ),
        ObservationProducerIdentity(
            "ordivon-runtime", "runtime-registry", ids.runtime_instance
        ),
    )
    mappings = (
        ("ordivon-host", "host-journal", "host-observation-v1"),
        ("ordivon-harness", "harness-journal", "harness-observation-v1"),
        ("ordivon-runtime", "runtime-registry", "runtime-observation-v1"),
    )
    with SQLiteObservationGateway.initialize(
        root / "gateway",
        gateway_instance_id=f"observation-gateway:{ids.suffix}",
        producer_allowlist=producers,
        mapping_versions=mappings,
        created_at_ms=8_100 + ids.number * 10,
    ) as gateway:
        for offset, bundle in enumerate((bundles[2], bundles[0], bundles[1])):
            for batch in bundle.batches:
                gateway.ingest(batch, ingested_at_ms=8_200 + ids.number * 10 + offset)
        if not gateway.doctor(full=True)["healthy"]:
            raise NativeTrialError("B5 Observation Gateway Doctor failed")
        selection = select_cross_owner_trajectory(
            gateway,
            TrajectoryQuerySpec(
                query_id=f"trajectory-query:{ids.suffix}",
                anchor_kind="ordivon.host.task",
                anchor_id=ids.host_task_id,
                artifact_coverage="owner_native_only",
            ),
        )
    return selection.to_dict()


def usage_int(value: dict[str, Any], *keys: str) -> int:
    for key in keys:
        candidate = value.get(key)
        if isinstance(candidate, int) and candidate >= 0:
            return candidate
    return 0


def write_attempt_closeout(
    output: Path,
    *,
    ids: TrialIds,
    status: str,
    reason: str,
    computing_revision: str,
    workspace_closed: bool,
    job_count: int,
) -> None:
    output.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(output, 0o700)
    value = with_integrity(
        {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-native-trial-attempt-closeout",
            "trialId": ids.trial_id,
            "status": status,
            "reason": reason[:2_048],
            "computingRevision": computing_revision,
            "workspaceClosed": workspace_closed,
            "runtimeJobCount": job_count,
            "comparisonEligible": False,
            "b6Implemented": False,
        }
    )
    path = output / "attempt-closeout.json"
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.chmod(path, 0o600)


def run(args: argparse.Namespace) -> dict[str, Any]:
    ids = TrialIds.build(args.trial_number)
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise NativeTrialError("ORDIVON_BEARER_TOKEN is not set")
    computing_revision = git(COMPUTING_ROOT, "rev-parse", "HEAD")
    computing_dirty = bool(git(COMPUTING_ROOT, "status", "--porcelain"))
    if computing_dirty and not args.allow_dirty_computing:
        raise NativeTrialError("Computing repository must be clean")
    for repo, expected in (
        (HOST_ROOT, HOST_REVISION),
        (HARNESS_ROOT, HARNESS_REVISION),
        (RUNTIME_ROOT, RUNTIME_REVISION),
    ):
        if git(repo, "rev-parse", "HEAD") != expected:
            raise NativeTrialError(f"owner revision differs: {repo.name}")
        if git(repo, "status", "--porcelain"):
            raise NativeTrialError(f"owner repository is dirty: {repo.name}")
    settings = DeepSeekSettings.from_secret_file(
        args.deepseek_secret,
        timeout_seconds=90.0,
        max_response_bytes=4_194_304,
        max_output_tokens=8_192,
    )
    registry_root = args.runtime_registry_root
    if registry_root is None:
        configured = os.environ.get("ORDIVON_REGISTRY_ROOT")
        if not configured:
            raise NativeTrialError("Runtime Registry root is not configured")
        registry_root = Path(configured)
    output = args.output_root.expanduser().resolve()
    client = McpRuntimeClient(
        args.runtime_endpoint,
        token,
        client_name="ordivon-b5-native-trial",
        client_version="1.0.0",
    )
    client.initialize()
    runtime = RuntimeRecorder(client)
    temporary = Path(tempfile.mkdtemp(prefix=f"ordivon-{ids.suffix}-"))
    workspace_id: str | None = None
    workspace_closed = False
    trial: TrialRecordStore | None = None
    try:
        source_root = temporary / "source"
        extracted_revision = b4.extract_historical_fixture(source_root)
        protected_expected = {
            "SPEC.md": file_digest(source_root / "SPEC.md"),
            "test_allocation.py": file_digest(source_root / "test_allocation.py"),
        }
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
            raise NativeTrialError("Runtime workspace.open omitted identity")
        workspace_id = observed_workspace
        messages = initial_messages(ids, workspace_id)
        prompt_digest = canonical_digest(list(messages))
        context_digest = canonical_digest(
            {
                "taskId": TASK_ID,
                "taskVersion": TASK_VERSION,
                "sourceRevision": HISTORICAL_HOST_REVISION,
                "protectedFiles": protected_expected,
                "artifactCoverage": "owner_native_only",
            }
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
            "provider": "deepseek",
            "model": settings.model,
            "credentialScopeId": settings.credential_scope_id,
        }
        trial = TrialRecordStore.initialize(
            output,
            trial_id=ids.trial_id,
            configuration_id=CONFIGURATION_ID,
            task_ref={"taskId": TASK_ID, "taskVersion": TASK_VERSION},
            created_at_ms=int(time.time_ns() // 1_000_000),
        )
        trial.advance(
            expected_stage="planned",
            next_stage="prepared",
            updated_at_ms=int(time.time_ns() // 1_000_000),
        )
        snapshot = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-system-snapshot",
                "computingRevision": computing_revision,
                "hostRevision": HOST_REVISION,
                "harnessRevision": HARNESS_REVISION,
                "runtimeRevision": RUNTIME_REVISION,
                "protocolRevision": PROTOCOL_REVISION,
                "b4ImplementationRevision": B4_IMPLEMENTATION_REVISION,
                "b4ReceiptRevision": B4_RECEIPT_REVISION,
                "b4CloseoutDigest": B4_CLOSEOUT_DIGEST,
                "sharedObservationContractRevision": SHARED_CONTRACT_REVISION,
                "productionActivated": False,
            }
        )
        snapshot_digest = trial.write_record("system-snapshot.json", snapshot)
        manifest = system_manifest(
            settings=settings,
            computing_revision=computing_revision,
            environment_digest=canonical_digest(environment),
            prompt_digest=prompt_digest,
            context_digest=context_digest,
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
        host_clock = Clock(10_000 + ids.number * 1_000)
        harness_clock = Clock(20_000 + ids.number * 1_000)
        contract = build_contract(
            ids,
            settings=settings,
            manifest_digest=manifest_digest,
            prompt_digest=prompt_digest,
            context_digest=context_digest,
            created_at_ms=harness_clock(),
        )
        capture = ExecutionCapture()

        def resolve(request) -> HarnessRunContract:
            if request.request_id != ids.external_request_id:
                raise NativeTrialError("unexpected external request")
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
                DeepSeekTurnAdapter(settings),
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
            )
            return Driver(runner, capture, messages)

        adapter = OrdivonHarnessExternalExecutorAdapter(
            harness_root,
            contract_resolver=resolve,
            driver_factory=driver_factory,
            clock_ms=harness_clock,
        )
        with HostStorage(host_root) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=host_clock,
                owner_id=f"host:{ids.suffix}",
            )
            created = kernel.create_task(
                event_id=f"event:{ids.suffix}:task-created",
                kind=EventKind.TASK_CREATED,
                task_id=ids.host_task_id,
                goal_id=ids.host_goal_id,
                payload={"taskId": TASK_ID, "taskVersion": TASK_VERSION},
                frontier=(f"node:{ids.suffix}",),
            ).projection
            request = ExternalExecutionRequest(
                request_id=ids.external_request_id,
                adapter_id=adapter.adapter_id,
                task_id=ids.host_task_id,
                task_revision=created.revision,
                task_attempt_ref=ids.host_attempt_ref,
                contract_digest=contract.digest,
                correlation_context={"trialId": ids.trial_id},
                created_at_ms=host_clock(),
            )
            coordinator = ExternalExecutorCoordinator(HostExtensionPort(storage, kernel))
            coordinator.start(request, adapter)
            coordinator.collect_completion(ids.host_task_id, adapter)
        if capture.driver_creations != 1 or capture.loop_result is None:
            raise NativeTrialError("independent Harness execution identity differs")
        loop = capture.loop_result

        candidate_source = b4.read_workspace(client, workspace_id, "allocation.py")
        protected_observed = {
            "SPEC.md": text_digest(b4.read_workspace(client, workspace_id, "SPEC.md")),
            "test_allocation.py": text_digest(
                b4.read_workspace(client, workspace_id, "test_allocation.py")
            ),
        }
        completion_text: str | None
        try:
            completion_text = b4.read_workspace(
                client, workspace_id, "artifacts/completion.json"
            )
        except Exception:  # noqa: BLE001 - absence is a candidate result, not runner failure.
            completion_text = None
        evaluation = evaluate_candidate(
            temporary,
            candidate_source=candidate_source,
            completion_text=completion_text,
            protected_observed=protected_observed,
            protected_expected=protected_expected,
        )
        decision = host_finalize(
            ids,
            host_root=host_root,
            host_clock=host_clock,
            evaluation=evaluation,
        )
        with SQLiteHarnessStore(harness_root) as reopened_harness:
            harness_doctor = reopened_harness.doctor(full=True)
            harness_event_count = len(
                reopened_harness.list_run_events(ids.harness_run_id)
            )
        if not harness_doctor["healthy"]:
            raise NativeTrialError("Harness Doctor failed")

        job_ids = tuple(sorted(runtime.job_ids))
        runtime_snapshot = temporary / "runtime-snapshot"
        if job_ids:
            copy_runtime_jobs(registry_root, runtime_snapshot, job_ids)
        client.call_tool(
            "workspace.close",
            {"schemaVersion": 1, "workspaceId": workspace_id, "force": True},
        )
        workspace_closed = workspace_absent(client, workspace_id)
        if not workspace_closed:
            raise NativeTrialError("Runtime Workspace remained present after close")

        if not job_ids:
            write_attempt_closeout(
                output,
                ids=ids,
                status="invalid_incomplete",
                reason="No Runtime Job was linked to the Trial",
                computing_revision=computing_revision,
                workspace_closed=workspace_closed,
                job_count=0,
            )
            raise NativeTrialError("Trial is invalid: no Runtime Job")
        selection = build_selection(
            ids,
            root=temporary,
            host_root=host_root,
            harness_root=harness_root,
            runtime_snapshot=runtime_snapshot,
        )
        if selection["completeness"]["complete"] is not True:
            write_attempt_closeout(
                output,
                ids=ids,
                status="invalid_incomplete",
                reason="Observation Selection is incomplete",
                computing_revision=computing_revision,
                workspace_closed=workspace_closed,
                job_count=len(job_ids),
            )
            raise NativeTrialError("Trial is invalid: incomplete Selection")

        native_refs = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-native-refs",
                "trialId": ids.trial_id,
                "hostTaskId": ids.host_task_id,
                "hostTaskAttemptRef": ids.host_attempt_ref,
                "externalRequestId": ids.external_request_id,
                "harnessRunId": ids.harness_run_id,
                "runtimeWorkspaceId": workspace_id,
                "runtimeJobIds": list(job_ids),
                "completionArtifactRef": (
                    f"workspace-artifact:{workspace_id}:artifacts/completion.json"
                    if completion_text is not None
                    else None
                ),
                "decisionRef": decision["decisionRef"],
                "outcomeRef": decision["outcomeRef"],
            }
        )
        grader_bundle = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-grader-bundle",
                "trialId": ids.trial_id,
                "verifierId": "HARNESS-REPO-REPAIR-001-verifier",
                "verifierRevision": "1",
                "visible": {
                    "status": "passed" if evaluation.visible_passed else "failed",
                    "digest": evaluation.visible_digest,
                },
                "hidden": {
                    "status": "passed" if evaluation.hidden_passed else "failed",
                    "digest": evaluation.hidden_digest,
                },
                "protectedFilesUnchanged": evaluation.protected_files_unchanged,
                "completionArtifactValid": evaluation.completion_artifact_valid,
                "completionArtifactDigest": evaluation.completion_artifact_digest,
                "candidateSourceDigest": evaluation.candidate_source_digest,
                "failureCodes": list(evaluation.failure_codes),
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
            raise NativeTrialError("Trial intent omitted createdAtMs")
        completed_at_ms = int(time.time_ns() // 1_000_000)
        trial_value = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-trial",
                "trialId": ids.trial_id,
                "taskRef": {"taskId": TASK_ID, "taskVersion": TASK_VERSION},
                "executionPath": "ordivon_harness",
                "model": {
                    "providerId": "deepseek",
                    "modelId": settings.model,
                    "modelRevision": None,
                    "adapterRevision": HARNESS_REVISION,
                },
                "harness": {
                    "harnessId": "ordivon-harness",
                    "harnessRevision": HARNESS_REVISION,
                    "manifestDigest": manifest_digest,
                },
                "bindings": {
                    "sourceRevision": HISTORICAL_HOST_REVISION,
                    "environmentDigest": canonical_digest(environment),
                    "contextDigest": context_digest,
                    "toolCatalogDigest": INDEPENDENT_REPOSITORY_REPAIR_TOOL_SURFACE_DIGEST,
                    "systemSnapshotRef": "system-snapshot.json",
                    "systemManifestRef": {
                        "repositoryId": "ordivon-computing",
                        "path": "system-manifest.json",
                        "digest": manifest_digest,
                    },
                },
                "sampling": {
                    "seed": None,
                    "temperature": None,
                    "topP": None,
                    "reasoningEffort": "disabled",
                },
                "budget": budget_value,
                "startedAtMs": intent_created_at,
                "completedAtMs": completed_at_ms,
                "sourceEvidenceRefs": [
                    {
                        "repositoryId": "ordivon-computing",
                        "path": "observation-selection.json",
                        "digest": selection["integrity"]["payloadDigest"],
                    },
                    {
                        "repositoryId": "ordivon-computing",
                        "path": (
                            "research/experiments/harness-evaluation-v0/"
                            "evidence/b4-smoke-78de3a6/closeout.json"
                        ),
                        "digest": B4_CLOSEOUT_DIGEST,
                    },
                ],
                "limitations": [
                    "Provider sampling parameters are omitted by the adapter and use Provider defaults.",
                    "This Trial contributes to a three-run development baseline, not a model ranking.",
                    "Runtime Artifact traversal is owner-native only.",
                ],
            }
        )
        b4.validate_track_r_record(trial_value)
        trial.write_record("trial.json", trial_value, minimum_stage="evidence_collected")

        usage = dict(loop.usage)
        input_tokens = usage_int(
            usage, "prompt_tokens", "promptTokens", "input_tokens", "inputTokens"
        )
        output_tokens = usage_int(
            usage,
            "completion_tokens",
            "completionTokens",
            "output_tokens",
            "outputTokens",
        )
        cached_tokens = usage_int(
            usage,
            "prompt_cache_hit_tokens",
            "cachedInputTokens",
            "cacheHitTokens",
        )
        total_tokens = usage_int(usage, "total_tokens", "totalTokens")
        if total_tokens == 0:
            total_tokens = input_tokens + output_tokens
        repeated_commands = max(0, len(job_ids) - 1)
        invalid_calls = sum(
            event.kind.endswith("tool-rejected") for event in loop.trace.events
        )
        result = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-result",
                "trialId": ids.trial_id,
                "taskRef": {"taskId": TASK_ID, "taskVersion": TASK_VERSION},
                "stopCode": loop.stop_code.value,
                "acceptance": {
                    "status": "accepted" if evaluation.accepted else "rejected",
                    "decisionRef": decision["decisionRef"],
                    "falseCompletion": bool(
                        loop.candidate_completed and not evaluation.accepted
                    ),
                    "verifier": {
                        "verifierId": "HARNESS-REPO-REPAIR-001-verifier",
                        "verifierRevision": "1",
                        "status": "passed" if evaluation.accepted else "failed",
                        "assertions": [
                            {
                                "assertionId": "visible-tests-pass",
                                "status": (
                                    "passed" if evaluation.visible_passed else "failed"
                                ),
                                "evidenceRefs": [evaluation.visible_digest],
                            },
                            {
                                "assertionId": "hidden-tests-pass",
                                "status": (
                                    "passed" if evaluation.hidden_passed else "failed"
                                ),
                                "evidenceRefs": [evaluation.hidden_digest],
                            },
                            {
                                "assertionId": "protected-files-unchanged",
                                "status": (
                                    "passed"
                                    if evaluation.protected_files_unchanged
                                    else "failed"
                                ),
                                "evidenceRefs": list(protected_expected.values()),
                            },
                            {
                                "assertionId": "completion-artifact-valid",
                                "status": (
                                    "passed"
                                    if evaluation.completion_artifact_valid
                                    else "failed"
                                ),
                                "evidenceRefs": (
                                    [evaluation.completion_artifact_digest]
                                    if evaluation.completion_artifact_digest
                                    else [decision["decisionRef"]]
                                ),
                            },
                        ],
                    },
                },
                "metrics": {
                    "modelCalls": loop.model_calls,
                    "toolCalls": loop.tool_calls,
                    "runtimeJobs": len(job_ids),
                    "observationBytes": loop.observation_bytes,
                    "inputTokens": input_tokens,
                    "outputTokens": output_tokens,
                    "cachedInputTokens": cached_tokens,
                    "reasoningTokens": 0,
                    "totalTokens": total_tokens,
                    "wallTimeMs": max(0, completed_at_ms - intent_created_at),
                    "estimatedCostUsd": None,
                    "repeatedReads": max(
                        0, runtime.calls.count("workspace.read") - 4
                    ),
                    "repeatedCommands": repeated_commands,
                    "invalidToolCalls": invalid_calls,
                    "humanInterventionCount": 0,
                },
                "artifacts": [
                    {
                        "ref": f"artifact:{ids.suffix}:completion",
                        "kind": "completion-artifact",
                        "digest": (
                            evaluation.completion_artifact_digest
                            or evaluation.candidate_source_digest
                        ),
                        "valid": evaluation.completion_artifact_valid,
                    }
                ],
                "trace": {
                    "digest": loop.trace.digest,
                    "eventCount": len(loop.trace.events),
                    "ref": f"harness-trace:{ids.harness_run_id}",
                },
                "failureRefs": [],
                "limitations": [
                    "No raw Provider response or private reasoning is retained.",
                    "Estimated monetary cost is unavailable from the Provider response.",
                ],
            }
        )
        b4.validate_track_r_record(result)
        trial.write_record("result.json", result, minimum_stage="evidence_collected")
        review = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-review",
                "trialId": ids.trial_id,
                "verdict": "accepted" if evaluation.accepted else "rejected",
                "validity": "valid",
                "comparisonEligible": True,
                "failureAttribution": (
                    "none" if evaluation.accepted else "candidate"
                ),
                "failureCodes": list(evaluation.failure_codes),
                "rawReasoningReviewed": False,
                "operatorIntervention": False,
            }
        )
        trial.write_record("review.json", review, minimum_stage="evidence_collected")
        trial.advance(
            expected_stage="evidence_collected",
            next_stage="verified",
            updated_at_ms=int(time.time_ns() // 1_000_000),
            records=(
                "observation-selection.json",
                "trial.json",
                "result.json",
                "review.json",
            ),
        )
        disposition = TrialDisposition(
            trial_id=ids.trial_id,
            validity="valid",
            semantic_outcome=("accepted" if evaluation.accepted else "rejected"),
            comparative_outcome="not_applicable",
            failure_attribution=("none" if evaluation.accepted else "candidate"),
            comparison_eligible=True,
            reasons=(
                "three-owner evidence and independent verification completed",
                (
                    "candidate passed all assertions"
                    if evaluation.accepted
                    else "candidate failed one or more frozen assertions"
                ),
            ),
            selection_digest=selection["selectionDigest"],
        )
        trial.dispose(
            disposition,
            updated_at_ms=int(time.time_ns() // 1_000_000),
        )
        closeout = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-b5-native-trial-closeout",
                "trialId": ids.trial_id,
                "configurationId": CONFIGURATION_ID,
                "computingRevision": computing_revision,
                "computingClean": not computing_dirty,
                "credentialScopeId": settings.credential_scope_id,
                "modelId": settings.model,
                "validity": "valid",
                "semanticOutcome": (
                    "accepted" if evaluation.accepted else "rejected"
                ),
                "comparisonEligible": True,
                "selectionDigest": selection["selectionDigest"],
                "resultDigest": result["integrity"]["payloadDigest"],
                "dispositionDigest": disposition.to_dict()["integrity"][
                    "payloadDigest"
                ],
                "modelCalls": loop.model_calls,
                "toolCalls": loop.tool_calls,
                "runtimeJobCount": len(job_ids),
                "harnessEventCount": harness_event_count,
                "workspaceClosed": workspace_closed,
                "productionActivated": False,
                "b6Implemented": False,
            }
        )
        trial.write_record("closeout.json", closeout, minimum_stage="disposed")
        trial.advance(
            expected_stage="disposed",
            next_stage="closed",
            updated_at_ms=int(time.time_ns() // 1_000_000),
            records=("closeout.json",),
        )
        if not trial.doctor()["healthy"]:
            raise NativeTrialError("Formal Runner Doctor failed")
        return closeout
    except Exception as error:
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
                workspace_closed = workspace_absent(client, workspace_id)
            except Exception:  # noqa: BLE001 - retain original Trial failure.
                workspace_closed = False
        if trial is not None and not (output / "attempt-closeout.json").exists():
            write_attempt_closeout(
                output,
                ids=ids,
                status="invalid_or_failed",
                reason=f"{type(error).__name__}: {error}",
                computing_revision=computing_revision,
                workspace_closed=workspace_closed,
                job_count=len(runtime.job_ids),
            )
        raise
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def main() -> int:
    args = parse_args()
    try:
        closeout = run(args)
    except Exception as error:
        print(f"B5 native Trial: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(closeout, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
