#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import deque
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

from common import (
    HARNESS_ROOT,
    HISTORICAL_HOST_REVISION,
    TASK_ID,
    TASK_VERSION,
    ensure_harness_source,
    harness_package_version,
    json_digest,
    load_b4_module,
    now_iso,
    repo_vector,
    text_digest,
    write_json,
)

ensure_harness_source()

from anc_canonical import canonical_digest  # noqa: E402
from ordivon_harness.api import (  # noqa: E402
    AgentTurnResult,
    HarnessAgentRun,
    HarnessAgentRunCompositionError,
    HarnessBoundReference,
    HarnessRunContract,
)
from ordivon_harness.domain_tools import (  # noqa: E402
    AgentRunConclusion,
    AgentToolCall,
    AgentToolDefinition,
    DomainToolCatalog,
    DomainToolLoopPlan,
    DomainToolLoopRunner,
    RunBudget,
    ToolObservation,
)


PROMPT = (
    "Repair allocation.py according to SPEC.md, preserve protected files, run the visible "
    "tests, inspect the diff, and produce the required completion claim."
)

READ_TASK = AgentToolDefinition(
    "read_task",
    "Read the visible repository-repair Task material.",
    {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
    },
)
WRITE_CANDIDATE = AgentToolDefinition(
    "write_candidate",
    "Write candidate allocation.py and completion Artifact into the evaluation workspace.",
    {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "source": {"type": "string"},
            "completion": {"type": "string"},
        },
        "required": ["source", "completion"],
    },
)
RUN_VISIBLE = AgentToolDefinition(
    "run_visible_tests",
    "Run only the Task-visible unittest suite.",
    {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
    },
)
INSPECT_DIFF = AgentToolDefinition(
    "inspect_diff",
    "Inspect the current Git diff without changing repository state.",
    {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
    },
)
CATALOG = DomainToolCatalog(
    "domain:p0-repository-repair",
    "1",
    (READ_TASK, WRITE_CANDIDATE, RUN_VISIBLE, INSPECT_DIFF),
)
ALLOWED_TOOLS = tuple(tool.name for tool in CATALOG.tools)


class QueueAdapter:
    adapter_id = "adapter:p0-scripted-harness"
    model_id = "model:p0-scripted-oracle"

    def __init__(self, results: tuple[AgentTurnResult, ...]) -> None:
        self.results = deque(results)
        self.requests = []

    def provider_request_digest(self, request) -> str:
        return canonical_digest(
            {
                "schemaVersion": 1,
                "kind": "p0-scripted-provider-request",
                "adapterId": self.adapter_id,
                "modelId": self.model_id,
                "dispatchDigest": request.dispatch_digest,
            }
        )

    def invoke(self, request) -> AgentTurnResult:
        self.requests.append(request)
        if not self.results:
            raise RuntimeError("scripted Harness cell exhausted Provider results")
        return self.results.popleft()


class RepositoryRepairBridge:
    catalog = CATALOG

    def __init__(self, root: Path) -> None:
        self.root = root
        self.bridge_identity = {
            "schemaVersion": 1,
            "kind": "p0-repository-repair-local-bridge",
            "truthRole": "evaluation-local-effect-not-production-runtime",
            "workspaceDigest": canonical_digest({"root": root.name}),
        }
        self.calls: list[str] = []

    def execute(self, call: AgentToolCall, *, step_id: str) -> ToolObservation:
        self.calls.append(call.name)
        if call.name == "read_task":
            content = {
                "spec": (self.root / "SPEC.md").read_text(encoding="utf-8"),
                "allocation": (self.root / "allocation.py").read_text(encoding="utf-8"),
                "tests": (self.root / "test_allocation.py").read_text(encoding="utf-8"),
            }
        elif call.name == "write_candidate":
            source = call.arguments.get("source")
            completion = call.arguments.get("completion")
            if not isinstance(source, str) or not isinstance(completion, str):
                raise TypeError("write_candidate requires source/completion strings")
            (self.root / "allocation.py").write_text(source, encoding="utf-8")
            artifact = self.root / "artifacts/completion.json"
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text(completion, encoding="utf-8")
            content = {
                "written": True,
                "sourceDigest": text_digest(source),
                "completionDigest": text_digest(completion),
            }
        elif call.name == "run_visible_tests":
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "-v", "test_allocation.py"],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            content = {
                "passed": result.returncode == 0,
                "outputDigest": text_digest(result.stdout + result.stderr),
            }
        elif call.name == "inspect_diff":
            result = subprocess.run(
                ["git", "-C", str(self.root), "diff", "--", "allocation.py", "artifacts/completion.json"],
                check=True,
                capture_output=True,
                text=True,
            )
            content = {
                "diffDigest": text_digest(result.stdout),
                "changed": bool(result.stdout),
            }
        else:
            raise ValueError(f"unexpected Tool: {call.name}")
        return ToolObservation(
            tool_call_id=call.tool_call_id,
            tool_name=call.name,
            status="observed",
            structured_content={**content, "stepId": step_id},
        )


