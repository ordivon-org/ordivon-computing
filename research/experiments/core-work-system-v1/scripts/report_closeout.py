#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from anc_core_work_system.conclusions import EvidenceInputs, write_closeout


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive the Round 1 closeout receipt")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--live", type=Path, required=True)
    parser.add_argument("--host-source-revision", required=True)
    parser.add_argument("--host-receipt-digest", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_closeout(
        EvidenceInputs(
            matrix_path=args.matrix,
            live_path=args.live,
            host_source_revision=args.host_source_revision,
            host_receipt_digest=args.host_receipt_digest,
        ),
        args.output,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
