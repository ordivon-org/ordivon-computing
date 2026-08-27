#!/usr/bin/env python3
"""Static discoverability check for the cross-owner environment entrypoint.

This checker does not own another repository's dependency graph and does not claim
that a static PASS proves cold-start reproducibility. Dynamic proof remains the
owner's `scripts/owner-environment cold-start`.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

MODES = ("bootstrap", "doctor", "test", "cold-start")
ROOT_MANIFESTS = (
    "pyproject.toml", "package.json", "Cargo.toml", "go.mod", "pom.xml",
    "build.gradle", "build.gradle.kts", "Makefile", "mise.toml",
)
SOURCE_ROOTS = ("src", "crates", "apps", "packages", "cmd", "lib")
CODE_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".rs", ".go", ".java", ".kt", ".c", ".cc", ".cpp", ".h", ".hpp", ".sh"}

def _has_files(path: Path) -> bool:
    return path.is_dir() and any(item.is_file() for item in path.rglob("*"))

def executable_pressure(repo: Path) -> tuple[bool, list[str]]:
    signals: list[str] = []
    manifests = [name for name in ROOT_MANIFESTS if (repo / name).is_file()]
    if manifests:
        signals.append("root-manifest:" + ",".join(manifests))
    for root_name in SOURCE_ROOTS:
        root = repo / root_name
        if root.is_dir() and any(item.is_file() and item.suffix in CODE_SUFFIXES for item in root.rglob("*")):
            signals.append("code-root:" + root_name)
    for test_name in ("tests", "test"):
        if _has_files(repo / test_name):
            signals.append("tests:" + test_name)
    scripts = repo / "scripts"
    if scripts.is_dir() and any(item.is_file() and os.access(item, os.X_OK) for item in scripts.iterdir()):
        signals.append("executable-scripts")
    return bool(signals), signals

def inspect(repo: Path) -> dict[str, object]:
    repo = repo.resolve()
    entry = repo / "scripts" / "owner-environment"
    git_probe = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"],
        text=True, capture_output=True, check=False,
    )
    if git_probe.returncode != 0 or git_probe.stdout.strip() != "true":
        return {
            "repo": str(repo),
            "entrypoint": str(entry),
            "applicability": "OUT_OF_SCOPE",
            "pressureSignals": [],
            "status": "OUT_OF_SCOPE",
            "reasons": ["path is not a Git worktree repository"],
        }
    required, signals = executable_pressure(repo)
    result: dict[str, object] = {
        "repo": str(repo),
        "entrypoint": str(entry),
        "applicability": "REQUIRED" if required else "NOT_APPLICABLE",
        "pressureSignals": signals,
        "status": "FAIL" if required else "NOT_APPLICABLE",
        "reasons": [],
    }
    reasons: list[str] = result["reasons"]  # type: ignore[assignment]
    if not entry.is_file():
        if required:
            reasons.append("executable pressure exists but scripts/owner-environment is missing")
        else:
            reasons.append("no executable environment pressure detected")
        return result
    if not os.access(entry, os.X_OK):
        reasons.append("scripts/owner-environment is not executable")
        return result
    proc = subprocess.run([str(entry), "--help"], cwd=repo, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        reasons.append(f"--help exited {proc.returncode}")
        return result
    help_text = proc.stdout + proc.stderr
    missing = [mode for mode in MODES if mode not in help_text]
    if missing:
        reasons.append("help omits modes: " + ",".join(missing))
        return result
    result["status"] = "DISCOVERABLE"
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repos", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows = [inspect(repo) for repo in args.repos]
    if args.json:
        print(json.dumps({"schemaVersion": 1, "kind": "ordivon.owner-environment-discoverability", "rows": rows}, sort_keys=True))
    else:
        for row in rows:
            suffix = "" if not row["reasons"] else " :: " + "; ".join(row["reasons"])  # type: ignore[arg-type]
            print(f"{row['status']} {row['repo']}{suffix}")
    accepted = {"DISCOVERABLE", "NOT_APPLICABLE", "OUT_OF_SCOPE"}
    return 0 if all(row["status"] in accepted for row in rows) else 1

if __name__ == "__main__":
    raise SystemExit(main())
