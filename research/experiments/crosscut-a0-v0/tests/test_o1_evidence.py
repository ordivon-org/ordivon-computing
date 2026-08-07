from __future__ import annotations

import json
from pathlib import Path
import unittest

from ordivon_observation_core import (
    ObservationExportBundle,
    ObservationSelectionManifest,
    canonical_digest,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "evidence"
EXPECTED_FILES = {
    "host-observation-bundle.json",
    "harness-observation-bundle.json",
    "runtime-observation-bundle.json",
    "selection.json",
    "receipt.json",
}
EXPECTED_COMPUTING_REVISION = "c772e93a9d102139842991c19922bed45e640211"
EXPECTED_HOST_REVISION = "a76a620160b28d870670696e04c39e539296fe00"
EXPECTED_HARNESS_REVISION = "0d1e825e37b139d6b0b31a307fdc8bf904eeb722"
EXPECTED_RUNTIME_REVISION = "a455fd01ce0dea25684956e5e5da899d41832a1b"
EXPECTED_RUNTIME_EXPORTER_REVISION = "4bc563e6da83af50679149002d31507cbd703305"


def evidence_directory() -> Path:
    matches = sorted(EVIDENCE_ROOT.glob("o1-current-a0-o1-*"))
    if len(matches) != 1:
        raise AssertionError(f"expected one retained O1 evidence directory, found {len(matches)}")
    return matches[0]


def load(name: str) -> dict[str, object]:
    value = json.loads((evidence_directory() / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} must contain an object")
    return value


class CrosscutA0O1EvidenceTests(unittest.TestCase):
    def test_inventory_and_receipt_integrity(self) -> None:
        root = evidence_directory()
        self.assertEqual({path.name for path in root.iterdir() if path.is_file()}, EXPECTED_FILES)
        receipt = load("receipt.json")
        payload = {key: value for key, value in receipt.items() if key != "integrity"}
        self.assertEqual(
            receipt["integrity"]["payloadDigest"],
            canonical_digest(payload),
        )
        self.assertEqual(receipt["status"], "accepted_fresh_current_trajectory")
        self.assertTrue(all(receipt["checks"].values()))
        self.assertFalse(receipt["productionObservationActivated"])

    def test_exact_source_revisions_and_large_registry_scope(self) -> None:
        receipt = load("receipt.json")
        source = receipt["source"]
        self.assertEqual(source["computingImplementationRevision"], EXPECTED_COMPUTING_REVISION)
        self.assertEqual(source["hostRevision"], EXPECTED_HOST_REVISION)
        self.assertEqual(source["harnessRevision"], EXPECTED_HARNESS_REVISION)
        self.assertEqual(source["runtimeOwnerRevision"], EXPECTED_RUNTIME_REVISION)
        self.assertEqual(
            source["runtimeExporterRevision"], EXPECTED_RUNTIME_EXPORTER_REVISION
        )
        self.assertFalse(source["computingDirtyAtStart"])
        self.assertFalse(source["hostDirtyAtStart"])
        self.assertFalse(source["harnessDirtyAtStart"])
        self.assertFalse(source["runtimeDirtyAtStart"])
        self.assertFalse(source["runtimeExporterDirtyAtStart"])
        observation = receipt["observation"]
        self.assertGreater(observation["runtimeRegistryJobCount"], 10_000)
        self.assertEqual(observation["runtimeExportJobCount"], 1)
        self.assertTrue(observation["exactRuntimeJobSelection"])
        self.assertEqual(observation["selectedEventCount"], 25)

    def test_bundles_selection_and_terminal_measurements_are_bound(self) -> None:
        receipt = load("receipt.json")
        selection = ObservationSelectionManifest.from_dict(load("selection.json"))
        self.assertEqual(selection.selection_digest, receipt["observation"]["selectionDigest"])
        self.assertTrue(selection.completeness["complete"])
        self.assertFalse(selection.completeness["trialValidityInferred"])
        self.assertTrue(selection.privacy["metadataOnly"])
        self.assertFalse(selection.privacy["payloadBytesCopied"])
        self.assertFalse(selection.privacy["secretForbiddenPresent"])

        bundles: dict[str, ObservationExportBundle] = {}
        for owner in ("host", "harness", "runtime"):
            bundle = ObservationExportBundle.from_dict(load(f"{owner}-observation-bundle.json"))
            bundles[owner] = bundle
            self.assertEqual(
                bundle.integrity_digest,
                receipt["observation"][f"{owner}BundleDigest"],
            )

        measurement_events = [
            event
            for batch in bundles["harness"].batches
            for event in batch.events
            if event.measurements
        ]
        self.assertEqual(len(measurement_events), 1)
        terminal = measurement_events[0]
        self.assertEqual(
            terminal.source.native_kind,
            "ordivon.harness.harness.run-completed",
        )
        observed = {
            key: {"value": measurement.value, "unit": measurement.unit}
            for key, measurement in terminal.measurements.items()
        }
        self.assertEqual(observed, receipt["observation"]["harnessTerminalMeasurements"])
        self.assertEqual(
            observed["ordivon.harness.total_tokens"],
            {"value": 58, "unit": "token"},
        )
        self.assertEqual(receipt["run"]["usageSummary"]["totalTokens"], 58)
        self.assertFalse(receipt["run"]["providerCallUsageDetailsRetained"])

    def test_crosscut_evidence_contains_no_provider_call_or_secret_payload(self) -> None:
        encoded = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(evidence_directory().iterdir())
            if path.is_file()
        ).lower()
        for forbidden in (
            "authorization",
            "bearer_token",
            "api_key",
            "raw chain of thought",
            "private reasoning",
            '"providerusage"',
            '"inputtokens"',
            '"outputtokens"',
            "/etc/ordivon/ordivon-runtime.env",
        ):
            self.assertNotIn(forbidden, encoded)


if __name__ == "__main__":
    unittest.main()
