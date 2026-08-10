import unittest

from compatibility import evaluate_entry, summarize


class CompatibilityTests(unittest.TestCase):
    def entry(self):
        return {
            "id": "compat:test",
            "owner": "owner",
            "path": "old.py",
            "reason": "historical source alias",
            "removalPredicate": "no current consumers or durable decode requirement",
            "evidenceRefs": ["grep:current"],
        }

    def test_test_only_self_consumer_does_not_need_to_be_listed_as_current_consumer(self):
        result = evaluate_entry(self.entry())
        self.assertEqual(result["disposition"], "removable_candidate")

    def test_real_consumer_blocks_removal(self):
        entry = self.entry()
        entry["currentConsumers"] = ["runtime-production"]
        self.assertEqual(evaluate_entry(entry)["disposition"], "retain_narrowest_compatible_form")

    def test_removed_entry_is_no_longer_current_debt(self):
        entry = self.entry()
        entry["removed"] = True
        self.assertEqual(evaluate_entry(entry)["disposition"], "removed")

    def test_summary(self):
        removed = self.entry() | {"removed": True}
        retained = self.entry() | {"id": "compat:retained", "currentConsumers": ["consumer"]}
        summary = summarize([removed, retained])
        self.assertEqual(summary["removed"], 1)
        self.assertEqual(summary["removableCandidates"], 0)
        self.assertEqual(summary["retained"], 1)


if __name__ == "__main__":
    unittest.main()
