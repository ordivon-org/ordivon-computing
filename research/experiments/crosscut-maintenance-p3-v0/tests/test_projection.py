from __future__ import annotations

import unittest

from freshness import make_event_hint, make_snapshot
from projection import build_temporal_projection


class ProjectionTests(unittest.TestCase):
    def test_event_invalidates_only_matching_signal(self) -> None:
        package = make_snapshot(signal_id="pkg", owner="workstation", observed_at_ms=1000, invalidation_keys=["temporary-equipment"], facts={}, max_age_ms=5000)
        runtime = make_snapshot(signal_id="runtime", owner="ordivon-runtime", observed_at_ms=1000, invalidation_keys=["runtime-health"], facts={}, max_age_ms=5000)
        event = make_event_hint(event_kind="workstation.temporary-equipment.acquire", occurred_at_ms=1500, owner="workstation")
        result = build_temporal_projection(snapshots=[package, runtime], event_hints=[event], now_ms=1600)
        by_id = {item["signalId"]: item for item in result["signals"]}
        self.assertEqual(by_id["pkg"]["freshness"]["freshnessState"], "invalidated")
        self.assertEqual(by_id["runtime"]["freshness"]["freshnessState"], "fresh")
        self.assertEqual(result["summary"]["reobserveSignals"], ["pkg"])

    def test_reobservation_after_event_returns_signal_to_fresh(self) -> None:
        event = make_event_hint(event_kind="workstation.temporary-equipment.acquire", occurred_at_ms=1500, owner="workstation")
        snapshot = make_snapshot(signal_id="pkg", owner="workstation", observed_at_ms=1600, invalidation_keys=["temporary-equipment"], facts={"lease": "active"}, max_age_ms=5000)
        result = build_temporal_projection(snapshots=[snapshot], event_hints=[event], now_ms=1700)
        self.assertEqual(result["signals"][0]["freshness"]["freshnessState"], "fresh")
        self.assertEqual(result["summary"]["actionableSignals"], ["pkg"])

    def test_immutable_evidence_is_identity_gated_not_ttl_gated(self) -> None:
        snapshot = make_snapshot(signal_id="proof", owner="ordivon-runtime", observed_at_ms=1000, invalidation_keys=[], facts={"proved": True}, max_age_ms=None, temporal_class="immutable_evidence", binding_identity={"revision": "a"})
        current = build_temporal_projection(snapshots=[snapshot], event_hints=[], now_ms=999999, current_bindings={"proof": {"revision": "a"}})
        changed = build_temporal_projection(snapshots=[snapshot], event_hints=[], now_ms=999999, current_bindings={"proof": {"revision": "b"}})
        self.assertEqual(current["signals"][0]["freshness"]["freshnessState"], "immutable_bound")
        self.assertEqual(changed["signals"][0]["freshness"]["freshnessState"], "binding_changed")


if __name__ == "__main__":
    unittest.main()
