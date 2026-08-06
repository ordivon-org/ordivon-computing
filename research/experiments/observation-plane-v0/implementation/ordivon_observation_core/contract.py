from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable

from .canonical import (
    JsonScalar,
    JsonValue,
    bounded_text,
    canonical_bytes,
    canonical_digest,
    digest,
    exact_object,
    namespaced_kind,
    scalar_map,
)

ENVELOPE_SCHEMA_VERSION = 1
ENVELOPE_KIND = "ordivon.observation-envelope"
BATCH_KIND = "ordivon.observation-ingest-batch"
ACK_KIND = "ordivon.observation-ingest-acknowledgement"
CANONICALIZATION = "ordivon-evidence-json-v1"
MAX_BATCH_EVENTS = 256

RELATION_TYPES = frozenset(
    {
        "belongs_to",
        "requested_by",
        "executes",
        "observes",
        "produced",
        "references",
        "proposes_for",
        "verifies",
        "accepted_by",
        "reconciles",
        "caused_by",
        "derived_from",
        "evaluates",
        "linked_to",
    }
)
PRIVACY_CLASSES = frozenset(
    {
        "public_metadata",
        "private_metadata",
        "private_content_ref",
        "restricted_content_ref",
        "secret_forbidden",
    }
)
LOCATOR_CLASSES = frozenset(
    {"owner_store", "owner_cas", "runtime_artifact", "external_reference"}
)

_HEX_32 = re.compile(r"^[0-9a-f]{32}$")
_HEX_16 = re.compile(r"^[0-9a-f]{16}$")


class ObservationContractError(ValueError):
    pass


class ObservationPrivacyError(ObservationContractError):
    pass


def _contract_error(error: ValueError) -> ObservationContractError:
    if isinstance(error, ObservationContractError):
        return error
    return ObservationContractError(str(error))


