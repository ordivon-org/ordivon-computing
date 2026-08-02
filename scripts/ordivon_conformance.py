from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "projects" / "conformance.toml"
REGISTRY = ROOT / "projects" / "registry.yaml"
_PROTOCOL_PIN = re.compile(
    r"ordivon-computing\.git@([0-9a-f]{40})#subdirectory=packages/ordivon-protocol"
)
_ALLOWED_RELATIONSHIPS = {
    "producer",
    "direct-consumer",
    "semantic-backend",
    "infrastructure-consumer",
    "domain-consumer",
    "research-consumer",
    "interface-consumer",
}


@dataclass(frozen=True)
class ProtocolSpec:
    package: str
    version: str
    source: PurePosixPath
    release: PurePosixPath
    profiles: tuple[str, ...]


@dataclass(frozen=True)
class ProjectSpec:
    id: str
    repository: str
    local_path: str
    relationship: str
    profiles: tuple[str, ...]
    protocol_requirement: str | None = None
    dependency_file: PurePosixPath | None = None
    vector_manifest: PurePosixPath | None = None


@dataclass(frozen=True)
class ConformanceManifest:
    schema_version: int
    registry: str
    protocol: ProtocolSpec
    projects: tuple[ProjectSpec, ...]

    def project(self, project_id: str) -> ProjectSpec:
        for project in self.projects:
            if project.id == project_id:
                return project
        raise ValueError(f"unknown project: {project_id}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def canonical_bytes(document: dict[str, Any]) -> bytes:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def integrity(document: dict[str, Any]) -> dict[str, str]:
    return {
        "algorithm": "sha256",
        "canonicalization": "json-sort-keys-v1",
        "payloadDigest": "sha256:" + hashlib.sha256(canonical_bytes(document)).hexdigest(),
    }


def file_digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _unique_strings(value: Any, label: str) -> tuple[str, ...]:
    require(isinstance(value, list) and value, f"{label} must be a non-empty list")
    require(all(isinstance(item, str) and item for item in value), f"{label} entries must be strings")
    require(len(value) == len(set(value)), f"{label} entries must be unique")
    return tuple(value)


def load_manifest(path: Path = DEFAULT_MANIFEST, *, repository_root: Path = ROOT) -> ConformanceManifest:
    document = tomllib.loads(path.read_text())
    require(
        set(document) == {"schema_version", "registry", "protocol", "projects"},
        "conformance manifest top-level fields are invalid",
    )
    require(document["schema_version"] == 1, "unsupported conformance schema")
    require(document["registry"] == "ordivon-conformance", "invalid conformance registry identity")

    raw_protocol = document["protocol"]
    require(
        isinstance(raw_protocol, dict)
        and set(raw_protocol) == {"package", "version", "source", "release", "profiles"},
        "protocol declaration fields are invalid",
    )
    source = PurePosixPath(raw_protocol["source"])
    release = PurePosixPath(raw_protocol["release"])
    require(not source.is_absolute() and ".." not in source.parts, "protocol source must be relative")
    require(not release.is_absolute() and ".." not in release.parts, "protocol release must be relative")
    protocol = ProtocolSpec(
        package=raw_protocol["package"],
        version=raw_protocol["version"],
        source=source,
        release=release,
        profiles=_unique_strings(raw_protocol["profiles"], "protocol profiles"),
    )
    require(protocol.package == "ordivon-protocol", "unexpected protocol package")

    raw_projects = document["projects"]
    require(isinstance(raw_projects, list) and raw_projects, "projects must be non-empty")
    projects: list[ProjectSpec] = []
    for raw in raw_projects:
        require(isinstance(raw, dict), "project declaration must be an object")
        required = {"id", "relationship", "profiles"}
        optional = {"protocol_requirement", "dependency_file", "vector_manifest"}
        require(set(raw) >= required and set(raw) <= required | optional, "project declaration fields are invalid")
        project_id = raw["id"]
        require(bool(re.fullmatch(r"ordivon-[a-z0-9-]+", project_id)), f"invalid project id: {project_id}")
        expected_repository = f"https://github.com/zycxfyh/{project_id}"
        require(raw["relationship"] in _ALLOWED_RELATIONSHIPS, f"invalid relationship for {project_id}")
        dependency_file = raw.get("dependency_file")
        dependency_path = None if dependency_file is None else PurePosixPath(dependency_file)
        vector_manifest = raw.get("vector_manifest")
        vector_path = None if vector_manifest is None else PurePosixPath(vector_manifest)
        for candidate, label in ((dependency_path, "dependency_file"), (vector_path, "vector_manifest")):
            if candidate is not None:
                require(
                    not candidate.is_absolute() and ".." not in candidate.parts,
                    f"{label} must be relative: {project_id}",
                )
        project = ProjectSpec(
            id=project_id,
            repository=expected_repository,
            local_path=project_id,
            relationship=raw["relationship"],
            profiles=_unique_strings(raw["profiles"], f"{project_id} profiles"),
            protocol_requirement=raw.get("protocol_requirement"),
            dependency_file=dependency_path,
            vector_manifest=vector_path,
        )
        pin_count = sum(item is not None for item in (project.dependency_file, project.vector_manifest))
        require(pin_count <= 1, f"project declares multiple protocol pin mechanisms: {project_id}")
        require(
            (project.protocol_requirement is None) == (pin_count == 0),
            f"protocol requirement and one pin mechanism must be declared together: {project_id}",
        )
        projects.append(project)

    ids = [project.id for project in projects]
    require(len(ids) == len(set(ids)), "project ids must be unique")
    require(ids[0] == "ordivon-computing", "ordivon-computing must be the first project")
    require(projects[0].relationship == "producer", "ordivon-computing must produce the protocol")
    host = next((project for project in projects if project.id == "ordivon-host"), None)
    require(host is not None and host.relationship == "direct-consumer", "ordivon-host must be a direct consumer")
    require(host.protocol_requirement == protocol.version, "Host protocol requirement must match the promoted version")
    game = next((project for project in projects if project.id == "ordivon-game"), None)
    require(game is not None and game.vector_manifest is not None, "Game must declare a protocol vector manifest")
    require(game.protocol_requirement == protocol.version, "Game protocol requirement must match the promoted version")

    package_manifest = repository_root / protocol.source / "pyproject.toml"
    require(package_manifest.is_file(), "protocol package manifest is missing")
    package_document = tomllib.loads(package_manifest.read_text())
    require(package_document["project"]["name"] == protocol.package, "protocol package name differs")
    require(package_document["project"]["version"] == protocol.version, "protocol package version differs")
    require((repository_root / protocol.release).is_file(), "protocol release manifest is missing")

    registry_ids = tuple(
        match.group(1)
        for line in REGISTRY.read_text().splitlines()
        if (match := re.fullmatch(r"  - id: (ordivon-[a-z0-9-]+)", line))
    )
    registry_positions = {project_id: index for index, project_id in enumerate(registry_ids)}
    require(set(ids) <= set(registry_ids), "conformance references a project outside projects/registry.yaml")
    require(
        tuple(ids) == tuple(sorted(ids, key=registry_positions.__getitem__)),
        "conformance project order differs from projects/registry.yaml",
    )

    return ConformanceManifest(
        schema_version=document["schema_version"],
        registry=document["registry"],
        protocol=protocol,
        projects=tuple(projects),
    )


def _run_git(root: Path, args: Sequence[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise ValueError(f"git {' '.join(args)} failed for {root}: {result.stderr.strip()}")
    return result


def git_blob(root: Path, revision: str, path: PurePosixPath) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path.as_posix()}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"cannot read {path} at {revision}")
    return result.stdout


def normalize_repository_url(value: str) -> str:
    value = value.strip().removesuffix("/")
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value.removeprefix("git@github.com:")
    elif value.startswith("ssh://git@github.com/"):
        value = "https://github.com/" + value.removeprefix("ssh://git@github.com/")
    return value.removesuffix(".git")


def git_info(project: ProjectSpec, root: Path) -> dict[str, Any]:
    require(root.is_dir(), f"repository root is missing: {project.id}={root}")
    revision = _run_git(root, ["rev-parse", "HEAD"]).stdout.strip()
    require(bool(re.fullmatch(r"[0-9a-f]{40}", revision)), f"invalid Git revision: {project.id}")
    status = _run_git(root, ["status", "--porcelain=v1"]).stdout
    branch_result = _run_git(root, ["symbolic-ref", "--quiet", "--short", "HEAD"], check=False)
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    remote_result = _run_git(root, ["remote", "get-url", "origin"], check=False)
    remote = remote_result.stdout.strip() if remote_result.returncode == 0 else project.repository
    normalized_remote = normalize_repository_url(remote)
    require(
        normalized_remote == normalize_repository_url(project.repository),
        f"origin differs for {project.id}: {remote}",
    )
    return {
        "id": project.id,
        "repository": project.repository,
        "revision": revision,
        "branch": branch,
        "clean": not bool(status),
        "relationship": project.relationship,
        "profiles": list(project.profiles),
    }


def parse_root_bindings(bindings: Iterable[str]) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    for binding in bindings:
        project_id, separator, raw_path = binding.partition("=")
        require(bool(separator and project_id and raw_path), "repository root must use ID=PATH")
        require(project_id not in roots, f"duplicate repository root: {project_id}")
        roots[project_id] = Path(raw_path).expanduser().resolve()
    return roots


def resolve_roots(
    manifest: ConformanceManifest,
    overrides: dict[str, Path],
    *,
    repository_root: Path = ROOT,
    require_all: bool = False,
) -> tuple[dict[str, Path], list[str]]:
    known = {project.id for project in manifest.projects}
    require(set(overrides) <= known, "repository root override references an unknown project")
    roots: dict[str, Path] = {}
    missing: list[str] = []
    sibling_root = repository_root.parent
    for project in manifest.projects:
        if project.id in overrides:
            candidate = overrides[project.id]
        elif project.id == "ordivon-computing":
            candidate = repository_root
        else:
            candidate = sibling_root / project.local_path
        if candidate.is_dir():
            roots[project.id] = candidate
        else:
            missing.append(project.id)
    if require_all:
        require(not missing, "missing repositories: " + ", ".join(missing))
    return roots, missing


def verify_host_pin(
    manifest: ConformanceManifest, roots: dict[str, Path]
) -> dict[str, Any] | None:
    if "ordivon-host" not in roots or "ordivon-computing" not in roots:
        return None
    host = manifest.project("ordivon-host")
    require(host.dependency_file is not None, "Host dependency file is not declared")
    dependency_path = roots[host.id] / host.dependency_file
    require(dependency_path.is_file(), "Host dependency file is missing")
    matches = _PROTOCOL_PIN.findall(dependency_path.read_text())
    require(len(matches) == 1, "Host must contain exactly one full Computing protocol pin")
    pin = matches[0]
    computing_root = roots["ordivon-computing"]
    _run_git(computing_root, ["cat-file", "-e", f"{pin}^{{commit}}"])
    ancestor = _run_git(computing_root, ["merge-base", "--is-ancestor", pin, "HEAD"], check=False)
    require(ancestor.returncode == 0, "Host protocol pin is not in the current Computing history")
    package_bytes = git_blob(
        computing_root,
        pin,
        manifest.protocol.source / "pyproject.toml",
    )
    package_document = tomllib.loads(package_bytes.decode("utf-8"))
    pinned_version = package_document["project"]["version"]
    require(pinned_version == host.protocol_requirement, "Host protocol pin resolves to another version")
    return {
        "projectId": host.id,
        "dependencyFile": host.dependency_file.as_posix(),
        "computingRevision": pin,
        "protocolVersion": pinned_version,
        "ancestorOfCapturedComputing": True,
    }


def revision_vector(
    manifest: ConformanceManifest,
    roots: dict[str, Path],
    missing: list[str],
) -> dict[str, Any]:
    repositories = [
        git_info(project, roots[project.id])
        for project in manifest.projects
        if project.id in roots
    ]
    computing = next(item for item in repositories if item["id"] == "ordivon-computing")
    document: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon-revision-vector",
        "capturedAt": utc_now(),
        "protocol": {
            "package": manifest.protocol.package,
            "version": manifest.protocol.version,
            "sourceRepositoryId": "ordivon-computing",
            "sourceRevision": computing["revision"],
            "profiles": list(manifest.protocol.profiles),
        },
        "repositories": repositories,
        "missingProjectIds": missing,
    }
    host_pin = verify_host_pin(manifest, roots)
    if host_pin is not None:
        document["hostProtocolPin"] = host_pin
    document["integrity"] = integrity(document)
    return document


