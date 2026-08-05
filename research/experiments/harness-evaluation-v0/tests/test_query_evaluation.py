from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
QUERY_PATH = ROOT / "query_evaluation.py"


def _load_query():
    spec = importlib.util.spec_from_file_location("track_r_query_test", QUERY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load query module: {QUERY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


query = _load_query()


class EvaluationQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.documents = query.load_records(query.DEFAULT_RECORDS)

    def test_status_preserves_frozen_inventory_and_no_global_score(self) -> None:
        value = query.status(
            self.documents,
            suite_path=query.DEFAULT_SUITE,
            minimum_trials=3,
        )
        self.assertEqual(
            value["inventory"],
            {"tasks": 7, "trials": 10, "results": 10, "failures": 6},
        )
        self.assertEqual(value["eligibleComparisons"], 0)
        self.assertFalse(value["globalScoreGenerated"])
        self.assertEqual(value["acceptance"]["accepted"], 4)

    def test_list_returns_compact_machine_records(self) -> None:
        trials = query.list_records(self.documents, kind="trial")
        self.assertEqual(len(trials), 10)
        self.assertEqual(
            set(trials[0]),
            {
                "kind",
                "identity",
                "trialId",
                "taskRef",
                "executionPath",
                "providerId",
                "modelId",
                "harnessId",
                "harnessRevision",
                "systemManifestRef",
                "payloadDigest",
            },
        )

    def test_show_trial_joins_result_and_failure_without_database(self) -> None:
        records = query.show_records(
            self.documents,
            "dogfood:20260802:provenance-verifier-rejected-pro",
        )
        kinds = [record["kind"] for record in records]
        self.assertEqual(
            kinds,
            [
                "ordivon.evaluation-failure",
                "ordivon.evaluation-result",
                "ordivon.evaluation-trial",
            ],
        )

    def test_failure_filters_use_owned_fields(self) -> None:
        failures = query.filter_failures(
            self.documents,
            failure_class="HARNESS",
            boundary="harness",
            trial_id=None,
            recovered="true",
        )
        self.assertEqual(len(failures), 2)
        self.assertTrue(all(item["recovered"] for item in failures))

    def test_comparison_readiness_exposes_blockers(self) -> None:
        value = query.comparison_readiness(
            self.documents,
            suite_path=query.DEFAULT_SUITE,
            minimum_trials=3,
        )
        self.assertEqual(value["eligibleComparisons"], 0)
        self.assertGreater(
            value["blockerCounts"]["insufficient_trials_per_configuration"],
            0,
        )
        self.assertFalse(value["globalScoreGenerated"])


if __name__ == "__main__":
    unittest.main()
