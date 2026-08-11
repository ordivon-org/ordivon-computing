from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "ordivon_lab.py"
SPEC = importlib.util.spec_from_file_location("ordivon_lab", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)
obs = lab.observation


class OrdivonLabTests(unittest.TestCase):
    def _bundle(self, directory: Path) -> Path:
        producer = obs.ObservationProducerIdentity(
            "ordivon-runtime", "runtime-registry", "runtime:test"
        )
        source = obs.ObservationSource(
            project_id="ordivon-runtime",
            component_id="runtime-registry",
            instance_id="runtime:test",
            stream_id="runtime-job:1",
            sequence=1,
            native_kind="ordivon.runtime.job-terminal",
            native_id="event:test:1",
            native_revision=None,
            native_digest="sha256:" + "a" * 64,
            mapping_version="runtime-observation-v1",
        )
        event = obs.ObservationEnvelope.build(
            occurred_at_ms=10,
            source=source,
            privacy=obs.ObservationPrivacy(
                "private_metadata", "test-policy"
            ),
            attributes={"status": "succeeded"},
        )
        checkpoint_path = directory / "checkpoint.json"
        before = obs.load_checkpoint(
            checkpoint_path,
            producer_identity=producer,
            mapping_version="runtime-observation-v1",
        )
        after = before.advance({source.stream_id: 1}, updated_at_ms=11)
        bundle = obs.ObservationExportBundle.build(
            producer_identity=producer,
            mapping_version="runtime-observation-v1",
            owner_revision="1" * 40,
            exporter_revision="2" * 40,
            exported_at_ms=12,
            checkpoint_before=before,
            checkpoint_after=after,
            batches=(obs.ObservationBatch.build(request_id="request:test", events=(event,)),),
        )
        return obs.write_export_bundle(directory / "outbox", bundle)

    def test_evidence_pack_preserves_owner_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            bundle = self._bundle(directory)
            pack = lab.build_evidence_pack(
                pack_id="pack:test", bundle_paths=(bundle,), created_at_ms=20
            )
            self.assertEqual(pack["summary"]["eventCount"], 1)
            self.assertFalse(pack["inferenceBoundary"]["ownerTruthCopied"])
            self.assertFalse(pack["inferenceBoundary"]["scientificCompletionInferred"] if "scientificCompletionInferred" in pack["inferenceBoundary"] else pack["inferenceBoundary"]["semanticCompletionInferred"])
            self.assertEqual(pack["integrity"]["payloadDigest"], lab.payload_digest(pack))

    def test_matrix_replays_terminal_trials_and_parquet_is_derived(self) -> None:
        if not Path("/usr/bin/duckdb").exists():
            self.skipTest("DuckDB CLI is not installed")
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            spec_path = directory / "matrix.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "kind": "ordivon.lab.experiment-matrix-spec",
                        "experimentId": "matrix:test",
                        "factors": {"mode": ["ok", "fail"]},
                        "replicates": 2,
                        "command": {
                            "executable": sys.executable,
                            "args": [
                                "-c",
                                "import sys; print(sys.argv[1]); sys.exit(0 if sys.argv[1]=='ok' else 3)",
                                "{mode}",
                            ],
                            "cwd": ".",
                        },
                        "timeoutMs": 5000,
                        "maxWorkers": 2,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            run_dir = directory / "run"
            first = lab.run_matrix(spec_path=spec_path, output_dir=run_dir)
            self.assertEqual(first["trialCount"], 4)
            self.assertEqual(first["mechanicalSuccesses"], 2)
            self.assertEqual(first["resumedTerminalTrials"], 0)
            second = lab.run_matrix(spec_path=spec_path, output_dir=run_dir)
            self.assertEqual(second["resumedTerminalTrials"], 4)
            self.assertEqual(second["newlyExecutedTrials"], 0)
            analysis = lab.materialize_matrix_analysis(
                run_dir=run_dir,
                output_dir=directory / "analysis",
                duckdb=Path("/usr/bin/duckdb"),
            )
            self.assertEqual(analysis["rows"], 4)
            self.assertTrue(Path(analysis["files"]["parquet"]["path"]).is_file())
            self.assertIn("derived analytical projection", analysis["authorityBoundary"])

    def test_pressure_pack_reports_delta_without_priority(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repo = root / "ordivon-test"
            repo.mkdir()
            subprocess.run(["/usr/bin/git", "init", "-q", str(repo)], check=True)
            subprocess.run(["/usr/bin/git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["/usr/bin/git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            (repo / "a.txt").write_text("one\n", encoding="utf-8")
            subprocess.run(["/usr/bin/git", "-C", str(repo), "add", "a.txt"], check=True)
            subprocess.run(["/usr/bin/git", "-C", str(repo), "commit", "-qm", "one"], check=True)
            observed = subprocess.check_output(["/usr/bin/git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            (repo / "a.txt").write_text("two\n", encoding="utf-8")
            subprocess.run(["/usr/bin/git", "-C", str(repo), "commit", "-qam", "two"], check=True)
            frontier = root / "frontier.json"
            frontier.write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "kind": "ordivon.world-model-assimilation-frontier",
                        "projects": [{"projectId": "ordivon-test", "observedRevision": observed}],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            pack = lab.build_pressure_pack(
                frontier_path=frontier,
                project_root=root,
                created_at_ms=30,
            )
            row = pack["projects"][0]
            self.assertEqual(row["relation"], "owner_advanced")
            self.assertEqual(row["changedPathCount"], 1)
            self.assertEqual(row["changedPaths"][0]["path"], "a.txt")
            self.assertFalse(pack["inferenceBoundary"]["importanceScoreProduced"])
            self.assertFalse(pack["inferenceBoundary"]["recommendedActionProduced"])


if __name__ == "__main__":
    unittest.main()
