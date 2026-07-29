from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any, Protocol

from .model import JsonValue, canonical_bytes


class LiveModelError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ChoiceDecision:
    action_id: str
    rationale: str

    def __post_init__(self) -> None:
        if not self.action_id.startswith("action:"):
            raise ValueError("choice action identity must start with action:")
        if not self.rationale or self.rationale != self.rationale.strip():
            raise ValueError("choice rationale is required")

    def to_dict(self) -> dict[str, JsonValue]:
        return {"actionId": self.action_id, "rationale": self.rationale}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ChoiceDecision:
        if set(value) != {"actionId", "rationale"}:
            raise ValueError("ChoiceDecision fields differ")
        if not isinstance(value["actionId"], str) or not isinstance(value["rationale"], str):
            raise ValueError("ChoiceDecision fields must be strings")
        return cls(value["actionId"], value["rationale"])


@dataclass(frozen=True, slots=True)
class LiveModelResult:
    decision: ChoiceDecision
    evidence: dict[str, JsonValue]


class ChoiceAdapter(Protocol):
    adapter_id: str

    def choose(self, context: dict[str, JsonValue]) -> LiveModelResult: ...


def _prompt(context: dict[str, JsonValue]) -> str:
    return (
        "You are one replaceable cognitive step inside a persistent engineering Host. "
        "You do not have the original conversation and have no authority to invent an "
        "external operation. Inspect only the bounded Context below. Choose exactly one "
        "item from allowedActions and copy its actionId exactly. Treat source trust, world "
        "revision, completed effects, and unresolved operations as binding facts. Return "
        "exactly one JSON object with actionId and rationale. Do not use markdown.\n\n"
        + canonical_bytes(context).decode("utf-8")
    )


class CodexChoiceAdapter:
    def __init__(
        self,
        *,
        working_directory: str | Path,
        model: str | None = None,
        timeout_seconds: int = 180,
    ) -> None:
        self.working_directory = Path(working_directory)
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.adapter_id = f"codex-cli-ephemeral-v1:{model or 'configured'}"

    def choose(self, context: dict[str, JsonValue]) -> LiveModelResult:
        self.working_directory.mkdir(parents=True, exist_ok=True)
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["actionId", "rationale"],
            "properties": {
                "actionId": {"type": "string", "pattern": "^action:"},
                "rationale": {"type": "string", "minLength": 1},
            },
        }
        with tempfile.TemporaryDirectory(prefix="anc-round1-codex-") as temporary:
            root = Path(temporary)
            schema_path = root / "choice.schema.json"
            output_path = root / "choice.json"
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
                input=_prompt(context),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout_seconds,
                check=False,
            )
            if completed.returncode != 0:
                raise LiveModelError(
                    "Codex choice failed: " + completed.stderr.strip()[-2_000:]
                )
            try:
                value = json.loads(output_path.read_text("utf-8"))
                if not isinstance(value, dict):
                    raise ValueError("Codex choice must be an object")
                decision = ChoiceDecision.from_dict(value)
            except (OSError, ValueError, json.JSONDecodeError) as error:
                raise LiveModelError("Codex returned invalid structured output") from error
        return LiveModelResult(
            decision=decision,
            evidence={
                "adapterId": self.adapter_id,
                "physicalProviderCall": True,
                "ephemeralSession": True,
                "sandbox": "read-only",
                "toolsExposed": [],
                "memoryLoaded": False,
            },
        )


