from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "research" / "experiments" / "harness-evaluation-v0" / "run_c1_independent_runtime_canary.py"
SPEC = importlib.util.spec_from_file_location("c1_canary", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
C1 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = C1
SPEC.loader.exec_module(C1)


class FakeMcpClient:
    def __init__(self, result: dict) -> None:
        self.result = result
        self.calls: list[tuple[str, dict]] = []

    def exchange(self, method: str, params: dict):
        self.calls.append((method, params))
        return 200, {"id": 1, "result": self.result}, {}


class EvaluationMcpRuntimeClientTests(unittest.TestCase):
    def test_structured_not_committed_error_becomes_tool_rejection(self) -> None:
        harness_root = Path("/root/projects/ordivon-harness")
        runtime_root = Path("/root/projects/ordivon-runtime")
        C1._prepare_imports(harness_root, runtime_root)
        from ordivon_harness.runtime_port import HarnessRuntimeToolRejected

        client = C1.EvaluationMcpRuntimeClient(
            FakeMcpClient(
                {
                    "isError": True,
                    "structuredContent": {
                        "error": {
                            "code": "WORKSPACE_PATH_NOT_FOUND",
                            "message": "workspace path does not exist",
                            "commitState": "not_committed",
                            "retryable": False,
                            "field": "relativePath",
                        }
                    },
                }
            ),
            inject_first_patch_response_loss=False,
        )
        with self.assertRaises(HarnessRuntimeToolRejected) as caught:
            client.call_tool("workspace.read", {"schemaVersion": 1})
        self.assertEqual(caught.exception.detail.code, "WORKSPACE_PATH_NOT_FOUND")
        self.assertEqual(caught.exception.detail.commit_state, "not_committed")

    def test_first_successful_patch_can_inject_ambiguous_response_loss(self) -> None:
        harness_root = Path("/root/projects/ordivon-harness")
        runtime_root = Path("/root/projects/ordivon-runtime")
        C1._prepare_imports(harness_root, runtime_root)
        from ordivon_harness.runtime_port import HarnessRuntimeClientError

        client = C1.EvaluationMcpRuntimeClient(
            FakeMcpClient(
                {
                    "isError": False,
                    "structuredContent": {"state": "committed"},
                }
            ),
            inject_first_patch_response_loss=True,
        )
        with self.assertRaises(HarnessRuntimeClientError):
            client.call_tool("workspace.patch", {"schemaVersion": 1})
        self.assertTrue(client.injected_patch_response_loss)
        self.assertEqual(client.patch_calls, 1)
        self.assertEqual(
            client.call_tool("workspace.patch", {"schemaVersion": 1}),
            {"state": "committed"},
        )
        self.assertEqual(client.patch_calls, 2)


if __name__ == "__main__":
    unittest.main()
