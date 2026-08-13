from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import time
import tomllib
from typing import Any

ROOTS = [pathlib.Path('/root/projects'), pathlib.Path('/root')]
PROJECT_NAMES = [
    'ordivon-computing',
    'ordivon-runtime',
    'ordivon-host',
    'ordivon-harness',
    'ordivon-world',
    'ordivon-game',
    'ordivon-security',
    'ordivon-finance',
    'ordivon-human',
    'ordivon-studio',
    'ordivon-web',
    'workstation-lab',
]

SURFACE_NAME_RE = re.compile(
    r'(api|cli|mcp|server|tool|capabil|surface|inspect|status|doctor|manifest|projection|adapter|provider|recover)',
    re.I,
)
EXPERIMENT_RE = re.compile(r'(acceptance|experiment|fixture|research|archive|eval)', re.I)


def run(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


def repo_path(name: str) -> pathlib.Path:
    if name == 'workstation-lab':
        return pathlib.Path('/root/workstation-lab')
    return pathlib.Path('/root/projects') / name


def sha256_bytes(value: bytes) -> str:
    return 'sha256:' + hashlib.sha256(value).hexdigest()


def doc_projection(path: pathlib.Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    raw = path.read_bytes()
    text = raw.decode('utf-8', errors='replace')
    lines = text.splitlines()
    headings = [line.strip() for line in lines if re.match(r'^#{1,3} ', line)]
    tokens = ['quick start', 'start here', 'agent', 'capabilit', 'status', 'recover', 'mcp', 'cli', 'tool', 'current', 'next']
    lower = text.lower()
    return {
        'path': str(path.name if path.parent.name not in {'docs'} else pathlib.Path('docs') / path.name),
        'bytes': len(raw),
        'digest': sha256_bytes(raw),
        'lines': len(lines),
        'headingCount': len(headings),
        'firstHeadings': headings[:16],
        'keywordPresence': {token: token in lower for token in tokens},
    }


def package_projection(repo: pathlib.Path) -> dict[str, Any]:
    value: dict[str, Any] = {}
    pyproject = repo / 'pyproject.toml'
    if pyproject.exists():
        parsed = tomllib.loads(pyproject.read_text())
        project = parsed.get('project', {})
        value['pythonScripts'] = project.get('scripts', {})
        value['pythonOptionalDependencyGroups'] = sorted(project.get('optional-dependencies', {}).keys())
    package = repo / 'package.json'
    if package.exists():
        parsed = json.loads(package.read_text())
        value['packageScripts'] = parsed.get('scripts', {})
        value['packageBin'] = parsed.get('bin', {})
        value['packageExports'] = parsed.get('exports', {})
    cargo = repo / 'Cargo.toml'
    if cargo.exists():
        parsed = tomllib.loads(cargo.read_text())
        value['cargoWorkspaceMembers'] = parsed.get('workspace', {}).get('members', [])
        value['cargoBins'] = parsed.get('bin', [])
    return value


def tracked_surface_files(repo: pathlib.Path) -> dict[str, Any]:
    files = run('git', 'ls-files', cwd=repo).splitlines()
    candidates = [f for f in files if SURFACE_NAME_RE.search(pathlib.PurePosixPath(f).name)]
    experiment_like = [f for f in candidates if EXPERIMENT_RE.search(f)]
    product_like = [f for f in candidates if f not in experiment_like]
    return {
        'candidateCount': len(candidates),
        'productLikeCount': len(product_like),
        'experimentLikeCount': len(experiment_like),
        'productLikeSample': product_like[:80],
        'experimentLikeSample': experiment_like[:80],
    }


def repo_projection(name: str) -> dict[str, Any]:
    repo = repo_path(name)
    head = run('git', 'rev-parse', 'HEAD', cwd=repo)
    status = run('git', 'status', '--porcelain=v1', cwd=repo)
    docs = []
    for rel in ['README.md', 'AGENTS.md', 'ARCHITECTURE.md', 'STATUS.md', 'docs/STATUS.md', 'docs/status.md']:
        value = doc_projection(repo / rel)
        if value is not None:
            value['path'] = rel
            docs.append(value)
    package = package_projection(repo)
    py_scripts = package.get('pythonScripts', {})
    pkg_scripts = package.get('packageScripts', {})
    return {
        'owner': name,
        'repo': str(repo),
        'headRevision': head,
        'dirty': bool(status),
        'dirtyPaths': status.splitlines()[:80] if status else [],
        'docs': docs,
        'package': package,
        'declaredCommandCounts': {
            'pythonScripts': len(py_scripts),
            'packageScripts': len(pkg_scripts),
            'packageBin': len(package.get('packageBin', {})),
        },
        'surfaceFiles': tracked_surface_files(repo),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    owners = [repo_projection(name) for name in PROJECT_NAMES]
    evidence = {
        'schemaVersion': 1,
        'kind': 'ordivon.computing.agent-consumption-surface-census',
        'observedAtMs': int(time.time() * 1000),
        'authorityNote': 'Derived cross-owner observation only; owner repositories remain authoritative.',
        'owners': owners,
    }
    payload = json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + '\n'
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload)
    print(json.dumps({
        'output': str(output),
        'owners': len(owners),
        'dirtyOwners': [owner['owner'] for owner in owners if owner['dirty']],
        'digest': sha256_bytes(payload.encode()),
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
