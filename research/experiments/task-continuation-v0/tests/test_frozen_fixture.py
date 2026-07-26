from __future__ import annotations

import json
import unittest
from pathlib import Path

from anc_continuation.ablation import capsule_ablation_receipt
from anc_continuation.store import FileObjectStore
from anc_continuation.validation import CapsuleValidator
from anc_continuation.workload import baseline_receipt, load_manifest


EXPERIMENT = Path(__file__).resolve().parents[1]
FIXTURE = EXPERIMENT / "fixtures/checkpoint-f0cc83f"
IMPLEMENTATION_REVISION = "f0cc83f709ff85b1b6a85302562fe904727fbc8b"
CAPSULE_DIGEST = "sha256:c5cceb3d1f57904851968f8685c73a0f138a9147d9c6dde22ca74862c318a956"


class FrozenFixtureTests(unittest.TestCase):
    def test_exact_checkpoint_fixture_resolves_and_validates(self) -> None:
        manifest = load_manifest(FIXTURE)
        self.assertEqual(manifest["sourceRevision"], IMPLEMENTATION_REVISION)
        self.assertEqual(manifest["capsuleDigest"], CAPSULE_DIGEST)
        store = FileObjectStore(FIXTURE / "objects")
        capsule = store.get_capsule(CAPSULE_DIGEST)
        report = CapsuleValidator(store).validate(capsule, world_root=FIXTURE)
        self.assertEqual(report.world_status, "current")
        self.assertEqual(len(report.completed_effect_ids), 2)
        self.assertEqual(len(report.resolved_actions), 1)

    def test_checked_receipts_match_the_frozen_fixture(self) -> None:
        evidence = json.loads(
            (EXPERIMENT / "evidence/continuation-f0cc83f.json").read_text()
        )
        evaluation = json.loads(
            (EXPERIMENT / "evidence/evaluation-f0cc83f.json").read_text()
        )
        self.assertEqual(evidence["sourceRevision"], IMPLEMENTATION_REVISION)
        self.assertEqual(evidence["capsuleDigest"], CAPSULE_DIGEST)
        self.assertTrue(evaluation["allRequiredCriteriaPassed"])
        self.assertEqual(
            evidence["freshProcessCodex"]["host"]["adapterId"],
            "codex-cli-ephemeral-v1:gpt-5.5",
        )
        self.assertFalse(evidence["freshProcessCodex"]["originalTranscriptLoaded"])
        self.assertEqual(
            baseline_receipt(FIXTURE)["results"],
            evidence["baselines"]["results"],
        )
        self.assertEqual(
            capsule_ablation_receipt(FIXTURE)["capsuleVariants"],
            evidence["ablations"]["capsuleVariants"],
        )


if __name__ == "__main__":
    unittest.main()
