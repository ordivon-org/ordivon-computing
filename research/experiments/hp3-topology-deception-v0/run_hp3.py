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
TEXT_SUFFIXES = {".py", ".rs", ".toml", ".md", ".json", ".yml", ".yaml", ".txt"}
TOPOLOGY_CLASSES = [
    "localized_owner_projection_loss",
    "cross_owner_substitution_authority_overlap",
    "distributed_representation_or_dataflow",
    "localized_exact_diagnostic",
    "other_or_uncertain",
]
OPERATOR_CLASSES = [
    "compiled_local",
    "adaptive_relation_following",
    "cross_owner_substitution_check",
    "full_bounded_inspection",
    "other",
]


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


def tools() -> list[dict[str, Any]]:
    return [
        function_tool(
            "search",
            "Literal case-insensitive search of one exact frozen owner repository. Use search to test causal alternatives, not to maximize match count.",
            {
                "repo": {"type": "string"},
                "query": {"type": "string", "maxLength": 240},
                "why": {"type": "string", "maxLength": 600},
            },
            ["repo", "query", "why"],
        ),
        function_tool(
            "read",
            "Read at most 180 numbered lines from one exact frozen owner file.",
            {
                "repo": {"type": "string"},
                "path": {"type": "string", "maxLength": 500},
                "start": {"type": "integer"},
                "end": {"type": "integer"},
                "why": {"type": "string", "maxLength": 600},
            },
            ["repo", "path", "start", "end", "why"],
        ),
        function_tool(
            "submit",
            "Submit the final causal topology judgment and next falsifier, or abstain. Submission ends the trial.",
            {
                "topologyClass": {"type": "string", "enum": TOPOLOGY_CLASSES},
                "surfaceClassDisposition": {"type": "string", "enum": ["accepted", "rejected", "not_provided", "uncertain"]},
                "operatorUsed": {"type": "string", "enum": OPERATOR_CLASSES},
                "switchedOperator": {"type": "boolean"},
                "owner": {"type": "string", "maxLength": 500},
                "hypothesis": {"type": "string"},
                "files": {"type": "array", "items": {"type": "string", "maxLength": 600}, "maxItems": 16},
                "causalMechanism": {"type": "string"},
                "nextFalsifier": {"type": "string"},
                "abstain": {"type": "boolean"},
                "confidence": {"type": "number"},
            },
            [
                "topologyClass",
                "surfaceClassDisposition",
                "operatorUsed",
                "switchedOperator",
                "owner",
                "hypothesis",
                "files",
                "causalMechanism",
                "nextFalsifier",
                "abstain",
                "confidence",
            ],
        ),
    ]


