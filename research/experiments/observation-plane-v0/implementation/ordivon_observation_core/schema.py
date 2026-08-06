from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contract import (
    ACK_KIND,
    BATCH_KIND,
    CANONICALIZATION,
    ENVELOPE_KIND,
    LOCATOR_CLASSES,
    MAX_BATCH_EVENTS,
    PRIVACY_CLASSES,
    RELATION_TYPES,
)
from .exporter import BUNDLE_KIND, CHECKPOINT_KIND
from .selection import ARTIFACT_COVERAGE_MODES, SELECTION_KIND

_DIGEST_PATTERN = r"^sha256:[0-9a-f]{64}$"
_KIND_PATTERN = r"^[a-z][a-z0-9]*(?:[.-][a-z0-9][a-z0-9_-]*)+$"


def _strict_object(
    properties: dict[str, Any],
    *,
    required: list[str],
) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
    }


def observation_envelope_schema() -> dict[str, Any]:
    scalar = {"type": ["string", "number", "integer", "boolean", "null"]}
    scalar_or_array = {
        "oneOf": [
            scalar,
            {"type": "array", "maxItems": 32, "items": scalar},
        ]
    }
    digest = {"type": "string", "pattern": _DIGEST_PATTERN}
    namespaced_kind = {"type": "string", "pattern": _KIND_PATTERN}
    source = _strict_object(
        {
            "projectId": namespaced_kind,
            "componentId": {"type": "string", "minLength": 1, "maxLength": 256},
            "instanceId": {"type": "string", "minLength": 1, "maxLength": 512},
            "streamId": {"type": "string", "minLength": 1, "maxLength": 1024},
            "sequence": {"type": "integer", "minimum": 1},
            "nativeKind": namespaced_kind,
            "nativeId": {"type": "string", "minLength": 1, "maxLength": 1024},
            "nativeRevision": {"type": ["integer", "string"]},
            "nativeDigest": digest,
            "mappingVersion": {"type": "string", "minLength": 1, "maxLength": 128},
        },
        required=[
            "projectId",
            "componentId",
            "instanceId",
            "streamId",
            "sequence",
            "nativeKind",
            "nativeId",
            "nativeDigest",
            "mappingVersion",
        ],
    )
    relation = _strict_object(
        {
            "relationType": {"enum": sorted(RELATION_TYPES)},
            "targetKind": namespaced_kind,
            "targetId": {"type": "string", "minLength": 1, "maxLength": 1024},
            "targetDigest": digest,
        },
        required=["relationType", "targetKind", "targetId"],
    )
    trace_link = _strict_object(
        {
            "traceId": {"type": "string", "pattern": r"^[0-9a-f]{32}$"},
            "spanId": {"type": "string", "pattern": r"^[0-9a-f]{16}$"},
        },
        required=["traceId", "spanId"],
    )
    trace = _strict_object(
        {
            "traceId": {"type": "string", "pattern": r"^[0-9a-f]{32}$"},
            "spanId": {"type": "string", "pattern": r"^[0-9a-f]{16}$"},
            "parentSpanId": {"type": "string", "pattern": r"^[0-9a-f]{16}$"},
            "links": {"type": "array", "items": trace_link, "maxItems": 128},
        },
        required=["links"],
    )
    privacy = _strict_object(
        {
            "class": {"enum": sorted(PRIVACY_CLASSES - {"secret_forbidden"})},
            "policyId": {"type": "string", "minLength": 1, "maxLength": 256},
            "containsInlineContent": {"const": False},
        },
        required=["class", "policyId", "containsInlineContent"],
    )
    payload_ref = _strict_object(
        {
            "owner": namespaced_kind,
            "kind": namespaced_kind,
            "nativeId": {"type": "string", "minLength": 1, "maxLength": 1024},
            "digest": digest,
            "locatorClass": {"enum": sorted(LOCATOR_CLASSES)},
        },
        required=["owner", "kind", "digest", "locatorClass"],
    )
    measurement = _strict_object(
        {
            "value": {"type": ["number", "integer"]},
            "unit": {"type": "string", "minLength": 1, "maxLength": 64},
        },
        required=["value", "unit"],
    )
    integrity = _strict_object(
        {
            "algorithm": {"const": "sha256"},
            "canonicalization": {"const": CANONICALIZATION},
            "payloadDigest": digest,
        },
        required=["algorithm", "canonicalization", "payloadDigest"],
    )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://ordivon.com/schemas/observation-envelope-v1.json",
        "title": "Ordivon Observation Envelope v1",
        **_strict_object(
            {
                "schemaVersion": {"const": 1},
                "kind": {"const": ENVELOPE_KIND},
                "eventId": digest,
                "occurredAtMs": {"type": "integer", "minimum": 0},
                "source": source,
                "relations": {
                    "type": "array",
                    "items": relation,
                    "maxItems": 256,
                },
                "trace": trace,
                "attributes": {
                    "type": "object",
                    "maxProperties": 128,
                    "additionalProperties": scalar_or_array,
                },
                "measurements": {
                    "type": "object",
                    "maxProperties": 128,
                    "additionalProperties": measurement,
                },
                "outcome": {
                    "type": "object",
                    "maxProperties": 32,
                    "additionalProperties": scalar_or_array,
                },
                "privacy": privacy,
                "payloadRef": payload_ref,
                "integrity": integrity,
            },
            required=[
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
            ],
        ),
    }


