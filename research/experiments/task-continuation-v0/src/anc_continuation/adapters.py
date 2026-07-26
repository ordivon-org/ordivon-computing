from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from anc_canonical import JsonValue, canonical_text

from .context import CompiledContext
from .model import ActionKind


class ModelAdapterError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ModelDecision:
    action_id: str
    kind: ActionKind
    effect_id: str | None
    binding_id: str | None
    dispatch_id: str | None
    rationale: str

    def __post_init__(self) -> None:
        if not self.action_id.startswith("action:") or not self.rationale:
            raise ValueError("model decision identity and rationale are required")
        if self.kind is ActionKind.APPLY_GUARDED_MUTATION:
            if self.effect_id is None or self.binding_id is None or self.dispatch_id is not None:
                raise ValueError("mutation decision requires Effect and Binding only")
        elif self.kind is ActionKind.OBSERVE_DISPATCH:
            if self.dispatch_id is None or self.effect_id is not None or self.binding_id is not None:
                raise ValueError("observe decision requires Dispatch only")
        elif self.kind is ActionKind.REFRESH_WORLD:
            if any(item is not None for item in (self.effect_id, self.binding_id, self.dispatch_id)):
                raise ValueError("refresh decision cannot carry semantic execution identities")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "actionId": self.action_id,
            "kind": self.kind.value,
            "effectId": self.effect_id,
            "bindingId": self.binding_id,
            "dispatchId": self.dispatch_id,
            "rationale": self.rationale,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ModelDecision:
        expected = {
            "actionId",
            "kind",
            "effectId",
            "bindingId",
            "dispatchId",
            "rationale",
        }
        if set(value) != expected:
            raise ValueError("ModelDecision fields differ")
        nullable = ("effectId", "bindingId", "dispatchId")
        for field in nullable:
            if value[field] is not None and not isinstance(value[field], str):
                raise ValueError(f"{field} must be null or a string")
        return cls(
            action_id=str(value["actionId"]),
            kind=ActionKind(str(value["kind"])),
            effect_id=value["effectId"],
            binding_id=value["bindingId"],
            dispatch_id=value["dispatchId"],
            rationale=str(value["rationale"]),
        )


class ModelAdapter(Protocol):
    adapter_id: str

    def decide(self, context: CompiledContext) -> ModelDecision: ...


class ScriptedModelAdapter:
    adapter_id = "scripted-continuation-model-v1"

    def decide(self, context: CompiledContext) -> ModelDecision:
        actions = context.payload["allowedActions"]
        if not isinstance(actions, list) or len(actions) != 1:
            raise ModelAdapterError("scripted adapter requires exactly one allowed action")
        action = actions[0]
        if not isinstance(action, dict):
            raise ModelAdapterError("allowed action must be an object")
        kind = ActionKind(str(action["kind"]))
        rationale = {
            ActionKind.APPLY_GUARDED_MUTATION: (
                "The audit and checkpoint reread are complete, the retained decision requires "
                "a guarded layout-preserving promotion, and the world digest is current."
            ),
            ActionKind.REFRESH_WORLD: (
                "The current world digest differs from the checkpoint, so mutation is unsafe."
            ),
            ActionKind.OBSERVE_DISPATCH: (
                "An unresolved Dispatch already crossed the boundary and must be observed."
            ),
        }[kind]
        return ModelDecision(
            action_id=str(action["actionId"]),
            kind=kind,
            effect_id=action.get("effectId"),
            binding_id=action.get("bindingId"),
            dispatch_id=action.get("dispatchId"),
            rationale=rationale,
        )


class CodexCliModelAdapter:
    adapter_id = "codex-cli-ephemeral-v1"

    def __init__(
        self,
        *,
        working_directory: str | Path,
        timeout_seconds: int = 120,
        model: str | None = None,
    ) -> None:
        self.working_directory = Path(working_directory)
        self.timeout_seconds = timeout_seconds
        self.model = model
        self.adapter_id = f"codex-cli-ephemeral-v1:{model or 'configured'}"

    def decide(self, context: CompiledContext) -> ModelDecision:
        self.working_directory.mkdir(parents=True, exist_ok=True)
        schema: dict[str, Any] = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "actionId",
                "kind",
                "effectId",
                "bindingId",
                "dispatchId",
                "rationale",
            ],
            "properties": {
                "actionId": {"type": "string"},
                "kind": {"enum": [item.value for item in ActionKind]},
                "effectId": {"type": ["string", "null"]},
                "bindingId": {"type": ["string", "null"]},
                "dispatchId": {"type": ["string", "null"]},
                "rationale": {"type": "string", "minLength": 1},
            },
        }
        prompt = (
            "You are one replaceable cognitive step inside a persistent Agent Host. "
            "You do not have the original conversation. Inspect only the compiled continuation "
            "context below. Choose exactly one item from allowedActions and copy its identities "
            "exactly. Never invent another action. Explain the decision briefly. Return JSON only.\n\n"
            + canonical_text(context.payload)
        )
        with tempfile.TemporaryDirectory(prefix="anc-codex-decision-") as temporary:
            temporary_path = Path(temporary)
            schema_path = temporary_path / "decision.schema.json"
            output_path = temporary_path / "decision.json"
            schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
            command = [
                "codex",
                "exec",
                "--ephemeral",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--ignore-rules",
                "--output-schema",
                str(schema_path),
                "--output-last-message",
                str(output_path),
                "--color",
                "never",
                "-C",
                str(self.working_directory),
            ]
            if self.model is not None:
                command.extend(["--model", self.model])
            command.append("-")
            completed = subprocess.run(
                command,
                input=prompt,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout_seconds,
                check=False,
            )
            if completed.returncode != 0:
                raise ModelAdapterError(
                    "Codex CLI decision failed: " + completed.stderr.strip()[-2_000:]
                )
            try:
                value = json.loads(output_path.read_text())
                if not isinstance(value, dict):
                    raise ValueError("decision must be an object")
                return ModelDecision.from_dict(value)
            except (OSError, ValueError, json.JSONDecodeError) as error:
                raise ModelAdapterError("Codex CLI returned an invalid decision") from error
