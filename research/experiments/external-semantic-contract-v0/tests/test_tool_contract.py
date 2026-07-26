from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path

from anc_tool_contract import (
    ContractChange,
    classify_contract_change,
    contract_digest,
    normalize_tool_contract,
)

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    raw = json.loads((ROOT / "fixtures/contracts" / name).read_text())
    return normalize_tool_contract(raw)


class ToolContractTests(unittest.TestCase):
    def test_presentation_metadata_does_not_change_digest(self) -> None:
        path = ROOT / "fixtures/contracts/ordivon-workspace-read-current.json"
        raw = json.loads(path.read_text())
        first = normalize_tool_contract(raw)
        raw["description"] = "different human explanation"
        raw["inputSchema"]["description"] = "ignored presentation"
        second = normalize_tool_contract(raw)
        self.assertEqual(contract_digest(first), contract_digest(second))

    def test_real_schema_version_tightening_requires_caller_adaptation(self) -> None:
        old = load("ordivon-workspace-exec-old.json")
        new = load("ordivon-workspace-exec-current.json")
        self.assertIs(
            classify_contract_change(old, new), ContractChange.CALLER_ADAPTATION
        )

    def test_semantic_action_change_is_breaking(self) -> None:
        contract = load("ordivon-workspace-read-current.json")
        changed = replace(contract, semantic_action="anc.object.replace-if-version.v1")
        self.assertIs(
            classify_contract_change(contract, changed), ContractChange.SEMANTIC_BREAK
        )

    def test_optional_output_extension_is_compatible(self) -> None:
        contract = load("ordivon-workspace-read-current.json")
        output = dict(contract.output_schema)
        properties = dict(output["properties"])
        properties["mediaType"] = {"type": "string"}
        output["properties"] = properties
        changed = replace(contract, revision="runtime-schema-v2", output_schema=output)
        self.assertIs(
            classify_contract_change(contract, changed),
            ContractChange.COMPATIBLE_EXTENSION,
        )

    def test_unknown_schema_keyword_fails_closed(self) -> None:
        raw = json.loads(
            (ROOT / "fixtures/contracts/ordivon-workspace-read-current.json").read_text()
        )
        raw["inputSchema"]["unevaluatedProperties"] = False
        with self.assertRaisesRegex(ValueError, "unsupported JSON Schema keyword"):
            normalize_tool_contract(raw)


if __name__ == "__main__":
    unittest.main()
