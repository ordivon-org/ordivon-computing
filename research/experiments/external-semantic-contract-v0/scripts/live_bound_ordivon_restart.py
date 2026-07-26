#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from live_bound_support import LiveBindingContext

from anc_effect_binding import lower_to_ordivon
from anc_effect_ir import (
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
)
from integration import BoundExecutionView, admit_bound_effect, discover_ordivon_contracts
from anc_semantic_core.bootstrap import authorized_journal_views
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.ordivon import OrdivonExecution, OrdivonSemanticAdapter, ordivon_workspace_object_id
from anc_semantic_core.state import EffectState
from anc_semantic_core.transport import ToolTransportError
from live_support import LocalMcpToolCaller


class DropFirstSuccessfulResponse:
    def __init__(self, underlying: LocalMcpToolCaller, tool_name: str) -> None:
        self.underlying = underlying
        self.tool_name = tool_name
        self.dropped = False

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        result = self.underlying.call_tool(name, arguments)
        if name == self.tool_name and not self.dropped:
            self.dropped = True
            raise ToolTransportError(
                f"injected response loss after successful {name} delivery"
            )
        return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prove a signed external Binding survives real Ordivon response loss and process restart"
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument("--source-repo", default="/root/projects/agent-native-computing")
    parser.add_argument("--source-revision")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--journal")
    parser.add_argument("--binding-store")
    parser.add_argument("--effect-id-value")
    return parser.parse_args()


def kernel_secret(*, create: bool) -> bytes:
    encoded = os.environ.get("ANC_AUTHORITY_SECRET_HEX")
    if encoded:
        try:
            secret = bytes.fromhex(encoded)
        except ValueError as error:
            raise SystemExit("ANC_AUTHORITY_SECRET_HEX must contain hexadecimal bytes") from error
        if len(secret) < 32:
            raise SystemExit("ANC_AUTHORITY_SECRET_HEX must contain at least 32 bytes")
        return secret
    if create:
        return secrets.token_bytes(32)
    raise SystemExit("ANC_AUTHORITY_SECRET_HEX is required to resume the signed Journal")


def launch_envelope(stamp: int, workspace_id: str, execution: OrdivonExecution) -> EffectEnvelope:
    action = "anc.execution.launch.v1"
    target = TargetRef(f"world_object:execution-scope:{workspace_id}")
    return EffectEnvelope(
        effect_id=f"effect:live-bound-restart:{stamp}",
        target=target,
        mode=EffectMode.CHANGE,
        action=SemanticAction(action, "anc.execution-input.v1"),
        input=CanonicalInput(
            {
                "executable": execution.executable,
                "args": list(execution.args),
                "cwdRelative": execution.cwd_relative,
                "env": dict(execution.env),
                "timeoutMs": execution.timeout_ms,
                "stdoutLimitBytes": execution.stdout_limit_bytes,
                "stderrLimitBytes": execution.stderr_limit_bytes,
                "waitMs": 0,
                "stdoutTailBytes": 4_096,
                "stderrTailBytes": 4_096,
            }
        ),
        capability=CapabilityRequirement(
            "principal:ordivon-live-agent", action, target.object_id
        ),
        delivery=DeliverySemantics(IdempotencyKind.NONE),
        result=ResultSemantics(
            ExecutionKind.ASYNCHRONOUS,
            CompletionKind.TERMINAL_OBSERVATION,
        ),
        verification=VerificationPlan(
            "terminal-job-observation.v1",
            (EvidenceKind.OBSERVATION, EvidenceKind.ARTIFACT),
        ),
    )


