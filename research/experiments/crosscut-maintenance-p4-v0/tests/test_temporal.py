from __future__ import annotations

import unittest

from temporal import EventHintConflict, assess_temporal_validity, make_event_hint, make_snapshot


class TemporalTests(unittest.TestCase):
    def snapshot(self, *, owner: str = "owner-a", observed: int = 1_000):
        return make_snapshot(
            signal_id=f"{owner}:delivery",
            owner=owner,
            observed_at_ms=observed,
            ordering_domain="clock-a",
            invalidation_keys=["source-delivery"],
            facts={},
            max_age_ms=60_000,
        )

    def event(self, *, owner: str = "owner-a", occurred: int = 2_000, available: int = 2_000, change: str = "changed", identity: str = "e1"):
        return make_event_hint(
            event_kind="git.publish.result",
            owner=owner,
            occurred_at_ms=occurred,
            available_at_ms=available,
            ordering_domain="clock-a",
            change_disposition=change,
            event_identity=identity,
        )

    def test_matching_owner_event_invalidates(self):
        result = assess_temporal_validity(self.snapshot(), now_ms=3_000, event_hints=[self.event()])
        self.assertEqual(result["freshnessState"], "invalidated")

    def test_same_key_different_owner_does_not_invalidate(self):
        result = assess_temporal_validity(self.snapshot(owner="owner-b"), now_ms=3_000, event_hints=[self.event(owner="owner-a")])
        self.assertEqual(result["freshnessState"], "fresh")
        self.assertEqual(result["eventTransport"]["suppressedCrossOwner"], 1)

    def test_no_change_event_does_not_invalidate(self):
        result = assess_temporal_validity(self.snapshot(), now_ms=3_000, event_hints=[self.event(change="no_change")])
        self.assertEqual(result["freshnessState"], "fresh")
        self.assertEqual(result["eventTransport"]["suppressedNoChange"], 1)

    def test_event_is_not_visible_before_available_at(self):
        result = assess_temporal_validity(self.snapshot(), now_ms=2_500, event_hints=[self.event(available=3_000)])
        self.assertEqual(result["freshnessState"], "fresh")
        self.assertEqual(result["eventTransport"]["notYetAvailable"], 1)

    def test_old_delayed_event_does_not_invalidate_newer_snapshot(self):
        result = assess_temporal_validity(self.snapshot(observed=4_000), now_ms=5_000, event_hints=[self.event(occurred=2_000, available=5_000)])
        self.assertEqual(result["freshnessState"], "fresh")
        self.assertEqual(result["eventTransport"]["olderThanSnapshot"], 1)

    def test_exact_event_replay_is_deduplicated(self):
        first = self.event(identity="same", available=2_500)
        replay = dict(first)
        replay["availableAtMs"] = 2_800
        replay["eventHintDigest"] = "transport-only-change"
        result = assess_temporal_validity(self.snapshot(), now_ms=3_000, event_hints=[first, replay])
        self.assertEqual(len(result["matchedInvalidations"]), 1)
        self.assertEqual(result["eventTransport"]["deduplicatedReplays"], 1)

    def test_conflicting_event_replay_fails_closed(self):
        first = self.event(identity="same")
        conflicting = self.event(identity="same", occurred=2_100, available=2_100)
        with self.assertRaises(EventHintConflict):
            assess_temporal_validity(self.snapshot(), now_ms=3_000, event_hints=[first, conflicting])

    def test_foreign_ordering_domain_cannot_invalidate(self):
        event = make_event_hint(event_kind="git.publish.result", owner="owner-a", occurred_at_ms=2_000, available_at_ms=2_000, ordering_domain="clock-b", change_disposition="changed")
        result = assess_temporal_validity(self.snapshot(), now_ms=3_000, event_hints=[event])
        self.assertEqual(result["freshnessState"], "fresh")
        self.assertEqual(result["eventTransport"]["foreignOrderingDomain"], 1)

    def test_immutable_evidence_requires_current_binding(self):
        snapshot = make_snapshot(signal_id="proof", owner="owner-a", observed_at_ms=1_000, ordering_domain="clock-a", invalidation_keys=[], facts={}, max_age_ms=None, temporal_class="immutable_evidence", binding_identity={"revision": "a"})
        unknown = assess_temporal_validity(snapshot, now_ms=999_999, event_hints=[])
        changed = assess_temporal_validity(snapshot, now_ms=999_999, event_hints=[], current_binding_identity={"revision": "b"})
        current = assess_temporal_validity(snapshot, now_ms=999_999, event_hints=[], current_binding_identity={"revision": "a"})
        self.assertEqual(unknown["freshnessState"], "binding_unknown")
        self.assertEqual(changed["freshnessState"], "binding_changed")
        self.assertEqual(current["freshnessState"], "immutable_bound")


if __name__ == "__main__":
    unittest.main()
