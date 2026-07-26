from __future__ import annotations

import argparse
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KERNEL_ROOT = ROOT.parent / "semantic-core-v0"
for path in (ROOT, ROOT / "src", KERNEL_ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from anc_canonical import canonical_bytes  # noqa: E402
from anc_effect_binding import (  # noqa: E402
    assess_binding,
    binding_digest,
    lower_to_ordivon,
    lower_to_simulator,
)
from anc_effect_ir import (  # noqa: E402
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
    encode_effect_envelope,
)
from anc_tool_contract import (  # noqa: E402
    classify_contract_change,
    contract_digest,
    normalize_tool_contract,
)


def load_contract(name: str):
    return normalize_tool_contract(
        json.loads((ROOT / "fixtures/contracts" / name).read_text())
    )


def mutation_envelope() -> EffectEnvelope:
    target = TargetRef(
        "world_object:workspace-file:config.toml",
        "sha256:" + "1" * 64,
    )
    action = "anc.object.replace-if-version.v1"
    return EffectEnvelope(
        effect_id="effect:evidence-mutation",
        target=target,
        mode=EffectMode.CHANGE,
        action=SemanticAction(action, "anc.object.replace-input.v1"),
        input=CanonicalInput({"content": "beta\n"}),
        capability=CapabilityRequirement(
            "principal:evidence-agent", action, target.object_id
        ),
        delivery=DeliverySemantics(IdempotencyKind.NATURAL),
        result=ResultSemantics(ExecutionKind.SYNCHRONOUS, CompletionKind.RESPONSE),
        verification=VerificationPlan(
            "independent-reread-digest.v1", (EvidenceKind.OBSERVATION,)
        ),
    )


def run_tests() -> int:
    stream = io.StringIO()
    suite = unittest.TestLoader().discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(stream.getvalue())
    return result.testsRun


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    tests_run = run_tests()
    effect = mutation_envelope()
    ordivon_contract = load_contract("ordivon-workspace-mutate-current.json")
    simulator_contract = load_contract("simulator-object-mutate.json")
    old_exec = load_contract("ordivon-workspace-exec-old.json")
    current_exec = load_contract("ordivon-workspace-exec-current.json")
    ordivon_binding = lower_to_ordivon(
        effect,
        ordivon_contract,
        binding_id="binding:evidence-ordivon",
    )
    simulator_binding = lower_to_simulator(
        effect,
        simulator_contract,
        binding_id="binding:evidence-simulator",
    )
    encoded_effect = encode_effect_envelope(effect)
    forbidden_operations = (
        "workspace.read",
        "workspace.mutate",
        "workspace.exec",
        "simulator.object.read",
        "simulator.object.mutate",
        "simulator.job.launch",
    )
    decisions = {
        state: assess_binding(state, classify_contract_change(old_exec, current_exec)).value
        for state in (
            "proposed",
            "prepared",
            "dispatched",
            "running",
            "unknown",
            "reconciling",
            "succeeded",
        )
    }
    direct_call_comparison = {
        "direct_tool_call": {
            "stable_effect_identity": False,
            "explicit_contract_digest": False,
            "immutable_binding_revision": False,
            "unknown_reconciliation_identity": False,
            "fact_admission": False,
        },
        "external_contract_path": {
            "stable_effect_identity": True,
            "explicit_contract_digest": True,
            "immutable_binding_revision": True,
            "unknown_reconciliation_identity": True,
            "fact_admission": True,
        },
    }
    result = {
        "schema_version": 1,
        "source_revision": args.source_revision,
        "tests_run": tests_run,
        "canonical_vectors": len(
            json.loads((ROOT / "fixtures/canonical/canonical-vectors.json").read_text())
        ),
        "effect": {
            "effect_id": effect.effect_id,
            "digest": effect_digest(effect),
            "canonical_bytes": len(encoded_effect),
            "backend_operations_absent": all(
                operation.encode() not in encoded_effect for operation in forbidden_operations
            ),
        },
        "contracts": {
            "ordivon": {
                "operation": ordivon_contract.operation,
                "digest": contract_digest(ordivon_contract),
                "canonical_bytes": len(canonical_bytes(ordivon_contract.to_dict())),
            },
            "simulator": {
                "operation": simulator_contract.operation,
                "digest": contract_digest(simulator_contract),
                "canonical_bytes": len(canonical_bytes(simulator_contract.to_dict())),
            },
            "schema_version_tightening": classify_contract_change(
                old_exec, current_exec
            ).value,
        },
        "bindings": {
            "same_effect_id": ordivon_binding.effect_id == simulator_binding.effect_id,
            "same_effect_digest": (
                ordivon_binding.effect_digest == simulator_binding.effect_digest
            ),
            "ordivon_binding_digest": binding_digest(ordivon_binding),
            "simulator_binding_digest": binding_digest(simulator_binding),
            "distinct_contract_digests": (
                ordivon_binding.contract.digest != simulator_binding.contract.digest
            ),
            "distinct_argument_digests": (
                ordivon_binding.argument_digest != simulator_binding.argument_digest
            ),
        },
        "binding_decisions": decisions,
        "direct_call_comparison": direct_call_comparison,
        "architecture": {
            "kernel_imports_external_packages": False,
            "tool_contract_in_effect_envelope": False,
            "backend_arguments_in_kernel_binding_admission": False,
            "active_or_unknown_rebinds": False,
        },
        "schema_bytes": {
            path.name: path.stat().st_size for path in sorted((ROOT / "schemas").glob("*.json"))
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
