#!/usr/bin/env python3
"""Run frozen-release and current-head Ordivon Protocol consumer gates."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

PIN = re.compile(r"ordivon-computing\.git@([0-9a-f]{40})#subdirectory=packages/ordivon-protocol")
REVISION = re.compile(r"^[0-9a-f]{40}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def run(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(
            f"command failed ({result.returncode}) in {cwd}: {' '.join(command)}\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return result


def git(root: Path, *args: str) -> str:
    return run(["git", "-C", str(root), *args], cwd=root).stdout.strip()


def git_bytes(root: Path, revision: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"cannot read {path} at {revision} in {root}")
    return result.stdout


def sha256(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def integrity(document: dict[str, Any]) -> dict[str, str]:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return {
        "algorithm": "sha256",
        "canonicalization": "json-sort-keys-v1",
        "payloadDigest": sha256(encoded),
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_repository(root: Path, expected_name: str) -> str:
    require(root.is_dir(), f"repository is missing: {root}")
    revision = git(root, "rev-parse", "HEAD")
    require(bool(REVISION.fullmatch(revision)), f"invalid revision: {expected_name}")
    require(not git(root, "status", "--porcelain=v1"), f"repository is dirty: {expected_name}")
    return revision


def protocol_pin(pyproject_text: str, label: str) -> str:
    matches = PIN.findall(pyproject_text)
    require(len(matches) == 1, f"{label} must contain exactly one full protocol pin")
    return matches[0]


def validate_protocol_revision(
    computing: Path,
    revision: str,
    *,
    release: dict[str, Any],
    release_artifacts: dict[str, str],
    label: str,
) -> None:
    require(bool(REVISION.fullmatch(revision)), f"{label} protocol revision is invalid")
    package_manifest = tomllib.loads(
        git_bytes(
            computing,
            revision,
            "packages/ordivon-protocol/pyproject.toml",
        ).decode("utf-8")
    )
    require(
        package_manifest["project"]["version"] == release["version"],
        f"{label} protocol pin resolves to another protocol version",
    )
    for path, expected in release_artifacts.items():
        require(
            sha256(git_bytes(computing, revision, path)) == expected,
            f"{label} protocol pin differs from released artifact: {path}",
        )


def validate_candidate_declaration(
    candidate_config: dict[str, Any],
    candidate: dict[str, Any],
) -> None:
    require(candidate.get("schemaVersion") == 1, "protocol candidate schema differs")
    require(candidate.get("kind") == "ordivon.protocol-candidate", "protocol candidate kind differs")
    require(candidate.get("version") == candidate_config.get("version"), "protocol candidate version declaration differs")
    require(candidate.get("status") == candidate_config.get("status") == "unreleased", "protocol candidate status declaration differs")
    require(candidate.get("baseRelease", {}).get("version") == candidate_config.get("base_release"), "protocol candidate base-release declaration differs")
    require(candidate.get("automaticConsumerUpgrade") is False, "protocol candidate may not auto-upgrade consumers")
    require(candidate.get("requiredOwnerAdmission") == candidate_config.get("required_owner_admission"), "protocol candidate owner-admission boundary differs")
    require(
        candidate.get("integrity", {}).get("payloadDigest")
        == integrity(candidate)["payloadDigest"],
        "protocol candidate manifest digest differs",
    )


def validate_current_protocol_revision(
    computing: Path,
    revision: str,
    *,
    release: dict[str, Any],
    release_artifacts: dict[str, str],
    candidate: dict[str, Any] | None,
    label: str,
) -> str:
    """Validate one current consumer pin and return its declared migration standing."""
    require(bool(REVISION.fullmatch(revision)), f"{label} protocol revision is invalid")
    package_manifest = tomllib.loads(
        git_bytes(
            computing,
            revision,
            "packages/ordivon-protocol/pyproject.toml",
        ).decode("utf-8")
    )
    observed_version = package_manifest["project"]["version"]
    if observed_version == release["version"]:
        standing = "release"
    else:
        require(candidate is not None, f"{label} protocol pin resolves to undeclared candidate version")
        require(candidate["status"] == "unreleased", "current protocol candidate must remain unreleased")
        require(
            candidate["baseRelease"]["version"] == release["version"],
            "current protocol candidate base release differs",
        )
        require(
            candidate.get("unchangedReleaseArtifacts") is True,
            "current protocol candidate does not preserve released artifacts",
        )
        require(
            observed_version == candidate["version"],
            f"{label} protocol pin resolves to undeclared candidate version",
        )
        standing = "candidate"
    for path, expected in release_artifacts.items():
        require(
            sha256(git_bytes(computing, revision, path)) == expected,
            f"{label} protocol pin differs from released artifact: {path}",
        )
    return standing


def validate_game_binding(
    *,
    computing: Path,
    game: Path,
    game_revision: str,
    manifest_path: PurePosixPath,
    release: dict[str, Any],
    release_artifacts: dict[str, str],
    expected_protocol_revision: str | None,
    label: str,
) -> str:
    require(bool(REVISION.fullmatch(game_revision)), f"{label} Game revision is invalid")
    git(game, "cat-file", "-e", f"{game_revision}^{{commit}}")
    game_manifest = json.loads(
        git_bytes(game, game_revision, manifest_path.as_posix())
    )
    require(
        game_manifest["protocolVersion"] == release["version"],
        f"{label} Game protocol version differs",
    )
    game_pin = game_manifest["sourceRevision"]
    require(bool(REVISION.fullmatch(game_pin)), f"{label} Game sourceRevision is invalid")
    if expected_protocol_revision is not None:
        require(
            game_pin == expected_protocol_revision,
            f"{label} Game protocol revision differs from frozen release declaration",
        )
    vector_path = game_manifest["sourcePath"]
    vector_bytes = git_bytes(computing, game_pin, vector_path)
    require(
        sha256(vector_bytes) == game_manifest["vectorFileDigest"],
        f"{label} Game source vector digest differs",
    )
    frozen_vectors = git_bytes(
        game,
        game_revision,
        manifest_path.with_name("vectors.json").as_posix(),
    )
    require(
        sha256(frozen_vectors) == game_manifest["vectorFileDigest"],
        f"{label} Game frozen vectors differ from manifest",
    )
    require(
        release_artifacts[vector_path] == game_manifest["vectorFileDigest"],
        f"{label} Game vectors differ from released vectors",
    )
    return game_pin


@contextmanager
def clean_worktree(root: Path, revision: str, *, prefix: str) -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix=prefix) as directory:
        checkout = Path(directory) / "checkout"
        run(
            ["git", "-C", str(root), "worktree", "add", "--detach", str(checkout), revision],
            cwd=root,
        )
        try:
            require(
                not git(checkout, "status", "--porcelain=v1"),
                f"temporary worktree is dirty: {checkout}",
            )
            yield checkout
        finally:
            subprocess.run(
                ["git", "-C", str(root), "worktree", "remove", "--force", str(checkout)],
                cwd=root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )


def run_host_tests(
    *,
    host: Path,
    revision: str,
    computing: Path,
    protocol_revision: str,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    with clean_worktree(
        computing,
        protocol_revision,
        prefix="ordivon-protocol-consumer-",
    ) as protocol_checkout:
        with clean_worktree(host, revision, prefix="ordivon-host-consumer-") as checkout:
            environment["PYTHONPATH"] = os.pathsep.join(
                [
                    str(protocol_checkout / "packages" / "ordivon-protocol" / "src"),
                    str(checkout / "src"),
                ]
            )
            return run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                cwd=checkout,
                env=environment,
            )


def run_game_vector_tests(
    *,
    game: Path,
    revision: str,
    node: str,
) -> subprocess.CompletedProcess[str]:
    with clean_worktree(game, revision, prefix="ordivon-game-consumer-") as checkout:
        return run(
            [node, "--test", "test/host-contract-vectors.test.ts"],
            cwd=checkout,
        )


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
        conformance = tomllib.loads(
            (computing / "projects" / "conformance.toml").read_text()
        )
        release_path = computing / conformance["protocol"]["release"]
        release = json.loads(release_path.read_text())
        release_artifacts = {
            item["path"]: item["digest"] for item in release["artifacts"]
        }
        release_consumers = {
            item["repositoryId"]: item for item in release["consumers"]
        }
        candidate_config = conformance.get("protocol_candidate")
        candidate = None
        if candidate_config is not None:
            candidate = json.loads(
                (computing / candidate_config["manifest"]).read_text()
            )
            validate_candidate_declaration(candidate_config, candidate)
        game_project = next(
            item for item in conformance["projects"] if item["id"] == "ordivon-game"
        )
        manifest_path = PurePosixPath(game_project["vector_manifest"])

        host_release = release_consumers["ordivon-host"]
        host_release_revision = host_release["observedRevision"]
        require(
            bool(REVISION.fullmatch(host_release_revision)),
            "frozen Host observedRevision is invalid",
        )
        git(host, "cat-file", "-e", f"{host_release_revision}^{{commit}}")
        host_release_pin = protocol_pin(
            git_bytes(host, host_release_revision, "pyproject.toml").decode("utf-8"),
            "frozen Host",
        )
        require(
            host_release_pin == host_release["protocolRevision"],
            "frozen Host pin differs from release declaration",
        )
        validate_protocol_revision(
            computing,
            host_release_pin,
            release=release,
            release_artifacts=release_artifacts,
            label="frozen Host",
        )
        steps.append(
            {
                "id": "release-host-pin",
                "scope": "release-frozen",
                "status": "passed",
                "consumerRevision": host_release_revision,
                "protocolRevision": host_release_pin,
            }
        )

        game_release = release_consumers["ordivon-game"]
        game_release_revision = game_release["observedRevision"]
        game_release_pin = validate_game_binding(
            computing=computing,
            game=game,
            game_revision=game_release_revision,
            manifest_path=manifest_path,
            release=release,
            release_artifacts=release_artifacts,
            expected_protocol_revision=game_release["protocolRevision"],
            label="frozen",
        )
        steps.append(
            {
                "id": "release-game-vector-pin",
                "scope": "release-frozen",
                "status": "passed",
                "consumerRevision": game_release_revision,
                "protocolRevision": game_release_pin,
            }
        )

        node = shutil.which("node")
        require(node is not None, "node is required for Game consumer tests")
        release_game_started = time.monotonic()
        release_game_result = run_game_vector_tests(
            game=game,
            revision=game_release_revision,
            node=node,
        )
        steps.append(
            {
                "id": "release-game-vector-tests",
                "scope": "release-frozen",
                "status": "passed",
                "consumerRevision": game_release_revision,
                "elapsedMs": round((time.monotonic() - release_game_started) * 1000),
                "summary": release_game_result.stdout.strip().splitlines()[-3:],
            }
        )

        host_current_pin = protocol_pin(
            (host / "pyproject.toml").read_text(),
            "current Host",
        )
        host_current_standing = validate_current_protocol_revision(
            computing,
            host_current_pin,
            release=release,
            release_artifacts=release_artifacts,
            candidate=candidate,
            label="current Host",
        )
        steps.append(
            {
                "id": "current-host-pin",
                "scope": "current-head",
                "status": "passed",
                "consumerRevision": revisions["ordivon-host"],
                "protocolRevision": host_current_pin,
                "protocolStanding": host_current_standing,
            }
        )

        host_started = time.monotonic()
        host_result = run_host_tests(
            host=host,
            revision=revisions["ordivon-host"],
            computing=computing,
            protocol_revision=host_current_pin,
        )
        steps.append(
            {
                "id": "current-host-tests",
                "scope": "current-head",
                "status": "passed",
                "consumerRevision": revisions["ordivon-host"],
                "elapsedMs": round((time.monotonic() - host_started) * 1000),
                "summary": host_result.stderr.strip().splitlines()[-1:],
            }
        )

        game_current_pin = validate_game_binding(
            computing=computing,
            game=game,
            game_revision=revisions["ordivon-game"],
            manifest_path=manifest_path,
            release=release,
            release_artifacts=release_artifacts,
            expected_protocol_revision=None,
            label="current",
        )
        steps.append(
            {
                "id": "current-game-vector-pin",
                "scope": "current-head",
                "status": "passed",
                "consumerRevision": revisions["ordivon-game"],
                "protocolRevision": game_current_pin,
                "protocolStanding": "release",
            }
        )

        current_game_started = time.monotonic()
        current_game_result = run_game_vector_tests(
            game=game,
            revision=revisions["ordivon-game"],
            node=node,
        )
        steps.append(
            {
                "id": "current-game-vector-tests",
                "scope": "current-head",
                "status": "passed",
                "consumerRevision": revisions["ordivon-game"],
                "elapsedMs": round((time.monotonic() - current_game_started) * 1000),
                "summary": current_game_result.stdout.strip().splitlines()[-3:],
            }
        )
        status = "passed"
        error = None
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        tomllib.TOMLDecodeError,
    ) as caught:
        status = "failed"
        error = str(caught)

    document: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.protocol-consumer-gate",
        "capturedAt": utc_now(),
        "status": status,
        "scopes": ["release-frozen", "current-head"],
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
