from __future__ import annotations

from .canonical import canonical_digest
from .contract import (
    ObservationBatch,
    ObservationEnvelope,
    ObservationPrivacy,
    ObservationProducerIdentity,
    ObservationRelation,
    ObservationSource,
)

HOST = ObservationProducerIdentity(
    "ordivon-host", "host-journal", "host:three-owner-fixture"
)
HARNESS = ObservationProducerIdentity(
    "ordivon-harness", "harness-journal", "harness:three-owner-fixture"
)
RUNTIME = ObservationProducerIdentity(
    "ordivon-runtime", "runtime-registry", "runtime:three-owner-fixture"
)
PRODUCERS = (HOST, HARNESS, RUNTIME)
MAPPING_VERSIONS = (
    ("ordivon-host", "host-journal", "host-observation-v1"),
    ("ordivon-harness", "harness-journal", "harness-observation-v1"),
    ("ordivon-runtime", "runtime-registry", "runtime-observation-v1"),
)


def _event(
    *,
    producer: ObservationProducerIdentity,
    stream_id: str,
    sequence: int,
    native_kind: str,
    native_id: str,
    mapping_version: str,
    attributes: dict[str, str | int | bool],
    relations: tuple[ObservationRelation, ...],
) -> ObservationEnvelope:
    native_record = {
        "projectId": producer.project_id,
        "componentId": producer.component_id,
        "instanceId": producer.instance_id,
        "streamId": stream_id,
        "sequence": sequence,
        "nativeKind": native_kind,
        "nativeId": native_id,
        "attributes": attributes,
    }
    return ObservationEnvelope.build(
        occurred_at_ms=1_000 + sequence,
        source=ObservationSource(
            project_id=producer.project_id,
            component_id=producer.component_id,
            instance_id=producer.instance_id,
            stream_id=stream_id,
            sequence=sequence,
            native_kind=native_kind,
            native_id=native_id,
            native_revision=sequence,
            native_digest=canonical_digest(native_record),
            mapping_version=mapping_version,
        ),
        relations=relations,
        attributes=attributes,
        privacy=ObservationPrivacy("private_metadata", "observation-metadata-v1"),
    )


