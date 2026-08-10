import unittest

from events import targeted_reobservation


class EventTests(unittest.TestCase):
    def test_release_reobserves_delivery_and_health_only(self):
        result = targeted_reobservation({"kind": "runtime.release.result"})
        self.assertEqual(result["targetedSignals"], ["source-delivery", "runtime-health"])
        self.assertFalse(result["fullGlobalScanRequired"])
        self.assertFalse(result["centralEffectAuthorized"])

    def test_equipment_release_does_not_trigger_global_scan(self):
        result = targeted_reobservation({"kind": "workstation.temporary-equipment.release"})
        self.assertEqual(result["decision"], "targeted_reobserve")
        self.assertIn("temporary-equipment", result["targetedSignals"])
        self.assertFalse(result["fullGlobalScanRequired"])

    def test_unknown_event_is_not_promoted_into_a_generic_loop(self):
        result = targeted_reobservation({"kind": "some.unowned.event"})
        self.assertEqual(result["decision"], "no_maintenance_trigger")
        self.assertEqual(result["targetedSignals"], [])


if __name__ == "__main__":
    unittest.main()