def call_model(messages: list[dict[str, Any]], *, max_tokens: int = 8000, protocol_retry: int = 0) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    secret = load_secret()
    body = {
        "model": secret["model"],
        "messages": messages,
        "tools": tools(),
        "tool_choice": "required",
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": max_tokens,
        "stream": False,
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
    started = time.time_ns()
    transport_retry = 0
    while True:
        req = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=encoded,
            headers={
                "Authorization": "Bearer " + str(secret["apiKey"]),
                "Content-Type": "application/json",
                "User-Agent": "ordivon-computing-hp3/1",
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
            if transport_retry >= 2:
                raise
            transport_retry += 1
            time.sleep(0.75 * transport_retry)
    payload = json.loads(raw)
    usage = payload.get("usage") or {}
    meta = {
        "inputTokens": int(usage.get("prompt_tokens", 0) or 0),
        "outputTokens": int(usage.get("completion_tokens", 0) or 0),
        "totalTokens": int(usage.get("total_tokens", 0) or 0),
        "elapsedMs": (time.time_ns() - started) // 1_000_000,
        "transportRetries": transport_retry,
        "providerProtocolRetries": 0,
    }
    message = payload["choices"][0]["message"]
    calls = message.get("tool_calls")
    parsed: list[dict[str, Any]] = []
    try:
        if not isinstance(calls, list) or not calls:
            raise ValueError("Provider must return one or more Tool calls")
        for call in calls:
            function = call.get("function") if isinstance(call, dict) else None
            if not isinstance(function, dict):
                raise ValueError("invalid Tool call")
            name = str(function.get("name", ""))
            if name not in {"search", "read", "submit"}:
                raise ValueError(f"out-of-catalog Tool {name}")
            arguments = json.loads(str(function.get("arguments", "")))
            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments must be object")
            parsed.append({"id": str(call["id"]), "name": name, "arguments": arguments})
        submit_calls = [call for call in parsed if call["name"] == "submit"]
        if submit_calls and (len(parsed) != 1 or len(submit_calls) != 1):
            raise ValueError("submit must be the sole Tool call in a Provider response")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        diagnostic = ROOT / "diagnostics" / "provider-protocol.jsonl"
        diagnostic.parent.mkdir(parents=True, exist_ok=True)
        with diagnostic.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({
                "protocolRetry": protocol_retry,
                "error": str(error),
                "messagesDigest": canonical_digest(messages),
                "rawToolCalls": calls,
                "usage": meta,
            }, ensure_ascii=False) + "\n")
        if protocol_retry >= 2:
            raise
        calls2, meta2, wire2 = call_model(messages, max_tokens=max_tokens, protocol_retry=protocol_retry + 1)
        for key in ["inputTokens", "outputTokens", "totalTokens", "elapsedMs", "transportRetries"]:
            meta2[key] = int(meta2.get(key, 0) or 0) + int(meta.get(key, 0) or 0)
        meta2["providerProtocolRetries"] = int(meta2.get("providerProtocolRetries", 0) or 0) + 1
        return calls2, meta2, wire2
    assistant_wire = {"role": "assistant", "content": message.get("content"), "tool_calls": calls}
    return parsed, meta, assistant_wire


def zero_usage() -> dict[str, int]:
    return {
        "inputTokens": 0,
        "outputTokens": 0,
        "totalTokens": 0,
        "elapsedMs": 0,
        "transportRetries": 0,
        "providerProtocolRetries": 0,
        "providerCalls": 0,
    }


def add_usage(total: dict[str, int], one: dict[str, Any]) -> None:
    for key in ["inputTokens", "outputTokens", "totalTokens", "elapsedMs", "transportRetries", "providerProtocolRetries"]:
        total[key] += int(one.get(key, 0) or 0)
    total["providerCalls"] += 1


def repo_spec(workload: dict[str, Any], repo: str) -> dict[str, Any] | None:
    value = workload["repos"].get(repo)
    return value if isinstance(value, dict) else None


def allowed_path(spec: dict[str, Any], path: str) -> bool:
    if not path or path.startswith("/") or ".." in Path(path).parts:
        return False
    for root in spec["roots"]:
        if path == root or path.startswith(str(root).rstrip("/") + "/"):
            return True
    return False


def git_catalog(workload: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    for repo, spec in workload["repos"].items():
        args = ["/usr/bin/git", "-C", spec["path"], "ls-tree", "-r", "--name-only", spec["revision"], "--", *spec["roots"]]
        out = subprocess.check_output(args, text=True)
        for line in out.splitlines():
            suffix = Path(line).suffix
            if line in spec["roots"] or suffix in TEXT_SUFFIXES:
                rows.append(f"{repo}:{line}")
    return sorted(rows)


def git_search(workload: dict[str, Any], repo: str, query: str, limit: int = 120) -> str:
    spec = repo_spec(workload, repo)
    if spec is None:
        return "<unknown repo>"
    query = query[:240]
    proc = subprocess.run(
        ["/usr/bin/git", "-C", spec["path"], "grep", "-n", "-i", "-F", query, spec["revision"], "--", *spec["roots"]],
        text=True,
        capture_output=True,
    )
    lines = (proc.stdout or "").splitlines()[:limit]
    return "\n".join(lines) if lines else "<no matches>"


def git_read(workload: dict[str, Any], repo: str, path: str, start: int, end: int) -> str:
    spec = repo_spec(workload, repo)
    if spec is None:
        return "<unknown repo>"
    if not allowed_path(spec, path):
        return "<invalid path>"
    try:
        text = subprocess.check_output(
            ["/usr/bin/git", "-C", spec["path"], "show", f"{spec['revision']}:{path}"],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as error:
        return "<read failed: " + error.output[-1000:] + ">"
    lines = text.splitlines()
    start = max(1, int(start))
    end = min(len(lines), max(start, int(end)), start + 179)
    return "\n".join(f"{i + 1}: {lines[i]}" for i in range(start - 1, end))


def surface_packet(workload: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    total = 0
    for item in workload["surfacePacket"]:
        output = git_search(workload, str(item["repo"]), str(item["query"]), limit=60)
        total += len(output.encode())
        rows.append({"repo": item["repo"], "query": item["query"], "output": output})
    return rows, total


def validate_revisions(battlefield: dict[str, Any]) -> None:
    for workload in battlefield["workloads"]:
        for spec in workload["repos"].values():
            subprocess.check_call(["/usr/bin/git", "-C", spec["path"], "cat-file", "-e", spec["revision"] + "^{commit}"])


def file_hit(submission: dict[str, Any], required: str) -> bool:
    files = submission.get("files")
    blob = json.dumps(submission, ensure_ascii=False).lower()
    if isinstance(files, list) and any(str(item).lower() == required.lower() for item in files):
        return True
    return required.lower() in blob


def score(workload: dict[str, Any], submission: dict[str, Any], treatment: str, observations: int) -> dict[str, Any]:
    blob = json.dumps(submission, ensure_ascii=False).lower()
    required_files = workload["hiddenOracle"]["requiredFiles"]
    file_hits = sum(file_hit(submission, item) for item in required_files)
    topology_correct = submission.get("topologyClass") == workload["trueClass"]
    forbidden: list[str] = []

    if workload["id"] == "SEC-UNKNOWN":
        concepts = {
            "harness_already_represents_unresolved_unknowns": (
                "harness" in blob and "unresolved_unknown" in blob and any(x in blob for x in ["already", "supports", "preserve", "agentrunconclusion", "structured completion"])
            ),
            "security_agent_turn_evidence_has_no_structured_unknown_field": (
                "agentturnevidence" in blob and "security" in blob and "unresolved" in blob and any(x in blob for x in ["lacks", "missing", "no field", "does not", "drops"])
            ),
            "security_cage_prompt_forces_candidate_completed_unknowns_empty": (
                "empty array" in blob and "unresolved" in blob and any(x in blob for x in ["prompt", "candidate_completed", "forces", "must"])
            ),
            "security_host_assigned_return_drops_conclusion_unknowns": (
                "host_assigned" in blob and "result.conclusion" in blob and "unresolved" in blob and any(x in blob for x in ["drops", "not", "only", "rationale", "summary"])
            ),
            "security_runtime_worker_projection_reconstructs_same_loss": (
                "runtime_assigned" in blob and any(x in blob for x in ["_evidence_from_worker", "worker projection", "reconstruct"] ) and "unresolved" in blob
            ),
            "next_falsifier_is_security_local_propagation_against_existing_harness_contract": (
                "security" in blob and "harness" in blob and "unresolved" in blob and any(x in blob for x in ["propagat", "round-trip", "retain", "preserv"]) and any(x in blob for x in ["existing", "already", "no harness core", "without changing harness"])
            ),
        }
        if "change harness core" in blob and any(x in blob for x in ["cannot represent", "does not support", "missing support"]):
            forbidden.append("misassign_harness_core")
        if any(x in blob for x in ["parse the rationale", "infer from rationale", "natural-language rationale authoritative"]):
            forbidden.append("prose_authority")
        if "move security" in blob and "into harness" in blob:
            forbidden.append("move_security_semantics")
        owner_correct = "security" in str(submission.get("owner", "")).lower()
        expected_operator = "compiled_local"
    elif workload["id"] == "NET-DUALAUTH":
        concepts = {
            "world_doctor_still_consumes_old_ordivon_vpn": (
                "world" in blob and "ordivon-vpn" in blob and any(x in blob for x in ["doctor", "/usr/local/sbin", "network_check"])
            ),
            "surfpath_owns_current_multiprotocol_discovery_and_revalidation": (
                "surfpath" in blob and "workstation" in blob and any(x in blob for x in ["multi-protocol", "multiprotocol", "revalidat", "pathdigest"])
            ),
            "ordivon_vpn_still_retains_isolated_wireguard_namespace_key_profile_invariants": (
                "ordivon-vpn" in blob and "wireguard" in blob and any(x in blob for x in ["namespace", "key", "profile"]) and any(x in blob for x in ["still", "retains", "owns", "invariant"])
            ),
            "world_explicitly_defers_deletion_until_workstation_proves_substitution": (
                "world" in blob and "workstation" in blob and any(x in blob for x in ["substitution", "prove", "until", "defer"]) and any(x in blob for x in ["delete", "remove", "retire"])
            ),
            "surfpath_revalidates_observation_path_provider_ingress_config_endpoint_and_destination": (
                "surfpath" in blob and "revalidat" in blob and "provider" in blob and "ingress" in blob and any(x in blob for x in ["config", "pathdigest"]) and any(x in blob for x in ["endpoint", "destination", "re-probe", "reprobe"])
            ),
            "next_falsifier_belongs_to_workstation_substitution_not_world_local_delete": (
                "workstation" in blob and "substitution" in blob and any(x in blob for x in ["falsif", "test", "prove", "coverage"]) and any(x in blob for x in ["namespace", "key", "profile", "cleanup"])
            ),
        }
        if "delete" in blob and "ordivon-vpn" in blob and not any(x in blob for x in ["substitution", "prove", "retain", "cannot", "not yet"]):
            forbidden.append("delete_without_substitution")
        if "redirect" in blob and "surfpath" in blob and not any(x in blob for x in ["substitution", "prove", "coverage"]):
            forbidden.append("redirect_without_proof")
        if "world" in blob and "recommendedpath" in blob and any(x in blob for x in ["choose", "execute", "authority"]):
            forbidden.append("world_path_authority")
        owner_correct = "workstation" in str(submission.get("owner", "")).lower()
        expected_operator = "cross_owner_substitution_check"
    else:
        raise ValueError(workload["id"])

    concept_hits = sum(bool(v) for v in concepts.values())
    operator_correct = submission.get("operatorUsed") == expected_operator
    surface_rejected = submission.get("surfaceClassDisposition") == "rejected" if treatment == "topology_challenge" else None
    switch_correct = bool(submission.get("switchedOperator")) if treatment == "topology_challenge" else None
    raw_score = int(topology_correct) + int(owner_correct) + int(operator_correct) + file_hits + concept_hits - 2 * len(forbidden)
    max_score = 1 + 1 + 1 + len(required_files) + len(concepts)
    success_threshold = max_score - 2
    success = (
        raw_score >= success_threshold
        and topology_correct
        and owner_correct
        and not forbidden
        and not bool(submission.get("abstain"))
    )
    return {
        "score": raw_score,
        "maxScore": max_score,
        "successThreshold": success_threshold,
        "success": success,
        "topologyCorrect": topology_correct,
        "ownerCorrect": owner_correct,
        "operatorCorrect": operator_correct,
        "requiredFileHits": file_hits,
        "concepts": concepts,
        "conceptHits": concept_hits,
        "forbiddenBoundaryHits": forbidden,
        "surfaceRejected": surface_rejected,
        "switchCorrect": switch_correct,
        "falseLocalization": bool(not topology_correct and not submission.get("abstain")),
        "falseStop": bool(not success and observations < 24 and not submission.get("abstain")),
    }


def policy_text(workload: dict[str, Any], treatment: str) -> str:
    if treatment == "surface_locked":
        if workload["surfaceClass"] == "distributed_representation_or_dataflow":
            operator = "Use adaptive semantic relation-following across the named repositories and layers; assume the distributed classification is the correct operating topology."
        else:
            operator = "Use localized exact-diagnostic search and bounded local reads around the visible World doctor seam; assume the localized classification is the correct operating topology."
        return (
            f"A cheap surface classifier has labeled this pressure `{workload['surfaceClass']}`. Treat that label as fixed for this trial. {operator} "
            "Do not spend the budget constructing a new topology classifier. Preserve owner authority and submit the narrowest source-grounded next falsifier."
        )
    if treatment == "topology_challenge":
        return (
            f"A cheap surface classifier has labeled this pressure `{workload['surfaceClass']}`, but this label is deliberately untrusted and may be adversarially misleading. "
            "Treat topology only as a defeasible hypothesis. Before committing to an operator, use owner evidence to seek the cheapest contradiction to the surface label. "
            "If contradicted, switch operator and say so in the final submission. Do not classify by file count, name count, repository count, or the location of one diagnostic alone. "
            "Spend additional compute only when it discriminates causal alternatives or validates the owner boundary."
        )
    if treatment == "open":
        return (
            "Choose your own research operator from the evidence. No topology label is supplied. The preloaded surface packet is intentionally incomplete and may over-emphasize some names. "
            "Localize the current owner-native causal boundary and next falsifier."
        )
    raise ValueError(treatment)


def run_trial(workload: dict[str, Any], treatment: str, replicate: int, max_observations: int = 24) -> dict[str, Any]:
    packet, packet_bytes = surface_packet(workload)
    catalog = git_catalog(workload)
    usage = zero_usage()
    trace: list[dict[str, Any]] = []
    observations = 0
    observed_bytes = 0
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a read-only research Agent on exact frozen owner revisions. You have a generous reasoning budget. "
                "Do not optimize for short answers or minimum tokens. Use additional compute when it improves causal discrimination, owner correctness, verification or the next falsifier. "
                "Use only search/read/submit. Never mutate an owner repository or infer current external state beyond these frozen source revisions. "
                + policy_text(workload, treatment)
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "workloadId": workload["id"],
                    "pressure": workload["pressure"],
                    "repos": {name: {"revision": spec["revision"]} for name, spec in workload["repos"].items()},
                    "catalog": catalog,
                    "preloadedSurfacePacket": packet,
                    "budget": {
                        "maxAdditionalPhysicalObservations": max_observations,
                        "maxReadLines": 180,
                        "maxCompletionTokensPerCall": 8000,
                        "tokenPolicy": "elastic/high; budget is capacity, not an obligation to exhaust evidence",
                    },
                    "submissionRule": "State a causal topology, owner boundary and smallest falsifier. A path/name distribution is not by itself a topology proof.",
                },
                ensure_ascii=False,
            ),
        },
    ]
    submission: dict[str, Any] | None = None
    forced = False
    for turn in range(max_observations + 18):
        calls, one_usage, assistant_wire = call_model(messages, max_tokens=8000)
        add_usage(usage, one_usage)
        if len(calls) == 1 and calls[0]["name"] == "submit":
            submission = dict(calls[0]["arguments"])
            submission["turnAtSubmit"] = turn
            break
        messages.append(assistant_wire)
        for call in calls:
            action = dict(call["arguments"])
            if observations >= max_observations:
                output = "<physical observation ceiling reached; submit or abstain now>"
                messages.append({"role": "tool", "tool_call_id": call["id"], "content": output})
                continue
            if call["name"] == "search":
                output = git_search(workload, str(action.get("repo", "")), str(action.get("query", "")))
            elif call["name"] == "read":
                output = git_read(
                    workload,
                    str(action.get("repo", "")),
                    str(action.get("path", "")),
                    int(action.get("start", 1) or 1),
                    int(action.get("end", 180) or 180),
                )
            else:
                raise RuntimeError("validated non-submit Tool response contained an unexpected Tool")
            observations += 1
            observed_bytes += len(output.encode())
            trace.append({
                "observationIndex": observations,
                "providerTurn": turn,
                "providerCallIndex": len(trace),
                "kind": call["name"],
                "request": action,
                "outputDigest": "sha256:" + hashlib.sha256(output.encode()).hexdigest(),
                "bytes": len(output.encode()),
                "output": output,
            })
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": output})
    if submission is None:
        forced = True
        submission = {
            "topologyClass": "other_or_uncertain",
            "surfaceClassDisposition": "uncertain" if treatment != "open" else "not_provided",
            "operatorUsed": "other",
            "switchedOperator": False,
            "owner": "unknown",
            "hypothesis": "observation ceiling reached without justified causal closure",
            "files": [],
            "causalMechanism": "",
            "nextFalsifier": "reformulate the operator rather than exhaust more of the same evidence",
            "abstain": True,
            "confidence": 0.0,
            "forcedByBudget": True,
        }
    metrics = score(workload, submission, treatment, observations)
    metrics.update({
        "observations": observations,
        "observedBytes": observed_bytes,
        "preloadedSurfaceBytes": packet_bytes,
        "forcedByBudget": forced,
        "tokenUtilizationAcceptedScorePer100k": (
            metrics["score"] * 100000.0 / usage["totalTokens"] if metrics["success"] and usage["totalTokens"] else None
        ),
    })
    return {
        "schemaVersion": 1,
        "kind": "ordivon.computing.hp3-topology-deception-trial",
        "workload": workload["id"],
        "treatment": treatment,
        "replicate": replicate,
        "surfaceClass": workload["surfaceClass"] if treatment != "open" else None,
        "submission": submission,
        "metrics": metrics,
        "usage": usage,
        "trace": trace,
    }


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for workload, treatment in sorted({(r["workload"], r["treatment"]) for r in records}):
        group = [r for r in records if r["workload"] == workload and r["treatment"] == treatment]
        result[f"{workload}:{treatment}"] = {
            "replicates": len(group),
            "successes": sum(bool(r["metrics"]["success"]) for r in group),
            "topologyCorrect": sum(bool(r["metrics"]["topologyCorrect"]) for r in group),
            "ownerCorrect": sum(bool(r["metrics"]["ownerCorrect"]) for r in group),
            "operatorCorrect": sum(bool(r["metrics"]["operatorCorrect"]) for r in group),
            "falseLocalizations": sum(bool(r["metrics"]["falseLocalization"]) for r in group),
            "surfaceRejected": sum(bool(r["metrics"].get("surfaceRejected")) for r in group if r["metrics"].get("surfaceRejected") is not None),
            "switchCorrect": sum(bool(r["metrics"].get("switchCorrect")) for r in group if r["metrics"].get("switchCorrect") is not None),
            "meanScore": sum(float(r["metrics"]["score"]) for r in group) / len(group),
            "meanObservations": sum(float(r["metrics"]["observations"]) for r in group) / len(group),
            "meanObservedBytes": sum(float(r["metrics"]["observedBytes"]) for r in group) / len(group),
            "providerCalls": sum(int(r["usage"]["providerCalls"]) for r in group),
            "totalTokens": sum(int(r["usage"]["totalTokens"]) for r in group),
            "inputTokens": sum(int(r["usage"]["inputTokens"]) for r in group),
            "outputTokens": sum(int(r["usage"]["outputTokens"]) for r in group),
        }
    return result


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["validate", "run"], required=True)
    parser.add_argument("--replicates", type=int, default=3)
    args = parser.parse_args()
    battlefield = json.loads(BATTLEFIELD.read_text())
    validate_revisions(battlefield)
    if args.phase == "validate":
        print(json.dumps({
            "ok": True,
            "battlefieldDigest": canonical_digest(battlefield),
            "workloads": [w["id"] for w in battlefield["workloads"]],
        }, indent=2))
        return 0
    progress = ROOT / "evidence" / "progress"
    records: list[dict[str, Any]] = []
    for workload in battlefield["workloads"]:
        for treatment in ["open", "surface_locked", "topology_challenge"]:
            for replicate in range(1, args.replicates + 1):
                path = progress / f"{workload['id'].lower()}-{treatment}-r{replicate}.json"
                if path.exists():
                    record = json.loads(path.read_text())
                else:
                    record = run_trial(workload, treatment, replicate)
                    write_json(path, record)
                records.append(record)
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.hp3-topology-deception-receipt",
        "battlefieldDigest": canonical_digest(battlefield),
        "replicatesPerCell": args.replicates,
        "records": [
            {
                "workload": r["workload"],
                "treatment": r["treatment"],
                "replicate": r["replicate"],
                "surfaceClass": r["surfaceClass"],
                "submission": r["submission"],
                "metrics": r["metrics"],
                "usage": r["usage"],
            }
            for r in records
        ],
        "aggregate": aggregate(records),
    }
    receipt["payloadDigest"] = canonical_digest(receipt)
    write_json(ROOT / "evidence" / "hp3-live-v1.json", receipt)
    print(json.dumps(receipt["aggregate"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
