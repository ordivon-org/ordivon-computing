from __future__ import annotations

from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]


class CoreCoverageTests(unittest.TestCase):
    def test_core_already_carries_the_minimum_temporal_law(self):
        foundations = (REPO / "core" / "foundations.md").read_text()
        stack = (REPO / "core" / "stack.md").read_text()
        primitives = (REPO / "core" / "primitives.md").read_text()
        loop = (REPO / "research" / "world-model-loop-v2.json").read_text()
        self.assertIn("historical evidence remains valid history without automatically proving current state", foundations)
        self.assertIn("revision-valid sources", stack)
        self.assertIn("A projection does not become a second owner", primitives)
        self.assertIn("historical_observation_validity_is_not_currentness", loop)
        self.assertIn("current_cross_project_claim_requires_explicit_freshness_assessment", loop)

    def test_core_does_not_name_a_global_temporal_service(self):
        text = "\n".join((REPO / "core" / name).read_text() for name in ["foundations.md", "stack.md", "primitives.md"])
        for forbidden in ["TemporalAuthority", "GlobalEventBus", "GlobalTimeOntology", "FreshnessService"]:
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
