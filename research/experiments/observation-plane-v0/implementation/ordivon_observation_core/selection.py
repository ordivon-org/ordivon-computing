from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .canonical import (
    JsonValue,
    bounded_text,
    canonical_bytes,
    canonical_digest,
    digest,
    exact_object,
    namespaced_kind,
)
from .gateway import SQLiteObservationGateway

SELECTION_KIND = "ordivon.observation-selection-manifest"
SELECTION_SCHEMA_VERSION = 1
QUERY_VERSION = "cross-owner-task-trajectory-v1"
INDEPENDENT_HARNESS_RUNTIME_QUERY_VERSION = "independent-harness-runtime-trajectory-v1"
ARTIFACT_COVERAGE_MODES = frozenset(
    {"owner_native_only", "observation_append_only"}
)

_CLOSURE_TARGET_KINDS = frozenset(
    {
        "ordivon.host.task",
        "ordivon.host.task-attempt",
        "ordivon.host.external-request",
        "ordivon.host.verification",
        "ordivon.harness.run",
        "ordivon.harness.tool-call",
        "ordivon.harness.completion-proposal",
        "ordivon.runtime.client-request",
        "ordivon.runtime.workspace",
        "ordivon.runtime.job",
        "ordivon.runtime.attempt",
    }
)
_REQUIRED_PROJECTS = frozenset(
    {"ordivon-host", "ordivon-harness", "ordivon-runtime"}
)
_INDEPENDENT_REQUIRED_PROJECTS = frozenset({"ordivon-harness", "ordivon-runtime"})
_HOST_VERIFICATION_KINDS = frozenset(
    {
        "ordivon.host.verification.recorded",
        "ordivon.host.verification.accepted",
        "ordivon.host.verification-recorded",
        "ordivon.host.verification-accepted",
    }
)
_HOST_OUTCOME_KINDS = frozenset(
    {
        "ordivon.host.task.outcome-recorded",
        "ordivon.host.task.result-applied",
        "ordivon.host.task-outcome-recorded",
        "ordivon.host.task-result-applied",
    }
)
_HARNESS_COMPLETION_KINDS = frozenset(
    {
        "ordivon.harness.completion.proposed",
        "ordivon.harness.completion.decided",
        "ordivon.harness.completion-proposed",
        "ordivon.harness.completion-decided",
        "ordivon.harness.harness.completion-proposed",
        "ordivon.harness.harness.run-completed",
    }
)
_HOST_EXTERNAL_COMPLETION_KINDS = frozenset(
    {"ordivon.host.external.completion-collected"}
)
_HARNESS_TERMINAL_KINDS = frozenset(
    {
        "ordivon.harness.harness.run-stopped",
        "ordivon.harness.harness.run-completed",
        "ordivon.harness.run-stopped",
        "ordivon.harness.run-completed",
    }
)


class ObservationSelectionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TrajectoryQuerySpec:
    query_id: str
    anchor_kind: str
    anchor_id: str
    artifact_coverage: str = "owner_native_only"
    query_version: str = QUERY_VERSION

    def __post_init__(self) -> None:
        try:
            bounded_text(self.query_id, label="query ID", max_bytes=256)
            bounded_text(self.query_version, label="query version", max_bytes=128)
            namespaced_kind(self.anchor_kind, label="query anchor kind")
            bounded_text(self.anchor_id, label="query anchor ID", max_bytes=1_024)
        except ValueError as error:
            raise ObservationSelectionError(str(error)) from error
        if self.query_version == QUERY_VERSION:
            if self.anchor_kind != "ordivon.host.task":
                raise ObservationSelectionError(
                    "cross-owner trajectory v1 requires a Host Task anchor"
                )
        elif self.query_version == INDEPENDENT_HARNESS_RUNTIME_QUERY_VERSION:
            if self.anchor_kind != "ordivon.harness.run":
                raise ObservationSelectionError(
                    "independent Harness-Runtime trajectory v1 requires a Harness Run anchor"
                )
        else:
            raise ObservationSelectionError(
                f"unsupported trajectory query version: {self.query_version}"
            )
        if self.artifact_coverage not in ARTIFACT_COVERAGE_MODES:
            raise ObservationSelectionError(
                f"unsupported Artifact coverage: {self.artifact_coverage}"
            )

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "queryId": self.query_id,
            "queryVersion": self.query_version,
            "anchor": {
                "targetKind": self.anchor_kind,
                "targetId": self.anchor_id,
            },
            "artifactCoverage": self.artifact_coverage,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "TrajectoryQuerySpec":
        try:
            item = exact_object(
                value,
                required={
                    "queryId",
                    "queryVersion",
                    "anchor",
                    "artifactCoverage",
                },
                label="TrajectoryQuerySpec",
            )
            anchor = exact_object(
                item["anchor"],
                required={"targetKind", "targetId"},
                label="TrajectoryQuerySpec anchor",
            )
            return cls(
                query_id=item["queryId"],
                query_version=item["queryVersion"],
                anchor_kind=anchor["targetKind"],
                anchor_id=anchor["targetId"],
                artifact_coverage=item["artifactCoverage"],
            )
        except ValueError as error:
            if isinstance(error, ObservationSelectionError):
                raise
            raise ObservationSelectionError(str(error)) from error