def tool_result(index: int, name: str, arguments: dict[str, Any]) -> AgentTurnResult:
    return AgentTurnResult(
        model_call_id=f"model-call:p0-a0:{index}",
        model_id=QueueAdapter.model_id,
        content=None,
        tool_calls=(AgentToolCall(f"tool-call:p0-a0:{index}", name, arguments),),
        conclusion=None,
        usage={"inputTokens": 10, "outputTokens": 5},
        finish_reason="tool_calls",
        raw_response_digest=canonical_digest({"p0A0": index, "tool": name}),
    )


def conclusion_result(index: int) -> AgentTurnResult:
    return AgentTurnResult(
        model_call_id=f"model-call:p0-a0:{index}",
        model_id=QueueAdapter.model_id,
        content="candidate ready for independent verification",
        tool_calls=(),
        conclusion=AgentRunConclusion(
            "candidate_completed",
            "Repository-repair candidate is ready; the independent verifier still owns acceptance.",
        ),
        usage={"inputTokens": 10, "outputTokens": 5},
        finish_reason="stop",
        raw_response_digest=canonical_digest({"p0A0": index, "conclusion": True}),
    )


def visible_task(root: Path) -> dict[str, str]:
    return {
        "SPEC.md": (root / "SPEC.md").read_text(encoding="utf-8"),
        "allocation.py": (root / "allocation.py").read_text(encoding="utf-8"),
        "test_allocation.py": (root / "test_allocation.py").read_text(encoding="utf-8"),
    }


