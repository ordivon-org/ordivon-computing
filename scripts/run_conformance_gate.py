#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def main() -> int:
    entry = ROOT / "scripts" / "owner-environment"
    command = [str(entry), "test", *sys.argv[1:]]
    environment = dict(os.environ)
    environment.setdefault("PYTHONUTF8", "1")
    return subprocess.run(command, cwd=ROOT, env=environment, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
