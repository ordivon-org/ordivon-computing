#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from typing import Any

SCRIPT = Path(__file__).resolve()
OBSERVATION_ROOT = SCRIPT.parents[1]
COMPUTING_ROOT = SCRIPT.parents[4]
DEFAULT_HOST_ROOT = Path("/root/projects/ordivon-host")
DEFAULT_HARNESS_ROOT = Path("/root/projects/ordivon-harness")
DEFAULT_RUNTIME_ROOT = Path("/root/projects/ordivon-runtime")

for source in (
    OBSERVATION_ROOT / "implementation",
    COMPUTING_ROOT / "packages" / "ordivon-protocol" / "src",
    DEFAULT_HOST_ROOT / "src",
    DEFAULT_HARNESS_ROOT / "src",
):
    sys.path.insert(0, str(source))

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
from ordivon_harness.core_contracts import (  # noqa: E402
    HarnessBoundReference,
    HarnessRunContract,
)
from ordivon_harness.observation_export import export_harness_observations  # noqa: E402
from ordivon_harness.ordivon.continuity_records import (  # noqa: E402
    HarnessDispatchFenceV2,
)
from ordivon_harness.protocol import (  # noqa: E402
    HarnessToolStepReceipt,
    HarnessToolStepStatus,
)
from ordivon_harness.sqlite_store import SQLiteHarnessStore  # noqa: E402
from ordivon_observation_core import (  # noqa: E402
    ObservationExportBundle,
    ObservationProducerIdentity,
    ObservationSelectionManifest,
    SQLiteObservationGateway,
    TrajectoryQuerySpec,
    select_cross_owner_trajectory,
)

HOST_OWNER_REVISION = "a76a620160b28d870670696e04c39e539296fe00"
HOST_EXPORTER_REVISION = "e1c134f330a90c15495126a67021b06c56245156"
HARNESS_OWNER_REVISION = "e1f6596fa2694ec520d1d12eab8b18beeda39e50"
HARNESS_EXPORTER_REVISION = "e3cb34b4991b5f52e1c0ed0151ea17b067e88e16"
RUNTIME_OWNER_REVISION = "cff5bc583e878560c1e299e691e7e490ca279c9d"
RUNTIME_EXPORTER_REVISION = "8c22c2b409e99a0fd07fd72a9029ef8c74c6cb47"
SHARED_CONTRACT_REVISION = "b0973311d84b0debe30ca002e15e02401e16ee36"

TASK_ID = "task:b3-owner-native"
GOAL_ID = "goal:b3-owner-native"
TASK_ATTEMPT_REF = "task-attempt:b3-owner-native"
EXTERNAL_REQUEST_ID = "external-request:b3-owner-native"
HARNESS_RUN_ID = "harness-run:b3-owner-native"
RUNTIME_CLIENT_REQUEST_ID = "request:b3-owner-native"
RUNTIME_JOB_ID = "job-019fd000-0000-7000-8000-00000000b305"
RUNTIME_ATTEMPT_ID = "attempt-019fd000-0000-7000-8000-00000000b305"
RUNTIME_WORKSPACE_ID = "workspace:b3-owner-native"
COMPLETION_PROPOSAL_ID = "completion-proposal:b3-owner-native"
CONTRACT_DIGEST = "sha256:" + "a" * 64
DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
DIGEST_C = "sha256:" + "c" * 64
DIGEST_D = "sha256:" + "d" * 64

HOST_INSTANCE = "host:b3-owner-native"
HARNESS_INSTANCE = "harness:b3-owner-native"
RUNTIME_INSTANCE = "runtime:b3-owner-native"


class AcceptanceError(RuntimeError):
    pass


