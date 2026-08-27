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

def inspect(repo: Path) -> dict[str, object]:
    repo = repo.resolve()
    entry = repo / "scripts" / "owner-environment"
    result: dict[str, object] = {"repo": str(repo), "entrypoint": str(entry), "status": "FAIL", "reasons": []}
    reasons: list[str] = result["reasons"]  # type: ignore[assignment]
    if not entry.is_file():
        reasons.append("missing scripts/owner-environment")
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
    return 0 if all(row["status"] == "DISCOVERABLE" for row in rows) else 1

if __name__ == "__main__":
    raise SystemExit(main())
