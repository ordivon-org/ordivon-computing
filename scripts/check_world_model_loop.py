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
ROUND = ROOT / "research" / "world-model-assimilation-round-001.json"
REGISTRY = ROOT / "projects" / "registry.yaml"


def digest(document: dict[str, Any]) -> str:
    payload = {k:v for k,v in document.items() if k != "integrity"}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def check() -> list[str]:
    issues: list[str] = []
    try:
        loop = json.loads(LOOP.read_text(encoding="utf-8"))
        frontier = json.loads(FRONTIER.read_text(encoding="utf-8"))
        round_doc = json.loads(ROUND.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"world-model records cannot be loaded: {exc}"]
    def req(ok: bool, msg: str) -> None:
        if not ok:
            issues.append(msg)
    req(loop.get("schemaVersion") == 1, "world-model loop schema differs")
    req(loop.get("kind") == "ordivon.world-model-loop", "world-model loop kind differs")
    req(loop.get("loopId") == "WML-2-001", "world-model loop id differs")
    req(loop.get("supersedes") == "research/world-model-loop-v1.json#WML-1-001", "world-model loop v2 predecessor differs")
    fs = loop.get("frontierSemantics", {})
    req(fs.get("recordRole") == "historical_observation_frontier", "frontier role differs")
    req(fs.get("freshnessPolicy") == "git_relation_freshness_v2", "freshness policy differs")
    req(fs.get("assessorRef") == "scripts/assess_world_model_freshness.py", "freshness assessor differs")
    req(loop.get("integrity", {}).get("payloadDigest") == digest(loop), "world-model loop digest differs")
    expected_stages = ["OBSERVE_PROJECT_DELTAS","EXTRACT_MODEL_PRESSURE","COMPARE_ACROSS_WORLDS","REVISE_OR_RETAIN","PROPAGATE_AS_QUESTIONS","PROJECT_RETEST","REASSIMILATE"]
    req([s.get("stage") for s in loop.get("stages", [])] == expected_stages, "world-model loop stages differ")
    req(round_doc.get("schemaVersion") == 1, "world-model assimilation round schema differs")
    req(round_doc.get("kind") == "ordivon.world-model-assimilation-round", "world-model assimilation round kind differs")
    req(round_doc.get("roundId") == "WML-R1-001", "world-model assimilation round id differs")
    req(round_doc.get("integrity", {}).get("payloadDigest") == digest(round_doc), "world-model assimilation round digest differs")
    req(frontier.get("observedByRound") == "research/world-model-assimilation-round-001.json", "world-model frontier is not bound to accepted round 001")
    req(frontier.get("schemaVersion") == 1, "world-model frontier schema differs")
    req(frontier.get("kind") == "ordivon.world-model-assimilation-frontier", "world-model frontier kind differs")
    req(frontier.get("loopRef") == "research/world-model-loop-v1.json", "historical world-model frontier loop binding differs")
    req(frontier.get("ownerFactsCopied") is False, "world-model frontier may not copy owner facts")
    req(frontier.get("integrity", {}).get("payloadDigest") == digest(frontier), "world-model frontier digest differs")
    registry_ids = [m.group(1) for line in REGISTRY.read_text(encoding="utf-8").splitlines() if (m := re.fullmatch(r"  - id: (ordivon-[a-z0-9-]+)", line))]
    project_ids = [p.get("projectId") for p in frontier.get("projects", []) if isinstance(p, dict)]
    req(len(project_ids) == len(set(project_ids)), "world-model frontier has duplicate projects")
    req(set(project_ids) == set(registry_ids) - {"ordivon-computing"}, "world-model frontier project set differs from registry")
    allowed = set(frontier.get("allowedStates", []))
    for item in frontier.get("projects", []):
        if not isinstance(item, dict):
            issues.append("world-model frontier entry is not an object")
            continue
        req(bool(re.fullmatch(r"[0-9a-f]{40}", str(item.get("observedRevision", "")))), f"invalid observed revision: {item.get('projectId')}")
        req(item.get("assimilationState") in allowed, f"invalid assimilation state: {item.get('projectId')}")
        req(bool(item.get("reason")), f"missing review reason: {item.get('projectId')}")
    for required in ("ordivon-finance", "ordivon-studio"):
        req(required in registry_ids, f"stable project registry is missing {required}")
    return issues

if __name__ == "__main__":
    issues = check()
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        raise SystemExit(1)
    print("World-model loop and assimilation frontier: OK")
