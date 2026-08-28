from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

FOUNDATION_PROJECTS = (
    ("ordivon-host", "ordivon-host"),
    ("ordivon-runtime", "ordivon-runtime"),
    ("ordivon-harness", "ordivon-harness"),
    ("ordivon-world", "ordivon-world"),
)


class CurrentnessError(RuntimeError):
    pass


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["/usr/bin/git", "-C", str(repo), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )


def _resolve(repo: Path, ref: str) -> str | None:
    result = _git(repo, "rev-parse", "--verify", ref, check=False)
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    if len(value) != 40:
        raise CurrentnessError(f"{repo}: {ref} did not resolve to an exact commit")
    return value


def _is_ancestor(repo: Path, ancestor: str, descendant: str) -> bool:
    result = _git(repo, "merge-base", "--is-ancestor", ancestor, descendant, check=False)
    if result.returncode not in (0, 1):
        raise CurrentnessError(
            f"{repo}: ancestry check failed for {ancestor} -> {descendant}: {result.stderr.strip()}"
        )
    return result.returncode == 0


def _count(repo: Path, revision_range: str) -> int:
    return int(_git(repo, "rev-list", "--count", revision_range).stdout.strip())


def relation(repo: Path, left: str | None, right: str | None) -> dict[str, Any]:
    if left is None or right is None:
        return {"state": "unavailable", "ahead": None, "behind": None}
    if left == right:
        return {"state": "exact", "ahead": 0, "behind": 0}
    if _is_ancestor(repo, right, left):
        return {"state": "left_ahead", "ahead": _count(repo, f"{right}..{left}"), "behind": 0}
    if _is_ancestor(repo, left, right):
        return {"state": "left_behind", "ahead": 0, "behind": _count(repo, f"{left}..{right}")}
    return {
        "state": "diverged",
        "ahead": _count(repo, f"{right}..{left}"),
        "behind": _count(repo, f"{left}..{right}"),
    }


def _fetch_origin_main(repo: Path) -> dict[str, Any]:
    result = _git(repo, "fetch", "--prune", "origin", "main", check=False)
    return {
        "attempted": True,
        "ok": result.returncode == 0,
        "stderr": result.stderr.strip() or None,
    }


def _worktree(repo: Path) -> dict[str, Any]:
    head = _resolve(repo, "HEAD")
    if head is None:
        raise CurrentnessError(f"{repo}: HEAD is unavailable")
    branch_result = _git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    dirty_paths = [
        line[3:]
        for line in _git(repo, "status", "--porcelain=v1").stdout.splitlines()
        if len(line) >= 4
    ]
    return {
        "head": head,
        "branch": branch,
        "detached": branch is None,
        "clean": not dirty_paths,
        "dirtyPaths": dirty_paths,
    }


