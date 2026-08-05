from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

EXPERIMENT = Path(__file__).resolve().parents[1]
REPOSITORY = EXPERIMENT.parents[2]
BASELINE = EXPERIMENT / "baselines" / "p0-20260804"
SUITE = EXPERIMENT / "suite-v1.json"
DOGFOOD = EXPERIMENT / "dogfood-20260802"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p0 = load_module("track_r_p0_test", EXPERIMENT / "validate_p0_artifacts.py")
records = load_module("track_r_records_test", EXPERIMENT / "validate_evaluation_evidence.py")
summarizer = load_module("track_r_summary_test", EXPERIMENT / "summarize_evaluation.py")
snapshot = load_module(
    "track_r_snapshot_test", REPOSITORY / "research" / "evidence" / "validate_system_snapshot.py"
)


class EvaluationP0ArtifactTests(unittest.TestCase):
    def test_committed_p0_artifacts_validate_as_one_collection(self) -> None:
        loaded = p0.load_documents([SUITE, BASELINE])
        p0.validate_collection(loaded, root=REPOSITORY)
        self.assertEqual(len(loaded), 5)

    def test_system_snapshot_binds_four_frozen_repositories(self) -> None:
        path = (
            REPOSITORY
            / "research"
            / "evidence"
            / "snapshots"
            / "host-harness-runtime-eval-p0-20260804t082600z.json"
        )
        document = snapshot.load(path)
        snapshot.validate(document)
        self.assertEqual(
            {repository["id"] for repository in document["repositories"]},
            {"ordivon-computing", "ordivon-host", "ordivon-harness", "ordivon-runtime"},
        )
        self.assertTrue(all(repository["clean"] for repository in document["repositories"]))

    def test_closeout_binds_exact_gate_and_unmerged_integration_blocker(self) -> None:
        document = json.loads((BASELINE / "closeout.json").read_text())
        p0.validate_closeout(document)
        self.assertEqual(
            document["testedRevision"],
            document["conformance"]["repositoryRevision"],
        )
        self.assertEqual(document["conformance"]["status"], "passed")
        self.assertEqual(document["integration"]["status"], "ready_unmerged")
        self.assertEqual(document["integration"]["foreignIndexStats"]["files"], 8)
        self.assertEqual(document["results"]["dogfood"]["eligibleComparisons"], 0)
        self.assertFalse(document["results"]["componentHealth"]["productQualityClaim"])

    def test_closeout_rejects_tested_revision_drift_even_with_new_digest(self) -> None:
        document = json.loads((BASELINE / "closeout.json").read_text())
        document["conformance"]["repositoryRevision"] = "1" * 40
        document["integrity"]["payloadDigest"] = p0.payload_digest(document)
        with self.assertRaisesRegex(ValueError, "repositoryRevision differs"):
            p0.validate_closeout(document)

    def test_component_baseline_is_health_not_product_quality(self) -> None:
        document = json.loads((BASELINE / "component-baseline.json").read_text())
        self.assertEqual(
            document["aggregate"],
            {
                "testSuites": 4,
                "contractChecks": 1,
                "passed": 601,
                "failed": 0,
                "ignored": 22,
                "productQualityClaim": False,
            },
        )
        p0.validate_component_baseline(document)

    def test_component_aggregate_tampering_fails_even_with_new_digest(self) -> None:
        document = json.loads((BASELINE / "component-baseline.json").read_text())
        document["aggregate"]["passed"] += 1
        document["integrity"]["payloadDigest"] = p0.payload_digest(document)
        with self.assertRaisesRegex(ValueError, "aggregate differs"):
            p0.validate_component_baseline(document)

    def test_manifest_nulls_are_explicitly_declared_unavailable(self) -> None:
        document = json.loads((BASELINE / "system-manifest.json").read_text())
        p0.validate_system_manifest(document)
        self.assertEqual(len(document["unavailableFields"]), 10)
        self.assertFalse(document["privacy"]["secretsIncluded"])
        self.assertFalse(document["privacy"]["rawReasoningRequired"])

    def test_committed_dogfood_summary_is_reproducible(self) -> None:
        loaded = records.load_documents([DOGFOOD])
        documents = [document for _, document in loaded]
        regenerated = summarizer.summarize(
            documents,
            summary_id="ordivon-dogfood-20260802-p0-summary",
            generated_at="2026-08-04T08:26:00Z",
            suite_ref={
                "path": SUITE.relative_to(REPOSITORY).as_posix(),
                "digest": p0.file_digest(SUITE),
            },
            minimum_trials=3,
        )
        committed = json.loads((BASELINE / "dogfood-summary.json").read_text())
        self.assertEqual(regenerated, committed)
        self.assertEqual(committed["inventory"], {"tasks": 7, "trials": 10, "results": 10, "failures": 6})
        self.assertFalse(committed["policy"]["globalScoreGenerated"])
        self.assertTrue(committed["comparisonCandidates"])
        self.assertTrue(all(not candidate["eligible"] for candidate in committed["comparisonCandidates"]))

    def test_failure_taxonomy_schema_and_validator_do_not_drift(self) -> None:
        taxonomy_path = EXPERIMENT / "failure-taxonomy.yaml"
        parsed: dict[str, set[str]] = {}
        current_class: str | None = None
        in_classes = False
        for raw_line in taxonomy_path.read_text().splitlines():
            if raw_line == "classes:":
                in_classes = True
                continue
            if raw_line == "rules:":
                break
            if not in_classes or not raw_line.strip():
                continue
            if raw_line.startswith("  ") and not raw_line.startswith("    ") and raw_line.endswith(":"):
                current_class = raw_line.strip().removesuffix(":")
                parsed[current_class] = set()
            elif raw_line.startswith("    - "):
                assert current_class is not None
                parsed[current_class].add(raw_line.strip().removeprefix("- "))
        self.assertEqual(parsed, records.FAILURE_CODES)

        schema = json.loads((EXPERIMENT / "schemas" / "failure-record.schema.json").read_text())
        self.assertEqual(set(schema["properties"]["failureClass"]["enum"]), set(records.FAILURE_CODES))
        self.assertEqual(
            set(schema["properties"]["responsibleBoundary"]["enum"]),
            {failure_class.lower() for failure_class in records.FAILURE_CODES},
        )

    def test_expanded_runtime_failure_class_validates(self) -> None:
        source = next(
            document
            for _, document in records.load_documents([DOGFOOD / "failures"])
            if document["kind"] == "ordivon.evaluation-failure"
        )
        document = copy.deepcopy(source)
        document["failureId"] = "failure:p0-runtime-source-drift-contract-test"
        document["failureClass"] = "RUNTIME"
        document["failureCode"] = "source_drift"
        document["responsibleBoundary"] = "runtime"
        document["integrity"]["payloadDigest"] = records.payload_digest(document)
        records.validate_document(document)

    def test_trial_system_manifest_binding_is_backward_compatible(self) -> None:
        source = next(
            document
            for _, document in records.load_documents([DOGFOOD / "trials"])
            if document["kind"] == "ordivon.evaluation-trial"
        )
        records.validate_document(source)
        current = copy.deepcopy(source)
        current["bindings"]["systemManifestRef"] = {
            "repositoryId": "ordivon-computing",
            "path": "research/experiments/harness-evaluation-v0/baselines/p0-20260804/system-manifest.json",
            "digest": "sha256:" + "1" * 64,
        }
        current["integrity"]["payloadDigest"] = records.payload_digest(current)
        records.validate_document(current)
        configuration = summarizer.group_configuration(
            current,
            next(
                document
                for _, document in records.load_documents([DOGFOOD / "results"])
                if document["trialId"] == current["trialId"]
            ),
        )
        self.assertEqual(configuration["systemManifestRef"], current["bindings"]["systemManifestRef"])

    def test_suite_forbids_one_heterogeneous_global_score(self) -> None:
        document = json.loads(SUITE.read_text())
        self.assertTrue(document["metrics"]["forbidGlobalScore"])
        document["metrics"]["forbidGlobalScore"] = False
        document["integrity"]["payloadDigest"] = p0.payload_digest(document)
        with self.assertRaisesRegex(ValueError, "global score"):
            p0.validate_suite(document)


if __name__ == "__main__":
    unittest.main()
