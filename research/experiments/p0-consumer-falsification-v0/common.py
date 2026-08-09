from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

EXPERIMENT = Path(__file__).resolve().parent
COMPUTING_ROOT = EXPERIMENT.parents[2]
HOST_ROOT = Path("/root/projects/ordivon-host")
HARNESS_ROOT = Path("/root/projects/ordivon-harness")
RUNTIME_ROOT = Path("/root/projects/ordivon-runtime")
B4_PATH = COMPUTING_ROOT / "research/experiments/harness-evaluation-v0/run_b4_deterministic_smoke.py"
HISTORICAL_HOST_REVISION = "b4bc43a4ea7eb1e7771644d507bc4a3a39b4e741"
TASK_ID = "HARNESS-REPO-REPAIR-001"
TASK_VERSION = 1


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def repo_vector(*, allow_dirty_computing: bool = False) -> dict[str, dict[str, Any]]:
    repos = {
        "ordivon-computing": COMPUTING_ROOT,
        "ordivon-host": HOST_ROOT,
        "ordivon-harness": HARNESS_ROOT,
        "ordivon-runtime": RUNTIME_ROOT,
    }
    result: dict[str, dict[str, Any]] = {}
    for name, root in repos.items():
        head = git(root, "rev-parse", "HEAD")
        dirty_paths = [line for line in git(root, "status", "--porcelain").splitlines() if line]
        if dirty_paths and not (name == "ordivon-computing" and allow_dirty_computing):
            raise RuntimeError(f"owner repository is dirty: {name}")
        result[name] = {
            "head": head,
            "dirty": bool(dirty_paths),
            "dirtyPathCount": len(dirty_paths),
        }
    return result


def ensure_harness_source() -> None:
    source = str(HARNESS_ROOT / "src")
    if source not in sys.path:
        sys.path.insert(0, source)


def load_b4_module():
    spec = importlib.util.spec_from_file_location("p0_b4_primitives", B4_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load B4 Task/verifier primitives")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def json_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def text_digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def harness_package_version() -> str:
    ensure_harness_source()
    from ordivon_harness import package_version

    return package_version()
