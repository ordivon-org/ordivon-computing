from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from anc_continuation.model import TaskCapsule, capsule_digest
from anc_continuation.store import FileObjectStore, ObjectCorrupt, ObjectMissing
from anc_continuation.workload import freeze_checkpoint


class ModelStoreTests(unittest.TestCase):
    def test_capsule_round_trip_is_content_addressed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            capsule = store.get_capsule(frozen.capsule_digest)
            self.assertIsInstance(capsule, TaskCapsule)
            self.assertEqual(capsule_digest(capsule), frozen.capsule_digest)
            self.assertEqual(store.put_capsule(capsule), frozen.capsule_digest)
            self.assertEqual(capsule.capsule_revision, 1)

    def test_missing_and_corrupt_objects_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            with self.assertRaises(ObjectMissing):
                store.get("sha256:" + "0" * 64)
            path = store.root / f"{frozen.capsule_digest[7:]}.json"
            path.write_text("{}")
            with self.assertRaises(ObjectCorrupt):
                store.get_capsule(frozen.capsule_digest)


if __name__ == "__main__":
    unittest.main()
