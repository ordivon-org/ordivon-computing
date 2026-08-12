from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / 'experiments' / 'fs0-shadow-portfolio' / 'statistical-calibration-v1.json'


class Fs0StatisticalCalibrationEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = json.loads(CAL.read_text(encoding='utf-8'))

    def test_calibration_is_bound_to_frozen_prediction_receipt(self):
        self.assertEqual(
            self.body['sourcePredictionReceiptDigest'],
            'sha256:bb406bf0907e9bb23fa41c9306c876b5f44b0dfe388008b9eb5c1deb776f89fc',
        )
        self.assertEqual(self.body['method']['name'], 'Wilson score interval')

    def test_small_n_intervals_prevent_point_estimate_overclaim(self):
        raw = self.body['observations']['rawTopChoiceGAF3']['wilson95']
        rfm = self.body['observations']['rfmTopChoiceRP5']['wilson95']
        self.assertLess(raw[0], 0.6)
        self.assertLess(rfm[0], 0.4)
        self.assertFalse(raw[1] < rfm[0] or rfm[1] < raw[0])

    def test_perfect_negative_control_counts_are_not_treated_as_certainty(self):
        neg_top = self.body['observations']['negativeControlTopChoice']['wilson95']
        neg_defer = self.body['observations']['negativeControlDeferral']['wilson95']
        self.assertGreater(neg_top[1], 0.27)
        self.assertLess(neg_defer[0], 0.73)


if __name__ == '__main__':
    unittest.main()
