from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from build_frontier_freshness_corpus import build
from frontier_freshness import classify_revision_relation
from run_frontier_freshness_self_change import resolve_fixture_dir


def git(repository: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repository), *args], text=True).strip()


def commit(repository: Path, name: str, content: str) -> str:
    (repository / name).write_text(content, encoding="utf-8")
    subprocess.run(["git", "-C", str(repository), "add", name], check=True)
    subprocess.run(["git", "-C", str(repository), "commit", "-m", content], check=True, stdout=subprocess.DEVNULL)
    return git(repository, "rev-parse", "HEAD")


class FrontierFreshnessTests(unittest.TestCase):
    def make_repo(self, root: Path) -> Path:
        repo = root / "repo"
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Freshness Test"], check=True)
        return repo

    def test_classifier_distinguishes_exact_advanced_behind_and_diverged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(Path(directory))
            a = commit(repo, "state.txt", "a")
            b = commit(repo, "state.txt", "b")
            self.assertEqual(classify_revision_relation(repo, b, b).state, "exact")
            advanced = classify_revision_relation(repo, a, b)
            self.assertEqual(advanced.state, "owner_advanced")
            self.assertEqual(advanced.commits_ahead, 1)
            behind = classify_revision_relation(repo, b, a)
            self.assertEqual(behind.state, "checkout_behind_observation")
            self.assertEqual(behind.commits_behind, 1)
            subprocess.run(["git", "-C", str(repo), "checkout", "-q", a], check=True)
            c = commit(repo, "branch.txt", "c")
            diverged = classify_revision_relation(repo, b, c)
            self.assertEqual(diverged.state, "diverged")
            self.assertEqual(diverged.commits_ahead, 1)
            self.assertEqual(diverged.commits_behind, 1)

    def test_current_cross_project_corpus_is_7_3_and_has_exact_plus_advanced(self) -> None:
        entries, labels = build()
        self.assertEqual(len(entries), 10)
        self.assertEqual(sum(x["split"] == "development" for x in entries), 7)
        self.assertEqual(sum(x["split"] == "holdout" for x in entries), 3)
        label_by_id = {x["projectId"]: x for x in labels}
        states = {x["expectedFreshnessState"] for x in labels}
        self.assertIn("exact", states)
        self.assertIn("owner_advanced", states)
        self.assertEqual(label_by_id["ordivon-human"]["expectedFreshnessState"], "exact")
        self.assertEqual(
            {x["projectId"] for x in entries if x["split"] == "holdout"},
            {"ordivon-harness", "ordivon-studio", "ordivon-web"},
        )

    def test_runner_resolves_relative_fixture_under_repository_root(self) -> None:
        resolved = resolve_fixture_dir(Path("research/experiments/experiment-loop-v0/fixtures/frontier-freshness-v1"))
        self.assertTrue(resolved.is_absolute())
        self.assertEqual(resolved, ROOT.parents[2] / "research/experiments/experiment-loop-v0/fixtures/frontier-freshness-v1")

    def test_frozen_fixture_labels_are_separate_from_candidate_visible_corpus(self) -> None:
        fixture = ROOT / "fixtures/frontier-freshness-v1"
        corpus = json.loads((fixture / "corpus.json").read_text())
        labels = json.loads((fixture / "evaluator-labels.json").read_text())
        encoded = json.dumps(corpus, sort_keys=True)
        self.assertNotIn("expectedFreshnessState", encoded)
        self.assertFalse(labels["candidateVisible"])
        self.assertEqual(corpus["splitCounts"], {"development": 7, "holdout": 3})


if __name__ == "__main__":
    unittest.main()