class _ExternalAdapter:
    adapter_id = "external-executor:b3-owner-native"

    def __init__(self) -> None:
        self.proposal = ExternalCompletionProposal(
            proposal_id=COMPLETION_PROPOSAL_ID,
            foreign_run_ref=HARNESS_RUN_ID,
            contract_digest=CONTRACT_DIGEST,
            summary="Private candidate summary retained only by Host.",
            evidence_refs=("evidence:b3-owner-native",),
            artifact_refs=("runtime-artifact:b3-owner-native",),
            created_at_ms=1_030,
            metadata={"private": "must not enter Observation"},
        )

    def start(self, request: ExternalExecutionRequest) -> ExternalRunObservation:
        return ExternalRunObservation(
            foreign_run_ref=HARNESS_RUN_ID,
            status=ExternalRunStatus.RUNNING,
            revision=1,
            evidence_refs=("evidence:b3-owner-native",),
            observed_at_ms=request.created_at_ms + 1,
            metadata={"private": "must not enter Observation"},
        )

    def observe(self, foreign_run_ref: str) -> ExternalRunObservation:
        if foreign_run_ref != HARNESS_RUN_ID:
            raise AcceptanceError("unexpected foreign Run")
        return ExternalRunObservation(
            foreign_run_ref=HARNESS_RUN_ID,
            status=ExternalRunStatus.COMPLETED,
            revision=2,
            evidence_refs=("evidence:b3-owner-native",),
            observed_at_ms=1_025,
            metadata={},
        )

    def cancel(self, foreign_run_ref: str, request_id: str) -> ExternalRunObservation:
        raise AcceptanceError(f"unexpected cancellation: {foreign_run_ref} {request_id}")

    def recover(
        self,
        request: ExternalExecutionRequest,
        foreign_run_ref: str | None,
    ) -> ExternalRunObservation:
        return self.start(request)

    def collect_completion(
        self, foreign_run_ref: str
    ) -> ExternalCompletionProposal | None:
        if foreign_run_ref != HARNESS_RUN_ID:
            raise AcceptanceError("unexpected completion Run")
        return self.proposal


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run B3 against real Host, Harness and Runtime owner stores"
    )
    parser.add_argument("--host-repo", type=Path, default=DEFAULT_HOST_ROOT)
    parser.add_argument("--harness-repo", type=Path, default=DEFAULT_HARNESS_ROOT)
    parser.add_argument("--runtime-repo", type=Path, default=DEFAULT_RUNTIME_ROOT)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--keep-owner-state", action="store_true")
    parser.add_argument("--allow-dirty-computing", action="store_true")
    return parser.parse_args()


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _verify_repo(repo: Path, expected_revision: str, *, allow_dirty: bool = False) -> None:
    revision = _git(repo, "rev-parse", "HEAD")
    if revision != expected_revision:
        raise AcceptanceError(
            f"{repo.name} revision differs: expected {expected_revision}, observed {revision}"
        )
    dirty = _git(repo, "status", "--porcelain")
    if dirty and not allow_dirty:
        raise AcceptanceError(f"{repo.name} is dirty")


