from __future__ import annotations

import json
import unittest

from jsonschema import Draft202012Validator

from ordivon_protocol import schema_text, vector_text
from ordivon_protocol.host_workload import (
    WorkloadValidationError,
    validate_host_workload_object,
)


class HostWorkloadSchemaConformanceTests(unittest.TestCase):
    def test_schema_and_python_accept_every_normative_valid_object(self) -> None:
        schema = json.loads(schema_text("host-workload-v1.schema.json"))
        validator = Draft202012Validator(schema)
        vectors = json.loads(vector_text("host-workload-vectors-v1.json"))
        for case in vectors["cases"]:
            if case["operation"] != "validate" or not case["expected"]["accepted"]:
                continue
            with self.subTest(case=case["caseId"]):
                validator.validate(case["input"])
                validate_host_workload_object(case["input"])

    def test_current_structural_negative_is_rejected_by_both_surfaces(self) -> None:
        schema = json.loads(schema_text("host-workload-v1.schema.json"))
        validator = Draft202012Validator(schema)
        vectors = json.loads(vector_text("host-workload-vectors-v1.json"))
        case = next(
            item
            for item in vectors["cases"]
            if item["caseId"] == "reject-invalid-task-descriptor-digest"
        )
        self.assertFalse(case["expected"]["accepted"])
        self.assertTrue(list(validator.iter_errors(case["input"])))
        with self.assertRaises(WorkloadValidationError):
            validate_host_workload_object(case["input"])


if __name__ == "__main__":
    unittest.main()
