from __future__ import annotations

import tempfile
import unittest
from dataclasses import fields
from pathlib import Path
from typing import get_type_hints

from anc_semantic_core.authority import AuthorityRole
from anc_semantic_core.conformance import (
    _successful_verified_effect,
    sample_effect,
    sid,
)
from anc_semantic_core.identity import IdKind
from anc_semantic_core.interfaces import (
    ExecutionView,
    FactView,
    VerificationView,
)
from anc_semantic_core.journal import JournalReducer
from anc_semantic_core.kernel import ReferenceReducer
from anc_semantic_core.model import KernelEffectProjection
from anc_semantic_core.ordivon import OrdivonSemanticAdapter
from anc_semantic_core.ordivon_io import OrdivonIoAdapter
from anc_semantic_core.provenance import (
    execution_authority_trace,
    execution_trace,
    fact_authority_trace,
    fact_provenance,
    recovery_view,
)
from anc_semantic_core.state import (
    DispatchState,
    EffectState,
    NextAction,
    can_transition_dispatch,
)
from anc_semantic_core.testing import reference_kernel, test_authority_policy
from anc_semantic_core.verification import verify_digest_fact


class P1BoundaryTests(unittest.TestCase):
    def test_adapters_and_verification_use_exact_role_protocols(self) -> None:
        semantic_hints = get_type_hints(OrdivonSemanticAdapter.__init__)
        io_hints = get_type_hints(OrdivonIoAdapter.__init__)
        verification_hints = get_type_hints(verify_digest_fact)
        self.assertIs(semantic_hints["kernel"], ExecutionView)
        self.assertIs(io_hints["kernel"], ExecutionView)
        self.assertIs(verification_hints["verification_kernel"], VerificationView)
        self.assertIs(verification_hints["fact_kernel"], FactView)

    def test_kernel_projection_does_not_store_provider_operation(self) -> None:
        import anc_semantic_core

        projection = sample_effect("projection-boundary")
        self.assertIsInstance(projection, KernelEffectProjection)
        self.assertNotIn("operation", {field.name for field in fields(projection)})
        self.assertFalse(hasattr(projection, "operation"))
        self.assertFalse(hasattr(anc_semantic_core, "EffectSpec"))
        self.assertTrue(
            projection.capability.operation.startswith("workspace.")
        )  # legacy sample remains decodable through the internal projection

    def test_raw_reducer_source_aliases_are_removed(self) -> None:
        import anc_semantic_core.journal as journal_module
        import anc_semantic_core.kernel as kernel_module

        self.assertFalse(hasattr(kernel_module, "ReferenceKernel"))
        self.assertFalse(hasattr(journal_module, "JournalKernel"))
        policy = test_authority_policy()
        reference = ReferenceReducer(policy)
        self.assertEqual(reference.journal_entry_count, 0)
        with tempfile.TemporaryDirectory() as directory:
            durable = JournalReducer(Path(directory) / "p1.sqlite3", policy)
            self.assertEqual(durable.journal_entry_count, 0)
            durable.close()

    def test_dispatch_transition_graph_is_explicit(self) -> None:
        allowed = {
            (DispatchState.STARTED, DispatchState.ADMITTED),
            (DispatchState.STARTED, DispatchState.UNKNOWN),
            (DispatchState.STARTED, DispatchState.REJECTED),
            (DispatchState.ADMITTED, DispatchState.UNKNOWN),
            (DispatchState.UNKNOWN, DispatchState.ADMITTED),
            (DispatchState.UNKNOWN, DispatchState.REJECTED),
        }
        for current in DispatchState:
            for target in DispatchState:
                self.assertEqual(
                    can_transition_dispatch(current, target),
                    (current, target) in allowed,
                    f"unexpected Dispatch transition {current.value} -> {target.value}",
                )

    def test_execution_trace_is_a_read_only_projection(self) -> None:
        kernel = reference_kernel(namespace="p1-execution-trace")
        _successful_verified_effect(kernel)
        effect_id = sid(IdKind.EFFECT, "effect:success")
        trace = execution_trace(kernel, effect_id)
        self.assertIs(trace.effect.state, EffectState.SUCCEEDED)
        self.assertIsNotNone(trace.dispatch)
        self.assertEqual(len(trace.events), 5)
        self.assertEqual(len(trace.observations), 1)
        self.assertEqual(len(trace.artifacts), 1)
        self.assertIs(trace.next_action, NextAction.NONE)
        self.assertEqual(kernel.get_effect(effect_id), trace.effect)

    def test_recovery_view_preserves_unknown_dispatch_identity(self) -> None:
        kernel = reference_kernel(namespace="p1-recovery")
        spec = sample_effect("p1-recovery")
        dispatch_id = sid(IdKind.DISPATCH, "dispatch:p1-recovery")
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "event:p1-recovery:0"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:p1-recovery:1"),
            recorded_at_ms=2,
        )
        kernel.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=dispatch_id,
            event_id=sid(IdKind.EVENT, "event:p1-recovery:2"),
            recorded_at_ms=3,
            request_digest="sha256:p1-recovery-request",
        )
        kernel.mark_dispatch_unknown(
            spec.effect_id,
            dispatch_id,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:p1-recovery:3"),
            recorded_at_ms=4,
            evidence_digest="sha256:p1-response-lost",
        )
        view = recovery_view(kernel, spec.effect_id)
        self.assertIs(view.effect_state, EffectState.UNKNOWN)
        self.assertEqual(view.dispatch_id, dispatch_id)
        self.assertIs(view.dispatch_state, DispatchState.UNKNOWN)
        self.assertIs(view.next_action, NextAction.RECONCILE)
        self.assertEqual(view.latest_evidence_digest, "sha256:p1-response-lost")

    def test_fact_provenance_reconstructs_evidence_chain(self) -> None:
        kernel = reference_kernel(namespace="p1-fact-provenance")
        _successful_verified_effect(kernel)
        fact_id = sid(IdKind.FACT, "fact:success")
        view = fact_provenance(kernel, fact_id)
        self.assertEqual(view.fact.fact_id, fact_id)
        self.assertEqual(view.verification.verification_id, view.fact.verification_id)
        self.assertEqual(view.claim.claim_id, view.fact.claim_id)
        self.assertEqual(view.origin_effect.spec.effect_id, view.claim.origin_effect_id)
        self.assertEqual(len(view.evidence), 2)
        self.assertTrue(
            all(
                item.producing_dispatch.effect_id
                == item.producing_effect.spec.effect_id
                for item in view.evidence
            )
        )

    def test_authority_trace_projects_roles_without_new_state(self) -> None:
        kernel = reference_kernel(namespace="p1-authority-trace")
        _successful_verified_effect(kernel)
        effect_id = sid(IdKind.EFFECT, "effect:success")
        fact_id = sid(IdKind.FACT, "fact:success")
        execution_roles = {
            entry.authority.role for entry in execution_authority_trace(kernel, effect_id).entries
        }
        fact_roles = {
            entry.authority.role for entry in fact_authority_trace(kernel, fact_id).entries
        }
        self.assertEqual(
            execution_roles,
            {AuthorityRole.EFFECT, AuthorityRole.DISPATCH, AuthorityRole.OBSERVATION},
        )
        self.assertEqual(
            fact_roles,
            {
                AuthorityRole.EFFECT,
                AuthorityRole.DISPATCH,
                AuthorityRole.OBSERVATION,
                AuthorityRole.VERIFICATION,
                AuthorityRole.FACT,
            },
        )
        kernel.validate_invariants()


if __name__ == "__main__":
    unittest.main()