def build_system_snapshot(
    manifest: ConformanceManifest,
    roots: dict[str, Path],
    *,
    snapshot_id: str,
    purpose: str,
) -> dict[str, Any]:
    require(bool(snapshot_id) and "current" not in snapshot_id and "latest" not in snapshot_id, "snapshot id must be historical")
    require(bool(purpose.strip()), "snapshot purpose is required")
    repository_entries: list[dict[str, Any]] = []
    for project in manifest.projects:
        if project.id not in roots:
            continue
        info = git_info(project, roots[project.id])
        require(info["clean"], f"snapshot requires a clean repository: {project.id}")
        repository_entries.append(
            {
                "id": info["id"],
                "repository": info["repository"],
                "revision": info["revision"],
                "clean": True,
            }
        )
    require(repository_entries, "snapshot requires at least one repository")
    computing = next(entry for entry in repository_entries if entry["id"] == "ordivon-computing")
    computing_root = roots["ordivon-computing"]
    revision = computing["revision"]
    schema_paths = (
        PurePosixPath("packages/ordivon-protocol/src/ordivon_protocol/schemas/effect-envelope-v1.schema.json"),
        PurePosixPath("packages/ordivon-protocol/src/ordivon_protocol/schemas/tool-contract-v1.schema.json"),
        PurePosixPath("packages/ordivon-protocol/src/ordivon_protocol/schemas/effect-binding-v1.schema.json"),
        PurePosixPath("packages/ordivon-protocol/src/ordivon_protocol/schemas/host-workload-v1.schema.json"),
    )
    contracts = [
        {
            "id": f"ordivon-protocol:{path.name.removesuffix('.schema.json')}",
            "revision": manifest.protocol.version,
            "digest": file_digest(git_blob(computing_root, revision, path)),
            "source": path.as_posix(),
        }
        for path in schema_paths
    ]
    vector_paths = (
        PurePosixPath(
            "packages/ordivon-protocol/src/ordivon_protocol/vectors/canonical-vectors.json"
        ),
        PurePosixPath(
            "packages/ordivon-protocol/src/ordivon_protocol/vectors/host-workload-vectors-v1.json"
        ),
    )
    artifacts = [
        {
            "id": f"ordivon-protocol:{path.name.removesuffix('.json')}",
            "kind": "conformance-vectors",
            "digest": file_digest(git_blob(computing_root, revision, path)),
            "path": path.as_posix(),
            "repositoryId": "ordivon-computing",
        }
        for path in vector_paths
    ]
    document: dict[str, Any] = {
        "schemaVersion": 1,
        "snapshotId": snapshot_id,
        "capturedAt": utc_now(),
        "purpose": purpose,
        "repositories": repository_entries,
        "services": [],
        "contracts": contracts,
        "artifacts": artifacts,
        "environment": {"protocolVersion": manifest.protocol.version},
    }
    document["integrity"] = integrity(document)
    return document


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def _gate_commands() -> list[tuple[str, list[str], Path, dict[str, str]]]:
    python = sys.executable
    ruff = shutil.which("ruff")
    rustc = shutil.which("rustc")
    vale = shutil.which("vale")
    markdownlint = shutil.which("markdownlint-cli2")
    cspell = shutil.which("cspell")
    lychee = shutil.which("lychee")
    require(ruff is not None, "ruff is required for the conformance gate")
    require(rustc is not None, "rustc is required for the conformance gate")
    require(vale is not None, "vale is required for the content gate; run mise install")
    require(markdownlint is not None, "markdownlint-cli2 is required for the content gate; run mise install")
    require(cspell is not None, "cspell is required for the content gate; run mise install")
    require(lychee is not None, "lychee is required for the content gate; run mise install")
    content_tool_paths = [
        "docs/content-engineering/README.md",
        "packages/content-contract/README.md",
        "packages/content-cli/README.md",
        *[path.relative_to(ROOT).as_posix() for path in sorted((ROOT / "packages" / "content-templates").rglob("*.md"))],
        *[path.relative_to(ROOT).as_posix() for path in sorted((ROOT / "packages" / "content-fixtures" / "valid").rglob("*.md"))],
        "research/evidence/content-engineering-p0-baseline.md",
    ]
    static_paths = [
        "packages/ordivon-protocol/src",
        "packages/ordivon-protocol/tests",
        "packages/content-cli/src",
        "packages/content-cli/tests",
        "research/experiments/external-semantic-contract-v0/integration",
        "research/experiments/external-semantic-contract-v0/tests",
        "research/experiments/external-semantic-contract-v0/scripts",
        "research/experiments/semantic-core-v0/src",
        "research/experiments/semantic-core-v0/tests",
        "research/experiments/semantic-core-v0/scripts",
        "research/experiments/task-continuation-v0/src",
        "research/experiments/task-continuation-v0/tests",
        "research/experiments/task-continuation-v0/scripts",
        "research/experiments/harness-evaluation-v0/validate_evaluation_evidence.py",
        "research/experiments/harness-evaluation-v0/tests",
        "research/evidence",
        "scripts/check_foundational_docs.py",
        "scripts/check_research_portfolio.py",
        "scripts/render_research_portfolio.py",
        "scripts/check_protocol_release.py",
        "scripts/check_protocol_consumers.py",
        "scripts/ordivon_content.py",
        "scripts/ordivon_conformance.py",
    ]
    commands: list[tuple[str, list[str], Path, dict[str, str]]] = [
        ("compileall", [python, "-m", "compileall", "-q", *static_paths], ROOT, {}),
        ("ruff", [ruff, "check", *static_paths], ROOT, {}),
        (
            "content-cli-tests",
            [python, "-m", "unittest", "discover", "-s", "packages/content-cli/tests"],
            ROOT,
            {"PYTHONPATH": "packages/content-cli/src"},
        ),
        (
            "content-managed-paths",
            [
                python,
                "scripts/ordivon_content.py",
                "check",
                "--root",
                ".",
                "--mode",
                "strict",
                "--receipt",
                "/tmp/ordivon-content-check.json",
            ],
            ROOT,
            {},
        ),
        ("content-vale", [vale, *content_tool_paths], ROOT, {}),
        ("content-markdownlint", [markdownlint, *content_tool_paths], ROOT, {}),
        (
            "content-spelling",
            [cspell, "lint", "--no-progress", "--no-summary", *content_tool_paths],
            ROOT,
            {},
        ),
        (
            "content-links",
            [lychee, "--config", "lychee.toml", *content_tool_paths],
            ROOT,
            {},
        ),
        (
            "foundational-docs",
            [python, "scripts/check_foundational_docs.py"],
            ROOT,
            {},
        ),
        (
            "research-portfolio",
            [python, "scripts/check_research_portfolio.py"],
            ROOT,
            {},
        ),
        (
            "research-portfolio-view",
            [python, "scripts/render_research_portfolio.py", "--check"],
            ROOT,
            {},
        ),
        (
            "protocol-release",
            [python, "scripts/check_protocol_release.py"],
            ROOT,
            {},
        ),
        (
            "protocol",
            [python, "-m", "unittest", "discover", "-s", "tests"],
            ROOT / "packages" / "ordivon-protocol",
            {"PYTHONPATH": "src"},
        ),
        (
            "external-contract",
            [python, "-m", "unittest", "discover", "-s", "tests"],
            ROOT / "research" / "experiments" / "external-semantic-contract-v0",
            {"PYTHONPATH": "../../../packages/ordivon-protocol/src:../semantic-core-v0/src:."},
        ),
        (
            "semantic-core",
            [python, "-m", "unittest", "discover", "-s", "tests"],
            ROOT / "research" / "experiments" / "semantic-core-v0",
            {"PYTHONPATH": "../../../packages/ordivon-protocol/src:src"},
        ),
        (
            "task-continuation",
            [python, "-m", "unittest", "discover", "-s", "tests"],
            ROOT / "research" / "experiments" / "task-continuation-v0",
            {
                "PYTHONPATH": "../../../packages/ordivon-protocol/src:src:../external-semantic-contract-v0:../semantic-core-v0/src",
                "TMPDIR": "/tmp",
            },
        ),
        (
            "track-r-evaluation",
            [
                python,
                "-m",
                "unittest",
                "discover",
                "-s",
                "research/experiments/harness-evaluation-v0/tests",
                "-p",
                "test_*.py",
            ],
            ROOT,
            {"PYTHONPATH": "."},
        ),
        (
            "evidence-and-conformance",
            [python, "-m", "unittest", "discover", "-s", "research/evidence/tests"],
            ROOT,
            {"PYTHONPATH": "."},
        ),
        (
            "rust-canonical-build",
            [
                rustc,
                "--edition=2021",
                "research/experiments/external-semantic-contract-v0/rust/canonical-verifier/main.rs",
                "-o",
                "/tmp/ordivon-canonical-verifier",
            ],
            ROOT,
            {},
        ),
        (
            "rust-canonical-vectors",
            [
                "/tmp/ordivon-canonical-verifier",
                "packages/ordivon-protocol/src/ordivon_protocol/vectors/canonical-vectors.tsv",
            ],
            ROOT,
            {},
        ),
    ]
    return commands


