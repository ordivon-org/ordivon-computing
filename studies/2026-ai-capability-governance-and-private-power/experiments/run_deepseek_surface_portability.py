#!/usr/bin/env python3
"""Run a benign DeepSeek OpenAI/Anthropic surface portability pilot."""

from __future__ import annotations

import hashlib
import json
import stat
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SECRET = Path("/root/.config/ordivon/secrets/deepseek.json")
MODELS = ("deepseek-v4-flash", "deepseek-v4-pro")
SURFACES = ("openai-chat-completions", "anthropic-messages")
REPLICATES = 2
FACTS = {"asset": "ORBITAL-7", "severity": "amber", "count": 42}
SYSTEM = (
    "You are participating in a benign API portability test. Return exactly one "
    "compact JSON object with no markdown and no additional keys."
)
ROUND1 = (
    "Record these authorized synthetic facts and return them as JSON with keys "
    "asset, severity, count: Asset ORBITAL-7; severity amber; count 42."
)
ROUND2 = (
    "Using the prior turn supplied by the caller, return exactly the same JSON "
    "object. Do not infer any other data."
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def read_secret() -> tuple[str, str]:
    if SECRET.is_symlink() or not SECRET.is_file():
        raise RuntimeError("DeepSeek secret path is invalid")
    mode = stat.S_IMODE(SECRET.stat().st_mode)
    if mode & 0o077:
        raise RuntimeError(f"DeepSeek secret permissions too broad: {oct(mode)}")
    value = json.loads(SECRET.read_text(encoding="utf-8"))
    if set(value) != {"schemaVersion", "provider", "apiKey", "baseUrl", "model"}:
        raise RuntimeError("DeepSeek secret fields differ")
    if value["schemaVersion"] != 1 or value["provider"] != "deepseek":
        raise RuntimeError("DeepSeek secret schema differs")
    return value["apiKey"], value["baseUrl"]


def post(url: str, headers: dict[str, str], body: dict[str, Any]) -> tuple[dict[str, Any], float]:
    raw_body = canonical(body)
    request = urllib.request.Request(url, data=raw_body, method="POST", headers=headers)
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read(4_194_305)
    except urllib.error.HTTPError as error:
        detail = error.read(16_384).decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code}: {detail}") from error
    elapsed = time.monotonic() - started
    if len(raw) > 4_194_304:
        raise RuntimeError("response exceeds bound")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("response is not an object")
    return value, elapsed


def extract_json(text: str) -> tuple[dict[str, Any] | None, str | None]:
    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3:
            candidate = "\n".join(lines[1:-1]).strip()
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError as error:
        return None, str(error)
    if not isinstance(value, dict):
        return None, "parsed value is not an object"
    return value, None


def openai_turn(api_key: str, base_url: str, model: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
    value, latency = post(
        base_url.rstrip("/") + "/chat/completions",
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ordivon-g6-portability/1",
        },
        {
            "model": model,
            "messages": messages,
            "thinking": {"type": "disabled"},
            "temperature": 0,
            "max_tokens": 256,
            "stream": False,
        },
    )
    choices = value.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        raise RuntimeError("OpenAI-compatible choices differ")
    message = choices[0].get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise RuntimeError("OpenAI-compatible message differs")
    return {
        "text": message["content"],
        "latencyMs": round(latency * 1000, 3),
        "responseIdDigest": digest(value.get("id")),
        "modelReturned": value.get("model"),
        "usage": value.get("usage", {}),
        "finishReason": choices[0].get("finish_reason"),
    }


