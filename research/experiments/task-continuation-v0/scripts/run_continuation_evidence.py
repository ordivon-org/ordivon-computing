#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
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
from anc_continuation.workload import (  # noqa: E402
    WORLD_RELATIVE_PATH,
    baseline_receipt,
    freeze_checkpoint,
)


def run_child(
    checkpoint: Path,
    *,
    adapter: str,
    model: str | None,
    provider: str | None = None,
    base_url: str | None = None,
    hermes_env_path: Path | None = None,
) -> dict:
    command = [
        sys.executable,
        str(EXPERIMENT / "scripts" / "run_fresh_host.py"),
        "--checkpoint",
        str(checkpoint),
        "--adapter",
        adapter,
    ]
    if model is not None:
        command.extend(["--model", model])
    if provider is not None:
        command.extend(["--provider", provider])
    if base_url is not None:
        command.extend(["--base-url", base_url])
    if hermes_env_path is not None:
        command.extend(["--hermes-env-path", str(hermes_env_path)])
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=os.environ.copy(),
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"fresh Host child ({adapter}) failed: {completed.stderr.strip()[-4000:]}"
        )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("fresh Host child receipt is not an object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate exact continuation baseline, ablation, and fresh-process evidence"
    )
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--include-codex", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--include-hermes", action="store_true")
    parser.add_argument("--hermes-model", default="deepseek-v4-pro")
    parser.add_argument("--hermes-provider", default="deepseek")
    parser.add_argument("--hermes-base-url", default="https://api.deepseek.com")
    parser.add_argument("--hermes-env-path", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="anc-continuation-evidence-") as temporary:
        root = Path(temporary)
        frozen = freeze_checkpoint(
            root / "frozen", source_revision=args.source_revision
        )
        baseline = baseline_receipt(frozen.root)
        ablation = capsule_ablation_receipt(frozen.root)

        scripted_checkpoint = root / "scripted"
        shutil.copytree(frozen.root, scripted_checkpoint)
        scripted = run_child(scripted_checkpoint, adapter="scripted", model=None)

        drift_checkpoint = root / "drift"
        shutil.copytree(frozen.root, drift_checkpoint)
        drift_world = drift_checkpoint / WORLD_RELATIVE_PATH
        drift_world.write_text("mode = externally-changed\n")
        drift = run_child(drift_checkpoint, adapter="scripted", model=None)

        codex = None
        if args.include_codex:
            codex_checkpoint = root / "codex"
            shutil.copytree(frozen.root, codex_checkpoint)
            codex = run_child(codex_checkpoint, adapter="codex", model=args.model)

        hermes = None
        if args.include_hermes:
            hermes_checkpoint = root / "hermes"
            shutil.copytree(frozen.root, hermes_checkpoint)
            hermes = run_child(
                hermes_checkpoint,
                adapter="hermes",
                model=args.hermes_model,
                provider=args.hermes_provider,
                base_url=args.hermes_base_url,
                hermes_env_path=args.hermes_env_path,
            )

        receipt = {
            "schemaVersion": 1,
            "kind": "anc.continuation-evidence",
            "sourceRevision": args.source_revision,
            "evidenceProcessId": os.getpid(),
            "capsuleDigest": frozen.capsule_digest,
            "initialWorldDigest": frozen.initial_digest,
            "terminalWorldDigest": frozen.terminal_digest,
            "baselines": baseline,
            "ablations": ablation,
            "freshProcessScripted": scripted,
            "freshProcessDrift": drift,
            "freshProcessCodex": codex,
            "freshProcessHermes": hermes,
        }
        for child in (scripted, drift, codex, hermes):
            if child is None:
                continue
            if child["processId"] == os.getpid():
                raise AssertionError("Host evidence did not run in a fresh process")
            if child["originalTranscriptLoaded"] is not False:
                raise AssertionError("fresh Host reported transcript loading")
        if scripted["host"]["status"] != "completed":
            raise AssertionError("scripted fresh Host did not complete")
        if drift["host"]["status"] != "blocked-world-drift":
            raise AssertionError("drifted fresh Host did not block")
        if codex is not None and codex["host"]["status"] != "completed":
            raise AssertionError("Codex fresh Host did not complete")
        if hermes is not None and hermes["host"]["status"] != "completed":
            raise AssertionError("Hermes fresh Host did not complete")
        rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
        print(rendered, end="")


if __name__ == "__main__":
    main()
