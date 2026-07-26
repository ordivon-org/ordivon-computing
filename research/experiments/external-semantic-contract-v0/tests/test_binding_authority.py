from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from anc_canonical import canonical_bytes
from anc_effect_binding import (
    BindingArtifactCorrupt,
    BindingArtifactMissing,
    FileBindingStore,
    SignedEffectBinding,
    binding_digest,
    lower_to_ordivon,
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
    ProtocolAttestationError,
    ProtocolAuthority,
    ResultSemantics,
    SemanticAction,
    SignedEffectEnvelope,
    TargetRef,
    VerificationPlan,
    effect_digest,
)
from anc_tool_contract import normalize_tool_contract
from integration import (
    BindingAuthorityService,
    BoundExecutionView,
    admit_bound_effect,
    project_binding_admission,
)
from anc_semantic_core.ordivon import ordivon_workspace_object_id
from anc_semantic_core.testing import reference_authority_views

ROOT = Path(__file__).resolve().parents[1]


def effect() -> EffectEnvelope:
    action = "anc.execution.launch.v1"
    target = TargetRef("world_object:execution-scope:authority-test")
    return EffectEnvelope(
        effect_id="effect:binding-authority-test",
        target=target,
        mode=EffectMode.CHANGE,
        action=SemanticAction(action, "anc.execution-input.v1"),
        input=CanonicalInput({"executable": "/usr/bin/true", "args": []}),
        capability=CapabilityRequirement(
            "principal:authority-test-agent", action, target.object_id
        ),
        delivery=DeliverySemantics(IdempotencyKind.NATURAL),
        result=ResultSemantics(
            ExecutionKind.ASYNCHRONOUS,
            CompletionKind.TERMINAL_OBSERVATION,
        ),
        verification=VerificationPlan(
            "terminal-job-observation.v1", (EvidenceKind.OBSERVATION,)
        ),
    )


def contract():
    return normalize_tool_contract(
        json.loads(
            (ROOT / "fixtures/contracts/ordivon-workspace-exec-current.json").read_text()
        )
    )


class BindingAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.effect_authority = ProtocolAuthority(
            authority_id="authority:effect-test",
            issuer_id="principal:protocol-issuer",
            principal_id="principal:authority-test-agent",
            role="effect",
            trust_domain="test",
            policy_version="v1",
            key_id="effect-key",
            secret=b"e" * 32,
        )
        self.binding_authority = ProtocolAuthority(
            authority_id="authority:binding-test",
            issuer_id="principal:protocol-issuer",
            principal_id="principal:binding-service",
            role="binding",
            trust_domain="test",
            policy_version="v1",
            key_id="binding-key",
            secret=b"b" * 32,
        )
        self.store = FileBindingStore(Path(self.temporary.name) / "bindings")
        self.service = BindingAuthorityService(
            effect_authority=self.effect_authority,
            binding_authority=self.binding_authority,
            store=self.store,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def signed_effect(self, value: EffectEnvelope | None = None) -> SignedEffectEnvelope:
        value = value or effect()
        return SignedEffectEnvelope(
            value,
            self.effect_authority.attest(
                kind="effect_proposal",
                contract_version="effect-envelope-v1",
                subject_digest=effect_digest(value),
                issued_at_ms=1,
            ),
        )

    def binding(self, value: EffectEnvelope | None = None):
        value = value or effect()
        return lower_to_ordivon(
            value,
            contract(),
            binding_id="binding:authority-test-r1",
            workspace_id="workspace-001",
        )

    def test_complete_binding_is_resolvable_from_kernel_admission(self) -> None:
        value = effect()
        views = reference_authority_views(namespace="binding-authority-resolve")
        _, admission = admit_bound_effect(
            views,
            self.signed_effect(value),
            contract(),
            self.binding(value),
            self.service,
            backend_target=ordivon_workspace_object_id("workspace-001"),
            event_namespace="binding-authority-resolve",
        )
        signed = self.service.resolve(admission)
        self.assertEqual(binding_digest(signed.binding), admission.binding_digest)
        self.assertEqual(signed.binding.effect_digest, admission.effect_digest)
        path = self.store.root / f"{admission.binding_digest[7:]}.json"
        self.assertTrue(path.is_file())

    def test_bound_view_rejects_request_not_present_in_binding(self) -> None:
        value = effect()
        views = reference_authority_views(namespace="binding-request-mismatch")
        projection, admission = admit_bound_effect(
            views,
            self.signed_effect(value),
            contract(),
            self.binding(value),
            self.service,
            backend_target=ordivon_workspace_object_id("workspace-001"),
            event_namespace="binding-request-mismatch",
        )
        complete = self.service.resolve(admission).binding
        bound = BoundExecutionView(views.execution, admission, complete)
        with self.assertRaisesRegex(ValueError, "actual Tool request differs"):
            bound.begin_dispatch(
                projection.effect_id, request_digest="sha256:" + "0" * 64
            )

    def test_forged_effect_attestation_is_rejected(self) -> None:
        signed = self.signed_effect()
        forged = SignedEffectEnvelope(
            signed.envelope,
            replace(signed.attestation, signature="hmac-sha256:" + "0" * 64),
        )
        with self.assertRaisesRegex(ProtocolAttestationError, "signature"):
            self.service.authorize(forged, contract(), self.binding(), issued_at_ms=2)

    def test_binding_with_another_effect_digest_is_rejected(self) -> None:
        changed = replace(self.binding(), effect_digest="sha256:" + "9" * 64)
        with self.assertRaisesRegex(ValueError, "signed Effect content"):
            self.service.authorize(
                self.signed_effect(), contract(), changed, issued_at_ms=2
            )

    def test_missing_binding_artifact_fails_closed(self) -> None:
        artifact = self.service.authorize(
            self.signed_effect(), contract(), self.binding(), issued_at_ms=2
        )
        admission = project_binding_admission(
            artifact.signed_binding.binding, admitted_at_ms=2
        )
        (self.store.root / f"{admission.binding_digest[7:]}.json").unlink()
        with self.assertRaises(BindingArtifactMissing):
            self.service.resolve(admission)

    def test_corrupt_binding_artifact_fails_closed(self) -> None:
        artifact = self.service.authorize(
            self.signed_effect(), contract(), self.binding(), issued_at_ms=2
        )
        admission = project_binding_admission(
            artifact.signed_binding.binding, admitted_at_ms=2
        )
        path = self.store.root / f"{admission.binding_digest[7:]}.json"
        path.write_text("{}")
        with self.assertRaises(BindingArtifactCorrupt):
            self.service.resolve(admission)

    def test_forged_binding_attestation_fails_closed(self) -> None:
        artifact = self.service.authorize(
            self.signed_effect(), contract(), self.binding(), issued_at_ms=2
        )
        admission = project_binding_admission(
            artifact.signed_binding.binding, admitted_at_ms=2
        )
        forged = SignedEffectBinding(
            artifact.signed_binding.binding,
            replace(
                artifact.signed_binding.attestation,
                signature="hmac-sha256:" + "0" * 64,
            ),
        )
        path = self.store.root / f"{admission.binding_digest[7:]}.json"
        path.write_bytes(canonical_bytes(forged.to_dict()))
        with self.assertRaisesRegex(ProtocolAttestationError, "signature"):
            self.service.resolve(admission)


if __name__ == "__main__":
    unittest.main()
