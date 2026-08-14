"""Non-authoritative cross-owner Agent Situation composition.

This module compiles already-observed owner facts. It does not query owners,
probe liveness, grant authority, select an execution locus, reconcile effects,
or infer semantic completion. Owner-native projections remain canonical.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import JsonValue, bounded_text, canonical_digest, digest, namespaced_kind

SITUATION_ROLES = frozenset(
    {
        "continuity",
        "locus-hint",
        "locus-observation",
        "action-surface",
        "admission",
        "occurrence",
        "recovery",
        "completion",
    }
)
SITUATION_CURRENTNESS = frozenset(
    {"current", "historical", "unknown", "not-claimed", "not-probed", "unavailable"}
)
SITUATION_AUTHORITY = frozenset(
    {"granted", "denied", "not-granted", "not-claimed", "not-applicable"}
)


def _identity(value: Any, *, label: str) -> str:
    return bounded_text(value, label=label, max_bytes=1_024)


@dataclass(frozen=True, slots=True, order=True)
class SituationRelation:
    kind: str
    identity: str

    def __post_init__(self) -> None:
        namespaced_kind(self.kind, label="Situation relation kind")
        _identity(self.identity, label="Situation relation identity")

    def to_dict(self) -> dict[str, JsonValue]:
        return {"kind": self.kind, "identity": self.identity}


@dataclass(frozen=True, slots=True)
class SituationAnchor:
    owner: str
    kind: str
    identity: str

    def __post_init__(self) -> None:
        namespaced_kind(self.owner, label="Situation anchor owner")
        namespaced_kind(self.kind, label="Situation anchor kind")
        _identity(self.identity, label="Situation anchor identity")

    def to_dict(self) -> dict[str, JsonValue]:
        return {"owner": self.owner, "kind": self.kind, "identity": self.identity}


@dataclass(frozen=True, slots=True)
class SituationFacet:
    owner: str
    role: str
    kind: str
    identity: str
    state: str
    currentness: str = "not-claimed"
    authority: str = "not-claimed"
    evidence_digest: str | None = None
    next_owner_operation: str | None = None
    related_to: tuple[SituationRelation, ...] = ()

    def __post_init__(self) -> None:
        namespaced_kind(self.owner, label="Situation facet owner")
        if self.role not in SITUATION_ROLES:
            raise ValueError(f"unsupported Situation role: {self.role}")
        namespaced_kind(self.kind, label="Situation facet kind")
        _identity(self.identity, label="Situation facet identity")
        bounded_text(self.state, label="Situation facet state", max_bytes=256)
        if self.currentness not in SITUATION_CURRENTNESS:
            raise ValueError(f"unsupported Situation currentness: {self.currentness}")
        if self.authority not in SITUATION_AUTHORITY:
            raise ValueError(f"unsupported Situation authority: {self.authority}")
        if self.evidence_digest is not None:
            digest(self.evidence_digest, label="Situation evidence digest")
        if self.next_owner_operation is not None:
            bounded_text(
                self.next_owner_operation,
                label="Situation next owner operation",
                max_bytes=512,
            )
        if tuple(sorted(self.related_to)) != self.related_to:
            raise ValueError("Situation relations must be sorted")
        if len(set(self.related_to)) != len(self.related_to):
            raise ValueError("Situation relations must be unique")

    def to_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "owner": self.owner,
            "role": self.role,
            "kind": self.kind,
            "identity": self.identity,
            "state": self.state,
            "currentness": self.currentness,
            "authority": self.authority,
            "relatedTo": [item.to_dict() for item in self.related_to],
        }
        if self.evidence_digest is not None:
            value["evidenceDigest"] = self.evidence_digest
        if self.next_owner_operation is not None:
            value["nextOwnerOperation"] = self.next_owner_operation
        return value


@dataclass(frozen=True, slots=True)
class SituationProjection:
    anchor: SituationAnchor
    facets: tuple[SituationFacet, ...]
    unresolved: tuple[dict[str, str], ...]
    next_owner_operations: tuple[dict[str, str], ...]
    rejected_implications: tuple[str, ...]

    def to_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "schemaVersion": 1,
            "kind": "ordivon.observation.agent-situation-projection",
            "truthRole": "derived-read-only-owner-qualified-projection",
            "anchor": self.anchor.to_dict(),
            "facets": [item.to_dict() for item in self.facets],
            "unresolved": [dict(item) for item in self.unresolved],
            "nextOwnerOperations": [dict(item) for item in self.next_owner_operations],
            "rejectedImplications": list(self.rejected_implications),
            "proofBoundaries": [
                "projection-does-not-grant-authority",
                "historical-evidence-does-not-prove-currentness",
                "runtime-physical-success-does-not-prove-semantic-completion",
                "navigation-hint-does-not-prove-current-locus",
                "unknown-does-not-authorize-redispatch",
                "owner-native-state-remains-canonical",
            ],
        }
        value["digest"] = canonical_digest(value)
        return value


def compile_situation(
    anchor: SituationAnchor,
    facets: tuple[SituationFacet, ...],
) -> SituationProjection:
    """Compile explicit owner observations into one non-authoritative view.

    The function performs only identity-equality joins and fixed proof-boundary
    checks. It deliberately cannot discover owners, choose a locus, probe
    currentness, execute a recovery hint, or validate domain completion.
    """

    ordered = tuple(
        sorted(facets, key=lambda item: (item.role, item.owner, item.kind, item.identity))
    )
    identities = [(item.owner, item.role, item.kind, item.identity) for item in ordered]
    if len(set(identities)) != len(identities):
        raise ValueError("Situation facets must have unique owner-qualified role identities")

    unresolved: list[dict[str, str]] = []
    next_ops: list[dict[str, str]] = []
    rejected = {
        "installed-capability-implies-current-authority",
        "historical-occurrence-implies-current-presence",
        "runtime-physical-success-implies-semantic-completion",
        "unknown-implies-safe-redispatch",
    }

    hints = [item for item in ordered if item.role == "locus-hint"]
    locus_observations = {
        (item.kind, item.identity): item
        for item in ordered
        if item.role == "locus-observation"
    }
    for hint in hints:
        observed = locus_observations.get((hint.kind, hint.identity))
        if observed is None:
            unresolved.append(
                {
                    "owner": hint.owner,
                    "identity": hint.identity,
                    "reason": "locus-hint-has-no-current-owner-observation",
                }
            )
        elif observed.currentness in {
            "unavailable",
            "unknown",
            "not-claimed",
            "not-probed",
        }:
            unresolved.append(
                {
                    "owner": observed.owner,
                    "identity": observed.identity,
                    "reason": "hinted-locus-is-not-currently-usable",
                }
            )
            rejected.add("navigation-hint-implies-current-locus")

    actions = [item for item in ordered if item.role == "action-surface"]
    admissions = {
        (item.kind, item.identity): item for item in ordered if item.role == "admission"
    }
    for action in actions:
        admitted = admissions.get((action.kind, action.identity))
        if admitted is None or admitted.authority != "granted":
            unresolved.append(
                {
                    "owner": action.owner,
                    "identity": action.identity,
                    "reason": "installed-action-has-no-exact-current-admission",
                }
            )

    runtime_success = any(
        item.role == "occurrence"
        and item.owner == "ordivon-runtime"
        and item.state in {"succeeded", "completed"}
        for item in ordered
    )
    completion = [item for item in ordered if item.role == "completion"]
    if runtime_success and not any(
        item.authority == "granted" and item.state in {"completed", "accepted"}
        for item in completion
    ):
        unresolved.append(
            {
                "owner": anchor.owner,
                "identity": anchor.identity,
                "reason": "semantic-completion-not-proven-by-physical-runtime-success",
            }
        )

    for item in ordered:
        if item.next_owner_operation is not None:
            next_ops.append(
                {
                    "owner": item.owner,
                    "identity": item.identity,
                    "operation": item.next_owner_operation,
                    "authority": item.authority,
                }
            )
        if item.state == "unknown":
            rejected.add("unknown-implies-failure")
            if item.next_owner_operation is None:
                unresolved.append(
                    {
                        "owner": item.owner,
                        "identity": item.identity,
                        "reason": "unknown-has-no-owner-recovery-route",
                    }
                )

    return SituationProjection(
        anchor=anchor,
        facets=ordered,
        unresolved=tuple(
            sorted(
                unresolved,
                key=lambda item: (item["owner"], item["identity"], item["reason"]),
            )
        ),
        next_owner_operations=tuple(
            sorted(
                next_ops,
                key=lambda item: (item["owner"], item["identity"], item["operation"]),
            )
        ),
        rejected_implications=tuple(sorted(rejected)),
    )


__all__ = [
    "SITUATION_AUTHORITY",
    "SITUATION_CURRENTNESS",
    "SITUATION_ROLES",
    "SituationAnchor",
    "SituationFacet",
    "SituationProjection",
    "SituationRelation",
    "compile_situation",
]
