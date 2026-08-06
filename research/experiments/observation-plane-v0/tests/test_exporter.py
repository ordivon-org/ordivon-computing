from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from ordivon_observation_core import (  # noqa: E402
    ObservationBundleConflict,
    ObservationCheckpointConflict,
    ObservationCheckpointCorrupt,
    ObservationExportBundle,
    ObservationExportCheckpoint,
    ObservationProducerIdentity,
    load_checkpoint,
    write_checkpoint,
    write_export_bundle,
)
from ordivon_observation_core.fixtures import (  # noqa: E402
    HOST,
    three_owner_batches,
)

OWNER_REVISION = "1" * 40
EXPORTER_REVISION = "2" * 40
MAPPING_VERSION = "host-observation-v1"


class ObservationExporterContractTests(unittest.TestCase):
    def test_checkpoint_roundtrip_advance_and_cas(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sidecar" / "host-checkpoint.json"
            empty = load_checkpoint(
                path,
                producer_identity=HOST,
                mapping_version=MAPPING_VERSION,
            )
            self.assertEqual(empty.streams, {})
            self.assertEqual(empty.updated_at_ms, 0)
            advanced = empty.advance(
                {"host-journal:fixture": 5, "runtime-job:fixture": 2},
                updated_at_ms=1_000,
            )
            write_checkpoint(path, advanced, expected_digest=None)
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
            self.assertEqual(os.stat(path.parent).st_mode & 0o777, 0o700)
            loaded = load_checkpoint(
                path,
                producer_identity=HOST,
                mapping_version=MAPPING_VERSION,
            )
            self.assertEqual(loaded, advanced)
            next_value = loaded.advance(
                {"runtime-job:fixture": 4}, updated_at_ms=1_001
            )
            write_checkpoint(
                path,
                next_value,
                expected_digest=loaded.integrity_digest,
            )
            with self.assertRaises(ObservationCheckpointConflict):
                write_checkpoint(
                    path,
                    loaded,
                    expected_digest=loaded.integrity_digest,
                )
            self.assertEqual(
                load_checkpoint(
                    path,
                    producer_identity=HOST,
                    mapping_version=MAPPING_VERSION,
                ),
                next_value,
            )

    def test_checkpoint_cannot_move_backward_or_cross_identity(self) -> None:
        current = ObservationExportCheckpoint.build(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
            streams={"host-stream": 4},
            updated_at_ms=100,
        )
        with self.assertRaises(ObservationCheckpointConflict):
            current.advance({"host-stream": 3}, updated_at_ms=101)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            write_checkpoint(path, current, expected_digest=None)
            other = ObservationProducerIdentity(
                "ordivon-host", "host-journal", "host:other"
            )
            with self.assertRaisesRegex(ObservationCheckpointCorrupt, "producer"):
                load_checkpoint(
                    path,
                    producer_identity=other,
                    mapping_version=MAPPING_VERSION,
                )
            with self.assertRaisesRegex(ObservationCheckpointCorrupt, "mapping"):
                load_checkpoint(
                    path,
                    producer_identity=HOST,
                    mapping_version="host-observation-v2",
                )

    def test_checkpoint_symlink_and_insecure_mode_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target.json"
            value = ObservationExportCheckpoint.empty(
                producer_identity=HOST,
                mapping_version=MAPPING_VERSION,
            )
            write_checkpoint(target, value, expected_digest=None)
            link = Path(directory) / "link.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(ObservationCheckpointCorrupt, "symlink"):
                load_checkpoint(
                    link,
                    producer_identity=HOST,
                    mapping_version=MAPPING_VERSION,
                )
            os.chmod(target, 0o644)
            with self.assertRaisesRegex(ObservationCheckpointCorrupt, "permissions"):
                load_checkpoint(
                    target,
                    producer_identity=HOST,
                    mapping_version=MAPPING_VERSION,
                )

            public_parent = Path(directory) / "public-sidecar"
            public_parent.mkdir(mode=0o755)
            with self.assertRaisesRegex(ObservationCheckpointCorrupt, "parent permissions"):
                write_checkpoint(
                    public_parent / "checkpoint.json",
                    value,
                    expected_digest=None,
                )
            self.assertEqual(os.stat(public_parent).st_mode & 0o777, 0o755)

    def test_export_bundle_roundtrip_and_dynamic_export_time(self) -> None:
        host_batch = three_owner_batches()[0]
        before = ObservationExportCheckpoint.empty(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
        )
        after = before.advance(
            {host_batch.stream_id: host_batch.last_sequence},
            updated_at_ms=2_000,
        )
        first = ObservationExportBundle.build(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
            owner_revision=OWNER_REVISION,
            exporter_revision=EXPORTER_REVISION,
            exported_at_ms=2_001,
            checkpoint_before=before,
            checkpoint_after=after,
            batches=(host_batch,),
        )
        decoded = ObservationExportBundle.from_dict(first.to_dict())
        self.assertEqual(decoded, first)
        second = ObservationExportBundle.build(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
            owner_revision=OWNER_REVISION,
            exporter_revision=EXPORTER_REVISION,
            exported_at_ms=9_999,
            checkpoint_before=before,
            checkpoint_after=after,
            batches=(host_batch,),
        )
        self.assertNotEqual(first.integrity_digest, second.integrity_digest)
        self.assertEqual(
            first.batches[0].events[0].canonical_digest,
            second.batches[0].events[0].canonical_digest,
        )
        self.assertNotIn("exportedAtMs", first.batches[0].events[0].to_dict())

    def test_export_bundle_rejects_backward_checkpoint(self) -> None:
        host_batch = three_owner_batches()[0]
        before = ObservationExportCheckpoint.build(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
            streams={host_batch.stream_id: host_batch.last_sequence},
            updated_at_ms=2_000,
        )
        after = ObservationExportCheckpoint.empty(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
        )
        with self.assertRaises(ObservationCheckpointConflict):
            ObservationExportBundle.build(
                producer_identity=HOST,
                mapping_version=MAPPING_VERSION,
                owner_revision=OWNER_REVISION,
                exporter_revision=EXPORTER_REVISION,
                exported_at_ms=2_001,
                checkpoint_before=before,
                checkpoint_after=after,
                batches=(host_batch,),
            )

    def test_export_bundle_rejects_mixed_producer_and_mapping(self) -> None:
        host_batch, harness_batch, _ = three_owner_batches()
        before = ObservationExportCheckpoint.empty(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
        )
        after = before.advance(
            {host_batch.stream_id: host_batch.last_sequence},
            updated_at_ms=2_000,
        )
        with self.assertRaisesRegex(Exception, "producer"):
            ObservationExportBundle.build(
                producer_identity=HOST,
                mapping_version=MAPPING_VERSION,
                owner_revision=OWNER_REVISION,
                exporter_revision=EXPORTER_REVISION,
                exported_at_ms=2_001,
                checkpoint_before=before,
                checkpoint_after=after,
                batches=(harness_batch,),
            )

    def test_bundle_outbox_is_private_atomic_and_idempotent(self) -> None:
        host_batch = three_owner_batches()[0]
        before = ObservationExportCheckpoint.empty(
            producer_identity=HOST, mapping_version=MAPPING_VERSION
        )
        after = before.advance(
            {host_batch.stream_id: host_batch.last_sequence}, updated_at_ms=2_000
        )
        bundle = ObservationExportBundle.build(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
            owner_revision=OWNER_REVISION,
            exporter_revision=EXPORTER_REVISION,
            exported_at_ms=2_001,
            checkpoint_before=before,
            checkpoint_after=after,
            batches=(host_batch,),
        )
        with tempfile.TemporaryDirectory() as directory:
            outbox = Path(directory) / "outbox"
            first = write_export_bundle(outbox, bundle)
            second = write_export_bundle(outbox, bundle)
            self.assertEqual(first, second)
            self.assertEqual(os.stat(outbox).st_mode & 0o777, 0o700)
            self.assertEqual(os.stat(first).st_mode & 0o777, 0o600)
            self.assertEqual(
                ObservationExportBundle.from_dict(
                    json.loads(first.read_text(encoding="utf-8"))
                ),
                bundle,
            )
            self.assertEqual([item.name for item in outbox.iterdir()], [first.name])

    def test_bundle_outbox_rejects_public_or_symlink_paths(self) -> None:
        host_batch = three_owner_batches()[0]
        before = ObservationExportCheckpoint.empty(
            producer_identity=HOST, mapping_version=MAPPING_VERSION
        )
        after = before.advance(
            {host_batch.stream_id: host_batch.last_sequence}, updated_at_ms=2_000
        )
        bundle = ObservationExportBundle.build(
            producer_identity=HOST,
            mapping_version=MAPPING_VERSION,
            owner_revision=OWNER_REVISION,
            exporter_revision=EXPORTER_REVISION,
            exported_at_ms=2_001,
            checkpoint_before=before,
            checkpoint_after=after,
            batches=(host_batch,),
        )
        with tempfile.TemporaryDirectory() as directory:
            public = Path(directory) / "public"
            public.mkdir(mode=0o755)
            os.chmod(public, 0o755)
            with self.assertRaisesRegex(ObservationBundleConflict, "permissions"):
                write_export_bundle(public, bundle)
            private = Path(directory) / "private"
            private.mkdir(mode=0o700)
            link = Path(directory) / "link"
            link.symlink_to(private, target_is_directory=True)
            with self.assertRaisesRegex(ObservationBundleConflict, "symlink"):
                write_export_bundle(link, bundle)

    def test_checkpoint_bytes_do_not_retain_temporary_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sidecar" / "checkpoint.json"
            value = ObservationExportCheckpoint.empty(
                producer_identity=HOST,
                mapping_version=MAPPING_VERSION,
            )
            write_checkpoint(path, value, expected_digest=None)
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")), value.to_dict()
            )
            self.assertEqual(
                [entry.name for entry in path.parent.iterdir()], [path.name]
            )


if __name__ == "__main__":
    unittest.main()
