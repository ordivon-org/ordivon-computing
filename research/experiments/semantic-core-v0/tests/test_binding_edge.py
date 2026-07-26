from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from anc_semantic_core.authority import AuthorityDenied, AuthorityRole
from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.errors import InvalidTransition, InvariantViolation
from anc_semantic_core.identity import IdKind
from anc_semantic_core.journal import JOURNAL_SCHEMA_VERSION
from anc_semantic_core.model import BindingAdmission
from anc_semantic_core.state import EffectState
from anc_semantic_core.testing import journal_authority_views, reference_authority_views

EFFECT_DIGEST = "sha256:" + "1" * 64
BINDING_DIGEST_1 = "sha256:" + "2" * 64
BINDING_DIGEST_2 = "sha256:" + "3" * 64


def admit_and_prepare(views, name: str):
    spec = sample_effect(name)
    views.effects.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"event:{name}:admit"),
        recorded_at_ms=1,
    )
    views.effects.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"event:{name}:prepare"),
        recorded_at_ms=2,
    )
    return spec


def binding(spec, revision: int = 1, *, admitted_at_ms: int = 3):
    return BindingAdmission(
        binding_id=sid(IdKind.BINDING, f"binding:{spec.effect_id.value}:r{revision}"),
        effect_id=spec.effect_id,
        effect_digest=EFFECT_DIGEST,
        binding_digest=(BINDING_DIGEST_1 if revision == 1 else BINDING_DIGEST_2),
        binding_revision=revision,
        admitted_at_ms=admitted_at_ms,
        supersedes_binding_id=(
            None
            if revision == 1
            else sid(IdKind.BINDING, f"binding:{spec.effect_id.value}:r{revision - 1}")
        ),
    )


