from __future__ import annotations

import argparse
import json
import os
import platform
import sqlite3
import statistics
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from anc_semantic_core.testing import test_authority_policy  # noqa: E402
from anc_semantic_core.journal import JournalReducer  # noqa: E402

from workloads import admit_and_prepare, open_reducer  # noqa: E402


PROFILES = {
    "smoke": {"memory": (10, 50), "journal": (10, 25)},
    "standard": {"memory": (10, 50, 100, 200), "journal": (10, 50, 100)},
}


def _median_run(function: Any, repeats: int) -> float:
    values = []
    for _ in range(repeats):
        started = time.perf_counter()
        function()
        values.append(time.perf_counter() - started)
    return statistics.median(values)


def memory_case(count: int, repeats: int) -> dict[str, Any]:
    run_index = 0

    def run() -> None:
        nonlocal run_index
        reducer, views = open_reducer("memory", f"bench-memory-{count}-{run_index}")
        run_index += 1
        for index in range(count):
            admit_and_prepare(views, index, prefix=f"memory-{run_index}")
        reducer.close()

    elapsed = _median_run(run, repeats)
    return {
        "effects": count,
        "commands": count * 2,
        "median_total_ms": round(elapsed * 1000, 3),
        "median_us_per_command": round(elapsed * 1_000_000 / (count * 2), 3),
    }


def journal_case(count: int, repeats: int) -> dict[str, Any]:
    elapsed_values: list[float] = []
    replay_values: list[float] = []
    db_sizes: list[int] = []
    for repeat in range(repeats):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "benchmark.sqlite3"
            reducer, views = open_reducer(
                "journal", f"bench-journal-{count}-{repeat}", path
            )
            started = time.perf_counter()
            for index in range(count):
                admit_and_prepare(views, index, prefix=f"journal-{repeat}")
            elapsed_values.append(time.perf_counter() - started)
            entries = reducer.journal_entry_count
            reducer.close()
            db_sizes.append(path.stat().st_size)
            started = time.perf_counter()
            reopened = JournalReducer(path, test_authority_policy())
            replay_values.append(time.perf_counter() - started)
            reopened.close()
    elapsed = statistics.median(elapsed_values)
    replay = statistics.median(replay_values)
    return {
        "effects": count,
        "commands": count * 2,
        "journal_entries": entries,
        "median_total_ms": round(elapsed * 1000, 3),
        "median_ms_per_command": round(elapsed * 1000 / (count * 2), 3),
        "median_reopen_ms": round(replay * 1000, 3),
        "median_db_bytes": int(statistics.median(db_sizes)),
    }


def environment(source_revision: str) -> dict[str, Any]:
    return {
        "source_revision": source_revision,
        "python": platform.python_version(),
        "sqlite": sqlite3.sqlite_version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "pid": os.getpid(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=tuple(PROFILES), default="standard")
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.repeats < 1:
        raise SystemExit("--repeats must be positive")
    profile = PROFILES[args.profile]
    result = {
        "schema_version": 1,
        "environment": environment(args.source_revision),
        "profile": args.profile,
        "repeats": args.repeats,
        "memory_scaling": [memory_case(n, args.repeats) for n in profile["memory"]],
        "journal_scaling": [journal_case(n, args.repeats) for n in profile["journal"]],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
