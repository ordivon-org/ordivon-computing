from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "harness-evaluation-v0/formal-trial-plan-v1.json"
PROGRAM = ROOT / "cognitive-reform-v0/program-v1.json"
OBSERVATION = ROOT / "observation-plane-v0/plan-v1.json"
AUTHORITY = (
    "research/experiments/harness-evaluation-v0/formal-trial-plan-v1.json"
    "#b5Preflight.independentHarnessCapability"
)


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


class IndependentHarnessCapabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.formal = load(FORMAL)
        cls.program = load(PROGRAM)
        cls.observation = load(OBSERVATION)
        cls.capability = cls.formal["b5Preflight"]["independentHarnessCapability"]

    def test_exact_harness_implementation_and_receipt_are_bound(self) -> None:
        value = self.capability
        self.assertEqual(value["capabilityId"], "HHR-INDEPENDENT-EDIT-V2")
        self.assertEqual(value["status"], "verified_noncomparable")
        self.assertEqual(
            value["implementationRevision"],
            "dd50136ef722b9df3dfb0fef195fcc1a137fd8ed",
        )
        self.assertEqual(
            value["evidenceRevision"],
            "593a389d1b035ee46b91b374bf76f40ed2c697ef",
        )
        self.assertEqual(
            value["receipt"],
            "ordivon-harness:evidence/"
            "repository-repair-edit-runtime-bridge-dd50136.json",
        )
        self.assertEqual(
            value["receiptDigest"],
            "sha256:3b89c2f092f7c4cb966751d2227744d5c3b3af7784e1ed2e44d8ad58c3e3c4e0",
        )
        self.assertEqual(
            value["toolSurfaceDigest"],
            "sha256:fc2daeee2a95ff5d83d4efbc17a003788c52277ec582be3a14c34662cf1d51eb",
        )
        self.assertEqual(
            value["toolGrantDigest"],
            "sha256:6c3a0a889c6082448b9e685f3388845e28e1b9ce226e95ad6404835324b37bec",
        )

    def test_runtime_acceptance_is_scripted_clean_and_nonproduction(self) -> None:
        value = self.capability
        self.assertEqual(
            value["runtimeAcceptance"],
            {
                "harnessClean": True,
                "scriptedProvider": True,
                "modelCalls": 8,
                "toolCalls": 6,
                "runtimeJobs": 1,
                "harnessEvents": 37,
                "workspaceClosed": True,
            },
        )
        self.assertIn(
            "workspace_patch_get_response_loss_reconciliation",
            value["guarantees"],
        )
        self.assertIn(
            "v1_surface_and_grant_digests_unchanged",
            value["guarantees"],
        )
        self.assertIn(
            "establish_provider_or_model_capability",
            value["doesNot"],
        )
        self.assertIn(
            "authorize_b6_production_or_architecture_comparison",
            value["doesNot"],
        )

    def test_program_and_observation_only_reference_formal_authority(self) -> None:
        expected = {
            "capabilityId": "HHR-INDEPENDENT-EDIT-V2",
            "authority": AUTHORITY,
            "effectOnB5": "none",
            "effectOnB6": "none",
        }
        progress = self.program["levelBProgress"]["B5"]
        self.assertEqual(progress["independentCapabilityRef"], expected)
        package = next(
            item
            for item in self.program["workPackages"]
            if item["id"] == "B5"
        )
        self.assertEqual(package["adjacentVerifiedCapabilities"], [expected])
        effect = self.observation["formalTrialEffect"]
        self.assertEqual(effect["independentHarnessCapabilityRef"], expected)

    def test_independent_capability_cannot_resume_b5_or_authorize_b6(self) -> None:
        preflight = self.formal["b5Preflight"]
        self.assertEqual(preflight["status"], "blocked_provider_capability")
        self.assertEqual(preflight["nextTrialNumber"], 6)
        self.assertFalse(preflight["b6Authorized"])
        self.assertEqual(
            preflight["selectedHarnessRevision"],
            "437de1666a4124bc8a2791ee1a52456f913e9677",
        )
        self.assertNotEqual(
            preflight["selectedHarnessRevision"],
            self.capability["implementationRevision"],
        )
        provider_gate = preflight["providerCapabilityGate"]
        self.assertEqual(provider_gate["status"], "blocked")
        self.assertTrue(provider_gate["noFurtherDeepSeekCanaries"])
        self.assertFalse(provider_gate["b6Authorized"])
        progress = self.program["levelBProgress"]["B5"]
        self.assertEqual(progress["status"], "blocked_provider_capability")
        self.assertFalse(progress["b6MayStart"])
        effect = self.observation["formalTrialEffect"]
        self.assertFalse(effect["liveTrialUnlocked"])
        self.assertTrue(effect["providerCapabilityBlocked"])


if __name__ == "__main__":
    unittest.main()
