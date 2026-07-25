#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import replace
from typing import Any

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.kernel import InvalidTransition, ReferenceKernel
from anc_semantic_core.model import (
    CapabilityRef,
    Claim,
    CompletionSemantics,
    EffectMode,
    EvidenceKind,
    EvidenceRef,
    Fact,
    Verification,
    VerificationDecision,
    VerificationPlan,
    WorldObjectRef,
)
from anc_semantic_core.ordivon import OrdivonExecution, OrdivonSemanticAdapter
from anc_semantic_core.state import EffectState
from anc_semantic_core.transport import ToolProtocolError, ToolRejected, ToolTransportError


class LocalMcpToolCaller:
    """Test-only local MCP caller; not a production transport implementation."""

    def __init__(self, endpoint: str, token: str) -> None:
        self.endpoint = endpoint
        self.token = token
        self.request_id = 100

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.request_id += 1
        body = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            },
            separators=(",", ":"),
        ).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = response.read()
        except urllib.error.HTTPError as error:
            detail = error.read(512).decode("utf-8", errors="replace")
            raise ToolTransportError(f"HTTP {error.code}: {detail}") from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise ToolTransportError(str(error)) from error
        try:
            envelope = json.loads(payload)
            result = envelope["result"]
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise ToolProtocolError("invalid MCP response envelope") from error
        structured = result.get("structuredContent")
        if result.get("isError") is True:
            detail = structured.get("error") if isinstance(structured, dict) else None
            if not isinstance(detail, dict):
                raise ToolProtocolError(f"unstructured Tool error from {name}")
            raise ToolRejected(
                name,
                code=str(detail.get("code", "TOOL_ERROR")),
                message=str(detail.get("message", "tool failed")),
                field=detail.get("field") if isinstance(detail.get("field"), str) else None,
                retryable=detail.get("retryable") is True,
                detail=detail,
            )
        if not isinstance(structured, dict):
            raise ToolProtocolError(f"Tool {name} returned no structuredContent")
        return structured


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run live Ordivon semantic conformance")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument(
        "--source-repo",
        default="/root/projects/agent-native-computing",
    )
    parser.add_argument("--source-revision", required=True)
    return parser.parse_args()


def digest_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


