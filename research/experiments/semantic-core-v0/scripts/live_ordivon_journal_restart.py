#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import secrets
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.bootstrap import KernelAuthorityViews, authorized_journal_views
from anc_semantic_core.model import (
    CapabilityRef,
    CompletionSemantics,
    EffectMode,
    WorldObjectRef,
)
from anc_semantic_core.ordivon import (
    OrdivonExecution,
    OrdivonSemanticAdapter,
    ordivon_workspace_object_id,
)
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
        description="Prove durable Semantic Kernel recovery across a real process restart"
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument(
        "--source-repo",
        default="/root/projects/agent-native-computing",
    )
    parser.add_argument("--source-revision")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--journal")
    parser.add_argument("--effect-id-value")
    return parser.parse_args()


def authority_secret(*, create: bool) -> bytes:
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
    raise SystemExit("ANC_AUTHORITY_SECRET_HEX is required to resume the signed journal")


def resume(args: argparse.Namespace, token: str) -> None:
    if not args.journal or not args.effect_id_value:
        raise SystemExit("--resume requires --journal and --effect-id-value")
    secret = authority_secret(create=False)
    views = authorized_journal_views(
        args.journal,
        secret,
        namespace="live-journal-restart",
        trust_domain="ordivon-live",
    )
    try:
        effect_id = SemanticId(IdKind.EFFECT, args.effect_id_value)
        adapter = OrdivonSemanticAdapter(
            views.execution,
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
            raise AssertionError("process restart produced no Job binding")
        views.read.validate_invariants()
        print(
            json.dumps(
                {
                    "terminalState": projection.state.value,
                    "dispatchId": str(projection.binding.dispatch_id),
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
    lossy_client = DropFirstSuccessfulResponse(real_client, "workspace.exec")
    stamp = int(time.time() * 1000)
    workspace_id = f"anc-live-journal-restart-{stamp}"
    journal_path = Path(f"/tmp/anc-semantic-journal-{stamp}.sqlite3")
    opened = False
    views: KernelAuthorityViews | None = None
    authority_key = authority_secret(create=True)
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
        target_id = ordivon_workspace_object_id(workspace_id)
        base = sample_effect(f"journal-restart-{stamp}")
        spec = replace(
            base,
            target=WorldObjectRef(target_id, version=resolved_revision),
            mode=EffectMode.CHANGE,
            operation="workspace.exec",
            capability=CapabilityRef(
                SemanticId(IdKind.PRINCIPAL, "agent:journal-restart-conformance"),
                "workspace.exec",
                target_id,
            ),
            completion=CompletionSemantics.VERIFIED,
        )
        clock = iter(range(stamp, stamp + 1_000_000)).__next__
        views = authorized_journal_views(
            journal_path,
            authority_key,
            namespace="live-journal-restart",
            trust_domain="ordivon-live",
        )
        views.effects.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"journal-restart:{stamp}:admit"),
            recorded_at_ms=clock(),
        )
        views.effects.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"journal-restart:{stamp}:prepare"),
            recorded_at_ms=clock(),
        )
        adapter = OrdivonSemanticAdapter(views.execution, lossy_client, clock_ms=clock)
        first = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution(
                workspace_id=workspace_id,
                executable="/usr/bin/bash",
                args=(
                    "-lc",
                    "printf 'journal-restart-start\\n'; sleep 1; "
                    "printf 'journal-restart-done\\n'",
                ),
                timeout_ms=20_000,
            ),
            wait_ms=0,
        )
        if first.state is not EffectState.UNKNOWN:
            raise AssertionError(f"response loss did not produce UNKNOWN: {first.state}")
        dispatch_id = views.read.get_effect(spec.effect_id).dispatch_id
        if dispatch_id is None:
            raise AssertionError("UNKNOWN Effect lost Dispatch identity")
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
                "--effect-id-value",
                spec.effect_id.value,
            ],
            check=True,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "ANC_AUTHORITY_SECRET_HEX": authority_key.hex(),
            },
        )
        child_receipt = json.loads(completed.stdout.strip().splitlines()[-1])
        if child_receipt["dispatchId"] != str(dispatch_id):
            raise AssertionError("process restart replaced Dispatch identity")

        reopened = authorized_journal_views(
            journal_path,
            authority_key,
            namespace="live-journal-restart",
            trust_domain="ordivon-live",
        )
        try:
            record = reopened.read.get_effect(spec.effect_id)
            if record.state is not EffectState.SUCCEEDED:
                raise AssertionError(f"replayed terminal state is {record.state}")
            reopened.read.validate_invariants()
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
                    "initialState": first.state.value,
                    "terminalState": child_receipt["terminalState"],
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
                    "journalPathRemovedAfterTest": True,
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


if __name__ == "__main__":
    main()
