from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "plan-v1.json"


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


class ContinuousExperimentLoopPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    def test_identity_status_and_integrity(self) -> None:
        self.assertEqual(self.plan["schemaVersion"], 1)
        self.assertEqual(
            self.plan["kind"],
            "ordivon.continuous-experiment-loop-plan",
        )
        self.assertEqual(self.plan["planId"], "CEL-R4-001")
        self.assertEqual(self.plan["status"], "designed_not_executed")
        self.assertEqual(
            self.plan["integrity"],
            {
                "algorithm": "sha256",
                "canonicalization": "ordivon-evidence-json-v1",
                "payloadDigest": canonical_digest(self.plan),
            },
        )

    def test_prerequisites_keep_observation_trial_and_campaign_separate(self) -> None:
        self.assertEqual(
            [item["planId"] for item in self.plan["prerequisites"]],
            ["HHO-P0-P1-001", "HHR-R3-001"],
        )
        decisions = self.plan["decisions"]
        self.assertTrue(decisions["observationIsSensingOnly"])
        self.assertTrue(decisions["formalTrialOwnsValidity"])
        self.assertTrue(decisions["campaignRecordsAreResearchOnly"])

    def test_no_platform_or_automatic_promotion_is_authorized(self) -> None:
        decisions = self.plan["decisions"]
        for key in (
            "newRepositoryAuthorized",
            "databaseAuthorized",
            "daemonAuthorized",
            "schedulerAuthorized",
            "automaticMergeAuthorized",
            "automaticDeploymentAuthorized",
            "automaticDatasetAdmission",
        ):
            self.assertFalse(decisions[key])
        self.assertTrue(decisions["humanOwnsPromotion"])

    def test_roles_have_non_overlapping_authority_boundaries(self) -> None:
        roles = {item["roleId"]: item for item in self.plan["roles"]}
        self.assertEqual(
            set(roles),
            {
                "proposer",
                "implementer",
                "evaluator",
                "search_controller",
                "human_release_authority",
            },
        )
        self.assertIn("mark_trial_valid", roles["proposer"]["forbidden"])
        self.assertIn("override_invalidity", roles["search_controller"]["forbidden"])
        self.assertIn("merge", roles["human_release_authority"]["may"])

    def test_trial_disposition_separates_validity_outcome_and_failure(self) -> None:
        disposition = self.plan["trialDisposition"]
        self.assertEqual(disposition["validity"], ["valid", "invalid", "unknown"])
        self.assertIn("accepted", disposition["semanticOutcome"])
        self.assertIn("not_reached", disposition["semanticOutcome"])
        self.assertIn("regressed", disposition["comparativeOutcome"])
        self.assertIn("not_applicable", disposition["comparativeOutcome"])
        self.assertIn("infrastructure", disposition["failureAttribution"])
        self.assertIn("evaluator", disposition["failureAttribution"])
        self.assertIn("validity_is_valid", disposition["selectionEligibleWhen"])
        self.assertIn(
            "required_observation_streams_complete",
            disposition["selectionEligibleWhen"],
        )

    def test_search_is_bounded_and_keeps_baseline_and_replication(self) -> None:
        policy = self.plan["searchPolicy"]
        self.assertEqual(policy["maxRounds"], 3)
        self.assertEqual(policy["maxCandidatesPerRoundIncludingBaseline"], 4)
        self.assertEqual(policy["validTrialsPerCandidateForDevelopment"], 3)
        self.assertTrue(policy["baselineRetainedEveryRound"])
        self.assertEqual(policy["freshReplicationForProvisionalWinner"], 1)
        self.assertTrue(policy["hardGatesDominatePerformance"])
        self.assertTrue(policy["noGlobalScoreRequired"])

    def test_first_live_campaign_optimizes_gateway_without_semantic_drift(self) -> None:
        e1 = next(
            item
            for item in self.plan["firstEvidenceProgram"]
            if item["phaseId"] == "E1"
        )
        self.assertIn("sqlite_indexes", e1["allowedSurface"])
        self.assertIn("privacy_rules", e1["forbiddenSurface"])
        self.assertIn("owner_mappings", e1["forbiddenSurface"])
        self.assertEqual(
            e1["promotionBoundary"],
            "candidate_commit_and_review_packet_only",
        )

    def test_anti_gaming_and_negative_result_requirements_are_explicit(self) -> None:
        anti = set(self.plan["antiGaming"])
        self.assertIn("hidden_grader_and_holdout_not_model_visible", anti)
        self.assertIn("candidate_patch_digest_frozen_before_trials", anti)
        self.assertIn("evaluator_disagreement_blocks_promotion", anti)
        self.assertTrue(self.plan["decisions"]["negativeResultsRetained"])
        self.assertIn(
            "campaign_retains_useful_negative_or_null_result",
            self.plan["acceptanceGates"],
        )

    def test_ready_frontier_does_not_claim_current_implementation(self) -> None:
        self.assertEqual(
            self.plan["readyFrontier"][0],
            "finish_hho_p0_closeout",
        )
        self.assertEqual(
            self.plan["readyFrontier"][-1],
            "run_e1_observation_gateway_self_optimization",
        )

    def test_no_secret_paths_or_reasoning_requirement(self) -> None:
        rendered = json.dumps(self.plan, sort_keys=True).lower()
        for forbidden in (
            "api_key",
            "bearer_token",
            "/root/.config/ordivon/secrets",
            'rawprivatereasoningrequired": true',
        ):
            self.assertNotIn(forbidden, rendered)


if __name__ == "__main__":
    unittest.main()
