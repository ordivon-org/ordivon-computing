from __future__ import annotations

import unittest

from sparse_events import run_sparse_event_falsifiers


class SparseEventTests(unittest.TestCase):
    def test_sparse_event_boundaries(self):
        result = run_sparse_event_falsifiers()
        self.assertEqual(result["noHint"]["state"], "fresh")
        self.assertFalse(result["noHint"]["absenceProvesNoChange"])
        self.assertGreater(result["noHint"]["staleExposureMs"], 0)
        self.assertEqual(result["delayedHintBeforeArrival"]["state"], "fresh")
        self.assertEqual(result["delayedHintAfterArrival"]["state"], "invalidated")
        self.assertEqual(result["delayedHintAfterArrival"]["matchedInvalidations"], 1)
        self.assertEqual(result["delayedHintAfterArrival"]["deduplicatedReplays"], 1)
        self.assertEqual(result["immediateHint"]["staleExposureMs"], 1)
        self.assertEqual(result["outOfOrderOldHintAfterNewObservation"]["state"], "fresh")
        self.assertEqual(result["outOfOrderOldHintAfterNewObservation"]["matchedInvalidations"], 0)
        self.assertEqual(result["noHintNoOwnerBound"]["state"], "freshness_unbounded")
        self.assertFalse(result["noHintNoOwnerBound"]["actionable"])


if __name__ == "__main__":
    unittest.main()
