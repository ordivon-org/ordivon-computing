from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "check_foundational_docs",
    ROOT / "scripts" / "check_foundational_docs.py",
)
assert SPEC is not None and SPEC.loader is not None
CHECK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECK
SPEC.loader.exec_module(CHECK)


class FoundationalDocsTests(unittest.TestCase):
    def test_repository_foundations_are_consistent(self) -> None:
        self.assertEqual(CHECK.check_repository(ROOT), [])

    def test_broken_relative_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            document = root / "README.md"
            document.write_text("[missing](not-there.md)\n", encoding="utf-8")
            self.assertEqual(
                CHECK.broken_relative_links(root, [document]),
                ["broken relative link: README.md -> not-there.md"],
            )

    def test_reference_ledger_rejects_unknown_identifier(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            study = root / "studies" / "2026-classical-to-agent-native-computing"
            study.mkdir(parents=True)
            (study / "REFERENCES.md").write_text(
                "### C01 — Known\n", encoding="utf-8"
            )
            (study / "README.md").write_text("Unknown [A99].\n", encoding="utf-8")
            self.assertEqual(
                CHECK.reference_issues(root),
                ["undeclared primary-source reference: A99"],
            )


if __name__ == "__main__":
    unittest.main()
