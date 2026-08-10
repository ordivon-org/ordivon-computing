from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FeatureCourtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((ROOT / "feature-court.json").read_text())

    def test_every_feature_has_a_complete_survival_burden(self):
        rows = self.doc["rows"]
        self.assertGreaterEqual(len(rows), 30)
        ids = [row["id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)))
        required = {"id", "subject", "currentConsumer", "protectedLoss", "strongestSimplerReplacement", "latestPressure", "verdict", "activeCarrier", "reopenCondition"}
        for row in rows:
            self.assertTrue(required <= row.keys(), row["id"])
            self.assertTrue(all(str(row[key]).strip() for key in required), row["id"])
            self.assertIn(row["verdict"], self.doc["verdicts"])

    def test_no_historical_experiment_is_retained_as_shared_implementation(self):
        forbidden = {"P0-E", "P2-D", "P3-B", "P4-H", "P4-J", "P0-P4-GATE"}
        by_id = {row["id"]: row for row in self.doc["rows"]}
        for feature_id in forbidden:
            self.assertEqual(by_id[feature_id]["verdict"], "delete-active")

    def test_owner_local_features_name_the_owner(self):
        by_id = {row["id"]: row for row in self.doc["rows"]}
        self.assertIn("ordivon-runtime", by_id["P1-B"]["activeCarrier"])
        self.assertIn("workstation", by_id["P2-C"]["activeCarrier"])
        self.assertEqual(by_id["P4-D"]["verdict"], "owner-local")


if __name__ == "__main__":
    unittest.main()
