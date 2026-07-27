from __future__ import annotations

import ast
import unittest
from pathlib import Path

from anc_canonical import canonical_digest
from anc_effect_binding import BindingDecision, assess_binding
from anc_effect_ir import EffectMode
from anc_tool_contract import ContractChange
from ordivon_semantics import DispatchState, EffectState, IdKind, SemanticId, next_action


class PromotedBoundaryTests(unittest.TestCase):
    def test_promoted_modules_import_without_experiment_paths(self) -> None:
        self.assertEqual(canonical_digest({"ok": True})[:7], "sha256:")
        self.assertEqual(EffectMode.OBSERVE.value, "observe")
        self.assertEqual(
            assess_binding("unknown", ContractChange.IDENTICAL),
            BindingDecision.OBSERVE_ORIGINAL,
        )

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
            "anc_effect_ir": {"anc_canonical"},
            "anc_tool_contract": {"anc_canonical"},
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


if __name__ == "__main__":
    unittest.main()
