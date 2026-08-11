from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "src"
sys.path.insert(0, str(IMPLEMENTATION))

from ordivon_observation_core import (  # noqa: E402
    ObservationBatch,
    ObservationCorruption,
    ObservationEnvelope,
    ObservationMappingRejected,
    ObservationPolicyRejected,
    ObservationPrivacy,
    ObservationProducerIdentity,
    ObservationRelation,
    ObservationSequenceGap,
    ObservationSource,
    SQLiteObservationGateway,
    canonical_digest,
)

PRODUCERS = (
    ObservationProducerIdentity("ordivon-host", "host-journal", "host:fixture"),
    ObservationProducerIdentity(
        "ordivon-harness", "harness-journal", "harness:fixture"
    ),
    ObservationProducerIdentity(
        "ordivon-runtime", "runtime-registry", "runtime:fixture"
    ),
)
MAPPINGS = (
    ("ordivon-host", "host-journal", "host-observation-v1"),
    ("ordivon-harness", "harness-journal", "harness-observation-v1"),
    ("ordivon-runtime", "runtime-registry", "runtime-observation-v1"),
)


def event(
    *,
    producer: ObservationProducerIdentity = PRODUCERS[0],
    stream_id: str = "host-stream:fixture",
    sequence: int,
    native_id: str,
    mapping_version: str = "host-observation-v1",
    relations: tuple[ObservationRelation, ...] = (),
    attributes: dict[str, object] | None = None,
) -> ObservationEnvelope:
    source = ObservationSource(
        project_id=producer.project_id,
        component_id=producer.component_id,
        instance_id=producer.instance_id,
        stream_id=stream_id,
        sequence=sequence,
        native_kind=f"{producer.project_id}.event",
        native_id=native_id,
        native_revision=sequence,
        native_digest=canonical_digest(
            {"nativeId": native_id, "sequence": sequence, "owner": producer.project_id}
        ),
        mapping_version=mapping_version,
    )
    return ObservationEnvelope.build(
        occurred_at_ms=1_000 + sequence,
        source=source,
        relations=relations,
        attributes=attributes or {"nativeState": "committed"},
        privacy=ObservationPrivacy("private_metadata", "observation-metadata-v1"),
    )


def batch(request_id: str, *events: ObservationEnvelope) -> ObservationBatch:
    return ObservationBatch.build(request_id=request_id, events=events)


