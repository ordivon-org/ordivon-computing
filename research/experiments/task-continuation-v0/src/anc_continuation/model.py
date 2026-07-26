from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Any

from anc_canonical import JsonValue, canonical_digest


_CAPSULE_KIND = "anc.task-capsule"
_CAPSULE_SCHEMA_VERSION = 1
_ALLOWED_REF_KINDS = {"effect", "binding", "dispatch", "fact", "artifact"}


def _exact(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{label} fields differ: {sorted(set(value) ^ expected)}")


def _identity(value: str, prefix: str) -> str:
    if not isinstance(value, str) or not value.startswith(prefix + ":"):
        raise ValueError(f"identity must start with {prefix}:")
    if value != value.strip() or len(value.encode("utf-8")) > 300:
        raise ValueError("identity is padded, empty, or too long")
    return value


def _digest(value: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 71
        or not value.startswith("sha256:")
        or any(ch not in "0123456789abcdef" for ch in value[7:])
    ):
        raise ValueError("digest must be sha256:<64 lowercase hex>")
    return value


def _revision(value: str) -> str:
    if len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError("source revision must be a 40-character lowercase Git SHA")
    return value


def _relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or value != str(path):
        raise ValueError("world path must be a normalized relative POSIX path")
    return value


class TaskPhase(StrEnum):
    READY = "ready"
    BLOCKED = "blocked"
    COMPLETE = "complete"


class ActionKind(StrEnum):
    APPLY_GUARDED_MUTATION = "apply-guarded-mutation"
    OBSERVE_DISPATCH = "observe-dispatch"
    REFRESH_WORLD = "refresh-world"


@dataclass(frozen=True, slots=True)
class SemanticRef:
    kind: str
    semantic_id: str
    digest: str

    def __post_init__(self) -> None:
        if self.kind not in _ALLOWED_REF_KINDS:
            raise ValueError(f"unsupported semantic reference kind: {self.kind}")
        _identity(self.semantic_id, self.kind)
        _digest(self.digest)

    def to_dict(self) -> dict[str, JsonValue]:
        return {"kind": self.kind, "semanticId": self.semantic_id, "digest": self.digest}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SemanticRef:
        _exact(value, {"kind", "semanticId", "digest"}, "SemanticRef")
        return cls(str(value["kind"]), str(value["semanticId"]), str(value["digest"]))


@dataclass(frozen=True, slots=True)
class GoalSpec:
    goal_id: str
    statement: str
    success_condition: JsonValue
    digest: str | None = None

    def __post_init__(self) -> None:
        _identity(self.goal_id, "goal")
        if not self.statement or self.statement != self.statement.strip():
            raise ValueError("Goal statement must be non-empty and trimmed")
        calculated = canonical_digest(
            {
                "goalId": self.goal_id,
                "statement": self.statement,
                "successCondition": self.success_condition,
            }
        )
        if self.digest is None:
            object.__setattr__(self, "digest", calculated)
        elif _digest(self.digest) != calculated:
            raise ValueError("Goal digest does not match Goal content")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "goalId": self.goal_id,
            "statement": self.statement,
            "successCondition": self.success_condition,
            "digest": self.digest,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> GoalSpec:
        _exact(value, {"goalId", "statement", "successCondition", "digest"}, "GoalSpec")
        return cls(
            str(value["goalId"]),
            str(value["statement"]),
            value["successCondition"],
            str(value["digest"]),
        )


@dataclass(frozen=True, slots=True)
class WorldBinding:
    world_id: str
    source_revision: str
    relative_path: str
    observed_digest: str
    terminal_digest: str

    def __post_init__(self) -> None:
        _identity(self.world_id, "world")
        _revision(self.source_revision)
        _relative_path(self.relative_path)
        _digest(self.observed_digest)
        _digest(self.terminal_digest)

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "worldId": self.world_id,
            "sourceRevision": self.source_revision,
            "relativePath": self.relative_path,
            "observedDigest": self.observed_digest,
            "terminalDigest": self.terminal_digest,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> WorldBinding:
        _exact(
            value,
            {"worldId", "sourceRevision", "relativePath", "observedDigest", "terminalDigest"},
            "WorldBinding",
        )
        return cls(
            str(value["worldId"]),
            str(value["sourceRevision"]),
            str(value["relativePath"]),
            str(value["observedDigest"]),
            str(value["terminalDigest"]),
        )


@dataclass(frozen=True, slots=True)
class ReadyAction:
    action_id: str
    kind: ActionKind
    effect: SemanticRef
    binding: SemanticRef
    required_world_digest: str
    expected_world_digest: str

    def __post_init__(self) -> None:
        _identity(self.action_id, "action")
        if self.effect.kind != "effect" or self.binding.kind != "binding":
            raise ValueError("ReadyAction requires Effect and Binding references")
        _digest(self.required_world_digest)
        _digest(self.expected_world_digest)
        if self.required_world_digest == self.expected_world_digest:
            raise ValueError("ready action must change the world digest")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "actionId": self.action_id,
            "kind": self.kind.value,
            "effect": self.effect.to_dict(),
            "binding": self.binding.to_dict(),
            "requiredWorldDigest": self.required_world_digest,
            "expectedWorldDigest": self.expected_world_digest,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ReadyAction:
        _exact(
            value,
            {
                "actionId",
                "kind",
                "effect",
                "binding",
                "requiredWorldDigest",
                "expectedWorldDigest",
            },
            "ReadyAction",
        )
        effect = value["effect"]
        binding = value["binding"]
        if not isinstance(effect, dict) or not isinstance(binding, dict):
            raise ValueError("ReadyAction references must be objects")
        return cls(
            str(value["actionId"]),
            ActionKind(str(value["kind"])),
            SemanticRef.from_dict(effect),
            SemanticRef.from_dict(binding),
            str(value["requiredWorldDigest"]),
            str(value["expectedWorldDigest"]),
        )


@dataclass(frozen=True, slots=True)
class TaskCapsule:
    task_id: str
    capsule_revision: int
    supersedes_digest: str | None
    goal: GoalSpec
    phase: TaskPhase
    world: WorldBinding
    completed_effects: tuple[SemanticRef, ...]
    current_bindings: tuple[SemanticRef, ...]
    unresolved_dispatches: tuple[SemanticRef, ...]
    facts: tuple[SemanticRef, ...]
    artifacts: tuple[SemanticRef, ...]
    open_questions: tuple[str, ...]
    blockers: tuple[str, ...]
    next_ready: tuple[ReadyAction, ...]
    checkpoint_id: str
    schema_version: int = _CAPSULE_SCHEMA_VERSION
    kind: str = _CAPSULE_KIND

    def __post_init__(self) -> None:
        _identity(self.task_id, "task")
        _identity(self.checkpoint_id, "checkpoint")
        if self.schema_version != _CAPSULE_SCHEMA_VERSION or self.kind != _CAPSULE_KIND:
            raise ValueError("unsupported TaskCapsule version or kind")
        if self.capsule_revision < 1:
            raise ValueError("capsule revision must be positive")
        if self.capsule_revision == 1 and self.supersedes_digest is not None:
            raise ValueError("initial capsule cannot supersede another capsule")
        if self.capsule_revision > 1:
            if self.supersedes_digest is None:
                raise ValueError("later capsule revision must supersede a digest")
            _digest(self.supersedes_digest)
        groups = (
            ("completed effect", self.completed_effects, "effect"),
            ("current binding", self.current_bindings, "binding"),
            ("unresolved dispatch", self.unresolved_dispatches, "dispatch"),
            ("Fact", self.facts, "fact"),
            ("Artifact", self.artifacts, "artifact"),
        )
        all_ids: set[str] = set()
        for label, refs, expected_kind in groups:
            for ref in refs:
                if ref.kind != expected_kind:
                    raise ValueError(f"{label} has the wrong reference kind")
                if ref.semantic_id in all_ids:
                    raise ValueError("TaskCapsule contains duplicate semantic identities")
                all_ids.add(ref.semantic_id)
        if len(set(self.open_questions)) != len(self.open_questions):
            raise ValueError("open questions must be unique")
        if len(set(self.blockers)) != len(self.blockers):
            raise ValueError("blockers must be unique")
        action_ids = [item.action_id for item in self.next_ready]
        if len(set(action_ids)) != len(action_ids):
            raise ValueError("next-ready action identities must be unique")
        if self.phase is TaskPhase.READY:
            if not self.next_ready:
                raise ValueError("ready TaskCapsule requires next-ready work")
            if self.world.observed_digest == self.world.terminal_digest:
                raise ValueError("ready TaskCapsule already matches its terminal world")
        if self.phase is TaskPhase.COMPLETE:
            if self.next_ready or self.blockers:
                raise ValueError("complete TaskCapsule cannot retain blockers or ready actions")
            if self.world.observed_digest != self.world.terminal_digest:
                raise ValueError("complete TaskCapsule must bind the terminal world digest")
        if self.phase is TaskPhase.BLOCKED and not self.blockers:
            raise ValueError("blocked TaskCapsule requires a blocker")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": self.schema_version,
            "kind": self.kind,
            "taskId": self.task_id,
            "capsuleRevision": self.capsule_revision,
            "supersedesDigest": self.supersedes_digest,
            "goal": self.goal.to_dict(),
            "phase": self.phase.value,
            "world": self.world.to_dict(),
            "completedEffects": [item.to_dict() for item in self.completed_effects],
            "currentBindings": [item.to_dict() for item in self.current_bindings],
            "unresolvedDispatches": [item.to_dict() for item in self.unresolved_dispatches],
            "facts": [item.to_dict() for item in self.facts],
            "artifacts": [item.to_dict() for item in self.artifacts],
            "openQuestions": list(self.open_questions),
            "blockers": list(self.blockers),
            "nextReady": [item.to_dict() for item in self.next_ready],
            "checkpointId": self.checkpoint_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> TaskCapsule:
        _exact(
            value,
            {
                "schemaVersion",
                "kind",
                "taskId",
                "capsuleRevision",
                "supersedesDigest",
                "goal",
                "phase",
                "world",
                "completedEffects",
                "currentBindings",
                "unresolvedDispatches",
                "facts",
                "artifacts",
                "openQuestions",
                "blockers",
                "nextReady",
                "checkpointId",
            },
            "TaskCapsule",
        )
        goal = value["goal"]
        world = value["world"]
        if not isinstance(goal, dict) or not isinstance(world, dict):
            raise ValueError("TaskCapsule Goal and world must be objects")

        def refs(name: str) -> tuple[SemanticRef, ...]:
            raw = value[name]
            if not isinstance(raw, list) or any(not isinstance(item, dict) for item in raw):
                raise ValueError(f"{name} must be a list of references")
            return tuple(SemanticRef.from_dict(item) for item in raw)

        raw_actions = value["nextReady"]
        if not isinstance(raw_actions, list) or any(not isinstance(item, dict) for item in raw_actions):
            raise ValueError("nextReady must be a list of actions")
        open_questions = value["openQuestions"]
        blockers = value["blockers"]
        if not isinstance(open_questions, list) or any(not isinstance(item, str) for item in open_questions):
            raise ValueError("openQuestions must be strings")
        if not isinstance(blockers, list) or any(not isinstance(item, str) for item in blockers):
            raise ValueError("blockers must be strings")
        supersedes = value["supersedesDigest"]
        if supersedes is not None and not isinstance(supersedes, str):
            raise ValueError("supersedesDigest must be null or a digest")
        return cls(
            task_id=str(value["taskId"]),
            capsule_revision=int(value["capsuleRevision"]),
            supersedes_digest=supersedes,
            goal=GoalSpec.from_dict(goal),
            phase=TaskPhase(str(value["phase"])),
            world=WorldBinding.from_dict(world),
            completed_effects=refs("completedEffects"),
            current_bindings=refs("currentBindings"),
            unresolved_dispatches=refs("unresolvedDispatches"),
            facts=refs("facts"),
            artifacts=refs("artifacts"),
            open_questions=tuple(open_questions),
            blockers=tuple(blockers),
            next_ready=tuple(ReadyAction.from_dict(item) for item in raw_actions),
            checkpoint_id=str(value["checkpointId"]),
            schema_version=int(value["schemaVersion"]),
            kind=str(value["kind"]),
        )


def capsule_digest(capsule: TaskCapsule) -> str:
    return canonical_digest(capsule.to_dict())
