from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from cel import write_record
from frontier_freshness import classify_revision_relation

REGISTRY = ROOT / "projects/registry.yaml"
FRONTIER = ROOT / "research/world-model-frontier.json"
PROJECT_ROOT = Path("/root/projects")


def _split_rank(project_id: str) -> int:
    return int(hashlib.sha256(project_id.encode("utf-8")).hexdigest()[:16], 16)


def _head(repository: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        text=True,
        encoding="utf-8",
    ).strip()


def build() -> tuple[list[dict], list[dict]]:
    registry_text = REGISTRY.read_text(encoding="utf-8")
    project_ids = re.findall(r"^  - id: (ordivon-[a-z0-9-]+)$", registry_text, re.MULTILINE)
    frontier = json.loads(FRONTIER.read_text(encoding="utf-8"))
    observed = {item["projectId"]: item["observedRevision"] for item in frontier["projects"]}
    expected_ids = [item for item in project_ids if item != "ordivon-computing"]
    if set(expected_ids) != set(observed):
        raise RuntimeError("registry/frontier project set differs")

    holdout_ids = {
        project_id
        for project_id in sorted(expected_ids, key=_split_rank)[:3]
    }
    entries = []
    labels = []
    for project_id in sorted(expected_ids):
        repository = PROJECT_ROOT / project_id
        current = _head(repository)
        relation = classify_revision_relation(repository, observed[project_id], current)
        entries.append(
            {
                "projectId": project_id,
                "repositoryPath": str(repository),
                "observedRevision": observed[project_id],
                "currentRevision": current,
                "split": "holdout" if project_id in holdout_ids else "development",
            }
        )
        labels.append(
            {
                "projectId": project_id,
                "expectedFreshnessState": relation.state,
                "expectedCurrent": relation.current,
                "expectedCommitsAhead": relation.commits_ahead,
                "expectedCommitsBehind": relation.commits_behind,
                "labelAuthority": "independent Git revision relation at corpus freeze",
            }
        )
    return entries, labels


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    entries, labels = build()
    corpus = {
        "schemaVersion": 1,
        "kind": "ordivon.world-model-frontier-freshness-corpus",
        "corpusId": "CEL-P2-FRONTIER-FRESHNESS-CORPUS-001",
        "frontierRef": "research/world-model-frontier.json",
        "entryCount": len(entries),
        "splitCounts": {
            "development": sum(item["split"] == "development" for item in entries),
            "holdout": sum(item["split"] == "holdout" for item in entries),
        },
        "entries": entries,
    }
    evaluator = {
        "schemaVersion": 1,
        "kind": "ordivon.world-model-frontier-freshness-labels",
        "evaluatorId": "CEL-P2-FRONTIER-FRESHNESS-EVALUATOR-001",
        "labels": labels,
        "candidateVisible": False,
    }
    write_record(args.output_dir / "corpus.json", corpus)
    write_record(args.output_dir / "evaluator-labels.json", evaluator)
    print(json.dumps({"entryCount": len(entries), "splitCounts": corpus["splitCounts"], "holdout": [x["projectId"] for x in entries if x["split"] == "holdout"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
