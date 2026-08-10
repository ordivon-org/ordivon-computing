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
    require(isinstance(method_ref, str) and bool(method_ref), "historical research method ref is invalid", issues)
    if isinstance(method_ref, str) and isinstance(source_revision, str):
        method = git("show", f"{source_revision}:{method_ref}")
        require(method.returncode == 0, f"historical research method is not Git-recoverable: {method_ref}", issues)
    require(isinstance(conclusion_ref, str) and bool(conclusion_ref), "durable conclusion ref is invalid", issues)
    if isinstance(conclusion_ref, str):
        require((ROOT / conclusion_ref).is_file(), f"durable conclusion ref is missing: {conclusion_ref}", issues)

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

    # Computer contraction C1 archives completed executable experiment apparatus
    # from the active tree while preserving exact Git recoverability.
    archive_path = ROOT / "research" / "evidence" / "computer-contraction-c1-active-tree-archive.json"
    if archive_path.is_file():
        try:
            archive = json.loads(archive_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            issues.append(f"active-tree archive manifest cannot be loaded: {error}")
        else:
            require(archive.get("schemaVersion") == 1, "active-tree archive schema differs", issues)
            require(archive.get("kind") == "ordivon.computer-active-tree-archive-manifest", "active-tree archive kind differs", issues)
            require(archive.get("archiveId") == "COMPUTER-CONTRACTION-C1", "active-tree archive identity differs", issues)
            require(archive.get("integrity", {}).get("payloadDigest") == canonical_digest(archive), "active-tree archive digest differs", issues)
            revision = archive.get("sourceRevision")
            require(isinstance(revision, str) and git("cat-file", "-e", f"{revision}^{{commit}}").returncode == 0, "active-tree archive source revision is unreachable", issues)
            rows = archive.get("files")
            require(isinstance(rows, list) and bool(rows), "active-tree archive file set is empty", issues)
            if isinstance(rows, list) and isinstance(revision, str):
                seen: set[str] = set()
                for item in rows:
                    if not isinstance(item, dict):
                        issues.append("active-tree archive entry is not an object")
                        continue
                    relative = item.get("path")
                    require(isinstance(relative, str) and relative.startswith("research/experiments/"), "active-tree archive path is invalid", issues)
                    if not isinstance(relative, str):
                        continue
                    require(relative not in seen, f"duplicate active-tree archive path: {relative}", issues)
                    seen.add(relative)
                    require(not (ROOT / relative).exists(), f"archived apparatus returned to active tree: {relative}", issues)
                    historical = git("show", f"{revision}:{relative}")
                    require(historical.returncode == 0, f"archived apparatus is not Git-recoverable: {relative}", issues)
                    if historical.returncode == 0:
                        content = historical.stdout.encode("utf-8")
                        digest = "sha256:" + hashlib.sha256(content).hexdigest()
                        require(digest == item.get("sha256"), f"archived apparatus digest differs: {relative}", issues)
                require(len(seen) == archive.get("removedFiles"), "active-tree archive file count differs", issues)
            utility = archive.get("extractedLiveUtility", {})
            current_utility = ROOT / str(utility.get("currentPath", ""))
            require(current_utility.is_file(), "extracted freshness utility is missing", issues)
            if current_utility.is_file():
                digest = "sha256:" + hashlib.sha256(current_utility.read_bytes()).hexdigest()
                require(digest == utility.get("sha256"), "extracted freshness utility digest differs", issues)

    return sorted(set(issues))


def main() -> int:
    issues = check()
    print(json.dumps({"schemaVersion": 1, "kind": "ordivon-historical-research-compression-check", "ok": not issues, "issues": issues}, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
