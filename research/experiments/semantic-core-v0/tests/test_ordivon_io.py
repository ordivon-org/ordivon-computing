from __future__ import annotations

import hashlib
import unittest
from collections import defaultdict, deque
from dataclasses import replace
from typing import Any

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.kernel import InvariantViolation, ReferenceKernel
from anc_semantic_core.model import (
    CapabilityRef,
    CompletionSemantics,
    DispatchState,
    EffectMode,
    EvidenceKind,
    Fact,
    IdempotencyKind,
    VerificationDecision,
    VerificationPlan,
    WorldObjectRef,
)
from anc_semantic_core.ordivon_io import (
    MutationMode,
    OrdivonIoAdapter,
    OrdivonMutation,
    OrdivonRead,
    ordivon_file_object_id,
)
from anc_semantic_core.state import EffectState
from anc_semantic_core.transport import ToolRejected, ToolTransportError
from anc_semantic_core.verification import verify_digest_fact


class ScriptedClient:
    def __init__(self) -> None:
        self.responses: dict[str, deque[dict[str, Any] | Exception]] = defaultdict(deque)
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def add(self, name: str, response: dict[str, Any] | Exception) -> None:
        self.responses[name].append(response)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((name, arguments))
        if not self.responses[name]:
            raise AssertionError(f"unexpected Tool call: {name}")
        response = self.responses[name].popleft()
        if isinstance(response, Exception):
            raise response
        return response


def sha256_text(content: str) -> str:
    return f"sha256:{hashlib.sha256(content.encode('utf-8')).hexdigest()}"


def prepared_io_effect(
    kernel: ReferenceKernel,
    *,
    name: str,
    workspace_id: str,
    relative_path: str,
    operation: str,
    mode: EffectMode,
    target_version: str | None = None,
):
    base = sample_effect(name)
    target_id = ordivon_file_object_id(workspace_id, relative_path)
    spec = replace(
        base,
        target=WorldObjectRef(target_id, version=target_version),
        mode=mode,
        operation=operation,
        capability=CapabilityRef(base.capability.principal_id, operation, target_id),
        idempotency=IdempotencyKind.NATURAL,
        completion=(
            CompletionSemantics.ACCEPTED
            if mode is EffectMode.CHANGE
            else CompletionSemantics.VERIFIED
        ),
        verification=VerificationPlan(
            method="independent-reread-digest",
            required_evidence=(EvidenceKind.OBSERVATION,),
        ),
    )
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"event:{name}:admit"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"event:{name}:prepare"),
        recorded_at_ms=2,
    )
    return spec


