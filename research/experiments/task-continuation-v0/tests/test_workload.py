from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from anc_continuation.ablation import capsule_ablation_receipt
from anc_continuation.workload import baseline_receipt, freeze_checkpoint


class WorkloadTests(unittest.TestCase):
    def test_checkpoint_is_deterministic_for_one_source_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = freeze_checkpoint(root / "first", source_revision="f" * 40)
            second = freeze_checkpoint(root / "second", source_revision="f" * 40)
            self.assertEqual(first.capsule_digest, second.capsule_digest)
            self.assertEqual(first.initial_digest, second.initial_digest)
            self.assertEqual(first.terminal_digest, second.terminal_digest)
            self.assertEqual(
                (first.root / "rubric.json").read_bytes(),
                (second.root / "rubric.json").read_bytes(),
            )

    def test_baselines_separate_continuation_from_reconstruction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            receipt = baseline_receipt(frozen.root)
            results = {item["baseline"]: item for item in receipt["results"]}
            self.assertTrue(results["fullTranscript"]["correctFirstAction"])
            self.assertTrue(results["manualHandoff"]["correctFirstAction"])
            self.assertFalse(results["noMemory"]["correctFirstAction"])
            self.assertEqual(
                results["noMemory"]["repeatedCompletedEffects"],
                ["effect:continuation-audit"],
            )
            self.assertLess(
                results["manualHandoff"]["bytes"],
                results["fullTranscript"]["bytes"],
            )

    def test_ablation_identifies_hard_and_provenance_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            receipt = capsule_ablation_receipt(frozen.root)
            variants = {item["variant"]: item for item in receipt["capsuleVariants"]}
            self.assertEqual(variants["full"]["outcome"], "valid")
            for name in (
                "withoutDecisionArtifact",
                "withoutCheckpointFact",
                "withoutCurrentBinding",
            ):
                self.assertEqual(variants[name]["outcome"], "fail-closed")
            self.assertEqual(
                variants["withoutCompletedEffects"]["outcome"], "valid"
            )
            self.assertFalse(
                variants["withoutCompletedEffects"]["provenanceComplete"]
            )
            self.assertEqual(
                variants["withoutCompletedEffects"]["forbiddenEffectCount"], 0
            )


if __name__ == "__main__":
    unittest.main()
