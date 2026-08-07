#!/usr/bin/env python3
"""Validate Agent-first historical research compression and Git recoverability."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "research" / "evidence" / "agent-first-historical-research-compression-f95d721.json"


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


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def require(condition: bool, message: str, issues: list[str]) -> None:
    if not condition:
        issues.append(message)


def check() -> list[str]:
    issues: list[str] = []
    try:
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"compression receipt cannot be loaded: {error}"]

    require(receipt.get("schemaVersion") == 1, "compression receipt schema differs", issues)
    require(
        receipt.get("kind") == "ordivon.agent-first-historical-research-compression",
        "compression receipt kind differs",
        issues,
    )
    require(receipt.get("compressionId") == "AFR-COMPRESS-001", "compression identity differs", issues)
    require(receipt.get("integrity", {}).get("payloadDigest") == canonical_digest(receipt), "compression receipt digest differs", issues)

    source_revision = receipt.get("sourceRevision")
    require(isinstance(source_revision, str) and len(source_revision) == 40, "compression source revision is invalid", issues)
    if isinstance(source_revision, str):
        require(git("cat-file", "-e", f"{source_revision}^{{commit}}").returncode == 0, "compression source revision is not reachable", issues)

    method_ref = receipt.get("researchMethodRef")
    conclusion_ref = receipt.get("durableConclusionRef")
    for label, relative in (("research method", method_ref), ("durable conclusion", conclusion_ref)):
        require(isinstance(relative, str) and bool(relative), f"{label} ref is invalid", issues)
        if isinstance(relative, str):
            require((ROOT / relative).is_file(), f"{label} ref is missing: {relative}", issues)

    removed = receipt.get("removedStudies")
    require(isinstance(removed, list) and bool(removed), "removed study set is empty", issues)
    removed_ids: set[str] = set()
    if isinstance(removed, list) and isinstance(source_revision, str):
        for item in removed:
            require(isinstance(item, dict), "removed study entry is not an object", issues)
            if not isinstance(item, dict):
                continue
            study_id = item.get("studyId")
            path = item.get("sourcePath")
            source_tree = item.get("sourceTree")
            require(isinstance(study_id, str) and bool(study_id), "removed study id is invalid", issues)
            if not isinstance(study_id, str):
                continue
            require(study_id not in removed_ids, f"duplicate removed study: {study_id}", issues)
            removed_ids.add(study_id)
            require(item.get("disposition") == "remove_from_current_tree_keep_in_git", f"invalid disposition: {study_id}", issues)
            require(item.get("sourceRevision") == source_revision, f"source revision drift: {study_id}", issues)
            require(path == f"studies/{study_id}", f"source path drift: {study_id}", issues)
            require(not (ROOT / "studies" / study_id).exists(), f"compressed study returned to current tree: {study_id}", issues)
            if isinstance(path, str):
                tree = git("rev-parse", f"{source_revision}:{path}")
                require(tree.returncode == 0, f"historical study is not recoverable from Git: {study_id}", issues)
                if tree.returncode == 0:
                    require(tree.stdout.strip() == source_tree, f"historical tree digest differs: {study_id}", issues)
                names = git("ls-tree", "-r", "--name-only", source_revision, path)
                require(names.returncode == 0, f"historical file list unavailable: {study_id}", issues)
                if names.returncode == 0:
                    file_count = len([line for line in names.stdout.splitlines() if line])
                    require(file_count == item.get("fileCount"), f"historical file count differs: {study_id}", issues)

    required_removed = {
        "2026-computing-stack-walkthrough",
        "2026-classical-to-agent-native-computing",
        "2026-scarcity-operability-and-paradigm-change",
        "2026-retention-default-inversion",
        "2026-agent-system-concept-system",
        "2026-model-to-work-and-ordivon-harness",
        "2026-linear-loop-to-temporal-cognitive-graph",
        "2026-task-to-world-interaction",
        "2026-agent-world-interface-overlay",
        "2026-ordivon-host-a-series-source-audit",
        "2026-ordivon-paradigm-reform",
    }
    require(removed_ids == required_removed, "compressed study set differs", issues)

    retained = receipt.get("retainedCurrentStudyClasses")
    require(isinstance(retained, list), "retained study classes are missing", issues)
    if isinstance(retained, list):
        for item in retained:
            if not isinstance(item, dict):
                issues.append("retained study entry is not an object")
                continue
            study_id = item.get("studyId")
            if isinstance(study_id, str):
                require((ROOT / "studies" / study_id).is_dir(), f"retained current study is missing: {study_id}", issues)

    # The one live TCG source audit must be byte-identical to the historical source.
    historical_audit = "studies/2026-linear-loop-to-temporal-cognitive-graph/evidence/source-audit-20260806.json"
    current_audit = ROOT / "research" / "evidence" / "observations" / "temporal-cognitive-source-audit-20260806.json"
    require(current_audit.is_file(), "relocated TCG source audit is missing", issues)
    if current_audit.is_file() and isinstance(source_revision, str):
        old = git("show", f"{source_revision}:{historical_audit}")
        require(old.returncode == 0, "historical TCG source audit is not recoverable", issues)
        if old.returncode == 0:
            require(current_audit.read_text(encoding="utf-8") == old.stdout, "relocated TCG source audit differs from historical evidence", issues)

    try:
        portfolio = json.loads((ROOT / "research" / "portfolio.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        issues.append(f"research portfolio cannot be loaded: {error}")
    else:
        current_studies = {item.get("id") for item in portfolio.get("studies", []) if isinstance(item, dict)}
        require(not (removed_ids & current_studies), "compressed studies remain in current research portfolio", issues)
        questions = {item.get("id"): item for item in portfolio.get("questions", []) if isinstance(item, dict)}
        tcg = questions.get("ANC-COMPILER-002", {})
        evidence = set(tcg.get("evidence", [])) if isinstance(tcg, dict) else set()
        require("research/evidence/observations/temporal-cognitive-source-audit-20260806.json" in evidence, "TCG live question lacks relocated exact source audit", issues)
        require(not any(str(item).startswith("studies/2026-linear-loop-to-temporal-cognitive-graph") for item in evidence), "TCG live question still depends on removed historical study", issues)

    policy = receipt.get("policy", {})
    retention_test = set(policy.get("retentionTest", [])) if isinstance(policy, dict) else set()
    for required in {
        "survives_material_model_improvement",
        "owns_or_explains_a_durable_responsibility",
        "has_a_current_consumer_or_live_falsifier",
        "cannot_be_recovered_more_cheaply_from_git_or_owner_native_evidence",
    }:
        require(required in retention_test, f"compression retention test is missing: {required}", issues)

    return sorted(set(issues))


def main() -> int:
    issues = check()
    print(json.dumps({"schemaVersion": 1, "kind": "ordivon-historical-research-compression-check", "ok": not issues, "issues": issues}, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
