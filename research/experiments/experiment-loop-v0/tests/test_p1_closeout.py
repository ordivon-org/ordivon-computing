from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cel import canonical_digest


def generic_digest(value: dict) -> str:
    payload = dict(value)
    payload.pop("integrity", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


class P1CloseoutTests(unittest.TestCase):
    def test_plan_v5_closes_bounded_recursive_evidence_with_both_rollbacks(self) -> None:
        plan = json.loads((ROOT / "plan-v5.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["integrity"]["payloadDigest"], canonical_digest(plan))
        self.assertEqual(
            plan["status"],
            "p1_closed_bounded_recursive_self_improvement_evidence",
        )
        evidence = plan["boundedRSIEvidence"]
        self.assertTrue(evidence["firstGeneration"]["heldOutPassed"])
        self.assertTrue(evidence["firstGeneration"]["rollbackRehearsed"])
        self.assertTrue(evidence["secondGeneration"]["drivenByImprovedLoop"])
        self.assertTrue(evidence["secondGeneration"]["heldOutPassed"])
        self.assertTrue(evidence["secondGeneration"]["rollbackRehearsed"])
        self.assertIn("not_open_ended_RSI", evidence["claimLimit"])
        self.assertEqual(
            plan["returnEdgeDriverDecision"]["disposition"],
            "reject_new_generic_driver_for_now",
        )

    def test_closeout_rejects_open_ended_rsi_claim(self) -> None:
        closeout = json.loads(
            (ROOT / "p1-bounded-rsi-closeout.json").read_text(encoding="utf-8")
        )
        self.assertEqual(closeout["integrity"]["payloadDigest"], generic_digest(closeout))
        claims = closeout["claims"]
        self.assertTrue(claims["boundedSelfChangeProven"])
        self.assertTrue(claims["heldOutEvaluationProven"])
        self.assertTrue(claims["rollbackProven"])
        self.assertTrue(claims["secondGenerationChangeDrivenByImprovedLoop"])
        self.assertFalse(claims["openEndedRSIProven"])
        self.assertFalse(claims["worldModelRound002Required"])

    def test_both_rollback_receipts_are_integrity_valid_and_owner_safe(self) -> None:
        receipts = (
            ROOT / "campaigns/cel-p1-selection-001/rollback-receipt.json",
            ROOT / "campaigns/cel-p1-prerequisite-002/rollback-receipt.json",
        )
        for path in receipts:
            receipt = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["integrity"]["payloadDigest"], generic_digest(receipt))
            self.assertTrue(receipt["rollbackDiffCheckPassed"])
            self.assertTrue(receipt["candidateWorkspaceRemoved"])
            self.assertFalse(receipt["ownerStateChanged"])


if __name__ == "__main__":
    unittest.main()