def anthropic_turn(api_key: str, model: str, system: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
    value, latency = post(
        "https://api.deepseek.com/anthropic/v1/messages",
        {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "User-Agent": "ordivon-g6-portability/1",
        },
        {
            "model": model,
            "system": system,
            "messages": messages,
            "temperature": 0,
            "max_tokens": 256,
            "stream": False,
        },
    )
    content = value.get("content")
    if not isinstance(content, list):
        raise RuntimeError("Anthropic-compatible content differs")
    texts = [item.get("text") for item in content if isinstance(item, dict) and item.get("type") == "text"]
    if not texts or any(not isinstance(item, str) for item in texts):
        raise RuntimeError("Anthropic-compatible text differs")
    usage = value.get("usage", {})
    return {
        "text": "".join(texts),
        "latencyMs": round(latency * 1000, 3),
        "responseIdDigest": digest(value.get("id")),
        "modelReturned": value.get("model"),
        "usage": usage,
        "finishReason": value.get("stop_reason"),
    }


def execute_trial(api_key: str, base_url: str, model: str, surface: str, replicate: int) -> dict[str, Any]:
    started = datetime.now(timezone.utc).isoformat()
    try:
        if surface == "openai-chat-completions":
            first = openai_turn(
                api_key,
                base_url,
                model,
                [{"role": "system", "content": SYSTEM}, {"role": "user", "content": ROUND1}],
            )
            second = openai_turn(
                api_key,
                base_url,
                model,
                [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": ROUND1},
                    {"role": "assistant", "content": first["text"]},
                    {"role": "user", "content": ROUND2},
                ],
            )
        else:
            first = anthropic_turn(
                api_key,
                model,
                SYSTEM,
                [{"role": "user", "content": ROUND1}],
            )
            second = anthropic_turn(
                api_key,
                model,
                SYSTEM,
                [
                    {"role": "user", "content": ROUND1},
                    {"role": "assistant", "content": first["text"]},
                    {"role": "user", "content": ROUND2},
                ],
            )
        first_value, first_error = extract_json(first["text"])
        second_value, second_error = extract_json(second["text"])
        return {
            "trialId": f"trial:g6:deepseek:{model}:{surface}:r{replicate}",
            "status": "observed",
            "observedAt": started,
            "provider": "deepseek",
            "modelRequested": model,
            "surface": surface,
            "replicate": replicate,
            "semanticRequestDigest": digest({"system": SYSTEM, "round1": ROUND1, "round2": ROUND2}),
            "first": {
                **{k: v for k, v in first.items() if k != "text"},
                "contentDigest": digest(first["text"]),
                "parsed": first_value,
                "parseError": first_error,
                "exactFacts": first_value == FACTS,
            },
            "second": {
                **{k: v for k, v in second.items() if k != "text"},
                "contentDigest": digest(second["text"]),
                "parsed": second_value,
                "parseError": second_error,
                "exactFacts": second_value == FACTS,
            },
            "callerResentHistory": True,
            "serverStateClaimed": False,
            "continuityPassed": first_value == FACTS and second_value == FACTS,
            "error": None,
        }
    except Exception as error:  # evidence must retain failed surfaces
        return {
            "trialId": f"trial:g6:deepseek:{model}:{surface}:r{replicate}",
            "status": "error",
            "observedAt": started,
            "provider": "deepseek",
            "modelRequested": model,
            "surface": surface,
            "replicate": replicate,
            "semanticRequestDigest": digest({"system": SYSTEM, "round1": ROUND1, "round2": ROUND2}),
            "callerResentHistory": True,
            "serverStateClaimed": False,
            "continuityPassed": False,
            "error": {"type": type(error).__name__, "message": str(error)[:4000]},
        }


def main() -> int:
    api_key, base_url = read_secret()
    trials = [
        execute_trial(api_key, base_url, model, surface, replicate)
        for model in MODELS
        for surface in SURFACES
        for replicate in range(1, REPLICATES + 1)
    ]
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.ai-capability-governance.surface-portability-pilot",
        "observedAt": datetime.now(timezone.utc).isoformat(),
        "provider": "deepseek",
        "models": list(MODELS),
        "surfaces": list(SURFACES),
        "replicates": REPLICATES,
        "authorizedSyntheticFacts": FACTS,
        "rawPromptsRetained": False,
        "rawResponsesRetained": False,
        "secretRetained": False,
        "summary": {
            "trials": len(trials),
            "observed": sum(item["status"] == "observed" for item in trials),
            "errors": sum(item["status"] == "error" for item in trials),
            "continuityPassed": sum(bool(item["continuityPassed"]) for item in trials),
        },
        "trials": trials,
        "limitations": [
            "Both surfaces terminate at the same DeepSeek Provider and do not measure cross-Provider exit.",
            "The task is benign and tests serialization/state portability rather than policy strictness.",
            "The caller resends history because both APIs are treated as stateless request interfaces.",
            "Two replicates per cell cannot estimate population failure rates.",
        ],
    }
    result["resultDigest"] = digest(result)
    output = Path("research/data/ai-capability-governance/controlled-observations/deepseek-surface-portability.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["summary"]["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
