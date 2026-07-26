from __future__ import annotations

import copy
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from anc_continuation.context import ContextCompiler
from anc_continuation.store import FileObjectStore
from anc_continuation.validation import CapsuleValidationError, CapsuleValidator
from anc_continuation.workload import freeze_checkpoint


class ValidationTests(unittest.TestCase):
    def test_complete_checkpoint_references_validate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            capsule = store.get_capsule(frozen.capsule_digest)
            report = CapsuleValidator(store).validate(capsule, world_root=frozen.root)
            context = ContextCompiler().compile(capsule, report)
            self.assertEqual(report.world_status, "current")
            self.assertEqual(len(report.completed_effect_ids), 2)
            self.assertEqual(len(report.fact_ids), 1)
            self.assertEqual(len(report.artifact_ids), 1)
            self.assertEqual(len(report.resolved_actions), 1)
            self.assertEqual(
                context.payload["allowedActions"][0]["actionId"],
                "action:apply-config-promotion",
            )

    def test_missing_decision_object_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            capsule = store.get_capsule(frozen.capsule_digest)
            decision = capsule.artifacts[0]
            (store.root / f"{decision.digest[7:]}.json").unlink()
            with self.assertRaisesRegex(CapsuleValidationError, "missing"):
                CapsuleValidator(store).validate(capsule, world_root=frozen.root)

    def test_forged_effect_signature_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            capsule = store.get_capsule(frozen.capsule_digest)
            original = capsule.completed_effects[0]
            payload = copy.deepcopy(store.resolve_semantic(original))
            payload["signedEffect"]["attestation"]["signature"] = (
                "hmac-sha256:" + "0" * 64
            )
            forged = store.put_semantic(original.kind, original.semantic_id, payload)
            capsule = replace(
                capsule,
                completed_effects=(forged, *capsule.completed_effects[1:]),
            )
            with self.assertRaisesRegex(
                CapsuleValidationError, "signed Effect verification failed"
            ):
                CapsuleValidator(store).validate(capsule, world_root=frozen.root)

    def test_world_drift_restricts_context_to_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            frozen = freeze_checkpoint(
                Path(temporary) / "checkpoint", source_revision="f" * 40
            )
            store = FileObjectStore(frozen.root / "objects")
            capsule = store.get_capsule(frozen.capsule_digest)
            (frozen.root / capsule.world.relative_path).write_text(
                "mode = externally-changed\n"
            )
            report = CapsuleValidator(store).validate(capsule, world_root=frozen.root)
            context = ContextCompiler().compile(capsule, report)
            self.assertEqual(report.world_status, "drifted")
            self.assertEqual(
                context.payload["allowedActions"],
                [
                    {
                        "actionId": "action:refresh-world",
                        "kind": "refresh-world",
                        "effectId": None,
                        "bindingId": None,
                        "dispatchId": None,
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
