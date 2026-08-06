from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "program-v1.json"


class CognitiveReformProgramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.program = json.loads(PROGRAM.read_text(encoding="utf-8"))

    def test_identity_and_current_level(self) -> None:
        self.assertEqual(self.program["schemaVersion"], 1)
        self.assertEqual(self.program["programId"], "OCR-V0-001")
        self.assertEqual(
            self.program["status"],
            "level_a_complete_b1_authorized",
        )
        levels = {item["levelId"]: item for item in self.program["levels"]}
        self.assertEqual(
            levels["A"]["status"],
            "completed",
        )
        self.assertEqual(
            levels["B"]["status"],
            "b1_authorized_remaining_packages_blocked",
        )
        self.assertEqual(levels["D"]["status"], "not_authorized")

    def test_future_architecture_is_conditional(self) -> None:
        decision = self.program["decision"]
        self.assertFalse(decision["architecturePreApproved"])
        self.assertFalse(decision["runActorIsPrerequisite"])
        self.assertFalse(decision["childRunsArePrerequisite"])
        self.assertFalse(decision["primeEngineIsPrerequisite"])
        self.assertFalse(decision["continualHarnessAuthorized"])
        self.assertTrue(decision["strongTranscriptBaselineRequired"])
        self.assertTrue(decision["shadowGraphBeforeAuthoritativeGraph"])

    def test_level_a_is_bounded(self) -> None:
        packages = {item["id"]: item for item in self.program["workPackages"]}
        self.assertEqual(set(packages), {"A1", "A2", "A3", "A4"})
        self.assertEqual(packages["A1"]["owner"], "ordivon-harness")
        self.assertEqual(packages["A2"]["owner"], "ordivon-computing")
        self.assertEqual(packages["A1"]["status"], "completed")
        self.assertEqual(packages["A1"]["progress"]["evidenceGate"], "passed")
        self.assertFalse(packages["A1"]["progress"]["cutoverActivated"])
        self.assertEqual(packages["A3"]["status"], "completed")
        self.assertEqual(packages["A4"]["status"], "completed")
        self.assertFalse(packages["A4"]["completion"]["productionActivated"])
        self.assertEqual(
            packages["A4"]["completion"]["receipt"],
            "research/experiments/cognitive-reform-v0/evidence/a4-staging-rehearsal-f6173b2.json",
        )
        self.assertEqual(
            packages["A3"]["completion"]["versionVector"],
            "research/experiments/cognitive-reform-v0/system-version-vector-v1.json",
        )
        self.assertIn("production_cutover_activation", packages["A1"]["outOfScope"])
        self.assertIn("product_behavior_change", packages["A2"]["outOfScope"])

    def test_level_a_core_does_not_block_b1_or_require_production(self) -> None:
        progress = self.program["levelAProgress"]
        self.assertEqual(progress["aCore"]["status"], "completed")
        self.assertEqual(progress["aRelease"]["status"], "completed")
        self.assertEqual(progress["aDeploy"]["status"], "completed")
        self.assertFalse(progress["aDeploy"]["productionActivated"])
        self.assertTrue(progress["aDeploy"]["stagingCleanupCompleted"])
        self.assertEqual(progress["levelAStatus"], "completed")
        self.assertFalse(progress["aDeploy"]["productionActivationRequiredForLevelB"])
        self.assertTrue(progress["b1ObservationMinimumCoreAuthorized"])

    def test_observation_is_split_by_real_consumer_need(self) -> None:
        observation = self.program["observationExecution"]
        self.assertIn("in_process_sqlite_ingest", observation["minimumCore"])
        self.assertIn("run_once_harness_exporter", observation["minimumCore"])
        self.assertIn("open_telemetry_bridge", observation["productionHardeningDeferred"])
        self.assertIn("million_event_benchmark", observation["productionHardeningDeferred"])

    def test_revisions_are_exact(self) -> None:
        revisions = self.program["observedRevisions"]
        self.assertEqual(
            set(revisions), {"computing", "host", "harness", "runtime", "protocol"}
        )
        for revision in revisions.values():
            self.assertEqual(len(revision), 40)
            int(revision, 16)


if __name__ == "__main__":
    unittest.main()
