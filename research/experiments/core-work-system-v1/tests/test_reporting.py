from __future__ import annotations

import json
from pathlib import Path
import unittest

from anc_core_work_system.reporting import derive_report_statistics


ROOT = Path(__file__).resolve().parents[1]


class ReportingTests(unittest.TestCase):
    def test_statistics_are_derived_from_bound_evidence(self) -> None:
        matrix = json.loads((ROOT / "evidence" / "deterministic-matrix.json").read_text())
        live = json.loads((ROOT / "evidence" / "live-provider-gauntlet.json").read_text())
        value = derive_report_statistics(matrix, live)
        self.assertEqual(value["deterministic"]["trials"], 16)
        self.assertEqual(value["deterministic"]["passed"], 10)
        self.assertEqual(value["live"]["accepted"], 6)
        self.assertEqual(value["live"]["reportedProviderTokens"]["total"], 10358)
        self.assertAlmostEqual(
            value["derivedComparisons"][
                "sourceBoundContextByteOverheadVsCurrentRetrieval"
            ],
            0.129808,
        )
        self.assertAlmostEqual(
            value["derivedComparisons"][
                "evidenceRichInterruptionReductionVsApprovalEverywhere"
            ],
            0.416667,
        )
        self.assertEqual(
            value["derivedComparisons"]["effectStateObjects"]["ordivon-effect"],
            6,
        )

    def test_full_report_binds_statistics_and_limitations(self) -> None:
        statistics = json.loads((ROOT / "evidence" / "report-statistics.json").read_text())
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn(statistics["statisticsDigest"], report)
        self.assertIn("action-order bias", report)
        self.assertIn("not a performance ranking", report)
        self.assertIn("configuration and invocation evidence", report)
        self.assertIn("state portability**, not **performance", report)


if __name__ == "__main__":
    unittest.main()
