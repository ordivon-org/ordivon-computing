"""Cross-repository content baseline generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .check import check_repository, utc_now


def build_baseline(
    repository_parent: Path | None = None,
    pattern: str = "ordivon-*",
    repository_roots: list[Path] | None = None,
) -> dict[str, Any]:
    repositories: list[dict[str, Any]] = []
    if repository_roots:
        roots = sorted(path.expanduser().resolve() for path in repository_roots)
    elif repository_parent is not None:
        roots = sorted(repository_parent.expanduser().resolve().glob(pattern))
    else:
        raise ValueError("baseline requires repository_parent or repository_roots")
    for root in roots:
        if not (root / ".git").exists():
            continue
        receipt = check_repository(root, mode="advisory")
        repositories.append(
            {
                "projectId": receipt["projectId"],
                "path": str(root),
                "contentState": receipt["contentState"],
                "checkedDocuments": receipt["checkedDocuments"],
                "metadataDocuments": receipt["metadataDocuments"],
                "blockingFailures": receipt["blockingFailures"],
                "warnings": receipt["warnings"],
                "metrics": receipt["metrics"],
                "manifestPresent": (root / ".ordivon" / "project.yaml").is_file(),
            }
        )
    return {
        "schemaVersion": 1,
        "kind": "ordivon-content-baseline",
        "capturedAt": utc_now(),
        "repositoryParent": None if repository_parent is None else str(repository_parent.expanduser().resolve()),
        "repositories": repositories,
        "totals": {
            "repositories": len(repositories),
            "documents": sum(item["checkedDocuments"] for item in repositories),
            "metadataDocuments": sum(item["metadataDocuments"] for item in repositories),
            "words": sum(item["metrics"]["words"] for item in repositories),
            "documentsWithoutLinks": sum(item["metrics"]["documentsWithoutLinks"] for item in repositories),
            "longDocuments": sum(item["metrics"]["longDocuments"] for item in repositories),
            "warnings": sum(item["warnings"] for item in repositories),
        },
    }


def render_markdown(document: dict[str, Any]) -> str:
    total = document["totals"]
    updated = document["capturedAt"][:10]
    lines = [
        "---",
        "schema_version: 1",
        "id: computing.content-engineering.baseline",
        "title: Ordivon content engineering baseline",
        "type: report",
        "profile: research",
        "lifecycle: active",
        "source_role: evidence",
        "visibility: public",
        "owners:",
        "  - ordivon-computing",
        "audience:",
        "  - maintainer",
        "  - agent",
        f"updated: {updated}",
        "summary: Advisory structural inventory of the current Ordivon documentation corpus.",
        "evidence_status: observed",
        "readiness: DEGRADED",
        "applies_to:",
        "  - ordivon-project-family",
        "related:",
        "  - computing.content-engineering.p0",
        "---",
        "# Ordivon content engineering baseline",
        "",
        "## Executive judgment",
        "",
        "Ordivon has crossed the threshold where documentation must be treated as shared engineering infrastructure. This inventory remains advisory: counts expose migration pressure but do not authorize rewriting, deletion, or promotion.",
        "",
        "## Question",
        "",
        "What structural documentation debt exists across the active Ordivon repositories before any large-scale text migration begins?",
        "",
        "## Method",
        "",
        "The dependency-free content checker scanned Git-tracked and unignored Markdown or MDX files under each repository's declared documentation roots. It counted metadata adoption, approximate words, Markdown links, long documents, and structural warnings. It did not judge claim truth or prose quality.",
        "",
        "## Findings",
        "",
        "### System summary",
        "",
        f"- Repositories: {total['repositories']}",
        f"- Markdown/MDX documents: {total['documents']}",
        f"- Documents with Ordivon metadata: {total['metadataDocuments']}",
        f"- Approximate words: {total['words']}",
        f"- Documents without Markdown links: {total['documentsWithoutLinks']}",
        f"- Documents at or above 2,000 words: {total['longDocuments']}",
        "",
        "### Repository inventory",
        "",
        "| Project | Documents | Metadata | Words | No links | Long | Manifest | State |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for item in document["repositories"]:
        metrics = item["metrics"]
        lines.append(
            f"| {item['projectId']} | {item['checkedDocuments']} | {item['metadataDocuments']} | "
            f"{metrics['words']} | {metrics['documentsWithoutLinks']} | {metrics['longDocuments']} | "
            f"{'yes' if item['manifestPresent'] else 'no'} | {item['contentState']} |"
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "Word count, link count, paragraph length, and phase-code detection are diagnostic proxies. A long or link-free document may be correct and useful. The baseline does not establish factual accuracy, citation support, reader comprehension, or whether any specific document should survive.",
            "",
            "## Evidence",
            "",
            f"The machine-readable sibling receipt records the same inventory at `{document['capturedAt']}`. Repository manifests were validated before inclusion.",
            "",
            "## Next action",
            "",
            "Admit only high-authority paths into strict management, starting with current architecture, active research questions, accepted decisions, operations, and flagship public reports. Do not bulk-convert the historical corpus.",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