def observation_batch_schema() -> dict[str, Any]:
    producer = _strict_object(
        {
            "projectId": {"type": "string", "pattern": _KIND_PATTERN},
            "componentId": {"type": "string", "minLength": 1, "maxLength": 256},
            "instanceId": {"type": "string", "minLength": 1, "maxLength": 512},
        },
        required=["projectId", "componentId", "instanceId"],
    )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://ordivon.com/schemas/observation-ingest-batch-v1.json",
        "title": "Ordivon Observation Ingest Batch v1",
        **_strict_object(
            {
                "schemaVersion": {"const": 1},
                "kind": {"const": BATCH_KIND},
                "requestId": {"type": "string", "minLength": 1, "maxLength": 512},
                "producerIdentity": producer,
                "streamId": {"type": "string", "minLength": 1, "maxLength": 1024},
                "firstSequence": {"type": "integer", "minimum": 1},
                "lastSequence": {"type": "integer", "minimum": 1},
                "events": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": MAX_BATCH_EVENTS,
                    "items": observation_envelope_schema(),
                },
                "batchDigest": {"type": "string", "pattern": _DIGEST_PATTERN},
            },
            required=[
                "schemaVersion",
                "kind",
                "requestId",
                "producerIdentity",
                "streamId",
                "firstSequence",
                "lastSequence",
                "events",
                "batchDigest",
            ],
        ),
    }


def observation_acknowledgement_schema() -> dict[str, Any]:
    producer = _strict_object(
        {
            "projectId": {"type": "string", "pattern": _KIND_PATTERN},
            "componentId": {"type": "string", "minLength": 1, "maxLength": 256},
            "instanceId": {"type": "string", "minLength": 1, "maxLength": 512},
        },
        required=["projectId", "componentId", "instanceId"],
    )
    properties: dict[str, Any] = {
        "schemaVersion": {"const": 1},
        "kind": {"const": ACK_KIND},
        "requestId": {"type": "string", "minLength": 1, "maxLength": 512},
        "producerIdentity": producer,
        "streamId": {"type": "string", "minLength": 1, "maxLength": 1024},
        "firstSequence": {"type": "integer", "minimum": 0},
        "lastSequence": {"type": "integer", "minimum": 0},
        "accepted": {"type": "integer", "minimum": 0},
        "duplicates": {"type": "integer", "minimum": 0},
        "rejected": {"type": "integer", "minimum": 0},
        "lastContiguousSequence": {"type": "integer", "minimum": 0},
        "status": {"enum": ["committed", "rejected"]},
        "ingestedAtMs": {"type": "integer", "minimum": 0},
        "gatewayReceiptDigest": {"type": "string", "pattern": _DIGEST_PATTERN},
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://ordivon.com/schemas/observation-ingest-acknowledgement-v1.json",
        "title": "Ordivon Observation Ingest Acknowledgement v1",
        **_strict_object(properties, required=list(properties)),
    }