def run_gate(receipt_path: Path | None) -> int:
    manifest = load_manifest()
    started = time.monotonic()
    steps: list[dict[str, Any]] = []
    failure: str | None = None
    for step_id, command, cwd, extra_environment in _gate_commands():
        step_started = time.monotonic()
        environment = os.environ.copy()
        environment.update(extra_environment)
        print(f"== {step_id} ==", flush=True)
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        steps.append(
            {
                "id": step_id,
                "command": command,
                "cwd": cwd.relative_to(ROOT).as_posix() or ".",
                "elapsedMs": round((time.monotonic() - step_started) * 1000),
                "exitCode": completed.returncode,
            }
        )
        if completed.returncode != 0:
            failure = step_id
            break
    revision = _run_git(ROOT, ["rev-parse", "HEAD"]).stdout.strip()
    receipt: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon-conformance-gate",
        "capturedAt": utc_now(),
        "repositoryRevision": revision,
        "protocolVersion": manifest.protocol.version,
        "status": "failed" if failure else "passed",
        "failedStep": failure,
        "elapsedMs": round((time.monotonic() - started) * 1000),
        "steps": steps,
    }
    receipt["integrity"] = integrity(receipt)
    if receipt_path is not None:
        write_json(receipt_path, receipt)
    return 1 if failure else 0


