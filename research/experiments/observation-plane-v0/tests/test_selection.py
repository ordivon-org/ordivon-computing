from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from ordivon_observation_core import (
    ObservationSelectionError,
    ObservationSelectionManifest,
    SQLiteObservationGateway,
    TrajectoryQuerySpec,
    select_cross_owner_trajectory,
)
from ordivon_observation_core.fixtures import (
    MAPPING_VERSIONS,
    PRODUCERS,
    three_owner_batches,
)


TASK_ID = "task:three-owner-fixture"
QUERY = TrajectoryQuerySpec(
    query_id="trajectory-query:three-owner-fixture",
    anchor_kind="ordivon.host.task",
    anchor_id=TASK_ID,
    artifact_coverage="owner_native_only",
)


def build_gateway(root: Path, batches: tuple, order: tuple[int, ...]) -> SQLiteObservationGateway:
    gateway = SQLiteObservationGateway.initialize(
        root,
        gateway_instance_id="observation-gateway:selection-test",
        producer_allowlist=PRODUCERS,
        mapping_versions=MAPPING_VERSIONS,
        created_at_ms=100,
    )
    for offset, index in enumerate(order):
        gateway.ingest(batches[index], ingested_at_ms=200 + offset)
    return gateway


class ObservationSelectionTests(unittest.TestCase):
    def test_complete_three_owner_selection_is_stable_and_not_trial_validity(self) -> None:
        batches = three_owner_batches()
        with tempfile.TemporaryDirectory() as directory:
            with build_gateway(Path(directory) / "gateway", batches, (0, 1, 2)) as gateway:
                selection = select_cross_owner_trajectory(gateway, QUERY)
                self.assertTrue(selection.completeness["complete"])
                self.assertFalse(selection.completeness["trialValidityInferred"])
                self.assertEqual(len(selection.selected_events), 13)
                self.assertEqual(
                    {entry["projectId"] for entry in selection.producer_mapping_versions},
                    {"ordivon-host", "ordivon-harness", "ordivon-runtime"},
                )
                self.assertTrue(selection.privacy["metadataOnly"])
                self.assertFalse(selection.privacy["payloadBytesCopied"])
                self.assertIn("owner-native only", selection.limitations[0])
                decoded = ObservationSelectionManifest.from_dict(selection.to_dict())
                self.assertEqual(decoded, selection)

    def test_ingest_order_and_gateway_rebuild_preserve_selection_digest(self) -> None:
        batches = three_owner_batches()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with build_gateway(root / "first", batches, (0, 1, 2)) as first:
                first_selection = select_cross_owner_trajectory(first, QUERY)
            with build_gateway(root / "second", batches, (2, 0, 1)) as second:
                second_selection = select_cross_owner_trajectory(second, QUERY)
            self.assertEqual(first_selection.catalog_digest, second_selection.catalog_digest)
            self.assertEqual(first_selection.selection_digest, second_selection.selection_digest)
            self.assertEqual(first_selection.selected_events, second_selection.selected_events)
            self.assertEqual(
                first_selection.source_stream_heads,
                second_selection.source_stream_heads,
            )

    def test_missing_runtime_owner_is_explicitly_incomplete(self) -> None:
        batches = three_owner_batches()
        with tempfile.TemporaryDirectory() as directory:
            with build_gateway(Path(directory) / "gateway", batches, (0, 1)) as gateway:
                selection = select_cross_owner_trajectory(gateway, QUERY)
                self.assertFalse(selection.completeness["complete"])
                claims = {
                    item["claimId"]: item["status"]
                    for item in selection.completeness["claims"]
                }
                self.assertEqual(claims["runtime_job_linked"], "missing")
                self.assertEqual(claims["three_owner_coverage"], "missing")
                self.assertFalse(selection.completeness["trialValidityInferred"])

    def test_unrelated_anchor_has_no_selection(self) -> None:
        batches = three_owner_batches()
        with tempfile.TemporaryDirectory() as directory:
            with build_gateway(Path(directory) / "gateway", batches, (0, 1, 2)) as gateway:
                with self.assertRaisesRegex(ObservationSelectionError, "no Observation Events"):
                    select_cross_owner_trajectory(
                        gateway,
                        TrajectoryQuerySpec(
                            query_id="trajectory-query:missing",
                            anchor_kind="ordivon.host.task",
                            anchor_id="task:missing",
                        ),
                    )

    def test_manifest_tampering_is_rejected(self) -> None:
        batches = three_owner_batches()
        with tempfile.TemporaryDirectory() as directory:
            with build_gateway(Path(directory) / "gateway", batches, (0, 1, 2)) as gateway:
                selection = select_cross_owner_trajectory(gateway, QUERY)
            value = copy.deepcopy(selection.to_dict())
            value["completeness"]["complete"] = False
            with self.assertRaisesRegex(ObservationSelectionError, "selection digest differs"):
                ObservationSelectionManifest.from_dict(value)

    def test_serialized_manifest_contains_no_copied_payload_bytes(self) -> None:
        batches = three_owner_batches()
        with tempfile.TemporaryDirectory() as directory:
            with build_gateway(Path(directory) / "gateway", batches, (0, 1, 2)) as gateway:
                selection = select_cross_owner_trajectory(gateway, QUERY)
            value = selection.to_dict()
            encoded = json.dumps(value, sort_keys=True)
            for event in value["selectedEvents"]:
                self.assertEqual(set(event), {"eventId", "envelopeDigest", "source"})
                self.assertNotIn("payloadRef", event)
                self.assertNotIn("attributes", event)
                self.assertNotIn("measurements", event)
                self.assertNotIn("outcome", event)
            self.assertNotIn("private reasoning", encoded.lower())


if __name__ == "__main__":
    unittest.main()
