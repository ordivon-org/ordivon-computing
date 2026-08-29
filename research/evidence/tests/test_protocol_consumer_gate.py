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


class WorkflowScopeTests(unittest.TestCase):
    def test_consumer_workflow_tracks_protocol_relation_not_general_conformance_launcher(self) -> None:
        workflow = (ROOT / ".github/workflows/protocol-consumers.yml").read_text(encoding="utf-8")
        for required in (
            '"packages/ordivon-protocol/**"',
            '"projects/conformance.toml"',
            '"research/evidence/tests/test_protocol_consumer_gate.py"',
            '"scripts/check_protocol_release.py"',
            '"scripts/check_protocol_consumers.py"',
        ):
            self.assertIn(required, workflow)
        self.assertNotIn('"scripts/ordivon_conformance.py"', workflow)


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


class CandidateDeclarationTests(unittest.TestCase):
    def _candidate(self) -> tuple[dict[str, object], dict[str, object]]:
        config: dict[str, object] = {
            "version": "0.4.0.dev0",
            "status": "unreleased",
            "base_release": "0.3.0",
            "required_owner_admission": ["ordivon-host"],
        }
        candidate: dict[str, object] = {
            "schemaVersion": 1,
            "kind": "ordivon.protocol-candidate",
            "version": "0.4.0.dev0",
            "status": "unreleased",
            "baseRelease": {"version": "0.3.0"},
            "automaticConsumerUpgrade": False,
            "requiredOwnerAdmission": ["ordivon-host"],
            "unchangedReleaseArtifacts": True,
        }
        candidate["integrity"] = CONSUMERS.integrity(candidate)
        return config, candidate

    def test_candidate_declaration_is_self_authenticating_for_consumer_gate(self) -> None:
        config, candidate = self._candidate()
        CONSUMERS.validate_candidate_declaration(config, candidate)

    def test_candidate_declaration_rejects_digest_tamper(self) -> None:
        config, candidate = self._candidate()
        candidate["version"] = "0.4.0.dev1"
        with self.assertRaisesRegex(ValueError, "version declaration differs|manifest digest differs"):
            CONSUMERS.validate_candidate_declaration(config, candidate)


class CurrentProtocolStandingTests(unittest.TestCase):
    def _computing_fixture(self, root: Path, version: str) -> tuple[Path, str, dict[str, str]]:
        computing = root / "computing"
        init_repository(computing)
        package = computing / "packages" / "ordivon-protocol"
        package.mkdir(parents=True)
        (package / "pyproject.toml").write_text(
            f'[project]\nname = "ordivon-protocol"\nversion = "{version}"\n',
            encoding="utf-8",
        )
        artifact = package / "artifact.json"
        artifact.write_text('{"stable":true}\n', encoding="utf-8")
        revision = commit_all(computing, version)
        artifacts = {
            "packages/ordivon-protocol/artifact.json": CONSUMERS.sha256(artifact.read_bytes())
        }
        return computing, revision, artifacts

    def test_current_release_consumer_keeps_release_standing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            computing, revision, artifacts = self._computing_fixture(Path(temporary), "0.3.0")
            standing = CONSUMERS.validate_current_protocol_revision(
                computing,
                revision,
                release={"version": "0.3.0"},
                release_artifacts=artifacts,
                candidate=None,
                label="current Host",
            )
            self.assertEqual(standing, "release")

    def test_current_declared_candidate_consumer_is_distinct_from_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            computing, revision, artifacts = self._computing_fixture(Path(temporary), "0.4.0.dev0")
            standing = CONSUMERS.validate_current_protocol_revision(
                computing,
                revision,
                release={"version": "0.3.0"},
                release_artifacts=artifacts,
                candidate={
                    "version": "0.4.0.dev0",
                    "status": "unreleased",
                    "baseRelease": {"version": "0.3.0"},
                    "unchangedReleaseArtifacts": True,
                },
                label="current Host",
            )
            self.assertEqual(standing, "candidate")

    def test_candidate_cannot_drift_released_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            computing, revision, artifacts = self._computing_fixture(Path(temporary), "0.4.0.dev0")
            artifacts["packages/ordivon-protocol/artifact.json"] = "sha256:" + "0" * 64
            with self.assertRaisesRegex(ValueError, "differs from released artifact"):
                CONSUMERS.validate_current_protocol_revision(
                    computing,
                    revision,
                    release={"version": "0.3.0"},
                    release_artifacts=artifacts,
                    candidate={
                        "version": "0.4.0.dev0",
                        "status": "unreleased",
                        "baseRelease": {"version": "0.3.0"},
                        "unchangedReleaseArtifacts": True,
                    },
                    label="current Host",
                )

    def test_undeclared_candidate_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            computing, revision, artifacts = self._computing_fixture(Path(temporary), "9.9.9.dev0")
            with self.assertRaisesRegex(ValueError, "undeclared candidate version"):
                CONSUMERS.validate_current_protocol_revision(
                    computing,
                    revision,
                    release={"version": "0.3.0"},
                    release_artifacts=artifacts,
                    candidate={
                        "version": "0.4.0.dev0",
                        "status": "unreleased",
                        "baseRelease": {"version": "0.3.0"},
                        "unchangedReleaseArtifacts": True,
                    },
                    label="current Host",
                )


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