class HermesChoiceAdapter:
    def __init__(
        self,
        *,
        working_directory: str | Path,
        model: str = "deepseek-v4-pro",
        provider: str = "deepseek",
        base_url: str = "https://api.deepseek.com",
        credential_env_path: str | Path = "/root/.hermes/.env",
        timeout_seconds: int = 240,
    ) -> None:
        self.working_directory = Path(working_directory)
        self.model = model
        self.provider = provider
        self.base_url = base_url.rstrip("/")
        self.credential_env_path = Path(credential_env_path)
        self.timeout_seconds = timeout_seconds
        self.adapter_id = f"hermes-cli-isolated-v1:{provider}/{model}"

    def choose(self, context: dict[str, JsonValue]) -> LiveModelResult:
        self.working_directory.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="anc-round1-hermes-") as temporary:
            root = Path(temporary)
            hermes_home = root / "hermes"
            user_home = root / "home"
            hermes_home.mkdir()
            user_home.mkdir()
            self._write_credentials(hermes_home / ".env")
            self._write_config(hermes_home / "config.yaml")
            (hermes_home / ".no-bundled-skills").touch()
            usage_path = root / "usage.json"
            command = [
                "hermes",
                "--oneshot",
                _prompt(context),
                "--model",
                self.model,
                "--provider",
                self.provider,
                "--ignore-rules",
                "--usage-file",
                str(usage_path),
            ]
            environment = os.environ.copy()
            environment.update(
                {"HOME": str(user_home), "HERMES_HOME": str(hermes_home), "NO_COLOR": "1"}
            )
            for name in (
                "HERMES_INFERENCE_MODEL",
                "HERMES_INFERENCE_PROVIDER",
                "HERMES_IGNORE_USER_CONFIG",
                "HERMES_SAFE_MODE",
            ):
                environment.pop(name, None)
            try:
                completed = subprocess.run(
                    command,
                    cwd=self.working_directory,
                    env=environment,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=self.timeout_seconds,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as error:
                raise LiveModelError("Hermes invocation failed") from error
            if completed.returncode != 0:
                raise LiveModelError(
                    "Hermes choice failed: " + completed.stderr.strip()[-2_000:]
                )
            try:
                value = json.loads(completed.stdout)
                usage = json.loads(usage_path.read_text("utf-8"))
                if not isinstance(value, dict) or not isinstance(usage, dict):
                    raise ValueError("Hermes result and usage must be objects")
                decision = ChoiceDecision.from_dict(value)
                if usage.get("completed") is not True or usage.get("failed") is not False:
                    raise ValueError("Hermes usage reports failure")
                if int(usage.get("api_calls") or 0) < 1:
                    raise ValueError("Hermes usage reports no provider call")
            except (OSError, ValueError, json.JSONDecodeError) as error:
                raise LiveModelError("Hermes returned invalid structured output") from error
        return LiveModelResult(
            decision=decision,
            evidence={
                "adapterId": self.adapter_id,
                "physicalProviderCall": True,
                "isolatedHome": True,
                "persistentSessionRetained": False,
                "toolsExposed": [],
                "memoryLoaded": False,
                "model": usage.get("model"),
                "provider": usage.get("provider"),
                "apiCalls": int(usage.get("api_calls") or 0),
                "inputTokens": int(usage.get("input_tokens") or 0),
                "outputTokens": int(usage.get("output_tokens") or 0),
                "reasoningTokens": int(usage.get("reasoning_tokens") or 0),
                "totalTokens": int(usage.get("total_tokens") or 0),
                "estimatedCostUsd": usage.get("estimated_cost_usd"),
            },
        )

    def _write_credentials(self, destination: Path) -> None:
        try:
            lines = self.credential_env_path.read_text("utf-8").splitlines()
        except OSError as error:
            raise LiveModelError("Hermes credential environment is unavailable") from error
        prefix = self.provider.upper().replace("-", "_")
        key_name = f"{prefix}_API_KEY"
        key_lines = [line for line in lines if line.startswith(key_name + "=")]
        if not key_lines or not key_lines[-1].split("=", 1)[1]:
            raise LiveModelError(f"Hermes credential file has no {key_name}")
        destination.write_text(
            key_lines[-1] + "\n" + f"{prefix}_BASE_URL={self.base_url}\n",
            encoding="utf-8",
        )
        destination.chmod(0o600)

    def _write_config(self, destination: Path) -> None:
        destination.write_text(
            "model:\n"
            f"  default: {json.dumps(self.model)}\n"
            f"  provider: {json.dumps(self.provider)}\n"
            f"  base_url: {json.dumps(self.base_url)}\n"
            "platform_toolsets:\n"
            "  cli: []\n"
            "mcp_servers: {}\n"
            "agent:\n"
            "  disabled_toolsets:\n"
            "    - kanban\n"
            "memory:\n"
            "  memory_enabled: false\n"
            "  user_profile_enabled: false\n"
            "  nudge_interval: 0\n"
            "  flush_min_turns: 999999\n"
            "skills:\n"
            "  creation_nudge_interval: 999999\n"
            "sessions:\n"
            "  write_json_snapshots: false\n",
            encoding="utf-8",
        )
        destination.chmod(0o600)