class BindingEdgeTests(unittest.TestCase):
    def test_binding_authority_is_separate_from_effect_and_dispatch(self) -> None:
        views = reference_authority_views(namespace="binding-authority")
        spec = admit_and_prepare(views, "binding-authority")
        draft = binding(spec)
        with self.assertRaisesRegex(AuthorityDenied, "binding authority"):
            views.effects.admit_binding(draft)
        with self.assertRaisesRegex(AuthorityDenied, "binding authority"):
            views.execution.admit_binding(draft)
        self.assertEqual(
            views.bindings.authority_for(AuthorityRole.BINDING).role,
            AuthorityRole.BINDING,
        )
        self.assertEqual(views.bindings.admit_binding(draft).value, "created")

    def test_bound_dispatch_references_exact_binding(self) -> None:
        views = reference_authority_views(namespace="bound-dispatch")
        spec = admit_and_prepare(views, "bound-dispatch")
        admitted = binding(spec)
        views.bindings.admit_binding(admitted)
        dispatch_id = sid(IdKind.DISPATCH, "dispatch:bound")
        views.execution.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=dispatch_id,
            event_id=sid(IdKind.EVENT, "event:bound:dispatch"),
            recorded_at_ms=4,
            request_digest="sha256:bound-request",
            binding_id=admitted.binding_id,
            binding_digest=admitted.binding_digest,
        )
        dispatch = views.read.get_dispatch(dispatch_id)
        self.assertEqual(dispatch.binding_id, admitted.binding_id)
        self.assertEqual(dispatch.binding_digest, admitted.binding_digest)
        self.assertEqual(views.read.current_binding_for(spec.effect_id).binding_id, admitted.binding_id)
        views.read.validate_invariants()

    def test_dispatch_rejects_stale_or_mismatched_binding(self) -> None:
        views = reference_authority_views(namespace="binding-mismatch")
        spec = admit_and_prepare(views, "binding-mismatch")
        admitted = binding(spec)
        views.bindings.admit_binding(admitted)
        with self.assertRaisesRegex(InvariantViolation, "digest"):
            views.execution.begin_dispatch(
                spec.effect_id,
                expected_revision=1,
                dispatch_id=sid(IdKind.DISPATCH, "dispatch:mismatch"),
                event_id=sid(IdKind.EVENT, "event:mismatch:dispatch"),
                recorded_at_ms=4,
                request_digest="sha256:mismatch-request",
                binding_id=admitted.binding_id,
                binding_digest=BINDING_DIGEST_2,
            )

    def test_retryable_pre_admission_rejection_allows_new_binding(self) -> None:
        views = reference_authority_views(namespace="binding-retry")
        spec = admit_and_prepare(views, "binding-retry")
        first = binding(spec)
        views.bindings.admit_binding(first)
        dispatch_id = sid(IdKind.DISPATCH, "dispatch:binding-retry")
        views.execution.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=dispatch_id,
            event_id=sid(IdKind.EVENT, "event:binding-retry:dispatch"),
            recorded_at_ms=4,
            request_digest="sha256:retry-request",
            binding_id=first.binding_id,
            binding_digest=first.binding_digest,
        )
        with self.assertRaisesRegex(InvalidTransition, "cannot admit Binding"):
            views.bindings.admit_binding(binding(spec, 2, admitted_at_ms=5))
        views.execution.reject_dispatch(
            spec.effect_id,
            dispatch_id,
            expected_revision=2,
            event_id=sid(IdKind.EVENT, "event:binding-retry:rejected"),
            recorded_at_ms=5,
            reason_code="CONTRACT_MISMATCH",
            retryable=True,
            evidence_digest="sha256:contract-mismatch",
        )
        second = binding(spec, 2, admitted_at_ms=6)
        views.bindings.admit_binding(second)
        self.assertEqual(
            tuple(item.binding_revision for item in views.read.bindings_for(spec.effect_id)),
            (1, 2),
        )
        self.assertEqual(views.read.current_binding_for(spec.effect_id), replace(second, attestation=views.read.current_binding_for(spec.effect_id).attestation))

    def test_unknown_and_terminal_effects_cannot_rebind(self) -> None:
        for terminal in (False, True):
            with self.subTest(terminal=terminal):
                views = reference_authority_views(namespace=f"binding-closed-{terminal}")
                spec = admit_and_prepare(views, f"binding-closed-{terminal}")
                first = binding(spec)
                views.bindings.admit_binding(first)
                dispatch_id = sid(IdKind.DISPATCH, f"dispatch:binding-closed-{terminal}")
                views.execution.begin_dispatch(
                    spec.effect_id,
                    expected_revision=1,
                    dispatch_id=dispatch_id,
                    event_id=sid(IdKind.EVENT, f"event:binding-closed-{terminal}:dispatch"),
                    recorded_at_ms=4,
                    request_digest="sha256:closed-request",
                    binding_id=first.binding_id,
                    binding_digest=first.binding_digest,
                )
                views.execution.admit_dispatch(
                    spec.effect_id,
                    dispatch_id,
                    expected_revision=2,
                    event_id=sid(IdKind.EVENT, f"event:binding-closed-{terminal}:admitted"),
                    recorded_at_ms=5,
                    backend_operation_id=f"backend:closed:{terminal}",
                    evidence_digest="sha256:admitted",
                )
                if terminal:
                    views.execution.advance_effect(
                        spec.effect_id,
                        EffectState.SUCCEEDED,
                        expected_revision=3,
                        event_id=sid(IdKind.EVENT, f"event:binding-closed-{terminal}:success"),
                        recorded_at_ms=6,
                        evidence_digest="sha256:success",
                    )
                else:
                    views.execution.mark_dispatch_unknown(
                        spec.effect_id,
                        dispatch_id,
                        expected_revision=3,
                        event_id=sid(IdKind.EVENT, f"event:binding-closed-{terminal}:unknown"),
                        recorded_at_ms=6,
                        evidence_digest="sha256:unknown",
                    )
                with self.assertRaisesRegex(InvalidTransition, "cannot admit Binding"):
                    views.bindings.admit_binding(binding(spec, 2, admitted_at_ms=7))

    def test_k12_effect_binding_separation_survives_journal_restart(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "binding.sqlite3"
            views = journal_authority_views(path, namespace="binding-journal")
            spec = admit_and_prepare(views, "binding-journal")
            admitted = binding(spec)
            views.bindings.admit_binding(admitted)
            stored = views.read.current_binding_for(spec.effect_id)
            dispatch_id = sid(IdKind.DISPATCH, "dispatch:binding-journal")
            views.execution.begin_dispatch(
                spec.effect_id,
                expected_revision=1,
                dispatch_id=dispatch_id,
                event_id=sid(IdKind.EVENT, "event:binding-journal:dispatch"),
                recorded_at_ms=4,
                request_digest="sha256:journal-request",
                binding_id=stored.binding_id,
                binding_digest=stored.binding_digest,
            )
            views.read.close()

            reopened = journal_authority_views(path, namespace="binding-journal-reopen")
            self.assertEqual(reopened.read.current_binding_for(spec.effect_id), stored)
            dispatch = reopened.read.get_dispatch(dispatch_id)
            self.assertEqual(dispatch.binding_id, stored.binding_id)
            self.assertEqual(dispatch.binding_digest, stored.binding_digest)
            reopened.read.verify_from_genesis()
            reopened.read.close()

    def test_v3_journal_migrates_to_v4_and_keeps_unbound_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy-v3.sqlite3"
            views = journal_authority_views(path, namespace="binding-v3-writer")
            spec = admit_and_prepare(views, "binding-v3")
            dispatch_id = sid(IdKind.DISPATCH, "dispatch:binding-v3")
            views.execution.begin_dispatch(
                spec.effect_id,
                expected_revision=1,
                dispatch_id=dispatch_id,
                event_id=sid(IdKind.EVENT, "event:binding-v3:dispatch"),
                recorded_at_ms=3,
                request_digest="sha256:v3-request",
            )
            views.read.close()

            connection = sqlite3.connect(path)
            connection.execute("DROP TRIGGER journal_entries_no_update")
            rows = connection.execute(
                "SELECT sequence, payload_json, previous_digest FROM journal_entries ORDER BY sequence"
            ).fetchall()
            previous = "sha256:" + "0" * 64
            import hashlib

            for sequence, payload_json, _ in rows:
                payload = json.loads(payload_json)
                payload["schemaVersion"] = 3
                rendered = json.dumps(
                    payload,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                    allow_nan=False,
                )
                digest = "sha256:" + hashlib.sha256(
                    f"{previous}\n{rendered}".encode()
                ).hexdigest()
                connection.execute(
                    "UPDATE journal_entries SET payload_json=?, previous_digest=?, entry_digest=? WHERE sequence=?",
                    (rendered, previous, digest, sequence),
                )
                previous = digest
            connection.execute(
                "UPDATE journal_metadata SET value='3' WHERE key='schema_version'"
            )
            connection.execute(
                "UPDATE journal_metadata SET value='semantic-core-v3-slim' WHERE key='semantic_model_version'"
            )
            connection.execute(
                "UPDATE journal_metadata SET value='incremental-reducer-v3' WHERE key='reducer_version'"
            )
            connection.execute(
                "UPDATE journal_metadata SET value=? WHERE key='head_digest'", (previous,)
            )
            connection.commit()
            connection.close()

            reopened = journal_authority_views(path, namespace="binding-v3-reader")
            dispatch = reopened.read.get_dispatch(dispatch_id)
            self.assertIsNone(dispatch.binding_id)
            self.assertIsNone(dispatch.binding_digest)
            reopened.read.verify_from_genesis()
            reopened.read.close()
            connection = sqlite3.connect(path)
            schema = connection.execute(
                "SELECT value FROM journal_metadata WHERE key='schema_version'"
            ).fetchone()[0]
            connection.close()
            self.assertEqual(schema, str(JOURNAL_SCHEMA_VERSION))


if __name__ == "__main__":
    unittest.main()