def command_manifest(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    print(
        json.dumps(
            {
                "schemaVersion": manifest.schema_version,
                "registry": manifest.registry,
                "protocolVersion": manifest.protocol.version,
                "protocolRelease": manifest.protocol.release.as_posix(),
                "projectIds": [project.id for project in manifest.projects],
            },
            indent=2,
        )
    )
    return 0


def _resolved(args: argparse.Namespace) -> tuple[ConformanceManifest, dict[str, Path], list[str]]:
    manifest = load_manifest(args.manifest)
    roots, missing = resolve_roots(
        manifest,
        parse_root_bindings(args.repository_root),
        require_all=args.require_all,
    )
    return manifest, roots, missing


def command_vector(args: argparse.Namespace) -> int:
    manifest, roots, missing = _resolved(args)
    document = revision_vector(manifest, roots, missing)
    if args.require_clean:
        dirty = [item["id"] for item in document["repositories"] if not item["clean"]]
        require(not dirty, "dirty repositories: " + ", ".join(dirty))
    if args.output:
        write_json(args.output, document)
    else:
        print(json.dumps(document, indent=2, ensure_ascii=False))
    return 0


def command_snapshot(args: argparse.Namespace) -> int:
    manifest, roots, missing = _resolved(args)
    require(not missing or not args.require_all, "snapshot is missing required repositories")
    document = build_system_snapshot(
        manifest,
        roots,
        snapshot_id=args.snapshot_id,
        purpose=args.purpose,
    )
    write_json(args.output, document)
    sys.path.insert(0, str(ROOT))
    from research.evidence.validate_system_snapshot import validate

    validate(document, repository_roots=roots)
    print(f"{args.output}: {document['snapshotId']} {document['integrity']['payloadDigest']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ordivon protocol, revision-vector, and cross-repository conformance base"
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest_parser = subparsers.add_parser("manifest", help="validate the conformance manifest")
    manifest_parser.set_defaults(handler=command_manifest)

    gate_parser = subparsers.add_parser("gate", help="run the complete deterministic Computing gate")
    gate_parser.add_argument("--receipt", type=Path)
    gate_parser.set_defaults(handler=lambda args: run_gate(args.receipt))

    for name, handler in (("vector", command_vector), ("snapshot", command_snapshot)):
        child = subparsers.add_parser(name)
        child.add_argument(
            "--repository-root",
            action="append",
            default=[],
            metavar="ID=PATH",
        )
        child.add_argument("--require-all", action="store_true")
        if name == "vector":
            child.add_argument("--require-clean", action="store_true")
            child.add_argument("--output", type=Path)
        else:
            child.add_argument("--snapshot-id", required=True)
            child.add_argument("--purpose", required=True)
            child.add_argument("--output", type=Path, required=True)
        child.set_defaults(handler=handler)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (OSError, ValueError, KeyError, tomllib.TOMLDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
