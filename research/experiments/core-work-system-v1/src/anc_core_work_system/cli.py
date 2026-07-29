from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

from .live_gauntlet import run_live_gauntlet
from .matrix import run_deterministic_matrix, write_matrix
from .model import canonical_bytes
from .world import freeze_fixture


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anc-core-work-system")
    commands = parser.add_subparsers(dest="command", required=True)

    freeze = commands.add_parser("freeze", help="freeze the contract-rebind maintenance fixture")
    freeze.add_argument("--output", required=True)
    freeze.add_argument("--replace", action="store_true")

    matrix = commands.add_parser("matrix", help="run the deterministic Round 1 matrix")
    matrix.add_argument("--fixture", required=True)
    matrix.add_argument("--output", required=True)
    matrix.add_argument("--working-root")
    matrix.add_argument("--temporal-cache")

    live = commands.add_parser("live", help="run real Codex/Hermes provider replacement trials")
    live.add_argument("--fixture", required=True)
    live.add_argument("--output", required=True)
    live.add_argument("--working-root", required=True)
    live.add_argument("--repeats", type=int, default=3)
    live.add_argument("--codex-model")
    live.add_argument("--hermes-model", default="deepseek-v4-pro")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "freeze":
        manifest = freeze_fixture(args.output, replace_existing=args.replace)
        print(canonical_bytes(manifest.to_dict()).decode("utf-8"))
        return 0
    output = Path(args.output)
    if args.command == "live":
        value = run_live_gauntlet(
            args.fixture,
            output=output,
            working_root=args.working_root,
            repeats=args.repeats,
            codex_model=args.codex_model,
            hermes_model=args.hermes_model,
        )
        print(value["gauntletDigest"])
        return 0
    with tempfile.TemporaryDirectory(prefix="anc-round1-") as temporary:
        working_root = Path(args.working_root) if args.working_root else Path(temporary) / "trials"
        temporal_cache = Path(args.temporal_cache) if args.temporal_cache else Path(temporary) / "temporal-cache"
        value = run_deterministic_matrix(
            args.fixture,
            working_root=working_root,
            temporal_cache=temporal_cache,
        )
        write_matrix(output, value)
    print(value["matrixDigest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
