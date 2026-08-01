from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
import json
from typing import Any, Mapping

JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


def canonical_bytes(value: JsonValue) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_digest(value: JsonValue) -> str:
    return "sha256:" + sha256(canonical_bytes(value)).hexdigest()


def deterministic_fraction(*parts: str) -> float:
    digest = sha256("\x1f".join(parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / float(2**64)


def require_identity(value: str, prefix: str) -> str:
    if (
        not value.startswith(prefix + ":")
        or value != value.strip()
        or len(value.encode("utf-8")) > 300
    ):
        raise ValueError(f"identity must start with {prefix}: and be bounded")
    return value


class Scenario(StrEnum):
    AGENT_HIJACKING = "agent-hijacking"
    RESPONSE_LOSS = "response-loss"
    INTERPRETATION_DIFFERENTIAL = "interpretation-differential"


class TrialStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    INVALID = "invalid"


class SourceTrust(StrEnum):
    TRUSTED_INSTRUCTION = "trusted-instruction"
    UNTRUSTED_EVIDENCE = "untrusted-evidence"


class ResponseState(StrEnum):
    ABSENT = "absent"
    UNKNOWN = "unknown"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class SourceRecord:
    source_id: str
    trust: SourceTrust
    revision: str
    content_label: str

    def __post_init__(self) -> None:
        require_identity(self.source_id, "source")
        if not self.revision or self.revision != self.revision.strip():
            raise ValueError("source revision is required")
        if not self.content_label or self.content_label != self.content_label.strip():
            raise ValueError("content label is required")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "sourceId": self.source_id,
            "trust": self.trust.value,
            "revision": self.revision,
            "contentLabel": self.content_label,
        }


@dataclass(frozen=True, slots=True)
class ToolGrant:
    grant_id: str
    tool_id: str
    effect_id: str
    resource_id: str
    onward_delegation: bool = False

    def __post_init__(self) -> None:
        require_identity(self.grant_id, "tool-grant")
        require_identity(self.tool_id, "tool")
        require_identity(self.effect_id, "effect")
        require_identity(self.resource_id, "resource")

    def allows(self, candidate: "CandidateAction") -> bool:
        return (
            candidate.tool_id == self.tool_id
            and candidate.effect_id == self.effect_id
            and candidate.resource_id == self.resource_id
        )

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "grantId": self.grant_id,
            "toolId": self.tool_id,
            "effectId": self.effect_id,
            "resourceId": self.resource_id,
            "onwardDelegation": self.onward_delegation,
        }


@dataclass(frozen=True, slots=True)
class CandidateAction:
    action_id: str
    tool_id: str
    effect_id: str
    resource_id: str
    source_id: str
    purpose: str

    def __post_init__(self) -> None:
        require_identity(self.action_id, "action")
        require_identity(self.tool_id, "tool")
        require_identity(self.effect_id, "effect")
        require_identity(self.resource_id, "resource")
        require_identity(self.source_id, "source")
        if not self.purpose or self.purpose != self.purpose.strip():
            raise ValueError("action purpose is required")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "actionId": self.action_id,
            "toolId": self.tool_id,
            "effectId": self.effect_id,
            "resourceId": self.resource_id,
            "sourceId": self.source_id,
            "purpose": self.purpose,
        }


@dataclass(frozen=True, slots=True)
class Receipt:
    receipt_id: str
    effect_id: str
    idempotency_key: str | None
    commit_index: int
    payload_digest: str

    def __post_init__(self) -> None:
        require_identity(self.receipt_id, "receipt")
        require_identity(self.effect_id, "effect")
        if self.idempotency_key is not None:
            require_identity(self.idempotency_key, "idempotency-key")
        if self.commit_index < 1:
            raise ValueError("commit index must be positive")
        if not self.payload_digest.startswith("sha256:"):
            raise ValueError("payload digest is required")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "receiptId": self.receipt_id,
            "effectId": self.effect_id,
            "idempotencyKey": self.idempotency_key,
            "commitIndex": self.commit_index,
            "payloadDigest": self.payload_digest,
        }


@dataclass(frozen=True, slots=True)
class TrialRecord:
    trial_id: str
    scenario: Scenario
    variant: str
    seed: int
    status: TrialStatus
    accepted_outcome: bool
    observations: Mapping[str, JsonValue]
    costs: Mapping[str, JsonValue]
    hard_failures: tuple[str, ...] = ()
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_identity(self.trial_id, "trial")
        if not self.variant or self.variant != self.variant.strip():
            raise ValueError("variant is required")
        if self.seed < 0:
            raise ValueError("seed must be non-negative")
        if len(self.hard_failures) != len(set(self.hard_failures)):
            raise ValueError("hard failures must be unique")
        if len(self.residuals) != len(set(self.residuals)):
            raise ValueError("residuals must be unique")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": 1,
            "kind": "anc.adversarial-range-trial",
            "trialId": self.trial_id,
            "scenario": self.scenario.value,
            "variant": self.variant,
            "seed": self.seed,
            "status": self.status.value,
            "acceptedOutcome": self.accepted_outcome,
            "hardFailures": list(self.hard_failures),
            "residuals": list(self.residuals),
            "observations": dict(self.observations),
            "costs": dict(self.costs),
        }


@dataclass(frozen=True, slots=True)
class RangeResult:
    source_revision: str
    trials: tuple[TrialRecord, ...]
    summary: Mapping[str, JsonValue]
    decisions: Mapping[str, JsonValue]

    def to_dict(self) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "schemaVersion": 1,
            "kind": "anc.adversarial-range-result",
            "sourceRevision": self.source_revision,
            "trials": [trial.to_dict() for trial in self.trials],
            "summary": dict(self.summary),
            "decisions": dict(self.decisions),
        }
        payload["resultDigest"] = canonical_digest(payload)
        return payload

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "RangeResult":
        trials = tuple(
            TrialRecord(
                trial_id=item["trialId"],
                scenario=Scenario(item["scenario"]),
                variant=item["variant"],
                seed=int(item["seed"]),
                status=TrialStatus(item["status"]),
                accepted_outcome=bool(item["acceptedOutcome"]),
                hard_failures=tuple(item["hardFailures"]),
                residuals=tuple(item["residuals"]),
                observations=item["observations"],
                costs=item["costs"],
            )
            for item in value["trials"]
        )
        return cls(
            source_revision=str(value["sourceRevision"]),
            trials=trials,
            summary=value["summary"],
            decisions=value["decisions"],
        )
