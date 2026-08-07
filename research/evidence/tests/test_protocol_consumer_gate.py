from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "check_protocol_consumers",
    ROOT / "scripts" / "check_protocol_consumers.py",
)
assert SPEC is not None and SPEC.loader is not None
CONSUMERS = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CONSUMERS
SPEC.loader.exec_module(CONSUMERS)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.strip()


def init_repository(root: Path) -> None:
    root.mkdir(parents=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "consumer-gate@example.invalid")
    git(root, "config", "user.name", "Consumer Gate Test")


def commit_all(root: Path, message: str) -> str:
    git(root, "add", ".")
    git(root, "commit", "-qm", message)
    return git(root, "rev-parse", "HEAD")


class CleanWorktreeTests(unittest.TestCase):
    def test_untracked_empty_directory_does_not_change_commit_under_test(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "host"
            init_repository(repository)
            (repository / "tracked.txt").write_text("tracked\n", encoding="utf-8")
            revision = commit_all(repository, "initial")
            residual = repository / "src" / "ordivon_host" / "providers"
            residual.mkdir(parents=True)
            self.assertTrue(residual.exists())
            self.assertEqual(git(repository, "status", "--porcelain=v1"), "")

            with CONSUMERS.clean_worktree(
                repository,
                revision,
                prefix="consumer-gate-test-",
            ) as checkout:
                self.assertFalse(
                    (checkout / "src" / "ordivon_host" / "providers").exists()
                )
                self.assertEqual(git(checkout, "status", "--porcelain=v1"), "")


class GameBindingTests(unittest.TestCase):
    def test_current_binding_is_checked_independently_from_frozen_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            computing = root / "computing"
            game = root / "game"
            init_repository(computing)
            vector_path = Path(
                "packages/ordivon-protocol/src/ordivon_protocol/vectors/"
                "host-workload-vectors-v1.json"
            )
            (computing / vector_path).parent.mkdir(parents=True)
            vector_bytes = b'{"cases":[]}\n'
            (computing / vector_path).write_bytes(vector_bytes)
            computing_revision = commit_all(computing, "vectors")

            init_repository(game)
            fixture = game / "fixtures" / "host-workload-v1"
            fixture.mkdir(parents=True)
            vector_digest = CONSUMERS.sha256(vector_bytes)
            (fixture / "vectors.json").write_bytes(vector_bytes)
            manifest = {
                "protocolVersion": "0.3.0",
                "sourceRevision": computing_revision,
                "sourcePath": vector_path.as_posix(),
                "vectorFileDigest": vector_digest,
            }
            (fixture / "manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            game_revision = commit_all(game, "current consumer")
            release = {"version": "0.3.0"}
            release_artifacts = {vector_path.as_posix(): vector_digest}

            observed = CONSUMERS.validate_game_binding(
                computing=computing,
                game=game,
                game_revision=game_revision,
                manifest_path=Path("fixtures/host-workload-v1/manifest.json"),
                release=release,
                release_artifacts=release_artifacts,
                expected_protocol_revision=None,
                label="current",
            )
            self.assertEqual(observed, computing_revision)

            with self.assertRaisesRegex(
                ValueError,
                "differs from frozen release declaration",
            ):
                CONSUMERS.validate_game_binding(
                    computing=computing,
                    game=game,
                    game_revision=game_revision,
                    manifest_path=Path("fixtures/host-workload-v1/manifest.json"),
                    release=release,
                    release_artifacts=release_artifacts,
                    expected_protocol_revision="0" * 40,
                    label="frozen",
                )


if __name__ == "__main__":
    unittest.main()
