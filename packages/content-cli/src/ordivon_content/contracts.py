"""Load and validate Ordivon content contracts without third-party packages."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any


DOCUMENT_TYPES = {
    "start",
    "quickstart",
    "concept",
    "how-to",
    "reference",
    "architecture",
    "proposal",
    "decision",
    "operations",
    "troubleshooting",
    "release",
    "deprecation",
    "question",
    "research-proposal",
    "protocol",
    "source-review",
    "experiment",
    "result",
    "report",
    "limitations",
    "closeout",
    "replication",
    "essay",
    "research-article",
    "engineering-report",
    "release-article",
    "short-finding",
    "position-paper",
    "correction",
    "capabilities",
    "configuration",
    "authentication",
    "security",
    "reliability",
    "limitations-reference",
    "examples",
    "compatibility",
}
PROFILES = {"engineering", "research", "publication", "provider", "organization"}
LIFECYCLES = {"draft", "review", "accepted", "active", "superseded", "deprecated", "archived"}
SOURCE_ROLES = {"canonical", "derived", "evidence", "historical", "generated"}
VISIBILITIES = {"public", "internal", "private"}
EVIDENCE_STATES = {"hypothesis", "observed", "verified", "refuted", "inconclusive", "not_applicable"}
READINESS_STATES = {"BLOCKED", "DEGRADED", "READY", "UNKNOWN", "not_applicable"}
PROJECT_KINDS = {"research", "engineering", "research-engineering", "publication", "adapter", "mixed"}
ENFORCEMENT = {"advisory", "strict"}
ID = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
PROJECT_ID = re.compile(r"^ordivon-[a-z0-9-]+$")


def find_contract_root(start: Path) -> Path:
    override = os.environ.get("ORDIVON_CONTENT_CONTRACT")
    if override:
        candidate = Path(override).expanduser().resolve()
        if (candidate / "schemas" / "document.schema.json").is_file():
            return candidate
        raise ValueError(f"ORDIVON_CONTENT_CONTRACT is invalid: {candidate}")
    for candidate in [start.resolve(), *start.resolve().parents]:
        direct = candidate / "packages" / "content-contract"
        if (direct / "schemas" / "document.schema.json").is_file():
            return direct
        if candidate.name == "content-cli":
            sibling = candidate.parent / "content-contract"
            if (sibling / "schemas" / "document.schema.json").is_file():
                return sibling
    raise ValueError("cannot locate packages/content-contract")


def load_profiles(contract_root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted((contract_root / "profiles").glob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        name = document.get("profile")
        if not isinstance(name, str) or name in result:
            raise ValueError(f"invalid or duplicate profile: {path}")
        result[name] = document
    missing = PROFILES - set(result)
    if missing:
        raise ValueError("missing content profiles: " + ", ".join(sorted(missing)))
    return result


def _strings(value: Any, field: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ValueError(f"{field} must be a {'possibly empty ' if allow_empty else 'non-empty '}list")
    if not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field} entries must be non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} entries must be unique")
    return value


def validate_project(document: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "id",
        "name",
        "repository",
        "kind",
        "default_profiles",
        "documentation_roots",
        "managed_paths",
        "enforcement",
        "maintainers",
    }
    optional = {"public_projection", "description"}
    unknown = set(document) - required - optional
    missing = required - set(document)
    if missing:
        raise ValueError("project manifest missing fields: " + ", ".join(sorted(missing)))
    if unknown:
        raise ValueError("project manifest has unknown fields: " + ", ".join(sorted(unknown)))
    if document["schema_version"] != 1:
        raise ValueError("unsupported project manifest schema_version")
    if not isinstance(document["id"], str) or not PROJECT_ID.fullmatch(document["id"]):
        raise ValueError("project id must match ordivon-<name>")
    if not isinstance(document["name"], str) or not document["name"].strip():
        raise ValueError("project name is required")
    if not isinstance(document["repository"], str) or not document["repository"].startswith("https://github.com/"):
        raise ValueError("project repository must be an https GitHub URL")
    if document["kind"] not in PROJECT_KINDS:
        raise ValueError(f"invalid project kind: {document['kind']}")
    profiles = _strings(document["default_profiles"], "default_profiles")
    invalid_profiles = set(profiles) - PROFILES
    if invalid_profiles:
        raise ValueError("invalid project profiles: " + ", ".join(sorted(invalid_profiles)))
    for field in ("documentation_roots", "managed_paths", "maintainers"):
        _strings(document[field], field, allow_empty=field == "managed_paths")
    if document["enforcement"] not in ENFORCEMENT:
        raise ValueError(f"invalid enforcement mode: {document['enforcement']}")


def validate_document(document: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "id",
        "title",
        "type",
        "profile",
        "lifecycle",
        "source_role",
        "visibility",
        "owners",
        "audience",
        "updated",
    }
    optional = {
        "summary",
        "evidence_status",
        "readiness",
        "applies_to",
        "supersedes",
        "related",
        "generated_from",
    }
    missing = required - set(document)
    unknown = set(document) - required - optional
    if missing:
        raise ValueError("document metadata missing fields: " + ", ".join(sorted(missing)))
    if unknown:
        raise ValueError("document metadata has unknown fields: " + ", ".join(sorted(unknown)))
    if document["schema_version"] != 1:
        raise ValueError("unsupported document schema_version")
    if not isinstance(document["id"], str) or not ID.fullmatch(document["id"]):
        raise ValueError("document id has an invalid form")
    if not isinstance(document["title"], str) or not document["title"].strip():
        raise ValueError("document title is required")
    if document["type"] not in DOCUMENT_TYPES:
        raise ValueError(f"invalid document type: {document['type']}")
    if document["profile"] not in PROFILES:
        raise ValueError(f"invalid document profile: {document['profile']}")
    if document["lifecycle"] not in LIFECYCLES:
        raise ValueError(f"invalid document lifecycle: {document['lifecycle']}")
    if document["source_role"] not in SOURCE_ROLES:
        raise ValueError(f"invalid source_role: {document['source_role']}")
    if document["visibility"] not in VISIBILITIES:
        raise ValueError(f"invalid visibility: {document['visibility']}")
    for field in ("owners", "audience"):
        _strings(document[field], field)
    for field in ("applies_to", "supersedes", "related", "generated_from"):
        if field in document:
            _strings(document[field], field, allow_empty=True)
    if "evidence_status" in document and document["evidence_status"] not in EVIDENCE_STATES:
        raise ValueError(f"invalid evidence_status: {document['evidence_status']}")
    if "readiness" in document and document["readiness"] not in READINESS_STATES:
        raise ValueError(f"invalid readiness: {document['readiness']}")
    if not isinstance(document["updated"], str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", document["updated"]):
        raise ValueError("updated must use YYYY-MM-DD")
