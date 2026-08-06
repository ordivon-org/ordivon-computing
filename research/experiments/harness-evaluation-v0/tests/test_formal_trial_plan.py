from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "formal-trial-plan-v1.json"
SUITE_PATH = ROOT / "suite-v1.json"


def canonical_digest(value: dict[str, object]) -> str:
    payload = dict(value)
    payload.pop("integrity", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


class FormalTrialPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        cls.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))

    def test_identity_status_and_integrity(self) -> None:
        self.assertEqual(self.plan["schemaVersion"], 1)
        self.assertEqual(
            self.plan["kind"],
            "ordivon.evaluation-formal-trial-plan",
        )
        self.assertEqual(self.plan["planId"], "HHR-R3-001")
        self.assertEqual(
            self.plan["status"],
            "b4_smoke_passed_b5_provider_capability_blocked",
        )
        self.assertEqual(
            self.plan["integrity"],
            {
                "algorithm": "sha256",
                "canonicalization": "ordivon-evidence-json-v1",
                "payloadDigest": canonical_digest(self.plan),
            },
        )

    def test_component_candidates_are_exact_revisions(self) -> None:
        revisions = self.plan["designBase"]
        self.assertEqual(
            set(revisions),
            {
                "computingRevision",
                "hostRevision",
                "harnessRevision",
                "runtimeRevision",
                "protocolRevision",
            },
        )
        for revision in revisions.values():
            self.assertRegex(revision, re.compile(r"^[0-9a-f]{40}$"))

    def test_b4_execution_base_and_closeout_are_exact(self) -> None:
        base = self.plan["executionBase"]
        self.assertEqual(
            base["computingImplementationRevision"],
            "78de3a6225802ea6eb7d8970eaabc1cca1e25407",
        )
        self.assertEqual(
            base["b4ReceiptRevision"],
            "fe4ba60c56f58017513b00b8b8fc54d0e7ffa57a",
        )
        self.assertEqual(
            base["harnessRevision"],
            "ac10497f1b6e681899cfe98c347ed6d48941ba23",
        )
        self.assertEqual(
            base["runtimeRevision"],
            "a455fd01ce0dea25684956e5e5da899d41832a1b",
        )
        closeout = self.plan["b4Closeout"]
        self.assertEqual(closeout["status"], "completed")
        self.assertEqual(closeout["integratedFaultCells"], 4)
        self.assertEqual(closeout["deterministicFaultCellGroups"], 3)
        self.assertTrue(closeout["liveTrialUnlocked"])
        self.assertFalse(closeout["b6Implemented"])

    def test_b5_preflight_selects_verified_conclusion_gate(self) -> None:
        preflight = self.plan["b5Preflight"]
        self.assertEqual(preflight["status"], "blocked_provider_capability")
        self.assertTrue(preflight["sequentialOnly"])
        self.assertEqual(preflight["nextTrialNumber"], 6)
        self.assertEqual(preflight["requiredValidCompleteTrials"], 3)
        self.assertFalse(preflight["b6Authorized"])
        self.assertEqual(
            preflight["invalidAttemptsRetained"],
            [
                "research/experiments/harness-evaluation-v0/diagnostics/b5-native-001-ad3ca58",
                "research/experiments/harness-evaluation-v0/diagnostics/b5-native-002-b7d2c47",
                "research/experiments/harness-evaluation-v0/diagnostics/b5-native-003-1e8eda0",
                "research/experiments/harness-evaluation-v0/diagnostics/b5-native-004-ead663e",
                "research/experiments/harness-evaluation-v0/diagnostics/b5-native-005-32ec1ea",
            ],
        )
        self.assertEqual(preflight["runnerPolicyTextFix"], "implemented")
        self.assertEqual(
            preflight["selectedHarnessRevision"],
            "437de1666a4124bc8a2791ee1a52456f913e9677",
        )
        self.assertEqual(
            preflight["conclusionGateImplementationRevision"],
            "b23d5fa6c820c10f937f48cc16c2d8e03d3e18ae",
        )
        self.assertEqual(
            preflight["conclusionGateReceiptRevision"],
            "437de1666a4124bc8a2791ee1a52456f913e9677",
        )
        self.assertEqual(
            preflight["conclusionGateReceiptDigest"],
            "sha256:a35fb2a4859657069b112cc3172dcb5e0f2aeb748d0fe693ff09c0dd95a1218a",
        )
        self.assertEqual(
            preflight["trialReservation"],
            {
                "acquisition": "exclusive_create",
                "acquireBefore": [
                    "runtime_workspace_open",
                    "provider_dispatch",
                ],
                "collisionPolicy": "fail_closed",
                "releasePolicy": "never",
                "evidenceRecord": "campaign-reservation.json",
                "stateRootMode": "operator_private_0700",
                "recordMode": "0600",
            },
        )
        self.assertEqual(
            preflight["traceEvidence"],
            {
                "record": "trace-summary.json",
                "metadataOnly": True,
                "retains": [
                    "event_sequence",
                    "event_kind",
                    "tool_identity",
                    "stop_code",
                    "error_type",
                    "error_digest",
                    "runtime_error_translation",
                    "tool_observation_summary",
                    "runtime_error_field",
                    "runtime_error_message_digest",
                ],
                "forbids": [
                    "model_content",
                    "tool_arguments",
                    "raw_error_detail",
                ],
            },
        )
        self.assertEqual(
            preflight["runtimeExceptionAdapter"],
            {
                "status": "implemented",
                "revision": "4c885c2934d573eddfba01d826fd13633c3cafd6",
                "sourceContract": "ordivon_host.runtime",
                "targetContract": "ordivon_harness.runtime_port",
                "traceSummaryRecord": "trace-summary.json",
                "trial003Diagnostic": (
                    "research/experiments/harness-evaluation-v0/"
                    "diagnostics/b5-native-003-1e8eda0"
                ),
            },
        )
        self.assertEqual(
            preflight["selectedConfigurationId"],
            "ordivon-harness-deepseek-pro",
        )
        self.assertEqual(preflight["selectedModelId"], "deepseek-v4-pro")
        pivot = preflight["providerPivot"]
        self.assertEqual(pivot["status"], "completed_negative")
        self.assertEqual(
            pivot["sourceTrialDiagnostic"],
            "research/experiments/harness-evaluation-v0/"
            "diagnostics/b5-native-004-ead663e",
        )
        self.assertEqual(
            pivot["proTrialDiagnostic"],
            "research/experiments/harness-evaluation-v0/"
            "diagnostics/b5-native-005-32ec1ea",
        )
        self.assertEqual(
            pivot["fromConfigurationId"],
            "ordivon-harness-deepseek",
        )
        self.assertEqual(
            pivot["toConfigurationId"],
            "ordivon-harness-deepseek-pro",
        )
        self.assertEqual(
            pivot["runnerRevision"],
            "ac7116082198f705cb03ef7d1aae5fa71e1e08a6",
        )
        self.assertTrue(pivot["noFurtherDeepSeekCanaries"])
        self.assertFalse(pivot["architectureComparisonEligible"])
        capability = preflight["providerCapabilityGate"]
        self.assertEqual(capability["status"], "blocked")
        self.assertEqual(capability["blocker"], "provider_tool_call_fidelity")
        self.assertEqual(
            capability["testedModels"],
            ["deepseek-v4-flash", "deepseek-v4-pro"],
        )
        self.assertEqual(
            capability["evidence"],
            [
                "research/experiments/harness-evaluation-v0/"
                "diagnostics/b5-native-004-ead663e",
                "research/experiments/harness-evaluation-v0/"
                "diagnostics/b5-native-005-32ec1ea",
            ],
        )
        self.assertTrue(capability["noFurtherDeepSeekCanaries"])
        self.assertFalse(capability["b6Authorized"])
        self.assertIn(
            "stronger_provider_or_adapter_selected",
            capability["requiredBeforeResume"],
        )

    def test_task_matches_admitted_suite_reference(self) -> None:
        task = self.plan["task"]
        admitted = next(
            family
            for family in self.suite["workloadFamilies"]
            if family["familyId"] == "repository_repair"
        )
        task_ref = admitted["taskRefs"][0]
        self.assertEqual(task["taskId"], task_ref["taskId"])
        self.assertEqual(task["taskVersion"], task_ref["taskVersion"])
        self.assertEqual(task["path"], task_ref["path"])
        self.assertEqual(task["fileDigest"], task_ref["digest"])
        self.assertRegex(task["payloadDigest"], re.compile(r"^sha256:[0-9a-f]{64}$"))
        self.assertNotEqual(task["payloadDigest"], task["fileDigest"])
        self.assertEqual(task["qa"]["cleanRebuildTrials"], 3)
        self.assertEqual(task["qa"]["requiredAgreement"], 3)

    def test_claims_keep_component_ownership_separate(self) -> None:
        claims = self.plan["claims"]
        ids = [claim["claimId"] for claim in claims]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            set(ids),
            {
                "harness_capability",
                "host_semantic_integrity",
                "runtime_physical_reliability",
                "cross_layer_continuity",
            },
        )

    def test_first_campaign_does_not_prematurely_run_all_comparisons(self) -> None:
        first = self.plan["firstCampaign"]
        self.assertEqual(first["status"], "b5_provider_capability_blocked")
        self.assertTrue(first["sequentialOnly"])
        self.assertIn(
            "three_ordivon_harness_deepseek_trials",
            first["phases"],
        )
        self.assertIn("deepseek_flash_negative_canary", first["phases"])
        self.assertIn("deepseek_pro_capability_canary", first["phases"])
        self.assertIn("stronger_provider_preflight", first["phases"])
        self.assertIn("one_shot_live_trials", first["excludedUntilBaselineCloseout"])
        self.assertIn(
            "provider_harness_live_trials",
            first["excludedUntilBaselineCloseout"],
        )
        self.assertEqual(
            first["completedPhases"],
            [
                "complete_campaign_preflight",
                "scripted_integrated_smoke",
                "five_boundary_fault_cells",
                "deepseek_flash_negative_canary",
                "deepseek_pro_negative_canary",
            ],
        )
        self.assertEqual(
            first["nextPhase"],
            "stronger_provider_preflight",
        )

    def test_observation_prerequisite_is_explicit(self) -> None:
        self.assertEqual(
            self.plan["prerequisites"],
            [
                {
                    "planId": "HHO-P0-P1-001",
                    "path": "research/experiments/observation-plane-v0/plan-v1.json",
                    "requiredStatus": "p0_passed_and_p1_core_passed",
                    "reason": "Host and Harness must be independently durable and Host/Harness/Runtime evidence must be automatically queryable before repeated formal Trials.",
                }
            ],
        )

    def test_configurations_share_model_for_future_competitive_cells(self) -> None:
        competitive = [
            configuration
            for configuration in self.plan["configurations"]
            if configuration["competitive"]
        ]
        self.assertEqual(len(competitive), 3)
        self.assertEqual(
            {configuration["providerId"] for configuration in competitive},
            {"deepseek"},
        )
        self.assertEqual(
            {configuration["modelId"] for configuration in competitive},
            {"deepseek-v4-flash"},
        )
        native = next(
            configuration
            for configuration in competitive
            if configuration["configurationId"] == "ordivon-harness-deepseek"
        )
        self.assertEqual(native["repetitions"]["development"], 3)
        self.assertGreaterEqual(native["repetitions"]["architectureDecision"], 5)
        self.assertEqual(native["status"], "negative_canary_observed")
        pro = next(
            configuration
            for configuration in self.plan["configurations"]
            if configuration["configurationId"]
            == "ordivon-harness-deepseek-pro"
        )
        self.assertFalse(pro["competitive"])
        self.assertEqual(pro["providerId"], "deepseek")
        self.assertEqual(pro["modelId"], "deepseek-v4-pro")
        self.assertEqual(pro["executionPath"], "ordivon_harness")
        self.assertEqual(pro["budget"], native["budget"])
        self.assertEqual(pro["status"], "negative_canary_observed")
        self.assertEqual(pro["repetitions"]["architectureDecision"], 0)
        scripted = next(
            configuration
            for configuration in self.plan["configurations"]
            if configuration["configurationId"] == "scripted-integrated-control"
        )
        self.assertEqual(scripted["status"], "completed")

    def test_fault_cells_cover_each_required_boundary(self) -> None:
        cells = self.plan["faultCells"]
        ids = [cell["cellId"] for cell in cells]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(cells), 5)
        self.assertEqual(
            {cell["owner"] for cell in cells},
            {"ordivon-host", "ordivon-harness", "ordivon-runtime", "cross_layer"},
        )
        self.assertTrue(all(cell["deterministic"] for cell in cells))

    def test_trial_disposition_and_observation_selection_are_explicit(self) -> None:
        disposition = self.plan["trialDisposition"]
        self.assertEqual(disposition["validity"], ["valid", "invalid", "unknown"])
        self.assertIn("infrastructure", disposition["failureAttribution"])
        self.assertIn("evaluator", disposition["failureAttribution"])
        self.assertIn("accepted", disposition["semanticOutcome"])
        self.assertIn("not_reached", disposition["semanticOutcome"])
        self.assertIn("regressed", disposition["comparativeOutcome"])
        self.assertIn("not_applicable", disposition["comparativeOutcome"])
        self.assertTrue(disposition["validNegativeResultsRetained"])
        self.assertTrue(
            disposition["invalidAndUnknownExcludedFromPerformanceAggregation"]
        )
        selection = self.plan["observationSelection"]
        self.assertEqual(selection["record"], "ObservationSelectionManifest")
        self.assertFalse(selection["trialValidityInferredByObservation"])
        self.assertIn("selection_digest", selection["contains"])

    def test_experiment_loop_handoff_does_not_expand_r3_authority(self) -> None:
        handoff = self.plan["experimentLoopHandoff"]
        self.assertEqual(handoff["planId"], "CEL-R4-001")
        self.assertTrue(Path(handoff["path"]).exists())
        self.assertIn("candidate_generation", handoff["r3DoesNotOwn"])
        self.assertIn("automatic_promotion", handoff["r3DoesNotOwn"])
        first = self.plan["firstCampaign"]
        self.assertIn(
            "automatic_candidate_generation",
            first["excludedUntilBaselineCloseout"],
        )
        self.assertIn("multi_round_search", first["excludedUntilBaselineCloseout"])

    def test_plan_requires_no_dashboard_or_reasoning_text(self) -> None:
        policy = self.plan["reviewPolicy"]
        self.assertFalse(policy["dashboardRequired"])
        self.assertFalse(policy["rawReasoningRequired"])
        rendered = json.dumps(self.plan, sort_keys=True).lower()
        self.assertNotIn("api_key", rendered)
        self.assertNotIn("bearer_token", rendered)
        self.assertNotIn("/root/.config/ordivon/secrets", rendered)


if __name__ == "__main__":
    unittest.main()
