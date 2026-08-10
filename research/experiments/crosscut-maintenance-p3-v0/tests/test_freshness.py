from __future__ import annotations

import unittest

from freshness import assess_freshness, make_event_hint, make_snapshot


class FreshnessTests(unittest.TestCase):
    def snapshot(self, *, observed=1000, max_age=1000):
        return make_snapshot(signal_id="x", owner="owner-x", observed_at_ms=observed, invalidation_keys=["temporary-equipment"], facts={"state": "old"}, max_age_ms=max_age)

    def test_owner_event_after_snapshot_invalidates_before_age_expiry(self):
        snapshot = self.snapshot()
        event = make_event_hint(event_kind="workstation.temporary-equipment.acquire", occurred_at_ms=1500, owner="workstation")
        result = assess_freshness(snapshot, now_ms=1600, event_hints=[event])
        self.assertEqual(result["freshnessState"], "invalidated")
        self.assertTrue(result["reobserveRequired"])

    def test_event_before_snapshot_does_not_invalidate_new_observation(self):
        snapshot = self.snapshot(observed=2000)
        event = make_event_hint(event_kind="workstation.temporary-equipment.acquire", occurred_at_ms=1500, owner="workstation")
        result = assess_freshness(snapshot, now_ms=2100, event_hints=[event])
        self.assertEqual(result["freshnessState"], "fresh")

    def test_unknown_event_does_not_create_generic_invalidation(self):
        snapshot = self.snapshot()
        event = make_event_hint(event_kind="some.unowned.event", occurred_at_ms=1500, owner="unknown")
        result = assess_freshness(snapshot, now_ms=1600, event_hints=[event])
        self.assertEqual(result["freshnessState"], "fresh")
        self.assertEqual(result["matchedInvalidations"], [])

    def test_age_bound_expires_without_event(self):
        result = assess_freshness(self.snapshot(max_age=500), now_ms=1600, event_hints=[])
        self.assertEqual(result["freshnessState"], "stale")
        self.assertTrue(result["reobserveRequired"])

    def test_missing_owner_freshness_bound_is_not_treated_as_fresh(self):
        snapshot = self.snapshot(max_age=None)
        result = assess_freshness(snapshot, now_ms=1100, event_hints=[])
        self.assertEqual(result["freshnessState"], "freshness_unbounded")
        self.assertFalse(result["actionableWithoutReobservation"])

    def test_immutable_evidence_does_not_age_when_binding_matches(self):
        snapshot = make_snapshot(
            signal_id="build-proof", owner="ordivon-runtime", observed_at_ms=1000,
            invalidation_keys=[], facts={"binaryEqual": True}, max_age_ms=None,
            temporal_class="immutable_evidence", binding_identity={"runtimeRevision": "abc"},
        )
        result = assess_freshness(snapshot, now_ms=999999999, event_hints=[], current_binding_identity={"runtimeRevision": "abc"})
        self.assertEqual(result["freshnessState"], "immutable_bound")
        self.assertTrue(result["actionableWithoutReobservation"])

    def test_immutable_evidence_requires_revalidation_when_binding_changes(self):
        snapshot = make_snapshot(
            signal_id="build-proof", owner="ordivon-runtime", observed_at_ms=1000,
            invalidation_keys=[], facts={"binaryEqual": True}, max_age_ms=None,
            temporal_class="immutable_evidence", binding_identity={"runtimeRevision": "abc"},
        )
        result = assess_freshness(snapshot, now_ms=2000, event_hints=[], current_binding_identity={"runtimeRevision": "def"})
        self.assertEqual(result["freshnessState"], "binding_changed")
        self.assertTrue(result["reobserveRequired"])


if __name__ == "__main__":
    unittest.main()
