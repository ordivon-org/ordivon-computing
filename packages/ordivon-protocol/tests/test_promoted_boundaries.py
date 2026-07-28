from __future__ import annotations

import ast
import unittest
from pathlib import Path

from anc_canonical import (
    canonical_digest,
    digest_bytes,
    digest_text,
    validate_digest,
)
from anc_effect_binding import BindingDecision, assess_binding
from anc_effect_ir import (
    CompletionKind as EffectCompletionKind,
    EffectMode,
    ExecutionKind as EffectExecutionKind,
)
from anc_tool_contract import (
    CompletionKind as ContractCompletionKind,
    ContractChange,
    ExecutionKind as ContractExecutionKind,
)
from ordivon_protocol import SCHEMA_FILES, VECTOR_FILES, schema_text, vector_text
from ordivon_semantics import DispatchState, EffectState, IdKind, SemanticId, next_action


class PromotedBoundaryTests(unittest.TestCase):
    def test_promoted_modules_import_without_experiment_paths(self) -> None:
        self.assertEqual(canonical_digest({"ok": True})[:7], "sha256:")
        self.assertEqual(EffectMode.OBSERVE.value, "observe")
        self.assertEqual(
            assess_binding("unknown", ContractChange.IDENTICAL),
            BindingDecision.OBSERVE_ORIGINAL,
        )

    def test_shared_execution_semantics_have_one_runtime_type(self) -> None:
        self.assertIs(EffectExecutionKind, ContractExecutionKind)
        self.assertIs(EffectCompletionKind, ContractCompletionKind)

    def test_canonical_digest_helpers_share_one_format_validator(self) -> None:
        digest = digest_text("ordivon")
        self.assertEqual(digest, digest_bytes(b"ordivon"))
        self.assertEqual(validate_digest(digest), digest)
        with self.assertRaises(ValueError):
            validate_digest("sha256:ABC")

    def test_normative_resources_ship_with_the_distribution(self) -> None:
        self.assertEqual(len(SCHEMA_FILES), 3)
        self.assertEqual(len(VECTOR_FILES), 2)
        self.assertIn("anc.effect-envelope.v1", schema_text(SCHEMA_FILES[1]))
        self.assertIn("sha256:", vector_text("canonical-vectors.tsv"))

    def test_unknown_requires_reconciliation(self) -> None:
        self.assertTrue(EffectState.UNKNOWN.requires_reconciliation)
        self.assertEqual(next_action(EffectState.UNKNOWN).value, "reconcile")
        self.assertEqual(DispatchState.UNKNOWN.value, "unknown")

    def test_semantic_identity_is_typed(self) -> None:
        value = SemanticId(IdKind.EFFECT, "effect-001")
        self.assertEqual(str(value), "effect:effect-001")

    def test_dependency_direction_remains_acyclic(self) -> None:
        root = Path(__file__).resolve().parents[1] / "src"
        allowed = {
            "anc_canonical": set(),
            "anc_protocol_types": set(),
            "anc_effect_ir": {"anc_canonical", "anc_protocol_types"},
            "anc_tool_contract": {"anc_canonical", "anc_protocol_types"},
            "anc_effect_binding": {
                "anc_canonical",
                "anc_effect_ir",
                "anc_tool_contract",
            },
            "ordivon_semantics": set(),
        }
        for package, permitted in allowed.items():
            imported: set[str] = set()
            for path in (root / package).glob("*.py"):
                tree = ast.parse(path.read_text())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imported.update(alias.name.split(".")[0] for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imported.add(node.module.split(".")[0])
            project_imports = {
                name
                for name in imported
                if name.startswith("anc_") or name == "ordivon_semantics"
            }
            self.assertTrue(project_imports.issubset(permitted), (package, project_imports))


class SourceChangeProtocolTests(unittest.TestCase):
    def test_source_change_effect_is_semantic_and_repository_bound(self) -> None:
        from anc_effect_ir import (
            SourceChangeSpec,
            SourceFileChange,
            source_change_effect,
        )

        content = "VALUE = 2\n"
        spec = SourceChangeSpec(
            repository_id="repository:ordivon-host",
            base_revision="a" * 40,
            files=(
                SourceFileChange(
                    "src/example.py",
                    "sha256:" + "1" * 64,
                    digest_text(content),
                    content,
                ),
            ),
            verification_ids=("ruff", "tests"),
        )
        effect = source_change_effect(
            effect_id="effect:source-change-test",
            principal_id="principal:local-owner",
            spec=spec,
        )
        self.assertEqual(effect.action.action_id, "anc.source.change.v1")
        self.assertEqual(effect.target.object_id, "world_object:repository:ordivon-host")
        self.assertEqual(effect.result.completion.value, "accepted-verification")
        self.assertNotIn("sourceRepo", effect.input.value)

    def test_source_change_rejects_content_digest_mismatch(self) -> None:
        from anc_effect_ir import SourceFileChange

        with self.assertRaisesRegex(ValueError, "does not match content"):
            SourceFileChange(
                "src/example.py",
                "sha256:" + "1" * 64,
                "sha256:" + "2" * 64,
                "VALUE = 2\n",
            )


if __name__ == "__main__":
    unittest.main()
