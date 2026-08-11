from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ordivon_observation_core import (
    ObservationBatch,
    ObservationEnvelope,
    ObservationPrivacy,
    ObservationProducerIdentity,
    ObservationRelation,
    ObservationSource,
    SQLiteObservationGateway,
    TrajectoryQuerySpec,
    select_cross_owner_trajectory,
)

DIGEST = "sha256:" + "a" * 64


class MinimalSelectionTests(unittest.TestCase):
    def test_task_anchor_selection_is_non_authoritative_when_incomplete(self) -> None:
        producer = ObservationProducerIdentity(
            "ordivon-host", "host-journal", "host:minimal"
        )
        source = ObservationSource(
            project_id=producer.project_id,
            component_id=producer.component_id,
            instance_id=producer.instance_id,
            stream_id="host-journal:minimal",
            sequence=1,
            native_kind="ordivon.host.task-created",
            native_id="event:minimal:1",
            native_revision=1,
            native_digest=DIGEST,
            mapping_version="host-observation-v1",
        )
        event = ObservationEnvelope.build(
            occurred_at_ms=1,
            source=source,
            relations=(
                ObservationRelation(
                    "belongs_to", "ordivon.host.task", "task:minimal"
                ),
            ),
            privacy=ObservationPrivacy("private_metadata", "test-policy"),
        )
        batch = ObservationBatch.build(request_id="request:minimal", events=(event,))
        with tempfile.TemporaryDirectory() as raw:
            with SQLiteObservationGateway.initialize(
                Path(raw) / "gateway",
                gateway_instance_id="gateway:minimal",
                producer_allowlist=(producer,),
                mapping_versions=((producer.project_id, producer.component_id, "host-observation-v1"),),
                created_at_ms=1,
            ) as gateway:
                gateway.ingest(batch, ingested_at_ms=2)
                selection = select_cross_owner_trajectory(
                    gateway,
                    TrajectoryQuerySpec(
                        query_id="query:minimal",
                        anchor_kind="ordivon.host.task",
                        anchor_id="task:minimal",
                    ),
                )
        self.assertEqual(len(selection.selected_events), 1)
        self.assertFalse(selection.completeness["complete"])
        self.assertFalse(selection.completeness["trialValidityInferred"])
        self.assertIn(
            "Selection is incomplete and cannot satisfy a formal Trial evidence gate",
            selection.limitations,
        )


if __name__ == "__main__":
    unittest.main()
