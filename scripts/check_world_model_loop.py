#!/usr/bin/env python3
"""Validate the Ordivon Computing world-model loop and assimilation frontier."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / "research" / "world-model-loop-v2.json"
FRONTIER = ROOT / "research" / "world-model-frontier.json"
FOUNDATIONS = ROOT / "core" / "foundations.md"
ROUND_PATTERN = "world-model-assimilation-round-*.json"


def digest(document: dict[str, Any]) -> str:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def load_json(path: Path, label: str, issues: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"{label} cannot be loaded: {exc}")
        return None
    if not isinstance(value, dict):
        issues.append(f"{label} is not an object")
        return None
    return value


def check() -> list[str]:
    issues: list[str] = []

    def req(ok: bool, msg: str) -> None:
        if not ok:
            issues.append(msg)

    loop = load_json(LOOP, "world-model loop", issues)
    frontier = load_json(FRONTIER, "world-model frontier", issues)
    if loop is None or frontier is None:
        return issues

    req(loop.get("schemaVersion") == 1, "world-model loop schema differs")
    req(loop.get("kind") == "ordivon.world-model-loop", "world-model loop kind differs")
    req(loop.get("loopId") == "WML-2-001", "world-model loop id differs")
    req(
        loop.get("supersedes") == "research/world-model-loop-v1.json#WML-1-001",
        "world-model loop v2 predecessor differs",
    )
    frontier_semantics = loop.get("frontierSemantics", {})
    req(
        frontier_semantics.get("recordRole") == "historical_observation_frontier",
        "frontier role differs",
    )
    req(
        frontier_semantics.get("freshnessPolicy") == "git_relation_freshness_v2",
        "freshness policy differs",
    )
    req(
        frontier_semantics.get("assessorRef") == "scripts/assess_world_model_freshness.py",
        "freshness assessor differs",
    )
    req(
        loop.get("integrity", {}).get("payloadDigest") == digest(loop),
        "world-model loop digest differs",
    )
    expected_stages = [
        "OBSERVE_PROJECT_DELTAS",
        "EXTRACT_MODEL_PRESSURE",
        "COMPARE_ACROSS_WORLDS",
        "REVISE_OR_RETAIN",
        "PROPAGATE_AS_QUESTIONS",
        "PROJECT_RETEST",
        "REASSIMILATE",
    ]
    req(
        [stage.get("stage") for stage in loop.get("stages", [])] == expected_stages,
        "world-model loop stages differ",
    )

    req(frontier.get("schemaVersion") == 1, "world-model frontier schema differs")
    req(
        frontier.get("kind") == "ordivon.world-model-assimilation-frontier",
        "world-model frontier kind differs",
    )
    req(
        frontier.get("loopRef") == "research/world-model-loop-v2.json",
        "world-model frontier loop binding differs",
    )
    req(frontier.get("ownerFactsCopied") is False, "world-model frontier may not copy owner facts")
    req(
        frontier.get("integrity", {}).get("payloadDigest") == digest(frontier),
        "world-model frontier digest differs",
    )

    observed_by_round = frontier.get("observedByRound")
    round_ref_ok = isinstance(observed_by_round, str) and bool(
        re.fullmatch(r"research/world-model-assimilation-round-[0-9]{3}\.json", observed_by_round)
    )
    req(round_ref_ok, "world-model frontier accepted-round reference differs")
    latest_round: dict[str, Any] | None = None
    if round_ref_ok:
        latest_round = load_json(ROOT / observed_by_round, "accepted world-model assimilation round", issues)

    rounds = sorted((ROOT / "research").glob(ROUND_PATTERN))
    req(bool(rounds), "world-model assimilation history is empty")
    for path in rounds:
        round_doc = load_json(path, f"world-model assimilation round {path.name}", issues)
        if round_doc is None:
            continue
        req(round_doc.get("schemaVersion") == 1, f"assimilation round schema differs: {path.name}")
        req(
            round_doc.get("kind") == "ordivon.world-model-assimilation-round",
            f"assimilation round kind differs: {path.name}",
        )
        req(
            bool(re.fullmatch(r"WML-R[0-9]+-[0-9]{3}", str(round_doc.get("roundId", "")))),
            f"assimilation round id differs: {path.name}",
        )
        req(
            round_doc.get("integrity", {}).get("payloadDigest") == digest(round_doc),
            f"assimilation round digest differs: {path.name}",
        )
        observed = round_doc.get("observedProjectRevisions", {})
        req(isinstance(observed, dict), f"assimilation observed revisions differ: {path.name}")
        if isinstance(observed, dict):
            for project_id, revision in observed.items():
                req(
                    bool(re.fullmatch(r"[0-9a-f]{40}", str(revision))),
                    f"invalid assimilation observed revision: {path.name}:{project_id}",
                )

    if latest_round is not None:
        req(
            latest_round.get("loopRef") == frontier.get("loopRef"),
            "accepted round and frontier loop binding differ",
        )

    project_ids = [
        item.get("projectId")
        for item in frontier.get("projects", [])
        if isinstance(item, dict)
    ]
    req(len(project_ids) == len(set(project_ids)), "world-model frontier has duplicate projects")
    req("ordivon-computing" not in project_ids, "historical owner-observation frontier may not contain Computing itself")
    allowed = set(frontier.get("allowedStates", []))
    for item in frontier.get("projects", []):
        if not isinstance(item, dict):
            issues.append("world-model frontier entry is not an object")
            continue
        req(
            bool(re.fullmatch(r"[0-9a-f]{40}", str(item.get("observedRevision", "")))),
            f"invalid observed revision: {item.get('projectId')}",
        )
        req(
            item.get("assimilationState") in allowed,
            f"invalid assimilation state: {item.get('projectId')}",
        )
        req(bool(item.get("reason")), f"missing review reason: {item.get('projectId')}")

    foundations = FOUNDATIONS.read_text(encoding="utf-8")
    req("## A1 — Inherit mature mechanism owners" in foundations, "A1 provider-first revision is missing")
    req("this burden is comparative" in foundations, "A11 comparative retention test is missing")

    return issues


if __name__ == "__main__":
    issues = check()
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        raise SystemExit(1)
    print("World-model loop and assimilation frontier: OK")
