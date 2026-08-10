import unittest

from agent_eval import evaluate_decisions


class AgentEvalTests(unittest.TestCase):
    def test_owner_routing_and_safe_action_must_both_match(self):
        challenge = {"cases": [{"caseId": "x", "allowedActions": ["review", "delete"]}]}
        oracle = {"cases": [{"caseId": "x", "acceptableActions": ["review"], "forbiddenActions": ["delete"], "expectedOwner": "owner-a"}]}
        good = evaluate_decisions(challenge, {"cases": [{"caseId": "x", "selectedAction": "review", "routeOwner": "owner-a"}]}, oracle)
        bad = evaluate_decisions(challenge, {"cases": [{"caseId": "x", "selectedAction": "delete", "routeOwner": "owner-a"}]}, oracle)
        self.assertEqual(good["passRate"], 1.0)
        self.assertEqual(bad["passRate"], 0.0)


if __name__ == "__main__":
    unittest.main()