@dataclass(frozen=True, slots=True)
class ObservationSelectionManifest:
    query: TrajectoryQuerySpec
    catalog_digest: str
    selected_events: tuple[dict[str, JsonValue], ...]
    source_stream_heads: tuple[dict[str, JsonValue], ...]
    producer_mapping_versions: tuple[dict[str, JsonValue], ...]
    completeness: dict[str, JsonValue]
    privacy: dict[str, JsonValue]
    limitations: tuple[str, ...]
    selection_digest: str
    integrity_digest: str

    def __post_init__(self) -> None:
        try:
            digest(self.catalog_digest, label="selection catalog digest")
            digest(self.selection_digest, label="selection digest")
            digest(self.integrity_digest, label="selection integrity digest")
        except ValueError as error:
            raise ObservationSelectionError(str(error)) from error
        if not self.selected_events:
            raise ObservationSelectionError("Observation selection cannot be empty")
        if tuple(sorted(self.selected_events, key=_event_sort_key)) != self.selected_events:
            raise ObservationSelectionError("selected Events must be sorted")
        event_ids = [str(item["eventId"]) for item in self.selected_events]
        if len(event_ids) != len(set(event_ids)):
            raise ObservationSelectionError("selected Events must be unique")
        if tuple(sorted(self.source_stream_heads, key=_stream_sort_key)) != self.source_stream_heads:
            raise ObservationSelectionError("source stream heads must be sorted")
        mappings = [
            (
                str(item["projectId"]),
                str(item["componentId"]),
                str(item["mappingVersion"]),
            )
            for item in self.producer_mapping_versions
        ]
        if mappings != sorted(set(mappings)):
            raise ObservationSelectionError(
                "producer mapping versions must be sorted and unique"
            )
        material = self._selection_material()
        if canonical_digest(material) != self.selection_digest:
            raise ObservationSelectionError("selection digest differs")
        if canonical_digest(self._payload_dict()) != self.integrity_digest:
            raise ObservationSelectionError("selection integrity differs")

    @classmethod
    def build(
        cls,
        *,
        query: TrajectoryQuerySpec,
        catalog_digest: str,
        selected_events: Iterable[dict[str, JsonValue]],
        source_stream_heads: Iterable[dict[str, JsonValue]],
        producer_mapping_versions: Iterable[dict[str, JsonValue]],
        completeness: dict[str, JsonValue],
        privacy: dict[str, JsonValue],
        limitations: Iterable[str] = (),
    ) -> "ObservationSelectionManifest":
        selected = tuple(sorted(selected_events, key=_event_sort_key))
        streams = tuple(sorted(source_stream_heads, key=_stream_sort_key))
        mappings = tuple(
            sorted(
                producer_mapping_versions,
                key=lambda item: (
                    str(item["projectId"]),
                    str(item["componentId"]),
                    str(item["mappingVersion"]),
                ),
            )
        )
        limits = tuple(sorted(set(limitations)))
        provisional = cls.__new__(cls)
        object.__setattr__(provisional, "query", query)
        object.__setattr__(provisional, "catalog_digest", catalog_digest)
        object.__setattr__(provisional, "selected_events", selected)
        object.__setattr__(provisional, "source_stream_heads", streams)
        object.__setattr__(provisional, "producer_mapping_versions", mappings)
        object.__setattr__(provisional, "completeness", completeness)
        object.__setattr__(provisional, "privacy", privacy)
        object.__setattr__(provisional, "limitations", limits)
        object.__setattr__(provisional, "selection_digest", "sha256:" + "0" * 64)
        object.__setattr__(provisional, "integrity_digest", "sha256:" + "0" * 64)
        selection_digest = canonical_digest(provisional._selection_material())
        object.__setattr__(provisional, "selection_digest", selection_digest)
        integrity_digest = canonical_digest(provisional._payload_dict())
        return cls(
            query=query,
            catalog_digest=catalog_digest,
            selected_events=selected,
            source_stream_heads=streams,
            producer_mapping_versions=mappings,
            completeness=completeness,
            privacy=privacy,
            limitations=limits,
            selection_digest=selection_digest,
            integrity_digest=integrity_digest,
        )

    def _selection_material(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": SELECTION_SCHEMA_VERSION,
            "kind": SELECTION_KIND,
            "query": self.query.to_dict(),
            "catalogDigest": self.catalog_digest,
            "selectedEvents": list(self.selected_events),
            "sourceStreamHeads": list(self.source_stream_heads),
            "producerMappingVersions": list(self.producer_mapping_versions),
            "completeness": self.completeness,
            "privacy": self.privacy,
            "limitations": list(self.limitations),
        }

    def _payload_dict(self) -> dict[str, JsonValue]:
        value = self._selection_material()
        value["selectionDigest"] = self.selection_digest
        return value

    @property
    def canonical_bytes(self) -> bytes:
        return canonical_bytes(self.to_dict())

    def to_dict(self) -> dict[str, JsonValue]:
        value = self._payload_dict()
        value["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": self.integrity_digest,
        }
        return value

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationSelectionManifest":
        try:
            item = exact_object(
                value,
                required={
                    "schemaVersion",
                    "kind",
                    "query",
                    "catalogDigest",
                    "selectedEvents",
                    "sourceStreamHeads",
                    "producerMappingVersions",
                    "completeness",
                    "privacy",
                    "limitations",
                    "selectionDigest",
                    "integrity",
                },
                label="ObservationSelectionManifest",
            )
            if (
                item["schemaVersion"] != SELECTION_SCHEMA_VERSION
                or item["kind"] != SELECTION_KIND
            ):
                raise ObservationSelectionError(
                    "unsupported ObservationSelectionManifest version or kind"
                )
            for field in (
                "selectedEvents",
                "sourceStreamHeads",
                "producerMappingVersions",
                "limitations",
            ):
                if not isinstance(item[field], list):
                    raise ObservationSelectionError(f"{field} must be an array")
            if not isinstance(item["completeness"], dict):
                raise ObservationSelectionError("completeness must be an object")
            if not isinstance(item["privacy"], dict):
                raise ObservationSelectionError("privacy must be an object")
            if any(not isinstance(entry, dict) for entry in item["selectedEvents"]):
                raise ObservationSelectionError("selectedEvents entries must be objects")
            if any(not isinstance(entry, dict) for entry in item["sourceStreamHeads"]):
                raise ObservationSelectionError(
                    "sourceStreamHeads entries must be objects"
                )
            if any(
                not isinstance(entry, dict)
                for entry in item["producerMappingVersions"]
            ):
                raise ObservationSelectionError(
                    "producerMappingVersions entries must be objects"
                )
            if any(not isinstance(entry, str) for entry in item["limitations"]):
                raise ObservationSelectionError("limitations entries must be strings")
            integrity = exact_object(
                item["integrity"],
                required={"algorithm", "canonicalization", "payloadDigest"},
                label="ObservationSelectionManifest integrity",
            )
            if (
                integrity["algorithm"] != "sha256"
                or integrity["canonicalization"] != "ordivon-evidence-json-v1"
            ):
                raise ObservationSelectionError(
                    "unsupported Observation Selection integrity"
                )
            return cls(
                query=TrajectoryQuerySpec.from_dict(item["query"]),
                catalog_digest=item["catalogDigest"],
                selected_events=tuple(item["selectedEvents"]),
                source_stream_heads=tuple(item["sourceStreamHeads"]),
                producer_mapping_versions=tuple(item["producerMappingVersions"]),
                completeness=dict(item["completeness"]),
                privacy=dict(item["privacy"]),
                limitations=tuple(item["limitations"]),
                selection_digest=item["selectionDigest"],
                integrity_digest=integrity["payloadDigest"],
            )
        except ValueError as error:
            if isinstance(error, ObservationSelectionError):
                raise
            raise ObservationSelectionError(str(error)) from error