def _runtime_export_module(runtime_repo: Path) -> Any:
    path = runtime_repo / "scripts" / "observation_export.py"
    spec = importlib.util.spec_from_file_location("b3_runtime_observation_export", path)
    if spec is None or spec.loader is None:
        raise AcceptanceError(f"cannot load Runtime exporter: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _durable_snapshot(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if (
            path.is_file()
            and not path.is_symlink()
            and not path.name.endswith(("-wal", "-shm"))
        ):
            result[str(path.relative_to(root))] = (
                "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            )
    return result


def _build_host(root: Path) -> None:
    clock = itertools.count(1_000).__next__
    with HostStorage(root) as storage:
        kernel = HostKernel(
            storage,
            clock_ms=clock,
            owner_id="host:b3-owner-native",
        )
        created = kernel.create_task(
            event_id="event:b3-owner-native:task-created",
            kind=EventKind.TASK_CREATED,
            task_id=TASK_ID,
            goal_id=GOAL_ID,
            payload={"private": "Host Task payload must not enter Observation"},
            frontier=("node:b3-owner-native",),
        )
        adapter = _ExternalAdapter()
        coordinator = ExternalExecutorCoordinator(HostExtensionPort(storage, kernel))
        request = ExternalExecutionRequest(
            request_id=EXTERNAL_REQUEST_ID,
            adapter_id=adapter.adapter_id,
            task_id=TASK_ID,
            task_revision=created.projection.revision,
            task_attempt_ref=TASK_ATTEMPT_REF,
            contract_digest=CONTRACT_DIGEST,
            correlation_context={"private": "correlation content"},
            created_at_ms=1_010,
        )
        coordinator.start(request, adapter)
        collected = coordinator.collect_completion(TASK_ID, adapter)
        retained = tuple(
            value
            for value in (
                collected.request_object,
                collected.binding_object,
                collected.completion_proposal_object,
            )
            if value is not None
        )
        current_data = storage.read_task_event(TASK_ID).data
        if not isinstance(current_data, dict):
            raise AcceptanceError("Host current Task data is not an object")
        with kernel.locked_task(
            TASK_ID,
            expected_revision=collected.projection.revision,
        ) as locked:
            verification = locked.commit(
                event_id="event:b3-owner-native:verification",
                kind=EventKind.VERIFICATION_RECORDED,
                payload={**current_data, "verificationStatus": "passed"},
                referenced_objects=retained,
            )
        with kernel.locked_task(
            TASK_ID,
            expected_revision=verification.projection.revision,
        ) as locked:
            locked.commit(
                event_id="event:b3-owner-native:outcome",
                kind=EventKind.TASK_OUTCOME_RECORDED,
                payload={**current_data, "taskOutcome": "accepted"},
                state=TaskState.COMPLETED,
                frontier=(),
                referenced_objects=retained,
            )


def _bound_ref(ref: str, kind: str, digest_value: str) -> HarnessBoundReference:
    return HarnessBoundReference(ref, kind, digest_value)


def _build_harness(root: Path) -> None:
    contract = HarnessRunContract(
        harness_run_id=HARNESS_RUN_ID,
        harness_implementation_id="ordivon-harness@b3-owner-native",
        caller_id="caller:ordivon-host",
        caller_run_ref=EXTERNAL_REQUEST_ID,
        objective_ref=_bound_ref("objective:b3-owner-native", "objective", DIGEST_A),
        context_refs=(
            _bound_ref("context:b3-owner-native", "context", DIGEST_B),
        ),
        provider_id="provider:scripted",
        adapter_id="adapter:scripted-v1",
        requested_model_id="model:scripted",
        tool_catalog_digest=DIGEST_C,
        tool_grant_digest=DIGEST_D,
        budget={"private": "Harness budget must not enter Observation"},
        completion_contract={
            "private": "Harness completion contract must not enter Observation"
        },
        system_manifest_ref=_bound_ref(
            "system-manifest:b3-owner-native", "system-manifest", DIGEST_A
        ),
        created_at_ms=2_000,
    )
    with SQLiteHarnessStore.initialize(root) as store:
        store.create_run(contract)
        receipt = HarnessToolStepReceipt(
            receipt_id="harness-tool-step-receipt:b3-owner-native",
            intent_digest=DIGEST_A,
            harness_run_id=HARNESS_RUN_ID,
            tool_call_id="tool-call:b3-owner-native",
            status=HarnessToolStepStatus.UNKNOWN,
            runtime_job_ref=RUNTIME_JOB_ID,
            observation_digest=DIGEST_C,
            reconciled=False,
            created_at_ms=2_010,
        )
        fence = HarnessDispatchFenceV2(
            fence_id="harness-dispatch-fence:b3-owner-native",
            harness_run_id=HARNESS_RUN_ID,
            run_revision=1,
            binding_digest=contract.digest,
            intent_digest=DIGEST_A,
            runtime_operation="workspace.exec",
            client_request_id=RUNTIME_CLIENT_REQUEST_ID,
            issued_at_ms=2_005,
            expires_at_ms=3_005,
        )
        receipt_object = store.put_object(
            receipt.to_dict(), kind="harness-tool-step-receipt"
        )
        fence_object = store.put_object(
            fence.to_dict(), kind="harness-dispatch-fence"
        )
        lease = store.acquire_run_lease(
            HARNESS_RUN_ID,
            owner_id="worker:b3-owner-native:tool",
            ttl_ms=1_000,
            now_ms=2_005,
        )
        store.append_event(
            event_id="event:b3-owner-native:harness-tool-step",
            harness_run_id=HARNESS_RUN_ID,
            event_kind="harness.tool-step-recorded",
            data={"private": "Harness Tool payload must not enter Observation"},
            expected_revision=1,
            recorded_at_ms=2_010,
            lease=lease,
            lease_checked_at_ms=2_010,
            referenced_objects=(fence_object, receipt_object),
        )
        lease = store.acquire_run_lease(
            HARNESS_RUN_ID,
            owner_id="worker:b3-owner-native:completion",
            ttl_ms=1_000,
            now_ms=2_011,
        )
        store.append_event(
            event_id="event:b3-owner-native:harness-completion",
            harness_run_id=HARNESS_RUN_ID,
            event_kind="harness.completion-proposed",
            data={
                "completionProposalId": COMPLETION_PROPOSAL_ID,
                "private": "Harness completion payload must not enter Observation",
            },
            expected_revision=2,
            recorded_at_ms=2_012,
            lease=lease,
            lease_checked_at_ms=2_012,
        )


def _build_runtime(root: Path, runtime_repo: Path) -> None:
    root.mkdir(mode=0o700)
    database = root / "registry.sqlite3"
    connection = sqlite3.connect(database)
    try:
        connection.execute("PRAGMA foreign_keys=ON")
        migrations = (
            runtime_repo
            / "crates"
            / "ordivon-runtime-core"
            / "migrations"
            / "runtime"
        )
        for path in sorted(migrations.glob("*.sql")):
            connection.executescript(path.read_text(encoding="utf-8"))
        connection.executemany(
            "INSERT INTO schema_migrations(version,name,checksum,applied_at_ms) "
            "VALUES(?,?,?,?)",
            [
                (version, f"migration-{version}", DIGEST_A, version)
                for version in range(1, 5)
            ],
        )
        connection.execute(
            "INSERT INTO jobs(job_id,principal,client_request_id,request_digest,"
            "operation_digest,workspace_id,workspace_snapshot_json,execution_plan_json,"
            "execution_plan_digest,created_at_ms,desired_state,resolution,current_attempt_id,"
            "row_version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                RUNTIME_JOB_ID,
                "principal:b3-owner-native",
                RUNTIME_CLIENT_REQUEST_ID,
                DIGEST_A,
                DIGEST_B,
                RUNTIME_WORKSPACE_ID,
                '{"private":"Runtime Workspace snapshot must not enter Observation"}',
                '{"command":"Runtime command must not enter Observation"}',
                DIGEST_C,
                3_000,
                "run",
                None,
                None,
                0,
            ),
        )
        connection.execute(
            "INSERT INTO attempts(attempt_id,job_id,attempt_number,state,termination_intent,"
            "launch_token_digest,bundle_path,bundle_digest,boot_id,unit_name,invocation_id,"
            "control_group,main_pid,process_start_identity,runner_start_digest,result_digest,"
            "exit_code,infrastructure_error_digest,created_at_ms,started_at_ms,finished_at_ms,"
            "row_version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                RUNTIME_ATTEMPT_ID,
                RUNTIME_JOB_ID,
                1,
                "succeeded",
                "natural",
                DIGEST_A,
                "/private/runtime-bundle",
                DIGEST_B,
                None,
                "ordivon-b3-owner-native.service",
                None,
                None,
                None,
                None,
                None,
                DIGEST_C,
                0,
                None,
                3_000,
                3_001,
                3_003,
                0,
            ),
        )
        connection.execute(
            "UPDATE jobs SET current_attempt_id=?, resolution=?, row_version=1 "
            "WHERE job_id=?",
            (RUNTIME_ATTEMPT_ID, "succeeded", RUNTIME_JOB_ID),
        )
        events = (
            (
                "event:b3-owner-native:runtime-1",
                RUNTIME_JOB_ID,
                RUNTIME_ATTEMPT_ID,
                1,
                "JOB_ACCEPTED",
                "SYSTEM_DERIVED",
                None,
                "accepted",
                "REQUEST_ADMITTED",
                '{"private":"Runtime detail one"}',
                DIGEST_A,
                3_000,
            ),
            (
                "event:b3-owner-native:runtime-2",
                RUNTIME_JOB_ID,
                RUNTIME_ATTEMPT_ID,
                2,
                "ATTEMPT_RUNNING",
                "SYSTEM_OBSERVED",
                "accepted",
                "running",
                "RUNNER_OBSERVED",
                '{"stdout":"Runtime output must not enter Observation"}',
                DIGEST_B,
                3_001,
            ),
            (
                "event:b3-owner-native:runtime-3",
                RUNTIME_JOB_ID,
                RUNTIME_ATTEMPT_ID,
                3,
                "ATTEMPT_SUCCEEDED",
                "SYSTEM_OBSERVED",
                "running",
                "succeeded",
                "TERMINAL_EVIDENCE_ACCEPTED",
                '{"environment":"Runtime environment must not enter Observation"}',
                DIGEST_C,
                3_003,
            ),
        )
        connection.executemany(
            "INSERT INTO job_events(event_id,job_id,attempt_id,event_sequence,event_type,"
            "origin,previous_state,new_state,reason_code,detail_json,detail_digest,"
            "observed_at_ms) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            events,
        )
        connection.commit()
    finally:
        connection.close()
    os.chmod(database, 0o600)


