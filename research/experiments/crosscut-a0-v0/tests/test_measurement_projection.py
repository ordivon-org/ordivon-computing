from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPUTING_ROOT = ROOT.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(
    0,
    str(
        COMPUTING_ROOT
        / "research"
        / "experiments"
        / "observation-plane-v0"
        / "implementation"
    ),
)

from measurement_projection import (  # noqa: E402
    MeasurementProjectionError,
    from_evaluation_metrics,
)

B5_RESULT = (
    COMPUTING_ROOT
    / "research"
    / "experiments"
    / "harness-evaluation-v0"
    / "diagnostics"
    / "b5-native-005-32ec1ea"
    / "result.json"
)


class MeasurementProjectionTests(unittest.TestCase):
    def metrics(self) -> dict[str, object]:
        result = json.loads(B5_RESULT.read_text(encoding="utf-8"))
        return dict(result["metrics"])

    def test_real_b5_metrics_project_without_inventing_cost(self) -> None:
        metrics = self.metrics()
        projection = from_evaluation_metrics(metrics)
        self.assertEqual(
            projection.measurements["ordivon.harness.input_tokens"].value,
            22789,
        )
        self.assertEqual(
            projection.measurements["ordivon.harness.cached_input_tokens"].value,
            17664,
        )
        self.assertIn("estimatedCostUsd", projection.omitted_fields)
        self.assertNotIn("ordivon.cost.estimated_usd", projection.measurements)
        self.assertEqual(
            projection.otel_aliases["ordivon.harness.input_tokens"],
            "gen_ai.usage.input_tokens",
        )

    def test_cost_requires_explicit_basis(self) -> None:
        metrics = self.metrics()
        metrics["estimatedCostUsd"] = 0.25
        with self.assertRaises(MeasurementProjectionError):
            from_evaluation_metrics(metrics)
        projection = from_evaluation_metrics(
            metrics,
            pricing_basis_digest="sha256:" + "a" * 64,
        )
        self.assertEqual(
            projection.measurements["ordivon.cost.estimated_usd"].value,
            0.25,
        )
        self.assertEqual(
            projection.basis_refs["ordivon.cost.estimated_usd"],
            "sha256:" + "a" * 64,
        )

    def test_negative_or_boolean_usage_is_rejected(self) -> None:
        metrics = self.metrics()
        metrics["modelCalls"] = -1
        with self.assertRaises(MeasurementProjectionError):
            from_evaluation_metrics(metrics)
        metrics = self.metrics()
        metrics["toolCalls"] = True
        with self.assertRaises(MeasurementProjectionError):
            from_evaluation_metrics(metrics)


if __name__ == "__main__":
    unittest.main()
