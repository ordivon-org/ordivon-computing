#!/usr/bin/env python3
"""Read-only oracle for current Host Task-head Workspace navigation references.

This script is research apparatus, not a production claimant service.
It reads current Host task heads and WorkingCheckpoint CAS objects directly so a
future Host candidate can be compared against an independent exact projection.
It never writes Host or Runtime state and never infers semantic ownership.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
from typing import Any


def _object(root: Path, digest: str) -> dict[str, Any]:
    if not digest.startswith("sha256:") or len(digest) != 71:
        raise ValueError(f"invalid object digest: {digest!r}")
    path = root / "objects" / f"{digest[7:]}.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"object is not a JSON object: {digest}")
    if value.get("schemaVersion") != 1 or set(value) != {"schemaVersion", "kind", "payload"}:
        raise ValueError(f"unexpected CAS envelope: {digest}")
    return value


def project(host_root: Path, runtime_workspaces: Path, workspace_id: str | None) -> dict[str, Any]:
    database = host_root / "host.sqlite3"
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            "SELECT p.task_id, p.goal_id, p.state, p.revision, p.updated_at_ms, "
            "e.event_kind, e.payload_digest "
            "FROM task_projection p JOIN events e "
            "ON e.stream_id = p.task_id AND e.stream_revision = p.revision "
            "ORDER BY p.updated_at_ms DESC, p.task_id"
        ).fetchall()
    finally:
        connection.close()

    relations: list[dict[str, Any]] = []
    state_counts: dict[str, int] = {}
    binding_counts: dict[str, int] = {}

    for task_id, goal_id, state, revision, updated_at_ms, event_kind, payload_digest in rows:
        state_counts[state] = state_counts.get(state, 0) + 1
        event_object = _object(host_root, payload_digest)
        event_payload = event_object["payload"]
        if not isinstance(event_payload, dict):
            raise ValueError(f"event payload is not an object: {task_id}@{revision}")
        data = event_payload.get("data")
        checkpoint_object_digest = data.get("checkpointObjectDigest") if isinstance(data, dict) else None
        if not isinstance(checkpoint_object_digest, str):
            continue
        checkpoint_object = _object(host_root, checkpoint_object_digest)
        checkpoint = checkpoint_object["payload"]
        if not isinstance(checkpoint, dict):
            raise ValueError(f"checkpoint payload is not an object: {task_id}@{revision}")
        runtime = checkpoint.get("runtime")
        relation_workspace = runtime.get("workspaceId") if isinstance(runtime, dict) else None
        if not isinstance(relation_workspace, str):
            continue
        binding_counts[state] = binding_counts.get(state, 0) + 1
        if workspace_id is not None and relation_workspace != workspace_id:
            continue
        workspace_exists = (runtime_workspaces / relation_workspace).is_dir()
        terminal = state in {"completed", "failed", "cancelled"}
        relations.append(
            {
                "workspaceId": relation_workspace,
                "workspaceDirectoryPresent": workspace_exists,
                "relationTruthRole": "current-host-task-head-runtime-navigation-reference",
                "task": {
                    "taskId": task_id,
                    "goalId": goal_id,
                    "state": state,
                    "revision": revision,
                    "updatedAtMs": updated_at_ms,
                    "headEventKind": event_kind,
                    "checkpointObjectDigest": checkpoint_object_digest,
                },
                "relationClass": "TERMINAL_HEAD_REFERENCE" if terminal else "READY_HEAD_REFERENCE",
                "semanticClaimantEvaluated": False,
                "runtimeCurrentnessValidatedByRuntimeApi": False,
                "ownerTruthEvaluated": False,
            }
        )

    by_workspace: dict[str, list[dict[str, Any]]] = {}
    for row in relations:
        by_workspace.setdefault(row["workspaceId"], []).append(row)

    workspace_rows: list[dict[str, Any]] = []
    for wid in sorted(by_workspace):
        refs = by_workspace[wid]
        ready = [row for row in refs if row["relationClass"] == "READY_HEAD_REFERENCE"]
        terminal = [row for row in refs if row["relationClass"] == "TERMINAL_HEAD_REFERENCE"]
        present = (runtime_workspaces / wid).is_dir()
        if ready:
            relation_status = (
                "EXPLICIT_READY_REFERENCE_PHYSICALLY_CURRENT"
                if present
                else "EXPLICIT_READY_REFERENCE_PHYSICALLY_ABSENT"
            )
        elif terminal:
            relation_status = "TERMINAL_HEAD_REFERENCE_ONLY"
        else:
            relation_status = "NO_CURRENT_HEAD_REFERENCE"
        workspace_rows.append(
            {
                "workspaceId": wid,
                "workspaceDirectoryPresent": present,
                "relationStatus": relation_status,
                "readyReferenceCount": len(ready),
                "terminalReferenceCount": len(terminal),
                "references": refs,
                "interpretation": (
                    "Host current-head reference projection only; this is not semantic claimant or owner truth"
                ),
            }
        )

    if workspace_id is not None and workspace_id not in by_workspace:
        workspace_rows.append(
            {
                "workspaceId": workspace_id,
                "workspaceDirectoryPresent": (runtime_workspaces / workspace_id).is_dir(),
                "relationStatus": "NO_CURRENT_HEAD_REFERENCE",
                "readyReferenceCount": 0,
                "terminalReferenceCount": 0,
                "references": [],
                "interpretation": (
                    "No current Host task head explicitly references this Workspace; semantic claimant state remains unknown"
                ),
            }
        )

    return {
        "schemaVersion": 1,
        "kind": "ordivon.workspace-claimant-discoverability-mechanical-oracle",
        "truthRole": "read-only-current-host-task-head-reference-oracle",
        "queryWorkspaceId": workspace_id,
        "summary": {
            "taskCount": len(rows),
            "taskStateCounts": dict(sorted(state_counts.items())),
            "taskHeadWorkspaceBindingCounts": dict(sorted(binding_counts.items())),
            "returnedRelationCount": len(relations),
            "returnedWorkspaceCount": len(workspace_rows),
        },
        "workspaces": workspace_rows,
        "globalInterpretation": (
            "Absence of a Host current-head reference is not proof that a Workspace is semantically unclaimed. "
            "Runtime and owner/domain currentness must be evaluated by their own authorities."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-state-root", type=Path, default=Path("/var/lib/ordivon/host"))
    parser.add_argument("--runtime-workspace-root", type=Path, default=Path("/var/lib/ordivon/runtime/workspaces"))
    parser.add_argument("--workspace-id")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = project(args.host_state_root, args.runtime_workspace_root, args.workspace_id)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
