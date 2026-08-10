from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]


class ContractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / "evidence" / "pre-contraction-inventory.json").read_text())

    def test_old_crosscut_families_are_not_in_active_tree(self):
        for row in self.inventory["families"]:
            self.assertFalse((REPO / row["path"]).exists(), row["path"])

    def test_every_removed_family_is_exactly_recoverable_from_git(self):
        revision = self.inventory["baseRevision"]
        for row in self.inventory["families"]:
            tree = subprocess.run(["git", "-C", str(REPO), "rev-parse", f"{revision}:{row['path']}"], text=True, capture_output=True, check=True).stdout.strip()
            self.assertEqual(tree, row["treeObject"])

    def test_removed_mass_is_material(self):
        total = self.inventory["totals"]
        self.assertEqual(total["files"], 87)
        self.assertEqual(total["bytes"], 438877)
        self.assertEqual(total["lines"], 10722)


if __name__ == "__main__":
    unittest.main()
