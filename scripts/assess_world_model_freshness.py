#!/usr/bin/env python3
"""Assess freshness of the retained world-model observation frontier.

This is a sensing projection only. Revision movement creates review pressure; it
never implies that a shared world-model claim changed or that owner state should
be copied into Computing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

from frontier_freshness import classify_revision_relation

ROOT = Path(__file__).resolve().parents[1]

FRONTIER = ROOT / "research/world-model-frontier.json"
PROJECT_ROOT = Path("/root/projects")


def digest(value: dict[str, Any]) -> str:
    payload = dict(value)
    payload.pop("integrity", None)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def head(repository: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    ).strip()


def assess() -> dict[str, Any]:
    frontier = json.loads(FRONTIER.read_text(encoding="utf-8"))
    observed = {item["projectId"]: item["observedRevision"] for item in frontier["projects"]}
    rows = []
    counts: dict[str, int] = {}
    for project_id in sorted(observed):
        repository = PROJECT_ROOT / project_id
        try:
            current = head(repository)
        except (OSError, subprocess.CalledProcessError):
            state = "local_repository_unavailable"
            counts[state] = counts.get(state, 0) + 1
            rows.append(
                {
                    "projectId": project_id,
                    "observedRevision": observed[project_id],
                    "localHeadRevision": None,
                    "freshnessState": state,
                    "commitsAhead": None,
                    "commitsBehind": None,
                    "current": False,
                    "observationBoundary": "local checkout unavailable; this is not evidence that the semantic owner/project is absent",
                }
            )
            continue
        relation = classify_revision_relation(repository, observed[project_id], current)
        counts[relation.state] = counts.get(relation.state, 0) + 1
        rows.append(
            {
                "projectId": project_id,
                "observedRevision": relation.observed_revision,
                "localHeadRevision": relation.current_revision,
                "freshnessState": relation.state,
                "commitsAhead": relation.commits_ahead,
                "commitsBehind": relation.commits_behind,
                "current": relation.current,
            }
        )
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.world-model-frontier-freshness-assessment",
        "frontierRef": "research/world-model-frontier.json",
        "policyId": "git_relation_freshness_v2",
        "sourceBasis": "local Git checkout HEAD when available; unavailable historical checkouts remain explicit non-current observations",
        "projectCount": len(rows),
        "allCurrent": all(row["current"] for row in rows),
        "counts": dict(sorted(counts.items())),
        "projects": rows,
        "inferenceBoundary": "revision relation or local-checkout unavailability is freshness/review pressure only; it does not imply owner absence or a shared world-model revision",
    }
    result["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evidence-json-v1",
        "payloadDigest": digest(result),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-current", action="store_true")
    args = parser.parse_args()
    result = assess()
    rendered = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if args.require_current and not result["allCurrent"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