def resume(args: argparse.Namespace, token: str) -> None:
    if not args.journal or not args.binding_store or not args.effect_id_value:
        raise SystemExit(
            "--resume requires --journal, --binding-store, and --effect-id-value"
        )
    views = authorized_journal_views(
        args.journal,
        kernel_secret(create=False),
        namespace="live-bound-journal-restart",
        trust_domain="ordivon-live",
    )
    context = LiveBindingContext.open(args.binding_store, create_secrets=False)
    try:
        effect_id = SemanticId(IdKind.EFFECT, args.effect_id_value)
        admission = views.read.current_binding_for(effect_id)
        if admission is None:
            raise AssertionError("restarted Kernel has no current Binding admission")
        complete = context.service.resolve(admission).binding
        adapter = OrdivonSemanticAdapter(
            BoundExecutionView(views.execution, admission, complete),
            LocalMcpToolCaller(args.endpoint, token),
        )
        projection = None
        for _ in range(5):
            projection = adapter.reconcile(effect_id, wait_ms=10_000)
            if projection.state.terminal:
                break
        if projection is None or projection.state is not EffectState.SUCCEEDED:
            raise AssertionError(
                f"process restart did not recover success: {getattr(projection, 'state', None)}"
            )
        if projection.binding is None:
            raise AssertionError("process restart produced no Ordivon Job binding")
        dispatch = views.read.get_dispatch(projection.binding.dispatch_id)
        if dispatch.binding_id != admission.binding_id:
            raise AssertionError("process restart changed the external Binding identity")
        if dispatch.binding_digest != admission.binding_digest:
            raise AssertionError("process restart changed the external Binding digest")
        views.read.verify_from_genesis()
        print(
            json.dumps(
                {
                    "terminalState": projection.state.value,
                    "dispatchId": str(projection.binding.dispatch_id),
                    "bindingId": str(admission.binding_id),
                    "bindingDigest": admission.binding_digest,
                    "jobId": projection.binding.job_id,
                    "attemptId": projection.binding.attempt_id,
                    "semanticArtifactCount": len(projection.artifacts),
                    "journalEntryCount": views.read.journal_entry_count,
                },
                sort_keys=True,
            )
        )
    finally:
        views.read.close()


