#!/usr/bin/env python3
"""Validate the Agent-first Ordivon Computer responsibility map."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "research" / "computer-responsibility-map-v1.json"


def canonical_digest(document: dict[str, Any]) -> str:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def require(condition: bool, message: str, issues: list[str]) -> None:
    if not condition:
        issues.append(message)


def check() -> list[str]:
    issues: list[str] = []
    try:
        document = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"computer responsibility map cannot be loaded: {error}"]

    require(document.get("schemaVersion") == 1, "responsibility map schema differs", issues)
    require(document.get("kind") == "ordivon.computer-responsibility-map", "responsibility map kind differs", issues)
    require(document.get("mapId") == "ACR-M1-001", "responsibility map identity differs", issues)
    require(document.get("status") == "active_reform_input", "responsibility map status differs", issues)
    require(document.get("methodRef") == "research/research-method-v1.json", "responsibility map method binding differs", issues)
    require((ROOT / "research" / "research-method-v1.json").is_file(), "Agent-first research method is missing", issues)
    require((ROOT / "research" / "COMPUTER-RESPONSIBILITY-REVIEW.md").is_file(), "human responsibility review is missing", issues)

    integrity = document.get("integrity")
    require(isinstance(integrity, dict), "responsibility map integrity is missing", issues)
    if isinstance(integrity, dict):
        require(integrity.get("algorithm") == "sha256", "responsibility map integrity algorithm differs", issues)
        require(
            integrity.get("canonicalization") == "ordivon-evidence-json-v1",
            "responsibility map canonicalization differs",
            issues,
        )
        require(integrity.get("payloadDigest") == canonical_digest(document), "responsibility map payload digest differs", issues)

    source_revision = document.get("sourceRevision")
    require(isinstance(source_revision, str) and len(source_revision) == 40, "responsibility map source revision is invalid", issues)
    if isinstance(source_revision, str):
        completed = subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-e", f"{source_revision}^{{commit}}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        require(completed.returncode == 0, "responsibility map source revision is not reachable", issues)

    items = document.get("responsibilities")
    require(isinstance(items, list) and bool(items), "responsibility map has no responsibilities", issues)
    by_id: dict[str, dict[str, Any]] = {}
    if isinstance(items, list):
        for item in items:
            require(isinstance(item, dict), "responsibility entry is not an object", issues)
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            require(isinstance(item_id, str) and bool(item_id), "responsibility id is invalid", issues)
            if not isinstance(item_id, str):
                continue
            require(item_id not in by_id, f"duplicate responsibility id: {item_id}", issues)
            by_id[item_id] = item
            for field in (
                "name",
                "futureModelRobustness",
                "classification",
                "lowestOwner",
                "disposition",
                "nextFalsifier",
            ):
                require(isinstance(item.get(field), str) and bool(item.get(field)), f"{item_id} missing {field}", issues)
            carriers = item.get("currentCarrier")
            require(
                isinstance(carriers, list)
                and bool(carriers)
                and all(isinstance(value, str) and value for value in carriers),
                f"{item_id} currentCarrier is invalid",
                issues,
            )
            evidence_refs = item.get("evidenceRefs")
            require(
                isinstance(evidence_refs, list)
                and bool(evidence_refs)
                and all(isinstance(value, str) and value for value in evidence_refs),
                f"{item_id} evidenceRefs are invalid",
                issues,
            )
            if isinstance(evidence_refs, list):
                for relative in evidence_refs:
                    if isinstance(relative, str) and ":" not in relative:
                        require((ROOT / relative).exists(), f"{item_id} evidence ref is missing: {relative}", issues)

    required_ids = {f"CR-{index:02d}" for index in range(1, 19)}
    require(set(by_id) == required_ids, "responsibility id set differs", issues)

    durable = {"CR-02", "CR-03", "CR-04", "CR-05", "CR-06", "CR-07", "CR-09"}
    for item_id in durable:
        item = by_id.get(item_id, {})
        require(item.get("futureModelRobustness") == "strong", f"durable responsibility lost strong future-model status: {item_id}", issues)
        require("defer" not in str(item.get("disposition", "")), f"durable responsibility was accidentally deferred: {item_id}", issues)

    conditional = {"CR-08", "CR-10", "CR-11", "CR-12", "CR-13", "CR-14", "CR-15", "CR-16", "CR-17", "CR-18"}
    for item_id in conditional:
        item = by_id.get(item_id, {})
        require(item.get("classification") != "durable_invariant", f"conditional candidate promoted to durable invariant: {item_id}", issues)

    for item_id in {"CR-11", "CR-13"}:
        require(by_id.get(item_id, {}).get("disposition") == "do_not_build_shared_layer", f"shared-layer rejection changed: {item_id}", issues)
    for item_id in {"CR-14", "CR-15", "CR-16"}:
        require(
            by_id.get(item_id, {}).get("disposition") == "defer_until_strong_baseline_fails",
            f"cognitive candidate is no longer gated by a strong baseline: {item_id}",
            issues,
        )
    require(by_id.get("CR-01", {}).get("disposition") == "delegate_to_classical", "classical substrate delegation changed", issues)
    require(by_id.get("CR-10", {}).get("disposition") == "keep_product_specific_not_core", "Harness packaging was promoted into Core", issues)

    frontier = document.get("reformFrontier")
    require(isinstance(frontier, list), "reform frontier is missing", issues)
    if isinstance(frontier, list):
        require([item.get("step") for item in frontier if isinstance(item, dict)] == ["C1", "C2", "C3", "C4", "C5"], "reform frontier order differs", issues)

    non_authorized = set(document.get("doesNotAuthorize", []))
    for required in {
        "B5_Trial006",
        "additional_DeepSeek_canaries",
        "B6_implementation",
        "Prime_or_TCG_implementation",
        "Host_Harness_Runtime_merge",
        "new_World_Memory_Graph_or_Organization_platform",
    }:
        require(required in non_authorized, f"responsibility map lost non-authorization: {required}", issues)

    receipt_path = ROOT / "research" / "evidence" / "computer-responsibility-reform-064345e.json"
    require(receipt_path.is_file(), "Computer responsibility reform acceptance receipt is missing", issues)
    if receipt_path.is_file():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            issues.append(f"Computer responsibility reform receipt cannot be loaded: {error}")
        else:
            require(receipt.get("schemaVersion") == 1, "Computer reform receipt schema differs", issues)
            require(
                receipt.get("kind") == "ordivon.computer-responsibility-reform-acceptance",
                "Computer reform receipt kind differs",
                issues,
            )
            require(receipt.get("acceptanceId") == "ACR-M1-C1-ACCEPT-001", "Computer reform receipt identity differs", issues)
            require(receipt.get("mapId") == "ACR-M1-001", "Computer reform receipt map identity differs", issues)
            require(receipt.get("cleanAcceptance") is True, "Computer reform receipt is not a clean acceptance", issues)
            require(receipt.get("integrity", {}).get("payloadDigest") == canonical_digest(receipt), "Computer reform receipt payload digest differs", issues)

            implementation = receipt.get("implementationRevision")
            require(isinstance(implementation, str) and len(implementation) == 40, "Computer reform implementation revision is invalid", issues)
            files = receipt.get("implementationFiles")
            require(isinstance(files, dict) and bool(files), "Computer reform implementation file bindings are missing", issues)
            if isinstance(implementation, str) and isinstance(files, dict):
                historical_map = subprocess.run(
                    ["git", "-C", str(ROOT), "show", f"{implementation}:research/computer-responsibility-map-v1.json"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
                )
                require(historical_map.returncode == 0, "Computer reform historical map is not recoverable", issues)
                if historical_map.returncode == 0:
                    try:
                        historical_document = json.loads(historical_map.stdout)
                    except json.JSONDecodeError:
                        issues.append("Computer reform historical map is invalid JSON")
                    else:
                        require(
                            receipt.get("mapPayloadDigest") == historical_document.get("integrity", {}).get("payloadDigest"),
                            "Computer reform receipt historical map digest differs",
                            issues,
                        )
                for relative, expected_digest in files.items():
                    completed = subprocess.run(
                        ["git", "-C", str(ROOT), "show", f"{implementation}:{relative}"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    require(completed.returncode == 0, f"Computer reform implementation file is not recoverable: {relative}", issues)
                    if completed.returncode == 0:
                        actual = "sha256:" + hashlib.sha256(completed.stdout).hexdigest()
                        require(actual == expected_digest, f"Computer reform implementation file digest differs: {relative}", issues)

            conformance = receipt.get("conformance")
            require(isinstance(conformance, dict), "Computer reform conformance summary is missing", issues)
            if isinstance(conformance, dict):
                require(conformance.get("status") == "passed", "Computer reform clean conformance did not pass", issues)
                steps = conformance.get("steps")
                require(isinstance(steps, list) and bool(steps), "Computer reform conformance steps are missing", issues)
                if isinstance(steps, list):
                    require(all(isinstance(step, dict) and step.get("exitCode") == 0 for step in steps), "Computer reform receipt contains a failed conformance step", issues)
                    step_ids = {step.get("id") for step in steps if isinstance(step, dict)}
                    for required_step in {
                        "foundational-docs",
                        "agent-research-method",
                        "computer-responsibility-map",
                        "historical-research-compression",
                        "task-continuation",
                        "track-r-evaluation",
                        "rust-canonical-vectors",
                    }:
                        require(required_step in step_ids, f"Computer reform receipt omits gate step: {required_step}", issues)

            limits = set(receipt.get("doesNotAuthorize", []))
            for required_limit in {
                "B5_Trial006",
                "additional_DeepSeek_canaries",
                "B6_implementation",
                "Prime_or_TCG_implementation",
                "Host_Harness_Runtime_merge",
                "product_repository_refactor",
                "new_World_Memory_Graph_or_Organization_platform",
            }:
                require(required_limit in limits, f"Computer reform receipt lost non-authorization: {required_limit}", issues)

    return sorted(set(issues))


def main() -> int:
    issues = check()
    print(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "ordivon-computer-responsibility-map-check",
                "ok": not issues,
                "issues": issues,
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
