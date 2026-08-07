from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from ordivon_observation_core import ObservationMeasurement, canonical_digest

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class MeasurementProjectionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class MeasurementProjection:
    profile_version: str
    measurements: dict[str, ObservationMeasurement]
    source_fields: dict[str, str]
    omitted_fields: tuple[str, ...]
    basis_refs: dict[str, str]
    otel_aliases: dict[str, str]

    @property
    def digest(self) -> str:
        return canonical_digest(self.payload())

    def payload(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.measurement-projection-experiment",
            "profileVersion": self.profile_version,
            "measurements": {
                key: value.to_dict()
                for key, value in sorted(self.measurements.items())
            },
            "sourceFields": dict(sorted(self.source_fields.items())),
            "omittedFields": list(self.omitted_fields),
            "basisRefs": dict(sorted(self.basis_refs.items())),
            "otelAliases": dict(sorted(self.otel_aliases.items())),
        }

    def to_dict(self) -> dict[str, Any]:
        value = self.payload()
        value["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": self.digest,
        }
        return value


def _non_negative(value: Any, label: str) -> int | float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise MeasurementProjectionError(f"{label} must be non-negative numeric or null")
    return value


def from_evaluation_metrics(
    metrics: dict[str, Any],
    *,
    pricing_basis_digest: str | None = None,
) -> MeasurementProjection:
    mappings = {
        "modelCalls": ("ordivon.harness.model_calls", "1"),
        "toolCalls": ("ordivon.harness.tool_calls", "1"),
        "runtimeJobs": ("ordivon.runtime.job_count", "1"),
        "observationBytes": ("ordivon.harness.observation_bytes", "By"),
        "inputTokens": ("ordivon.harness.input_tokens", "token"),
        "outputTokens": ("ordivon.harness.output_tokens", "token"),
        "cachedInputTokens": ("ordivon.harness.cached_input_tokens", "token"),
        "reasoningTokens": ("ordivon.harness.reasoning_tokens", "token"),
        "totalTokens": ("ordivon.harness.total_tokens", "token"),
        "wallTimeMs": ("ordivon.harness.wall_time", "ms"),
        "repeatedReads": ("ordivon.harness.repeated_reads", "1"),
        "repeatedCommands": ("ordivon.harness.repeated_commands", "1"),
        "invalidToolCalls": ("ordivon.harness.invalid_tool_calls", "1"),
        "humanInterventionCount": ("ordivon.human.intervention_count", "1"),
    }
    measurements: dict[str, ObservationMeasurement] = {}
    source_fields: dict[str, str] = {}
    omitted: list[str] = []
    for source, (target, unit) in mappings.items():
        if source not in metrics:
            raise MeasurementProjectionError(f"required Evaluation metric is absent: {source}")
        value = _non_negative(metrics[source], source)
        if value is None:
            omitted.append(source)
            continue
        measurements[target] = ObservationMeasurement(value=value, unit=unit)
        source_fields[target] = source

    cost = _non_negative(metrics.get("estimatedCostUsd"), "estimatedCostUsd")
    basis_refs: dict[str, str] = {}
    if cost is None:
        omitted.append("estimatedCostUsd")
    else:
        if pricing_basis_digest is None or _DIGEST.fullmatch(pricing_basis_digest) is None:
            raise MeasurementProjectionError(
                "estimated monetary cost requires an explicit SHA-256 pricing/billing basis"
            )
        target = "ordivon.cost.estimated_usd"
        measurements[target] = ObservationMeasurement(value=cost, unit="USD")
        source_fields[target] = "estimatedCostUsd"
        basis_refs[target] = pricing_basis_digest

    aliases = {
        "ordivon.harness.input_tokens": "gen_ai.usage.input_tokens",
        "ordivon.harness.output_tokens": "gen_ai.usage.output_tokens",
        "ordivon.harness.cached_input_tokens": "gen_ai.usage.cache_read.input_tokens",
        "ordivon.harness.reasoning_tokens": "gen_ai.usage.reasoning.output_tokens",
    }
    return MeasurementProjection(
        profile_version="a0-u1-evaluation-v1",
        measurements=measurements,
        source_fields=source_fields,
        omitted_fields=tuple(sorted(set(omitted))),
        basis_refs=basis_refs,
        otel_aliases=aliases,
    )