def _int(value: Any, *, label: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ObservationContractError(f"{label} must be an integer >= {minimum}")
    return value


def _optional_revision(value: Any) -> int | str | None:
    if value is None:
        return None
    if type(value) is int:
        if value < 0:
            raise ObservationContractError("native revision must be non-negative")
        return value
    try:
        return bounded_text(value, label="native revision", max_bytes=256)
    except ValueError as error:
        raise _contract_error(error) from error


def event_identity(source: "ObservationSource") -> str:
    return canonical_digest(
        {
            "projectId": source.project_id,
            "componentId": source.component_id,
            "instanceId": source.instance_id,
            "streamId": source.stream_id,
            "nativeId": source.native_id,
        }
    )


@dataclass(frozen=True, slots=True)
class ObservationSource:
    project_id: str
    component_id: str
    instance_id: str
    stream_id: str
    sequence: int
    native_kind: str
    native_id: str
    native_digest: str
    mapping_version: str
    native_revision: int | str | None = None

    def __post_init__(self) -> None:
        try:
            namespaced_kind(self.project_id, label="source projectId")
            bounded_text(self.component_id, label="source componentId", max_bytes=256)
            bounded_text(self.instance_id, label="source instanceId", max_bytes=512)
            bounded_text(self.stream_id, label="source streamId", max_bytes=1_024)
            namespaced_kind(self.native_kind, label="source nativeKind")
            bounded_text(self.native_id, label="source nativeId", max_bytes=1_024)
            digest(self.native_digest, label="source nativeDigest")
            bounded_text(self.mapping_version, label="source mappingVersion", max_bytes=128)
            _int(self.sequence, label="source sequence", minimum=1)
            _optional_revision(self.native_revision)
        except ValueError as error:
            raise _contract_error(error) from error

    def to_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "projectId": self.project_id,
            "componentId": self.component_id,
            "instanceId": self.instance_id,
            "streamId": self.stream_id,
            "sequence": self.sequence,
            "nativeKind": self.native_kind,
            "nativeId": self.native_id,
            "nativeDigest": self.native_digest,
            "mappingVersion": self.mapping_version,
        }
        if self.native_revision is not None:
            value["nativeRevision"] = self.native_revision
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationSource":
        try:
            item = exact_object(
                value,
                required={
                    "projectId",
                    "componentId",
                    "instanceId",
                    "streamId",
                    "sequence",
                    "nativeKind",
                    "nativeId",
                    "nativeDigest",
                    "mappingVersion",
                },
                optional={"nativeRevision"},
                label="ObservationSource",
            )
            return cls(
                project_id=item["projectId"],
                component_id=item["componentId"],
                instance_id=item["instanceId"],
                stream_id=item["streamId"],
                sequence=item["sequence"],
                native_kind=item["nativeKind"],
                native_id=item["nativeId"],
                native_revision=_optional_revision(item.get("nativeRevision")),
                native_digest=item["nativeDigest"],
                mapping_version=item["mappingVersion"],
            )
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True, order=True)
class ObservationRelation:
    relation_type: str
    target_kind: str
    target_id: str
    target_digest: str | None = None

    def __post_init__(self) -> None:
        try:
            if self.relation_type not in RELATION_TYPES:
                raise ObservationContractError(
                    f"unsupported relation type: {self.relation_type}"
                )
            namespaced_kind(self.target_kind, label="relation targetKind")
            bounded_text(self.target_id, label="relation targetId", max_bytes=1_024)
            if self.target_digest is not None:
                digest(self.target_digest, label="relation targetDigest")
        except ValueError as error:
            raise _contract_error(error) from error

    def to_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "relationType": self.relation_type,
            "targetKind": self.target_kind,
            "targetId": self.target_id,
        }
        if self.target_digest is not None:
            value["targetDigest"] = self.target_digest
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationRelation":
        try:
            item = exact_object(
                value,
                required={"relationType", "targetKind", "targetId"},
                optional={"targetDigest"},
                label="ObservationRelation",
            )
            return cls(
                relation_type=item["relationType"],
                target_kind=item["targetKind"],
                target_id=item["targetId"],
                target_digest=item.get("targetDigest"),
            )
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True, order=True)
class ObservationTraceLink:
    trace_id: str
    span_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.trace_id, str) or _HEX_32.fullmatch(self.trace_id) is None:
            raise ObservationContractError("trace link traceId must be 32 lowercase hex")
        if self.trace_id == "0" * 32:
            raise ObservationContractError("trace link traceId cannot be zero")
        if not isinstance(self.span_id, str) or _HEX_16.fullmatch(self.span_id) is None:
            raise ObservationContractError("trace link spanId must be 16 lowercase hex")
        if self.span_id == "0" * 16:
            raise ObservationContractError("trace link spanId cannot be zero")

    def to_dict(self) -> dict[str, JsonValue]:
        return {"traceId": self.trace_id, "spanId": self.span_id}

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationTraceLink":
        try:
            item = exact_object(
                value,
                required={"traceId", "spanId"},
                label="ObservationTraceLink",
            )
            return cls(trace_id=item["traceId"], span_id=item["spanId"])
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True)
class ObservationTrace:
    trace_id: str | None = None
    span_id: str | None = None
    parent_span_id: str | None = None
    links: tuple[ObservationTraceLink, ...] = ()

    def __post_init__(self) -> None:
        if (self.trace_id is None) != (self.span_id is None):
            raise ObservationContractError(
                "traceId and spanId must be present or absent together"
            )
        if self.parent_span_id is not None and self.trace_id is None:
            raise ObservationContractError(
                "parentSpanId requires traceId and spanId"
            )
        if self.trace_id is not None and self.span_id is not None:
            ObservationTraceLink(self.trace_id, self.span_id)
        if self.parent_span_id is not None:
            ObservationTraceLink(self.trace_id, self.parent_span_id)
        if tuple(sorted(self.links)) != self.links or len(set(self.links)) != len(self.links):
            raise ObservationContractError("trace links must be sorted and unique")

    def to_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {"links": [item.to_dict() for item in self.links]}
        if self.trace_id is not None:
            value["traceId"] = self.trace_id
        if self.span_id is not None:
            value["spanId"] = self.span_id
        if self.parent_span_id is not None:
            value["parentSpanId"] = self.parent_span_id
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationTrace":
        try:
            item = exact_object(
                value,
                required={"links"},
                optional={"traceId", "spanId", "parentSpanId"},
                label="ObservationTrace",
            )
            links = item["links"]
            if not isinstance(links, list):
                raise ObservationContractError("ObservationTrace links must be an array")
            return cls(
                trace_id=item.get("traceId"),
                span_id=item.get("spanId"),
                parent_span_id=item.get("parentSpanId"),
                links=tuple(ObservationTraceLink.from_dict(entry) for entry in links),
            )
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True)
class ObservationPrivacy:
    privacy_class: str
    policy_id: str
    contains_inline_content: bool = False

    def __post_init__(self) -> None:
        if self.privacy_class not in PRIVACY_CLASSES:
            raise ObservationPrivacyError(
                f"unsupported privacy class: {self.privacy_class}"
            )
        try:
            bounded_text(self.policy_id, label="privacy policyId", max_bytes=256)
        except ValueError as error:
            raise ObservationPrivacyError(str(error)) from error
        if type(self.contains_inline_content) is not bool:
            raise ObservationPrivacyError("containsInlineContent must be boolean")
        if self.privacy_class == "secret_forbidden":
            raise ObservationPrivacyError("secret_forbidden observations are rejected")
        if self.contains_inline_content:
            raise ObservationPrivacyError(
                "Observation Minimum Core accepts metadata and references only"
            )

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "class": self.privacy_class,
            "policyId": self.policy_id,
            "containsInlineContent": self.contains_inline_content,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationPrivacy":
        try:
            item = exact_object(
                value,
                required={"class", "policyId", "containsInlineContent"},
                label="ObservationPrivacy",
            )
            return cls(
                privacy_class=item["class"],
                policy_id=item["policyId"],
                contains_inline_content=item["containsInlineContent"],
            )
        except ObservationPrivacyError:
            raise
        except ValueError as error:
            raise ObservationPrivacyError(str(error)) from error


