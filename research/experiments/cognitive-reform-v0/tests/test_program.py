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
            "level_a_complete_b4_complete_b5_ready",
        )
        levels = {item["levelId"]: item for item in self.program["levels"]}
        self.assertEqual(
            levels["A"]["status"],
            "completed",
        )
        self.assertEqual(
            levels["B"]["status"],
            "b4_complete_b5_ready",
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
        self.assertEqual(set(packages), {"A1", "A2", "A3", "A4", "B1", "B2-C", "B2-J", "B2-H", "B2-A", "B2-R", "B3", "B4", "B5", "B6"})
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
        self.assertEqual(packages["B1"]["status"], "completed")
        self.assertEqual(packages["B1"]["completion"]["tests"], 21)
        self.assertIn("owner_exporters", packages["B1"]["outOfScope"])
        self.assertEqual(packages["B2-C"]["status"], "completed")
        self.assertEqual(
            packages["B2-C"]["completion"]["contractRevision"],
            "ad1d0240966441e783c1ce9ef0f79f710580ba70",
        )
        self.assertEqual(
            packages["B2-C"]["completion"]["streamSemantics"]["runtime"],
            "one_stream_per_runtime_job",
        )

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

    def test_b1_through_b4_are_closed_and_b5_is_ready(self) -> None:
        progress = self.program["levelBProgress"]
        self.assertEqual(progress["B1"]["status"], "completed")
        self.assertEqual(progress["exporters"]["status"], "completed")
        self.assertEqual(
            progress["exporters"]["packages"],
            {"B2-H": "completed", "B2-A": "completed", "B2-R": "completed"},
        )
        self.assertEqual(
            progress["exporters"]["sharedContractRevision"],
            "b0973311d84b0debe30ca002e15e02401e16ee36",
        )
        self.assertEqual(progress["B3"]["status"], "completed")
        self.assertFalse(progress["B3"]["trialValidityInferred"])
        self.assertEqual(progress["B3"]["artifactCoverage"], "owner_native_only")
        self.assertEqual(progress["B4"]["status"], "completed")
        self.assertEqual(
            progress["B4"]["implementationRevision"],
            "78de3a6225802ea6eb7d8970eaabc1cca1e25407",
        )
        self.assertEqual(
            progress["B4"]["receiptRevision"],
            "fe4ba60c56f58017513b00b8b8fc54d0e7ffa57a",
        )
        self.assertTrue(progress["B4"]["liveTrialUnlocked"])
        self.assertFalse(progress["B4"]["productionActivated"])
        self.assertEqual(progress["B5"]["status"], "ready")
        self.assertEqual(progress["B5"]["blockers"], [])
        self.assertEqual(progress["B5"]["requiredValidTrials"], 3)
        self.assertFalse(progress["B5"]["b6MayStart"])
        self.assertEqual(
            progress["B5"]["selectedVersionVector"]["harness"],
            "437de1666a4124bc8a2791ee1a52456f913e9677",
        )
        gate = progress["B5"]["harnessConclusionGate"]
        self.assertEqual(
            gate["implementationRevision"],
            "b23d5fa6c820c10f937f48cc16c2d8e03d3e18ae",
        )
        self.assertEqual(
            gate["receiptDigest"],
            "sha256:a35fb2a4859657069b112cc3172dcb5e0f2aeb748d0fe693ff09c0dd95a1218a",
        )
        self.assertEqual(gate["status"], "verified")
        self.assertEqual(
            progress["B6"]["status"],
            "blocked_by_B5_and_explicit_review",
        )

    def test_observation_is_split_by_real_consumer_need(self) -> None:
        observation = self.program["observationExecution"]
        self.assertIn("in_process_sqlite_ingest", observation["minimumCore"])
        self.assertIn("run_once_harness_exporter", observation["minimumCore"])
        self.assertIn("open_telemetry_bridge", observation["productionHardeningDeferred"])
        self.assertIn("million_event_benchmark", observation["productionHardeningDeferred"])

    def test_revision_authority_is_explicit(self) -> None:
        authority = self.program["revisionAuthority"]
        revisions = {
            "authority": authority["authoritySourceRevision"],
            "contract": authority["sharedContractRevision"],
            **authority["selectedOwnerRevisions"],
            **authority["implementationRevisions"],
            **authority["receiptRevisions"],
        }
        self.assertEqual(
            authority["implementationRevisions"],
            {
                "B2-H": "e1c134f330a90c15495126a67021b06c56245156",
                "B2-A": "e3cb34b4991b5f52e1c0ed0151ea17b067e88e16",
                "B2-R": "8c22c2b409e99a0fd07fd72a9029ef8c74c6cb47",
            },
        )
        self.assertEqual(
            authority["selectedOwnerRevisions"],
            {
                "host": "a76a620160b28d870670696e04c39e539296fe00",
                "harness": "437de1666a4124bc8a2791ee1a52456f913e9677",
                "runtime": "a455fd01ce0dea25684956e5e5da899d41832a1b",
                "protocol": "420dc356cb664d75db0f34f356156baebe5843db",
            },
        )
        for revision in revisions.values():
            self.assertEqual(len(revision), 40)
            int(revision, 16)

    def test_level_b_packages_have_executable_closeout(self) -> None:
        packages = {item["id"]: item for item in self.program["workPackages"]}
        self.assertEqual(packages["B2-J"]["status"], "completed")
        for package_id in ("B2-H", "B2-A", "B2-R"):
            package = packages[package_id]
            self.assertEqual(package["status"], "completed")
            self.assertIn("completion", package)
            self.assertIn("receipt", package["completion"])
            self.assertIn("implementationRevision", package["completion"])
        self.assertEqual(packages["B3"]["status"], "completed")
        self.assertEqual(
            packages["B3"]["completion"]["implementationRevision"],
            "e9bc8b49941fb332f9f1f5774588bddca72a5b49",
        )
        self.assertEqual(
            packages["B3"]["completion"]["receiptRevision"],
            "e6e480b03a7db336b950b73d8a837ef1799bde12",
        )
        self.assertTrue(packages["B3"]["completion"]["formalRunnerUnblocked"])
        self.assertFalse(packages["B3"]["completion"]["liveTrialUnlocked"])
        self.assertEqual(packages["B4"]["status"], "completed")
        self.assertEqual(
            packages["B4"]["completion"]["implementationRevision"],
            "78de3a6225802ea6eb7d8970eaabc1cca1e25407",
        )
        self.assertEqual(
            packages["B4"]["completion"]["receiptRevision"],
            "fe4ba60c56f58017513b00b8b8fc54d0e7ffa57a",
        )
        self.assertTrue(packages["B4"]["completion"]["liveTrialUnlocked"])
        self.assertFalse(packages["B4"]["completion"]["productionActivated"])
        self.assertFalse(packages["B4"]["completion"]["b6Implemented"])
        self.assertEqual(packages["B5"]["status"], "ready")
        self.assertEqual(packages["B6"]["status"], "blocked_by_B5")
        closeout = self.program["p0P4Closeout"]
        self.assertEqual(closeout["status"], "completed")
        self.assertFalse(closeout["formalTrialUnlocked"])


if __name__ == "__main__":
    unittest.main()
