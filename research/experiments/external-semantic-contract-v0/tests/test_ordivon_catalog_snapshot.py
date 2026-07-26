from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "fixtures/contracts/ordivon-live-catalog.json"


class OrdivonCatalogSnapshotTests(unittest.TestCase):
    def test_snapshot_contains_the_first_live_contract_set(self) -> None:
        snapshot = json.loads(SNAPSHOT.read_text())
        self.assertEqual(snapshot["schemaVersion"], 1)
        self.assertEqual(snapshot["providerId"], "ordivon-runtime")
        self.assertTrue(snapshot["catalogRevision"].startswith("mcp-catalog:"))
        self.assertEqual(
            set(snapshot["contracts"]),
            {
                "workspace.read",
                "workspace.mutate",
                "workspace.exec",
                "task.observe",
                "artifact.read",
            },
        )

    def test_exec_snapshot_matches_the_nested_runtime_request(self) -> None:
        snapshot = json.loads(SNAPSHOT.read_text())
        contract = snapshot["contracts"]["workspace.exec"]
        execution = contract["inputSchema"]["properties"]["execution"]
        self.assertEqual(execution["$ref"], "#/$defs/UniversalExecutionRequest")
        self.assertEqual(contract["semanticAction"], "anc.execution.launch.v1")
        self.assertEqual(contract["idempotencySupport"], "keyed")

    def test_observation_and_artifact_contracts_are_normalized(self) -> None:
        contracts = json.loads(SNAPSHOT.read_text())["contracts"]
        self.assertEqual(
            contracts["task.observe"]["semanticAction"],
            "anc.execution.observe.v1",
        )
        self.assertEqual(
            contracts["artifact.read"]["semanticAction"],
            "anc.artifact.read.v1",
        )
        self.assertIsNone(contracts["task.observe"]["outputSchema"])
        self.assertIsNone(contracts["artifact.read"]["outputSchema"])

    def test_presentation_schema_marker_is_not_in_contract_identity(self) -> None:
        snapshot = SNAPSHOT.read_text()
        self.assertNotIn('"$schema"', snapshot)
        self.assertNotIn('"description"', snapshot)


if __name__ == "__main__":
    unittest.main()
