from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "staging_rehearsal.py"
SPEC = importlib.util.spec_from_file_location("staging_rehearsal", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class StagingRehearsalContractTests(unittest.TestCase):
    def test_staging_path_guard_rejects_authority_and_external_paths(self) -> None:
        for path in (
            Path("/var/lib/ordivon/host"),
            Path("/var/lib/ordivon/harness"),
            Path("/var/lib/ordivon/staging"),
            Path("/tmp/a4"),
        ):
            with self.subTest(path=path), self.assertRaises(ValueError):
                MODULE._validate_staging_root(path)
        accepted = MODULE._validate_staging_root(
            Path("/var/lib/ordivon/staging/a4-contract-test")
        )
        self.assertEqual(
            accepted, Path("/var/lib/ordivon/staging/a4-contract-test")
        )

    def test_vector_is_integrity_bound_and_exact(self) -> None:
        vector, revisions = MODULE._load_vector(ROOT / "system-version-vector-v1.json")
        self.assertEqual(vector["vectorId"], "OCR-A3-20260806-01")
        self.assertEqual(
            set(revisions),
            {"computing", "host", "harness", "harnessImplementation", "runtime", "protocol"},
        )
        for revision in revisions.values():
            self.assertEqual(len(revision), 40)
            int(revision, 16)

    def test_vector_tampering_is_rejected(self) -> None:
        source = json.loads((ROOT / "system-version-vector-v1.json").read_text())
        source["repositories"]["host"]["revision"] = "0" * 40
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vector.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "integrity"):
                MODULE._load_vector(path)

    def test_canonical_digest_ignores_only_integrity(self) -> None:
        value = {"schemaVersion": 1, "kind": "fixture", "value": 3}
        digest = MODULE._canonical_digest(value)
        value["integrity"] = {"payloadDigest": digest}
        self.assertEqual(MODULE._canonical_digest(value), digest)
        value["value"] = 4
        self.assertNotEqual(MODULE._canonical_digest(value), digest)


if __name__ == "__main__":
    unittest.main()
