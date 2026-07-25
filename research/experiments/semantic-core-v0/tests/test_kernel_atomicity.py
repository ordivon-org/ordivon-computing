from __future__ import annotations

import unittest

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.kernel import (
    IdentityConflict,
    InvalidTransition,
    InvariantViolation,
    NotFound,
    ReferenceKernel,
)


class KernelAtomicityTests(unittest.TestCase):
    def _dispatched(self, name: str = "atomic"):
        kernel = ReferenceKernel()
        spec = sample_effect(name)
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"{name}:admit"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"{name}:prepare"),
            recorded_at_ms=2,
        )
        dispatch_id = sid(IdKind.DISPATCH, f"{name}:dispatch")
        kernel.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=dispatch_id,
            event_id=sid(IdKind.EVENT, f"{name}:started"),
            recorded_at_ms=3,
            request_digest="sha256:request",
        )
        return kernel, spec, dispatch_id

    def test_admission_event_conflict_rolls_back_every_projection(self) -> None:
        kernel, spec, dispatch_id = self._dispatched("admit-rollback")
        before = kernel.state_snapshot()
        with self.assertRaises(IdentityConflict):
            kernel.admit_dispatch(
                spec.effect_id,
                dispatch_id,
                expected_revision=2,
                event_id=sid(IdKind.EVENT, "admit-rollback:started"),
                recorded_at_ms=4,
                backend_operation_id="job-1",
                evidence_digest="sha256:admitted",
            )
        self.assertEqual(kernel.state_snapshot(), before)
        kernel.validate_invariants()

    def test_unknown_time_regression_rolls_back_dispatch_and_effect(self) -> None:
        kernel, spec, dispatch_id = self._dispatched("unknown-rollback")
        before = kernel.state_snapshot()
        with self.assertRaises((InvariantViolation, ValueError)):
            kernel.mark_dispatch_unknown(
                spec.effect_id,
                dispatch_id,
                expected_revision=2,
                event_id=sid(IdKind.EVENT, "unknown-rollback:unknown"),
                recorded_at_ms=2,
                evidence_digest="sha256:response-loss",
            )
        self.assertEqual(kernel.state_snapshot(), before)
        kernel.validate_invariants()

    def test_rejection_event_conflict_rolls_back_dispatch_and_effect(self) -> None:
        kernel, spec, dispatch_id = self._dispatched("reject-rollback")
        before = kernel.state_snapshot()
        with self.assertRaises(IdentityConflict):
            kernel.reject_dispatch(
                spec.effect_id,
                dispatch_id,
                expected_revision=2,
                event_id=sid(IdKind.EVENT, "reject-rollback:started"),
                recorded_at_ms=4,
                reason_code="BUSY",
                retryable=True,
                evidence_digest="sha256:rejection",
            )
        self.assertEqual(kernel.state_snapshot(), before)
        kernel.validate_invariants()

    def test_outer_transaction_rolls_back_multiple_successful_commands(self) -> None:
        kernel = ReferenceKernel()
        spec = sample_effect("batch-rollback")
        with self.assertRaises(InvalidTransition):
            with kernel.transaction():
                kernel.admit_effect(
                    spec,
                    event_id=sid(IdKind.EVENT, "batch-rollback:admit"),
                    recorded_at_ms=1,
                )
                kernel.prepare_effect(
                    spec.effect_id,
                    expected_revision=0,
                    event_id=sid(IdKind.EVENT, "batch-rollback:prepare"),
                    recorded_at_ms=2,
                )
                kernel.prepare_effect(
                    spec.effect_id,
                    expected_revision=1,
                    event_id=sid(IdKind.EVENT, "batch-rollback:invalid"),
                    recorded_at_ms=3,
                )
        with self.assertRaises(NotFound):
            kernel.get_effect(spec.effect_id)
        kernel.validate_invariants()


if __name__ == "__main__":
    unittest.main()
