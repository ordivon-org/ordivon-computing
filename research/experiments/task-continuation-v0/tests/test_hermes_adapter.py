from __future__ import annotations

import json
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from anc_continuation.adapters import HermesCliModelAdapter
from anc_continuation.context import CompiledContext


class HermesAdapterTests(unittest.TestCase):
    def test_isolated_hermes_adapter_returns_structured_decision_and_usage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            credentials = root / "source.env"
            credentials.write_text(
                "DEEPSEEK_API_KEY=test-secret\n"
                "DEEPSEEK_BASE_URL=https://wrong.example\n"
                "OTHER_API_KEY=must-not-copy\n"
            )
            log_path = root / "fake-log.json"
            executable = root / "hermes"
            executable.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    import json
                    import os
                    import pathlib
                    import sys

                    args = sys.argv[1:]
                    def value(flag):
                        return args[args.index(flag) + 1]

                    home = pathlib.Path(os.environ["HOME"])
                    hermes_home = pathlib.Path(os.environ["HERMES_HOME"])
                    config = (hermes_home / "config.yaml").read_text()
                    env_text = (hermes_home / ".env").read_text()
                    assert home != pathlib.Path.home() or str(home).startswith("/tmp/")
                    assert "cli: []" in config
                    assert "- kanban" in config
                    assert "memory_enabled: false" in config
                    assert env_text == (
                        "DEEPSEEK_API_KEY=test-secret\\n"
                        "DEEPSEEK_BASE_URL=https://api.deepseek.com\\n"
                    )
                    assert "OTHER_API_KEY" not in env_text
                    assert "--ignore-rules" in args
                    prompt = value("--oneshot")
                    assert "action:apply-config-promotion" in prompt
                    usage = {
                        "model": value("--model"),
                        "provider": value("--provider"),
                        "api_calls": 1,
                        "input_tokens": 101,
                        "output_tokens": 17,
                        "reasoning_tokens": 9,
                        "total_tokens": 127,
                        "estimated_cost_usd": 0.001,
                        "completed": True,
                        "failed": False,
                    }
                    pathlib.Path(value("--usage-file")).write_text(json.dumps(usage))
                    pathlib.Path(os.environ["FAKE_HERMES_LOG"]).write_text(json.dumps({
                        "home": str(home),
                        "hermesHome": str(hermes_home),
                        "config": config,
                        "env": env_text,
                    }))
                    print(json.dumps({
                        "actionId": "action:apply-config-promotion",
                        "kind": "apply-guarded-mutation",
                        "effectId": "effect:continuation-apply-promotion",
                        "bindingId": "binding:continuation-apply-r1",
                        "dispatchId": None,
                        "rationale": "The current world matches the checkpoint.",
                    }))
                    """
                )
            )
            executable.chmod(0o755)
            context = CompiledContext(
                {
                    "allowedActions": [
                        {
                            "actionId": "action:apply-config-promotion",
                            "kind": "apply-guarded-mutation",
                            "effectId": "effect:continuation-apply-promotion",
                            "bindingId": "binding:continuation-apply-r1",
                            "dispatchId": None,
                        }
                    ]
                }
            )
            adapter = HermesCliModelAdapter(
                working_directory=root / "world",
                credential_env_path=credentials,
                hermes_executable=str(executable),
            )
            with patch.dict(os.environ, {"FAKE_HERMES_LOG": str(log_path)}):
                decision = adapter.decide(context)
            self.assertEqual(decision.action_id, "action:apply-config-promotion")
            evidence = adapter.evidence_metadata()
            self.assertEqual(evidence["model"], "deepseek-v4-pro")
            self.assertEqual(evidence["provider"], "deepseek")
            self.assertEqual(evidence["apiCalls"], 1)
            self.assertEqual(evidence["totalTokens"], 127)
            self.assertEqual(evidence["enabledToolsets"], [])
            self.assertTrue(evidence["isolatedHome"])
            self.assertFalse(evidence["persistentSessionRetained"])
            log = json.loads(log_path.read_text())
            self.assertNotEqual(log["home"], str(Path.home()))
            self.assertNotEqual(log["hermesHome"], str(Path.home() / ".hermes"))
            self.assertFalse(Path(log["hermesHome"]).exists())


if __name__ == "__main__":
    unittest.main()
