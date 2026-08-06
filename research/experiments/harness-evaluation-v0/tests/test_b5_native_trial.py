from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "run_b5_native_trial.py"


def load_module():
    spec = importlib.util.spec_from_file_location("b5_native_trial_tested", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load run_b5_native_trial.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


b5 = load_module()

CORRECTED_TAIL = '''    weight_total = sum(weights)
    floors = [(total * weight) // weight_total for weight in weights]
    remainders = [(total * weight) % weight_total for weight in weights]
    remaining = total - sum(floors)
    order = sorted(
        range(len(weights)),
        key=lambda index: (-remainders[index], index),
    )
    for index in order[:remaining]:
        floors[index] += 1
    return floors
'''
DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
DIGEST_C = "sha256:" + "c" * 64


def loop_result(
    stop_code,
    *,
    usage: dict[str, object] | None = None,
    observations: tuple[object, ...] = (),
    events: tuple[object, ...] = (),
):
    return SimpleNamespace(
        stop_code=stop_code,
        candidate_completed=stop_code is b5.RunStopCode.CANDIDATE_COMPLETED,
        model_calls=2,
        tool_calls=3,
        observation_bytes=512,
        usage=usage
        or {
            "toolCorrections": 0,
            "providerUsage": [
                {
                    "prompt_tokens": 120,
                    "completion_tokens": 30,
                    "prompt_cache_hit_tokens": 20,
                    "total_tokens": 150,
                }
            ],
            "totalTokens": 150,
        },
        observations=observations,
        trace=SimpleNamespace(digest=DIGEST_A, events=events),
    )


def evaluation(*, accepted: bool) -> object:
    return b5.CandidateEvaluation(
        accepted=accepted,
        visible_passed=accepted,
        hidden_passed=accepted,
        protected_files_unchanged=True,
        completion_artifact_valid=accepted,
        candidate_source_digest=DIGEST_B,
        completion_artifact_digest=DIGEST_C if accepted else None,
        visible_digest=DIGEST_A,
        hidden_digest=DIGEST_B,
        failure_codes=() if accepted else ("hidden_check_failed",),
    )


class B5NativeTrialTests(unittest.TestCase):
    def test_runner_source_contains_no_policy_forbidden_sensitive_text(self) -> None:
        source = Path(b5.__file__).read_text(encoding="utf-8")
        lowered = source.lower()
        for forbidden in (
            "raw reasoning",
            "private reasoning",
            "raw chain of thought",
            "bearer ",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_selected_harness_conclusion_gate_is_exact(self) -> None:
        self.assertEqual(
            b5.HARNESS_REVISION,
            "437de1666a4124bc8a2791ee1a52456f913e9677",
        )
        self.assertEqual(
            b5.HARNESS_CONCLUSION_GATE_IMPLEMENTATION_REVISION,
            "b23d5fa6c820c10f937f48cc16c2d8e03d3e18ae",
        )
        self.assertEqual(
            b5.HARNESS_CONCLUSION_GATE_RECEIPT_REVISION,
            "437de1666a4124bc8a2791ee1a52456f913e9677",
        )
        self.assertEqual(
            b5.HARNESS_CONCLUSION_GATE_RECEIPT_DIGEST,
            "sha256:a35fb2a4859657069b112cc3172dcb5e0f2aeb748d0fe693ff09c0dd95a1218a",
        )

    def test_formal_plan_enforces_the_next_trial_number(self) -> None:
        plan = json.loads(b5.FORMAL_TRIAL_PLAN.read_text(encoding="utf-8"))
        self.assertEqual(
            b5.validate_planned_trial_number(4),
            plan["integrity"]["payloadDigest"],
        )
        with self.assertRaises(b5.NativeTrialError):
            b5.validate_planned_trial_number(3)
        with self.assertRaises(b5.NativeTrialError):
            b5.validate_planned_trial_number(5)

    def test_trial_reservation_is_private_durable_and_single_use(self) -> None:
        ids = b5.TrialIds.build(3)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "campaign"
            output = Path(directory) / "trial-output"
            value = b5.reserve_trial_number(
                root,
                ids,
                computing_revision="a" * 40,
                output_root=output,
                formal_plan_digest=DIGEST_A,
                created_at_ms=10,
            )
            path = root / "trial-003.json"
            self.assertEqual(root.stat().st_mode & 0o777, 0o700)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            loaded = json.loads(path.read_text(encoding="utf-8"))
            b5.verify_integrity(loaded)
            self.assertEqual(loaded, value)
            self.assertEqual(loaded["trialId"], ids.trial_id)
            self.assertEqual(loaded["formalTrialPlanDigest"], DIGEST_A)
            self.assertNotIn(str(output), json.dumps(loaded, sort_keys=True))
            with self.assertRaisesRegex(
                b5.NativeTrialError,
                "already reserved",
            ):
                b5.reserve_trial_number(
                    root,
                    ids,
                    computing_revision="b" * 40,
                    output_root=Path(directory) / "other-output",
                    formal_plan_digest=DIGEST_B,
                    created_at_ms=11,
                )
            root.chmod(0o755)
            with self.assertRaisesRegex(
                b5.NativeTrialError,
                "private 0700",
            ):
                b5.reserve_trial_number(
                    root,
                    b5.TrialIds.build(4),
                    computing_revision="c" * 40,
                    output_root=Path(directory) / "fourth-output",
                    formal_plan_digest=DIGEST_C,
                    created_at_ms=12,
                )

    def test_trial_identities_are_stable_and_distinct(self) -> None:
        first = b5.TrialIds.build(1)
        second = b5.TrialIds.build(2)
        self.assertEqual(first.trial_id, "trial:b5-native-001")
        self.assertEqual(first.host_task_id, "task:b5-native-001")
        self.assertEqual(first.harness_run_id, "harness-run:b5-native-001")
        self.assertNotEqual(first.trial_id, second.trial_id)
        self.assertNotEqual(first.runtime_instance, second.runtime_instance)
        with self.assertRaises(ValueError):
            b5.TrialIds.build(0)

    def test_host_runtime_rejection_is_translated_to_harness_contract(self) -> None:
        detail = SimpleNamespace(
            code="invalid_argument",
            message="patch range differs",
            commit_state="not_started",
            retryable=False,
            field="files",
        )

        class Delegate:
            def call_tool(self, name, arguments):
                raise b5.HostRuntimeToolRejected(name, detail)

        runtime = b5.RuntimeRecorder(Delegate())
        with self.assertRaises(b5.HarnessRuntimeToolRejected) as caught:
            runtime.call_tool("workspace.patch", {"schemaVersion": 1})
        self.assertEqual(caught.exception.operation, "workspace.patch")
        self.assertEqual(caught.exception.detail.code, "invalid_argument")
        self.assertEqual(caught.exception.detail.commit_state, "not_started")
        self.assertEqual(
            runtime.error_translations,
            [
                {
                    "sourceType": "RuntimeToolRejected",
                    "targetType": "HarnessRuntimeToolRejected",
                    "operation": "workspace.patch",
                    "code": "invalid_argument",
                    "commitState": "not_started",
                    "retryable": False,
                    "field": "files",
                    "messageDigest": b5.text_digest("patch range differs"),
                }
            ],
        )

    def test_host_runtime_client_failure_is_translated_to_harness_contract(self) -> None:
        class Delegate:
            def call_tool(self, name, arguments):
                raise b5.HostRuntimeClientError("transport unavailable")

        runtime = b5.RuntimeRecorder(Delegate())
        with self.assertRaises(b5.HarnessRuntimeClientError):
            runtime.call_tool("workspace.read", {"schemaVersion": 1})
        self.assertEqual(
            runtime.error_translations[0]["targetType"],
            "HarnessRuntimeClientError",
        )
        self.assertEqual(runtime.error_translations[0]["commitState"], "unknown")
        self.assertIsNone(runtime.error_translations[0]["field"])
        self.assertEqual(
            runtime.error_translations[0]["messageDigest"],
            b5.text_digest("transport unavailable"),
        )

    def test_model_override_preserves_secret_and_selects_exact_configuration(self) -> None:
        base = b5.DeepSeekSettings(
            api_key="sk-" + "m" * 32,
            model="deepseek-v4-flash",
            credential_scope_id="credential-scope:deepseek:pivot:test",
            timeout_seconds=45.0,
            max_response_bytes=123_456,
            max_output_tokens=4_096,
        )
        selected, configuration_id = b5.select_deepseek_settings(
            base,
            "deepseek-v4-pro",
        )
        self.assertEqual(selected.model, "deepseek-v4-pro")
        self.assertEqual(configuration_id, b5.PRO_CONFIGURATION_ID)
        self.assertEqual(selected.api_key, base.api_key)
        self.assertEqual(selected.base_url, base.base_url)
        self.assertEqual(selected.credential_scope_id, base.credential_scope_id)
        self.assertEqual(selected.timeout_seconds, base.timeout_seconds)
        self.assertEqual(selected.max_response_bytes, base.max_response_bytes)
        self.assertEqual(selected.max_output_tokens, base.max_output_tokens)
        self.assertEqual(base.model, "deepseek-v4-flash")
        default, default_configuration = b5.select_deepseek_settings(base, None)
        self.assertEqual(default.model, "deepseek-v4-flash")
        self.assertEqual(default_configuration, b5.FLASH_CONFIGURATION_ID)
        with self.assertRaisesRegex(b5.NativeTrialError, "unsupported"):
            b5.select_deepseek_settings(base, "unknown-model")

    def test_trace_summary_is_metadata_only_and_retains_failure_boundary(self) -> None:
        events = (
            SimpleNamespace(
                sequence=1,
                kind="tool_call_proposed",
                payload={
                    "toolCallId": "tool:patch",
                    "toolName": "patch_workspace",
                    "toolCallDigest": DIGEST_A,
                    "toolCall": {
                        "arguments": {"unretainedField": "must-not-survive"}
                    },
                },
            ),
            SimpleNamespace(
                sequence=2,
                kind="run_stopped",
                payload={
                    "stopCode": "harness_failed",
                    "detail": (
                        "RuntimeProtocolError: sensitive path omitted from summary"
                    ),
                },
            ),
        )
        observation = SimpleNamespace(
            tool_call_id="tool:patch",
            tool_name="patch_workspace",
            status="rejected",
            runtime_job_ref=None,
            reconciled=False,
            structured_content={
                "relativePath": "allocation.py",
                "clientRequestId": "private-request-id-not-retained",
                "error": {
                    "type": "RuntimeToolRejected",
                    "code": "INVALID_REQUEST",
                    "field": "files[0].edits[0].range",
                    "commitState": "not_committed",
                    "retryable": False,
                    "message": "line range differs and must not survive",
                    "nestedPayload": {"unretainedField": "must-not-survive"},
                },
            },
        )
        loop = loop_result(
            b5.RunStopCode.HARNESS_FAILED,
            events=events,
            observations=(observation,),
        )
        runtime = b5.RuntimeRecorder(SimpleNamespace())
        runtime.error_translations.append(
            {
                "sourceType": "RuntimeProtocolError",
                "targetType": "HarnessRuntimeClientError",
                "operation": "workspace.patch",
                "code": "runtime_client_error",
                "commitState": "unknown",
                "retryable": False,
                "field": None,
                "messageDigest": DIGEST_B,
            }
        )
        value = b5.build_trace_summary(b5.TrialIds.build(3), loop, runtime)
        encoded = json.dumps(value, sort_keys=True)
        self.assertNotIn("must-not-survive", encoded)
        self.assertNotIn("sensitive path omitted", encoded)
        self.assertNotIn("private-request-id-not-retained", encoded)
        self.assertNotIn("line range differs", encoded)
        self.assertEqual(value["events"][0]["metadata"]["toolName"], "patch_workspace")
        stopped = value["events"][1]["metadata"]
        self.assertEqual(stopped["stopCode"], "harness_failed")
        self.assertEqual(stopped["detailType"], "RuntimeProtocolError")
        self.assertTrue(stopped["detailDigest"].startswith("sha256:"))
        self.assertEqual(value["toolObservationCount"], 1)
        retained = value["toolObservations"][0]
        self.assertEqual(retained["toolName"], "patch_workspace")
        self.assertEqual(retained["status"], "rejected")
        self.assertEqual(retained["metadata"]["relativePath"], "allocation.py")
        self.assertEqual(retained["error"]["code"], "INVALID_REQUEST")
        self.assertEqual(
            retained["error"]["field"],
            "files[0].edits[0].range",
        )
        self.assertEqual(retained["error"]["commitState"], "not_committed")
        self.assertEqual(
            retained["error"]["messageDigest"],
            b5.text_digest("line range differs and must not survive"),
        )
        self.assertFalse(value["privacy"]["toolArgumentsRetained"])
        self.assertFalse(value["privacy"]["observationContentRetained"])
        self.assertFalse(value["privacy"]["errorMessageTextRetained"])
        self.assertEqual(
            value["runtimeErrorTranslations"][0]["sourceType"],
            "RuntimeProtocolError",
        )

    def test_provider_configuration_excludes_secret_material(self) -> None:
        settings = b5.DeepSeekSettings(
            api_key="sk-" + "x" * 32,
            credential_scope_id="credential-scope:deepseek:flash:test",
        )
        value = b5.provider_configuration(settings)
        encoded = json.dumps(value, sort_keys=True)
        self.assertNotIn(settings.api_key, encoded)
        self.assertNotIn("/root/.config/ordivon/secrets", encoded)
        self.assertNotIn("apiKey", encoded)
        self.assertEqual(
            value["credentialScopeId"],
            "credential-scope:deepseek:flash:test",
        )
        with tempfile.TemporaryDirectory() as directory:
            store = b5.TrialRecordStore.initialize(
                Path(directory) / "trial",
                trial_id="trial:provider-config",
                configuration_id="configuration:provider-config",
                task_ref={"taskId": b5.TASK_ID, "taskVersion": b5.TASK_VERSION},
                created_at_ms=1,
            )
            store.write_record("provider-configuration.json", value)

    def test_system_manifest_is_frozen_schema_and_secret_free(self) -> None:
        settings = b5.DeepSeekSettings(
            api_key="sk-" + "y" * 32,
            credential_scope_id="credential-scope:deepseek:flash:test",
        )
        manifest = b5.system_manifest(
            b5.TrialIds.build(1),
            settings=settings,
            environment_digest="sha256:" + "2" * 64,
            prompt_digest="sha256:" + "3" * 64,
            context_digest="sha256:" + "4" * 64,
            budget_digest="sha256:" + "5" * 64,
            snapshot_digest="sha256:" + "6" * 64,
        )
        encoded = json.dumps(manifest, sort_keys=True)
        self.assertNotIn(settings.api_key, encoded)
        self.assertNotIn(settings.credential_scope_id, encoded)
        self.assertNotIn("apiKey", encoded)
        self.assertEqual(
            set(manifest["configuration"]["provider"]),
            {"providerId", "modelId", "modelRevision", "adapterRevision"},
        )
        self.assertFalse(manifest["privacy"]["secretsIncluded"])
        self.assertFalse(manifest["privacy"]["rawReasoningRequired"])
        b5.validate_system_manifest_record(manifest)

    def test_prompt_requires_owner_bounded_artifact_and_host_verification(self) -> None:
        messages = b5.initial_messages(
            b5.TrialIds.build(1),
            "workspace:test-b5-native",
        )
        encoded = json.dumps(messages)
        self.assertIn("artifacts/completion.json", encoded)
        self.assertIn("Host owns acceptance", encoded)
        self.assertIn("visible-tests", encoded)
        self.assertIn(b5.HISTORICAL_HOST_REVISION, encoded)
        self.assertNotIn("deepseek.json", encoded)
        self.assertNotIn("apiKey", encoded)

    def test_correct_candidate_passes_visible_hidden_artifact_and_protection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            b5.b4.extract_historical_fixture(source)
            original = (source / "allocation.py").read_text(encoding="utf-8")
            candidate = original.replace(
                "    weight_total = sum(weights)\n"
                "    return [(total * weight) // weight_total for weight in weights]\n",
                CORRECTED_TAIL,
            )
            completion = b5.b4.build_completion_artifact(candidate)
            protected = {
                "SPEC.md": b5.file_digest(source / "SPEC.md"),
                "test_allocation.py": b5.file_digest(source / "test_allocation.py"),
            }
            result = b5.evaluate_candidate(
                root,
                candidate_source=candidate,
                completion_text=json.dumps(completion, sort_keys=True),
                protected_observed=protected,
                protected_expected=protected,
            )
        self.assertTrue(result.accepted)
        self.assertTrue(result.visible_passed)
        self.assertTrue(result.hidden_passed)
        self.assertTrue(result.completion_artifact_valid)
        self.assertEqual(result.failure_codes, ())

    def test_missing_completion_artifact_is_semantic_rejection_not_runner_crash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            b5.b4.extract_historical_fixture(source)
            candidate = (source / "allocation.py").read_text(encoding="utf-8")
            protected = {
                "SPEC.md": b5.file_digest(source / "SPEC.md"),
                "test_allocation.py": b5.file_digest(source / "test_allocation.py"),
            }
            result = b5.evaluate_candidate(
                root,
                candidate_source=candidate,
                completion_text=None,
                protected_observed=protected,
                protected_expected=protected,
            )
        self.assertFalse(result.accepted)
        self.assertFalse(result.completion_artifact_valid)
        self.assertIn("completion_artifact_missing", result.failure_codes)
        self.assertIn("hidden_check_failed", result.failure_codes)

    def test_provider_usage_totals_support_native_provider_shapes(self) -> None:
        totals = b5.provider_usage_totals(
            {
                "providerUsage": [
                    {
                        "prompt_tokens": 100,
                        "completion_tokens": 20,
                        "prompt_cache_hit_tokens": 30,
                        "total_tokens": 120,
                    },
                    {
                        "promptTokens": 40,
                        "completionTokens": 10,
                        "cachedInputTokens": 5,
                    },
                ],
                "totalTokens": 170,
            }
        )
        self.assertEqual(
            totals,
            {
                "inputTokens": 140,
                "outputTokens": 30,
                "cachedInputTokens": 35,
                "totalTokens": 170,
            },
        )

    def test_valid_rejected_candidate_is_comparison_eligible_negative(self) -> None:
        loop = loop_result(b5.RunStopCode.CANDIDATE_COMPLETED)
        rejected = evaluation(accepted=False)
        axes = b5.trial_axes(loop, rejected, selection_complete=True)
        self.assertEqual(
            axes,
            {
                "validity": "valid",
                "semanticOutcome": "rejected",
                "failureAttribution": "candidate",
                "comparisonEligible": True,
            },
        )
        failure = b5.build_failure_record(
            b5.TrialIds.build(1),
            loop=loop,
            evaluation=rejected,
            selection_complete=True,
        )
        self.assertEqual(failure["failureClass"], "MODEL")
        self.assertEqual(failure["failureCode"], "false_completion")
        self.assertEqual(
            failure["evidenceRefs"][0],
            "harness-run:b5-native-001",
        )
        result = b5.build_result_record(
            b5.TrialIds.build(1),
            loop=loop,
            evaluation=rejected,
            decision={"decisionRef": "host-event:decision"},
            completion_text=None,
            workspace_id="workspace:test",
            job_ids=("job:test",),
            started_at_ms=1,
            completed_at_ms=2,
            failure=failure,
        )
        self.assertEqual(result["acceptance"]["status"], "rejected")
        self.assertTrue(result["acceptance"]["falseCompletion"])
        self.assertEqual(result["trace"]["ref"], "harness-run:b5-native-001")
        b5.b4.validate_track_r_record(result)

    def test_provider_failure_without_runtime_job_is_formal_invalid_trial(self) -> None:
        event = SimpleNamespace(sequence=2, kind="run_stopped")
        loop = loop_result(
            b5.RunStopCode.PROVIDER_UNAVAILABLE,
            usage={"toolCorrections": "invalid", "providerUsage": []},
            events=(event,),
        )
        self.assertEqual(b5.runtime_job_ids(loop, SimpleNamespace(job_ids=set())), ())
        axes = b5.trial_axes(loop, None, selection_complete=False)
        self.assertEqual(axes["validity"], "invalid")
        self.assertFalse(axes["comparisonEligible"])
        failure = b5.build_failure_record(
            b5.TrialIds.build(1),
            loop=loop,
            evaluation=None,
            selection_complete=False,
        )
        self.assertEqual(failure["failureClass"], "PROVIDER")
        self.assertEqual(failure["failureCode"], "transport_error")
        result = b5.build_result_record(
            b5.TrialIds.build(1),
            loop=loop,
            evaluation=None,
            decision=None,
            completion_text=None,
            workspace_id="workspace:test",
            job_ids=(),
            started_at_ms=1,
            completed_at_ms=2,
            failure=failure,
        )
        self.assertEqual(result["acceptance"]["status"], "not_adjudicated")
        self.assertEqual(result["metrics"]["runtimeJobs"], 0)
        self.assertEqual(result["metrics"]["invalidToolCalls"], 0)
        b5.b4.validate_track_r_record(result)

    def test_incomplete_selection_preserves_rejected_semantic_outcome(self) -> None:
        loop = loop_result(b5.RunStopCode.CANDIDATE_COMPLETED)
        rejected = evaluation(accepted=False)
        axes = b5.trial_axes(loop, rejected, selection_complete=False)
        self.assertEqual(axes["validity"], "invalid")
        self.assertEqual(axes["semanticOutcome"], "rejected")
        self.assertEqual(axes["failureAttribution"], "candidate")
        self.assertFalse(axes["comparisonEligible"])
        failure = b5.build_failure_record(
            b5.TrialIds.build(1),
            loop=loop,
            evaluation=rejected,
            selection_complete=False,
        )
        self.assertEqual(failure["failureClass"], "MODEL")
        self.assertEqual(failure["failureCode"], "false_completion")

    def test_candidate_completion_without_host_proposal_is_harness_failure(self) -> None:
        loop = loop_result(b5.RunStopCode.CANDIDATE_COMPLETED)
        failure = b5.build_failure_record(
            b5.TrialIds.build(1),
            loop=loop,
            evaluation=None,
            selection_complete=False,
        )
        self.assertEqual(failure["failureClass"], "HARNESS")
        self.assertEqual(failure["failureCode"], "result_misrouting")


if __name__ == "__main__":
    unittest.main()
