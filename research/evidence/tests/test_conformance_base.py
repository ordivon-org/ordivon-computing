from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "ordivon_conformance",
    ROOT / "scripts" / "ordivon_conformance.py",
)
assert SPEC is not None and SPEC.loader is not None
CONFORMANCE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CONFORMANCE
SPEC.loader.exec_module(CONFORMANCE)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.strip()


def init_repository(root: Path, repository: str) -> None:
    root.mkdir(parents=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "conformance@example.invalid")
    git(root, "config", "user.name", "Conformance Test")
    git(root, "remote", "add", "origin", repository + ".git")


def commit_all(root: Path, message: str) -> str:
    git(root, "add", ".")
    git(root, "commit", "-qm", message)
    return git(root, "rev-parse", "HEAD")


class ManifestTests(unittest.TestCase):
    def test_manifest_matches_protocol_and_project_registry(self) -> None:
        manifest = CONFORMANCE.load_manifest()
        self.assertEqual(manifest.protocol.version, "0.3.0")
        self.assertEqual(manifest.projects[0].id, "ordivon-computing")
        self.assertEqual(manifest.project("ordivon-host").protocol_requirement, "0.3.0")
        self.assertEqual(
            [project.id for project in manifest.projects],
            [
                "ordivon-computing",
                "ordivon-runtime",
                "ordivon-host",
                "ordivon-game",
            ],
        )
        registry_text = (ROOT / "projects" / "registry.yaml").read_text()
        registry_ids = [
            match.group(1)
            for line in registry_text.splitlines()
            if (match := re.fullmatch(r"  - id: (ordivon-[a-z0-9-]+)", line))
        ]
        self.assertTrue(set(project.id for project in manifest.projects) <= set(registry_ids))
        self.assertIn("ordivon-harness", registry_ids)
        self.assertIn("ordivon-human", registry_ids)

    def test_research_map_uses_registry_project_ids(self) -> None:
        registry_text = (ROOT / "projects" / "registry.yaml").read_text()
        registry_ids = {
            match.group(1)
            for line in registry_text.splitlines()
            if (match := re.fullmatch(r"  - id: (ordivon-[a-z0-9-]+)", line))
        }
        related_projects: list[str] = []
        inside_related_projects = False
        for line in (ROOT / "research" / "map.yaml").read_text().splitlines():
            if line == "    related_projects:":
                inside_related_projects = True
            elif inside_related_projects and line.startswith("      - "):
                related_projects.append(line.removeprefix("      - "))
            elif inside_related_projects and line.strip():
                inside_related_projects = False
        self.assertTrue(related_projects)
        for project_id in related_projects:
            self.assertRegex(project_id, r"^ordivon-[a-z0-9-]+$")
            self.assertIn(project_id, registry_ids)
        self.assertNotIn("    current_slice:", registry_text)

    def test_manifest_rejects_protocol_version_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "packages" / "ordivon-protocol"
            package.mkdir(parents=True)
            (package / "pyproject.toml").write_text(
                '[project]\nname = "ordivon-protocol"\nversion = "9.9.9"\n'
            )
            manifest_path = root / "manifest.toml"
            manifest_path.write_text((ROOT / "projects" / "conformance.toml").read_text())
            with self.assertRaisesRegex(ValueError, "protocol package version differs"):
                CONFORMANCE.load_manifest(manifest_path, repository_root=root)


class RepositoryIdentityTests(unittest.TestCase):
    def test_github_https_and_ssh_remotes_share_one_identity(self) -> None:
        self.assertEqual(
            CONFORMANCE.normalize_repository_url(
                "git@github.com:zycxfyh/ordivon-host.git"
            ),
            "https://github.com/zycxfyh/ordivon-host",
        )
        self.assertEqual(
            CONFORMANCE.normalize_repository_url(
                "ssh://git@github.com/zycxfyh/ordivon-host.git"
            ),
            "https://github.com/zycxfyh/ordivon-host",
        )