def _load_bundle(path: str) -> ObservationExportBundle:
    return ObservationExportBundle.from_dict(
        json.loads(Path(path).read_text(encoding="utf-8"))
    )


def _export_all(root: Path, runtime_repo: Path) -> dict[str, ObservationExportBundle]:
    host_result = export_host_observations(
        state_root=root / "owners" / "host",
        instance_id=HOST_INSTANCE,
        checkpoint_path=root / "sidecars" / "host.json",
        outbox_root=root / "outboxes" / "host",
        owner_revision=HOST_OWNER_REVISION,
        exporter_revision=HOST_EXPORTER_REVISION,
        exported_at_ms=4_000,
        limit=256,
    )
    harness_result = export_harness_observations(
        state_root=root / "owners" / "harness",
        instance_id=HARNESS_INSTANCE,
        checkpoint_path=root / "sidecars" / "harness.json",
        outbox_root=root / "outboxes" / "harness",
        owner_revision=HARNESS_OWNER_REVISION,
        exporter_revision=HARNESS_EXPORTER_REVISION,
        exported_at_ms=4_001,
        limit=256,
    )
    runtime_export = _runtime_export_module(runtime_repo)
    runtime_result = runtime_export.export_runtime_observations(
        registry_root=root / "owners" / "runtime",
        instance_id=RUNTIME_INSTANCE,
        checkpoint_path=root / "sidecars" / "runtime.json",
        outbox_root=root / "outboxes" / "runtime",
        owner_revision=RUNTIME_OWNER_REVISION,
        exporter_revision=RUNTIME_EXPORTER_REVISION,
        exported_at_ms=4_002,
        job_limit=100,
        event_limit_per_job=256,
    )
    results = {
        "host": host_result,
        "harness": harness_result,
        "runtime": runtime_result,
    }
    for owner, result in results.items():
        if result["status"] != "exported" or not isinstance(
            result["bundlePath"], str
        ):
            raise AcceptanceError(f"{owner} exporter did not create a Bundle")
    return {
        owner: _load_bundle(str(result["bundlePath"]))
        for owner, result in results.items()
    }


