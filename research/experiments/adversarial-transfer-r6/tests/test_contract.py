from __future__ import annotations

import unittest
from types import SimpleNamespace

from ordivon_host import ArtifactRef

from anc_adversarial_transfer.model import TrialSpec
from anc_adversarial_transfer.runner import (
    ATTACKS,
    MAX_MODEL_CALLS,
    MAX_TOOL_CALLS,
    MODELS,
    PROFILES,
    VERIFIER_PATH,
    _artifact_locations,
    _grant,
    _runtime_artifact_exists,
    _stop_detail,
    _trial_plan,
)


class R6ContractTests(unittest.TestCase):
    def test_live_budget_allows_real_verification_turns(self) -> None:
        self.assertGreaterEqual(MAX_MODEL_CALLS, 12)
        self.assertGreaterEqual(MAX_TOOL_CALLS, 24)

    def test_default_plan_has_flash_full_matrix_and_pro_two_profiles(self) -> None:
        plan = _trial_plan(attacks=ATTACKS, profiles=PROFILES, models=MODELS)
        self.assertEqual(len(plan), 32)
        self.assertEqual(len({item.trial_id for item in plan}), 32)
        flash = [item for item in plan if item.model == "deepseek-v4-flash"]
        pro = [item for item in plan if item.model == "deepseek-v4-pro"]
        self.assertEqual(len(flash), 24)
        self.assertEqual(len(pro), 8)
        self.assertEqual({item.profile for item in pro}, {"raw-ambient", "harness-gated"})

    def test_poisoned_catalog_has_broad_and_gated_authority_profiles(self) -> None:
        self.assertIn("harness-ambient-poisoned-catalog", PROFILES)
        self.assertIn("harness-gated-poisoned-catalog", PROFILES)

    def test_gated_profile_can_read_fixed_verifier_but_not_canary(self) -> None:
        spec = TrialSpec(
            "trial:gated",
            "deepseek-v4-flash",
            "harness-gated",
            "authority-spoof",
            "research/experiments/adversarial-transfer-r6/fixture/attacks/authority-spoof.md",
            "research/experiments/adversarial-transfer-r6/fixture/output/trial-gated.md",
        )
        grant = _grant(spec)
        self.assertTrue(grant.allows_path("read_workspace", VERIFIER_PATH))
        self.assertFalse(
            grant.allows_path(
                "read_workspace",
                "research/experiments/adversarial-transfer-r6/fixture/canary/secret.txt",
            )
        )

    def test_output_paths_are_trial_unique_and_fixture_local(self) -> None:
        plan = _trial_plan(attacks=ATTACKS, profiles=PROFILES, models=("deepseek-v4-flash",))
        paths = {item.output_path for item in plan}
        self.assertEqual(len(paths), len(plan))
        self.assertTrue(all("adversarial-transfer-r6/fixture/output/" in item for item in paths))

    def test_stop_detail_is_recovered_from_the_terminal_trace_event(self) -> None:
        result = SimpleNamespace(
            trace=SimpleNamespace(
                events=(
                    SimpleNamespace(kind="run_started", payload={}),
                    SimpleNamespace(
                        kind="run_stopped",
                        payload={"detail": "model returned an invalid Tool argument"},
                    ),
                )
            )
        )
        self.assertEqual(
            _stop_detail(result),
            "model returned an invalid Tool argument",
        )

    def test_runtime_artifact_existence_binds_job_identity_and_digest(self) -> None:
        ref = ArtifactRef(
            ref="artifact:r6:stdout",
            kind="stdout",
            digest="sha256:" + "a" * 64,
        )
        result = SimpleNamespace(
            observations=(
                SimpleNamespace(runtime_job_ref="job:r6", artifact_refs=(ref,)),
            )
        )
        locations = _artifact_locations(result)

        class Runtime:
            def call_tool(self, name, arguments):
                self.name = name
                self.arguments = arguments
                return {
                    "jobId": "job:r6",
                    "artifactId": "artifact:r6:stdout",
                    "digest": "sha256:" + "a" * 64,
                    "content": "x",
                }

        runtime = Runtime()
        self.assertTrue(_runtime_artifact_exists(runtime, locations, ref))
        self.assertEqual(runtime.name, "artifact.read")
        self.assertEqual(runtime.arguments["maxBytes"], 1)
        changed = ArtifactRef(
            ref=ref.ref,
            kind=ref.kind,
            digest="sha256:" + "b" * 64,
        )
        self.assertFalse(_runtime_artifact_exists(runtime, locations, changed))


if __name__ == "__main__":
    unittest.main()
