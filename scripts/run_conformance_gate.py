#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON_VERSION = "3.12.13"
REQUIREMENTS = ROOT / "requirements-conformance.txt"


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise SystemExit(f"error: {name} is required for the Computing conformance launcher")
    return path


def main() -> int:
    mise = require_tool("mise")
    uv = require_tool("uv")
    command = [
        mise,
        "exec",
        "--",
        uv,
        "run",
        "--no-project",
        "--python",
        PYTHON_VERSION,
        "--with-requirements",
        str(REQUIREMENTS),
        "python",
        str(ROOT / "scripts" / "ordivon_conformance.py"),
        "gate",
        *sys.argv[1:],
    ]
    environment = dict(os.environ)
    environment.setdefault("PYTHONUTF8", "1")
    return subprocess.run(command, cwd=ROOT, env=environment, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