def run_one_shot_cell(b4) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ordivon-p0-a0-one-shot-") as temporary_name:
        temporary = Path(temporary_name)
        source = temporary / "source"
        extracted_revision = b4.extract_historical_fixture(source)
        task = visible_task(source)
        oracle = (HARNESS_ROOT / "evals/harness-repository-repair-001/oracle/allocation.py").read_text(encoding="utf-8")
        completion = b4.build_completion_artifact(oracle)
        completion_text = json.dumps(completion, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        protected = {
            "SPEC.md": b4.file_digest(source / "SPEC.md"),
            "test_allocation.py": b4.file_digest(source / "test_allocation.py"),
        }
        verifier = b4.run_verifier(
            temporary,
            candidate_source=oracle,
            completion_text=completion_text,
            protected=protected,
        )
        if not verifier["visiblePassed"] or not verifier["hiddenPassed"]:
            raise RuntimeError("scripted one-shot oracle did not pass the frozen verifier")
        return {
            "cellId": "S",
            "executionPath": "strong-simple-one-shot",
            "competitive": False,
            "scripted": True,
            "extractedSourceRevision": extracted_revision,
            "visibleTaskDigest": json_digest(task),
            "candidateSourceDigest": text_digest(oracle),
            "completionArtifactDigest": text_digest(completion_text),
            "verifier": verifier,
            "metrics": {
                "modelCalls": 1,
                "toolCalls": 0,
                "runtimeJobs": 0,
            },
        }


def run_harness_cell(b4) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ordivon-p0-a0-harness-") as temporary_name:
        temporary = Path(temporary_name)
        source = temporary / "source"
        extracted_revision = b4.extract_historical_fixture(source)
        task = visible_task(source)
        oracle = (HARNESS_ROOT / "evals/harness-repository-repair-001/oracle/allocation.py").read_text(encoding="utf-8")
        completion = b4.build_completion_artifact(oracle)
        completion_text = json.dumps(completion, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        protected = {
            "SPEC.md": b4.file_digest(source / "SPEC.md"),
            "test_allocation.py": b4.file_digest(source / "test_allocation.py"),
        }
        context_digest = canonical_digest(
            {
                "taskId": TASK_ID,
                "taskVersion": TASK_VERSION,
                "visibleTaskDigest": json_digest(task),
                "prompt": PROMPT,
            }
        )
        results = (
            tool_result(1, "read_task", {}),
            tool_result(2, "write_candidate", {"source": oracle, "completion": completion_text}),
            tool_result(3, "run_visible_tests", {}),
            tool_result(4, "inspect_diff", {}),
            conclusion_result(5),
        )
        adapter = QueueAdapter(results)
        bridge = RepositoryRepairBridge(source)
        plan = DomainToolLoopPlan(
            harness_run_id="harness-run:p0-a0-scripted",
            assignment_id="assignment:p0-a0-scripted",
            context_digest=context_digest,
            initial_messages=(
                {"role": "system", "content": "Work only from the visible Task and granted Tools."},
                {"role": "user", "content": PROMPT},
            ),
            allowed_tools=ALLOWED_TOOLS,
            budget=RunBudget(
                max_model_calls=5,
                max_tool_calls=4,
                max_observation_bytes=1_048_576,
                max_wall_time_ms=60_000,
                max_total_tokens=10_000,
                max_model_retries=0,
                max_tool_corrections=0,
                max_conclusion_corrections=0,
                max_observation_only_turns=0,
                max_no_progress_turns=1,
            ),
        )
        result = DomainToolLoopRunner(adapter, bridge).run(plan)
        if not result.candidate_completed:
            raise RuntimeError(f"current Harness domain loop did not complete: {result.stop_code.value}")
        candidate = (source / "allocation.py").read_text(encoding="utf-8")
        completion_observed = (source / "artifacts/completion.json").read_text(encoding="utf-8")
        verifier = b4.run_verifier(
            temporary,
            candidate_source=candidate,
            completion_text=completion_observed,
            protected=protected,
        )
        if not verifier["visiblePassed"] or not verifier["hiddenPassed"]:
            raise RuntimeError("scripted Harness cell did not pass the frozen verifier")
        if tuple(bridge.calls) != ALLOWED_TOOLS:
            raise RuntimeError(f"scripted Harness Tool sequence differs: {bridge.calls}")
        first = adapter.requests[0]
        return {
            "cellId": "H",
            "executionPath": "current-public-domain-tool-loop",
            "competitive": False,
            "scripted": True,
            "extractedSourceRevision": extracted_revision,
            "visibleTaskDigest": json_digest(task),
            "contextDigest": context_digest,
            "candidateSourceDigest": text_digest(candidate),
            "completionArtifactDigest": text_digest(completion_observed),
            "verifier": verifier,
            "toolCatalogDigest": bridge.catalog.digest,
            "toolGrantDigest": bridge.catalog.granted_digest(ALLOWED_TOOLS),
            "firstRequestToolCount": len(first.tools),
            "metrics": {
                "modelCalls": result.model_calls,
                "toolCalls": result.tool_calls,
                "runtimeJobs": 0,
                "observationBytes": result.observation_bytes,
            },
        }


def probe_high_level_agent_run_gap() -> dict[str, Any]:
    digest_a = canonical_digest({"p0": "a"})
    digest_b = canonical_digest({"p0": "b"})
    digest_c = canonical_digest({"p0": "c"})
    contract = HarnessRunContract(
        harness_run_id="harness-run:p0-a0-surface-probe",
        harness_implementation_id=f"ordivon-harness@{harness_package_version()}",
        caller_id="caller:p0-computing",
        caller_run_ref="trial:p0-a0-surface-probe",
        objective_ref=HarnessBoundReference("objective:p0-a0", "objective", digest_a),
        context_refs=(HarnessBoundReference("context:p0-a0", "context", digest_b),),
        provider_id="provider:p0-scripted",
        adapter_id=QueueAdapter.adapter_id,
        requested_model_id=QueueAdapter.model_id,
        tool_catalog_digest=CATALOG.digest,
        tool_grant_digest=CATALOG.granted_digest(ALLOWED_TOOLS),
        budget={"maxModelCalls": 5, "maxToolCalls": 4, "maxWallTimeMs": 60_000},
        completion_contract={"mode": "propose"},
        system_manifest_ref=HarnessBoundReference("system-manifest:p0-a0", "system-manifest", digest_c),
        created_at_ms=1,
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-p0-agent-run-probe-") as temporary_name:
        try:
            HarnessAgentRun.create(
                Path(temporary_name) / "state",
                contract,
                lambda _contract: QueueAdapter((conclusion_result(1),)),
            )
        except HarnessAgentRunCompositionError as error:
            message = str(error)
            if "does not implement" not in message:
                raise
            return {
                "supported": False,
                "surface": "HarnessAgentRun",
                "customToolCatalogDigest": CATALOG.digest,
                "reason": message,
                "meaning": (
                    "The recommended high-level state-root handle is not closed over this custom "
                    "repository-repair Tool surface; P0-A must use the public domain loop or an "
                    "advanced composition rather than mislabeling the old B4 path as HarnessAgentRun."
                ),
            }
        raise RuntimeError("HarnessAgentRun unexpectedly accepted the custom repository-repair surface")


def run(*, allow_dirty_computing: bool = False) -> dict[str, Any]:
    owners = repo_vector(allow_dirty_computing=allow_dirty_computing)
    b4 = load_b4_module()
    cell_s = run_one_shot_cell(b4)
    cell_h = run_harness_cell(b4)
    if cell_s["visibleTaskDigest"] != cell_h["visibleTaskDigest"]:
        raise RuntimeError("scripted cells did not bind the same visible Task")
    if cell_s["candidateSourceDigest"] != cell_h["candidateSourceDigest"]:
        raise RuntimeError("scripted cells did not converge on the same candidate bytes")
    for key in ("visiblePassed", "hiddenPassed", "protectedFilesUnchanged"):
        if cell_s["verifier"][key] != cell_h["verifier"][key]:
            raise RuntimeError(f"scripted cells disagree on verifier field: {key}")
    surface_probe = probe_high_level_agent_run_gap()
    return {
        "schemaVersion": 1,
        "kind": "ordivon.p0-a0-scripted-comparator-acceptance",
        "createdAt": now_iso(),
        "task": {
            "taskId": TASK_ID,
            "taskVersion": TASK_VERSION,
            "historicalHostRevision": HISTORICAL_HOST_REVISION,
            "verifierId": "HARNESS-REPO-REPAIR-001-verifier",
            "verifierRevision": "1",
        },
        "ownerVector": owners,
        "harnessPackageVersion": harness_package_version(),
        "highLevelSurfaceProbe": surface_probe,
        "cells": [cell_s, cell_h],
        "comparability": {
            "sameVisibleTask": True,
            "sameFrozenVerifier": True,
            "sameCandidateBytesUnderScriptedOracle": True,
            "hiddenVerifierModelVisible": False,
            "competitiveProviderEvidence": False,
        },
        "disposition": {
            "a0Ready": True,
            "liveComparisonAuthorizedByThisReceipt": False,
            "architectureDecisionAuthorized": False,
            "next": (
                "Build the current-revision live S/H canary only after Agent-visible MCP contract "
                "freshness is proven. Treat HarnessAgentRun custom-Tool closure as a measured surface "
                "gap, not as permission to revive historical B5."
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run P0-A0 scripted one-shot/Harness comparator acceptance")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--allow-dirty-computing", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        receipt = run(allow_dirty_computing=args.allow_dirty_computing)
        if args.receipt is not None:
            write_json(args.receipt, receipt)
        print(json.dumps(receipt, sort_keys=True))
        return 0
    except Exception as error:
        print(f"P0-A0 scripted comparator: {type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
