from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionC3Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = json.loads((ROOT / "evidence/computer-contraction-c3-research-contract.json").read_text())

    def test_global_method_surface_is_removed(self) -> None:
        for relative in (
            "research-method-v1.json",
            "AGENT-FIRST-RESEARCH-METHOD.md",
        ):
            self.assertFalse((ROOT / relative).exists())
        self.assertFalse((ROOT.parent / "scripts/check_agent_research_method.py").exists())

    def test_old_method_objects_are_git_recoverable(self) -> None:
        revision = self.doc["baseRevision"]
        for item in self.doc["removedGitObjects"]:
            actual = subprocess.check_output(["git", "-C", str(ROOT.parent), "rev-parse", f"{revision}:{item['path']}"], text=True).strip()
            self.assertEqual(actual, item["gitObject"])

    def test_current_contract_is_much_smaller_and_not_semantic_authority(self) -> None:
        self.assertLess(self.doc["after"]["surfaceRatioLines"], 0.2)
        contract = json.loads((ROOT / "experiment-contract-v1.json").read_text())
        self.assertIn("template_does_not_choose_the_hypothesis_or_correct_answer", contract["invariants"])
        self.assertIn("authorizes no experiment", contract["localizationRule"])


if __name__ == "__main__":
    unittest.main()
