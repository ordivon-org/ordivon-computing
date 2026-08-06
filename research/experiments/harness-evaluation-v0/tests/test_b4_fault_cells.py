from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "b4_fault_cells.py"


def load_module():
    spec = importlib.util.spec_from_file_location("b4_fault_cells_tested", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load b4_fault_cells.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cells = load_module()


class B4FaultCellTests(unittest.TestCase):
    def test_execute_records_only_digests_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = cells._execute(
                cell_id="CELL-OK",
                command=("/usr/bin/python3", "-c", "print('bounded output')"),
                cwd=Path(directory),
                expected_test_count=1,
            )
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["exitCode"], 0)
        self.assertEqual(result["expectedTestCount"], 1)
        self.assertEqual(
            set(result),
            {
                "cellId",
                "status",
                "expectedTestCount",
                "exitCode",
                "stdoutDigest",
                "stderrDigest",
            },
        )
        self.assertNotIn("bounded output", json.dumps(result))

    def test_execute_failure_reports_digests_without_raw_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(cells.B4FaultCellError) as caught:
                cells._execute(
                    cell_id="CELL-FAIL",
                    command=(
                        "/usr/bin/python3",
                        "-c",
                        "import sys; print('private output'); sys.exit(7)",
                    ),
                    cwd=Path(directory),
                    expected_test_count=1,
                )
        message = str(caught.exception)
        self.assertIn("exit 7", message)
        self.assertIn("stdoutDigest=sha256:", message)
        self.assertNotIn("private output", message)

    def test_aggregate_receipt_binds_revision_and_integrity(self) -> None:
        outcomes = [
            {
                "cellId": "HOST-STALE-ASSIGNMENT",
                "status": "passed",
                "expectedTestCount": 1,
                "exitCode": 0,
                "stdoutDigest": "sha256:" + "a" * 64,
                "stderrDigest": "sha256:" + "b" * 64,
            },
            {
                "cellId": "HARNESS-INVALID-TOOL-CORRECTION",
                "status": "passed",
                "expectedTestCount": 2,
                "exitCode": 0,
                "stdoutDigest": "sha256:" + "c" * 64,
                "stderrDigest": "sha256:" + "d" * 64,
            },
            {
                "cellId": "OBSERVATION-GAP-MAPPING-CORRUPTION-PRIVACY",
                "status": "passed",
                "expectedTestCount": 7,
                "exitCode": 0,
                "stdoutDigest": "sha256:" + "e" * 64,
                "stderrDigest": "sha256:" + "f" * 64,
            },
        ]
        with mock.patch.object(
            cells,
            "_git",
            side_effect=["1" * 40, ""],
        ), mock.patch.object(cells, "_execute", side_effect=outcomes):
            receipt = cells.run_b4_fault_cells(
                computing_root=Path("/tmp/computing"),
                harness_root=Path("/tmp/harness"),
                harness_revision="1" * 40,
            )
        integrity = receipt.pop("integrity")
        encoded = json.dumps(
            receipt,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        self.assertEqual(
            integrity["payloadDigest"],
            "sha256:" + hashlib.sha256(encoded).hexdigest(),
        )
        self.assertTrue(receipt["allPassed"])
        self.assertFalse(receipt["liveTrialUnlockedByThisRecordAlone"])
        self.assertFalse(receipt["b6Implemented"])


if __name__ == "__main__":
    unittest.main()