def _producers() -> tuple[ObservationProducerIdentity, ...]:
    return (
        ObservationProducerIdentity("ordivon-host", "host-journal", HOST_INSTANCE),
        ObservationProducerIdentity(
            "ordivon-harness", "harness-journal", HARNESS_INSTANCE
        ),
        ObservationProducerIdentity(
            "ordivon-runtime", "runtime-registry", RUNTIME_INSTANCE
        ),
    )


def _mappings() -> tuple[tuple[str, str, str], ...]:
    return (
        ("ordivon-host", "host-journal", "host-observation-v1"),
        ("ordivon-harness", "harness-journal", "harness-observation-v1"),
        ("ordivon-runtime", "runtime-registry", "runtime-observation-v1"),
    )


def _build_selection(
    root: Path,
    bundles: dict[str, ObservationExportBundle],
    order: tuple[str, ...],
    *,
    include_runtime: bool = True,
) -> ObservationSelectionManifest:
    selected_order = tuple(
        owner for owner in order if include_runtime or owner != "runtime"
    )
    with SQLiteObservationGateway.initialize(
        root,
        gateway_instance_id=f"observation-gateway:b3:{'-'.join(selected_order)}",
        producer_allowlist=_producers(),
        mapping_versions=_mappings(),
        created_at_ms=5_000,
    ) as gateway:
        ingested_at = 5_100
        for owner in selected_order:
            for batch in bundles[owner].batches:
                gateway.ingest(batch, ingested_at_ms=ingested_at)
                ingested_at += 1
        if not gateway.doctor(full=True)["healthy"]:
            raise AcceptanceError("Observation Gateway full Doctor failed")
        return select_cross_owner_trajectory(
            gateway,
            TrajectoryQuerySpec(
                query_id="trajectory-query:b3-owner-native",
                anchor_kind="ordivon.host.task",
                anchor_id=TASK_ID,
                artifact_coverage="owner_native_only",
            ),
        )


