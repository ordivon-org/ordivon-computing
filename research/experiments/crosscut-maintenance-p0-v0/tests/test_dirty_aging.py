import unittest

from dirty_aging import HOUR_MS, classify_dirty_workspaces


class DirtyAgingTests(unittest.TestCase):
    def test_dirty_state_is_queued_not_deleted(self):
        now = 1_000 * HOUR_MS
        report = {"candidates": [
            {"workspaceId": "recent", "classification": "blocked_dirty", "lastActivityUnixMs": now - 2 * HOUR_MS},
            {"workspaceId": "checkpoint", "classification": "blocked_dirty", "lastActivityUnixMs": now - 30 * HOUR_MS},
            {"workspaceId": "review", "classification": "blocked_dirty", "lastActivityUnixMs": now - 80 * HOUR_MS},
            {"workspaceId": "quarantine", "classification": "blocked_dirty", "lastActivityUnixMs": now - 200 * HOUR_MS},
            {"workspaceId": "clean", "classification": "closable", "lastActivityUnixMs": now - 500 * HOUR_MS},
        ]}
        result = classify_dirty_workspaces(report, now_ms=now)
        actions = {item["workspaceId"]: item["action"] for item in result["queue"]}
        self.assertEqual(actions["recent"], "recent_dirty")
        self.assertEqual(actions["checkpoint"], "checkpoint_or_export")
        self.assertEqual(actions["review"], "owner_review")
        self.assertEqual(actions["quarantine"], "quarantine_review")
        self.assertNotIn("clean", actions)
        self.assertTrue(all(not item["automaticDeletionAllowed"] for item in result["queue"]))


if __name__ == "__main__":
    unittest.main()
