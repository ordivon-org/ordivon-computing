from __future__ import annotations

import json
import subprocess
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionC4Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = json.loads((ROOT / "evidence/computer-contraction-c4-protocol-candidate.json").read_text())

    def test_released_line_and_candidate_are_distinct(self) -> None:
        package = tomllib.loads((ROOT.parent / "packages/ordivon-protocol/pyproject.toml").read_text())
        self.assertEqual(self.doc["releasedLine"]["version"], "0.3.0")
        self.assertEqual(package["project"]["version"], "0.4.0.dev0")
        self.assertFalse((ROOT.parent / "packages/ordivon-protocol/releases/0.4.0.json").exists())

    def test_semantic_state_is_absent_current_but_git_recoverable(self) -> None:
        self.assertFalse((ROOT.parent / "packages/ordivon-protocol/src/ordivon_semantics").exists())
        release = self.doc["releasedLine"]
        actual = subprocess.check_output(["git", "-C", str(ROOT.parent), "rev-parse", f"{release['releaseRevision']}:packages/ordivon-protocol/src/ordivon_semantics"], text=True).strip()
        self.assertEqual(actual, release["semanticStateTree"])

    def test_candidate_does_not_claim_consumer_cutover(self) -> None:
        candidate = json.loads((ROOT.parent / "packages/ordivon-protocol/candidates/0.4.0.dev0.json").read_text())
        self.assertFalse(candidate["automaticConsumerUpgrade"])
        self.assertEqual(candidate["requiredOwnerAdmission"], ["ordivon-host"])
        self.assertFalse(self.doc["candidate"]["releaseManifestCreated"])


if __name__ == "__main__":
    unittest.main()