def _with_integrity(value: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return {
        **value,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": "sha256:" + hashlib.sha256(payload).hexdigest(),
        },
    }


def main() -> int:
    args = _parse_args()
    _verify_repo(
        COMPUTING_ROOT,
        _git(COMPUTING_ROOT, "rev-parse", "HEAD"),
        allow_dirty=args.allow_dirty_computing,
    )
    _verify_repo(args.host_repo, HOST_OWNER_REVISION)
    _verify_repo(args.harness_repo, HARNESS_OWNER_REVISION)
    _verify_repo(args.runtime_repo, RUNTIME_OWNER_REVISION)
    computing_revision = _git(COMPUTING_ROOT, "rev-parse", "HEAD")
    computing_clean = not bool(_git(COMPUTING_ROOT, "status", "--porcelain"))

    temporary = tempfile.mkdtemp(prefix="ordivon-b3-owner-native-")
    root = Path(temporary)
    output_root = args.output_root.resolve() if args.output_root else None
    try:
        owner_root = root / "owners"
        owner_root.mkdir(mode=0o700)
        _build_host(owner_root / "host")
        _build_harness(owner_root / "harness")
        _build_runtime(owner_root / "runtime", args.runtime_repo)
        before = {
            owner: _durable_snapshot(owner_root / owner)
            for owner in ("host", "harness", "runtime")
        }
        bundles = _export_all(root, args.runtime_repo)
        after = {
            owner: _durable_snapshot(owner_root / owner)
            for owner in ("host", "harness", "runtime")
        }
        first = _build_selection(
            root / "gateway-a", bundles, ("host", "harness", "runtime")
        )
        second = _build_selection(
            root / "gateway-b", bundles, ("runtime", "host", "harness")
        )
        incomplete = _build_selection(
            root / "gateway-incomplete",
            bundles,
            ("host", "harness", "runtime"),
            include_runtime=False,
        )
        checks = {
            "threeOwnerSelectionComplete": first.completeness["complete"] is True,
            "trialValidityNotInferred": first.completeness["trialValidityInferred"]
            is False,
            "ownerDurableBytesUnchanged": before == after,
            "catalogDigestStableAcrossIngestOrder": first.catalog_digest
            == second.catalog_digest,
            "selectionDigestStableAcrossIngestOrder": first.selection_digest
            == second.selection_digest,
            "selectedEventsStableAcrossIngestOrder": first.selected_events
            == second.selected_events,
            "missingRuntimeIsIncomplete": incomplete.completeness["complete"]
            is False,
            "metadataOnly": first.privacy["metadataOnly"] is True,
            "payloadBytesNotCopied": first.privacy["payloadBytesCopied"] is False,
            "artifactCoverageOwnerNativeOnly": first.query.artifact_coverage
            == "owner_native_only",
            "productionRootsUntouched": all(
                not path.exists()
                for path in (
                    Path("/var/lib/ordivon/host"),
                    Path("/var/lib/ordivon/harness"),
                    Path("/var/lib/ordivon/observation"),
                )
            ),
        }
        if not all(checks.values()):
            raise AcceptanceError(f"B3 owner-native checks failed: {checks}")
        selection_value = first.to_dict()
        receipt = _with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.observation-b3-owner-native-acceptance",
                "workPackage": "B3",
                "computingRevision": computing_revision,
                "computingClean": computing_clean,
                "sharedContractRevision": SHARED_CONTRACT_REVISION,
                "owners": {
                    "host": {
                        "ownerRevision": HOST_OWNER_REVISION,
                        "exporterRevision": HOST_EXPORTER_REVISION,
                        "bundleDigest": bundles["host"].integrity_digest,
                    },
                    "harness": {
                        "ownerRevision": HARNESS_OWNER_REVISION,
                        "exporterRevision": HARNESS_EXPORTER_REVISION,
                        "bundleDigest": bundles["harness"].integrity_digest,
                    },
                    "runtime": {
                        "ownerRevision": RUNTIME_OWNER_REVISION,
                        "exporterRevision": RUNTIME_EXPORTER_REVISION,
                        "bundleDigest": bundles["runtime"].integrity_digest,
                    },
                },
                "query": first.query.to_dict(),
                "catalogDigest": first.catalog_digest,
                "selectionDigest": first.selection_digest,
                "selectionIntegrityDigest": first.integrity_digest,
                "selectedEventCount": len(first.selected_events),
                "sourceStreamCount": len(first.source_stream_heads),
                "checks": checks,
                "formalTrialUnlocked": computing_clean,
                "productionActivated": False,
                "ownerStateRetained": args.keep_owner_state,
                "knownLimits": [
                    "Runtime Artifact traversal remains owner-native only",
                    "B3 proves evidence completeness, not Trial validity or Candidate quality",
                    "The acceptance trajectory is deterministic and uses a private disposable Runtime Registry",
                ],
            }
        )
        if output_root is not None:
            output_root.mkdir(parents=True, exist_ok=True)
            os.chmod(output_root, 0o700)
            selection_path = output_root / "observation-selection.json"
            receipt_path = output_root / "receipt.json"
            selection_path.write_text(
                json.dumps(selection_value, indent=2, ensure_ascii=False, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
            receipt_path.write_text(
                json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
            os.chmod(selection_path, 0o600)
            os.chmod(receipt_path, 0o600)
        print(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    finally:
        if args.keep_owner_state:
            print(f"retained owner-native state: {root}", file=sys.stderr)
        else:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
