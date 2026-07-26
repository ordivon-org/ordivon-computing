#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
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

from anc_continuation.adapters import (  # noqa: E402
    CodexCliModelAdapter,
    ScriptedModelAdapter,
)
from anc_continuation.host import FreshHost  # noqa: E402
from anc_continuation.workload import load_manifest  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Continue a frozen ANC task in one fresh Host process"
    )
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--capsule-digest")
    parser.add_argument("--world-root", type=Path)
    parser.add_argument("--adapter", choices=("scripted", "codex"), default="scripted")
    parser.add_argument("--model")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stop-before-model", action="store_true")
    args = parser.parse_args()
    manifest = load_manifest(args.checkpoint)
    digest = args.capsule_digest or str(manifest["capsuleDigest"])
    if args.adapter == "scripted":
        adapter = ScriptedModelAdapter()
    else:
        adapter = CodexCliModelAdapter(
            working_directory=(args.world_root or args.checkpoint),
            model=args.model,
        )
    started_ns = time.monotonic_ns()
    receipt = FreshHost(args.checkpoint, adapter).run(
        digest,
        world_root=args.world_root,
        stop_before_model=args.stop_before_model,
    )
    elapsed_ms = (time.monotonic_ns() - started_ns) // 1_000_000
    value = {
        "schemaVersion": 1,
        "kind": "anc.fresh-host-process-receipt",
        "processId": os.getpid(),
        "parentProcessId": os.getppid(),
        "originalTranscriptLoaded": False,
        "checkpoint": str(args.checkpoint),
        "elapsedMs": elapsed_ms,
        "modelCallCount": 1,
        "semanticExecutionCount": len(receipt.executed_effects),
        "humanCorrectionCount": 0,
        "modelTokenCount": None,
        "host": receipt.to_dict(),
    }
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
