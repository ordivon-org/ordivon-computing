import unittest

from conflicts import classify_finding, summarize_findings


class ConflictTests(unittest.TestCase):
    def test_contained_path_mismatch_is_observation_context_not_owner_drift(self):
        finding = {"name": "path:canonical-human", "severity": "error"}
        result = classify_finding(
            finding,
            observer_path="/usr/bin:/bin",
            canonical_human_path="/root/tools/bin:/usr/local/bin:/usr/bin:/root/.local/bin",
        )
        self.assertEqual(result["classification"], "observer_context_mismatch")
        self.assertFalse(result["centralPolicyMutationAllowed"])

    def test_provider_and_policy_drift_remain_distinct(self):
        result = summarize_findings(
            [
                {"name": "path:user-local-allowlist", "severity": "error"},
                {"name": "package-forbidden:msitools", "severity": "error"},
                {"name": "windows-live:ambient-interop-privilege", "severity": "warning"},
            ]
        )
        self.assertEqual(result["counts"]["provider_placement_drift"], 1)
        self.assertEqual(result["counts"]["owner_policy_drift"], 1)
        self.assertEqual(result["counts"]["ambient_privilege_warning"], 1)


if __name__ == "__main__":
    unittest.main()
