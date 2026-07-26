from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from anc_continuation.adapters import (
    ModelAdapterError,
    ModelDecision,
    ScriptedModelAdapter,
)
from anc_continuation.host import (
    FreshHost,
    HostDecisionRejected,
    HostInterrupted,
)
from anc_continuation.model import ActionKind, TaskPhase
from anc_continuation.store import FileObjectStore
from anc_continuation.validation import CapsuleValidator
from anc_continuation.workload import (
    AUDIT_EFFECT_ID,
    INITIAL_CONTENT,
    TERMINAL_CONTENT,
    freeze_checkpoint,
)


class FailingModel:
    adapter_id = "failing-model"

    def decide(self, context):
        raise ModelAdapterError("injected model failure")


class RepeatingModel:
    adapter_id = "repeating-model"

    def decide(self, context):
        action = context.payload["allowedActions"][0]
        return ModelDecision(
            action_id=action["actionId"],
            kind=ActionKind(action["kind"]),
            effect_id=AUDIT_EFFECT_ID,
            binding_id=action["bindingId"],
            dispatch_id=None,
            rationale="repeat the audit even though it is complete",
        )


class HostTests(unittest.TestCase):
    def test_fresh_host_completes_without_repeating_checkpoint_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            host = FreshHost(frozen.root, ScriptedModelAdapter())
            receipt = host.run(frozen.capsule_digest)
            self.assertEqual(receipt.status, "completed")
            self.assertEqual(
                receipt.executed_effects,
                (
                    "effect:continuation-apply-promotion",
                    "effect:continuation-terminal-read",
                ),
            )
            self.assertNotIn(AUDIT_EFFECT_ID, receipt.executed_effects)
            self.assertEqual(
                (frozen.root / "world/config.toml").read_text(), TERMINAL_CONTENT
            )
            store = FileObjectStore(frozen.root / "objects")
            final = store.get_capsule(receipt.capsule_after)
            self.assertIs(final.phase, TaskPhase.COMPLETE)
            self.assertEqual(final.capsule_revision, 2)
            self.assertEqual(final.supersedes_digest, frozen.capsule_digest)
            report = CapsuleValidator(store).validate(final, world_root=frozen.root)
            self.assertEqual(report.world_status, "current")
            self.assertEqual(len(report.completed_effect_ids), 4)
            self.assertEqual(len(report.fact_ids), 2)

    def test_host_exit_before_model_has_no_semantic_side_effect(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            before_objects = sorted(path.name for path in store.root.iterdir())
            before_world = (frozen.root / "world/config.toml").read_bytes()
            with self.assertRaises(HostInterrupted):
                FreshHost(frozen.root, ScriptedModelAdapter()).run(
                    frozen.capsule_digest, stop_before_model=True
                )
            self.assertEqual(
                sorted(path.name for path in store.root.iterdir()), before_objects
            )
            self.assertEqual(
                (frozen.root / "world/config.toml").read_bytes(), before_world
            )

    def test_model_failure_and_repeated_effect_proposal_do_not_mutate_world(self) -> None:
        for model, error in (
            (FailingModel(), ModelAdapterError),
            (RepeatingModel(), HostDecisionRejected),
        ):
            with self.subTest(model=model.adapter_id), tempfile.TemporaryDirectory() as temporary:
                frozen = freeze_checkpoint(
                    Path(temporary) / "checkpoint", source_revision="f" * 40
                )
                before = (frozen.root / "world/config.toml").read_bytes()
                with self.assertRaises(error):
                    FreshHost(frozen.root, model).run(frozen.capsule_digest)
                self.assertEqual(
                    (frozen.root / "world/config.toml").read_bytes(), before
                )

    def test_world_drift_blocks_mutation_and_writes_recoverable_capsule(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            world = frozen.root / "world/config.toml"
            changed = "mode = externally-changed\n"
            world.write_text(changed)
            receipt = FreshHost(frozen.root, ScriptedModelAdapter()).run(
                frozen.capsule_digest
            )
            self.assertEqual(receipt.status, "blocked-world-drift")
            self.assertEqual(receipt.executed_effects, ())
            self.assertEqual(world.read_text(), changed)
            store = FileObjectStore(frozen.root / "objects")
            blocked = store.get_capsule(receipt.capsule_after)
            self.assertIs(blocked.phase, TaskPhase.BLOCKED)
            self.assertTrue(blocked.blockers[0].startswith("world-drift:sha256:"))
            report = CapsuleValidator(store).validate(blocked, world_root=frozen.root)
            self.assertEqual(report.world_status, "drifted")

    def test_unknown_dispatch_is_observed_not_redispatched(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            capsule = store.get_capsule(frozen.capsule_digest)
            dispatch = store.put_semantic(
                "dispatch",
                "dispatch:continuation-unknown",
                {
                    "dispatchId": "dispatch:continuation-unknown",
                    "effectId": "effect:continuation-running",
                    "state": "unknown",
                },
            )
            variant = replace(capsule, unresolved_dispatches=(dispatch,))
            variant_digest = store.put_capsule(variant)
            receipt = FreshHost(frozen.root, ScriptedModelAdapter()).run(variant_digest)
            self.assertEqual(receipt.status, "blocked-observation-required")
            self.assertEqual(receipt.decision.kind, ActionKind.OBSERVE_DISPATCH)
            self.assertEqual(
                receipt.decision.dispatch_id, "dispatch:continuation-unknown"
            )
            self.assertEqual(receipt.executed_effects, ())
            self.assertEqual(
                (frozen.root / "world/config.toml").read_text(), INITIAL_CONTENT
            )


if __name__ == "__main__":
    unittest.main()