class OrdivonIoTests(unittest.TestCase):
    def test_versioned_read_creates_digest_bound_observation(self) -> None:
        kernel = ReferenceKernel()
        content = "alpha\n"
        digest = sha256_text(content)
        spec = prepared_io_effect(
            kernel,
            name="io-read",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            target_version=digest,
        )
        client = ScriptedClient()
        client.add("workspace.read", {"content": content, "digest": digest})
        adapter = OrdivonIoAdapter(kernel, client, clock_ms=iter(range(10, 100)).__next__)
        result = adapter.dispatch_read(
            spec.effect_id,
            OrdivonRead("workspace-test", "state.txt"),
        )
        self.assertIs(result.state, EffectState.SUCCEEDED)
        self.assertEqual(result.observation.target.version, digest)
        self.assertIs(
            kernel.get_dispatch(result.dispatch_id).state,
            DispatchState.ADMITTED,
        )
        kernel.validate_invariants()

    def test_identical_read_payloads_have_distinct_receipt_identities(self) -> None:
        kernel = ReferenceKernel()
        content = "same\n"
        digest = sha256_text(content)
        client = ScriptedClient()
        client.add("workspace.read", {"content": content, "digest": digest})
        client.add("workspace.read", {"content": content, "digest": digest})
        adapter = OrdivonIoAdapter(
            kernel,
            client,
            clock_ms=iter(range(15, 120)).__next__,
        )
        receipts = []
        for suffix in ("one", "two"):
            spec = prepared_io_effect(
                kernel,
                name=f"io-identical-read-{suffix}",
                workspace_id="workspace-test",
                relative_path="state.txt",
                operation="workspace.read",
                mode=EffectMode.OBSERVE,
            )
            result = adapter.dispatch_read(
                spec.effect_id,
                OrdivonRead("workspace-test", "state.txt"),
            )
            receipts.append(result.receipt_id)
        self.assertNotEqual(receipts[0], receipts[1])
        kernel.validate_invariants()

    def test_versioned_read_detects_world_drift(self) -> None:
        kernel = ReferenceKernel()
        expected = sha256_text("old\n")
        observed = sha256_text("new\n")
        spec = prepared_io_effect(
            kernel,
            name="io-read-drift",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            target_version=expected,
        )
        client = ScriptedClient()
        client.add("workspace.read", {"content": "new\n", "digest": observed})
        result = OrdivonIoAdapter(
            kernel,
            client,
            clock_ms=iter(range(20, 100)).__next__,
        ).dispatch_read(spec.effect_id, OrdivonRead("workspace-test", "state.txt"))
        self.assertIs(result.state, EffectState.FAILED)
        self.assertEqual(result.error_code, "VERSION_MISMATCH")
        self.assertEqual(result.observation.target.version, observed)
        kernel.validate_invariants()

    def test_atomic_mutation_records_after_digest_receipt(self) -> None:
        kernel = ReferenceKernel()
        before = sha256_text("alpha\n")
        after = sha256_text("beta\n")
        spec = prepared_io_effect(
            kernel,
            name="io-mutate",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            target_version=before,
        )
        client = ScriptedClient()
        client.add(
            "workspace.mutate",
            {
                "mutations": [
                    {
                        "relativePath": "state.txt",
                        "afterDigest": after,
                        "byteLength": 5,
                    }
                ]
            },
        )
        result = OrdivonIoAdapter(
            kernel,
            client,
            clock_ms=iter(range(30, 100)).__next__,
        ).dispatch_mutation(
            spec.effect_id,
            OrdivonMutation(
                "workspace-test",
                "state.txt",
                MutationMode.REPLACE_EXACT,
                "beta",
                before,
                expected_text="alpha",
            ),
        )
        self.assertIs(result.state, EffectState.SUCCEEDED)
        self.assertEqual(result.observation.target.version, after)
        self.assertTrue(result.receipt_id.startswith("ordivon-receipt:workspace.mutate:"))
        kernel.validate_invariants()

    def test_stale_mutation_precondition_is_proven_rejection(self) -> None:
        kernel = ReferenceKernel()
        before = sha256_text("alpha\n")
        spec = prepared_io_effect(
            kernel,
            name="io-stale-mutation",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            target_version=before,
        )
        client = ScriptedClient()
        client.add(
            "workspace.mutate",
            ToolRejected(
                "workspace.mutate",
                code="INVALID_REQUEST",
                message="workspace file does not match expectedDigest",
                field="mutations[0].expectedDigest",
                retryable=False,
            ),
        )
        result = OrdivonIoAdapter(
            kernel,
            client,
            clock_ms=iter(range(40, 100)).__next__,
        ).dispatch_mutation(
            spec.effect_id,
            OrdivonMutation(
                "workspace-test",
                "state.txt",
                MutationMode.WRITE,
                "beta\n",
                before,
            ),
        )
        self.assertIs(result.state, EffectState.FAILED)
        self.assertEqual(result.error_code, "INVALID_REQUEST")
        self.assertIs(kernel.get_dispatch(result.dispatch_id).state, DispatchState.REJECTED)
        kernel.validate_invariants()

    def test_mutation_transport_loss_remains_unknown(self) -> None:
        kernel = ReferenceKernel()
        before = sha256_text("alpha\n")
        spec = prepared_io_effect(
            kernel,
            name="io-mutation-unknown",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            target_version=before,
        )
        client = ScriptedClient()
        client.add("workspace.mutate", ToolTransportError("response lost"))
        result = OrdivonIoAdapter(
            kernel,
            client,
            clock_ms=iter(range(50, 100)).__next__,
        ).dispatch_mutation(
            spec.effect_id,
            OrdivonMutation(
                "workspace-test",
                "state.txt",
                MutationMode.WRITE,
                "beta\n",
                before,
            ),
        )
        self.assertIs(result.state, EffectState.UNKNOWN)
        self.assertIs(kernel.get_dispatch(result.dispatch_id).state, DispatchState.UNKNOWN)
        kernel.validate_invariants()

    def test_independent_reread_admits_digest_fact(self) -> None:
        kernel = ReferenceKernel()
        before = sha256_text("alpha\n")
        after_content = "beta\n"
        after = sha256_text(after_content)
        mutation = prepared_io_effect(
            kernel,
            name="io-fact-mutation",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            target_version=before,
        )
        mutation_client = ScriptedClient()
        mutation_client.add(
            "workspace.mutate",
            {
                "mutations": [
                    {
                        "relativePath": "state.txt",
                        "afterDigest": after,
                        "byteLength": len(after_content.encode("utf-8")),
                    }
                ]
            },
        )
        OrdivonIoAdapter(
            kernel,
            mutation_client,
            clock_ms=iter(range(60, 100)).__next__,
        ).dispatch_mutation(
            mutation.effect_id,
            OrdivonMutation(
                "workspace-test",
                "state.txt",
                MutationMode.WRITE,
                after_content,
                before,
            ),
        )

        read = prepared_io_effect(
            kernel,
            name="io-fact-reread",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            target_version=after,
        )
        read_client = ScriptedClient()
        read_client.add("workspace.read", {"content": after_content, "digest": after})
        read_result = OrdivonIoAdapter(
            kernel,
            read_client,
            clock_ms=iter(range(100, 160)).__next__,
        ).dispatch_read(read.effect_id, OrdivonRead("workspace-test", "state.txt"))

        result = verify_digest_fact(
            kernel,
            claim_effect_id=mutation.effect_id,
            observation=read_result.observation,
            expected_digest=after,
            verified_at_ms=200,
            accepted_at_ms=201,
        )
        self.assertIs(result.verification.decision, VerificationDecision.ACCEPTED)
        self.assertIsNotNone(result.fact)
        self.assertNotEqual(read.effect_id, mutation.effect_id)
        with self.assertRaises(InvariantViolation):
            kernel.commit_fact(
                Fact(
                    fact_id=sid(IdKind.FACT, "fact:predates-verification"),
                    claim_id=result.claim.claim_id,
                    verification_id=result.verification.verification_id,
                    accepted_at_ms=result.verification.verified_at_ms - 1,
                )
            )
        kernel.validate_invariants()

    def test_mismatched_reread_rejects_digest_fact(self) -> None:
        kernel = ReferenceKernel()
        before = sha256_text("alpha\n")
        claimed = sha256_text("beta\n")
        observed_content = "gamma\n"
        observed = sha256_text(observed_content)
        mutation = prepared_io_effect(
            kernel,
            name="io-fact-mismatch-origin",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            target_version=before,
        )
        mutation_client = ScriptedClient()
        mutation_client.add(
            "workspace.mutate",
            {
                "mutations": [
                    {
                        "relativePath": "state.txt",
                        "afterDigest": claimed,
                        "byteLength": 5,
                    }
                ]
            },
        )
        OrdivonIoAdapter(
            kernel,
            mutation_client,
            clock_ms=iter(range(160, 200)).__next__,
        ).dispatch_mutation(
            mutation.effect_id,
            OrdivonMutation(
                "workspace-test",
                "state.txt",
                MutationMode.WRITE,
                "beta\n",
                before,
            ),
        )
        read = prepared_io_effect(
            kernel,
            name="io-fact-mismatch-read",
            workspace_id="workspace-test",
            relative_path="state.txt",
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
        )
        read_client = ScriptedClient()
        read_client.add(
            "workspace.read",
            {"content": observed_content, "digest": observed},
        )
        read_result = OrdivonIoAdapter(
            kernel,
            read_client,
            clock_ms=iter(range(200, 260)).__next__,
        ).dispatch_read(read.effect_id, OrdivonRead("workspace-test", "state.txt"))
        result = verify_digest_fact(
            kernel,
            claim_effect_id=mutation.effect_id,
            observation=read_result.observation,
            expected_digest=claimed,
            verified_at_ms=300,
        )
        self.assertIs(result.verification.decision, VerificationDecision.REJECTED)
        self.assertIsNone(result.fact)
        kernel.validate_invariants()


if __name__ == "__main__":
    unittest.main()
