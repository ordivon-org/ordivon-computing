from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from anc_adversarial_transfer.merge import merge_parts
from anc_adversarial_transfer.model import MatrixResult, TrialResult, TrialSpec

REVISION = "a" * 40
HOST = "b" * 40


def trial(name: str) -> TrialResult:
    return TrialResult(
        spec=TrialSpec(name, "deepseek-v4-flash", "harness-gated", "attack", "attack.md", "out.md"),
        status="passed",
        source_revision=REVISION,
        host_revision=HOST,
        runtime_catalog_digest="sha256:" + "1" * 64,
        tool_definition_digest="sha256:" + "2" * 64,
        committed_tool_catalog_digest="sha256:" + "1" * 64,
        context_digest="sha256:" + "3" * 64,
        omitted_context_blocks=(),
        stop_code="candidate_completed",
        stop_detail=None,
        model_calls=1,
        tool_calls=0,
        usage={},
        proposed_calls=(),
        observations=(),
        authorized_utility=True,
        attack_objective_success=False,
        secret_read_attempted=False,
        secret_read_observed=False,
        secret_leaked=False,
        outbox_changed=False,
        registry_changed=False,
        memory_changed=False,
        unauthorized_mutation_observed=False,
        opaque_exec_attempted=False,
        opaque_exec_observed=False,
        false_completion=False,
        host_verifier_accepted=True,
        completion_reason_code="accepted",
        final_task_state="completed",
        candidate_summary="done",
        output_digest="sha256:" + "4" * 64,
        diff_digest="sha256:" + "5" * 64,
        hard_failures=(),
    )


class MergeTests(unittest.TestCase):
    def test_merges_unique_parts_and_recomputes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, item in enumerate((trial("trial:a"), trial("trial:b")), start=1):
                payload = MatrixResult(
                    REVISION,
                    HOST,
                    "http://127.0.0.1:8897/mcp",
                    (item,),
                    {"partial": index},
                    {"partial": index},
                ).to_dict()
                (root / f"part-{index}.json").write_text(json.dumps(payload), encoding="utf-8")
            merged = merge_parts(tuple(root.glob("*.json")), expected_trials=2)
            self.assertEqual(len(merged.trials), 2)
            self.assertEqual(merged.summary["passed"], 2)
            self.assertEqual(merged.summary["errors"], 0)

    def test_rejects_conflicting_duplicate_trial(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = trial("trial:a")
            second = replace(first, status="failed")
            for name, item in (("one", first), ("two", second)):
                payload = MatrixResult(
                    REVISION,
                    HOST,
                    "http://127.0.0.1:8897/mcp",
                    (item,),
                    {},
                    {},
                ).to_dict()
                (root / f"{name}.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "conflicting duplicate"):
                merge_parts(tuple(root.glob("*.json")), expected_trials=1)


if __name__ == "__main__":
    unittest.main()
