#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "projects" / "registry.yaml"
JSON_OUT = ROOT / "projects" / "system-map.json"
MD_OUT = ROOT / "projects" / "SYSTEM-MAP.md"


def parse_registry() -> list[dict[str, str]]:
    projects: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in REGISTRY.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"  - id: (ordivon-[a-z0-9-]+)", raw)
        if match:
            if current is not None:
                projects.append(current)
            current = {"id": match.group(1)}
            continue
        if current is None:
            continue
        match = re.fullmatch(r"    (repository|role): (.+)", raw)
        if match:
            current[match.group(1)] = match.group(2)
    if current is not None:
        projects.append(current)
    if not projects:
        raise RuntimeError("project registry is empty")
    for project in projects:
        missing = {"id", "repository", "role"} - set(project)
        if missing:
            raise RuntimeError(
                f"{project.get('id', '<unknown>')} missing stable fields: {sorted(missing)}"
            )
    ids = [project["id"] for project in projects]
    if len(ids) != len(set(ids)):
        raise RuntimeError("project registry contains duplicate ids")
    return projects


def outputs() -> tuple[str, str]:
    projects = parse_registry()
    payload = {
        "schemaVersion": 1,
        "kind": "ordivon.project-family-system-map",
        "truthRole": "generated-computing-project-family-packaging-projection",
        "source": "projects/registry.yaml",
        "sourceDigest": "sha256:" + hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
        "projectCount": len(projects),
        "projects": projects,
        "doesNotOwn": [
            "current semantic owner identity",
            "current owner display name",
            "owner authority",
            "owner semantic currentness",
            "current implementation state",
            "deployment state",
            "research maturity",
            "runtime health",
            "task status",
        ],
    }
    json_text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    rows = "\n".join(
        f"| `{item['id']}` | {item['role']} | {item['repository']} |" for item in projects
    )
    md_text = (
        "# Generated Project-Family System Map\n\n"
        "This file is generated from [`registry.yaml`](registry.yaml), Computing's non-exhaustive project-family packaging/compatibility roster. "
        "It is not a current semantic-owner registry; do not hand-maintain packaging counts or recorded roles here.\n\n"
        f"**Registered Computing packaging identities: {len(projects)}**\n\n"
        "| Packaging identity | Recorded role | Repository |\n"
        "| --- | --- | --- |\n"
        f"{rows}\n\n"
        "This projection deliberately excludes current semantic owner identity/name/authority/currentness as well as mutable maturity, deployment, Task, service, and live-state claims. "
        "For current semantic ownership, follow owner-native authority; use Atlas generated owner/current-recovery projections where covered. "
        "Historical packaging identities may remain for Computing lineage. Regenerate with `python3 scripts/generate_project_family.py --write`; "
        "verify with `--check`.\n"
    )
    return json_text, md_text


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    json_text, md_text = outputs()
    if args.write:
        JSON_OUT.write_text(json_text, encoding="utf-8")
        MD_OUT.write_text(md_text, encoding="utf-8")
        print(
            "project-family map: wrote "
            f"{JSON_OUT.relative_to(ROOT)} and {MD_OUT.relative_to(ROOT)}"
        )
        return 0
    failures: list[str] = []
    for path, expected in ((JSON_OUT, json_text), (MD_OUT, md_text)):
        if not path.is_file():
            failures.append(f"missing {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            failures.append(f"stale {path.relative_to(ROOT)}")
    if failures:
        for failure in failures:
            print(f"project-family map: {failure}")
        return 1
    print("project-family map: current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
