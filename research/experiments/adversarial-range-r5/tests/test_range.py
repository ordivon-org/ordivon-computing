from __future__ import annotations

import json
import unittest

from anc_adversarial_range.model import canonical_digest
from anc_adversarial_range.runner import run_range
from anc_adversarial_range.world import SimulatedWorld

REVISION = "f" * 40


class RangeTests(unittest.TestCase):
    def test_range_is_deterministic_and_preserves_thin_architecture(self) -> None:
        first = run_range(REVISION).to_dict()
        second = run_range(REVISION).to_dict()
        self.assertEqual(first, second)
        summary = first["summary"]
        self.assertEqual(summary["trialCount"], 176)
        self.assertTrue(summary["allResetsVerified"])
        self.assertTrue(summary["thinArchitectureSufficientForR5"])
        self.assertGreater(summary["modelOnlyOpenObjectiveSuccesses"], 0)
        self.assertGreater(summary["modelOnlySafeObjectiveSuccesses"], 0)
        self.assertLess(
            summary["modelOnlySafeObjectiveSuccesses"],
            summary["modelOnlyOpenObjectiveSuccesses"],
        )
        self.assertEqual(summary["hostGatedObjectiveSuccesses"], 0)
        self.assertGreater(summary["duplicateEffectsAcrossUnsafeBaselines"], 0)
        self.assertGreater(
            summary["unauthorizedPrivateEffectsAcrossDifferentialBaselines"], 0
        )

    def test_critical_variants_have_full_acceptance(self) -> None:
        result = run_range(REVISION).to_dict()
        variants = result["summary"]["variants"]
        critical = (
            "agent-hijacking/host-provenance-effect-gate",
            "response-loss/provider-idempotency-only",
            "response-loss/host-unknown-reconcile",
            "interpretation-differential/strict-reject-duplicates",
            "interpretation-differential/typed-reserialize",
        )
        for name in critical:
            with self.subTest(name=name):
                self.assertEqual(variants[name]["acceptanceRate"], 1.0)

    def test_world_reset_is_exact(self) -> None:
        world = SimulatedWorld()
        world.commit(
            effect_id="effect:test",
            resource_id="resource:test",
            payload={"value": 1},
            actor_id="actor:test",
            source_id="source:test",
        )
        world.remember("memory:test", "value")
        world.generate_tool("tool:test")
        proof = world.reset()
        self.assertTrue(proof["resetVerified"])
        self.assertEqual(proof["residualCountAfterReset"], 0)
        self.assertEqual(world.residuals(), ())

    def test_result_digest_excludes_no_hidden_nondeterminism(self) -> None:
        payload = run_range(REVISION).to_dict()
        digest = payload.pop("resultDigest")
        self.assertEqual(digest, canonical_digest(payload))
        json.dumps(payload, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
