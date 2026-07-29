from __future__ import annotations

from pathlib import Path
import unittest

from anc_core_work_system.conclusions import EvidenceInputs, derive_closeout


ROOT = Path(__file__).resolve().parents[1]


class ConclusionTests(unittest.TestCase):
    def test_closeout_is_evidence_derived_and_conservative(self) -> None:
        receipt = derive_closeout(
            EvidenceInputs(
                matrix_path=ROOT / "evidence" / "deterministic-matrix.json",
                live_path=ROOT / "evidence" / "live-provider-gauntlet.json",
                host_source_revision="394e205d165c0d891448179fbc0fdc7270a98970",
                host_receipt_digest=(
                    "sha256:8eec72773621dacbf3826b467d010bed6717e80642e1d10eb2c3fe66253bf785"
                ),
            )
        )
        dispositions = receipt["dispositions"]
        self.assertEqual(dispositions["E1-open-work-continuity"]["decision"], "localize")
        self.assertEqual(dispositions["E2-effect-commitment"]["decision"], "shrink")
        self.assertEqual(dispositions["E3-context-provenance"]["decision"], "shrink")
        self.assertEqual(dispositions["E5-operator-attention"]["decision"], "localize")
        self.assertEqual(dispositions["E7-provider-replacement"]["decision"], "retain")
        self.assertFalse(receipt["repositoryActions"]["protocolPromoted"])
        self.assertFalse(receipt["repositoryActions"]["runtimeProductionChanged"])


if __name__ == "__main__":
    unittest.main()