def three_owner_batches() -> tuple[ObservationBatch, ...]:
    host_events = (
        _event(
            producer=HOST,
            stream_id="host-journal:three-owner-fixture",
            sequence=1,
            native_kind="ordivon.host.task-created",
            native_id="host-event:task-created",
            mapping_version="host-observation-v1",
            attributes={"taskState": "ready", "taskRevision": 1},
            relations=(
                ObservationRelation(
                    "belongs_to", "ordivon.host.task", "task:three-owner-fixture"
                ),
            ),
        ),
        _event(
            producer=HOST,
            stream_id="host-journal:three-owner-fixture",
            sequence=2,
            native_kind="ordivon.host.attempt-started",
            native_id="host-event:attempt-started",
            mapping_version="host-observation-v1",
            attributes={"attemptState": "active", "taskRevision": 2},
            relations=(
                ObservationRelation(
                    "belongs_to", "ordivon.host.task", "task:three-owner-fixture"
                ),
                ObservationRelation(
                    "belongs_to",
                    "ordivon.host.attempt",
                    "attempt:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=HOST,
            stream_id="host-journal:three-owner-fixture",
            sequence=3,
            native_kind="ordivon.host.external-request-recorded",
            native_id="host-event:external-request",
            mapping_version="host-observation-v1",
            attributes={"requestState": "committed", "taskRevision": 3},
            relations=(
                ObservationRelation(
                    "belongs_to", "ordivon.host.task", "task:three-owner-fixture"
                ),
                ObservationRelation(
                    "belongs_to",
                    "ordivon.host.external-request",
                    "external-request:three-owner-fixture",
                ),
                ObservationRelation(
                    "executes",
                    "ordivon.harness.run",
                    "harness-run:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=HOST,
            stream_id="host-journal:three-owner-fixture",
            sequence=4,
            native_kind="ordivon.host.verification-recorded",
            native_id="host-event:verification",
            mapping_version="host-observation-v1",
            attributes={"verificationState": "passed", "taskRevision": 4},
            relations=(
                ObservationRelation(
                    "belongs_to", "ordivon.host.task", "task:three-owner-fixture"
                ),
                ObservationRelation(
                    "belongs_to",
                    "ordivon.host.verification",
                    "verification:three-owner-fixture",
                ),
                ObservationRelation(
                    "verifies",
                    "ordivon.harness.completion-proposal",
                    "completion-proposal:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=HOST,
            stream_id="host-journal:three-owner-fixture",
            sequence=5,
            native_kind="ordivon.host.task-outcome-recorded",
            native_id="host-event:task-outcome",
            mapping_version="host-observation-v1",
            attributes={"taskState": "completed", "taskRevision": 5},
            relations=(
                ObservationRelation(
                    "belongs_to", "ordivon.host.task", "task:three-owner-fixture"
                ),
                ObservationRelation(
                    "accepted_by",
                    "ordivon.host.verification",
                    "verification:three-owner-fixture",
                ),
            ),
        ),
    )
    harness_events = (
        _event(
            producer=HARNESS,
            stream_id="harness-journal:three-owner-fixture",
            sequence=1,
            native_kind="ordivon.harness.run-created",
            native_id="harness-event:run-created",
            mapping_version="harness-observation-v1",
            attributes={"runState": "ready", "runRevision": 1},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.harness.run",
                    "harness-run:three-owner-fixture",
                ),
                ObservationRelation(
                    "requested_by",
                    "ordivon.host.external-request",
                    "external-request:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=HARNESS,
            stream_id="harness-journal:three-owner-fixture",
            sequence=2,
            native_kind="ordivon.harness.provider-call-recorded",
            native_id="harness-event:provider-call",
            mapping_version="harness-observation-v1",
            attributes={"providerCallState": "completed", "runRevision": 2},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.harness.run",
                    "harness-run:three-owner-fixture",
                ),
                ObservationRelation(
                    "belongs_to",
                    "ordivon.harness.provider-call",
                    "provider-call:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=HARNESS,
            stream_id="harness-journal:three-owner-fixture",
            sequence=3,
            native_kind="ordivon.harness.tool-step-recorded",
            native_id="harness-event:tool-step",
            mapping_version="harness-observation-v1",
            attributes={"toolStepState": "completed", "runRevision": 3},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.harness.run",
                    "harness-run:three-owner-fixture",
                ),
                ObservationRelation(
                    "belongs_to",
                    "ordivon.harness.tool-step",
                    "tool-step:three-owner-fixture",
                ),
                ObservationRelation(
                    "executes",
                    "ordivon.runtime.job",
                    "runtime-job:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=HARNESS,
            stream_id="harness-journal:three-owner-fixture",
            sequence=4,
            native_kind="ordivon.harness.completion-proposed",
            native_id="harness-event:completion-proposed",
            mapping_version="harness-observation-v1",
            attributes={"proposalState": "candidate", "runRevision": 4},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.harness.run",
                    "harness-run:three-owner-fixture",
                ),
                ObservationRelation(
                    "belongs_to",
                    "ordivon.harness.completion-proposal",
                    "completion-proposal:three-owner-fixture",
                ),
                ObservationRelation(
                    "proposes_for",
                    "ordivon.host.task",
                    "task:three-owner-fixture",
                ),
                ObservationRelation(
                    "references",
                    "ordivon.runtime.artifact",
                    "runtime-artifact:three-owner-fixture",
                ),
            ),
        ),
    )
    runtime_events = (
        _event(
            producer=RUNTIME,
            stream_id="runtime-job:three-owner-fixture",
            sequence=1,
            native_kind="ordivon.runtime.job-admitted",
            native_id="runtime-event:job-admitted",
            mapping_version="runtime-observation-v1",
            attributes={"physicalState": "accepted", "eventSequence": 1},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.runtime.job",
                    "runtime-job:three-owner-fixture",
                ),
                ObservationRelation(
                    "requested_by",
                    "ordivon.harness.tool-step",
                    "tool-step:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=RUNTIME,
            stream_id="runtime-job:three-owner-fixture",
            sequence=2,
            native_kind="ordivon.runtime.attempt-started",
            native_id="runtime-event:attempt-started",
            mapping_version="runtime-observation-v1",
            attributes={"physicalState": "running", "eventSequence": 2},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.runtime.job",
                    "runtime-job:three-owner-fixture",
                ),
                ObservationRelation(
                    "belongs_to",
                    "ordivon.runtime.attempt",
                    "runtime-attempt:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=RUNTIME,
            stream_id="runtime-job:three-owner-fixture",
            sequence=3,
            native_kind="ordivon.runtime.artifact-recorded",
            native_id="runtime-event:artifact-recorded",
            mapping_version="runtime-observation-v1",
            attributes={"physicalState": "recorded", "eventSequence": 3},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.runtime.job",
                    "runtime-job:three-owner-fixture",
                ),
                ObservationRelation(
                    "produced",
                    "ordivon.runtime.artifact",
                    "runtime-artifact:three-owner-fixture",
                ),
            ),
        ),
        _event(
            producer=RUNTIME,
            stream_id="runtime-job:three-owner-fixture",
            sequence=4,
            native_kind="ordivon.runtime.job-completed",
            native_id="runtime-event:job-completed",
            mapping_version="runtime-observation-v1",
            attributes={"physicalState": "succeeded", "eventSequence": 4},
            relations=(
                ObservationRelation(
                    "belongs_to",
                    "ordivon.runtime.job",
                    "runtime-job:three-owner-fixture",
                ),
                ObservationRelation(
                    "observes",
                    "ordivon.runtime.artifact",
                    "runtime-artifact:three-owner-fixture",
                ),
            ),
        ),
    )
    return (
        ObservationBatch.build(
            request_id="observation-request:three-owner:host", events=host_events
        ),
        ObservationBatch.build(
            request_id="observation-request:three-owner:harness",
            events=harness_events,
        ),
        ObservationBatch.build(
            request_id="observation-request:three-owner:runtime",
            events=runtime_events,
        ),
    )


def independent_harness_runtime_batches() -> tuple[ObservationBatch, ...]:
    run_id = "harness-run:independent-fixture"
    job_id = "runtime-job:independent-fixture"
    harness_events = (
        _event(
            producer=HARNESS,
            stream_id="harness-journal:independent-fixture",
            sequence=1,
            native_kind="ordivon.harness.harness.run-created",
            native_id="harness-event:independent-run-created",
            mapping_version="harness-observation-v1",
            attributes={"runState": "running", "runRevision": 1},
            relations=(
                ObservationRelation("belongs_to", "ordivon.harness.run", run_id),
            ),
        ),
        _event(
            producer=HARNESS,
            stream_id="harness-journal:independent-fixture",
            sequence=2,
            native_kind="ordivon.harness.harness.tool-step-recorded",
            native_id="harness-event:independent-tool-step",
            mapping_version="harness-observation-v1",
            attributes={"toolStepState": "completed", "runRevision": 2},
            relations=(
                ObservationRelation("belongs_to", "ordivon.harness.run", run_id),
                ObservationRelation("executes", "ordivon.runtime.job", job_id),
            ),
        ),
        _event(
            producer=HARNESS,
            stream_id="harness-journal:independent-fixture",
            sequence=3,
            native_kind="ordivon.harness.harness.run-stopped",
            native_id="harness-event:independent-run-stopped",
            mapping_version="harness-observation-v1",
            attributes={"runState": "stopped", "runRevision": 3},
            relations=(
                ObservationRelation("belongs_to", "ordivon.harness.run", run_id),
                ObservationRelation("executes", "ordivon.runtime.job", job_id),
            ),
        ),
    )
    runtime_events = (
        _event(
            producer=RUNTIME,
            stream_id="runtime-job:independent-fixture",
            sequence=1,
            native_kind="ordivon.runtime.job-admitted",
            native_id="runtime-event:independent-job-admitted",
            mapping_version="runtime-observation-v1",
            attributes={"physicalState": "accepted", "eventSequence": 1},
            relations=(
                ObservationRelation("belongs_to", "ordivon.runtime.job", job_id),
            ),
        ),
        _event(
            producer=RUNTIME,
            stream_id="runtime-job:independent-fixture",
            sequence=2,
            native_kind="ordivon.runtime.job-completed",
            native_id="runtime-event:independent-job-completed",
            mapping_version="runtime-observation-v1",
            attributes={"physicalState": "succeeded", "eventSequence": 2},
            relations=(
                ObservationRelation("belongs_to", "ordivon.runtime.job", job_id),
            ),
        ),
    )
    return (
        ObservationBatch.build(
            request_id="observation-request:independent:harness",
            events=harness_events,
        ),
        ObservationBatch.build(
            request_id="observation-request:independent:runtime",
            events=runtime_events,
        ),
    )


__all__ = [
    "HARNESS",
    "HOST",
    "MAPPING_VERSIONS",
    "PRODUCERS",
    "RUNTIME",
    "three_owner_batches",
    "independent_harness_runtime_batches",
]
