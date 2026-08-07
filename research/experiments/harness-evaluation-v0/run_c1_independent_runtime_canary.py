#!/usr/bin/env python3
"""Run the bounded C1 independent Harness -> Runtime real-model canary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def git_revision(root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, encoding="utf-8"
    ).strip()


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def _prepare_imports(harness_root: Path, runtime_root: Path) -> None:
    computing_root = Path(__file__).resolve().parents[3]
    for source in (
        computing_root / "packages" / "ordivon-protocol" / "src",
        harness_root / "src",
        runtime_root / "scripts",
    ):
        text = str(source)
        if text not in sys.path:
            sys.path.insert(0, text)


class EvaluationMcpRuntimeClient:
    """Evaluation-local adapter; not a Harness product transport."""

    def __init__(self, client: object, *, inject_first_patch_response_loss: bool) -> None:
        from ordivon_harness.runtime_port import HarnessRuntimeClientError

        self._client = client
        self._client_error = HarnessRuntimeClientError
        self.inject_first_patch_response_loss = inject_first_patch_response_loss
        self.patch_calls = 0
        self.injected_patch_response_loss = False

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        from ordivon_harness.runtime_port import (
            HarnessRuntimeErrorDetail,
            HarnessRuntimeToolRejected,
        )

        try:
            status, message, _ = self._client.exchange(
                "tools/call", {"name": name, "arguments": arguments}
            )
        except Exception as error:
            raise self._client_error(f"MCP transport failed: {error}") from error
        protocol_error = message.get("error")
        if status >= 400 or isinstance(protocol_error, dict):
            raise self._client_error(
                f"MCP tools/call failed with HTTP {status}: {protocol_error or message}"
            )
        result = message.get("result")
        if not isinstance(result, dict):
            raise self._client_error("MCP tools/call response lacks an object result")
        structured = result.get("structuredContent")
        if not isinstance(structured, dict):
            raise self._client_error(f"Runtime Tool {name} omitted structuredContent")
        if result.get("isError") is True:
            error = structured.get("error")
            if not isinstance(error, dict):
                raise self._client_error(
                    f"Runtime Tool {name} returned an unstructured error"
                )
            code = error.get("code")
            message_text = error.get("message")
            commit_state = error.get("commitState")
            retryable = error.get("retryable", False)
            field = error.get("field")
            if (
                isinstance(code, str)
                and isinstance(message_text, str)
                and isinstance(commit_state, str)
                and type(retryable) is bool
                and (field is None or isinstance(field, str))
            ):
                raise HarnessRuntimeToolRejected(
                    name,
                    HarnessRuntimeErrorDetail(
                        code=code,
                        message=message_text,
                        commit_state=commit_state,
                        retryable=retryable,
                        field=field,
                    ),
                )
            raise self._client_error(
                f"Runtime Tool {name} returned an unsupported error envelope"
            )
        if name == "workspace.patch":
            self.patch_calls += 1
            if (
                self.inject_first_patch_response_loss
                and not self.injected_patch_response_loss
            ):
                self.injected_patch_response_loss = True
                raise self._client_error(
                    "C1 injected response loss after committed workspace.patch"
                )
        return dict(structured)


def _initialize_source(fixture_root: Path, replica: int) -> tuple[Path, str]:
    source = Path(tempfile.mkdtemp(prefix=f"ordivon-c1-r{replica}-source-"))
    for name in ("SPEC.md", "allocation.py", "test_allocation.py"):
        shutil.copy2(fixture_root / name, source / name)
    (source / "artifacts").mkdir()
    (source / "artifacts" / ".gitkeep").write_text("", encoding="utf-8")
    for command in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "c1-canary@example.invalid"],
        ["git", "config", "user.name", "C1 Canary"],
        ["git", "add", "."],
        ["git", "commit", "-qm", "frozen C1 fixture"],
    ):
        subprocess.run(command, cwd=source, check=True)
    return source, git_revision(source)


def _verify_candidate(
    *,
    candidate_content: str,
    fixture_root: Path,
    hidden_verifier: Path,
) -> tuple[bool, bool]:
    directory = Path(tempfile.mkdtemp(prefix="ordivon-c1-verifier-"))
    try:
        shutil.copy2(fixture_root / "test_allocation.py", directory / "test_allocation.py")
        (directory / "allocation.py").write_text(candidate_content, encoding="utf-8")
        environment = {
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "ORDIVON_EVAL_WORKSPACE": str(directory),
        }
        visible = subprocess.run(
            [sys.executable, "-m", "unittest", "-q", "test_allocation.py"],
            cwd=directory,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            check=False,
        )
        hidden = subprocess.run(
            [sys.executable, str(hidden_verifier)],
            cwd=directory,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            check=False,
        )
        return visible.returncode == 0, hidden.returncode == 0
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def run_replica(
    *,
    replica: int,
    computing_root: Path,
    harness_root: Path,
    runtime_root: Path,
    runtime_client: object,
    secret_file: Path,
    state_parent: Path,
    runtime_binary: Path,
) -> dict[str, Any]:
    from anc_canonical import canonical_digest
    from ordivon_harness.core_contracts import HarnessBoundReference, HarnessRunContract
    from ordivon_harness.execution_binding import (
        HarnessExecutionBinding,
        HarnessRuntimeReference,
    )
    from ordivon_harness.ordivon.deepseek import DeepSeekSettings, DeepSeekTurnAdapter
    from ordivon_harness.ordivon.loop import RunBudget
    from ordivon_harness.ordivon.sqlite_repository_repair_bridge import (
        INDEPENDENT_REPOSITORY_REPAIR_EDIT_TOOL_GRANT_DIGEST,
        INDEPENDENT_REPOSITORY_REPAIR_EDIT_TOOL_SURFACE_DIGEST,
        SQLiteHarnessRepositoryRepairEditRuntimeBridge,
    )
    from ordivon_harness.ordivon.sqlite_run_store import SQLiteHarnessRunContinuityStore
    from ordivon_harness.sqlite_store import SQLiteHarnessStore
    from ordivon_harness.standalone import StandaloneHarnessRunner

    fixture_root = harness_root / "fixtures" / "harness-replacement-repository-repair-v1"
    hidden_verifier = (
        harness_root / "evals" / "harness-repository-repair-001" / "verifier" / "test_outcome.py"
    )
    task = json.loads(
        (harness_root / "evals" / "harness-repository-repair-001" / "task.json").read_text(
            encoding="utf-8"
        )
    )
    source, source_revision = _initialize_source(fixture_root, replica)
    timestamp = f"{int(time.time())}-{os.getpid()}-r{replica}"
    workspace_id = f"c1-independent-{timestamp}"
    harness_run_id = f"harness-run:c1-independent-{timestamp}"
    state_root = state_parent / f"replica-{replica}"
    if state_root.exists():
        raise ValueError(f"state root already exists: {state_root}")
    state_root.mkdir(parents=True, mode=0o700)
    opened = False
    store = None
    try:
        runtime_client.call_tool(
            "workspace.open",
            {
                "schemaVersion": 1,
                "sourceRepo": str(source),
                "sourceRevision": source_revision,
                "workspaceId": workspace_id,
            },
        )
        opened = True
        prompt = (
            "Repair allocation.py according to SPEC.md. Work only through admitted tools. "
            "Read allocation.py before editing. Implement the full largest-remainder behavior, "
            "then create artifacts/completion.json with a concise JSON completion claim, run "
            "visible-tests, inspect the diff, and reread allocation.py. Only then submit "
            "candidate_completed. The required artifact reference is "
            f"workspace-artifact:{workspace_id}:artifacts/completion.json. "
            "Do not modify SPEC.md or test_allocation.py."
        )
        system_material = {
            "schemaVersion": 1,
            "kind": "ordivon.c1-system-material",
            "computingRevision": git_revision(computing_root),
            "harnessRevision": git_revision(harness_root),
            "runtimeRepositoryRevision": git_revision(runtime_root),
            "runtimeBinaryDigest": file_digest(runtime_binary),
            "provider": "deepseek",
            "model": "deepseek-v4-flash",
            "fixtureDigest": task["initialState"]["environmentDigest"],
            "replicaPolicy": "fixed-3",
        }
        system_digest = canonical_digest(system_material)
        budget = RunBudget(
            max_model_calls=8,
            max_tool_calls=12,
            max_observation_bytes=1_048_576,
            max_wall_time_ms=300_000,
            max_total_tokens=120_000,
            max_model_retries=1,
            max_tool_corrections=4,
            max_observation_only_turns=6,
            max_no_progress_turns=4,
            max_model_observation_bytes=65_536,
        )
        now_ms = time.time_ns() // 1_000_000
        contract = HarnessRunContract(
            harness_run_id=harness_run_id,
            harness_implementation_id=f"ordivon-harness@{system_material['harnessRevision']}",
            caller_id="caller:ordivon-computing-evaluation",
            caller_run_ref=f"trial:c1:{replica}:{timestamp}",
            objective_ref=HarnessBoundReference(
                f"objective:{task['taskId']}:v{task['taskVersion']}",
                "evaluation-objective",
                canonical_digest(
                    {
                        "taskId": task["taskId"],
                        "taskVersion": task["taskVersion"],
                        "objective": task["objective"],
                    }
                ),
            ),
            context_refs=(
                HarnessBoundReference(
                    f"context:c1:{replica}:{timestamp}",
                    "evaluation-context",
                    canonical_digest(
                        {
                            "prompt": prompt,
                            "fixtureEnvironmentDigest": task["initialState"]["environmentDigest"],
                        }
                    ),
                ),
            ),
            provider_id="provider:deepseek",
            adapter_id=DeepSeekTurnAdapter.adapter_id,
            requested_model_id="deepseek-v4-flash",
            tool_catalog_digest=INDEPENDENT_REPOSITORY_REPAIR_EDIT_TOOL_SURFACE_DIGEST,
            tool_grant_digest=INDEPENDENT_REPOSITORY_REPAIR_EDIT_TOOL_GRANT_DIGEST,
            budget=budget.to_contract_dict(),
            completion_contract={
                "mode": "proposal",
                "requiredArtifact": "artifacts/completion.json",
                "visibleCheck": "visible-tests",
            },
            system_manifest_ref=HarnessBoundReference(
                f"system-manifest:c1:{replica}:{timestamp}",
                "system-manifest",
                system_digest,
            ),
            created_at_ms=now_ms,
            source_refs=(
                HarnessBoundReference(
                    f"fixture:{task['taskId']}:v{task['taskVersion']}",
                    "evaluation-fixture",
                    task["initialState"]["environmentDigest"],
                ),
            ),
            deadline_ms=now_ms + 300_000,
        )
        store = SQLiteHarnessStore.initialize(state_root)
        store.create_run(contract)
        continuity = SQLiteHarnessRunContinuityStore(
            store,
            contract,
            clock_ms=lambda: time.time_ns() // 1_000_000,
        )
        binding = continuity.binding
        references = tuple(
            sorted(
                (
                    HarnessRuntimeReference(
                        "ordivon.harness",
                        "harness_run",
                        harness_run_id,
                        str(binding.assignment_generation),
                        binding.digest,
                    ),
                    HarnessRuntimeReference(
                        "ordivon.harness",
                        "run_contract",
                        f"harness-run-contract:{contract.digest[7:31]}",
                        "1",
                        contract.digest,
                    ),
                    HarnessRuntimeReference(
                        "ordivon.harness",
                        "tool_grant",
                        f"tool-grant:{contract.tool_grant_digest[7:31]}",
                        "1",
                        contract.tool_grant_digest,
                    ),
                ),
                key=lambda item: item.sort_key,
            )
        )
        execution_binding = HarnessExecutionBinding(
            harness_run_id=harness_run_id,
            workspace_ref=workspace_id,
            assignment_id=binding.assignment_id,
            assignment_generation=binding.assignment_generation,
            assignment_digest=binding.assignment_digest,
            runtime_binding_digest=canonical_digest(
                {
                    "harnessRunId": harness_run_id,
                    "workspaceId": workspace_id,
                    "sourceRevision": source_revision,
                }
            ),
            tool_catalog_digest=contract.tool_catalog_digest,
            tool_grant_digest=contract.tool_grant_digest,
            deadline_ms=contract.deadline_ms,
            runtime_references=references,
        )
        adapter_client = EvaluationMcpRuntimeClient(
            runtime_client,
            inject_first_patch_response_loss=True,
        )
        bridge = SQLiteHarnessRepositoryRepairEditRuntimeBridge(
            contract,
            continuity,
            execution_binding,
            adapter_client,
        )
        adapter = DeepSeekTurnAdapter(
            DeepSeekSettings.from_secret_file(
                secret_file,
                timeout_seconds=60.0,
                max_output_tokens=4_096,
            )
        )
        runner = StandaloneHarnessRunner(
            contract,
            continuity,
            adapter,
            bridge,
            budget=budget,
            clock_ms=lambda: time.time_ns() // 1_000_000,
            monotonic_ms=lambda: int(time.monotonic() * 1_000),
        )
        execution = runner.run(({"role": "user", "content": prompt},))
        terminal = execution.terminal_result
        diff = runtime_client.call_tool(
            "workspace.diff",
            {
                "schemaVersion": 1,
                "workspaceId": workspace_id,
                "maxBytes": 65_536,
            },
        )
        visible_passed = False
        hidden_passed = False
        if "allocation.py" in set(diff.get("modifiedPaths", [])):
            candidate = runtime_client.call_tool(
                "workspace.read",
                {
                    "schemaVersion": 1,
                    "workspaceId": workspace_id,
                    "relativePath": "allocation.py",
                    "mode": "FULL",
                    "offset": 0,
                    "maxBytes": 65_536,
                },
            )
            content = candidate.get("content")
            if isinstance(content, str):
                visible_passed, hidden_passed = _verify_candidate(
                    candidate_content=content,
                    fixture_root=fixture_root,
                    hidden_verifier=hidden_verifier,
                )
        completion_proposal = (
            None
            if terminal is None or terminal.completion_proposal is None
            else terminal.completion_proposal.to_dict()
        )
        run_receipt = None if terminal is None else terminal.receipt.to_dict()
        return {
            "replica": replica,
            "status": (
                "passed"
                if completion_proposal is not None and visible_passed and hidden_passed
                else "incomplete"
            ),
            "systemMaterial": system_material,
            "systemManifestDigest": system_digest,
            "harnessRunId": harness_run_id,
            "runtimeWorkspaceId": workspace_id,
            "sourceRevision": source_revision,
            "stateRoot": str(state_root),
            "execution": {
                "stopCode": execution.loop_result.stop_code.value,
                "candidateCompleted": execution.loop_result.candidate_completed,
                "usage": execution.loop_result.usage,
                "patchCalls": adapter_client.patch_calls,
                "injectedPatchResponseLoss": adapter_client.injected_patch_response_loss,
                "doctorHealthy": runner.doctor().get("healthy"),
            },
            "runReceipt": run_receipt,
            "completionProposal": completion_proposal,
            "verification": {
                "visiblePassed": visible_passed,
                "hiddenPassed": hidden_passed,
                "changedPaths": diff.get("changedPaths", []),
                "modifiedPaths": diff.get("modifiedPaths", []),
                "untrackedPaths": diff.get("untrackedPaths", []),
                "protectedSpecDigest": file_digest(fixture_root / "SPEC.md"),
                "protectedTestsDigest": file_digest(fixture_root / "test_allocation.py"),
            },
        }
    finally:
        if store is not None:
            store.close()
        if opened:
            try:
                runtime_client.call_tool(
                    "workspace.close",
                    {
                        "schemaVersion": 1,
                        "workspaceId": workspace_id,
                        "force": True,
                    },
                )
            except Exception as error:
                print(
                    json.dumps(
                        {
                            "replica": replica,
                            "cleanupWarning": str(error)[:512],
                        }
                    ),
                    file=sys.stderr,
                )
        shutil.rmtree(source, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness-root", type=Path, required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--runtime-env-file", type=Path, required=True)
    parser.add_argument("--runtime-binary", type=Path, required=True)
    parser.add_argument("--secret-file", type=Path, required=True)
    parser.add_argument("--state-parent", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replicas", type=int, default=3)
    args = parser.parse_args()
    if args.replicas < 1 or args.replicas > 10:
        raise SystemExit("replicas must be between 1 and 10")
    computing_root = Path(__file__).resolve().parents[3]
    harness_root = args.harness_root.resolve()
    runtime_root = args.runtime_root.resolve()
    _prepare_imports(harness_root, runtime_root)
    from mcp_probe import connect_compatible

    environment = load_env_file(args.runtime_env_file.resolve())
    bind = environment.get("ORDIVON_BIND", "127.0.0.1:8897")
    token = environment.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("Runtime environment omits ORDIVON_BEARER_TOKEN")
    runtime_client = connect_compatible(
        f"http://{bind}/mcp",
        token,
        client_name="ordivon-computing-c1-canary",
        timeout=45.0,
    )
    args.state_parent.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for replica in range(1, args.replicas + 1):
        result = run_replica(
            replica=replica,
            computing_root=computing_root,
            harness_root=harness_root,
            runtime_root=runtime_root,
            runtime_client=runtime_client,
            secret_file=args.secret_file.resolve(),
            state_parent=args.state_parent.resolve(),
            runtime_binary=args.runtime_binary.resolve(),
        )
        results.append(result)
        print(
            json.dumps(
                {
                    "replica": replica,
                    "status": result["status"],
                    "stopCode": result["execution"]["stopCode"],
                    "modelCalls": result["execution"]["usage"]["modelCalls"],
                    "toolCalls": result["execution"]["usage"]["toolCalls"],
                    "patchCalls": result["execution"]["patchCalls"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    document = {
        "schemaVersion": 1,
        "kind": "ordivon.c1-independent-runtime-canary-set",
        "replicaPolicy": {"count": args.replicas, "successDoesNotStopSet": True},
        "results": results,
        "summary": {
            "replicas": len(results),
            "passed": sum(result["status"] == "passed" for result in results),
            "incomplete": sum(result["status"] != "passed" for result in results),
        },
    }
    document["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "json-sort-keys-v1",
        "payloadDigest": canonical_sha256(document),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(document["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
