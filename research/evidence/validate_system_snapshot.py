from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_REVISION = re.compile(r"^[0-9a-f]{40}$")
_SNAPSHOT_ID = re.compile(r"^(?!.*(?:current|latest))[a-z0-9][a-z0-9._:-]{2,127}$")


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


def bytes_digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def git_blob(root: Path, revision: str, path: PurePosixPath) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path.as_posix()}"],
        check=False,
        capture_output=True,
    )
    require(result.returncode == 0, f"cannot read historical Artifact: {path}")
    return result.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_unique(items: list[dict[str, Any]], label: str) -> set[str]:
    identifiers = [item.get("id") for item in items]
    require(len(identifiers) == len(set(identifiers)), f"duplicate {label} id")
    return {identifier for identifier in identifiers if isinstance(identifier, str)}


def validate(
    document: dict[str, Any], *, repository_roots: dict[str, Path] | None = None
) -> None:
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

    repository_ids = require_unique(repositories, "repository")
    repository_by_id = {repository["id"]: repository for repository in repositories}
    service_ids = require_unique(services, "service")
    contract_ids = require_unique(contracts, "contract")
    artifact_ids = require_unique(artifacts, "artifact")
    require(bool(service_ids | artifact_ids), "snapshot must bind service or Artifact evidence")

    repository_fields = {"id", "repository", "revision", "clean"}
    for repository in repositories:
        require(set(repository) == repository_fields, "repository fields are invalid")
        require(bool(repository.get("id")), "repository id is required")
        require(str(repository.get("repository", "")).startswith("https://"), "repository URI must use HTTPS")
        require(bool(_REVISION.fullmatch(repository.get("revision", ""))), "repository revision must be a full Git SHA")
        require(repository.get("clean") is True, "repository snapshot must be captured from a clean tree")

    service_fields = {
        "id",
        "sourceRepositoryId",
        "executable",
        "binaryDigest",
        "unitDigest",
        "observedState",
        "contractIds",
    }
    for service in services:
        require(set(service) <= service_fields, "service contains unknown fields")
        require(bool(service.get("id")), "service id is required")
        source_repository = service.get("sourceRepositoryId")
        require(source_repository in repository_ids, "service sourceRepositoryId is unknown")
        require(bool(service.get("executable")), "service executable is required")
        require(bool(_DIGEST.fullmatch(service.get("binaryDigest", ""))), "invalid service binaryDigest")
        if "unitDigest" in service:
            require(bool(_DIGEST.fullmatch(service["unitDigest"])), "invalid service unitDigest")
        require(service.get("observedState") in {"active", "inactive", "failed", "unknown"}, "invalid observedState")
        bound_contracts = service.get("contractIds")
        require(isinstance(bound_contracts, list), "service contractIds must be a list")
        require(len(bound_contracts) == len(set(bound_contracts)), "duplicate service contractId")
        require(set(bound_contracts) <= contract_ids, "service references unknown contract")

    contract_fields = {"id", "revision", "digest", "source"}
    for contract in contracts:
        require(set(contract) <= contract_fields, "contract contains unknown fields")
        require(bool(contract.get("id")), "contract id is required")
        revision = contract.get("revision")
        if revision is not None:
            lowered = str(revision).lower()
            require("current" not in lowered and "latest" not in lowered, "contract revision must be historical")
        require(bool(_DIGEST.fullmatch(contract.get("digest", ""))), "invalid contract digest")

    artifact_fields = {
        "id", "kind", "digest", "path", "repositoryId", "producedBy"
    }
    for artifact in artifacts:
        require(set(artifact) <= artifact_fields, "artifact contains unknown fields")
        require(bool(artifact.get("id")), "artifact id is required")
        require(bool(artifact.get("kind")), "artifact kind is required")
        require(bool(_DIGEST.fullmatch(artifact.get("digest", ""))), "invalid artifact digest")
        if "producedBy" in artifact:
            require(artifact["producedBy"] in service_ids, "artifact producedBy is unknown")
        if "path" in artifact:
            repository_id = artifact.get("repositoryId")
            require(repository_id in repository_ids, "artifact repositoryId is unknown")
            relative = PurePosixPath(artifact["path"])
            require(
                not relative.is_absolute() and ".." not in relative.parts,
                "artifact path must be normalized",
            )
            if repository_roots is not None and repository_id in repository_roots:
                revision = repository_by_id[repository_id]["revision"]
                content = git_blob(repository_roots[repository_id], revision, relative)
                require(
                    bytes_digest(content) == artifact["digest"],
                    f"artifact digest mismatch: {artifact['id']}",
                )

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
    parser.add_argument(
        "--repository-root",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="checkout used to verify historical path Artifacts",
    )
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[2]
    repository_roots = {
        "ordivon-architecture": repository_root,
        # Historical immutable snapshots retain the repository identity used when captured.
        "agent-native-computing": repository_root,
    }
    for binding in args.repository_root:
        repository_id, separator, raw_path = binding.partition("=")
        require(bool(separator and repository_id and raw_path), "repository root must use ID=PATH")
        repository_roots[repository_id] = Path(raw_path).resolve()

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
        validate(document, repository_roots=repository_roots)
        print(f"{path}: {document['snapshotId']} {document['integrity']['payloadDigest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