def observation_export_checkpoint_schema() -> dict[str, Any]:
    producer = _strict_object(
        {
            "projectId": {"type": "string", "pattern": _KIND_PATTERN},
            "componentId": {"type": "string", "minLength": 1, "maxLength": 256},
            "instanceId": {"type": "string", "minLength": 1, "maxLength": 512},
        },
        required=["projectId", "componentId", "instanceId"],
    )
    integrity = _strict_object(
        {
            "algorithm": {"const": "sha256"},
            "canonicalization": {"const": "ordivon-evidence-json-v1"},
            "payloadDigest": {"type": "string", "pattern": _DIGEST_PATTERN},
        },
        required=["algorithm", "canonicalization", "payloadDigest"],
    )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://ordivon.com/schemas/observation-export-checkpoint-v1.json",
        "title": "Ordivon Observation Export Checkpoint v1",
        **_strict_object(
            {
                "schemaVersion": {"const": 1},
                "kind": {"const": CHECKPOINT_KIND},
                "producerIdentity": producer,
                "mappingVersion": {"type": "string", "minLength": 1, "maxLength": 128},
                "streams": {
                    "type": "object",
                    "maxProperties": 1000000,
                    "additionalProperties": {"type": "integer", "minimum": 0},
                },
                "updatedAtMs": {"type": "integer", "minimum": 0},
                "integrity": integrity,
            },
            required=[
                "schemaVersion",
                "kind",
                "producerIdentity",
                "mappingVersion",
                "streams",
                "updatedAtMs",
                "integrity",
            ],
        ),
    }


def observation_export_bundle_schema() -> dict[str, Any]:
    producer = _strict_object(
        {
            "projectId": {"type": "string", "pattern": _KIND_PATTERN},
            "componentId": {"type": "string", "minLength": 1, "maxLength": 256},
            "instanceId": {"type": "string", "minLength": 1, "maxLength": 512},
        },
        required=["projectId", "componentId", "instanceId"],
    )
    integrity = _strict_object(
        {
            "algorithm": {"const": "sha256"},
            "canonicalization": {"const": "ordivon-evidence-json-v1"},
            "payloadDigest": {"type": "string", "pattern": _DIGEST_PATTERN},
        },
        required=["algorithm", "canonicalization", "payloadDigest"],
    )
    revision = {"type": "string", "pattern": r"^[0-9a-f]{40}$"}
    digest = {"type": "string", "pattern": _DIGEST_PATTERN}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://ordivon.com/schemas/observation-export-bundle-v1.json",
        "title": "Ordivon Observation Export Bundle v1",
        **_strict_object(
            {
                "schemaVersion": {"const": 1},
                "kind": {"const": BUNDLE_KIND},
                "producerIdentity": producer,
                "mappingVersion": {"type": "string", "minLength": 1, "maxLength": 128},
                "ownerRevision": revision,
                "exporterRevision": revision,
                "exportedAtMs": {"type": "integer", "minimum": 0},
                "checkpointBeforeDigest": digest,
                "checkpointAfterDigest": digest,
                "batches": {
                    "type": "array",
                    "items": observation_batch_schema(),
                },
                "integrity": integrity,
            },
            required=[
                "schemaVersion",
                "kind",
                "producerIdentity",
                "mappingVersion",
                "ownerRevision",
                "exporterRevision",
                "exportedAtMs",
                "checkpointBeforeDigest",
                "checkpointAfterDigest",
                "batches",
                "integrity",
            ],
        ),
    }



