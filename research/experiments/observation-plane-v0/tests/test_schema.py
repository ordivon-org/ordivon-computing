from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from ordivon_observation_core.schema import schemas  # noqa: E402


class ObservationSchemaTests(unittest.TestCase):
    def test_generated_schemas_are_valid_and_frozen(self) -> None:
        generated = schemas()
        self.assertEqual(
            set(generated),
            {
                "observation-envelope-v1.schema.json",
                "observation-ingest-batch-v1.schema.json",
                "observation-ingest-acknowledgement-v1.schema.json",
                "observation-export-checkpoint-v1.schema.json",
                "observation-export-bundle-v1.schema.json",
                "observation-selection-manifest-v1.schema.json",
            },
        )
        for name, schema in generated.items():
            with self.subTest(name=name):
                Draft202012Validator.check_schema(schema)
                frozen = json.loads((ROOT / "schemas" / name).read_text())
                self.assertEqual(frozen, schema)

    def test_canonical_envelope_omits_dynamic_export_time(self) -> None:
        schema = schemas()["observation-envelope-v1.schema.json"]
        properties = schema["properties"]
        self.assertNotIn("exportedAtMs", properties)
        self.assertIn("occurredAtMs", properties)
        self.assertFalse(schema["additionalProperties"])

    def test_export_receipt_schemas_keep_dynamic_time_outside_envelopes(self) -> None:
        generated = schemas()
        checkpoint = generated["observation-export-checkpoint-v1.schema.json"]
        bundle = generated["observation-export-bundle-v1.schema.json"]
        self.assertIn("updatedAtMs", checkpoint["properties"])
        self.assertIn("exportedAtMs", bundle["properties"])
        self.assertNotIn(
            "exportedAtMs",
            generated["observation-envelope-v1.schema.json"]["properties"],
        )
        self.assertEqual(
            bundle["properties"]["ownerRevision"]["pattern"],
            "^[0-9a-f]{40}$",
        )

    def test_minimum_core_is_metadata_and_reference_only(self) -> None:
        schema = schemas()["observation-envelope-v1.schema.json"]
        privacy = schema["properties"]["privacy"]
        self.assertEqual(
            privacy["properties"]["containsInlineContent"], {"const": False}
        )
        self.assertNotIn(
            "secret_forbidden", privacy["properties"]["class"]["enum"]
        )


if __name__ == "__main__":
    unittest.main()
