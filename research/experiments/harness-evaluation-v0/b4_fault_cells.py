from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any


class B4FaultCellError(RuntimeError):
    pass


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _with_integrity(value: dict[str, Any]) -> dict[str, Any]:
    return {
        **value,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": _digest_bytes(_canonical_bytes(value)),
        },
    }


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _execute(
    *,
    cell_id: str,
    command: tuple[str, ...],
    cwd: Path,
    env: dict[str, str] | None = None,
    expected_test_count: int,
    timeout_seconds: int = 180,
) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        timeout=timeout_seconds,
    )
    stdout = completed.stdout
    stderr = completed.stderr
    if completed.returncode != 0:
        raise B4FaultCellError(
            f"{cell_id} failed with exit {completed.returncode}; "
            f"stdoutDigest={_digest_bytes(stdout)} stderrDigest={_digest_bytes(stderr)}"
        )
    return {
        "cellId": cell_id,
        "status": "passed",
        "expectedTestCount": expected_test_count,
        "exitCode": completed.returncode,
        "stdoutDigest": _digest_bytes(stdout),
        "stderrDigest": _digest_bytes(stderr),
    }


def run_b4_fault_cells(
    *,
    computing_root: Path,
    harness_root: Path,
    harness_revision: str,
) -> dict[str, Any]:
    observed_harness_revision = _git(harness_root, "rev-parse", "HEAD")
    if observed_harness_revision != harness_revision:
        raise B4FaultCellError(
            "Harness revision differs for deterministic fault cells: "
            f"expected {harness_revision}, observed {observed_harness_revision}"
        )
    if _git(harness_root, "status", "--porcelain"):
        raise B4FaultCellError("Harness repository is dirty during deterministic fault cells")

    harness_python = "/root/.local/bin/uv"
    harness_env = dict(os.environ)
    existing_pythonpath = harness_env.get("PYTHONPATH")
    harness_env["PYTHONPATH"] = str(harness_root / "tests") + (
        os.pathsep + existing_pythonpath if existing_pythonpath else ""
    )
    stale = _execute(
        cell_id="HOST-STALE-ASSIGNMENT",
        command=(
            harness_python,
            "run",
            "python",
            "-m",
            "unittest",
            (
                "test_harness_h1.HarnessH1LifecycleTests."
                "test_stale_generation_proposal_is_retained_and_rejected"
            ),
            "-v",
        ),
        cwd=harness_root,
        env=harness_env,
        expected_test_count=1,
    )
    correction = _execute(
        cell_id="HARNESS-INVALID-TOOL-CORRECTION",
        command=(
            harness_python,
            "run",
            "python",
            "-m",
            "unittest",
            (
                "test_runner_r2_r3.HarnessR2R3Tests."
                "test_local_tool_rejection_returns_to_model_without_effect"
            ),
            (
                "test_runner_r2_r3.HarnessR2R3Tests."
                "test_malformed_provider_arguments_are_corrected_without_effect"
            ),
            "-v",
        ),
        cwd=harness_root,
        env=harness_env,
        expected_test_count=2,
    )
    observation_env = dict(os.environ)
    observation_env["PYTHONPATH"] = str(
        computing_root
        / "research"
        / "experiments"
        / "observation-plane-v0"
        / "implementation"
    )
    observation = _execute(
        cell_id="OBSERVATION-GAP-MAPPING-CORRUPTION-PRIVACY",
        command=(
            "/root/.local/bin/python3.12",
            "-m",
            "unittest",
            "discover",
            "-s",
            "research/experiments/observation-plane-v0/tests",
            "-p",
            "test_gateway.py",
            "-v",
        ),
        cwd=computing_root,
        env=observation_env,
        expected_test_count=7,
    )
    return _with_integrity(
        {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-b4-deterministic-fault-cells",
            "harnessRevision": harness_revision,
            "cells": [stale, correction, observation],
            "allPassed": True,
            "liveTrialUnlockedByThisRecordAlone": False,
            "productionActivated": False,
            "b6Implemented": False,
        }
    )


__all__ = ["B4FaultCellError", "run_b4_fault_cells"]
