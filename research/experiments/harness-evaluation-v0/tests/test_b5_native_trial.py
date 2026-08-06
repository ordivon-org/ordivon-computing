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
