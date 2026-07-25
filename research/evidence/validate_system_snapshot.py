from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_REVISION = re.compile(r"^[0-9a-f]{40}$")
_SNAPSHOT_ID = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,127}$")


def canonical_payload(document: dict[str, Any]) -> bytes:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def payload_digest(document: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_payload(document)).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_unique(items: list[dict[str, Any]], label: str) -> None:
    identifiers = [item.get("id") for item in items]
    require(len(identifiers) == len(set(identifiers)), f"duplicate {label} id")


def validate(document: dict[str, Any]) -> None:
    required = {
        "schemaVersion",
        "snapshotId",
        "capturedAt",
        "purpose",
        "repositories",
        "services",
        "contracts",
        "artifacts",
        "integrity",
    }
    allowed = required | {"supersedes", "environment"}
    require(set(document) >= required, "snapshot is missing required top-level fields")
    require(set(document) <= allowed, "snapshot contains unknown top-level fields")
    require(document["schemaVersion"] == 1, "unsupported schemaVersion")
    require(bool(_SNAPSHOT_ID.fullmatch(document["snapshotId"])), "invalid snapshotId")
    if "supersedes" in document:
        require(bool(_SNAPSHOT_ID.fullmatch(document["supersedes"])), "invalid supersedes")
        require(document["supersedes"] != document["snapshotId"], "snapshot cannot supersede itself")
    datetime.fromisoformat(document["capturedAt"].replace("Z", "+00:00"))
    require(bool(document["purpose"].strip()), "purpose is required")

    repositories = document["repositories"]
    services = document["services"]
    contracts = document["contracts"]
    artifacts = document["artifacts"]
    require(isinstance(repositories, list) and repositories, "repositories must be non-empty")
    require(isinstance(services, list), "services must be a list")
    require(isinstance(contracts, list), "contracts must be a list")
    require(isinstance(artifacts, list) and artifacts, "artifacts must be non-empty")
    for label, items in (
        ("repository", repositories),
        ("service", services),
        ("contract", contracts),
        ("artifact", artifacts),
    ):
        require_unique(items, label)

    for repository in repositories:
        require(bool(repository.get("id")), "repository id is required")
        require(str(repository.get("repository", "")).startswith("https://"), "repository URI must use HTTPS")
        require(bool(_REVISION.fullmatch(repository.get("revision", ""))), "repository revision must be a full Git SHA")
        require(repository.get("clean") is True, "repository snapshot must be captured from a clean tree")

    for service in services:
        require(bool(service.get("id")), "service id is required")
        require(bool(service.get("executable")), "service executable is required")
        require(bool(_DIGEST.fullmatch(service.get("binaryDigest", ""))), "invalid service binaryDigest")
        if "unitDigest" in service:
            require(bool(_DIGEST.fullmatch(service["unitDigest"])), "invalid service unitDigest")
        require(service.get("observedState") in {"active", "inactive", "failed", "unknown"}, "invalid observedState")

    for contract in contracts:
        require(bool(contract.get("id")), "contract id is required")
        require(bool(_DIGEST.fullmatch(contract.get("digest", ""))), "invalid contract digest")

    for artifact in artifacts:
        require(bool(artifact.get("id")), "artifact id is required")
        require(bool(artifact.get("kind")), "artifact kind is required")
        require(bool(_DIGEST.fullmatch(artifact.get("digest", ""))), "invalid artifact digest")

    integrity = document["integrity"]
    require(integrity.get("algorithm") == "sha256", "unsupported integrity algorithm")
    require(integrity.get("canonicalization") == "json-sort-keys-v1", "unsupported canonicalization")
    require(bool(_DIGEST.fullmatch(integrity.get("payloadDigest", ""))), "invalid payloadDigest")
    require(integrity["payloadDigest"] == payload_digest(document), "payloadDigest does not match canonical payload")


def load(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text())
    require(isinstance(document, dict), "snapshot root must be an object")
    return document


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate immutable system snapshots")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--write-digest", action="store_true")
    args = parser.parse_args()

    for path in args.paths:
        document = load(path)
        if args.write_digest:
            document.setdefault("integrity", {})
            document["integrity"] = {
                "algorithm": "sha256",
                "canonicalization": "json-sort-keys-v1",
                "payloadDigest": payload_digest(document),
            }
            path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
        validate(document)
        print(f"{path}: {document['snapshotId']} {document['integrity']['payloadDigest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
