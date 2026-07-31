#!/usr/bin/env python3
"""Validate one immutable Ordivon Protocol release manifest."""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
REVISION = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_STABILITY = {"release-candidate", "reference-candidate", "deprecated"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact(value: dict[str, Any], fields: set[str], label: str) -> None:
    require(set(value) == fields, f"{label} fields differ: {sorted(set(value) ^ fields)}")


def digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def relative_path(value: str, label: str) -> PurePosixPath:
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts, f"{label} must be relative")
    return path


def load_release_path(root: Path = ROOT) -> tuple[dict[str, Any], Path]:
    conformance = tomllib.loads((root / "projects" / "conformance.toml").read_text())
    protocol = conformance["protocol"]
    require("release" in protocol, "protocol release manifest is not declared")
    release = root / relative_path(protocol["release"], "protocol release")
    require(release.is_file(), "protocol release manifest is missing")
    return conformance, release


def validate(root: Path = ROOT) -> dict[str, Any]:
    conformance, release_path = load_release_path(root)
    document = json.loads(release_path.read_text(encoding="utf-8"))
    require(isinstance(document, dict), "protocol release must be an object")
    exact(
        document,
        {
            "schemaVersion",
            "kind",
            "package",
            "version",
            "releaseTag",
            "status",
            "profiles",
            "artifacts",
            "consumers",
            "promotionEvidence",
            "constraintAdmission",
            "supersessionTrigger",
        },
        "protocol release",
    )
    require(document["schemaVersion"] == 1, "unsupported protocol release schema")
    require(document["kind"] == "ordivon.protocol-release", "invalid protocol release kind")
    protocol = conformance["protocol"]
    require(document["package"] == protocol["package"], "release package differs")
    require(document["version"] == protocol["version"], "release version differs")
    require(document["releaseTag"] == f"ordivon-protocol-v{document['version']}", "release tag differs")
    require(document["status"] == "released", "protocol release status must be released")

    profiles = document["profiles"]
    require(isinstance(profiles, list) and profiles, "release profiles must be non-empty")
    profile_ids: list[str] = []
    for profile in profiles:
        require(isinstance(profile, dict), "profile declaration must be an object")
        exact(profile, {"id", "stability", "scope", "limitations", "consumers"}, "profile declaration")
        profile_id = profile["id"]
        require(isinstance(profile_id, str) and profile_id, "profile id is required")
        profile_ids.append(profile_id)
        require(profile["stability"] in ALLOWED_STABILITY, f"invalid stability: {profile_id}")
        require(bool(str(profile["scope"]).strip()), f"profile scope is missing: {profile_id}")
        require(isinstance(profile["limitations"], list), f"profile limitations must be a list: {profile_id}")
        require(isinstance(profile["consumers"], list), f"profile consumers must be a list: {profile_id}")
    require(len(profile_ids) == len(set(profile_ids)), "release profile ids must be unique")
    require(profile_ids == protocol["profiles"], "release profile order differs from conformance")
    host_profile = next(item for item in profiles if item["id"] == "host-workload-v1")
    limitation_text = " ".join(host_profile["limitations"]).lower()
    require("bounded" in limitation_text and "open" in limitation_text, "Host workload limitation must distinguish bounded and open cognition")

    package_root = root / protocol["source"]
    artifacts = document["artifacts"]
    require(isinstance(artifacts, list) and artifacts, "release artifacts must be non-empty")
    artifact_paths: list[str] = []
    package_parts = PurePosixPath(protocol["source"]).parts
    for artifact in artifacts:
        require(isinstance(artifact, dict), "artifact declaration must be an object")
        exact(artifact, {"path", "kind", "digest"}, "release artifact")
        path = relative_path(artifact["path"], "release artifact path")
        require(path.parts[: len(package_parts)] == package_parts, "release artifact escapes package source")
        source = root / path
        require(source.is_file(), f"release artifact is missing: {path}")
        require(bool(DIGEST.fullmatch(artifact["digest"])), f"invalid release artifact digest: {path}")
        require(digest(source.read_bytes()) == artifact["digest"], f"release artifact digest differs: {path}")
        artifact_paths.append(path.as_posix())
    require(len(artifact_paths) == len(set(artifact_paths)), "release artifact paths must be unique")
    normative_root = package_root / "src" / "ordivon_protocol"
    expected = sorted(
        path.relative_to(root).as_posix()
        for directory in (normative_root / "schemas", normative_root / "vectors")
        for path in directory.glob("*")
        if path.is_file()
    )
    require(sorted(artifact_paths) == expected, "release artifacts differ from packaged Schemas and vectors")

    consumers = document["consumers"]
    require(isinstance(consumers, list) and consumers, "release consumers must be non-empty")
    consumer_ids: list[str] = []
    for consumer in consumers:
        require(isinstance(consumer, dict), "consumer declaration must be an object")
        exact(consumer, {"repositoryId", "observedRevision", "protocolRevision", "profiles", "evidence"}, "consumer declaration")
        consumer_ids.append(consumer["repositoryId"])
        require(bool(REVISION.fullmatch(consumer["observedRevision"])), "consumer observedRevision is invalid")
        require(bool(REVISION.fullmatch(consumer["protocolRevision"])), "consumer protocolRevision is invalid")
        require(set(consumer["profiles"]) <= set(profile_ids), "consumer references unknown profile")
        require(isinstance(consumer["evidence"], list) and consumer["evidence"], "consumer evidence is required")
    require(len(consumer_ids) == len(set(consumer_ids)), "release consumer ids must be unique")
    require({"ordivon-host", "ordivon-game"} <= set(consumer_ids), "Host and Game release consumers are required")

    promotion = document["promotionEvidence"]
    require(isinstance(promotion, list) and promotion, "promotion evidence is required")
    for item in promotion:
        require(isinstance(item, str) and (root / item).exists(), f"promotion evidence is missing: {item}")

    admission = document["constraintAdmission"]
    require(isinstance(admission, dict), "constraintAdmission must be an object")
    exact(admission, {"protectedFailure", "operatingCost", "deletionTrigger", "rejectedAlternatives"}, "constraintAdmission")
    for field in ("protectedFailure", "operatingCost", "deletionTrigger"):
        require(bool(str(admission[field]).strip()), f"constraintAdmission {field} is required")
    require(isinstance(admission["rejectedAlternatives"], list), "rejectedAlternatives must be a list")
    require(bool(str(document["supersessionTrigger"]).strip()), "supersessionTrigger is required")
    return document


def main() -> int:
    try:
        document = validate()
    except (OSError, ValueError, KeyError, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
        print(json.dumps({"schemaVersion": 1, "kind": "ordivon.protocol-release-check", "ok": False, "error": str(error)}, indent=2))
        return 1
    print(json.dumps({"schemaVersion": 1, "kind": "ordivon.protocol-release-check", "ok": True, "version": document["version"], "profiles": len(document["profiles"]), "artifacts": len(document["artifacts"]), "consumers": [item["repositoryId"] for item in document["consumers"]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
