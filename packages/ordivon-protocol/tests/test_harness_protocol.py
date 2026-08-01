from __future__ import annotations

import unittest

from anc_canonical import canonical_digest
from ordivon_protocol import (
    HarnessRecoveryConsequence,
    HarnessRunPauseReason,
    HarnessRunSnapshot,
    HarnessToolStepIntent,
    HarnessToolStepReceipt,
    HarnessToolStepStatus,
)


D1 = "sha256:" + "1" * 64
D2 = "sha256:" + "2" * 64
D3 = "sha256:" + "3" * 64
D4 = "sha256:" + "4" * 64
D5 = "sha256:" + "5" * 64


class HarnessProtocolTests(unittest.TestCase):
    def intent(self) -> HarnessToolStepIntent:
        return HarnessToolStepIntent(
            intent_id="harness-tool-step-intent:run-1:turn-1:tool-1",
            harness_run_id="harness-run:run-1",
            assignment_id="assignment:assignment-1",
            assignment_generation=2,
            assignment_digest=D1,
            turn_id="turn:run-1:1",
            tool_call_id="provider-tool-call-1",
            tool_name="run_check",
            tool_call_digest=D2,
            runtime_operation="workspace.exec",
            runtime_arguments_digest=D3,
            client_request_id="harness-run-1-turn-1-tool-1",
            recovery_consequence=HarnessRecoveryConsequence.PROCESS_OR_EXTERNAL_EFFECT_POSSIBLE,
            created_at_ms=10,
        )

    def test_tool_step_intent_round_trips_and_binds_dispatch_identity(self) -> None:
        intent = self.intent()
        self.assertEqual(HarnessToolStepIntent.from_dict(intent.to_dict()), intent)
        self.assertEqual(intent.digest, canonical_digest(intent.to_dict()))
        self.assertEqual(intent.client_request_id, "harness-run-1-turn-1-tool-1")

    def test_tool_step_receipt_round_trips_unknown_without_inventing_failure(self) -> None:
        intent = self.intent()
        receipt = HarnessToolStepReceipt(
            receipt_id="harness-tool-step-receipt:run-1:turn-1:tool-1:r1",
            intent_digest=intent.digest,
            harness_run_id=intent.harness_run_id,
            tool_call_id=intent.tool_call_id,
            status=HarnessToolStepStatus.UNKNOWN,
            runtime_job_ref="job:job-1",
            observation_digest=D4,
            reconciled=False,
            created_at_ms=20,
        )
        self.assertEqual(HarnessToolStepReceipt.from_dict(receipt.to_dict()), receipt)

    def test_snapshot_is_run_local_and_requires_intent_for_pending_effect(self) -> None:
        intent = self.intent()
        snapshot = HarnessRunSnapshot(
            snapshot_id="harness-run-snapshot:run-1:s1",
            harness_run_id=intent.harness_run_id,
            assignment_id=intent.assignment_id,
            assignment_generation=intent.assignment_generation,
            assignment_digest=intent.assignment_digest,
            sequence=1,
            tool_catalog_digest=D5,
            requested_model_id="deepseek-v4-flash",
            effective_model_id="deepseek-v4-flash",
            messages_digest=D2,
            observation_digests=(D4,),
            active_tool_step_intent_digests=(intent.digest,),
            remaining_budget={"modelCalls": 2, "toolCalls": 3, "wallTimeMs": 1000},
            pause_reason=HarnessRunPauseReason.EFFECT_DISPATCH_PENDING,
            created_at_ms=30,
        )
        self.assertEqual(HarnessRunSnapshot.from_dict(snapshot.to_dict()), snapshot)
        self.assertNotIn("taskId", snapshot.to_dict())
        self.assertNotIn("runtimeJobRef", snapshot.to_dict())

    def test_rejected_step_cannot_claim_runtime_job(self) -> None:
        with self.assertRaisesRegex(ValueError, "rejected Tool Step"):
            HarnessToolStepReceipt(
                receipt_id="harness-tool-step-receipt:run-1:turn-1:tool-1:r1",
                intent_digest=D1,
                harness_run_id="harness-run:run-1",
                tool_call_id="provider-tool-call-1",
                status=HarnessToolStepStatus.REJECTED,
                runtime_job_ref="job:job-1",
                observation_digest=D2,
                reconciled=False,
                created_at_ms=1,
            )


if __name__ == "__main__":
    unittest.main()
