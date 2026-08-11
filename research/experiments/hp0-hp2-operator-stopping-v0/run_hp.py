from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
BATTLEFIELD = ROOT / "battlefield-v1.json"
SECRET = Path("/root/.config/ordivon/secrets/deepseek.json")
TEXT_SUFFIXES = {".py", ".rs", ".toml", ".md", ".json", ".yml", ".yaml"}


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def load_secret() -> dict[str, Any]:
    return json.loads(SECRET.read_text())


def function_tool(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        },
    }


def call_tool_model(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    *,
    max_tokens: int = 8000,
    _malformed_retries: int = 0,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    secret = load_secret()
    body = {
        "model": secret["model"],
        "messages": messages,
        "tools": tools,
        "tool_choice": "required",
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": max_tokens,
        "stream": False,
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
    started = time.time_ns()
    retries = 0
    while True:
        req = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=encoded,
            headers={
                "Authorization": "Bearer " + str(secret["apiKey"]),
                "Content-Type": "application/json",
                "User-Agent": "ordivon-computing-hp0-hp2/1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                raw = response.read(8_388_608)
            break
        except urllib.error.HTTPError as error:
            detail = error.read(8192).decode(errors="replace")
            raise RuntimeError(f"Provider HTTP {error.code}: {detail}") from error
        except (http.client.HTTPException, urllib.error.URLError, TimeoutError, OSError):
            if retries >= 2:
                raise
            retries += 1
            time.sleep(0.75 * retries)
    payload = json.loads(raw)
    message = payload["choices"][0]["message"]
    calls = message.get("tool_calls")
    usage = payload.get("usage") or {}
    failed_meta = {
        "model": payload.get("model", secret["model"]),
        "inputTokens": int(usage.get("prompt_tokens", 0) or 0),
        "outputTokens": int(usage.get("completion_tokens", 0) or 0),
        "totalTokens": int(usage.get("total_tokens", 0) or 0),
        "elapsedMs": (time.time_ns() - started) // 1_000_000,
        "transportRetries": retries,
        "malformedResponseRetries": 0,
    }
    if not isinstance(calls, list) or not calls:
        raise ValueError("Provider returned no tool calls")
    parsed: list[dict[str, Any]] = []
    try:
        for call in calls:
            function = call.get("function") if isinstance(call, dict) else None
            if not isinstance(function, dict):
                raise ValueError("invalid tool call")
            args = json.loads(function["arguments"])
            if not isinstance(args, dict):
                raise ValueError("tool arguments must be object")
            parsed.append({"id": call["id"], "name": function["name"], "arguments": args})
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as parse_error:
        diagnostic_path = ROOT / "diagnostics" / "malformed-tool-arguments.jsonl"
        diagnostic_path.parent.mkdir(parents=True, exist_ok=True)
        bad_arguments = None
        try:
            bad_arguments = function.get("arguments") if isinstance(function, dict) else None
        except Exception:
            bad_arguments = None
        diagnostic_record = {
            "malformedRetryIndex": _malformed_retries,
            "error": str(parse_error),
            "toolName": function.get("name") if isinstance(function, dict) else None,
            "arguments": bad_arguments,
            "messagesDigest": canonical_digest(messages),
            "usage": failed_meta,
        }
        with diagnostic_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(diagnostic_record, ensure_ascii=False) + "\n")
        if _malformed_retries >= 2:
            raise
        retry_parsed, retry_meta, retry_wire = call_tool_model(
            messages,
            tools,
            max_tokens=max_tokens,
            _malformed_retries=_malformed_retries + 1,
        )
        retry_meta = dict(retry_meta)
        for key in ["inputTokens", "outputTokens", "totalTokens", "elapsedMs", "transportRetries"]:
            retry_meta[key] = int(retry_meta.get(key, 0) or 0) + int(failed_meta.get(key, 0) or 0)
        retry_meta["malformedResponseRetries"] = int(retry_meta.get("malformedResponseRetries", 0) or 0) + 1
        return retry_parsed, retry_meta, retry_wire
    expected_names = {
        str(tool.get("function", {}).get("name"))
        for tool in tools
        if isinstance(tool, dict) and isinstance(tool.get("function"), dict)
    }
    invalid_names = [call["name"] for call in parsed if call["name"] not in expected_names]
    if invalid_names:
        diagnostic_path = ROOT / "diagnostics" / "unexpected-tool-calls.jsonl"
        diagnostic_path.parent.mkdir(parents=True, exist_ok=True)
        with diagnostic_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "protocolRetryIndex": _malformed_retries,
                        "unexpectedToolNames": invalid_names,
                        "expectedToolNames": sorted(expected_names),
                        "messagesDigest": canonical_digest(messages),
                        "usage": failed_meta,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        if _malformed_retries >= 2:
            raise ValueError("Provider repeatedly returned out-of-catalog Tool names: " + ",".join(invalid_names))
        retry_parsed, retry_meta, retry_wire = call_tool_model(
            messages,
            tools,
            max_tokens=max_tokens,
            _malformed_retries=_malformed_retries + 1,
        )
        retry_meta = dict(retry_meta)
        for key in ["inputTokens", "outputTokens", "totalTokens", "elapsedMs", "transportRetries"]:
            retry_meta[key] = int(retry_meta.get(key, 0) or 0) + int(failed_meta.get(key, 0) or 0)
        retry_meta["providerProtocolRetries"] = int(retry_meta.get("providerProtocolRetries", 0) or 0) + 1
        return retry_parsed, retry_meta, retry_wire
    meta = failed_meta
    assistant_wire = {"role": "assistant", "content": message.get("content"), "tool_calls": calls}
    return parsed, meta, assistant_wire


def allowed_path(workload: dict[str, Any], path: str) -> bool:
    if ".." in path or path.startswith("/"):
        return False
    for root in workload["allowedRoots"]:
        if path == root or path.startswith(root.rstrip("/") + "/"):
            return True
    return False


def git_catalog(workload: dict[str, Any]) -> list[str]:
    args = ["/usr/bin/git", "-C", workload["repo"], "ls-tree", "-r", "--name-only", workload["revision"], "--"] + list(workload["allowedRoots"])
    out = subprocess.check_output(args, text=True)
    result = []
    for line in out.splitlines():
        path = Path(line)
        if line == "pyproject.toml" or path.suffix in TEXT_SUFFIXES:
            result.append(line)
    return result


def git_search(workload: dict[str, Any], query: str, limit: int = 100) -> str:
    query = query[:240]
    args = ["/usr/bin/git", "-C", workload["repo"], "grep", "-n", "-i", "-F", query, workload["revision"], "--"] + list(workload["allowedRoots"])
    proc = subprocess.run(args, text=True, capture_output=True)
    lines = (proc.stdout or "").splitlines()[:limit]
    return "\n".join(lines) if lines else "<no matches>"


def git_read(workload: dict[str, Any], path: str, start: int, end: int) -> str:
    if not allowed_path(workload, path):
        return "<invalid path>"
    try:
        text = subprocess.check_output(
            ["/usr/bin/git", "-C", workload["repo"], "show", f"{workload['revision']}:{path}"],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as error:
        return "<read failed: " + error.output[-1000:] + ">"
    lines = text.splitlines()
    start = max(1, start)
    end = min(len(lines), max(start, end), start + 179)
    return "\n".join(f"{i + 1}: {lines[i]}" for i in range(start - 1, end))


def parse_search_matches(output: str) -> list[tuple[str, int]]:
    result: list[tuple[str, int]] = []
    if output == "<no matches>":
        return result
    for line in output.splitlines():
        parts = line.split(":", 3)
        if len(parts) < 3:
            continue
        if re.fullmatch(r"[0-9a-f]{40}", parts[0]):
            if len(parts) < 4:
                continue
            path, line_text = parts[1], parts[2]
        else:
            path, line_text = parts[0], parts[1]
        try:
            line_no = int(line_text)
        except ValueError:
            continue
        result.append((path, line_no))
    return result


def simple_tools(marginal: bool = False) -> list[dict[str, Any]]:
    common = {
        "why": {"type": "string", "maxLength": 600},
    }
    required_common = ["why"]
    if marginal:
        common.update(
            {
                "alts": {"type": "string", "maxLength": 700},
                "decision": {"type": "string", "maxLength": 500},
                "discriminator": {"type": "string", "maxLength": 500},
                "decisionChange": {"type": "string", "maxLength": 500},
            }
        )
        required_common += ["alts", "decision", "discriminator", "decisionChange"]
    search_props = {"query": {"type": "string", "maxLength": 240}, **common}
    read_props = {
        "path": {"type": "string", "maxLength": 500},
        "start": {"type": "integer"},
        "end": {"type": "integer"},
        **common,
    }
    submit_props: dict[str, Any] = {
        "hypothesis": {"type": "string"},
        "files": {"type": "array", "items": {"type": "string", "maxLength": 500}, "maxItems": 12},
        "causalMechanism": {"type": "string"},
        "nextFalsifier": {"type": "string"},
        "abstain": {"type": "boolean"},
        "confidence": {"type": "number"},
    }
    submit_required = ["hypothesis", "files", "causalMechanism", "nextFalsifier", "abstain", "confidence"]
    if marginal:
        submit_props.update(
            {
                "alts": {"type": "string", "maxLength": 700},
                "remainingDiscriminator": {"type": "string", "maxLength": 600},
                "stopReason": {"type": "string", "maxLength": 600},
            }
        )
        submit_required += ["alts", "remainingDiscriminator", "stopReason"]
    return [
        function_tool("search", "Literal case-insensitive search of the exact frozen owner tree. For marginal stopping, alts is a compact plain-text list of live alternatives; decision is the current causal decision; discriminator says why this observation can separate alternatives; decisionChange says what result would change the decision. Keep these audit fields concise and do not paste source excerpts into them.", search_props, ["query", *required_common]),
        function_tool("read", "Read at most 180 numbered lines from one exact frozen owner file. For marginal stopping, alts is a compact plain-text list of live alternatives; decision is the current causal decision; discriminator says why this observation can separate alternatives; decisionChange says what result would change the decision. Keep these audit fields concise and do not paste source excerpts into them.", read_props, ["path", "start", "end", *required_common]),
        function_tool("submit", "Submit a causal localization or explicit abstention. Submission ends the trial. For marginal stopping, alts names remaining live alternatives, remainingDiscriminator names any affordable observation that could still change the decision or 'none', and stopReason explains why stopping is justified. Detailed causal evidence belongs in hypothesis/causalMechanism/nextFalsifier.", submit_props, submit_required),
    ]


def submit_only_tool() -> list[dict[str, Any]]:
    return [
        function_tool(
            "submit",
            "Submit a causal localization or explicit abstention from the compiled evidence.",
            {
                "hypothesis": {"type": "string"},
                "files": {"type": "array", "items": {"type": "string"}},
                "causalMechanism": {"type": "string"},
                "nextFalsifier": {"type": "string"},
                "abstain": {"type": "boolean"},
                "confidence": {"type": "number"},
            },
            ["hypothesis", "files", "causalMechanism", "nextFalsifier", "abstain", "confidence"],
        )
    ]


def score_submission(workload: dict[str, Any], submission: dict[str, Any]) -> dict[str, Any]:
    blob = json.dumps(submission, ensure_ascii=False).lower()
    files = [str(x) for x in submission.get("files", [])] if isinstance(submission.get("files"), list) else []
    file_hits = sum(path in files or path.lower() in blob for path in workload["hiddenOracle"]["requiredFiles"])
    forbidden = [phrase for phrase in workload["hiddenOracle"]["forbidden"] if phrase.lower() in blob]
    if workload["id"] == "H-PACKAGE":
        concepts = {
            "mcp_is_an_unconditional_project_dependency": (
                "pyproject" in blob and "mcp" in blob and any(x in blob for x in ["unconditional", "dependencies", "required dependency", "install dependency"])
            ),
            "mcp_server_is_a_separate_console_entrypoint_and_direct_mcp_import_carrier": (
                "mcp_server" in blob and any(x in blob for x in ["entrypoint", "console", "script"]) and "mcp" in blob
            ),
            "core_semantic_compatibility_is_not_the_current_failure": (
                "44/44" in blob or ("semantic" in blob and any(x in blob for x in ["compatible", "not the blocker", "not the failure"]))
            ),
            "next_falsifier_is_package_import_dependency_graph_not_world_semantics": (
                any(x in blob for x in ["dependency graph", "install graph", "optional extra", "import-time", "package metadata"]) and "world" in blob
            ),
        }
        max_score = 6
        success_threshold = 5
    elif workload["id"] == "R-WININPUT":
        concepts = {
            "execbound_reaches_run_task_proposal_with_inputs": (
                "workspace.execbound" in blob and any(x in blob for x in ["run_task_proposal_with_inputs", "bind_bound"])
            ),
            "input_bound_admission_rejects_windows_native_before_materialization_dispatch": (
                "windows_native" in blob and "not implemented" in blob and any(x in blob for x in ["admit_new_task_with_inputs", "before material", "admission"])
            ),
            "immutable_inputs_require_contained_local_but_windows_native_requires_trusted_local": (
                "contained_local" in blob and "trusted_local" in blob and "windows" in blob
            ),
            "local_linux_dispatch_has_input_set_presentation_while_windows_dispatch_has_no_equivalent_input_presentation": (
                any(x in blob for x in ["input_set_path", "input set", "input presentation"]) and "windows" in blob and any(x in blob for x in ["launcher", "dispatch", "no equivalent", "missing"])
            ),
            "existing_job_replay_precedes_current_input_authority_or_policy_checks": (
                "replay" in blob and any(x in blob for x in ["existing job", "idempotent", "before consulting", "before current"])
            ),
        }
        max_score = 7
        success_threshold = 6
    else:
        raise ValueError(workload["id"])
    score = file_hits + sum(bool(v) for v in concepts.values()) - 2 * len(forbidden)
    return {
        "score": score,
        "maxScore": max_score,
        "successThreshold": success_threshold,
        "success": score >= success_threshold and not forbidden and not bool(submission.get("abstain")),
        "requiredFileHits": file_hits,
        "concepts": concepts,
        "forbiddenBoundaryHits": forbidden,
        "abstain": bool(submission.get("abstain")),
    }


def usage_zero() -> dict[str, int]:
    return {"inputTokens": 0, "outputTokens": 0, "totalTokens": 0, "elapsedMs": 0, "transportRetries": 0, "providerCalls": 0}


def add_usage(total: dict[str, int], usage: dict[str, Any]) -> None:
    for key in ["inputTokens", "outputTokens", "totalTokens", "elapsedMs", "transportRetries"]:
        total[key] += int(usage.get(key, 0) or 0)
    total["providerCalls"] += 1


def record_observation(trace: list[dict[str, Any]], *, index: int, kind: str, request: dict[str, Any], output: str) -> None:
    encoded = output.encode()
    trace.append(
        {
            "observationIndex": index,
            "kind": kind,
            "request": request,
            "bytes": len(encoded),
            "digest": "sha256:" + hashlib.sha256(encoded).hexdigest(),
            "output": output,
        }
    )


def seed_evidence(workload: dict[str, Any], trace: list[dict[str, Any]]) -> tuple[int, int, str]:
    observations = 0
    observed_bytes = 0
    rendered: list[str] = []
    for anchor in workload["anchors"]:
        output = git_search(workload, anchor)
        observations += 1
        observed_bytes += len(output.encode())
        record_observation(trace, index=observations, kind="seed_search", request={"query": anchor}, output=output)
        rendered.append(f"ANCHOR {anchor}\n{output}")
    return observations, observed_bytes, "\n\n".join(rendered)


def adaptive_trial(
    workload: dict[str, Any],
    *,
    treatment: str,
    replicate: int,
    max_observations: int,
    seed: bool,
    marginal: bool,
    policy_text: str,
) -> dict[str, Any]:
    catalog = git_catalog(workload)
    trace: list[dict[str, Any]] = []
    observations = 0
    observed_bytes = 0
    usage = usage_zero()
    system = (
        "You are a read-only research Agent on an exact frozen owner revision. You have a generous reasoning budget. "
        "Spend tokens when they integrate evidence, discriminate live hypotheses, or improve the next falsifier; do not optimize for short answers. "
        "Use only search/read/submit. Preserve the owner boundary. " + policy_text
    )
    if marginal:
        system += (
            " Before every observation, explicitly name the still-live alternatives, current decision, why this observation discriminates them, and what result would change the decision. "
            "Stop only when you cannot name an affordable observation expected to change the causal decision; confidence alone is not a stop rule."
        )
    prompt = {
        "workload": workload["id"],
        "pressure": workload["pressure"],
        "sourceRevision": workload["revision"],
        "catalog": catalog,
        "budget": {
            "maxPhysicalObservations": max_observations,
            "maxReadLines": 180,
            "providerCompletionBudgetPerTurn": 8000,
            "tokenPolicy": "elastic; total-token minimization is not the objective",
        },
        "rule": "Submit only a source-grounded causal localization and next physical falsifier, or abstain if evidence cannot justify one.",
    }
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
    ]
    if seed:
        observations, observed_bytes, rendered = seed_evidence(workload, trace)
        messages.append(
            {
                "role": "user",
                "content": "PRECOMPUTED OWNER-EVIDENCE OBSERVATIONS. These are already counted against the same physical evidence ceiling:\n" + rendered,
            }
        )
    submission: dict[str, Any] | None = None
    for turn in range(max_observations + 16):
        calls, one_usage, assistant_wire = call_tool_model(messages, simple_tools(marginal), max_tokens=8000)
        add_usage(usage, one_usage)
        allowed = {"search", "read", "submit"}
        if any(call["name"] not in allowed for call in calls):
            raise ValueError("unexpected tool call")
        submit_calls = [call for call in calls if call["name"] == "submit"]
        if submit_calls:
            submission = dict(submit_calls[0]["arguments"])
            submission["parallelCallCountAtSubmit"] = len(calls)
            submission["turnAtSubmit"] = turn
            break
        messages.append(assistant_wire)
        for call in calls:
            action = dict(call["arguments"])
            if observations >= max_observations:
                output = "<physical observation ceiling reached; submit or abstain now>"
                kind = "budget_notice"
            elif call["name"] == "search":
                output = git_search(workload, str(action.get("query", "")))
                observations += 1
                observed_bytes += len(output.encode())
                kind = "search"
                record_observation(trace, index=observations, kind=kind, request=action, output=output)
            elif call["name"] == "read":
                output = git_read(
                    workload,
                    str(action.get("path", "")),
                    int(action.get("start", 1) or 1),
                    int(action.get("end", 180) or 180),
                )
                observations += 1
                observed_bytes += len(output.encode())
                kind = "read"
                record_observation(trace, index=observations, kind=kind, request=action, output=output)
            else:
                output = "<invalid non-submit tool>"
                kind = "invalid"
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": output})
    forced = submission is None
    if submission is None:
        submission = {
            "hypothesis": "physical observation ceiling reached without a justified submission",
            "files": [],
            "causalMechanism": "",
            "nextFalsifier": "reformulate the research policy rather than extending the same search",
            "abstain": True,
            "confidence": 0.0,
            "forcedByBudget": True,
        }
    score = score_submission(workload, submission)
    first_full_file_coverage: int | None = None
    required = set(workload["hiddenOracle"]["requiredFiles"])
    seen: set[str] = set()
    for item in trace:
        output = item.get("output", "")
        request_path = str(item.get("request", {}).get("path", ""))
        for path in required:
            if path == request_path or path in output:
                seen.add(path)
        if seen == required and first_full_file_coverage is None:
            first_full_file_coverage = int(item["observationIndex"])
    score.update(
        {
            "observations": observations,
            "observedBytes": observed_bytes,
            "firstRequiredFileCoverageObservation": first_full_file_coverage,
            "postRequiredFileCoverageObservations": None if first_full_file_coverage is None else observations - first_full_file_coverage,
            "forcedByBudget": forced,
            "falseStop": bool(not score["success"] and not forced and observations < max_observations),
            "tokenUtilizationScorePer100k": (score["score"] * 100000.0 / usage["totalTokens"]) if usage["totalTokens"] else 0.0,
        }
    )
    return {
        "phase": "hp2" if marginal or treatment.startswith("hp2") else "hp1",
        "workload": workload["id"],
        "treatment": treatment,
        "replicate": replicate,
        "submission": submission,
        "metrics": score,
        "usage": usage,
        "trace": trace,
    }


def compile_evidence(workload: dict[str, Any], max_observations: int) -> dict[str, Any]:
    search_items: list[dict[str, Any]] = []
    stats: dict[str, dict[str, Any]] = {}
    observations = 0
    observed_bytes = 0
    for anchor_index, anchor in enumerate(workload["anchors"]):
        output = git_search(workload, anchor)
        observations += 1
        observed_bytes += len(output.encode())
        search_items.append({"anchor": anchor, "output": output})
        for path, line in parse_search_matches(output):
            if not allowed_path(workload, path):
                continue
            entry = stats.setdefault(path, {"path": path, "anchors": set(), "hits": 0, "firstLine": line})
            entry["anchors"].add(anchor_index)
            entry["hits"] += 1
            entry["firstLine"] = min(entry["firstLine"], line)
    ranked = sorted(stats.values(), key=lambda x: (-len(x["anchors"]), -x["hits"], x["path"]))
    windows: list[dict[str, Any]] = []
    remaining = max(0, max_observations - observations)
    for item in ranked[:remaining]:
        output = git_read(workload, item["path"], max(1, item["firstLine"] - 70), item["firstLine"] + 109)
        observations += 1
        observed_bytes += len(output.encode())
        windows.append({"path": item["path"], "centerLine": item["firstLine"], "output": output})
    return {
        "searches": search_items,
        "windows": windows,
        "observations": observations,
        "observedBytes": observed_bytes,
        "rankedPaths": [x["path"] for x in ranked],
    }


def compiled_trial(workload: dict[str, Any], *, treatment: str, replicate: int, max_observations: int) -> dict[str, Any]:
    evidence = compile_evidence(workload, max_observations)
    packet = {
        "workload": workload["id"],
        "pressure": workload["pressure"],
        "sourceRevision": workload["revision"],
        "operatorPolicy": "deterministic identity-preserving literal searches; rank files by distinct anchor coverage then hit count; bounded local read windows; one semantic synthesis",
        "tokenPolicy": "Use a large synthesis budget if useful; total-token minimization is not an objective.",
        "literalSearches": evidence["searches"],
        "boundedReadWindows": evidence["windows"],
        "rule": "Use only this exact compiled evidence. Submit causal localization only if justified; otherwise abstain. Preserve owner authority and propose only the next falsifier, not a product mutation.",
    }
    calls, usage, _ = call_tool_model(
        [
            {"role": "system", "content": "You are the semantic synthesis stage after deterministic evidence compilation. You have a generous reasoning budget. Use submit exactly once."},
            {"role": "user", "content": json.dumps(packet, ensure_ascii=False)},
        ],
        submit_only_tool(),
        max_tokens=8000,
    )
    submission = dict(calls[0]["arguments"])
    score = score_submission(workload, submission)
    score.update(
        {
            "observations": evidence["observations"],
            "observedBytes": evidence["observedBytes"],
            "compiledReadPaths": [x["path"] for x in evidence["windows"]],
            "falseStop": bool(not score["success"] and evidence["observations"] < max_observations),
            "forcedByBudget": False,
            "tokenUtilizationScorePer100k": (score["score"] * 100000.0 / int(usage.get("totalTokens", 0) or 1)),
        }
    )
    usage_total = usage_zero()
    add_usage(usage_total, usage)
    return {
        "phase": "hp1",
        "workload": workload["id"],
        "treatment": treatment,
        "replicate": replicate,
        "submission": submission,
        "metrics": score,
        "usage": usage_total,
        "evidencePlan": {
            "searches": [{"anchor": x["anchor"], "digest": "sha256:" + hashlib.sha256(x["output"].encode()).hexdigest()} for x in evidence["searches"]],
            "readPaths": [x["path"] for x in evidence["windows"]],
            "rankedPaths": evidence["rankedPaths"],
        },
    }


def load_battlefield() -> dict[str, Any]:
    return json.loads(BATTLEFIELD.read_text())


def validate_frozen_revisions(battlefield: dict[str, Any]) -> None:
    for workload in battlefield["workloads"]:
        subprocess.check_call(["/usr/bin/git", "-C", workload["repo"], "cat-file", "-e", workload["revision"] + "^{commit}"])


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    keys = sorted({(r["workload"], r["treatment"]) for r in records})
    for workload, treatment in keys:
        group = [r for r in records if r["workload"] == workload and r["treatment"] == treatment]
        result[f"{workload}:{treatment}"] = {
            "replicates": len(group),
            "successes": sum(bool(r["metrics"]["success"]) for r in group),
            "falseStops": sum(bool(r["metrics"].get("falseStop")) for r in group),
            "meanScore": sum(float(r["metrics"]["score"]) for r in group) / len(group),
            "meanObservations": sum(float(r["metrics"]["observations"]) for r in group) / len(group),
            "meanObservedBytes": sum(float(r["metrics"]["observedBytes"]) for r in group) / len(group),
            "providerCalls": sum(int(r["usage"]["providerCalls"]) for r in group),
            "totalTokens": sum(int(r["usage"]["totalTokens"]) for r in group),
            "inputTokens": sum(int(r["usage"]["inputTokens"]) for r in group),
            "outputTokens": sum(int(r["usage"]["outputTokens"]) for r in group),
            "meanTokenUtilizationScorePer100k": sum(float(r["metrics"]["tokenUtilizationScorePer100k"]) for r in group) / len(group),
        }
    return result


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def run_hp1(battlefield: dict[str, Any], replicates: int) -> dict[str, Any]:
    progress_dir = ROOT / "evidence" / "hp1-progress"
    records: list[dict[str, Any]] = []
    for workload in battlefield["workloads"]:
        for treatment in ["open", "rfm_selected", "wrong_operator"]:
            for replicate in range(1, replicates + 1):
                path = progress_dir / f"{workload['id'].lower()}-{treatment}-r{replicate}.json"
                if path.exists():
                    record = json.loads(path.read_text())
                else:
                    if workload["id"] == "H-PACKAGE":
                        if treatment == "rfm_selected":
                            record = compiled_trial(workload, treatment=treatment, replicate=replicate, max_observations=16)
                        elif treatment == "wrong_operator":
                            record = adaptive_trial(
                                workload,
                                treatment=treatment,
                                replicate=replicate,
                                max_observations=24,
                                seed=True,
                                marginal=False,
                                policy_text="Deliberately use the distributed-relation policy: follow semantic/import relations adaptively even if evidence appears locally concentrated.",
                            )
                        else:
                            record = adaptive_trial(workload, treatment=treatment, replicate=replicate, max_observations=24, seed=False, marginal=False, policy_text="Choose your own research operations.")
                    else:
                        if treatment == "rfm_selected":
                            record = adaptive_trial(
                                workload,
                                treatment=treatment,
                                replicate=replicate,
                                max_observations=24,
                                seed=True,
                                marginal=False,
                                policy_text="Use initial exact owner-evidence anchors only to contract the frontier, then adaptively follow semantic relations across request binding, Core admission/profile validation, immutable-input presentation and Windows dispatch.",
                            )
                        elif treatment == "wrong_operator":
                            record = compiled_trial(workload, treatment=treatment, replicate=replicate, max_observations=16)
                        else:
                            record = adaptive_trial(workload, treatment=treatment, replicate=replicate, max_observations=24, seed=False, marginal=False, policy_text="Choose your own research operations.")
                    write_json(path, record)
                records.append(record)
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.hp1-operator-transfer-receipt",
        "battlefieldDigest": canonical_digest(battlefield),
        "replicatesPerCell": replicates,
        "records": [{"workload": r["workload"], "treatment": r["treatment"], "replicate": r["replicate"], "metrics": r["metrics"], "usage": r["usage"]} for r in records],
        "aggregate": aggregate(records),
    }
    receipt["payloadDigest"] = canonical_digest(receipt)
    write_json(ROOT / "evidence" / "hp1-live-v1.json", receipt)
    return receipt


def run_hp2(battlefield: dict[str, Any], replicates: int) -> dict[str, Any]:
    progress_dir = ROOT / "evidence" / "hp2-progress"
    records: list[dict[str, Any]] = []
    for workload in battlefield["workloads"]:
        for treatment in ["high_budget_open", "marginal_value_stop"]:
            for replicate in range(1, replicates + 1):
                path = progress_dir / f"{workload['id'].lower()}-{treatment}-r{replicate}.json"
                if path.exists():
                    record = json.loads(path.read_text())
                else:
                    marginal = treatment == "marginal_value_stop"
                    record = adaptive_trial(
                        workload,
                        treatment="hp2_" + treatment,
                        replicate=replicate,
                        max_observations=32,
                        seed=True,
                        marginal=marginal,
                        policy_text=(
                            "Use the current TM4 topology prior only as a defeasible initial hypothesis. Switch operator if observations contradict it."
                            if marginal
                            else "Use a generous evidence budget and ordinary adaptive research. You may submit whenever you believe the causal decision is justified."
                        ),
                    )
                    write_json(path, record)
                records.append(record)
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.hp2-marginal-stopping-receipt",
        "battlefieldDigest": canonical_digest(battlefield),
        "replicatesPerCell": replicates,
        "records": [{"workload": r["workload"], "treatment": r["treatment"], "replicate": r["replicate"], "metrics": r["metrics"], "usage": r["usage"]} for r in records],
        "aggregate": aggregate(records),
    }
    receipt["payloadDigest"] = canonical_digest(receipt)
    write_json(ROOT / "evidence" / "hp2-live-v1.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["validate", "hp1", "hp2"], required=True)
    parser.add_argument("--replicates", type=int, default=3)
    args = parser.parse_args()
    battlefield = load_battlefield()
    validate_frozen_revisions(battlefield)
    if args.phase == "validate":
        print(json.dumps({"ok": True, "battlefieldDigest": canonical_digest(battlefield), "workloads": [w["id"] for w in battlefield["workloads"]]}, indent=2))
        return 0
    if args.phase == "hp1":
        print(json.dumps(run_hp1(battlefield, args.replicates)["aggregate"], indent=2))
        return 0
    print(json.dumps(run_hp2(battlefield, args.replicates)["aggregate"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
