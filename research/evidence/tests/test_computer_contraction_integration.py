from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = json.loads((ROOT / "evidence/computer-contraction-concurrent-integration.json").read_text())

    def test_concurrent_lines_are_assimilated_not_rewritten(self) -> None:
        self.assertFalse(self.doc["rawConcurrentEvidenceRewritten"])
        self.assertEqual(self.doc["concurrentEvidenceAssimilation"]["newResponsibilitySlots"], 0)
        self.assertEqual(set(self.doc["concurrentEvidenceAssimilation"]["wl0EvidenceAddedToResponsibilities"]), {"CR-03", "CR-05", "CR-06", "CR-07", "CR-09"})

    def test_completed_concurrent_apparatus_is_archived(self) -> None:
        archive = self.doc["concurrentApparatusArchive"]
        self.assertEqual(archive["removedFiles"], 9)
        self.assertEqual(archive["removedLines"], 916)
        self.assertEqual(self.doc["mergedSurface"]["experimentExecutableLikeFiles"], 0)

    def test_current_null_state_survives_concurrency(self) -> None:
        surface = self.doc["mergedSurface"]
        self.assertEqual(surface["portfolioActiveIds"], [])
        self.assertEqual(surface["portfolioReadyIds"], [])
        self.assertEqual(len(surface["responsibilityIds"]), 10)

    def test_deterministic_links_do_not_depend_on_live_network(self) -> None:
        boundary = self.doc["deterministicLinkBoundary"]
        self.assertIn("--offline", boundary["currentGateRule"])
        self.assertIn("0 errors", boundary["offlineRecheck"])


if __name__ == "__main__":
    unittest.main()
