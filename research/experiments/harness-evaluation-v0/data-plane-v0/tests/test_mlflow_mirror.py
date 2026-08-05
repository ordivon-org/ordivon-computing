from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from mlflow import MlflowClient

from ordivon_eval_data.mlflow_mirror import check_server_health, mirror
from ordivon_eval_data.projection import project
from ordivon_eval_data.status import inspect_status

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]


def _free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


class MlflowMirrorTests(unittest.TestCase):
    def test_direct_mirror_is_idempotent_and_ui_reads_same_store(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ordivon-mlflow-") as temporary:
            root = Path(temporary)
            evaluation_root = root / "evaluation"
            project(REPOSITORY_ROOT, evaluation_root)
            backend = root / "mlflow.db"
            artifacts = root / "artifacts"
            artifacts.mkdir()
            direct_uri = f"sqlite:///{backend}"
            artifact_location = artifacts.resolve().as_uri()

            first = mirror(
                evaluation_root,
                direct_uri,
                artifact_location=artifact_location,
            )
            second = mirror(
                evaluation_root,
                direct_uri,
                artifact_location=artifact_location,
            )
            self.assertEqual(first["created"], 10)
            self.assertEqual(first["reused"], 0)
            self.assertEqual(second["created"], 0)
            self.assertEqual(second["reused"], 10)
            self.assertEqual(first["runIds"], second["runIds"])

            client = MlflowClient(tracking_uri=direct_uri)
            experiment = client.get_experiment_by_name("ordivon-harness-evaluation-v0")
            self.assertIsNotNone(experiment)
            self.assertEqual(experiment.artifact_location, artifact_location)
            runs = client.search_runs([experiment.experiment_id], max_results=100)
            self.assertEqual(len(runs), 10)
            for run in runs:
                self.assertEqual(
                    run.data.tags["ordivon.mirror_authority"],
                    "downstream_projection_only",
                )
                self.assertIn("ordivon.source_set_digest", run.data.tags)
                artifacts_for_run = client.list_artifacts(run.info.run_id, "ordivon")
                names = {Path(item.path).name for item in artifacts_for_run}
                self.assertEqual(
                    names,
                    {
                        "artifact-references.json",
                        "failures.json",
                        "projection-reference.json",
                        "result.json",
                        "task.json",
                        "trial.json",
                    },
                )
                self.assertTrue(all("terminal-evidence" not in name for name in names))

            status = inspect_status(
                evaluation_root=evaluation_root,
                tracking_uri=direct_uri,
                mlflow_database=backend,
            )
            self.assertEqual(status["status"], "healthy")
            self.assertEqual(status["mlflow"]["runCount"], 10)
            self.assertEqual(status["projection"]["inventory"]["trials"], 10)

            port = _free_port()
            http_uri = f"http://127.0.0.1:{port}"
            mlflow_executable = Path(sys.executable).parent / "mlflow"
            process = subprocess.Popen(
                [
                    str(mlflow_executable),
                    "server",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(port),
                    "--workers",
                    "1",
                    "--backend-store-uri",
                    direct_uri,
                    "--artifacts-destination",
                    str(artifacts),
                    "--allowed-hosts",
                    f"127.0.0.1:{port},localhost:{port}",
                ],
                cwd=root,
                env={
                    **os.environ,
                    "MLFLOW_SERVER_ENABLE_JOB_EXECUTION": "false",
                    "MLFLOW_DISABLE_TELEMETRY": "true",
                },
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            try:
                deadline = time.monotonic() + 45
                while True:
                    if process.poll() is not None:
                        self.fail(f"MLflow server exited with code {process.returncode}")
                    try:
                        check_server_health(http_uri, timeout_seconds=1)
                        break
                    except OSError:
                        if time.monotonic() >= deadline:
                            self.fail("MLflow UI server did not become healthy")
                        time.sleep(0.25)
                http_client = MlflowClient(tracking_uri=http_uri)
                http_experiment = http_client.get_experiment_by_name(
                    "ordivon-harness-evaluation-v0"
                )
                http_runs = http_client.search_runs(
                    [http_experiment.experiment_id], max_results=100
                )
                self.assertEqual(len(http_runs), 10)
            finally:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=10)


if __name__ == "__main__":
    unittest.main()
