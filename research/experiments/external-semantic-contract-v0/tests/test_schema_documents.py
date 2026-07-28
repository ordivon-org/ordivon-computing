from __future__ import annotations

import json
import unittest

from ordivon_protocol import schema_text


class SchemaDocumentTests(unittest.TestCase):
    def test_public_schemas_are_closed_and_versioned(self) -> None:
        expected = {
            "effect-envelope-v1.schema.json": "anc.effect-envelope.v1",
            "tool-contract-v1.schema.json": "anc.tool-contract.v1",
            "effect-binding-v1.schema.json": "anc.effect-binding.v1",
        }
        for filename, schema_id in expected.items():
            with self.subTest(filename=filename):
                schema = json.loads(schema_text(filename))
                self.assertEqual(schema["$id"], schema_id)
                self.assertFalse(schema["additionalProperties"])
                self.assertEqual(schema["type"], "object")
                self.assertTrue(schema["required"])

    def test_canonical_json_schema_domain_excludes_floats(self) -> None:
        for filename in (
            "effect-envelope-v1.schema.json",
            "effect-binding-v1.schema.json",
        ):
            schema = json.loads(schema_text(filename))
            branches = schema["$defs"]["jsonValue"]["oneOf"]
            scalar_types = {branch.get("type") for branch in branches if "type" in branch}
            self.assertIn("integer", scalar_types)
            self.assertNotIn("number", scalar_types)

    def test_effect_schema_freezes_only_proven_actions(self) -> None:
        schema = json.loads(schema_text("effect-envelope-v1.schema.json"))
        actions = schema["properties"]["action"]["properties"]["actionId"]["enum"]
        self.assertEqual(
            actions,
            [
                "anc.object.read.v1",
                "anc.object.replace-if-version.v1",
                "anc.execution.launch.v1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
