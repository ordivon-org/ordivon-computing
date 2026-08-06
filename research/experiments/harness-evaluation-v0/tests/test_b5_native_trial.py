from __future__ import annotations

import importlib.util
import json
from pathlib import Path
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

    def test_system_manifest_excludes_secret_material(self) -> None:
        settings = b5.DeepSeekSettings(
            api_key="sk-" + "x" * 32,
            credential_scope_id="credential-scope:deepseek:flash:test",
        )
        manifest = b5.system_manifest(
            settings=settings,
            computing_revision="1" * 40,
            environment_digest="sha256:" + "2" * 64,
            prompt_digest="sha256:" + "3" * 64,
            context_digest="sha256:" + "4" * 64,
            budget_digest="sha256:" + "5" * 64,
            snapshot_digest="sha256:" + "6" * 64,
        )
        encoded = json.dumps(manifest, sort_keys=True)
        self.assertNotIn(settings.api_key, encoded)
        self.assertNotIn("/root/.config/ordivon/secrets", encoded)
        self.assertNotIn("apiKey", encoded)
        provider = manifest["configuration"]["provider"]
        self.assertEqual(provider["modelId"], "deepseek-v4-flash")
        self.assertEqual(
            provider["credentialScopeId"],
            "credential-scope:deepseek:flash:test",
        )
        self.assertEqual(provider["thinkingMode"], "disabled")
        self.assertFalse(manifest["privacy"]["secretsIncluded"])
        self.assertFalse(manifest["privacy"]["rawReasoningRequired"])

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

    def test_usage_compatibility_prefers_first_nonnegative_integer(self) -> None:
        value = {"prompt_tokens": 123, "inputTokens": 999, "bad": -1}
        self.assertEqual(
            b5.usage_int(value, "prompt_tokens", "inputTokens"),
            123,
        )
        self.assertEqual(b5.usage_int(value, "bad", "missing"), 0)


if __name__ == "__main__":
    unittest.main()
