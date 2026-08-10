from __future__ import annotations
import json, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class P2CloseoutTests(unittest.TestCase):
    def test_plan_v7_records_cross_evidence_transfer_and_rollback(self):
        p=json.loads((ROOT/"plan-v7.json").read_text())
        self.assertEqual(p["planId"],"CEL-R4-007")
        g=p["boundedRSIEvidence"]["thirdGeneration"]
        self.assertTrue(g["materiallyDifferentEvidenceFamily"])
        self.assertTrue(g["heldOutPassed"])
        self.assertTrue(g["rollbackRehearsed"])
        self.assertFalse(p["distributionAuthority"]["forcePushAllowed"])
    def test_p2_closeout_rejects_open_ended_rsi_and_auto_assimilation(self):
        p=json.loads((ROOT/"p2-bounded-rsi-closeout.json").read_text())
        self.assertTrue(p["claims"]["materiallyDifferentEvidenceFamilyTransferProven"])
        self.assertFalse(p["claims"]["ownerRevisionMovementAutoRevisesWorldModel"])
        self.assertFalse(p["claims"]["openEndedRSIProven"])
        self.assertFalse(p["claims"]["worldModelRound002Required"])
    def test_third_generation_rollback_receipt_is_owner_safe(self):
        p=json.loads((ROOT/"campaigns/cel-p2-frontier-freshness-003/rollback-receipt.json").read_text())
        self.assertEqual(p["priorStateTestsPassed"],26)
        self.assertTrue(p["worldModelCheckerPassed"])
        self.assertFalse(p["ownerStateChanged"])
if __name__ == "__main__": unittest.main()