@dataclass(frozen=True, slots=True)
class ObservationPayloadRef:
    owner: str
    kind: str
    digest_value: str
    locator_class: str
    native_id: str | None = None

    def __post_init__(self) -> None:
        try:
            namespaced_kind(self.owner, label="payloadRef owner")
            namespaced_kind(self.kind, label="payloadRef kind")
            digest(self.digest_value, label="payloadRef digest")
            if self.locator_class not in LOCATOR_CLASSES:
                raise ObservationContractError(
                    f"unsupported payload locator class: {self.locator_class}"
                )
            if self.native_id is not None:
                bounded_text(self.native_id, label="payloadRef nativeId", max_bytes=1_024)
        except ValueError as error:
            raise _contract_error(error) from error

    def to_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "owner": self.owner,
            "kind": self.kind,
            "digest": self.digest_value,
            "locatorClass": self.locator_class,
        }
        if self.native_id is not None:
            value["nativeId"] = self.native_id
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationPayloadRef":
        try:
            item = exact_object(
                value,
                required={"owner", "kind", "digest", "locatorClass"},
                optional={"nativeId"},
                label="ObservationPayloadRef",
            )
            return cls(
                owner=item["owner"],
                kind=item["kind"],
                native_id=item.get("nativeId"),
                digest_value=item["digest"],
                locator_class=item["locatorClass"],
            )
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True)
class ObservationMeasurement:
    value: int | float
    unit: str

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise ObservationContractError("measurement value must be numeric")
        if isinstance(self.value, float) and (self.value != self.value or abs(self.value) == float("inf")):
            raise ObservationContractError("measurement value must be finite")
        try:
            bounded_text(self.unit, label="measurement unit", max_bytes=64)
        except ValueError as error:
            raise _contract_error(error) from error

    def to_dict(self) -> dict[str, JsonValue]:
        return {"value": self.value, "unit": self.unit}

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationMeasurement":
        try:
            item = exact_object(
                value,
                required={"value", "unit"},
                label="ObservationMeasurement",
            )
            return cls(value=item["value"], unit=item["unit"])
        except ValueError as error:
            raise _contract_error(error) from error


def _measurements(value: Any) -> dict[str, ObservationMeasurement]:
    if not isinstance(value, dict) or len(value) > 128:
        raise ObservationContractError("measurements must be a bounded object")
    result: dict[str, ObservationMeasurement] = {}
    for key, item in value.items():
        try:
            checked = bounded_text(key, label="measurement key", max_bytes=128)
        except ValueError as error:
            raise _contract_error(error) from error
        result[checked] = ObservationMeasurement.from_dict(item)
    return result


