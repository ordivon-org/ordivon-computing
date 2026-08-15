from __future__ import annotations

import unittest

from ordivon_observation_core.canonical import CanonicalValueError, namespaced_kind


class NamespacedKindTests(unittest.TestCase):
    def test_accepts_historical_language_without_regex_backtracking(self) -> None:
        accepted = (
            "world.resource",
            "world-resource",
            "a-b-c",
            "a.b-c_d",
            "a-b--c_",
            "a1.b2.c3",
        )
        for value in accepted:
            with self.subTest(value=value):
                self.assertEqual(namespaced_kind(value, label="kind"), value)

    def test_rejects_invalid_boundaries(self) -> None:
        rejected = (
            "a",
            "A.kind",
            "a_thing.kind",
            "a-",
            "a--b",
            "a..b",
            "a._b",
            "a-b.",
            "a/b.kind",
        )
        for value in rejected:
            with self.subTest(value=value):
                with self.assertRaises(CanonicalValueError):
                    namespaced_kind(value, label="kind")

    def test_adversarial_hyphen_shape_is_bounded_before_linear_parse(self) -> None:
        with self.assertRaises(CanonicalValueError):
            namespaced_kind("a-0" + "-0" * 300, label="kind")


if __name__ == "__main__":
    unittest.main()
