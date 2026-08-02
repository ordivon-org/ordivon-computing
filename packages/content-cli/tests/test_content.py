from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ordivon_content.check import check_repository
from ordivon_content.yaml_subset import loads


PROJECT = """schema_version: 1
id: ordivon-fixture
name: Ordivon Fixture
repository: https://github.com/zycxfyh/ordivon-fixture
kind: engineering
default_profiles:
  - engineering
documentation_roots:
  - docs
managed_paths:
  - docs/managed
enforcement: advisory
maintainers:
  - fixture
"""

VALID = """---
schema_version: 1
id: fixture.architecture
title: Fixture Architecture
type: architecture
profile: engineering
lifecycle: active
source_role: canonical
visibility: internal
owners:
  - ordivon-fixture
audience:
  - maintainer
updated: 2026-08-03
---
# Fixture Architecture

## Purpose

Test the strict content path.

## Boundaries

No external effects.

## Components

One fixture.

## Data flow

Input to output.

## Failure modes

A missing section fails.

## Verification

The check returns READY.
"""


class YamlSubsetTests(unittest.TestCase):
    def test_flat_mapping_and_block_list(self) -> None:
        self.assertEqual(loads("schema_version: 1\nitems:\n  - one\n  - two\n"), {"schema_version": 1, "items": ["one", "two"]})

    def test_nested_mapping_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "nested mappings"):
            loads("outer:\n  inner: value\n")


class RepositoryCheckTests(unittest.TestCase):
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / ".ordivon").mkdir()
        (root / ".ordivon" / "project.yaml").write_text(PROJECT, encoding="utf-8")
        (root / "docs" / "managed").mkdir(parents=True)
        return root

    def test_advisory_legacy_document_is_degraded(self) -> None:
        root = self.make_root()
        (root / "docs" / "legacy.md").write_text("# Legacy\n\nNo metadata yet.\n", encoding="utf-8")
        receipt = check_repository(root, mode="advisory")
        self.assertEqual(receipt["contentState"], "DEGRADED")
        self.assertEqual(receipt["blockingFailures"], 0)

    def test_strict_managed_document_requires_metadata(self) -> None:
        root = self.make_root()
        (root / "docs" / "managed" / "missing.md").write_text("# Missing\n", encoding="utf-8")
        receipt = check_repository(root, mode="strict")
        self.assertEqual(receipt["contentState"], "BLOCKED")
        self.assertIn("DOC001", {issue["code"] for issue in receipt["issues"]})

    def test_valid_managed_document_is_ready(self) -> None:
        root = self.make_root()
        (root / "docs" / "managed" / "valid.md").write_text(VALID, encoding="utf-8")
        receipt = check_repository(root, mode="strict")
        self.assertEqual(receipt["contentState"], "READY")

    def test_broken_link_blocks_strict_managed_document(self) -> None:
        root = self.make_root()
        text = VALID.replace("The check returns READY.", "The check returns READY. [Missing](missing.md)")
        (root / "docs" / "managed" / "valid.md").write_text(text, encoding="utf-8")
        receipt = check_repository(root, mode="strict")
        self.assertEqual(receipt["contentState"], "BLOCKED")
        self.assertIn("LINK001", {issue["code"] for issue in receipt["issues"]})


if __name__ == "__main__":
    unittest.main()