class SQLiteObservationGatewayTests(unittest.TestCase):
    def initialize(self, directory: str) -> SQLiteObservationGateway:
        return SQLiteObservationGateway.initialize(
            Path(directory) / "gateway",
            gateway_instance_id="observation-gateway:fixture",
            producer_allowlist=PRODUCERS,
            mapping_versions=MAPPINGS,
            created_at_ms=100,
        )

    def test_symlink_state_root_is_rejected_before_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            link = Path(directory) / "gateway-link"
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                SQLiteObservationGateway.initialize(
                    link,
                    gateway_instance_id="gateway:symlink",
                    producer_allowlist=PRODUCERS,
                    mapping_versions=MAPPINGS,
                    created_at_ms=100,
                )

    def test_initialize_private_modes_ingest_replay_and_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.initialize(directory) as gateway:
                first = event(sequence=1, native_id="event:host:1")
                second = event(sequence=2, native_id="event:host:2")
                value = batch("request:host:1-2", first, second)
                acknowledgement = gateway.ingest(value, ingested_at_ms=2_000)
                self.assertEqual(acknowledgement.accepted, 2)
                self.assertEqual(acknowledgement.duplicates, 0)
                self.assertEqual(acknowledgement.last_contiguous_sequence, 2)
                exact_replay = gateway.ingest(value, ingested_at_ms=9_999)
                self.assertEqual(exact_replay, acknowledgement)
                duplicate = gateway.ingest(
                    batch("request:host:1-2:replay", first, second),
                    ingested_at_ms=2_001,
                )
                self.assertEqual(duplicate.accepted, 0)
                self.assertEqual(duplicate.duplicates, 2)
                self.assertEqual(gateway.event(first.event_id), first)
                self.assertTrue(gateway.doctor(full=True)["healthy"])
                digest_before = gateway.catalog_digest
                root = gateway.root
                database = gateway.database
                self.assertEqual(os.stat(root).st_mode & 0o777, 0o700)
                self.assertEqual(os.stat(database).st_mode & 0o777, 0o600)
            with SQLiteObservationGateway(root) as reopened:
                self.assertEqual(reopened.catalog_digest, digest_before)
                self.assertEqual(reopened.status()["events"], 2)
                self.assertTrue(reopened.doctor(full=True)["healthy"])

    def test_sequence_gap_is_visible_and_later_fill_restores_completeness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.initialize(directory) as gateway:
                second = event(sequence=2, native_id="event:host:2")
                with self.assertRaises(ObservationSequenceGap) as caught:
                    gateway.ingest(batch("request:gap:2", second), ingested_at_ms=2_000)
                self.assertEqual(caught.exception.acknowledgement.rejected, 1)
                status = gateway.stream_status(
                    project_id="ordivon-host",
                    component_id="host-journal",
                    instance_id="host:fixture",
                    stream_id="host-stream:fixture",
                )
                self.assertEqual(status["lastContiguousSequence"], 0)
                self.assertEqual(status["highestSeenSequence"], 2)
                self.assertEqual(status["completenessState"], "gap")
                self.assertEqual(gateway.status()["events"], 0)
                self.assertEqual(gateway.quarantine()[0]["reason"], "sequence_gap")

                first = event(sequence=1, native_id="event:host:1")
                gateway.ingest(batch("request:fill:1", first), ingested_at_ms=2_001)
                gateway.ingest(batch("request:fill:2", second), ingested_at_ms=2_002)
                status = gateway.stream_status(
                    project_id="ordivon-host",
                    component_id="host-journal",
                    instance_id="host:fixture",
                    stream_id="host-stream:fixture",
                )
                self.assertEqual(status["lastContiguousSequence"], 2)
                self.assertEqual(status["completenessState"], "complete")

    def test_event_conflict_rolls_back_the_complete_batch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.initialize(directory) as gateway:
                first = event(sequence=1, native_id="event:shared")
                gateway.ingest(batch("request:base", first), ingested_at_ms=2_000)
                second = event(sequence=2, native_id="event:new")
                conflicting = event(sequence=3, native_id="event:shared")
                with self.assertRaises(ObservationCorruption):
                    gateway.ingest(
                        batch("request:atomic-conflict", second, conflicting),
                        ingested_at_ms=2_001,
                    )
                self.assertEqual(gateway.status()["events"], 1)
                with self.assertRaises(KeyError):
                    gateway.event(second.event_id)
                self.assertEqual(
                    gateway.quarantine()[-1]["reason"], "event_identity_conflict"
                )

    def test_same_request_id_with_different_batch_is_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.initialize(directory) as gateway:
                first = event(sequence=1, native_id="event:host:1")
                gateway.ingest(batch("request:identity", first), ingested_at_ms=2_000)
                changed = event(
                    sequence=1,
                    native_id="event:host:1",
                    attributes={"nativeState": "different"},
                )
                with self.assertRaisesRegex(
                    ObservationCorruption, "request_identity_conflict"
                ):
                    gateway.ingest(
                        batch("request:identity", changed), ingested_at_ms=2_001
                    )
                self.assertEqual(gateway.status()["events"], 1)

    def test_privacy_and_mapping_rejections_do_not_store_payload_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.initialize(directory) as gateway:
                original = batch(
                    "request:privacy",
                    event(sequence=1, native_id="event:host:1"),
                ).to_dict()
                private = copy.deepcopy(original)
                private["events"][0]["attributes"] = {
                    "accessToken": "must-not-be-retained"
                }
                with self.assertRaises(ObservationPolicyRejected):
                    gateway.ingest_dict(private, ingested_at_ms=2_000)
                quarantine = gateway.quarantine()
                self.assertEqual(quarantine[-1]["reason"], "privacy_rejected")
                serialized = json.dumps(quarantine)
                self.assertNotIn("must-not-be-retained", serialized)
                self.assertEqual(gateway.status()["events"], 0)

                unsupported = event(
                    sequence=1,
                    native_id="event:host:unsupported",
                    mapping_version="host-observation-v2",
                )
                with self.assertRaises(ObservationMappingRejected):
                    gateway.ingest(
                        batch("request:mapping", unsupported), ingested_at_ms=2_001
                    )
                self.assertEqual(
                    gateway.quarantine()[-1]["reason"],
                    "mapping_version_not_allowlisted",
                )

    def test_catalog_digest_is_rebuild_deterministic_across_ingest_times(self) -> None:
        host_task = event(
            sequence=1,
            native_id="host-event:task",
            relations=(
                ObservationRelation(
                    "belongs_to", "ordivon.host.task", "task:fixture"
                ),
            ),
        )
        harness_run = event(
            producer=PRODUCERS[1],
            stream_id="harness-stream:fixture",
            sequence=1,
            native_id="harness-event:run",
            mapping_version="harness-observation-v1",
            relations=(
                ObservationRelation(
                    "requested_by", "ordivon.host.task", "task:fixture"
                ),
                ObservationRelation(
                    "belongs_to", "ordivon.harness.run", "harness-run:fixture"
                ),
            ),
        )
        runtime_job = event(
            producer=PRODUCERS[2],
            stream_id="runtime-job:fixture",
            sequence=1,
            native_id="runtime-event:job",
            mapping_version="runtime-observation-v1",
            relations=(
                ObservationRelation(
                    "requested_by",
                    "ordivon.harness.run",
                    "harness-run:fixture",
                ),
                ObservationRelation(
                    "belongs_to", "ordivon.runtime.job", "runtime-job:fixture"
                ),
            ),
        )
        batches = (
            batch("request:host", host_task),
            batch("request:harness", harness_run),
            batch("request:runtime", runtime_job),
        )
        digests: list[str] = []
        for run in range(2):
            with tempfile.TemporaryDirectory() as directory:
                with self.initialize(directory) as gateway:
                    for index, value in enumerate(batches):
                        gateway.ingest(
                            value,
                            ingested_at_ms=10_000 * (run + 1) + index,
                        )
                    digests.append(gateway.catalog_digest)
                    self.assertEqual(len(gateway.catalog_snapshot()["events"]), 3)
                    self.assertTrue(gateway.doctor(full=True)["healthy"])
        self.assertEqual(digests[0], digests[1])


if __name__ == "__main__":
    unittest.main()
