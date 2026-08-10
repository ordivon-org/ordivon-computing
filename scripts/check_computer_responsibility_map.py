#!/usr/bin/env python3
"""Validate the current, contracted Ordivon Computer responsibility prior."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "research/computer-responsibility-map-v2.json"


def digest(document: dict[str, Any]) -> str:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def activity_digest(state: dict[str, list[str]]) -> str:
    encoded = json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def check() -> list[str]:
    issues: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            issues.append(message)

    try:
        document = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        portfolio = json.loads((ROOT / document["portfolioRef"]).read_text(encoding="utf-8"))
    except (OSError, KeyError, json.JSONDecodeError) as error:
        return [f"responsibility prior cannot be loaded: {error}"]

    require(document.get("schemaVersion") == 2, "responsibility prior schema differs")
    require(document.get("kind") == "ordivon.computer-responsibility-map", "responsibility prior kind differs")
    require(document.get("mapId") == "ACR-M2-001", "responsibility prior identity differs")
    require(document.get("status") == "current_responsibility_prior", "responsibility prior status differs")
    require(document.get("methodRef") == "research/experiment-contract-v1.json", "responsibility prior experiment-contract binding differs")
    require((ROOT / document.get("methodRef", "")).is_file(), "responsibility prior experiment contract is missing")
    require(document.get("integrity", {}).get("payloadDigest") == digest(document), "responsibility prior digest differs")

    revision = document.get("sourceRevision")
    require(isinstance(revision, str) and len(revision) == 40, "responsibility prior source revision is invalid")
    if isinstance(revision, str):
        result = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{revision}^{{commit}}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        require(result.returncode == 0, "responsibility prior source revision is unreachable")

    current_activity = {
        "activeIds": sorted(q["id"] for q in portfolio.get("questions", []) if isinstance(q, dict) and q.get("status") == "active"),
        "readyIds": sorted(q["id"] for q in portfolio.get("questions", []) if isinstance(q, dict) and q.get("status") == "ready"),
    }
    binding = document.get("portfolioActivityBinding", {})
    require(binding.get("activeIds") == current_activity["activeIds"], "responsibility prior active portfolio binding is stale")
    require(binding.get("readyIds") == current_activity["readyIds"], "responsibility prior ready portfolio binding is stale")
    require(binding.get("stateDigest") == activity_digest(current_activity), "responsibility prior portfolio activity digest differs")

    items = document.get("responsibilities")
    require(isinstance(items, list) and bool(items), "responsibility prior has no responsibilities")
    by_id: dict[str, dict[str, Any]] = {}
    if isinstance(items, list):
        for item in items:
            require(isinstance(item, dict), "responsibility entry is not an object")
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            require(isinstance(item_id, str) and item_id not in by_id, f"invalid or duplicate responsibility id: {item_id}")
            if not isinstance(item_id, str):
                continue
            by_id[item_id] = item
            for field in ("name", "classification", "lowestOwner", "disposition", "nextFalsifier", "futureModelRobustness"):
                require(isinstance(item.get(field), str) and bool(item.get(field)), f"{item_id} missing {field}")
            carriers = item.get("currentCarrier")
            require(isinstance(carriers, list) and bool(carriers) and all(isinstance(v, str) and v for v in carriers), f"{item_id} current carriers are invalid")
            evidence = item.get("evidenceRefs")
            require(isinstance(evidence, list) and bool(evidence), f"{item_id} evidence refs are invalid")
            if isinstance(evidence, list):
                for relative in evidence:
                    require(isinstance(relative, str) and (ROOT / relative).exists(), f"{item_id} evidence ref is missing: {relative}")

    expected = {"CR-01", "CR-02", "CR-03", "CR-04", "CR-05", "CR-06", "CR-07", "CR-09", "CR-12", "CR-17"}
    require(set(by_id) == expected, "current responsibility id set differs")
    for item_id in {"CR-02", "CR-03", "CR-04", "CR-05", "CR-06", "CR-07", "CR-09"}:
        require(by_id.get(item_id, {}).get("futureModelRobustness") == "strong", f"durable responsibility lost strong status: {item_id}")
        require("defer" not in str(by_id.get(item_id, {}).get("disposition", "")), f"durable responsibility was deferred: {item_id}")
    require(by_id.get("CR-01", {}).get("disposition") == "delegate_to_classical", "classical substrate delegation changed")
    require(by_id.get("CR-12", {}).get("name") == "shared_protocol_boundary", "shared protocol responsibility regressed to universal IR")
    require(by_id.get("CR-17", {}).get("disposition") == "retain_bounded_experiment_discipline", "bounded self-reform responsibility differs")

    limits = set(document.get("doesNotAuthorize", []))
    for required in {
        "new_shared_platform_from_absence_of_pressure",
        "owner_repository_mutation",
        "automatic_protocol_0_4_release_or_consumer_cutover",
        "autonomous_pressure_or_evaluator_law_discovery",
        "open_ended_RSI_claim",
    }:
        require(required in limits, f"responsibility prior lost authority boundary: {required}")
    return sorted(set(issues))


if __name__ == "__main__":
    issues = check()
    print(json.dumps({"schemaVersion": 2, "kind": "ordivon-computer-responsibility-prior-check", "ok": not issues, "issues": issues}, indent=2, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if not issues else 1)
