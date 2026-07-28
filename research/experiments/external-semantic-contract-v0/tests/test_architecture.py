from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[2]
SRC = REPOSITORY / "packages" / "ordivon-protocol" / "src"


class ArchitectureTests(unittest.TestCase):
    def test_package_dependency_direction(self) -> None:
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
        }
        for package, permitted in allowed.items():
            imported: set[str] = set()
            for path in (SRC / package).glob("*.py"):
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

    def test_kernel_does_not_import_external_contract_packages(self) -> None:
        kernel = ROOT.parent / "semantic-core-v0" / "src" / "anc_semantic_core"
        for path in kernel.glob("*.py"):
            source = path.read_text()
            for forbidden in (
                "anc_canonical",
                "anc_effect_ir",
                "anc_tool_contract",
                "anc_effect_binding",
            ):
                self.assertNotIn(forbidden, source, path)

    def test_experiment_has_no_shadow_protocol_source(self) -> None:
        shadow = ROOT / "src"
        self.assertFalse(any(shadow.glob("anc_*")))


if __name__ == "__main__":
    unittest.main()
