import unittest

from maintenance import LIFECYCLE_CLASSES, build_projection, cleanup_decision


class MaintenanceTests(unittest.TestCase):
    def test_unknown_and_dirty_never_auto_delete(self):
        self.assertFalse(cleanup_decision("unknown", active_references=False, dirty=False, owner_reclaim_operation="x", rebuildable=True)["automaticActionAllowed"])
        self.assertFalse(cleanup_decision("cache", active_references=False, dirty=True, owner_reclaim_operation="owner.prune", rebuildable=True)["automaticActionAllowed"])

    def test_owner_rebuildable_cache_can_be_candidate(self):
        result = cleanup_decision("cache", active_references=False, dirty=False, owner_reclaim_operation="runtime.cache.prune", rebuildable=True)
        self.assertEqual(result["decision"], "owner_reclaim_candidate")
        self.assertTrue(result["automaticActionAllowed"])

    def test_projection_is_explicitly_non_authoritative(self):
        projection = build_projection(
            host_status={"doctor": {"checks": [{"name": "x", "status": "ok"}]}, "authority": {"tasks": 1}},
            runtime_status={"status": "healthy", "health": {"status": "healthy"}, "deployment": {"commit": "abc", "artifacts": []}, "service": {"activeState": "active"}, "registry": {"recoveryRequired": 0}},
            runtime_lifecycle={"summary": {"counts": {"blocked_dirty": 1}, "policyEligible": 2}},
            runtime_cache={"summary": {"legacyBytes": 10, "sourceGroups": 2}, "issues": []},
            content_baseline={"repositories": [], "totals": {"repositories": 0}},
            conformance_status={"passed": True, "exitCode": 0, "blockedBy": None},
            owner_doctors=[
                {"owner": "ordivon-world", "sourceKind": "doctor", "status": "ok", "checks": 2, "failedChecks": [], "skippedChecks": 1},
                {"owner": "workstation-lab", "sourceKind": "doctor", "status": "fail", "checks": 3, "failedChecks": [{"name": "path"}], "skippedChecks": 0},
            ],
            compatibility_summary={"entries": 0, "removableCandidates": 0, "unsupportedDebt": 0},
            dirty_aging_summary={"dirtyWorkspaces": 1, "actionable": 1},
        )
        self.assertEqual(projection["lifecycleVocabulary"], list(LIFECYCLE_CLASSES))
        self.assertFalse(projection["truthBoundary"]["projectionAuthoritative"])
        self.assertTrue(projection["truthBoundary"]["dirtyNeverAutoDeleted"])
        self.assertEqual(projection["signals"][1]["area"], "runtime-health-and-deployment")


if __name__ == "__main__":
    unittest.main()
