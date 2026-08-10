#!/usr/bin/env python3
"""Validate the explicit unreleased Ordivon Protocol source candidate."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def digest(document: dict[str, Any]) -> str:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def check() -> list[str]:
    issues: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            issues.append(message)

    try:
        conformance = tomllib.loads((ROOT / "projects/conformance.toml").read_text())
        candidate_decl = conformance["protocol_candidate"]
        candidate_path = ROOT / candidate_decl["manifest"]
        candidate = json.loads(candidate_path.read_text())
        package = tomllib.loads((ROOT / "packages/ordivon-protocol/pyproject.toml").read_text())
        release = json.loads((ROOT / "packages/ordivon-protocol/releases/0.3.0.json").read_text())
    except (OSError, KeyError, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
        return [f"protocol candidate cannot be loaded: {error}"]

    require(candidate_decl.get("version") == "0.4.0.dev0", "candidate declaration version differs")
    require(candidate_decl.get("status") == "unreleased", "candidate declaration is not unreleased")
    require(candidate_decl.get("base_release") == "0.3.0", "candidate base release differs")
    require(candidate_decl.get("required_owner_admission") == ["ordivon-host"], "candidate owner-admission boundary differs")
    require(package["project"]["version"] == candidate_decl["version"], "current package version is not the declared candidate")

    require(candidate.get("schemaVersion") == 1, "candidate schema differs")
    require(candidate.get("kind") == "ordivon.protocol-candidate", "candidate kind differs")
    require(candidate.get("version") == candidate_decl["version"], "candidate manifest version differs")
    require(candidate.get("status") == "unreleased", "candidate manifest is not unreleased")
    require(candidate.get("automaticConsumerUpgrade") is False, "candidate may not auto-upgrade consumers")
    require(candidate.get("requiredOwnerAdmission") == ["ordivon-host"], "candidate manifest owner-admission boundary differs")
    require(candidate.get("integrity", {}).get("payloadDigest") == digest(candidate), "candidate manifest digest differs")
    require(not (ROOT / "packages/ordivon-protocol/releases/0.4.0.json").exists(), "unadmitted candidate was materialized as a 0.4 release")
    require(not (ROOT / "packages/ordivon-protocol/src/ordivon_semantics").exists(), "semantic-state implementation remains in current candidate source")

    base = candidate.get("baseRelease", {})
    require(base.get("version") == release.get("version") == "0.3.0", "candidate base release identity differs")
    revision = base.get("releaseRevision")
    expected_tree = base.get("semanticStateTree")
    if isinstance(revision, str):
        tree = git("rev-parse", f"{revision}:packages/ordivon-protocol/src/ordivon_semantics")
        require(tree.returncode == 0, "0.3 semantic-state tree is not Git-recoverable")
        if tree.returncode == 0:
            require(tree.stdout.decode().strip() == expected_tree, "0.3 semantic-state tree identity differs")
    else:
        issues.append("candidate base release revision is invalid")

    require(candidate.get("unchangedReleaseArtifacts") is True, "candidate does not preserve released artifact bytes")
    for artifact in release.get("artifacts", []):
        path = ROOT / artifact["path"]
        require(path.is_file(), f"released artifact is missing from candidate source: {artifact['path']}")
        if path.is_file():
            actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            require(actual == artifact["digest"], f"released artifact changed in candidate source: {artifact['path']}")

    evidence = candidate.get("compatibilityEvidence", [])
    require(isinstance(evidence, list) and bool(evidence), "candidate compatibility evidence is missing")
    for relative in evidence if isinstance(evidence, list) else []:
        require(isinstance(relative, str) and (ROOT / relative).is_file(), f"candidate evidence is missing: {relative}")
    return sorted(set(issues))


if __name__ == "__main__":
    issues = check()
    print(json.dumps({"schemaVersion": 1, "kind": "ordivon-protocol-candidate-check", "ok": not issues, "issues": issues}, indent=2, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if not issues else 1)
