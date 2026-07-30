#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from anc_core_work_system.model import canonical_bytes
from anc_core_work_system.reporting import derive_report_statistics


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive statistics for the Round 1 report")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--live", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
    live = json.loads(args.live.read_text(encoding="utf-8"))
    payload = derive_report_statistics(matrix, live)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_bytes(payload) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
