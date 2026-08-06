from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "plan-v1.json"


def canonical_digest(value: dict[str, object]) -> str:
    payload = dict(value)
    payload.pop("integrity", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


class ObservationPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    def test_identity_status_and_integrity(self) -> None:
        self.assertEqual(self.plan["schemaVersion"], 1)
        self.assertEqual(
            self.plan["kind"],
            "ordivon.host-harness-observation-plan",
        )
        self.assertEqual(self.plan["planId"], "HHO-P0-P1-001")
        self.assertEqual(
            self.plan["status"],
            "level_a_complete_join_inventory_frozen_exporters_ready",
        )
        self.assertEqual(
            self.plan["integrity"],
            {
                "algorithm": "sha256",
                "canonicalization": "ordivon-evidence-json-v1",
                "payloadDigest": canonical_digest(self.plan),
            },
        )

    def test_revision_authority_is_exact(self) -> None:
        authority = self.plan["revisionAuthority"]
        revisions = [
            authority["authoritySourceRevision"],
            authority["sharedContractRevision"],
            *authority["selectedOwnerRevisions"].values(),
        ]
        for revision in revisions:
            self.assertRegex(revision, re.compile(r"^[0-9a-f]{40}$"))
        self.assertEqual(
            authority["implementationRevisions"],
            {"B2-A": None, "B2-H": None, "B2-R": None},
        )

    def test_authorities_remain_separate(self) -> None:
        decisions = self.plan["decisions"]
        self.assertTrue(decisions["hostAndHarnessIndependentAuthorities"])
        self.assertTrue(decisions["newRunDualWriteForbidden"])
        self.assertFalse(decisions["observationPlaneAuthoritative"])
        self.assertFalse(decisions["openTelemetryProjectionAuthoritative"])
        self.assertFalse(decisions["automaticEvalAdmission"])
        self.assertTrue(decisions["ownerDatabasesReadOnlyToObservation"])
        self.assertTrue(decisions["exporterCheckpointsOutsideOwnerStores"])
        owners = {item["owner"] for item in self.plan["authority"]}
        self.assertEqual(
            owners,
            {
                "ordivon-host",
                "ordivon-harness",
                "ordivon-runtime",
                "domain_project",
                "observation_plane",
            },
        )

    def test_p0_contains_no_observation_platform(self) -> None:
        p0 = self.plan["p0"]
        self.assertEqual(
            p0["status"],
            "accepted_release_reproducible_staging_rehearsed_production_inactive",
        )
        self.assertEqual(p0["closeoutBlockers"], [])
        self.assertFalse(p0["productionAuthorityActivated"])
        self.assertIn(
            "request_only_external_recovery_gap_full_tested",
            p0["completedCloseoutItems"],
        )
        forbidden = set(p0["forbiddenCapabilities"])
        self.assertTrue(
            {
                "observation_gateway",
                "open_telemetry_collector",
                "global_observation_database",
                "dashboard",
                "new_run_dual_write",
            }.issubset(forbidden)
        )
        self.assertEqual(p0["migration"]["newRunStoreCount"], 1)
        self.assertFalse(p0["migration"]["bulkRewriteHistoricalBytes"])
        self.assertFalse(p0["migration"]["crossStoreAtomicTransactionClaim"])

    def test_p0_has_independent_state_roots_and_composition_gates(self) -> None:
        p0 = self.plan["p0"]
        self.assertEqual(p0["stateRoots"]["host"], "/var/lib/ordivon/host")
        self.assertEqual(p0["stateRoots"]["harness"], "/var/lib/ordivon/harness")
        gates = set(p0["acceptanceGates"])
        self.assertIn("host_complete_suite_without_harness_installed", gates)
        self.assertIn("harness_core_suite_without_host_installed", gates)
        self.assertIn("host_fake_external_harness_end_to_end", gates)
        self.assertIn("domain_harness_without_synthetic_host_task", gates)
        self.assertIn("no_new_run_written_to_both_stores", gates)

    def test_p1_uses_journals_and_at_least_once_deduplication(self) -> None:
        decisions = self.plan["decisions"]
        self.assertTrue(decisions["hostJournalAsOutbox"])
        self.assertTrue(decisions["harnessJournalAsOutbox"])
        self.assertTrue(decisions["transactionalOutboxForMutableDomainStores"])
        delivery = self.plan["p1"]["delivery"]
        self.assertEqual(delivery["sourceToGateway"], "at_least_once")
        self.assertEqual(delivery["catalogDeduplication"], "event_id")
        self.assertTrue(delivery["perSourceOrdering"])
        self.assertFalse(delivery["gatewayRequiredForOwnerCommit"])
        self.assertFalse(delivery["collectorRequiredForOwnerCommit"])

    def test_p1_core_producers_and_privacy(self) -> None:
        p1 = self.plan["p1"]
        self.assertEqual(
            p1["status"],
            "minimum_core_m1_and_join_inventory_complete_exporters_pending",
        )
        self.assertFalse(
            p1["executionReadiness"]["contractAndGatewayFixtureWorkMayStart"]
        )
        self.assertTrue(p1["executionReadiness"]["p0CloseoutSatisfied"])
        self.assertTrue(
            p1["executionReadiness"]["runOnceExporterWorkMayStart"]
        )
        self.assertTrue(
            p1["executionReadiness"]["productionExporterEnablementRequiresP0Closeout"]
        )
        self.assertTrue(
            p1["executionReadiness"]["formalTrialsRequireMinimumExperimentalCore"]
        )
        self.assertFalse(
            p1["executionReadiness"]["formalTrialsRequireP1CoreCloseout"]
        )
        self.assertFalse(
            p1["executionReadiness"]["openTelemetryInteropBlocksFormalTrials"]
        )
        self.assertEqual(
            p1["requiredProducers"],
            ["ordivon-host", "ordivon-harness", "ordivon-runtime"],
        )
        privacy = p1["privacy"]
        self.assertEqual(privacy["rawPrivateReasoning"], "forbidden")
        self.assertEqual(privacy["secrets"], "reject")
        self.assertEqual(
            privacy["defaultModelContent"],
            "digest_and_private_owner_ref",
        )
        self.assertFalse(p1["repositoryAdmissionGate"]["authorizedNow"])

    def test_reliability_and_correlation_gates_are_explicit(self) -> None:
        gates = set(self.plan["p1"]["acceptanceGates"])
        self.assertIn(
            "gateway_down_during_ten_thousand_source_events_then_zero_missing",
            gates,
        )
        self.assertIn(
            "exporter_crash_after_ingest_before_ack_deduplicates",
            gates,
        )
        self.assertIn("standalone_harness_run_query_without_host_ids", gates)
        self.assertIn(
            "host_external_harness_query_without_ordivon_harness_types", gates
        )
        self.assertIn("host_harness_runtime_complete_correlation", gates)
        self.assertIn("process_exit_success_does_not_imply_task_acceptance", gates)

    def test_formal_trials_are_blocked_but_design_is_retained(self) -> None:
        value = self.plan["formalTrialEffect"]
        self.assertEqual(value["planId"], "HHR-R3-001")
        self.assertTrue(value["designRetained"])
        self.assertEqual(
            value["executionStatus"],
            "blocked_by_p1_exporters_selection_and_formal_runner",
        )
        self.assertEqual(len(value["resumeRequirements"]), 5)
        self.assertEqual(value["satisfiedPrerequisites"], ["p0_passed"])
        self.assertIn(
            "observation_selection_manifest_stable",
            value["resumeRequirements"],
        )
        self.assertIn("p1_minimum_core_passed", value["resumeRequirements"])

    def test_execution_plan_and_read_only_exporter_state_are_explicit(self) -> None:
        execution_path = Path(self.plan["executionPlanRef"])
        self.assertTrue(execution_path.exists())
        rendered = execution_path.read_text(encoding="utf-8")
        self.assertIn("P1 Core", rendered)
        self.assertIn("Owner databases are read-only to P1", rendered)
        self.assertIn("Immediate Ready Frontier", rendered)
        delivery = self.plan["p1"]["delivery"]
        self.assertFalse(delivery["ownerDatabaseWrites"])
        self.assertEqual(
            delivery["exporterCheckpointLocation"],
            "observation_owned_sidecar",
        )
        self.assertEqual(
            self.plan["p1"]["nativeStreams"]["ordivon-runtime"],
            "one_stream_per_runtime_job",
        )

    def test_experiment_loop_boundary_keeps_p1_as_sensing_only(self) -> None:
        decisions = self.plan["decisions"]
        self.assertFalse(decisions["observationOwnsTrialValidity"])
        self.assertFalse(decisions["observationOwnsCandidateSelection"])
        boundary = self.plan["p1"]["experimentLoopBoundary"]
        self.assertEqual(boundary["downstreamPlanId"], "CEL-R4-001")
        self.assertIn("source_stream_completeness", boundary["p1Owns"])
        self.assertIn("trial_validity", boundary["p1DoesNotOwn"])
        self.assertEqual(
            boundary["selectionFreezeRecord"],
            "ObservationSelectionManifest",
        )
        relations = self.plan["p1"]["relationVocabulary"]
        self.assertIn("derived_from", relations)
        self.assertIn("evaluates", relations)
        fixtures = self.plan["p1"]["evaluationReadinessFixtures"]
        self.assertEqual(len(fixtures), 4)
        self.assertIn("externally_invalid_complete_trajectory", fixtures)
        self.assertIn("incomplete_trajectory", fixtures)
        self.assertIn(
            "observation_selection_manifest_fixture_stable",
            self.plan["p1"]["coreCloseoutGate"],
        )

    def test_join_inventory_and_typed_key_policy_are_frozen(self) -> None:
        p1 = self.plan["p1"]
        policy = p1["typedPayloadKeyExtraction"]
        self.assertTrue(policy["authorized"])
        self.assertEqual(policy["purpose"], "stable_foreign_identity_only")
        inventory = Path(policy["inventory"])
        self.assertTrue(inventory.exists())
        self.assertIn("raw_payload_not_copied", policy["requirements"])

    def test_m1_implementation_and_canonical_time_correction_are_frozen(self) -> None:
        p1 = self.plan["p1"]
        correction = p1["contractCorrections"]
        self.assertTrue(correction["canonicalEnvelopeExcludesDynamicExportTime"])
        self.assertTrue(correction["occurredAtMsIsOwnerNativeAndCanonical"])
        self.assertTrue(correction["exportedAtAndIngestedAtAreReceiptOnly"])
        progress = p1["implementationProgress"]
        self.assertEqual(progress["M1"]["status"], "implemented")
        self.assertEqual(progress["M1"]["tests"], 21)
        self.assertEqual(progress["M1"]["fixture"]["events"], 13)
        self.assertEqual(progress["M1"]["fixture"]["streams"], 3)
        self.assertEqual(
            progress["M2"]["status"],
            "shared_contract_and_join_inventory_complete_owner_exporters_ready",
        )
        self.assertEqual(
            progress["M2"]["contractRevision"],
            "b0973311d84b0debe30ca002e15e02401e16ee36",
        )
        self.assertEqual(
            progress["M2"]["streamSemantics"]["runtime"],
            "per_job_event_sequence",
        )
        self.assertEqual(progress["M3"]["status"], "blocked_by_M2")
        self.assertIn("owner_exporters", progress["M1"]["notIncluded"])

    def test_minimum_core_precedes_production_hardening(self) -> None:
        p1 = self.plan["p1"]
        self.assertIn("in_process_sqlite_gateway", p1["minimumExperimentalCore"])
        self.assertIn("run_once_harness_exporter", p1["minimumExperimentalCore"])
        self.assertIn(
            "open_telemetry_bridge_and_collector",
            p1["productionHardeningDeferred"],
        )
        self.assertIn(
            "one_million_event_query_benchmark",
            p1["productionHardeningDeferred"],
        )

    def test_no_heavy_platform_or_secret_paths(self) -> None:
        rendered = json.dumps(self.plan, sort_keys=True).lower()
        for forbidden in (
            "api_key",
            "bearer_token",
            "/root/.config/ordivon/secrets",
            'raw_chain_of_thought_collection": true',
        ):
            self.assertNotIn(forbidden, rendered)
        self.assertIn("kafka", self.plan["nonGoals"])
        self.assertIn("clickhouse", self.plan["nonGoals"])
        self.assertIn("dashboard", self.plan["nonGoals"])


if __name__ == "__main__":
    unittest.main()