def main() -> None:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")
    if args.resume:
        resume(args, token)
        return
    if not args.source_revision:
        raise SystemExit("--source-revision is required")

    real_client = LocalMcpToolCaller(args.endpoint, token)
    real_client.initialize()
    contracts = discover_ordivon_contracts(real_client)
    lossy_client = DropFirstSuccessfulResponse(real_client, "workspace.exec")
    stamp = int(time.time() * 1_000)
    workspace_id = f"anc-live-bound-restart-{stamp}"
    journal_path = Path(f"/tmp/anc-bound-journal-{stamp}.sqlite3")
    binding_store_path = Path(f"/tmp/anc-bound-bindings-{stamp}")
    opened = False
    views = None
    kernel_key = kernel_secret(create=True)
    context = LiveBindingContext.open(binding_store_path, create_secrets=True)
    try:
        opened_payload = real_client.call_tool(
            "workspace.open",
            {
                "schemaVersion": 1,
                "sourceRepo": args.source_repo,
                "sourceRevision": args.source_revision,
                "workspaceId": workspace_id,
            },
        )
        opened = True
        resolved_revision = opened_payload["sourceRevision"]
        execution = OrdivonExecution(
            workspace_id=workspace_id,
            executable="/usr/bin/bash",
            args=(
                "-lc",
                "printf 'bound-restart-start\\n'; sleep 1; printf 'bound-restart-done\\n'",
            ),
            timeout_ms=20_000,
        )
        envelope = launch_envelope(stamp, workspace_id, execution)
        signed_effect = context.sign(envelope, issued_at_ms=stamp)
        binding = lower_to_ordivon(
            envelope,
            contracts["workspace.exec"],
            binding_id=f"binding:live-bound-restart:{stamp}:r1",
            workspace_id=workspace_id,
        )
        clock = iter(range(stamp, stamp + 1_000_000)).__next__
        views = authorized_journal_views(
            journal_path,
            kernel_key,
            namespace="live-bound-journal-restart",
            trust_domain="ordivon-live",
        )
        projection, admission = admit_bound_effect(
            views,
            signed_effect,
            contracts["workspace.exec"],
            binding,
            context.service,
            backend_target=ordivon_workspace_object_id(workspace_id),
            event_namespace=f"live-bound-restart:{stamp}",
            admitted_at_ms=clock(),
        )
        complete = context.service.resolve(admission).binding
        adapter = OrdivonSemanticAdapter(
            BoundExecutionView(views.execution, admission, complete),
            lossy_client,
            clock_ms=clock,
        )
        first = adapter.dispatch_exec(projection.effect_id, execution, wait_ms=0)
        if first.state is not EffectState.UNKNOWN:
            raise AssertionError(f"response loss did not produce UNKNOWN: {first.state}")
        dispatch_id = views.read.get_effect(projection.effect_id).dispatch_id
        if dispatch_id is None:
            raise AssertionError("UNKNOWN Effect lost Dispatch identity")
        dispatch = views.read.get_dispatch(dispatch_id)
        if dispatch.binding_id != admission.binding_id:
            raise AssertionError("bound Dispatch omitted the admitted Binding")
        if dispatch.binding_digest != admission.binding_digest:
            raise AssertionError("bound Dispatch recorded the wrong Binding digest")
        client_request_id = next(
            arguments["clientRequestId"]
            for name, arguments in real_client.calls
            if name == "workspace.exec"
        )
        before_restart_entries = views.read.journal_entry_count
        views.read.close()
        views = None

        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--resume",
                "--endpoint",
                args.endpoint,
                "--journal",
                str(journal_path),
                "--binding-store",
                str(binding_store_path),
                "--effect-id-value",
                projection.effect_id.value,
            ],
            check=True,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "ANC_AUTHORITY_SECRET_HEX": kernel_key.hex(),
                **context.child_environment(),
            },
        )
        child_receipt = json.loads(completed.stdout.strip().splitlines()[-1])
        if child_receipt["dispatchId"] != str(dispatch_id):
            raise AssertionError("process restart replaced Dispatch identity")
        if child_receipt["bindingDigest"] != admission.binding_digest:
            raise AssertionError("process restart replaced Binding identity")

        reopened = authorized_journal_views(
            journal_path,
            kernel_key,
            namespace="live-bound-journal-restart",
            trust_domain="ordivon-live",
        )
        try:
            record = reopened.read.get_effect(projection.effect_id)
            if record.state is not EffectState.SUCCEEDED:
                raise AssertionError(f"replayed terminal state is {record.state}")
            current = reopened.read.current_binding_for(projection.effect_id)
            if current is None:
                raise AssertionError("replayed Effect lost Binding admission")
            context.service.resolve(current)
            reopened.read.verify_from_genesis()
            final_entries = reopened.read.journal_entry_count
        finally:
            reopened.read.close()

        jobs = real_client.call_tool("task.list", {"limit": 100})["jobs"]
        matches = [
            job for job in jobs if job.get("clientRequestId") == client_request_id
        ]
        exec_deliveries = [
            name for name, _ in real_client.calls if name == "workspace.exec"
        ]
        if len(matches) != 1 or len(exec_deliveries) != 1:
            raise AssertionError("durable recovery duplicated or lost the original Job")

        print(
            json.dumps(
                {
                    "workspaceId": workspace_id,
                    "sourceRevision": resolved_revision,
                    "catalogRevision": contracts["workspace.exec"].revision,
                    "contractDigest": binding.contract.digest,
                    "initialState": first.state.value,
                    "terminalState": child_receipt["terminalState"],
                    "dispatchId": str(dispatch_id),
                    "bindingId": str(admission.binding_id),
                    "bindingDigest": admission.binding_digest,
                    "bindingArtifactResolvedAfterRestart": True,
                    "dispatchIdPreserved": True,
                    "jobId": child_receipt["jobId"],
                    "attemptId": child_receipt["attemptId"],
                    "workspaceExecDeliveries": len(exec_deliveries),
                    "correlatedJobCount": len(matches),
                    "responseDroppedAfterSuccessfulDelivery": lossy_client.dropped,
                    "kernelProcessRestarted": True,
                    "beforeRestartJournalEntries": before_restart_entries,
                    "finalJournalEntries": final_entries,
                    "semanticArtifactCount": child_receipt["semanticArtifactCount"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    finally:
        if views is not None:
            views.read.close()
        if opened:
            closed = real_client.call_tool(
                "workspace.close",
                {"schemaVersion": 1, "workspaceId": workspace_id, "force": False},
            )
            if closed.get("workspaceId") != workspace_id:
                raise AssertionError("workspace close identity mismatch")
        for suffix in ("", "-wal", "-shm"):
            Path(str(journal_path) + suffix).unlink(missing_ok=True)
        shutil.rmtree(binding_store_path, ignore_errors=True)


if __name__ == "__main__":
    main()
