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
        self.assertEqual(self.plan["status"], "designed_not_executed")
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
        self.assertEqual(first["status"], "blocked_by_hho_p0_p1")
        self.assertTrue(first["sequentialOnly"])
        self.assertIn(
            "three_ordivon_harness_deepseek_trials",
            first["phases"],
        )
        self.assertIn("one_shot_live_trials", first["excludedUntilBaselineCloseout"])
        self.assertIn(
            "provider_harness_live_trials",
            first["excludedUntilBaselineCloseout"],
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
