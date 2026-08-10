from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECK = _load("check_research_portfolio", "scripts/check_research_portfolio.py")
RENDER = _load("render_research_portfolio", "scripts/render_research_portfolio.py")


class ResearchPortfolioTests(unittest.TestCase):
    def test_repository_portfolio_is_valid(self) -> None:
        self.assertEqual(CHECK.check_portfolio(ROOT), [])

    def test_rendered_view_is_current(self) -> None:
        document = json.loads((ROOT / "research" / "portfolio.json").read_text())
        self.assertEqual(
            RENDER.render(document),
            (ROOT / "research" / "PORTFOLIO.md").read_text(),
        )

    def test_judgment_rule_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "research" / "questions").mkdir(parents=True)
            document = json.loads((ROOT / "research" / "portfolio.json").read_text())
            document["policy"].pop("judgmentRule")
            path = root / "research" / "portfolio.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            issues = CHECK.check_portfolio(root, path)
            self.assertIn("portfolio judgmentRule is missing", issues)

    def test_source_identity_rule_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "research" / "questions").mkdir(parents=True)
            document = json.loads((ROOT / "research" / "portfolio.json").read_text())
            document["policy"].pop("sourceIdentityRule")
            path = root / "research" / "portfolio.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            issues = CHECK.check_portfolio(root, path)
            self.assertIn("portfolio sourceIdentityRule is missing", issues)

    def test_external_observation_must_bind_exact_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "research" / "questions").mkdir(parents=True)
            document = json.loads((ROOT / "research" / "portfolio.json").read_text())
            harness = next(item for item in document["questions"] if item["id"] == "ANC-HARNESS-002")
            harness["status"] = "active"
            evidence_rel = harness["externalObservation"]["evidence"][0]
            evidence_path = root / evidence_rel
            evidence_path.parent.mkdir(parents=True)
            evidence_path.write_text(json.dumps({"repositoryId":"ordivon-harness","revision":"0" * 40}), encoding="utf-8")
            source_page = root / harness["source"]
            source_page.parent.mkdir(parents=True, exist_ok=True)
            source_page.write_text("# fixture\n", encoding="utf-8")
            path = root / "research" / "portfolio.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            issues = CHECK.check_portfolio(root, path)
            self.assertIn("externalObservation evidence does not bind exact revision: ANC-HARNESS-002", issues)

    def test_wip_limit_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "research" / "questions").mkdir(parents=True)
            source = ROOT / "research" / "portfolio.json"
            document = json.loads(source.read_text())
            document["policy"]["activeLineLimit"] = 1
            document["activeLines"] = [
                {
                    "id": "TEST-LINE-A",
                    "title": "Fixture line A",
                    "priority": "P0",
                    "questions": ["ANC-VERIFY-001"],
                    "issues": ["test#line-a"],
                    "exitCriteria": "fixture",
                },
                {
                    "id": "TEST-LINE-B",
                    "title": "Fixture line B",
                    "priority": "P1",
                    "questions": ["ANC-VERIFY-002"],
                    "issues": ["test#line-b"],
                    "exitCriteria": "fixture",
                },
            ]
            path = root / "research" / "portfolio.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            issues = CHECK.check_portfolio(root, path)
            self.assertIn("active research-line WIP limit exceeded", issues)


if __name__ == "__main__":
    unittest.main()
