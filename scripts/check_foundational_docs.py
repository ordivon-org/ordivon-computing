#!/usr/bin/env python3
"""Validate foundational Ordivon Computing documents without network access."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REFERENCE = re.compile(r"\[([A-Z]\d{2})\]")
REFERENCE_HEADING = re.compile(r"^### ([A-Z]\d{2}) — ", re.MULTILINE)

SOURCE_LEDGER_STUDIES = (
    "2026-classical-to-agent-native-computing",
    "2026-adaptive-acceleration",
)

REQUIRED_PATHS = (
    "README.md",
    "core/README.md",
    "core/foundations.md",
    "core/stack.md",
    "core/primitives.md",
    "knowledge/computing/classical-substrate-and-agent-overlay.md",
    "knowledge/agents/probabilistic-work-control-loop.md",
    "knowledge/agents/task-context-authority-effect-evidence.md",
    "research/portfolio.json",
    "research/PORTFOLIO.md",
    "research/charters/README.md",
    "research/questions/ANC-STACK-001-classical-to-agent-native-transition.md",
    "studies/2026-classical-to-agent-native-computing/README.md",
    "studies/2026-classical-to-agent-native-computing/REFERENCES.md",
    "studies/2026-adaptive-acceleration/README.md",
    "studies/2026-adaptive-acceleration/ARTICLE.md",
    "studies/2026-adaptive-acceleration/PUBLICATION-DRAFT.md",
    "studies/2026-adaptive-acceleration/PUBLICATION-EDIT.md",
    "studies/2026-adaptive-acceleration/ARGUMENT-MAP.md",
    "studies/2026-adaptive-acceleration/REFERENCES.md",
)


def markdown_paths(root: Path) -> list[Path]:
    paths = [
        root / "README.md",
        root / "research" / "README.md",
        root / "research" / "PORTFOLIO.md",
        root / "research" / "charters" / "README.md",
    ]
    for directory in (
        root / "core",
        root / "knowledge",
        root / "studies",
    ):
        paths.extend(sorted(directory.rglob("*.md")))
    paths.append(
        root
        / "research"
        / "questions"
        / "ANC-STACK-001-classical-to-agent-native-transition.md"
    )
    return sorted(set(paths))


def _link_target(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1]
    # Optional Markdown titles are not used by foundational documents. Splitting
    # protects a future simple title without turning it into a filesystem path.
    if " \"" in raw:
        raw = raw.split(" \"", 1)[0]
    return raw


def broken_relative_links(root: Path, paths: list[Path]) -> list[str]:
    issues: list[str] = []
    for path in paths:
        if not path.is_file():
            issues.append(f"missing foundational document: {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            raw = _link_target(match.group(1))
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
                issues.append(
                    f"link escapes repository: {path.relative_to(root)} -> {raw}"
                )
                continue
            if not target.exists():
                issues.append(
                    f"broken relative link: {path.relative_to(root)} -> {raw}"
                )
    return issues


def reference_issues(root: Path) -> list[str]:
    issues: list[str] = []
    for study_name in SOURCE_LEDGER_STUDIES:
        study = root / "studies" / study_name
        if not study.exists():
            continue
        ledger = study / "REFERENCES.md"
        if not ledger.is_file():
            issues.append(f"primary-source ledger is missing: {study_name}")
            continue
        declared = set(REFERENCE_HEADING.findall(ledger.read_text(encoding="utf-8")))
        if not declared:
            issues.append(
                f"primary-source ledger declares no reference identifiers: {study_name}"
            )
        used: set[str] = set()
        for path in sorted(study.glob("*.md")):
            if path == ledger:
                continue
            used.update(REFERENCE.findall(path.read_text(encoding="utf-8")))
        for identifier in sorted(used - declared):
            issues.append(
                f"undeclared primary-source reference in {study_name}: {identifier}"
            )
        if not used:
            issues.append(f"study uses no primary-source references: {study_name}")
    return issues


def architecture_issues(root: Path) -> list[str]:
    issues: list[str] = []
    stack = (root / "core" / "stack.md").read_text(encoding="utf-8")
    if "## 1. Inherited substrate map" not in stack:
        issues.append("core stack lacks inherited substrate map")
    if "## 2. Agent-native responsibility overlay" not in stack:
        issues.append("core stack lacks Agent-native responsibility overlay")

    for relative in ("README.md", "core/README.md", "core/stack.md"):
        text = (root / relative).read_text(encoding="utf-8").lower()
        if "fourteen-layer stack" in text or "fourteen vertical layers" in text:
            issues.append(f"obsolete single-stack wording remains in {relative}")

    for path in markdown_paths(root):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        if "idempotent identity" in text:
            issues.append(
                f"Effect identity is still conflated with idempotency in {path.relative_to(root)}"
            )

    active_alignment_paths = (
        "README.md",
        "core/README.md",
        "core/foundations.md",
        "core/stack.md",
        "core/primitives.md",
        "knowledge/agents/goal-task-effect.md",
        "knowledge/computing/classical-substrate-and-agent-overlay.md",
        "knowledge/institutions/plural-intelligence-organization.md",
        "research/questions/ANC-ORG-001-agent-native-organization.md",
        "research/questions/ANC-ADAPT-001-agent-era-capabilities.md",
    )
    obsolete_alignment_phrases = (
        "humans retain purpose and consequence ownership",
        "human purpose and consequence ownership",
        "human consequence owner",
        "semantic control layer between probabilistic cognition and classical computing",
        "final commitments remains explicitly human",
    )
    for relative in active_alignment_paths:
        text = (root / relative).read_text(encoding="utf-8").lower()
        for phrase in obsolete_alignment_phrases:
            if phrase in text:
                issues.append(
                    f"obsolete human-exclusive or control framing remains in {relative}: {phrase}"
                )

    foundations = (root / "core" / "foundations.md").read_text(encoding="utf-8")
    required_alignment_fragments = (
        "Purpose and commitment belong to identifiable participants",
        "Capability and consequence are separate dimensions",
        "Every durable constraint must prove net acceleration",
        "Cooperation must not require permanent domination",
        "verified improvement per unit time",
    )
    for fragment in required_alignment_fragments:
        if fragment not in foundations:
            issues.append(f"working foundations lack acceleration alignment: {fragment}")

    primitives = (root / "core" / "primitives.md").read_text(encoding="utf-8")
    for fragment in (
        "ActionProposal",
        "CapabilityProfile",
        "DecisionRequest",
        "Refusal and Exit",
    ):
        if fragment not in primitives:
            issues.append(f"core primitives lack plural-intelligence candidate: {fragment}")

    research_map = (root / "research" / "map.yaml").read_text(encoding="utf-8")
    required = (
        "schema_version: 3",
        "- id: ANC-STACK",
        "- id: ANC-STACK-001",
        "file: questions/ANC-STACK-001-classical-to-agent-native-transition.md",
        "responsibilities: [",
    )
    for fragment in required:
        if fragment not in research_map:
            issues.append(f"research map lacks required fragment: {fragment}")
    if re.search(r"^\s+layers:", research_map, re.MULTILINE):
        issues.append("research map still binds construction tracks to obsolete L-layers")
    return issues


def check_repository(root: Path = ROOT) -> list[str]:
    issues: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            issues.append(f"required path is missing: {relative}")
    paths = markdown_paths(root)
    issues.extend(broken_relative_links(root, paths))
    issues.extend(reference_issues(root))
    issues.extend(architecture_issues(root))
    return sorted(set(issues))


def main() -> int:
    issues = check_repository()
    document = {
        "schemaVersion": 1,
        "kind": "ordivon-foundational-docs-check",
        "checkedMarkdownFiles": len(markdown_paths(ROOT)),
        "ok": not issues,
        "issues": issues,
    }
    print(json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
