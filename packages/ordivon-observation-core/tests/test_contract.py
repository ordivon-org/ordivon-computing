from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "src"
sys.path.insert(0, str(IMPLEMENTATION))

from ordivon_observation_core import (  # noqa: E402
    ObservationBatch,
    ObservationContractError,
    ObservationEnvelope,
    ObservationMeasurement,
    ObservationPayloadRef,
    ObservationPrivacy,
    ObservationPrivacyError,
    ObservationRelation,
    ObservationSource,
    ObservationTrace,
)

DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64


def source(*, sequence: int = 1, native_id: str = "event:host:1") -> ObservationSource:
    return ObservationSource(
        project_id="ordivon-host",
        component_id="host-journal",
        instance_id="host-instance:fixture",
        stream_id="host-journal:fixture",
        sequence=sequence,
        native_kind="ordivon.host.task-event",
        native_id=native_id,
        native_revision=sequence,
        native_digest=DIGEST_A,
        mapping_version="host-observation-v1",
    )


def envelope(*, sequence: int = 1, native_id: str = "event:host:1") -> ObservationEnvelope:
    return ObservationEnvelope.build(
        occurred_at_ms=1_000 + sequence,
        source=source(sequence=sequence, native_id=native_id),
        relations=(
            ObservationRelation(
                "belongs_to",
                "ordivon.host.task",
                "task:fixture",
                DIGEST_B,
            ),
        ),
        attributes={"taskState": "ready", "attemptCount": sequence},
        measurements={
            "duration": ObservationMeasurement(value=sequence, unit="ms")
        },
        privacy=ObservationPrivacy("private_metadata", "observation-metadata-v1"),
    )


class ObservationContractTests(unittest.TestCase):
    def test_envelope_roundtrip_and_canonical_digest(self) -> None:
        original = envelope()
        decoded = ObservationEnvelope.from_dict(original.to_dict())
        self.assertEqual(decoded, original)
        self.assertEqual(decoded.canonical_bytes, original.canonical_bytes)
        self.assertNotIn("exportedAtMs", original.to_dict())

    def test_event_identity_is_native_and_mapping_stable(self) -> None:
        first = envelope()
        second = ObservationEnvelope.build(
            occurred_at_ms=2_000,
            source=source(),
            attributes={"taskState": "running"},
            privacy=ObservationPrivacy("private_metadata", "observation-metadata-v1"),
        )
        self.assertEqual(first.event_id, second.event_id)
        self.assertNotEqual(first.canonical_digest, second.canonical_digest)

    def test_unknown_fields_and_integrity_drift_are_rejected(self) -> None:
        value = envelope().to_dict()
        value["unexpected"] = True
        with self.assertRaisesRegex(ObservationContractError, "fields differ"):
            ObservationEnvelope.from_dict(value)

        value = envelope().to_dict()
        value["attributes"]["taskState"] = "completed"
        with self.assertRaisesRegex(ObservationContractError, "integrity"):
            ObservationEnvelope.from_dict(value)

    def test_relation_and_privacy_vocabularies_are_closed(self) -> None:
        with self.assertRaisesRegex(ObservationContractError, "relation"):
            ObservationRelation("invented", "ordivon.host.task", "task:fixture")
        with self.assertRaises(ObservationPrivacyError):
            ObservationPrivacy("secret_forbidden", "observation-metadata-v1")
        with self.assertRaises(ObservationPrivacyError):
            ObservationPrivacy(
                "private_metadata",
                "observation-metadata-v1",
                contains_inline_content=True,
            )

    def test_content_reference_privacy_requires_payload_ref(self) -> None:
        with self.assertRaisesRegex(ObservationPrivacyError, "payloadRef"):
            ObservationEnvelope.build(
                occurred_at_ms=1_000,
                source=source(),
                privacy=ObservationPrivacy(
                    "private_content_ref", "observation-content-ref-v1"
                ),
            )
        value = ObservationEnvelope.build(
            occurred_at_ms=1_000,
            source=source(),
            privacy=ObservationPrivacy(
                "private_content_ref", "observation-content-ref-v1"
            ),
            payload_ref=ObservationPayloadRef(
                owner="ordivon-host",
                kind="ordivon.host.object",
                native_id="object:fixture",
                digest_value=DIGEST_B,
                locator_class="owner_cas",
            ),
        )
        self.assertEqual(value.payload_ref.native_id, "object:fixture")

    def test_secret_like_and_raw_content_keys_are_rejected(self) -> None:
        for key in ("accessToken", "api_key", "password", "raw_prompt", "stdout"):
            with self.subTest(key=key), self.assertRaises(ObservationPrivacyError):
                ObservationEnvelope.build(
                    occurred_at_ms=1_000,
                    source=source(),
                    attributes={key: "redacted"},
                    privacy=ObservationPrivacy(
                        "private_metadata", "observation-metadata-v1"
                    ),
                )

    def test_trace_requires_a_complete_w3c_identity_pair(self) -> None:
        with self.assertRaisesRegex(ObservationContractError, "traceId and spanId"):
            ObservationTrace(trace_id="1" * 32)
        with self.assertRaisesRegex(ObservationContractError, "traceId and spanId"):
            ObservationTrace(span_id="2" * 16)
        with self.assertRaisesRegex(ObservationContractError, "parentSpanId"):
            ObservationTrace(parent_span_id="3" * 16)
        value = ObservationTrace(trace_id="1" * 32, span_id="2" * 16)
        self.assertEqual(value.trace_id, "1" * 32)

    def test_batch_roundtrip_and_range_strictness(self) -> None:
        batch = ObservationBatch.build(
            request_id="observation-request:host:1",
            events=(
                envelope(sequence=1, native_id="event:host:1"),
                envelope(sequence=2, native_id="event:host:2"),
            ),
        )
        self.assertEqual(ObservationBatch.from_dict(batch.to_dict()), batch)
        drifted = copy.deepcopy(batch.to_dict())
        drifted["lastSequence"] = 3
        with self.assertRaises(ObservationContractError):
            ObservationBatch.from_dict(drifted)


if __name__ == "__main__":
    unittest.main()
