from __future__ import annotations

import unittest

from anc_canonical import canonical_digest
from ordivon_protocol import (
    HarnessDispatchFence,
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

    def test_tool_step_receipt_round_trips_unknown_without_inventing_failure(
        self,
    ) -> None:
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
            previous_receipt_digest=None,
        )
        self.assertTrue(receipt.terminal)
        self.assertEqual(HarnessToolStepReceipt.from_dict(receipt.to_dict()), receipt)

    def test_legacy_receipt_without_predecessor_field_still_decodes(self) -> None:
        receipt = HarnessToolStepReceipt(
            receipt_id="harness-tool-step-receipt:run-1:legacy",
            intent_digest=D1,
            harness_run_id="harness-run:run-1",
            tool_call_id="legacy-call",
            status=HarnessToolStepStatus.UNKNOWN,
            runtime_job_ref=None,
            observation_digest=D2,
            reconciled=False,
            created_at_ms=1,
        )
        legacy = receipt.to_dict()
        legacy.pop("previousReceiptDigest")
        self.assertIsNone(
            HarnessToolStepReceipt.from_dict(legacy).previous_receipt_digest
        )

    def test_cancel_requested_receipt_is_non_terminal_and_can_be_superseded(
        self,
    ) -> None:
        intent = self.intent()
        requested = HarnessToolStepReceipt(
            receipt_id="harness-tool-step-receipt:run-1:turn-1:tool-1:r1",
            intent_digest=intent.digest,
            harness_run_id=intent.harness_run_id,
            tool_call_id=intent.tool_call_id,
            status=HarnessToolStepStatus.CANCEL_REQUESTED,
            runtime_job_ref="job:job-1",
            observation_digest=D4,
            reconciled=False,
            created_at_ms=20,
        )
        final = HarnessToolStepReceipt(
            receipt_id="harness-tool-step-receipt:run-1:turn-1:tool-1:r2",
            intent_digest=intent.digest,
            harness_run_id=intent.harness_run_id,
            tool_call_id=intent.tool_call_id,
            status=HarnessToolStepStatus.CANCELLED,
            runtime_job_ref="job:job-1",
            observation_digest=D5,
            reconciled=True,
            created_at_ms=21,
            previous_receipt_digest=requested.digest,
        )
        self.assertFalse(requested.terminal)
        self.assertTrue(final.terminal)
        self.assertEqual(HarnessToolStepReceipt.from_dict(final.to_dict()), final)

    def test_dispatch_fence_round_trips_and_binds_post_intent_revision(self) -> None:
        intent = self.intent()
        fence = HarnessDispatchFence(
            fence_id="harness-dispatch-fence:run-1:tool-1",
            task_id="task:task-1",
            task_revision=7,
            harness_run_id=intent.harness_run_id,
            assignment_id=intent.assignment_id,
            assignment_generation=intent.assignment_generation,
            assignment_digest=intent.assignment_digest,
            intent_digest=intent.digest,
            runtime_operation=intent.runtime_operation,
            client_request_id=intent.client_request_id,
            issued_at_ms=30,
            expires_at_ms=5_030,
        )
        self.assertEqual(HarnessDispatchFence.from_dict(fence.to_dict()), fence)

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