def observation_selection_manifest_schema() -> dict[str, Any]:
    digest = {"type": "string", "pattern": _DIGEST_PATTERN}
    namespaced_kind = {"type": "string", "pattern": _KIND_PATTERN}
    source = _strict_object(
        {
            "projectId": namespaced_kind,
            "componentId": {"type": "string", "minLength": 1, "maxLength": 256},
            "instanceId": {"type": "string", "minLength": 1, "maxLength": 512},
            "streamId": {"type": "string", "minLength": 1, "maxLength": 1024},
            "sequence": {"type": "integer", "minimum": 1},
            "nativeKind": namespaced_kind,
            "nativeId": {"type": "string", "minLength": 1, "maxLength": 1024},
            "mappingVersion": {"type": "string", "minLength": 1, "maxLength": 128},
        },
        required=[
            "projectId",
            "componentId",
            "instanceId",
            "streamId",
            "sequence",
            "nativeKind",
            "nativeId",
            "mappingVersion",
        ],
    )
    selected_event = _strict_object(
        {"eventId": digest, "envelopeDigest": digest, "source": source},
        required=["eventId", "envelopeDigest", "source"],
    )
    stream_head = _strict_object(
        {
            "projectId": namespaced_kind,
            "componentId": {"type": "string", "minLength": 1},
            "instanceId": {"type": "string", "minLength": 1},
            "streamId": {"type": "string", "minLength": 1},
            "lastContiguousSequence": {"type": "integer", "minimum": 0},
            "highestSeenSequence": {"type": "integer", "minimum": 0},
            "completenessState": {"enum": ["complete", "gap", "quarantined"]},
        },
        required=[
            "projectId",
            "componentId",
            "instanceId",
            "streamId",
            "lastContiguousSequence",
            "highestSeenSequence",
            "completenessState",
        ],
    )
    mapping = _strict_object(
        {
            "projectId": namespaced_kind,
            "componentId": {"type": "string", "minLength": 1},
            "mappingVersion": {"type": "string", "minLength": 1},
        },
        required=["projectId", "componentId", "mappingVersion"],
    )
    claim = _strict_object(
        {
            "claimId": {"type": "string", "minLength": 1},
            "status": {"enum": ["satisfied", "missing"]},
        },
        required=["claimId", "status"],
    )
    query = _strict_object(
        {
            "queryId": {"type": "string", "minLength": 1},
            "queryVersion": {"const": "cross-owner-task-trajectory-v1"},
            "anchor": _strict_object(
                {
                    "targetKind": {"const": "ordivon.host.task"},
                    "targetId": {"type": "string", "minLength": 1},
                },
                required=["targetKind", "targetId"],
            ),
            "artifactCoverage": {"enum": sorted(ARTIFACT_COVERAGE_MODES)},
        },
        required=["queryId", "queryVersion", "anchor", "artifactCoverage"],
    )
    integrity = _strict_object(
        {
            "algorithm": {"const": "sha256"},
            "canonicalization": {"const": "ordivon-evidence-json-v1"},
            "payloadDigest": digest,
        },
        required=["algorithm", "canonicalization", "payloadDigest"],
    )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://ordivon.com/schemas/observation-selection-manifest-v1.json",
        "title": "Ordivon Observation Selection Manifest v1",
        **_strict_object(
            {
                "schemaVersion": {"const": 1},
                "kind": {"const": SELECTION_KIND},
                "query": query,
                "catalogDigest": digest,
                "selectedEvents": {
                    "type": "array",
                    "minItems": 1,
                    "items": selected_event,
                },
                "sourceStreamHeads": {
                    "type": "array",
                    "minItems": 1,
                    "items": stream_head,
                },
                "producerMappingVersions": {
                    "type": "array",
                    "minItems": 1,
                    "items": mapping,
                },
                "completeness": _strict_object(
                    {
                        "complete": {"type": "boolean"},
                        "claims": {"type": "array", "items": claim},
                        "trialValidityInferred": {"const": False},
                    },
                    required=["complete", "claims", "trialValidityInferred"],
                ),
                "privacy": _strict_object(
                    {
                        "metadataOnly": {"const": True},
                        "payloadBytesCopied": {"const": False},
                        "privacyClasses": {
                            "type": "array",
                            "items": {"type": "string", "minLength": 1},
                        },
                        "secretForbiddenPresent": {"const": False},
                    },
                    required=[
                        "metadataOnly",
                        "payloadBytesCopied",
                        "privacyClasses",
                        "secretForbiddenPresent",
                    ],
                ),
                "limitations": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                },
                "selectionDigest": digest,
                "integrity": integrity,
            },
            required=[
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
            ],
        ),
    }

def schemas() -> dict[str, dict[str, Any]]:
    return {
        "observation-envelope-v1.schema.json": observation_envelope_schema(),
        "observation-ingest-batch-v1.schema.json": observation_batch_schema(),
        "observation-ingest-acknowledgement-v1.schema.json": observation_acknowledgement_schema(),
        "observation-export-checkpoint-v1.schema.json": observation_export_checkpoint_schema(),
        "observation-export-bundle-v1.schema.json": observation_export_bundle_schema(),
        "observation-selection-manifest-v1.schema.json": observation_selection_manifest_schema(),
    }


def write_schemas(root: str | Path) -> None:
    destination = Path(root)
    destination.mkdir(parents=True, exist_ok=True)
    for name, value in schemas().items():
        (destination / name).write_text(
            json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )


__all__ = [
    "observation_acknowledgement_schema",
    "observation_batch_schema",
    "observation_envelope_schema",
    "observation_export_bundle_schema",
    "observation_export_checkpoint_schema",
    "observation_selection_manifest_schema",
    "schemas",
    "write_schemas",
]
