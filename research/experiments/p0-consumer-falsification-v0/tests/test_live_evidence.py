from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

EXPERIMENT = Path(__file__).resolve().parents[1]
EVIDENCE = EXPERIMENT / "evidence"
LIVE = EVIDENCE / "live"
IMPLEMENTATION = "9b9906e9a6fe3f601f28dabec1652ba2cf6f8cf8"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(document: dict) -> str:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


class P0LiveEvidenceTests(unittest.TestCase):
    def test_live_receipts_are_integrity_valid_and_revision_bound(self) -> None:
        paths = sorted(LIVE.glob("p0-*.json"))
        self.assertEqual(len(paths), 11)
        provider = None
        for path in paths:
            receipt = load(path)
            self.assertEqual(receipt["integrity"]["payloadDigest"], digest(receipt))
            self.assertEqual(
                receipt["ownerVector"]["ordivon-computing"]["head"],
                IMPLEMENTATION,
            )
            self.assertTrue(receipt["trialValidPair"])
            if provider is None:
                provider = receipt["provider"]
            self.assertEqual(receipt["provider"], provider)

    def test_p0_a_scoped_result(self) -> None:
        receipts = [load(LIVE / f"p0-a-live-r{i}.json") for i in range(1, 6)]
        cells = {
            cell_id: [
                next(cell for cell in receipt["cells"] if cell["cellId"] == cell_id)
                for receipt in receipts
            ]
            for cell_id in ("S", "H")
        }
        self.assertEqual(sum(int(row["semanticAccepted"]) for row in cells["S"]), 0)
        self.assertEqual(sum(int(row["semanticAccepted"]) for row in cells["H"]), 3)
        self.assertEqual(
            sum(
                int(
                    row["verifier"]["visiblePassed"]
                    and row["verifier"]["hiddenPassed"]
                    and row["verifier"]["protectedFilesUnchanged"]
                )
                for row in cells["S"]
            ),
            0,
        )
        self.assertEqual(
            sum(
                int(
                    row["verifier"]["visiblePassed"]
                    and row["verifier"]["hiddenPassed"]
                    and row["verifier"]["protectedFilesUnchanged"]
                )
                for row in cells["H"]
            ),
            4,
        )

    def test_p0_b_repeated_authority_timing_effect(self) -> None:
        def rows(fixture: str, treatment: str) -> list[dict]:
            return [
                next(
                    cell
                    for cell in load(LIVE / f"p0-b-{fixture}-r{i}.json")["cells"]
                    if cell["treatment"] == treatment
                )
                for i in range(1, 4)
            ]

        self.assertEqual(sum(int(row["oracleConsistent"]) for row in rows("act", "direct")), 3)
        self.assertEqual(sum(int(row["oracleConsistent"]) for row in rows("act", "late-authority")), 3)
        self.assertEqual(sum(int(row["oracleConsistent"]) for row in rows("hold", "direct")), 0)
        self.assertEqual(sum(int(row["oracleConsistent"]) for row in rows("hold", "late-authority")), 3)
        self.assertEqual(sum(row["effectIntentCount"] for row in rows("hold", "direct")), 3)
        self.assertEqual(sum(row["effectIntentCount"] for row in rows("hold", "late-authority")), 0)

    def test_closeout_matches_retained_evidence(self) -> None:
        closeout = load(EVIDENCE / "p0-live-closeout.json")
        self.assertEqual(closeout["integrity"]["payloadDigest"], digest(closeout))
        self.assertEqual(closeout["experimentImplementationRevision"], IMPLEMENTATION)
        self.assertEqual(closeout["p0A"]["summary"]["S"]["semanticAccepted"], 0)
        self.assertEqual(closeout["p0A"]["summary"]["H"]["semanticAccepted"], 3)
        self.assertEqual(closeout["p0A"]["summary"]["H"]["verifierPassedCandidates"], 4)
        self.assertEqual(closeout["p0B"]["summary"]["hold"]["direct"]["oracleCorrect"], 0)
        self.assertEqual(closeout["p0B"]["summary"]["hold"]["late-authority"]["oracleCorrect"], 3)
        self.assertFalse(closeout["worldModelImpact"]["round002Required"])


if __name__ == "__main__":
    unittest.main()