def main() -> None:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")
    client = LocalMcpToolCaller(args.endpoint, token)
    stamp = int(time.time() * 1000)
    workspace_id = f"anc-live-semantic-{stamp}"
    opened = False
    try:
        opened_payload = client.call_tool(
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
        target = WorldObjectRef(
            SemanticId(IdKind.WORLD_OBJECT, f"ordivon-workspace:{workspace_id}"),
            version=resolved_revision,
        )
        base = sample_effect(f"live-{stamp}")
        spec = replace(
            base,
            target=target,
            mode=EffectMode.CHANGE,
            operation="workspace.exec",
            capability=CapabilityRef(
                SemanticId(IdKind.PRINCIPAL, "agent:live-conformance"),
                "workspace.exec",
                target.object_id,
            ),
            completion=CompletionSemantics.VERIFIED,
            verification=VerificationPlan(
                method="stdout-markers",
                required_evidence=(EvidenceKind.OBSERVATION, EvidenceKind.ARTIFACT),
            ),
        )
        kernel = ReferenceKernel()
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"live:{stamp}:admit"),
            recorded_at_ms=stamp,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"live:{stamp}:prepare"),
            recorded_at_ms=stamp + 1,
        )
        adapter = OrdivonSemanticAdapter(kernel, client)
        projection = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution(
                workspace_id=workspace_id,
                executable="/usr/bin/bash",
                args=(
                    "-lc",
                    "printf 'semantic-live-start\\n'; sleep 1; "
                    "printf 'semantic-live-done\\n'",
                ),
                timeout_ms=20_000,
            ),
            wait_ms=0,
        )
        initial_state = projection.state
        for _ in range(4):
            if projection.state.terminal:
                break
            projection = adapter.observe(spec.effect_id, wait_ms=10_000)
        if projection.state is not EffectState.SUCCEEDED:
            raise AssertionError(f"live Effect did not succeed: {projection.state}")
        if projection.binding is None or projection.observation is None:
            raise AssertionError("live Effect lacks Ordivon identity or terminal observation")
        if not projection.artifacts:
            raise AssertionError("live terminal result has no semantic Artifacts")

        duplicate_blocked = False
        try:
            adapter.dispatch_exec(
                spec.effect_id,
                OrdivonExecution(workspace_id, "/usr/bin/true"),
            )
        except InvalidTransition:
            duplicate_blocked = True
        if not duplicate_blocked:
            raise AssertionError("terminal Effect was redispatched")

        jobs = client.call_tool("task.list", {"limit": 100})["jobs"]
        matching_jobs = [
            job
            for job in jobs
            if job.get("clientRequestId") == projection.binding.client_request_id
        ]
        if len(matching_jobs) != 1:
            raise AssertionError(
                f"expected exactly one correlated Job, found {len(matching_jobs)}"
            )

        raw_artifacts = projection.payload.get("artifacts", []) if projection.payload else []
        stdout_raw = next(
            (artifact for artifact in raw_artifacts if artifact.get("kind") == "stdout"),
            None,
        )
        stdout_semantic = next(
            (artifact for artifact in projection.artifacts if artifact.kind == "stdout"),
            None,
        )
        if stdout_raw is None or stdout_semantic is None:
            raise AssertionError("terminal result has no stdout Artifact")
        artifact_read = client.call_tool(
            "artifact.read",
            {
                "schemaVersion": 1,
                "jobId": projection.binding.job_id,
                "artifactId": stdout_raw["artifactId"],
                "offset": 0,
                "maxBytes": 65_536,
            },
        )
        content = artifact_read["content"]
        markers = ("semantic-live-start", "semantic-live-done")
        if not all(marker in content for marker in markers):
            raise AssertionError("stdout Artifact does not contain both live markers")

        claim = Claim(
            claim_id=sid(IdKind.CLAIM, f"live:{stamp}:claim"),
            effect_id=spec.effect_id,
            subject=target,
            predicate="stdout_contains_markers",
            value_digest=digest_text("\n".join(markers)),
        )
        kernel.admit_claim(claim)
        verification = Verification(
            verification_id=sid(IdKind.VERIFICATION, f"live:{stamp}:verification"),
            claim_id=claim.claim_id,
            method="stdout-markers",
            evidence=(
                EvidenceRef(
                    EvidenceKind.OBSERVATION,
                    projection.observation.observation_id,
                ),
                EvidenceRef(EvidenceKind.ARTIFACT, stdout_semantic.artifact_id),
            ),
            decision=VerificationDecision.ACCEPTED,
            verified_at_ms=int(time.time() * 1000),
        )
        kernel.record_verification(verification)
        fact = Fact(
            fact_id=sid(IdKind.FACT, f"live:{stamp}:fact"),
            claim_id=claim.claim_id,
            verification_id=verification.verification_id,
            accepted_at_ms=int(time.time() * 1000),
        )
        kernel.commit_fact(fact)
        kernel.validate_invariants()

        print(
            json.dumps(
                {
                    "workspaceId": workspace_id,
                    "sourceRevision": resolved_revision,
                    "initialState": initial_state.value,
                    "terminalState": projection.state.value,
                    "jobId": projection.binding.job_id,
                    "attemptId": projection.binding.attempt_id,
                    "semanticArtifactCount": len(projection.artifacts),
                    "correlatedJobCount": len(matching_jobs),
                    "duplicateDispatchBlocked": duplicate_blocked,
                    "stdoutDigest": artifact_read["digest"],
                    "stdoutMarkersVerified": True,
                    "factCommitted": True,
                },
                indent=2,
                sort_keys=True,
            )
        )
    finally:
        if opened:
            closed = client.call_tool(
                "workspace.close",
                {"schemaVersion": 1, "workspaceId": workspace_id, "force": False},
            )
            if closed.get("workspaceId") != workspace_id:
                raise AssertionError("workspace close identity mismatch")


if __name__ == "__main__":
    main()