class RevisionVectorTests(unittest.TestCase):
    def _fixture(self, root: Path) -> tuple[object, dict[str, Path], str]:
        computing = root / "ordivon-computing"
        host = root / "ordivon-host"
        init_repository(computing, "https://github.com/zycxfyh/ordivon-computing")
        protocol = computing / "packages" / "ordivon-protocol"
        resources = protocol / "src" / "ordivon_protocol"
        (resources / "schemas").mkdir(parents=True)
        (resources / "vectors").mkdir(parents=True)
        (protocol / "pyproject.toml").write_text(
            '[project]\nname = "ordivon-protocol"\nversion = "0.3.0"\n'
        )
        for name in (
            "effect-envelope-v1.schema.json",
            "tool-contract-v1.schema.json",
            "effect-binding-v1.schema.json",
            "host-workload-v1.schema.json",
        ):
            (resources / "schemas" / name).write_text('{"schema":1}\n')
        (resources / "vectors" / "canonical-vectors.json").write_text('{"vectors":[]}\n')
        (resources / "vectors" / "host-workload-vectors-v1.json").write_text('{"cases":[]}\n')
        computing_revision = commit_all(computing, "protocol")

        init_repository(host, "https://github.com/zycxfyh/ordivon-host")
        (host / "pyproject.toml").write_text(
            textwrap.dedent(
                f'''\
                [project]
                name = "ordivon-host"
                version = "0.1.0"
                dependencies = [
                  "ordivon-protocol @ git+https://github.com/zycxfyh/ordivon-computing.git@{computing_revision}#subdirectory=packages/ordivon-protocol",
                ]
                '''
            )
        )
        commit_all(host, "host")
        manifest = CONFORMANCE.load_manifest()
        return manifest, {"ordivon-computing": computing, "ordivon-host": host}, computing_revision

    def test_revision_vector_binds_host_pin_and_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest, roots, revision = self._fixture(Path(temporary))
            document = CONFORMANCE.revision_vector(
                manifest,
                roots,
                [project.id for project in manifest.projects if project.id not in roots],
            )
            self.assertEqual(document["protocol"]["sourceRevision"], revision)
            self.assertEqual(document["hostProtocolPin"]["computingRevision"], revision)
            self.assertEqual(document["hostProtocolPin"]["protocolVersion"], "0.3.0")
            self.assertEqual(document["integrity"], CONFORMANCE.integrity(document))

    def test_system_snapshot_uses_committed_protocol_resources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest, roots, _ = self._fixture(Path(temporary))
            document = CONFORMANCE.build_system_snapshot(
                manifest,
                roots,
                snapshot_id="ordivon-test-20260728t000000z",
                purpose="verify deterministic snapshot generation",
            )
            self.assertEqual(len(document["repositories"]), 2)
            self.assertEqual(len(document["contracts"]), 4)
            self.assertEqual(len(document["artifacts"]), 2)
            self.assertTrue(
                all(
                    artifact["repositoryId"] == "ordivon-computing"
                    for artifact in document["artifacts"]
                )
            )
            self.assertEqual(document["integrity"], CONFORMANCE.integrity(document))
            from research.evidence.validate_system_snapshot import validate

            validate(document, repository_roots=roots)

    def test_host_pin_must_be_in_captured_computing_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest, roots, revision = self._fixture(Path(temporary))
            host_path = roots["ordivon-host"] / "pyproject.toml"
            host_path.write_text(
                host_path.read_text().replace(f"@{revision}#", "@deadbeef#")
            )
            with self.assertRaisesRegex(ValueError, "exactly one full Computing protocol pin"):
                CONFORMANCE.verify_host_pin(manifest, roots)


class SerializationTests(unittest.TestCase):
    def test_write_json_is_atomic_and_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "nested" / "receipt.json"
            CONFORMANCE.write_json(path, {"value": 1})
            self.assertEqual(json.loads(path.read_text()), {"value": 1})
            self.assertFalse(path.with_name(path.name + ".tmp").exists())


class GateLauncherContractTests(unittest.TestCase):
    def test_public_gate_delegates_to_repo_owned_environment(self) -> None:
        readme = (ROOT / "README.md").read_text()
        workflow = (ROOT / ".github" / "workflows" / "deterministic-contracts.yml").read_text()
        launcher = (ROOT / "scripts" / "run_conformance_gate.py").read_text()
        owner_environment = (ROOT / "scripts" / "owner-environment").read_text()
        requirements = (ROOT / "requirements-conformance.txt").read_text()
        lock = (ROOT / "requirements-conformance.lock.txt").read_text()

        public_command = "python scripts/run_conformance_gate.py"
        self.assertIn(public_command, readme)
        self.assertIn(public_command, workflow)
        self.assertNotIn("python3.12 scripts/ordivon_conformance.py gate", readme)
        self.assertIn('ROOT / "scripts" / "owner-environment"', launcher)
        self.assertIn('command = [str(entry), "test"', launcher)
        self.assertIn('python_version=${ORDIVON_OWNER_PYTHON:-3.12.13}', owner_environment)
        self.assertIn('requirements-conformance.lock.txt', owner_environment)
        self.assertIn('"$mise_bin" install', owner_environment)
        self.assertIn("jsonschema==4.25.1", requirements)
        self.assertIn("jsonschema==4.25.1", lock)
        self.assertIn("ruff==0.15.14", lock)


if __name__ == "__main__":
    unittest.main()
