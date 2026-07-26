#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import secrets
import time
from dataclasses import replace

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.bootstrap import authorized_reference_views
from anc_semantic_core.kernel import InvalidTransition
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
from live_support import LocalMcpToolCaller, digest_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run live Ordivon semantic conformance")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument(
        "--source-repo",
        default="/root/projects/ordivon-architecture",
    )
    parser.add_argument("--source-revision", required=True)
    return parser.parse_args()


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
        views = authorized_reference_views(
            secrets.token_bytes(32), namespace="live-exec"
        )
        views.effects.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"live:{stamp}:admit"),
            recorded_at_ms=stamp,
        )
        views.effects.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"live:{stamp}:prepare"),
            recorded_at_ms=stamp + 1,
        )
        adapter = OrdivonSemanticAdapter(views.execution, client)
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
            origin_effect_id=spec.effect_id,
            subject=target,
            predicate="stdout_contains_markers",
            value_digest=digest_text("\n".join(markers)),
        )
        verified_at_ms = int(time.time() * 1000)
        views.verification.admit_claim(claim, proposed_at_ms=verified_at_ms)
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
            verified_at_ms=verified_at_ms,
        )
        views.verification.record_verification(verification)
        fact = Fact(
            fact_id=sid(IdKind.FACT, f"live:{stamp}:fact"),
            claim_id=claim.claim_id,
            verification_id=verification.verification_id,
            accepted_at_ms=int(time.time() * 1000),
        )
        views.facts.commit_fact(fact)
        views.read.validate_invariants()

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
