from __future__ import annotations

import json
import unittest
from anc_canonical import CanonicalError, canonical_digest, canonical_text, loads_strict
from ordivon_protocol import vector_text


class CanonicalTests(unittest.TestCase):
    def test_golden_vectors(self) -> None:
        vectors = json.loads(vector_text("canonical-vectors.json"))
        for vector in vectors:
            with self.subTest(vector=vector["name"]):
                self.assertEqual(canonical_text(vector["value"]), vector["canonical"])
                self.assertEqual(canonical_digest(vector["value"]), vector["digest"])

    def test_object_order_is_not_semantic(self) -> None:
        self.assertEqual(canonical_digest({"a": 1, "b": 2}), canonical_digest({"b": 2, "a": 1}))

    def test_array_order_is_semantic(self) -> None:
        self.assertNotEqual(canonical_digest([1, 2]), canonical_digest([2, 1]))

    def test_duplicate_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(CanonicalError, "duplicate"):
            loads_strict('{"a":1,"a":2}')

    def test_float_and_nonfinite_numbers_are_rejected(self) -> None:
        for raw in ("1.25", "NaN", "Infinity", "-Infinity"):
            with self.subTest(raw=raw), self.assertRaises(CanonicalError):
                loads_strict(raw)

    def test_null_and_absent_are_different(self) -> None:
        self.assertNotEqual(canonical_digest({"x": None}), canonical_digest({}))


if __name__ == "__main__":
    unittest.main()
