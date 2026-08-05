from __future__ import annotations

import os
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path

from ordivon_eval_data.backup import create_backup, restore_check
from ordivon_eval_data.projection import project

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
RESTIC = Path("/usr/bin/restic")


class BackupTests(unittest.TestCase):
    def test_backup_uses_online_sqlite_copy_and_restores_cleanly(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ordivon-restic-") as temporary:
            root = Path(temporary)
            evaluation_root = root / "evaluation"
            project(REPOSITORY_ROOT, evaluation_root)

            mlflow_database = root / "mlflow" / "mlflow.db"
            mlflow_database.parent.mkdir()
            connection = sqlite3.connect(mlflow_database)
            try:
                connection.execute(
                    "CREATE TABLE smoke (id INTEGER PRIMARY KEY, value TEXT NOT NULL)"
                )
                connection.execute("INSERT INTO smoke(value) VALUES ('verified')")
                connection.commit()
            finally:
                connection.close()
            artifacts = root / "mlflow" / "artifacts"
            artifacts.mkdir()
            (artifacts / "bounded.json").write_text('{"ok":true}\n', encoding="utf-8")

            password_file = root / "restic-password"
            password_file.write_text("local-test-password\n", encoding="utf-8")
            os.chmod(password_file, 0o600)
            repository = root / "restic-repository"
            environment = {
                **os.environ,
                "RESTIC_REPOSITORY": str(repository),
                "RESTIC_PASSWORD_FILE": str(password_file),
            }
            subprocess.run(
                [str(RESTIC), "init"],
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )

            backup = create_backup(
                evaluation_root=evaluation_root,
                mlflow_database=mlflow_database,
                mlflow_artifacts=artifacts,
                staging_root=root / "staging",
                repository=repository,
                password_file=password_file,
                restic=RESTIC,
            )
            restored = restore_check(
                repository=repository,
                password_file=password_file,
                restic=RESTIC,
            )
            self.assertEqual(restored["snapshotId"], backup["snapshotId"])
            self.assertEqual(
                restored["projectionGeneration"],
                backup["projectionGeneration"],
            )
            self.assertEqual(restored["sqliteIntegrity"], "ok")
            self.assertEqual(list((root / "staging").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
