#!/usr/bin/env python3
"""Validate the Ordivon research portfolio without network access."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "research" / "portfolio.json"
QUESTION_ID = re.compile(r"^(ANC-[A-Z]+-\d+)")


def _require(condition: bool, message: str, issues: list[str]) -> None:
    if not condition:
        issues.append(message)


def load_portfolio(path: Path = PORTFOLIO) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_portfolio(root: Path = ROOT, path: Path | None = None) -> list[str]:
    path = path or root / "research" / "portfolio.json"
    issues: list[str] = []
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"research portfolio cannot be loaded: {error}"]

    _require(document.get("schemaVersion") == 1, "unsupported portfolio schema", issues)
    _require(document.get("portfolio") == "ordivon-research", "invalid portfolio identity", issues)
    _require(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", document.get("asOf", ""))), "invalid portfolio asOf date", issues)

    policy = document.get("policy", {})
    allowed = set(policy.get("allowedStatuses", []))
    maturity = set(policy.get("maturityLevels", {}))
    active_limit = policy.get("activeLineLimit")
    _require(isinstance(active_limit, int) and active_limit > 0, "activeLineLimit must be positive", issues)

    lines = document.get("activeLines", [])
    _require(isinstance(lines, list), "activeLines must be a list", issues)
    if isinstance(active_limit, int):
        _require(len(lines) <= active_limit, "active research-line WIP limit exceeded", issues)
    line_ids = [line.get("id") for line in lines]
    _require(len(line_ids) == len(set(line_ids)), "active line ids must be unique", issues)

    questions = document.get("questions", [])
    _require(isinstance(questions, list) and questions, "questions must be non-empty", issues)
    question_ids = [question.get("id") for question in questions]
    _require(len(question_ids) == len(set(question_ids)), "question ids must be unique", issues)
    by_id = {question.get("id"): question for question in questions}

    active_members: list[str] = []
    for line in lines:
        _require(line.get("priority") in {"P0", "P1", "P2", "P3"}, f"invalid priority for line {line.get('id')}", issues)
        members = line.get("questions", [])
        _require(isinstance(members, list) and members, f"active line {line.get('id')} has no questions", issues)
        for question_id in members:
            active_members.append(question_id)
            question = by_id.get(question_id)
            _require(question is not None, f"active line references unknown question: {question_id}", issues)
            if question is not None:
                _require(question.get("status") == "active", f"active line question is not active: {question_id}", issues)
                _require(question.get("activeLine") == line.get("id"), f"activeLine mismatch: {question_id}", issues)
    _require(len(active_members) == len(set(active_members)), "question appears in multiple active lines", issues)

    required_fields = {
        "id", "title", "status", "maturity", "priority", "owner", "source",
        "blockedBy", "nextFalsifier", "nextAction", "disposition", "evidence"
    }
    for question in questions:
        question_id = question.get("id", "<missing>")
        _require(required_fields <= set(question), f"question fields are incomplete: {question_id}", issues)
        _require(question.get("status") in allowed, f"invalid status for {question_id}", issues)
        _require(question.get("maturity") in maturity, f"invalid maturity for {question_id}", issues)
        _require(question.get("priority") in {"P0", "P1", "P2", "P3", "reference"}, f"invalid priority for {question_id}", issues)
        _require(isinstance(question.get("blockedBy"), list), f"blockedBy must be a list: {question_id}", issues)
        _require(bool(question.get("nextFalsifier")), f"nextFalsifier is missing: {question_id}", issues)
        _require(bool(question.get("nextAction")), f"nextAction is missing: {question_id}", issues)
        if question.get("status") == "active":
            _require(question_id in active_members, f"active question lacks active line: {question_id}", issues)
        if question.get("status") == "blocked":
            _require(bool(question.get("blockedBy")), f"blocked question has no blocker: {question_id}", issues)
        if question.get("status") == "superseded":
            _require(bool(question.get("supersededBy")), f"superseded question lacks successor: {question_id}", issues)
        source = question.get("source", "")
        if isinstance(source, str) and not source.startswith("github:"):
            _require((root / source).is_file(), f"question source is missing: {question_id} -> {source}", issues)
        for evidence in question.get("evidence", []):
            _require((root / evidence).exists(), f"evidence reference is missing: {question_id} -> {evidence}", issues)

    file_question_ids: set[str] = set()
    for question_path in (root / "research" / "questions").glob("*.md"):
        match = QUESTION_ID.match(question_path.name)
        if match:
            file_question_ids.add(match.group(1))
    missing = sorted(file_question_ids - set(question_ids))
    _require(not missing, "question files missing from portfolio: " + ", ".join(missing), issues)

    for study in document.get("studies", []):
        study_id = study.get("id", "<missing>")
        _require(study.get("status") in allowed, f"invalid study status: {study_id}", issues)
        _require((root / "studies" / study_id).is_dir(), f"study directory is missing: {study_id}", issues)
        _require(bool(study.get("nextAction")), f"study nextAction is missing: {study_id}", issues)

    program_issues = [program.get("issue") for program in document.get("programs", [])]
    _require(len(program_issues) == len(set(program_issues)), "program issue ids must be unique", issues)
    for program in document.get("programs", []):
        _require(program.get("status") in allowed, f"invalid program status: {program.get('id')}", issues)
        _require(bool(program.get("nextAction")), f"program nextAction is missing: {program.get('id')}", issues)

    return sorted(set(issues))


def main() -> int:
    issues = check_portfolio()
    output = {
        "schemaVersion": 1,
        "kind": "ordivon-research-portfolio-check",
        "ok": not issues,
        "issues": issues,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
