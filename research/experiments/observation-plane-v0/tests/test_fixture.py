from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from ordivon_observation_core import (  # noqa: E402
    ObservationBatch,
    ObservationProducerIdentity,
    SQLiteObservationGateway,
    canonical_digest,
)
from ordivon_observation_core.fixtures import (  # noqa: E402
    MAPPING_VERSIONS,
    PRODUCERS,
    three_owner_batches,
)

FIXTURE = ROOT / "fixtures" / "three-owner-trajectory-v1.json"


class ThreeOwnerFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_fixture_identity_integrity_and_no_payload_content(self) -> None:
        self.assertEqual(
            self.value["kind"], "ordivon.observation-three-owner-fixture"
        )
        payload = dict(self.value)
        integrity = payload.pop("integrity")
        self.assertEqual(integrity["payloadDigest"], canonical_digest(payload))
        serialized = json.dumps(self.value, sort_keys=True).lower()
        for forbidden in (
            "raw_prompt",
            "model_output",
            "tool_payload",
            "stdout",
            "stderr",
            "access_token",
            "password",
            "chain_of_thought",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_frozen_fixture_matches_the_contract_builder(self) -> None:
        self.assertEqual(
            self.value["producerAllowlist"],
            [producer.to_dict() for producer in PRODUCERS],
        )
        self.assertEqual(
            self.value["mappingVersions"],
            [
                {
                    "projectId": project,
                    "componentId": component,
                    "mappingVersion": mapping,
                }
                for project, component, mapping in MAPPING_VERSIONS
            ],
        )
        self.assertEqual(
            self.value["batches"],
            [batch.to_dict() for batch in three_owner_batches()],
        )

    def test_fixture_rebuilds_the_expected_catalog(self) -> None:
        producers = tuple(
            ObservationProducerIdentity.from_dict(value)
            for value in self.value["producerAllowlist"]
        )
        mappings = tuple(
            (
                value["projectId"],
                value["componentId"],
                value["mappingVersion"],
            )
            for value in self.value["mappingVersions"]
        )
        batches = tuple(
            ObservationBatch.from_dict(value) for value in self.value["batches"]
        )
        digests: list[str] = []
        for iteration in range(2):
            with tempfile.TemporaryDirectory() as directory:
                with SQLiteObservationGateway.initialize(
                    Path(directory) / "gateway",
                    gateway_instance_id=f"gateway:fixture:{iteration}",
                    producer_allowlist=producers,
                    mapping_versions=mappings,
                    created_at_ms=100 + iteration,
                ) as gateway:
                    for index, value in enumerate(batches):
                        gateway.ingest(
                            value,
                            ingested_at_ms=1_000 * (iteration + 1) + index,
                        )
                    digests.append(gateway.catalog_digest)
                    self.assertEqual(
                        gateway.status()["events"],
                        self.value["expected"]["eventCount"],
                    )
                    self.assertEqual(
                        len(gateway.catalog_snapshot()["streams"]),
                        self.value["expected"]["streamCount"],
                    )
                    self.assertTrue(gateway.doctor(full=True)["healthy"])
        self.assertEqual(digests[0], digests[1])
        self.assertEqual(digests[0], self.value["expected"]["catalogDigest"])


if __name__ == "__main__":
    unittest.main()
