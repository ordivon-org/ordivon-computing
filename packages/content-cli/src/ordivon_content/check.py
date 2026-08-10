"""Narrow managed-document metadata validation for Ordivon repositories."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .contracts import validate_document, validate_project
from .yaml_subset import loads as load_yaml_subset


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str
    line: int | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_digest(document: dict[str, Any]) -> str:
    encoded = json.dumps(document, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def load_project_manifest(root: Path) -> dict[str, Any]:
    path = root / ".ordivon" / "project.yaml"
    if not path.is_file():
        raise ValueError("missing .ordivon/project.yaml")
    document = load_yaml_subset(path.read_text(encoding="utf-8"))
    validate_project(document)
    return document


def _git_documents(root: Path) -> list[Path]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode != 0:
        return sorted(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".mdx"})
    return sorted(
        root / item
        for item in completed.stdout.splitlines()
        if item.lower().endswith((".md", ".mdx")) and (root / item).is_file()
    )


def _under(path: PurePosixPath, declared: Iterable[str]) -> bool:
    for raw in declared:
        candidate = PurePosixPath(raw)
        if path == candidate or candidate in path.parents:
            return True
    return False


def _documentation_paths(root: Path, manifest: dict[str, Any]) -> list[Path]:
    return [
        path
        for path in _git_documents(root)
        if _under(PurePosixPath(path.relative_to(root).as_posix()), manifest["documentation_roots"])
    ]


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter is not terminated")
    return load_yaml_subset(text[4:end]), text[end + 5 :]


def check_repository(root: Path, mode: str | None = None) -> dict[str, Any]:
    root = root.expanduser().resolve()
    manifest = load_project_manifest(root)
    effective_mode = mode or manifest["enforcement"]
    if effective_mode not in {"advisory", "strict"}:
        raise ValueError(f"invalid check mode: {effective_mode}")

    managed = manifest.get("managed_paths", [])
    documents = [
        path
        for path in _documentation_paths(root, manifest)
        if _under(PurePosixPath(path.relative_to(root).as_posix()), managed)
    ]
    issues: list[Issue] = []
    ids: dict[str, str] = {}
    canonical_ids: dict[str, str] = {}
    metadata_documents = 0
    severity = "error" if effective_mode == "strict" else "warning"

    for path in documents:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            metadata, _body = parse_frontmatter(text)
        except ValueError as error:
            issues.append(Issue(severity, "DOC002", relative, str(error), 1))
            continue
        if metadata is None:
            issues.append(Issue(severity, "DOC001", relative, "managed document has no Ordivon metadata", 1))
            continue
        metadata_documents += 1
        try:
            validate_document(metadata)
        except ValueError as error:
            issues.append(Issue(severity, "DOC003", relative, str(error), 1))
            continue
        metadata_id = metadata["id"]
        if metadata_id in ids:
            issues.append(Issue(severity, "DOC004", relative, f"duplicate managed document id also used by {ids[metadata_id]}: {metadata_id}", 1))
        else:
            ids[metadata_id] = relative
        if metadata["source_role"] == "canonical":
            if metadata_id in canonical_ids:
                issues.append(Issue(severity, "DOC005", relative, f"duplicate managed canonical id also used by {canonical_ids[metadata_id]}: {metadata_id}", 1))
            else:
                canonical_ids[metadata_id] = relative

    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    state = "BLOCKED" if errors else "DEGRADED" if warnings else "READY"
    receipt: dict[str, Any] = {
        "schemaVersion": 2,
        "kind": "ordivon-managed-metadata-check",
        "capturedAt": utc_now(),
        "projectId": manifest["id"],
        "repositoryRoot": str(root),
        "mode": effective_mode,
        "contentState": state,
        "checkedDocuments": len(documents),
        "managedDocuments": len(documents),
        "metadataDocuments": metadata_documents,
        "blockingFailures": errors,
        "warnings": warnings,
        "issues": [asdict(issue) for issue in sorted(issues, key=lambda item: (item.path, item.line or 0, item.code))],
    }
    receipt["receiptDigest"] = canonical_digest(receipt)
    return receipt