def _runtime_live(repo: Path) -> dict[str, Any]:
    script = repo / "scripts" / "ordivon-runtime-status"
    if not script.is_file():
        return {"state": "unavailable", "reason": "runtime status script is absent"}
    result = subprocess.run(
        [sys.executable, str(script), "--health", "--json"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return {
            "state": "error",
            "reason": "runtime owner-native status failed",
            "stderr": result.stderr.strip() or None,
        }
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        return {"state": "error", "reason": f"runtime status returned invalid JSON: {error}"}
    deployment = report.get("deployment")
    commit = deployment.get("commit") if isinstance(deployment, dict) else None
    return {
        "state": "observed",
        "health": report.get("status"),
        "deployedRevision": commit if isinstance(commit, str) else None,
        "generatedAtMs": report.get("generatedAtMs"),
    }


def inspect_project(
    project_id: str,
    repo: Path,
    *,
    fetch: bool,
    live_runtime: bool,
) -> dict[str, Any]:
    if not (repo / ".git").exists():
        return {
            "id": project_id,
            "repository": str(repo),
            "state": "missing",
            "remoteFreshness": "not_observed",
        }

    fetch_result = _fetch_origin_main(repo) if fetch else {"attempted": False, "ok": None, "stderr": None}
    worktree = _worktree(repo)
    local_main = _resolve(repo, "refs/heads/main")
    origin_main = _resolve(repo, "refs/remotes/origin/main")
    project: dict[str, Any] = {
        "id": project_id,
        "repository": str(repo),
        "state": "observed",
        "remoteFreshness": "observed_after_fetch" if fetch_result["ok"] else "not_claimed",
        "fetch": fetch_result,
        "worktree": worktree,
        "refs": {
            "localMain": local_main,
            "originMain": origin_main,
            "localMainToOriginMain": relation(repo, local_main, origin_main),
            "worktreeHeadToLocalMain": relation(repo, worktree["head"], local_main),
            "worktreeHeadToOriginMain": relation(repo, worktree["head"], origin_main),
        },
        "deployment": {
            "state": "not_observed",
            "reason": "deployment truth is owner-native; this projection does not infer it from Git",
        },
    }
    if project_id == "ordivon-runtime" and live_runtime:
        live = _runtime_live(repo)
        deployed = live.get("deployedRevision") if live.get("state") == "observed" else None
        live["toLocalMain"] = relation(repo, deployed, local_main)
        live["toOriginMain"] = relation(repo, deployed, origin_main)
        live["toWorktreeHead"] = relation(repo, deployed, worktree["head"])
        project["deployment"] = live
    return project


def parse_project_spec(value: str) -> tuple[str, Path]:
    project_id, separator, repository = value.partition("=")
    project_id = project_id.strip()
    repository = repository.strip()
    if separator != "=" or not project_id or not repository:
        raise argparse.ArgumentTypeError("--project must be PROJECT_ID=REPOSITORY")
    return project_id, Path(repository).expanduser()


def build_report(
    projects_root: Path,
    *,
    fetch: bool,
    live_runtime: bool,
    project_specs: list[tuple[str, Path]] | None = None,
) -> dict[str, Any]:
    selected_projects = project_specs or [
        (project_id, projects_root / directory) for project_id, directory in FOUNDATION_PROJECTS
    ]
    projects = [
        inspect_project(project_id, repo, fetch=fetch, live_runtime=live_runtime)
        for project_id, repo in selected_projects
    ]
    non_exact = []
    dirty = []
    for project in projects:
        if project.get("state") != "observed":
            non_exact.append({"id": project["id"], "reason": "repository_missing"})
            continue
        relation_state = project["refs"]["localMainToOriginMain"]["state"]
        if relation_state != "exact":
            non_exact.append({"id": project["id"], "reason": relation_state})
        if not project["worktree"]["clean"]:
            dirty.append(project["id"])
    return {
        "schemaVersion": 1,
        "kind": "ordivon.foundation-currentness",
        "generatedAtMs": int(time.time() * 1000),
        "projectsRoot": str(projects_root),
        "projectSelection": "explicit" if project_specs else "foundation-defaults",
        "remoteFreshnessClaimed": fetch,
        "sourceAuthoritySelection": "not_performed",
        "semanticCurrentnessClaimed": False,
        "projects": projects,
        "summary": {
            "projectCount": len(projects),
            "localMainOriginMismatch": non_exact,
            "dirtyWorktrees": dirty,
        },
        "semantics": {
            "localMain": "refs/heads/main in the local Git repository",
            "originMain": "the locally observed refs/remotes/origin/main; current remote truth is claimed only after --fetch",
            "deployment": "owner-native live evidence only; absence is not inferred as no deployment",
            "rule": "never use the bare word current when local main, observed origin/main, worktree HEAD, and deployed revision differ",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Project exact local-main/origin-main/worktree/deployment currentness without choosing authority."
    )
    parser.add_argument(
        "--projects-root",
        type=Path,
        default=Path(os.environ.get("ORDIVON_PROJECTS_ROOT", "/root/projects")),
    )
    parser.add_argument(
        "--project",
        action="append",
        type=parse_project_spec,
        help=(
            "observe an explicit repository as PROJECT_ID=REPOSITORY; repeatable. "
            "When supplied, replaces the default foundation-project set without selecting source authority."
        ),
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="refresh origin/main before projection; without this flag remote freshness is explicitly not claimed",
    )
    parser.add_argument(
        "--live-runtime",
        action="store_true",
        help="include Runtime's owner-native deployed revision and health projection",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report(
        args.projects_root,
        fetch=args.fetch,
        live_runtime=args.live_runtime,
        project_specs=args.project,
    )
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
