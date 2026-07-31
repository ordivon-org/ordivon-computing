from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "validate_evaluation_evidence.py"
EXAMPLES = ROOT / "examples"
SCHEMAS = ROOT / "schemas"

spec = importlib.util.spec_from_file_location("track_r_validator", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class EvaluationEvidenceTests(unittest.TestCase):
    def load_examples(self) -> list[dict]:
        return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(EXAMPLES.rglob("*.json"))]

    def test_all_schemas_are_valid_json_objects(self) -> None:
        for path in sorted(SCHEMAS.glob("*.json")):
            with self.subTest(schema=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsInstance(value, dict)
                self.assertEqual(value["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_historical_examples_validate_as_one_collection(self) -> None:
        documents = self.load_examples()
        validator.validate_collection(documents)
        self.assertEqual(len(documents), 11)

    def test_integrity_detects_tampering(self) -> None:
        document = self.load_examples()[0]
        tampered = copy.deepcopy(document)
        if tampered["kind"] == "ordivon.evaluation-trial":
            tampered["limitations"].append("tampered")
        else:
            tampered["integrity"]["payloadDigest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "payloadDigest"):
            validator.validate_document(tampered)

    def test_accepted_result_requires_passed_verifier(self) -> None:
        result = next(item for item in self.load_examples() if item["kind"] == "ordivon.evaluation-result" and item["acceptance"]["status"] == "accepted")
        invalid = copy.deepcopy(result)
        invalid["acceptance"]["verifier"]["status"] = "not_run"
        invalid["integrity"]["payloadDigest"] = validator.payload_digest(invalid)
        with self.assertRaisesRegex(ValueError, "passed verifier"):
            validator.validate_result(invalid)

    def test_missing_trial_relation_is_rejected(self) -> None:
        documents = self.load_examples()
        result = next(item for item in documents if item["kind"] == "ordivon.evaluation-result")
        filtered = [
            item
            for item in documents
            if not (item["kind"] == "ordivon.evaluation-trial" and item["trialId"] == result["trialId"])
        ]
        with self.assertRaisesRegex(ValueError, "missing Trial Manifest"):
            validator.validate_collection(filtered)

    def test_write_digest_round_trip(self) -> None:
        source = next(path for path in sorted(EXAMPLES.rglob("*.json")) if json.loads(path.read_text())["kind"] == "ordivon.evaluation-trial")
        document = json.loads(source.read_text(encoding="utf-8"))
        document["integrity"]["payloadDigest"] = "sha256:" + "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            loaded = validator.load_documents([path])
            validator.write_digests(loaded)
            rewritten = json.loads(path.read_text(encoding="utf-8"))
            validator.validate_document(rewritten)


if __name__ == "__main__":
    unittest.main()
