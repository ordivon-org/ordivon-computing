#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
EXPERIMENT = SCRIPT.parents[1]
EXPERIMENTS = EXPERIMENT.parent
for path in (
    EXPERIMENT / "src",
    EXPERIMENTS / "external-semantic-contract-v0" / "src",
    EXPERIMENTS / "external-semantic-contract-v0",
    EXPERIMENTS / "semantic-core-v0" / "src",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from anc_continuation.workload import freeze_checkpoint  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freeze the deterministic ANC continuation workload at its checkpoint"
    )
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    frozen = freeze_checkpoint(args.output, source_revision=args.source_revision)
    print(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "anc.freeze-workload-receipt",
                "sourceRevision": frozen.source_revision,
                "capsuleDigest": frozen.capsule_digest,
                "initialWorldDigest": frozen.initial_digest,
                "terminalWorldDigest": frozen.terminal_digest,
                "manifestPath": str(frozen.manifest_path),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
