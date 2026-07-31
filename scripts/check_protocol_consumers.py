#!/usr/bin/env python3
"""Run the bounded cross-repository Ordivon Protocol consumer gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PIN = re.compile(r"ordivon-computing\.git@([0-9a-f]{40})#subdirectory=packages/ordivon-protocol")
REVISION = re.compile(r"^[0-9a-f]{40}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise ValueError(
            f"command failed ({result.returncode}) in {cwd}: {' '.join(command)}\n{result.stdout}\n{result.stderr}"
        )
    return result


def git(root: Path, *args: str) -> str:
    return run(["git", "-C", str(root), *args], cwd=root).stdout.strip()


def git_bytes(root: Path, revision: str, path: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{path}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(result.returncode == 0, f"cannot read {path} at {revision} in {root}")
    return result.stdout


def sha256(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def integrity(document: dict[str, Any]) -> dict[str, str]:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return {"algorithm": "sha256", "canonicalization": "json-sort-keys-v1", "payloadDigest": sha256(encoded)}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_repository(root: Path, expected_name: str) -> str:
    require(root.is_dir(), f"repository is missing: {root}")
    revision = git(root, "rev-parse", "HEAD")
    require(bool(REVISION.fullmatch(revision)), f"invalid revision: {expected_name}")
    require(not git(root, "status", "--porcelain=v1"), f"repository is dirty: {expected_name}")
    return revision


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--computing-root", type=Path, required=True)
    parser.add_argument("--host-root", type=Path, required=True)
    parser.add_argument("--game-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    computing = args.computing_root.resolve()
    host = args.host_root.resolve()
    game = args.game_root.resolve()
    started = time.monotonic()
    steps: list[dict[str, Any]] = []
    try:
        revisions = {
            "ordivon-computing": validate_repository(computing, "ordivon-computing"),
            "ordivon-host": validate_repository(host, "ordivon-host"),
            "ordivon-game": validate_repository(game, "ordivon-game"),
        }
        conformance = tomllib.loads((computing / "projects" / "conformance.toml").read_text())
        release_path = computing / conformance["protocol"]["release"]
        release = json.loads(release_path.read_text())
        release_artifacts = {item["path"]: item["digest"] for item in release["artifacts"]}

        host_pyproject = (host / "pyproject.toml").read_text()
        matches = PIN.findall(host_pyproject)
        require(len(matches) == 1, "Host must contain exactly one full protocol pin")
        host_pin = matches[0]
        package_manifest = tomllib.loads(
            git_bytes(computing, host_pin, "packages/ordivon-protocol/pyproject.toml").decode("utf-8")
        )
        require(package_manifest["project"]["version"] == release["version"], "Host pin resolves to another protocol version")
        for path, expected in release_artifacts.items():
            require(sha256(git_bytes(computing, host_pin, path)) == expected, f"Host pin differs from released artifact: {path}")
        steps.append({"id": "host-pin", "status": "passed", "protocolRevision": host_pin})

        game_manifest = json.loads((game / "fixtures" / "host-workload-v1" / "manifest.json").read_text())
        require(game_manifest["protocolVersion"] == release["version"], "Game protocol version differs")
        game_pin = game_manifest["sourceRevision"]
        require(bool(REVISION.fullmatch(game_pin)), "Game sourceRevision is invalid")
        vector_path = game_manifest["sourcePath"]
        vector_bytes = git_bytes(computing, game_pin, vector_path)
        require(sha256(vector_bytes) == game_manifest["vectorFileDigest"], "Game source vector digest differs")
        require(sha256((game / "fixtures" / "host-workload-v1" / "vectors.json").read_bytes()) == game_manifest["vectorFileDigest"], "Game frozen vectors differ from manifest")
        require(release_artifacts[vector_path] == game_manifest["vectorFileDigest"], "Game vectors differ from released vectors")
        steps.append({"id": "game-vector-pin", "status": "passed", "protocolRevision": game_pin})

        host_started = time.monotonic()
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join(
            [str(computing / "packages" / "ordivon-protocol" / "src"), str(host / "src")]
        )
        host_result = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=host, env=environment)
        steps.append({"id": "host-tests", "status": "passed", "elapsedMs": round((time.monotonic() - host_started) * 1000), "summary": host_result.stderr.strip().splitlines()[-1:]})

        node = shutil.which("node")
        require(node is not None, "node is required for Game consumer tests")
        game_started = time.monotonic()
        game_result = run([node, "--test", "test/host-contract-vectors.test.ts"], cwd=game)
        steps.append({"id": "game-vector-tests", "status": "passed", "elapsedMs": round((time.monotonic() - game_started) * 1000), "summary": game_result.stdout.strip().splitlines()[-3:]})
        status = "passed"
        error = None
    except (OSError, ValueError, KeyError, json.JSONDecodeError, tomllib.TOMLDecodeError) as caught:
        status = "failed"
        error = str(caught)

    document: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.protocol-consumer-gate",
        "capturedAt": utc_now(),
        "status": status,
        "releaseVersion": locals().get("release", {}).get("version"),
        "repositories": locals().get("revisions", {}),
        "steps": steps,
        "error": error,
        "elapsedMs": round((time.monotonic() - started) * 1000),
    }
    document["integrity"] = integrity(document)
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(document, indent=2, ensure_ascii=False))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
