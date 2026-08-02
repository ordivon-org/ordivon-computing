"""Repository documentation checks for Ordivon content engineering P0."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit

from .contracts import find_contract_root, load_profiles, validate_document, validate_project
from .yaml_subset import loads as load_yaml_subset


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
WORD = re.compile(r"[A-Za-z0-9_'-]+|[\u4e00-\u9fff]")
PHASE_NAME = re.compile(r"(?:^|/)(?:[A-Z]{0,3}[0-9]+|P[0-9]+|R[0-9]+|E[0-9]+|H[0-9]+)[-_]", re.IGNORECASE)
EXCLUDED_PARTS = {".git", "node_modules", ".venv", "venv", "target", "dist", "build", "out", ".next"}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str
    line: int | None = None


@dataclass(frozen=True)
class DocumentRecord:
    path: str
    words: int
    links: int
    max_paragraph_words: int
    has_frontmatter: bool
    metadata_id: str | None
    source_role: str | None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_digest(document: dict[str, Any]) -> str:
    payload = json.dumps(document, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


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
    if completed.returncode == 0:
        return [
            root / item
            for item in completed.stdout.splitlines()
            if item.lower().endswith((".md", ".mdx")) and (root / item).is_file()
        ]
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".md", ".mdx"}
        and not (set(path.relative_to(root).parts) & EXCLUDED_PARTS)
    ]


def _under(path: PurePosixPath, declared: Iterable[str]) -> bool:
    for raw in declared:
        candidate = PurePosixPath(raw)
        if path == candidate or candidate in path.parents:
            return True
    return False


def _documentation_paths(root: Path, manifest: dict[str, Any]) -> list[Path]:
    return sorted(
        path
        for path in _git_documents(root)
        if _under(PurePosixPath(path.relative_to(root).as_posix()), manifest["documentation_roots"])
    )


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter is not terminated")
    raw = text[4:end]
    return load_yaml_subset(raw), text[end + 5 :]


def _paragraph_lengths(text: str) -> list[int]:
    lengths: list[int] = []
    for paragraph in re.split(r"\n\s*\n", text):
        stripped = paragraph.strip()
        if not stripped or stripped.startswith(("#", "- ", "* ", ">", "```", "|")):
            continue
        lengths.append(len(WORD.findall(re.sub(r"\s+", " ", stripped))))
    return lengths


def _line_for(text: str, fragment: str) -> int | None:
    index = text.find(fragment)
    return None if index < 0 else text.count("\n", 0, index) + 1


def _local_link_issues(root: Path, path: Path, text: str, severity: str) -> list[Issue]:
    issues: list[Issue] = []
    for match in MARKDOWN_LINK.finditer(text):
        raw = match.group(1).strip().strip("<>")
        if " \"" in raw:
            raw = raw.split(" \"", 1)[0]
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or raw.startswith(("#", "mailto:")):
            continue
        target_text = unquote(parsed.path)
        if not target_text:
            continue
        target = (path.parent / target_text).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            issues.append(Issue(severity, "LINK002", path.relative_to(root).as_posix(), f"relative link escapes repository: {raw}", _line_for(text, match.group(0))))
            continue
        if not target.exists():
            issues.append(Issue(severity, "LINK001", path.relative_to(root).as_posix(), f"broken relative link: {raw}", _line_for(text, match.group(0))))
    return issues


def _required_section_issues(
    root: Path,
    path: Path,
    body: str,
    metadata: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
) -> list[Issue]:
    issues: list[Issue] = []
    profile = profiles[metadata["profile"]]
    required = profile.get("types", {}).get(metadata["type"], {}).get("required_sections", [])
    headings = {title.strip().lower() for _, title in HEADING.findall(body)}
    for section in required:
        if section.lower() not in headings:
            issues.append(Issue("error", "DOC006", path.relative_to(root).as_posix(), f"required section is missing: {section}"))
    return issues


def check_repository(root: Path, mode: str | None = None) -> dict[str, Any]:
    root = root.expanduser().resolve()
    issues: list[Issue] = []
    try:
        manifest = load_project_manifest(root)
    except (OSError, ValueError) as error:
        project_id = root.name
        effective_mode = mode or "advisory"
        issues.append(Issue("error" if effective_mode == "strict" else "warning", "PROJECT001", ".ordivon/project.yaml", str(error)))
        manifest = {
            "id": project_id,
            "documentation_roots": ["README.md", "docs", "research", "studies", "core", "knowledge"],
            "managed_paths": [],
            "enforcement": effective_mode,
        }
    effective_mode = mode or manifest["enforcement"]
    if effective_mode not in {"advisory", "strict"}:
        raise ValueError(f"invalid check mode: {effective_mode}")
    contract_root = find_contract_root(Path(__file__))
    profiles = load_profiles(contract_root)
    records: list[DocumentRecord] = []
    ids: dict[str, str] = {}
    canonical_ids: dict[str, str] = {}
    documents = _documentation_paths(root, manifest)
    for path in documents:
        relative = PurePosixPath(path.relative_to(root).as_posix())
        managed = _under(relative, manifest.get("managed_paths", []))
        strict = effective_mode == "strict" and managed
        text = path.read_text(encoding="utf-8", errors="replace")
        headings = HEADING.findall(text)
        try:
            metadata, body = parse_frontmatter(text)
        except ValueError as error:
            issues.append(Issue("error", "DOC002", relative.as_posix(), str(error), 1))
            metadata, body = None, text
        if metadata is None:
            issues.append(Issue("error" if strict else "warning", "DOC001", relative.as_posix(), "document has no Ordivon metadata"))
        else:
            try:
                validate_document(metadata)
            except ValueError as error:
                issues.append(Issue("error", "DOC003", relative.as_posix(), str(error), 1))
            else:
                metadata_id = metadata["id"]
                if metadata_id in ids:
                    issues.append(Issue("error", "DOC004", relative.as_posix(), f"duplicate document id also used by {ids[metadata_id]}: {metadata_id}", 1))
                else:
                    ids[metadata_id] = relative.as_posix()
                if metadata["source_role"] == "canonical":
                    if metadata_id in canonical_ids:
                        issues.append(Issue("error", "DOC005", relative.as_posix(), f"duplicate canonical document id also used by {canonical_ids[metadata_id]}: {metadata_id}", 1))
                    canonical_ids[metadata_id] = relative.as_posix()
                issues.extend(_required_section_issues(root, path, body, metadata, profiles))
                h1 = [title for level, title in HEADING.findall(body) if len(level) == 1]
                if h1 and h1[0].strip() != metadata["title"].strip():
                    issues.append(Issue("error" if strict else "warning", "DOC007", relative.as_posix(), "front matter title differs from the first H1"))
        h1_count = sum(1 for level, _ in headings if len(level) == 1)
        if h1_count != 1:
            issues.append(Issue("error" if strict else "warning", "MD001", relative.as_posix(), f"expected exactly one H1, found {h1_count}"))
        paragraph_lengths = _paragraph_lengths(body)
        maximum = max(paragraph_lengths or [0])
        if maximum > 180:
            issues.append(Issue("warning", "STYLE001", relative.as_posix(), f"paragraph contains {maximum} words; review progressive disclosure"))
        links = len(MARKDOWN_LINK.findall(body))
        words = len(WORD.findall(body))
        if words >= 500 and links == 0:
            issues.append(Issue("warning", "NAV001", relative.as_posix(), "long document has no Markdown links"))
        if PHASE_NAME.search(relative.as_posix()):
            issues.append(Issue("warning", "LIFE001", relative.as_posix(), "phase or round code appears in the primary path; declare lifecycle metadata before promotion"))
        issues.extend(_local_link_issues(root, path, body, "error" if strict else "warning"))
        records.append(
            DocumentRecord(
                path=relative.as_posix(),
                words=words,
                links=links,
                max_paragraph_words=maximum,
                has_frontmatter=metadata is not None,
                metadata_id=None if metadata is None else metadata.get("id"),
                source_role=None if metadata is None else metadata.get("source_role"),
            )
        )
    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    state = "BLOCKED" if errors else "DEGRADED" if warnings else "READY"
    document: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon-content-check",
        "capturedAt": utc_now(),
        "projectId": manifest["id"],
        "repositoryRoot": str(root),
        "mode": effective_mode,
        "contentState": state,
        "checkedDocuments": len(records),
        "managedDocuments": sum(_under(PurePosixPath(record.path), manifest.get("managed_paths", [])) for record in records),
        "metadataDocuments": sum(record.has_frontmatter for record in records),
        "blockingFailures": errors,
        "warnings": warnings,
        "issues": [asdict(issue) for issue in sorted(issues, key=lambda item: (item.path, item.line or 0, item.code))],
        "tooling": {
            name: {"available": bool(path), "path": path}
            for name, path in (
                ("vale", shutil.which("vale")),
                ("markdownlint-cli2", shutil.which("markdownlint-cli2")),
                ("cspell", shutil.which("cspell")),
                ("lychee", shutil.which("lychee")),
            )
        },
        "metrics": {
            "words": sum(record.words for record in records),
            "documentsWithoutLinks": sum(record.links == 0 for record in records),
            "longDocuments": sum(record.words >= 2000 for record in records),
            "longestDocuments": [asdict(record) for record in sorted(records, key=lambda item: item.words, reverse=True)[:10]],
        },
    }
    document["receiptDigest"] = canonical_digest(document)
    return document