@dataclass(frozen=True, slots=True)
class ObservationEnvelope:
    event_id: str
    occurred_at_ms: int
    source: ObservationSource
    relations: tuple[ObservationRelation, ...]
    attributes: dict[str, JsonScalar | list[JsonScalar]]
    measurements: dict[str, ObservationMeasurement]
    privacy: ObservationPrivacy
    integrity_digest: str
    trace: ObservationTrace | None = None
    outcome: dict[str, JsonScalar | list[JsonScalar]] | None = None
    payload_ref: ObservationPayloadRef | None = None

    def __post_init__(self) -> None:
        try:
            digest(self.event_id, label="Observation eventId")
            digest(self.integrity_digest, label="Observation payloadDigest")
        except ValueError as error:
            raise _contract_error(error) from error
        _int(self.occurred_at_ms, label="occurredAtMs")
        if self.event_id != event_identity(self.source):
            raise ObservationContractError("Observation eventId differs from native identity")
        if tuple(sorted(self.relations)) != self.relations:
            raise ObservationContractError("Observation relations must be sorted")
        if len(set(self.relations)) != len(self.relations):
            raise ObservationContractError("Observation relations must be unique")
        try:
            checked_attributes = scalar_map(self.attributes, label="attributes")
        except ValueError as error:
            raise ObservationPrivacyError(str(error)) from error
        if checked_attributes != self.attributes:
            raise ObservationContractError("Observation attributes differ after validation")
        if self.outcome is not None:
            try:
                checked_outcome = scalar_map(
                    self.outcome, label="outcome", max_fields=32, max_bytes=4_096
                )
            except ValueError as error:
                raise ObservationPrivacyError(str(error)) from error
            if checked_outcome != self.outcome:
                raise ObservationContractError("Observation outcome differs after validation")
        if self.privacy.privacy_class in {
            "private_content_ref",
            "restricted_content_ref",
        } and self.payload_ref is None:
            raise ObservationPrivacyError(
                f"{self.privacy.privacy_class} requires payloadRef"
            )
        expected = canonical_digest(self._payload_dict())
        if self.integrity_digest != expected:
            raise ObservationContractError("Observation integrity differs")

    @classmethod
    def build(
        cls,
        *,
        occurred_at_ms: int,
        source: ObservationSource,
        relations: Iterable[ObservationRelation] = (),
        attributes: dict[str, JsonScalar | list[JsonScalar]] | None = None,
        measurements: dict[str, ObservationMeasurement] | None = None,
        privacy: ObservationPrivacy,
        trace: ObservationTrace | None = None,
        outcome: dict[str, JsonScalar | list[JsonScalar]] | None = None,
        payload_ref: ObservationPayloadRef | None = None,
    ) -> "ObservationEnvelope":
        relation_tuple = tuple(sorted(relations))
        provisional = cls.__new__(cls)
        object.__setattr__(provisional, "event_id", event_identity(source))
        object.__setattr__(provisional, "occurred_at_ms", occurred_at_ms)
        object.__setattr__(provisional, "source", source)
        object.__setattr__(provisional, "relations", relation_tuple)
        object.__setattr__(provisional, "attributes", attributes or {})
        object.__setattr__(provisional, "measurements", measurements or {})
        object.__setattr__(provisional, "privacy", privacy)
        object.__setattr__(provisional, "trace", trace)
        object.__setattr__(provisional, "outcome", outcome)
        object.__setattr__(provisional, "payload_ref", payload_ref)
        object.__setattr__(provisional, "integrity_digest", "sha256:" + "0" * 64)
        payload_digest = canonical_digest(provisional._payload_dict())
        return cls(
            event_id=event_identity(source),
            occurred_at_ms=occurred_at_ms,
            source=source,
            relations=relation_tuple,
            attributes=attributes or {},
            measurements=measurements or {},
            privacy=privacy,
            trace=trace,
            outcome=outcome,
            payload_ref=payload_ref,
            integrity_digest=payload_digest,
        )

    def _payload_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "schemaVersion": ENVELOPE_SCHEMA_VERSION,
            "kind": ENVELOPE_KIND,
            "eventId": self.event_id,
            "occurredAtMs": self.occurred_at_ms,
            "source": self.source.to_dict(),
            "relations": [item.to_dict() for item in self.relations],
            "attributes": self.attributes,
            "measurements": {
                key: item.to_dict() for key, item in sorted(self.measurements.items())
            },
            "privacy": self.privacy.to_dict(),
        }
        if self.trace is not None:
            value["trace"] = self.trace.to_dict()
        if self.outcome is not None:
            value["outcome"] = self.outcome
        if self.payload_ref is not None:
            value["payloadRef"] = self.payload_ref.to_dict()
        return value

    @property
    def canonical_bytes(self) -> bytes:
        return canonical_bytes(self.to_dict())

    @property
    def canonical_digest(self) -> str:
        return self.integrity_digest

    def to_dict(self) -> dict[str, JsonValue]:
        value = self._payload_dict()
        value["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": CANONICALIZATION,
            "payloadDigest": self.integrity_digest,
        }
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationEnvelope":
        try:
            item = exact_object(
                value,
                required={
                    "schemaVersion",
                    "kind",
                    "eventId",
                    "occurredAtMs",
                    "source",
                    "relations",
                    "attributes",
                    "measurements",
                    "privacy",
                    "integrity",
                },
                optional={"trace", "outcome", "payloadRef"},
                label="ObservationEnvelope",
            )
            if item["schemaVersion"] != ENVELOPE_SCHEMA_VERSION or item["kind"] != ENVELOPE_KIND:
                raise ObservationContractError("unsupported ObservationEnvelope version or kind")
            relations = item["relations"]
            if not isinstance(relations, list):
                raise ObservationContractError("ObservationEnvelope relations must be an array")
            integrity = exact_object(
                item["integrity"],
                required={"algorithm", "canonicalization", "payloadDigest"},
                label="ObservationIntegrity",
            )
            if integrity["algorithm"] != "sha256" or integrity["canonicalization"] != CANONICALIZATION:
                raise ObservationContractError("unsupported Observation integrity")
            try:
                attributes = scalar_map(item["attributes"], label="attributes")
                outcome = (
                    None
                    if "outcome" not in item
                    else scalar_map(
                        item["outcome"],
                        label="outcome",
                        max_fields=32,
                        max_bytes=4_096,
                    )
                )
            except ValueError as error:
                raise ObservationPrivacyError(str(error)) from error
            return cls(
                event_id=item["eventId"],
                occurred_at_ms=item["occurredAtMs"],
                source=ObservationSource.from_dict(item["source"]),
                relations=tuple(ObservationRelation.from_dict(entry) for entry in relations),
                attributes=attributes,
                measurements=_measurements(item["measurements"]),
                privacy=ObservationPrivacy.from_dict(item["privacy"]),
                trace=(
                    None
                    if "trace" not in item
                    else ObservationTrace.from_dict(item["trace"])
                ),
                outcome=outcome,
                payload_ref=(
                    None
                    if "payloadRef" not in item
                    else ObservationPayloadRef.from_dict(item["payloadRef"])
                ),
                integrity_digest=integrity["payloadDigest"],
            )
        except ObservationContractError:
            raise
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True)
class ObservationProducerIdentity:
    project_id: str
    component_id: str
    instance_id: str

    def __post_init__(self) -> None:
        try:
            namespaced_kind(self.project_id, label="producer projectId")
            bounded_text(self.component_id, label="producer componentId", max_bytes=256)
            bounded_text(self.instance_id, label="producer instanceId", max_bytes=512)
        except ValueError as error:
            raise _contract_error(error) from error

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "projectId": self.project_id,
            "componentId": self.component_id,
            "instanceId": self.instance_id,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationProducerIdentity":
        try:
            item = exact_object(
                value,
                required={"projectId", "componentId", "instanceId"},
                label="ObservationProducerIdentity",
            )
            return cls(
                project_id=item["projectId"],
                component_id=item["componentId"],
                instance_id=item["instanceId"],
            )
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True)
class ObservationBatch:
    request_id: str
    producer_identity: ObservationProducerIdentity
    stream_id: str
    first_sequence: int
    last_sequence: int
    events: tuple[ObservationEnvelope, ...]
    batch_digest: str

    def __post_init__(self) -> None:
        try:
            bounded_text(self.request_id, label="batch requestId", max_bytes=512)
            bounded_text(self.stream_id, label="batch streamId", max_bytes=1_024)
            digest(self.batch_digest, label="batchDigest")
        except ValueError as error:
            raise _contract_error(error) from error
        _int(self.first_sequence, label="batch firstSequence", minimum=1)
        _int(self.last_sequence, label="batch lastSequence", minimum=1)
        if not self.events or len(self.events) > MAX_BATCH_EVENTS:
            raise ObservationContractError(
                f"Observation batch must contain 1..{MAX_BATCH_EVENTS} events"
            )
        if self.last_sequence - self.first_sequence + 1 != len(self.events):
            raise ObservationContractError("Observation batch range differs from event count")
        expected_sequences = tuple(range(self.first_sequence, self.last_sequence + 1))
        actual_sequences = tuple(event.source.sequence for event in self.events)
        if actual_sequences != expected_sequences:
            raise ObservationContractError("Observation batch sequences are not contiguous")
        for event in self.events:
            source = event.source
            if (
                source.project_id != self.producer_identity.project_id
                or source.component_id != self.producer_identity.component_id
                or source.instance_id != self.producer_identity.instance_id
                or source.stream_id != self.stream_id
            ):
                raise ObservationContractError(
                    "Observation batch mixes producer instances or source streams"
                )
        if self.batch_digest != canonical_digest(self._payload_dict()):
            raise ObservationContractError("Observation batch digest differs")

    @classmethod
    def build(
        cls,
        *,
        request_id: str,
        events: Iterable[ObservationEnvelope],
    ) -> "ObservationBatch":
        event_tuple = tuple(events)
        if not event_tuple:
            raise ObservationContractError("Observation batch requires events")
        first = event_tuple[0].source
        producer = ObservationProducerIdentity(
            first.project_id, first.component_id, first.instance_id
        )
        provisional = cls.__new__(cls)
        object.__setattr__(provisional, "request_id", request_id)
        object.__setattr__(provisional, "producer_identity", producer)
        object.__setattr__(provisional, "stream_id", first.stream_id)
        object.__setattr__(provisional, "first_sequence", first.sequence)
        object.__setattr__(provisional, "last_sequence", event_tuple[-1].source.sequence)
        object.__setattr__(provisional, "events", event_tuple)
        object.__setattr__(provisional, "batch_digest", "sha256:" + "0" * 64)
        value = canonical_digest(provisional._payload_dict())
        return cls(
            request_id=request_id,
            producer_identity=producer,
            stream_id=first.stream_id,
            first_sequence=first.sequence,
            last_sequence=event_tuple[-1].source.sequence,
            events=event_tuple,
            batch_digest=value,
        )

    def _payload_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": 1,
            "kind": BATCH_KIND,
            "requestId": self.request_id,
            "producerIdentity": self.producer_identity.to_dict(),
            "streamId": self.stream_id,
            "firstSequence": self.first_sequence,
            "lastSequence": self.last_sequence,
            "events": [event.to_dict() for event in self.events],
        }

    def to_dict(self) -> dict[str, JsonValue]:
        value = self._payload_dict()
        value["batchDigest"] = self.batch_digest
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationBatch":
        try:
            item = exact_object(
                value,
                required={
                    "schemaVersion",
                    "kind",
                    "requestId",
                    "producerIdentity",
                    "streamId",
                    "firstSequence",
                    "lastSequence",
                    "events",
                    "batchDigest",
                },
                label="ObservationBatch",
            )
            if item["schemaVersion"] != 1 or item["kind"] != BATCH_KIND:
                raise ObservationContractError("unsupported ObservationBatch version or kind")
            events = item["events"]
            if not isinstance(events, list):
                raise ObservationContractError("ObservationBatch events must be an array")
            return cls(
                request_id=item["requestId"],
                producer_identity=ObservationProducerIdentity.from_dict(
                    item["producerIdentity"]
                ),
                stream_id=item["streamId"],
                first_sequence=item["firstSequence"],
                last_sequence=item["lastSequence"],
                events=tuple(ObservationEnvelope.from_dict(event) for event in events),
                batch_digest=item["batchDigest"],
            )
        except ObservationContractError:
            raise
        except ValueError as error:
            raise _contract_error(error) from error