def select_cross_owner_trajectory(
    gateway: SQLiteObservationGateway,
    query: TrajectoryQuerySpec,
) -> ObservationSelectionManifest:
    catalog = gateway.catalog_snapshot()
    events = tuple(catalog["events"])
    entities: set[tuple[str, str]] = {(query.anchor_kind, query.anchor_id)}
    selected_ids: set[str] = set()

    for _ in range(16):
        changed = False
        for event in events:
            relations = event["relations"]
            if not any(
                (str(relation["targetKind"]), str(relation["targetId"]))
                in entities
                for relation in relations
            ):
                continue
            event_id = str(event["eventId"])
            if event_id not in selected_ids:
                selected_ids.add(event_id)
                changed = True
            for relation in relations:
                target_kind = str(relation["targetKind"])
                target_id = str(relation["targetId"])
                if target_kind in _CLOSURE_TARGET_KINDS and (
                    target_kind,
                    target_id,
                ) not in entities:
                    entities.add((target_kind, target_id))
                    changed = True
        if not changed:
            break
    else:
        raise ObservationSelectionError("trajectory relation closure did not converge")

    selected_catalog_events = tuple(
        event for event in events if str(event["eventId"]) in selected_ids
    )
    if not selected_catalog_events:
        raise ObservationSelectionError(
            f"no Observation Events match {query.anchor_kind} {query.anchor_id}"
        )

    selected_events = tuple(
        {
            "eventId": event["eventId"],
            "envelopeDigest": event["envelopeDigest"],
            "source": event["source"],
        }
        for event in selected_catalog_events
    )
    stream_keys = {
        (
            str(event["source"]["projectId"]),
            str(event["source"]["componentId"]),
            str(event["source"]["instanceId"]),
            str(event["source"]["streamId"]),
        )
        for event in selected_catalog_events
    }
    stream_by_key = {
        (
            str(stream["projectId"]),
            str(stream["componentId"]),
            str(stream["instanceId"]),
            str(stream["streamId"]),
        ): stream
        for stream in catalog["streams"]
    }
    missing_streams = sorted(stream_keys - set(stream_by_key))
    if missing_streams:
        raise ObservationSelectionError(
            f"selected Events have no source stream head: {missing_streams}"
        )
    source_stream_heads = tuple(stream_by_key[key] for key in sorted(stream_keys))
    mappings = tuple(
        {
            "projectId": key[0],
            "componentId": key[1],
            "mappingVersion": key[2],
        }
        for key in sorted(
            {
                (
                    str(event["source"]["projectId"]),
                    str(event["source"]["componentId"]),
                    str(event["source"]["mappingVersion"]),
                )
                for event in selected_catalog_events
            }
        )
    )

    selected_projects = {
        str(event["source"]["projectId"]) for event in selected_catalog_events
    }
    native_kinds = {
        str(event["source"]["nativeKind"]) for event in selected_catalog_events
    }
    entity_kinds = {kind for kind, _ in entities}
    harness_run_ids = {
        identity for kind, identity in entities if kind == "ordivon.harness.run"
    }
    runtime_job_ids = {
        identity for kind, identity in entities if kind == "ordivon.runtime.job"
    }
    harness_event_run_ids = {
        str(relation["targetId"])
        for event in selected_catalog_events
        if event["source"]["projectId"] == "ordivon-harness"
        for relation in event["relations"]
        if relation["targetKind"] == "ordivon.harness.run"
    }
    runtime_event_job_ids = {
        str(relation["targetId"])
        for event in selected_catalog_events
        if event["source"]["projectId"] == "ordivon-runtime"
        for relation in event["relations"]
        if relation["targetKind"] == "ordivon.runtime.job"
    }
    anchor_present = any(
        relation["targetKind"] == query.anchor_kind
        and relation["targetId"] == query.anchor_id
        for event in selected_catalog_events
        for relation in event["relations"]
    )
    streams_complete = all(
        stream["completenessState"] == "complete"
        and stream["lastContiguousSequence"] == stream["highestSeenSequence"]
        for stream in source_stream_heads
    )
    if query.query_version == INDEPENDENT_HARNESS_RUNTIME_QUERY_VERSION:
        claim_values = {
            "harness_run_anchored": anchor_present,
            "harness_terminal_receipt_recorded": bool(
                native_kinds & _HARNESS_TERMINAL_KINDS
            ),
            "runtime_jobs_covered": (
                bool(runtime_job_ids) and runtime_job_ids <= runtime_event_job_ids
            ),
            "two_owner_coverage": selected_projects == _INDEPENDENT_REQUIRED_PROJECTS,
            "selected_streams_complete": streams_complete,
        }
    else:
        claim_values = {
            "host_task_anchored": anchor_present,
            "host_external_request_linked": (
                "ordivon.host.external-request" in entity_kinds
            ),
            "harness_run_linked": bool(harness_run_ids & harness_event_run_ids),
            "runtime_job_linked": bool(runtime_job_ids & runtime_event_job_ids),
            "harness_completion_proposed": bool(
                native_kinds
                & (_HARNESS_COMPLETION_KINDS | _HOST_EXTERNAL_COMPLETION_KINDS)
            ),
            "host_verification_recorded": bool(native_kinds & _HOST_VERIFICATION_KINDS),
            "host_task_outcome_recorded": bool(native_kinds & _HOST_OUTCOME_KINDS),
            "three_owner_coverage": selected_projects == _REQUIRED_PROJECTS,
            "selected_streams_complete": streams_complete,
        }
    claims = [
        {
            "claimId": claim_id,
            "status": "satisfied" if satisfied else "missing",
        }
        for claim_id, satisfied in sorted(claim_values.items())
    ]
    complete = all(claim_values.values())

    envelopes = tuple(gateway.event(str(event["eventId"])) for event in selected_events)
    privacy_classes = sorted({envelope.privacy.privacy_class for envelope in envelopes})
    privacy = {
        "metadataOnly": all(
            not envelope.privacy.contains_inline_content for envelope in envelopes
        ),
        "payloadBytesCopied": False,
        "privacyClasses": privacy_classes,
        "secretForbiddenPresent": False,
    }
    limitations = []
    if query.artifact_coverage == "owner_native_only":
        limitations.append(
            "Runtime Artifact traversal is owner-native only in " + query.query_version
        )
    if not complete:
        limitations.append(
            "Selection is incomplete and cannot satisfy a formal Trial evidence gate"
        )

    return ObservationSelectionManifest.build(
        query=query,
        catalog_digest=gateway.catalog_digest,
        selected_events=selected_events,
        source_stream_heads=source_stream_heads,
        producer_mapping_versions=mappings,
        completeness={
            "complete": complete,
            "claims": claims,
            "trialValidityInferred": False,
        },
        privacy=privacy,
        limitations=limitations,
    )


def _event_sort_key(item: dict[str, JsonValue]) -> tuple[Any, ...]:
    source = item["source"]
    if not isinstance(source, dict):
        raise ObservationSelectionError("selected Event source must be an object")
    return (
        source["projectId"],
        source["componentId"],
        source["instanceId"],
        source["streamId"],
        source["sequence"],
        item["eventId"],
    )


def _stream_sort_key(item: dict[str, JsonValue]) -> tuple[Any, ...]:
    return (
        item["projectId"],
        item["componentId"],
        item["instanceId"],
        item["streamId"],
    )


__all__ = [
    "ARTIFACT_COVERAGE_MODES",
    "QUERY_VERSION",
    "INDEPENDENT_HARNESS_RUNTIME_QUERY_VERSION",
    "SELECTION_KIND",
    "SELECTION_SCHEMA_VERSION",
    "ObservationSelectionError",
    "ObservationSelectionManifest",
    "TrajectoryQuerySpec",
    "select_cross_owner_trajectory",
]
