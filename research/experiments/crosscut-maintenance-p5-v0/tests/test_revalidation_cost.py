from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RevalidationCostTests(unittest.TestCase):
    def test_local_exact_checks_do_not_justify_a_central_freshness_cache(self):
        doc = json.loads((ROOT / "evidence" / "action-time-revalidation-cost.json").read_text())
        self.assertEqual(doc["samplesPerCheck"], 7)
        self.assertLess(doc["p50Ms"]["runtimeHealthAndDeploymentIdentity"], 200)
        self.assertLess(doc["p50Ms"]["workstationTemporaryEquipmentStatus"], 100)
        self.assertLess(doc["p50Ms"]["runtimeSourceRevision"], 10)
        self.assertIn("do not replace owner currentness with a central cache", doc["optimizationLaw"])


if __name__ == "__main__":
    unittest.main()