@dataclass(frozen=True, slots=True)
class ObservationIngestAcknowledgement:
    request_id: str
    producer_identity: ObservationProducerIdentity
    stream_id: str
    first_sequence: int
    last_sequence: int
    accepted: int
    duplicates: int
    rejected: int
    last_contiguous_sequence: int
    status: str
    ingested_at_ms: int
    gateway_receipt_digest: str

    def __post_init__(self) -> None:
        try:
            bounded_text(self.request_id, label="ack requestId", max_bytes=512)
            bounded_text(self.stream_id, label="ack streamId", max_bytes=1_024)
            digest(self.gateway_receipt_digest, label="gatewayReceiptDigest")
        except ValueError as error:
            raise _contract_error(error) from error
        for label, value in (
            ("firstSequence", self.first_sequence),
            ("lastSequence", self.last_sequence),
            ("accepted", self.accepted),
            ("duplicates", self.duplicates),
            ("rejected", self.rejected),
            ("lastContiguousSequence", self.last_contiguous_sequence),
            ("ingestedAtMs", self.ingested_at_ms),
        ):
            _int(value, label=f"ack {label}")
        if self.status not in {"committed", "rejected"}:
            raise ObservationContractError("unsupported acknowledgement status")
        if self.gateway_receipt_digest != canonical_digest(self._payload_dict()):
            raise ObservationContractError("gateway receipt digest differs")

    @classmethod
    def build(
        cls,
        *,
        batch: ObservationBatch,
        accepted: int,
        duplicates: int,
        rejected: int,
        last_contiguous_sequence: int,
        status: str,
        ingested_at_ms: int,
    ) -> "ObservationIngestAcknowledgement":
        provisional = cls.__new__(cls)
        values = {
            "request_id": batch.request_id,
            "producer_identity": batch.producer_identity,
            "stream_id": batch.stream_id,
            "first_sequence": batch.first_sequence,
            "last_sequence": batch.last_sequence,
            "accepted": accepted,
            "duplicates": duplicates,
            "rejected": rejected,
            "last_contiguous_sequence": last_contiguous_sequence,
            "status": status,
            "ingested_at_ms": ingested_at_ms,
            "gateway_receipt_digest": "sha256:" + "0" * 64,
        }
        for key, value in values.items():
            object.__setattr__(provisional, key, value)
        receipt_digest = canonical_digest(provisional._payload_dict())
        values["gateway_receipt_digest"] = receipt_digest
        return cls(**values)

    def _payload_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": 1,
            "kind": ACK_KIND,
            "requestId": self.request_id,
            "producerIdentity": self.producer_identity.to_dict(),
            "streamId": self.stream_id,
            "firstSequence": self.first_sequence,
            "lastSequence": self.last_sequence,
            "accepted": self.accepted,
            "duplicates": self.duplicates,
            "rejected": self.rejected,
            "lastContiguousSequence": self.last_contiguous_sequence,
            "status": self.status,
            "ingestedAtMs": self.ingested_at_ms,
        }

    def to_dict(self) -> dict[str, JsonValue]:
        value = self._payload_dict()
        value["gatewayReceiptDigest"] = self.gateway_receipt_digest
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationIngestAcknowledgement":
        try:
            item = exact_object(
                value,
                required={
                    "schemaVersion",
                    "kind",
                    "requestId",
                    "producerIdentity",
                    "streamId",
                    "firstSequence",
                    "lastSequence",
                    "accepted",
                    "duplicates",
                    "rejected",
                    "lastContiguousSequence",
                    "status",
                    "ingestedAtMs",
                    "gatewayReceiptDigest",
                },
                label="ObservationIngestAcknowledgement",
            )
            if item["schemaVersion"] != 1 or item["kind"] != ACK_KIND:
                raise ObservationContractError(
                    "unsupported Observation acknowledgement version or kind"
                )
            return cls(
                request_id=item["requestId"],
                producer_identity=ObservationProducerIdentity.from_dict(
                    item["producerIdentity"]
                ),
                stream_id=item["streamId"],
                first_sequence=item["firstSequence"],
                last_sequence=item["lastSequence"],
                accepted=item["accepted"],
                duplicates=item["duplicates"],
                rejected=item["rejected"],
                last_contiguous_sequence=item["lastContiguousSequence"],
                status=item["status"],
                ingested_at_ms=item["ingestedAtMs"],
                gateway_receipt_digest=item["gatewayReceiptDigest"],
            )
        except ObservationContractError:
            raise
        except ValueError as error:
            raise _contract_error(error) from error


__all__ = [
    "ACK_KIND",
    "BATCH_KIND",
    "CANONICALIZATION",
    "ENVELOPE_KIND",
    "ENVELOPE_SCHEMA_VERSION",
    "LOCATOR_CLASSES",
    "MAX_BATCH_EVENTS",
    "ObservationBatch",
    "ObservationContractError",
    "ObservationEnvelope",
    "ObservationIngestAcknowledgement",
    "ObservationMeasurement",
    "ObservationPayloadRef",
    "ObservationPrivacy",
    "ObservationPrivacyError",
    "ObservationProducerIdentity",
    "ObservationRelation",
    "ObservationSource",
    "ObservationTrace",
    "ObservationTraceLink",
    "PRIVACY_CLASSES",
    "RELATION_TYPES",
    "event_identity",
]
