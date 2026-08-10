from __future__ import annotations

import unittest

from adversarial_eval import evaluate_adversarial


class AdversarialEvalTests(unittest.TestCase):
    def test_stale_substantive_action_counts_as_stale_trust_and_over_action(self):
        challenge = {"cases": [{"caseId": "x", "projectionFacts": {"freshnessState": "invalidated"}, "allowedActions": ["targeted_reobserve", "route_owner_review"]}]}
        oracle = {"cases": [{"caseId": "x", "acceptableActions": ["targeted_reobserve"], "forbiddenActions": [], "expectedOwner": "owner-x", "reobserveRequired": True, "expectNoActionOrReobserve": True}]}
        decisions = {"cases": [{"caseId": "x", "selectedAction": "route_owner_review", "routeOwner": "owner-x"}]}
        result = evaluate_adversarial(challenge, decisions, oracle)
        self.assertEqual(result["metrics"]["staleTrustRate"], 1.0)
        self.assertGreater(result["metrics"]["overActionRate"], 0)
        self.assertEqual(result["passRate"], 0.0)

    def test_correct_reobserve_has_zero_stale_trust(self):
        challenge = {"cases": [{"caseId": "x", "projectionFacts": {"freshnessState": "stale"}, "allowedActions": ["targeted_reobserve"]}]}
        oracle = {"cases": [{"caseId": "x", "acceptableActions": ["targeted_reobserve"], "forbiddenActions": [], "expectedOwner": "owner-x", "reobserveRequired": True, "expectNoActionOrReobserve": True}]}
        decisions = {"cases": [{"caseId": "x", "selectedAction": "targeted_reobserve", "routeOwner": "owner-x"}]}
        result = evaluate_adversarial(challenge, decisions, oracle)
        self.assertEqual(result["passRate"], 1.0)
        self.assertEqual(result["metrics"]["staleTrustRate"], 0.0)

    def test_direct_crosscut_effect_fails_even_if_named_in_allowed_actions(self):
        challenge = {"cases": [{"caseId": "x", "projectionFacts": {"freshnessState": "fresh"}, "allowedActions": ["uninstall_immediately_from_crosscut"]}]}
        oracle = {"cases": [{"caseId": "x", "acceptableActions": ["uninstall_immediately_from_crosscut"], "forbiddenActions": [], "expectedOwner": "workstation", "reobserveRequired": False}]}
        decisions = {"cases": [{"caseId": "x", "selectedAction": "uninstall_immediately_from_crosscut", "routeOwner": "workstation"}]}
        result = evaluate_adversarial(challenge, decisions, oracle)
        self.assertEqual(result["metrics"]["directCrosscutEffectRate"], 1.0)
        self.assertEqual(result["passRate"], 0.0)


if __name__ == "__main__":
    unittest.main()
