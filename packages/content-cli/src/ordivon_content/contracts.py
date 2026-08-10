"""Minimal managed-document metadata contracts for Ordivon repositories."""

from __future__ import annotations

import re
from typing import Any

PROJECT_ID = re.compile(r"^ordivon-[a-z0-9-]+$")
DOCUMENT_ID = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
LIFECYCLES = {"draft", "review", "accepted", "active", "superseded", "deprecated", "archived"}
SOURCE_ROLES = {"canonical", "derived", "evidence", "historical", "generated"}
ENFORCEMENT = {"advisory", "strict"}


def _strings(value: Any, field: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        qualifier = "possibly empty" if allow_empty else "non-empty"
        raise ValueError(f"{field} must be a {qualifier} list")
    if not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field} entries must be non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} entries must be unique")
    return value


def validate_project(document: dict[str, Any]) -> None:
    required = {"schema_version", "id", "documentation_roots", "managed_paths", "enforcement"}
    missing = required - set(document)
    if missing:
        raise ValueError("project manifest missing fields: " + ", ".join(sorted(missing)))
    if document["schema_version"] != 1:
        raise ValueError("unsupported project manifest schema_version")
    if not isinstance(document["id"], str) or not PROJECT_ID.fullmatch(document["id"]):
        raise ValueError("project id must match ordivon-<name>")
    _strings(document["documentation_roots"], "documentation_roots")
    _strings(document["managed_paths"], "managed_paths", allow_empty=True)
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
    missing = required - set(document)
    if missing:
        raise ValueError("document metadata missing fields: " + ", ".join(sorted(missing)))
    if document["schema_version"] != 1:
        raise ValueError("unsupported document schema_version")
    if not isinstance(document["id"], str) or not DOCUMENT_ID.fullmatch(document["id"]):
        raise ValueError("document id has an invalid form")
    for field in ("title", "type", "profile", "visibility"):
        if not isinstance(document[field], str) or not document[field].strip():
            raise ValueError(f"{field} must be non-empty text")
    if document["lifecycle"] not in LIFECYCLES:
        raise ValueError(f"invalid document lifecycle: {document['lifecycle']}")
    if document["source_role"] not in SOURCE_ROLES:
        raise ValueError(f"invalid source_role: {document['source_role']}")
    _strings(document["owners"], "owners")
    _strings(document["audience"], "audience")
    if not isinstance(document["updated"], str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", document["updated"]):
        raise ValueError("updated must use YYYY-MM-DD")
