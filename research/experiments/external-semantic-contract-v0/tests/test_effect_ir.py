from __future__ import annotations

import unittest
from dataclasses import replace

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
    ProtocolAttestation,
    ResultSemantics,
    SemanticAction,
    SignedEffectEnvelope,
    TargetRef,
    VerificationPlan,
    decode_effect_envelope,
    effect_digest,
    encode_effect_envelope,
)

DIGEST = "sha256:" + "1" * 64


def sample_effect(*, action: str = "anc.object.read.v1") -> EffectEnvelope:
    mode = EffectMode.OBSERVE if action == "anc.object.read.v1" else EffectMode.CHANGE
    result = (
        ResultSemantics(ExecutionKind.ASYNCHRONOUS, CompletionKind.TERMINAL_OBSERVATION)
        if action == "anc.execution.launch.v1"
        else ResultSemantics(ExecutionKind.SYNCHRONOUS, CompletionKind.RESPONSE)
    )
    value = (
        {"executable": "/usr/bin/true", "args": []}
        if action == "anc.execution.launch.v1"
        else ({"content": "beta\n"} if action.endswith("replace-if-version.v1") else {})
    )
    target = TargetRef("world_object:workspace-file:config.toml", DIGEST if "replace" in action else None)
    return EffectEnvelope(
        effect_id="effect:public-ir-001",
        target=target,
        mode=mode,
        action=SemanticAction(action, "anc.input.v1"),
        input=CanonicalInput(value),
        capability=CapabilityRequirement(
            "principal:agent-001", action, target.object_id
        ),
        delivery=DeliverySemantics(IdempotencyKind.NATURAL),
        result=result,
        verification=VerificationPlan(
            "independent-reread-digest.v1", (EvidenceKind.OBSERVATION,)
        ),
    )


class EffectIrTests(unittest.TestCase):
    def test_round_trip_and_stable_digest(self) -> None:
        effect = sample_effect()
        encoded = encode_effect_envelope(effect)
        self.assertEqual(decode_effect_envelope(encoded), effect)
        self.assertEqual(effect_digest(decode_effect_envelope(encoded)), effect_digest(effect))

    def test_backend_operation_names_are_absent(self) -> None:
        encoded = encode_effect_envelope(sample_effect(action="anc.execution.launch.v1")).decode()
        for forbidden in ("workspace.exec", "simulator.job.launch", "task.observe", "jobId"):
            self.assertNotIn(forbidden, encoded)

    def test_same_identity_different_content_changes_digest(self) -> None:
        effect = sample_effect(action="anc.object.replace-if-version.v1")
        changed = replace(effect, input=CanonicalInput({"content": "gamma\n"}))
        self.assertEqual(effect.effect_id, changed.effect_id)
        self.assertNotEqual(effect_digest(effect), effect_digest(changed))

    def test_unknown_field_is_rejected(self) -> None:
        value = sample_effect().to_dict()
        value["provider"] = "ordivon"
        import json

        with self.assertRaisesRegex(ValueError, "fields differ"):
            decode_effect_envelope(json.dumps(value))

    def test_attestation_binds_effect_digest(self) -> None:
        effect = sample_effect()
        attestation = ProtocolAttestation(
            authority_id="authority:test-effect",
            issuer_id="principal:issuer",
            principal_id="principal:agent-001",
            role="effect",
            trust_domain="test",
            policy_version="v1",
            key_id="k1",
            authority_signature="hmac-sha256:" + "a" * 64,
            kind="effect_proposal",
            contract_version="effect-envelope-v1",
            subject_digest=effect_digest(effect),
            issued_at_ms=1,
            signature="hmac-sha256:" + "b" * 64,
        )
        self.assertEqual(SignedEffectEnvelope(effect, attestation).envelope, effect)
        with self.assertRaisesRegex(ValueError, "does not bind"):
            SignedEffectEnvelope(
                effect,
                replace(attestation, subject_digest="sha256:" + "2" * 64),
            )


if __name__ == "__main__":
    unittest.main()
