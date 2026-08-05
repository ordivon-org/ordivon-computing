from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import duckdb

from ordivon_eval_data.projection import project, validate_projection

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]


class ProjectionTests(unittest.TestCase):
    def test_projection_is_relationally_valid_and_repeatable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ordivon-eval-project-") as temporary:
            output_root = Path(temporary) / "evaluation"
            first = project(REPOSITORY_ROOT, output_root)
            second = project(REPOSITORY_ROOT, output_root)

            self.assertEqual(first, second)
            self.assertEqual(
                first["inventory"],
                {"tasks": 7, "trials": 10, "results": 10, "failures": 6},
            )
            self.assertEqual(validate_projection(output_root), first)
            self.assertEqual(len(list((output_root / "generations").iterdir())), 1)

            database = output_root / "current" / "evaluation.duckdb"
            connection = duckdb.connect(str(database), read_only=True)
            try:
                counts = connection.execute(
                    """
                    SELECT
                        (SELECT count(*) FROM tasks),
                        (SELECT count(*) FROM trials),
                        (SELECT count(*) FROM results),
                        (SELECT count(*) FROM failures),
                        (SELECT count(*) FROM result_metrics),
                        (SELECT count(*) FROM verifier_assertions)
                    """
                ).fetchone()
                self.assertEqual(counts, (7, 10, 10, 6, 150, 21))
                missing_timestamps = connection.execute(
                    "SELECT count(*) FROM trials WHERE started_at_ms IS NULL"
                ).fetchone()[0]
                self.assertEqual(missing_timestamps, 1)
                eligible = connection.execute(
                    "SELECT count(*) FROM trials WHERE comparison_eligible"
                ).fetchone()[0]
                self.assertEqual(eligible, 0)
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
