#!/usr/bin/env python3
"""Validate the G0-G2 AI capability-governance foundation without network access."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

STUDY = Path(__file__).resolve().parents[1]
SCHEMAS = STUDY / "schemas"
EXAMPLES = STUDY / "examples"
REFERENCE_PATTERN = re.compile(r"\[(G\d{3})\]")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def issue(condition: bool, message: str, issues: list[str]) -> None:
    if not condition:
        issues.append(message)


def load_json(path: Path, issues: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        issues.append(f"cannot load JSON {path.relative_to(STUDY)}: {error}")
        return None


def check_schema_documents(issues: list[str]) -> dict[str, dict[str, Any]]:
    expected = {
        "case.schema.json",
        "policy-revision.schema.json",
        "enforcement-event.schema.json",
        "provider-observation.schema.json",
    }
    observed = {path.name for path in SCHEMAS.glob("*.schema.json")}
    issue(observed == expected, f"schema set differs: {sorted(observed)}", issues)
    values: dict[str, dict[str, Any]] = {}
    ids: list[str] = []
    for name in sorted(expected):
        value = load_json(SCHEMAS / name, issues)
        if not isinstance(value, dict):
            continue
        values[name] = value
        issue(
            value.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
            f"{name} does not use JSON Schema draft 2020-12",
            issues,
        )
        schema_id = value.get("$id")
        issue(isinstance(schema_id, str) and schema_id.startswith("https://ordivon.com/"), f"{name} has invalid $id", issues)
        if isinstance(schema_id, str):
            ids.append(schema_id)
        issue(value.get("type") == "object", f"{name} root is not an object", issues)
        issue(value.get("additionalProperties") is False, f"{name} root is not closed", issues)
        required = value.get("required")
        issue(isinstance(required, list) and bool(required), f"{name} has no required fields", issues)
        properties = value.get("properties")
        issue(isinstance(properties, dict), f"{name} has no properties", issues)
        if isinstance(required, list) and isinstance(properties, dict):
            missing = sorted(set(required) - set(properties))
            issue(not missing, f"{name} required fields absent from properties: {missing}", issues)
        schema_version = properties.get("schemaVersion") if isinstance(properties, dict) else None
        issue(isinstance(schema_version, dict) and schema_version.get("const") == 1, f"{name} lacks schemaVersion const 1", issues)
    issue(len(ids) == len(set(ids)), "schema $id values are not unique", issues)
    return values


def check_case_example(case_schema: dict[str, Any] | None, issues: list[str]) -> None:
    example_path = EXAMPLES / "hypothetical-capability-case.json"
    value = load_json(example_path, issues)
    if not isinstance(value, dict) or not isinstance(case_schema, dict):
        return
    required = case_schema.get("required", [])
    issue(set(required) <= set(value), "case example omits root required fields", issues)
    issue(value.get("schemaVersion") == 1, "case example schemaVersion differs", issues)
    issue(value.get("status") == "hypothetical", "case example must remain hypothetical", issues)
    case_id = value.get("caseId")
    issue(isinstance(case_id, str) and case_id.startswith("case:hypothetical:"), "case example identity differs", issues)

    collections = {
        "actors": "actorId",
        "resources": "resourceId",
        "claims": "claimId",
        "relations": "relationId",
    }
    identifiers: set[str] = set()
    for collection, field in collections.items():
        entries = value.get(collection)
        issue(isinstance(entries, list), f"case example {collection} is not an array", issues)
        if not isinstance(entries, list):
            continue
        ids = [entry.get(field) for entry in entries if isinstance(entry, dict)]
        issue(len(ids) == len(entries), f"case example {collection} contains non-object or missing identity", issues)
        issue(len(ids) == len(set(ids)), f"case example {collection} identities are not unique", issues)
        identifiers.update(item for item in ids if isinstance(item, str))

    for relation in value.get("relations", []):
        if not isinstance(relation, dict):
            continue
        issue(relation.get("subjectId") in identifiers, f"relation subject is unresolved: {relation.get('subjectId')}", issues)
        issue(relation.get("objectId") in identifiers, f"relation object is unresolved: {relation.get('objectId')}", issues)
        dimensions = relation.get("powerDimensions")
        issue(isinstance(dimensions, list) and bool(dimensions), f"relation has no power dimensions: {relation.get('relationId')}", issues)
        evidence = relation.get("evidenceRefs")
        issue(isinstance(evidence, list) and bool(evidence), f"relation has no evidence: {relation.get('relationId')}", issues)

    for claim in value.get("claims", []):
        if not isinstance(claim, dict):
            continue
        issue(claim.get("class") in {"D", "C", "N", "A"}, f"claim class differs: {claim.get('claimId')}", issues)
        issue(claim.get("confidence") in {"low", "medium", "high"}, f"claim confidence differs: {claim.get('claimId')}", issues)
        issue(bool(claim.get("falsifier")), f"claim lacks falsifier: {claim.get('claimId')}", issues)

    privacy = value.get("privacy")
    issue(isinstance(privacy, dict) and privacy.get("containsPersonalData") is False, "hypothetical example contains personal data", issues)


def check_references(issues: list[str]) -> None:
    reference_path = STUDY / "REFERENCES.md"
    text = reference_path.read_text(encoding="utf-8")
    defined = set(re.findall(r"^### \[(G\d{3})\]", text, re.MULTILINE))
    issue(len(defined) >= 20, f"reference ledger too small: {len(defined)}", issues)
    used: set[str] = set()
    for path in STUDY.rglob("*.md"):
        if path == reference_path:
            continue
        used.update(REFERENCE_PATTERN.findall(path.read_text(encoding="utf-8")))
    missing = sorted(used - defined)
    issue(not missing, f"undefined references: {missing}", issues)
    theory_files = sorted((STUDY / "theories").glob("*.md"))
    for path in theory_files:
        ids = set(REFERENCE_PATTERN.findall(path.read_text(encoding="utf-8")))
        issue(bool(ids), f"theory file has no primary reference: {path.name}", issues)


def check_local_links(issues: list[str]) -> None:
    for path in STUDY.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_text = target.split("#", 1)[0]
            if not path_text:
                continue
            resolved = (path.parent / path_text).resolve()
            try:
                resolved.relative_to(STUDY.resolve())
            except ValueError:
                # Links intentionally pointing to repository-local research data are valid.
                if resolved.exists():
                    continue
                issues.append(f"local link escapes study and is missing: {path.relative_to(STUDY)} -> {target}")
                continue
            issue(resolved.exists(), f"broken local link: {path.relative_to(STUDY)} -> {target}", issues)


def check_safety_and_scope(issues: list[str]) -> None:
    required_phrases = {
        "README.md": ["does **not** yet rank providers", "earns no new runtime service"],
        "00-scope-and-claim-boundaries.md": ["does not authorize evasion", "Admission and deletion rule"],
        "01-core-questions-and-falsifiers.md": ["No provider ranking", "Effect-level governance"],
        "20-power-grammar.md": ["not a universal", "No layer may claim another layer's fact"],
    }
    for relative, phrases in required_phrases.items():
        text = (STUDY / relative).read_text(encoding="utf-8")
        for phrase in phrases:
            issue(phrase in text, f"{relative} omits required boundary phrase: {phrase}", issues)

    forbidden_patterns = [
        re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{16,}"),
        re.compile(r"Bearer\s+[A-Za-z0-9._-]{16,}"),
    ]
    for path in STUDY.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".json", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            issue(pattern.search(text) is None, f"possible secret in {path.relative_to(STUDY)}", issues)


def main() -> int:
    issues: list[str] = []
    schemas = check_schema_documents(issues)
    check_case_example(schemas.get("case.schema.json"), issues)
    check_references(issues)
    check_local_links(issues)
    check_safety_and_scope(issues)
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.ai-capability-governance-g0-g2-validation",
        "ok": not issues,
        "study": str(STUDY),
        "schemaCount": len(schemas),
        "markdownCount": len(tuple(STUDY.rglob("*.md"))),
        "jsonCount": len(tuple(STUDY.rglob("*.json"))),
        "issues": sorted(set(issues)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
