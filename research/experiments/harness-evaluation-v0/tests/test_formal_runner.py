from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "formal_runner.py"
B3_SELECTION = (
    ROOT.parent
    / "observation-plane-v0"
    / "evidence"
    / "b3-owner-native-e9bc8b4"
    / "observation-selection.json"
)


def load_runner():
    spec = importlib.util.spec_from_file_location("b4_formal_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load formal_runner.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = load_runner()


class FormalRunnerTests(unittest.TestCase):
    def initialize(self, root: Path):
        return runner.TrialRecordStore.initialize(
            root,
            trial_id="trial:b4-formal-runner-test",
            configuration_id="scripted-integrated-control",
            task_ref={"taskId": "HARNESS-REPO-REPAIR-001", "taskVersion": 1},
            created_at_ms=100,
        )

    def test_write_once_intent_reopen_and_stage_cas(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "trial"
            store = self.initialize(root)
            self.assertEqual(store.state()["stage"], "planned")
            store.advance(
                expected_stage="planned",
                next_stage="prepared",
                updated_at_ms=101,
            )
            replay = store.advance(
                expected_stage="planned",
                next_stage="prepared",
                updated_at_ms=999,
            )
            self.assertEqual(replay["stage"], "prepared")
            reopened = runner.TrialRecordStore(root)
            self.assertEqual(reopened.trial_id, "trial:b4-formal-runner-test")
            self.assertTrue(reopened.doctor()["healthy"])
            with self.assertRaises(runner.FormalRunnerConflict):
                runner.TrialRecordStore.initialize(
                    root,
                    trial_id="trial:different",
                    configuration_id="scripted-integrated-control",
                    task_ref={
                        "taskId": "HARNESS-REPO-REPAIR-001",
                        "taskVersion": 1,
                    },
                    created_at_ms=100,
                )

    def test_records_are_write_once_and_bound_when_stage_advances(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.initialize(Path(directory) / "trial")
            store.advance(
                expected_stage="planned",
                next_stage="prepared",
                updated_at_ms=101,
            )
            digest = store.write_record(
                "system-manifest.json",
                {
                    "schemaVersion": 1,
                    "kind": "ordivon.test-system-manifest",
                    "configurationId": "scripted-integrated-control",
                },
                minimum_stage="prepared",
            )
            self.assertTrue(digest.startswith("sha256:"))
            store.advance(
                expected_stage="prepared",
                next_stage="executing",
                updated_at_ms=102,
                records=("system-manifest.json",),
            )
            self.assertEqual(
                store.state()["recordDigests"]["system-manifest.json"],
                digest,
            )
            with self.assertRaises(runner.FormalRunnerConflict):
                store.write_record(
                    "system-manifest.json",
                    {
                        "schemaVersion": 1,
                        "kind": "ordivon.test-system-manifest",
                        "configurationId": "changed",
                    },
                )

    def test_selection_gate_requires_complete_metadata_only_non_validating_record(self) -> None:
        selection = json.loads(B3_SELECTION.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            store = self.initialize(Path(directory) / "trial")
            for expected, next_stage, timestamp in (
                ("planned", "prepared", 101),
                ("prepared", "executing", 102),
                ("executing", "evidence_collected", 103),
            ):
                store.advance(
                    expected_stage=expected,
                    next_stage=next_stage,
                    updated_at_ms=timestamp,
                )
            digest = store.admit_selection(selection)
            self.assertEqual(
                digest,
                selection["integrity"]["payloadDigest"],
            )
            for mutation in (
                lambda value: value["completeness"].update(complete=False),
                lambda value: value["completeness"].update(
                    trialValidityInferred=True
                ),
                lambda value: value["privacy"].update(payloadBytesCopied=True),
            ):
                invalid = copy.deepcopy(selection)
                mutation(invalid)
                invalid.pop("integrity", None)
                invalid = runner.with_integrity(invalid)
                another = runner.TrialRecordStore.initialize(
                    Path(directory) / canonical_name(invalid),
                    trial_id=f"trial:{canonical_name(invalid)}",
                    configuration_id="scripted-integrated-control",
                    task_ref={
                        "taskId": "HARNESS-REPO-REPAIR-001",
                        "taskVersion": 1,
                    },
                    created_at_ms=100,
                )
                for expected, next_stage, timestamp in (
                    ("planned", "prepared", 101),
                    ("prepared", "executing", 102),
                    ("executing", "evidence_collected", 103),
                ):
                    another.advance(
                        expected_stage=expected,
                        next_stage=next_stage,
                        updated_at_ms=timestamp,
                    )
                with self.assertRaises(runner.FormalRunnerPolicyError):
                    another.admit_selection(invalid)

    def test_disposition_is_three_axis_and_bound_to_selection(self) -> None:
        selection = json.loads(B3_SELECTION.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            store = self.initialize(Path(directory) / "trial")
            for expected, next_stage, timestamp in (
                ("planned", "prepared", 101),
                ("prepared", "executing", 102),
                ("executing", "evidence_collected", 103),
            ):
                store.advance(
                    expected_stage=expected,
                    next_stage=next_stage,
                    updated_at_ms=timestamp,
                )
            store.admit_selection(selection)
            store.advance(
                expected_stage="evidence_collected",
                next_stage="verified",
                updated_at_ms=104,
                records=("observation-selection.json",),
            )
            disposed = store.dispose(
                runner.TrialDisposition(
                    trial_id=store.trial_id,
                    validity="valid",
                    semantic_outcome="accepted",
                    comparative_outcome="not_applicable",
                    failure_attribution="none",
                    comparison_eligible=True,
                    reasons=("scripted deterministic smoke passed",),
                    selection_digest=selection["selectionDigest"],
                ),
                updated_at_ms=105,
            )
            self.assertEqual(disposed["stage"], "disposed")
            self.assertTrue(store.doctor()["healthy"])
            with self.assertRaises(ValueError):
                runner.TrialDisposition(
                    trial_id="trial:x",
                    validity="invalid",
                    semantic_outcome="accepted",
                    comparative_outcome="not_applicable",
                    failure_attribution="infrastructure",
                    comparison_eligible=True,
                    reasons=(),
                    selection_digest=selection["selectionDigest"],
                )

    def test_sensitive_fields_and_text_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.initialize(Path(directory) / "trial")
            for value in (
                {"schemaVersion": 1, "kind": "test", "api_key": "secret"},
                {
                    "schemaVersion": 1,
                    "kind": "test",
                    "note": "read /root/.config/ordivon/secrets/a.json",
                },
                {
                    "schemaVersion": 1,
                    "kind": "test",
                    "privateReasoning": "not allowed",
                },
            ):
                with self.assertRaises(runner.FormalRunnerPolicyError):
                    store.write_record("forbidden.json", value)

    def test_tampered_state_and_public_directory_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "trial"
            store = self.initialize(root)
            state = json.loads(store.state_path.read_text(encoding="utf-8"))
            state["stage"] = "closed"
            store.state_path.write_text(json.dumps(state), encoding="utf-8")
            with self.assertRaises(runner.FormalRunnerError):
                store.state()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "public"
            root.mkdir(mode=0o755)
            with self.assertRaises(runner.FormalRunnerPolicyError):
                runner.TrialRecordStore.initialize(
                    root,
                    trial_id="trial:public",
                    configuration_id="scripted",
                    task_ref={"taskId": "T", "taskVersion": 1},
                    created_at_ms=1,
                )


def canonical_name(value: dict[str, object]) -> str:
    payload = json.dumps(value, sort_keys=True).encode("utf-8")
    import hashlib

    return "case-" + hashlib.sha256(payload).hexdigest()[:12]


if __name__ == "__main__":
    unittest.main()
