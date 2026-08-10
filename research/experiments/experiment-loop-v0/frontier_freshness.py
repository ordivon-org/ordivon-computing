from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from typing import Any

_REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


class FrontierFreshnessError(RuntimeError):
    pass


@dataclass(frozen=True)
class RevisionRelation:
    state: str
    observed_revision: str
    current_revision: str
    commits_ahead: int | None
    commits_behind: int | None

    @property
    def current(self) -> bool:
        return self.state == "exact"


def _git(repository: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )


def _exact_revision(value: Any, label: str) -> str:
    if not isinstance(value, str) or _REVISION_RE.fullmatch(value) is None:
        raise FrontierFreshnessError(f"{label} is not an exact Git revision")
    return value


def repository_head(repository: Path) -> str:
    completed = _git(repository, "rev-parse", "HEAD")
    return _exact_revision(completed.stdout.strip(), "repository HEAD")


def revision_exists(repository: Path, revision: str) -> bool:
    revision = _exact_revision(revision, "observed revision")
    return _git(repository, "cat-file", "-e", f"{revision}^{{commit}}", check=False).returncode == 0


def _is_ancestor(repository: Path, ancestor: str, descendant: str) -> bool:
    completed = _git(
        repository,
        "merge-base",
        "--is-ancestor",
        ancestor,
        descendant,
        check=False,
    )
    if completed.returncode not in (0, 1):
        raise FrontierFreshnessError(
            f"Git ancestry check failed for {ancestor} -> {descendant}: {completed.stderr.strip()}"
        )
    return completed.returncode == 0


def _count(repository: Path, revision_range: str) -> int:
    completed = _git(repository, "rev-list", "--count", revision_range)
    try:
        return int(completed.stdout.strip())
    except ValueError as error:
        raise FrontierFreshnessError("Git rev-list count is not an integer") from error


def classify_revision_relation(
    repository: Path,
    observed_revision: str,
    current_revision: str | None = None,
) -> RevisionRelation:
    observed = _exact_revision(observed_revision, "observed revision")
    current = _exact_revision(
        current_revision if current_revision is not None else repository_head(repository),
        "current revision",
    )
    if not revision_exists(repository, observed):
        return RevisionRelation("observed_unavailable", observed, current, None, None)
    if observed == current:
        return RevisionRelation("exact", observed, current, 0, 0)
    observed_is_ancestor = _is_ancestor(repository, observed, current)
    current_is_ancestor = _is_ancestor(repository, current, observed)
    if observed_is_ancestor:
        return RevisionRelation(
            "owner_advanced",
            observed,
            current,
            _count(repository, f"{observed}..{current}"),
            0,
        )
    if current_is_ancestor:
        return RevisionRelation(
            "checkout_behind_observation",
            observed,
            current,
            0,
            _count(repository, f"{current}..{observed}"),
        )
    return RevisionRelation(
        "diverged",
        observed,
        current,
        _count(repository, f"{observed}..{current}"),
        _count(repository, f"{current}..{observed}"),
    )


def baseline_syntax_only(entry: dict[str, Any]) -> dict[str, Any]:
    observed = entry.get("observedRevision")
    valid = isinstance(observed, str) and _REVISION_RE.fullmatch(observed) is not None
    return {
        "policyId": "syntactic_revision_v1",
        "freshnessState": "exact" if valid else "invalid_revision",
        "current": bool(valid),
    }


def candidate_git_relation(entry: dict[str, Any]) -> dict[str, Any]:
    relation = classify_revision_relation(
        Path(entry["repositoryPath"]),
        entry["observedRevision"],
        entry["currentRevision"],
    )
    return {
        "policyId": "git_relation_freshness_v2",
        "freshnessState": relation.state,
        "current": relation.current,
        "commitsAhead": relation.commits_ahead,
        "commitsBehind": relation.commits_behind,
    }
