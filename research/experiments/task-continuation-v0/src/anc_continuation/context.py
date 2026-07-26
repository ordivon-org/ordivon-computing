from __future__ import annotations

from dataclasses import dataclass

from anc_canonical import JsonValue, canonical_bytes, canonical_digest

from .model import ActionKind, TaskCapsule
from .validation import ValidationReport


@dataclass(frozen=True, slots=True)
class CompiledContext:
    payload: dict[str, JsonValue]

    @property
    def digest(self) -> str:
        return canonical_digest(self.payload)

    @property
    def byte_length(self) -> int:
        return len(canonical_bytes(self.payload))


class ContextCompiler:
    """Compile current semantic state into bounded model context without transcript replay."""

    def compile(
        self, capsule: TaskCapsule, report: ValidationReport
    ) -> CompiledContext:
        if report.world_status == "drifted":
            allowed_actions: list[JsonValue] = [
                {
                    "actionId": "action:refresh-world",
                    "kind": ActionKind.REFRESH_WORLD.value,
                    "effectId": None,
                    "bindingId": None,
                    "dispatchId": None,
                }
            ]
        elif report.unresolved_dispatch_ids:
            allowed_actions = [
                {
                    "actionId": f"action:observe:{dispatch_id}",
                    "kind": ActionKind.OBSERVE_DISPATCH.value,
                    "effectId": None,
                    "bindingId": None,
                    "dispatchId": dispatch_id,
                }
                for dispatch_id in report.unresolved_dispatch_ids
            ]
        else:
            allowed_actions = [
                {
                    "actionId": item.action.action_id,
                    "kind": item.action.kind.value,
                    "effectId": item.action.effect.semantic_id,
                    "bindingId": item.action.binding.semantic_id,
                    "dispatchId": None,
                    "requiredWorldDigest": item.action.required_world_digest,
                    "expectedWorldDigest": item.action.expected_world_digest,
                }
                for item in report.resolved_actions
            ]
        payload: dict[str, JsonValue] = {
            "schemaVersion": 1,
            "kind": "anc.compiled-continuation-context",
            "task": {
                "taskId": capsule.task_id,
                "capsuleRevision": capsule.capsule_revision,
                "phase": capsule.phase.value,
                "checkpointId": capsule.checkpoint_id,
            },
            "goal": {
                "goalId": capsule.goal.goal_id,
                "digest": capsule.goal.digest,
                "statement": capsule.goal.statement,
                "successCondition": capsule.goal.success_condition,
            },
            "world": {
                "worldId": capsule.world.world_id,
                "relativePath": capsule.world.relative_path,
                "sourceRevision": capsule.world.source_revision,
                "checkpointDigest": capsule.world.observed_digest,
                "currentDigest": report.current_world_digest,
                "terminalDigest": capsule.world.terminal_digest,
                "status": report.world_status,
            },
            "verifiedState": {
                "completedEffects": list(report.completed_effect_ids),
                "facts": list(report.fact_ids),
                "artifacts": list(report.artifact_ids),
            },
            "retainedDecisions": list(report.decisions),
            "unresolvedDispatches": list(report.unresolved_dispatch_ids),
            "forbiddenEffects": list(report.completed_effect_ids),
            "openQuestions": list(capsule.open_questions),
            "blockers": list(capsule.blockers),
            "allowedActions": allowed_actions,
            "instruction": (
                "Choose exactly one allowed action. Never repeat a forbidden Effect. "
                "When world status is drifted, refresh before mutation. When an unresolved "
                "Dispatch exists, observe it rather than redispatching its Effect."
            ),
        }
        return CompiledContext(payload)
