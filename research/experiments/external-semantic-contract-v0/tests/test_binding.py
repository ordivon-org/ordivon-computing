from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path

from anc_effect_binding import (
    BindingDecision,
    assess_binding,
    binding_digest,
    lower_to_ordivon,
    lower_to_simulator,
)
from anc_effect_ir import (
    CanonicalInput,
    CapabilityRequirement,
    CompletionKind,
    DeliverySemantics,
    EffectEnvelope,
    EffectMode,
    EvidenceKind,
    ExecutionKind,
    IdempotencyKind,
    ResultSemantics,
    SemanticAction,
    TargetRef,
    VerificationPlan,
    effect_digest,
)
from anc_tool_contract import ContractChange, normalize_tool_contract

ROOT = Path(__file__).resolve().parents[1]
DIGEST = "sha256:" + "1" * 64


def effect(action: str) -> EffectEnvelope:
    mode = EffectMode.OBSERVE if action == "anc.object.read.v1" else EffectMode.CHANGE
    value = {}
    result = ResultSemantics(ExecutionKind.SYNCHRONOUS, CompletionKind.RESPONSE)
    version = None
    if "replace" in action:
        value = {"content": "beta\n"}
        version = DIGEST
    if action == "anc.execution.launch.v1":
        value = {"executable": "/usr/bin/true", "args": []}
        result = ResultSemantics(
            ExecutionKind.ASYNCHRONOUS, CompletionKind.TERMINAL_OBSERVATION
        )
    target = TargetRef("world_object:workspace-file:config.toml", version)
    return EffectEnvelope(
        "effect:binding-001",
        target,
        mode,
        SemanticAction(action, "anc.input.v1"),
        CanonicalInput(value),
        CapabilityRequirement("principal:agent", action, target.object_id),
        DeliverySemantics(IdempotencyKind.NATURAL),
        result,
        VerificationPlan("independent-reread-digest.v1", (EvidenceKind.OBSERVATION,)),
    )


def contract(name: str):
    return normalize_tool_contract(
        json.loads((ROOT / "fixtures/contracts" / name).read_text())
    )


class BindingTests(unittest.TestCase):
    def test_same_effect_binds_two_distinct_backends(self) -> None:
        envelope = effect("anc.object.replace-if-version.v1")
        ordivon = lower_to_ordivon(
            envelope,
            contract("ordivon-workspace-mutate-current.json"),
            binding_id="binding:ordivon-r1",
        )
        simulator = lower_to_simulator(
            envelope,
            contract("simulator-object-mutate.json"),
            binding_id="binding:simulator-r1",
        )
        self.assertEqual(ordivon.effect_id, simulator.effect_id)
        self.assertEqual(ordivon.effect_digest, simulator.effect_digest)
        self.assertEqual(ordivon.effect_digest, effect_digest(envelope))
        self.assertNotEqual(ordivon.contract.digest, simulator.contract.digest)
        self.assertNotEqual(ordivon.argument_digest, simulator.argument_digest)
        self.assertNotEqual(binding_digest(ordivon), binding_digest(simulator))

    def test_rebind_keeps_effect_and_supersedes_binding(self) -> None:
        envelope = effect("anc.execution.launch.v1")
        old = lower_to_ordivon(
            envelope,
            contract("ordivon-workspace-exec-old.json"),
            binding_id="binding:exec-r1",
        )
        new = lower_to_ordivon(
            envelope,
            contract("ordivon-workspace-exec-current.json"),
            binding_id="binding:exec-r2",
            revision=2,
            supersedes=old.binding_id,
        )
        self.assertEqual(old.effect_id, new.effect_id)
        self.assertEqual(old.effect_digest, new.effect_digest)
        self.assertEqual(new.supersedes_binding_id, old.binding_id)
        self.assertNotEqual(binding_digest(old), binding_digest(new))

    def test_binding_decisions_respect_active_dispatch(self) -> None:
        self.assertIs(
            assess_binding("prepared", ContractChange.CALLER_ADAPTATION),
            BindingDecision.REBIND,
        )
        for state in ("dispatched", "running", "unknown", "reconciling"):
            with self.subTest(state=state):
                self.assertIs(
                    assess_binding(state, ContractChange.CALLER_ADAPTATION),
                    BindingDecision.OBSERVE_ORIGINAL,
                )
        self.assertIs(
            assess_binding("succeeded", ContractChange.CALLER_ADAPTATION),
            BindingDecision.KEEP,
        )
        self.assertIs(
            assess_binding("prepared", ContractChange.SEMANTIC_BREAK),
            BindingDecision.NEW_EFFECT,
        )

    def test_argument_change_changes_binding_digest(self) -> None:
        envelope = effect("anc.object.read.v1")
        binding = lower_to_ordivon(
            envelope,
            contract("ordivon-workspace-read-current.json"),
            binding_id="binding:read-r1",
        )
        changed = replace(binding, arguments={**binding.arguments, "relativePath": "other"}, argument_digest=None)
        self.assertNotEqual(binding_digest(binding), binding_digest(changed))


if __name__ == "__main__":
    unittest.main()
