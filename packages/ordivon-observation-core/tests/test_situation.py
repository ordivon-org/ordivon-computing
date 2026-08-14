from __future__ import annotations

import unittest

from ordivon_observation_core.situation import (
    SituationAnchor,
    SituationFacet,
    SituationRelation,
    compile_situation,
)


class SituationProjectionTests(unittest.TestCase):
    def anchor(self, suffix: str = "1") -> SituationAnchor:
        return SituationAnchor(
            "ordivon-host",
            "ordivon.host.task",
            f"task:p3:{suffix}",
        )

    def test_stale_locus_hint_requires_owner_currentness(self) -> None:
        anchor = self.anchor("stale")
        projection = compile_situation(
            anchor,
            (
                SituationFacet(
                    "ordivon-host",
                    "locus-hint",
                    "ordivon.runtime.workspace",
                    "workspace:p3:closed",
                    "navigation-hint",
                    related_to=(SituationRelation(anchor.kind, anchor.identity),),
                ),
                SituationFacet(
                    "ordivon-runtime",
                    "locus-observation",
                    "ordivon.runtime.workspace",
                    "workspace:p3:closed",
                    "closed",
                    currentness="unavailable",
                    authority="not-applicable",
                ),
            ),
        )
        self.assertIn(
            "hinted-locus-is-not-currently-usable",
            {item["reason"] for item in projection.unresolved},
        )
        self.assertIn(
            "navigation-hint-implies-current-locus",
            projection.rejected_implications,
        )

    def test_missing_locus_probe_remains_unresolved(self) -> None:
        anchor = self.anchor("missing-probe")
        projection = compile_situation(
            anchor,
            (
                SituationFacet(
                    "ordivon-host",
                    "locus-hint",
                    "ordivon.runtime.workspace",
                    "workspace:p3:hint-only",
                    "navigation-hint",
                ),
            ),
        )
        self.assertEqual(
            projection.unresolved[0]["reason"],
            "locus-hint-has-no-current-owner-observation",
        )

    def test_installed_action_requires_exact_admission(self) -> None:
        anchor = self.anchor("action")
        action = SituationFacet(
            "ordivon-harness",
            "action-surface",
            "ordivon.harness.action",
            "compose_tool_program",
            "installed",
            currentness="current",
        )
        missing = compile_situation(anchor, (action,))
        self.assertIn(
            "installed-action-has-no-exact-current-admission",
            {item["reason"] for item in missing.unresolved},
        )
        admitted = compile_situation(
            anchor,
            (
                action,
                SituationFacet(
                    "ordivon-harness",
                    "admission",
                    "ordivon.harness.action",
                    "compose_tool_program",
                    "turn-admitted",
                    currentness="current",
                    authority="granted",
                ),
            ),
        )
        self.assertNotIn(
            "installed-action-has-no-exact-current-admission",
            {item["reason"] for item in admitted.unresolved},
        )

    def test_runtime_success_does_not_prove_semantic_completion(self) -> None:
        anchor = self.anchor("completion")
        projection = compile_situation(
            anchor,
            (
                SituationFacet(
                    "ordivon-runtime",
                    "occurrence",
                    "ordivon.runtime.job",
                    "job:p3:1",
                    "succeeded",
                    currentness="historical",
                    authority="not-applicable",
                ),
                SituationFacet(
                    "ordivon-host",
                    "completion",
                    "ordivon.host.task",
                    anchor.identity,
                    "ready",
                    currentness="current",
                ),
            ),
        )
        self.assertIn(
            "semantic-completion-not-proven-by-physical-runtime-success",
            {item["reason"] for item in projection.unresolved},
        )

    def test_world_unknown_surfaces_owner_route_without_authority(self) -> None:
        anchor = self.anchor("world")
        projection = compile_situation(
            anchor,
            (
                SituationFacet(
                    "ordivon-world",
                    "recovery",
                    "ordivon.world.provider-dispatch",
                    "dispatch:p3:unknown",
                    "unknown",
                    currentness="unknown",
                    authority="not-granted",
                    next_owner_operation="reconcile-original-request-without-redispatch",
                ),
            ),
        )
        self.assertEqual(
            projection.next_owner_operations[0],
            {
                "owner": "ordivon-world",
                "identity": "dispatch:p3:unknown",
                "operation": "reconcile-original-request-without-redispatch",
                "authority": "not-granted",
            },
        )
        self.assertIn("unknown-implies-failure", projection.rejected_implications)

    def test_unknown_without_owner_route_remains_unresolved(self) -> None:
        anchor = self.anchor("unknown-no-route")
        projection = compile_situation(
            anchor,
            (
                SituationFacet(
                    "ordivon-world",
                    "recovery",
                    "ordivon.world.provider-dispatch",
                    "dispatch:p3:no-route",
                    "unknown",
                    currentness="unknown",
                    authority="not-granted",
                ),
            ),
        )
        self.assertIn(
            "unknown-has-no-owner-recovery-route",
            {item["reason"] for item in projection.unresolved},
        )

    def test_projection_is_order_independent_and_digest_stable(self) -> None:
        anchor = self.anchor("order")
        facets = (
            SituationFacet(
                "ordivon-runtime",
                "occurrence",
                "ordivon.runtime.job",
                "job:p3:2",
                "succeeded",
                currentness="historical",
                authority="not-applicable",
            ),
            SituationFacet(
                "ordivon-host",
                "completion",
                "ordivon.host.task",
                anchor.identity,
                "ready",
                currentness="current",
            ),
        )
        self.assertEqual(
            compile_situation(anchor, facets).to_dict(),
            compile_situation(anchor, tuple(reversed(facets))).to_dict(),
        )

    def test_duplicate_owner_role_identity_fails(self) -> None:
        anchor = self.anchor("duplicate")
        facet = SituationFacet(
            "ordivon-host",
            "continuity",
            "ordivon.host.task",
            anchor.identity,
            "ready",
            currentness="current",
        )
        with self.assertRaisesRegex(ValueError, "unique owner-qualified"):
            compile_situation(anchor, (facet, facet))

    def test_contract_validation_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            SituationAnchor("Host", "ordivon.host.task", "task:p3:bad-owner")
        with self.assertRaisesRegex(ValueError, "unsupported Situation role"):
            SituationFacet(
                "ordivon-host",
                "memory",
                "ordivon.host.task",
                "task:p3:bad-role",
                "ready",
            )
        with self.assertRaisesRegex(ValueError, "unsupported Situation currentness"):
            SituationFacet(
                "ordivon-host",
                "continuity",
                "ordivon.host.task",
                "task:p3:bad-currentness",
                "ready",
                currentness="probably",
            )
        with self.assertRaisesRegex(ValueError, "unsupported Situation authority"):
            SituationFacet(
                "ordivon-host",
                "continuity",
                "ordivon.host.task",
                "task:p3:bad-authority",
                "ready",
                authority="superuser",
            )


if __name__ == "__main__":
    unittest.main()
