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

from anc_continuation.ablation import capsule_ablation_receipt  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TaskCapsule v0 field ablations")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = capsule_ablation_receipt(args.checkpoint)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
