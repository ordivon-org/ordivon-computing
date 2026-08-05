from __future__ import annotations

import os
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SYSTEMD_ROOT = PACKAGE_ROOT / "packaging" / "systemd"


class PackagingTests(unittest.TestCase):
    def test_mlflow_ui_is_bounded_and_on_demand(self) -> None:
        unit = (SYSTEMD_ROOT / "ordivon-mlflow.service").read_text(encoding="utf-8")
        self.assertIn("--host 127.0.0.1", unit)
        self.assertIn("--allowed-hosts 127.0.0.1:5050,localhost:5050", unit)
        self.assertIn("MLFLOW_SERVER_ENABLE_JOB_EXECUTION=false", unit)
        self.assertIn("MLFLOW_DISABLE_TELEMETRY=true", unit)
        self.assertIn("MemoryMax=768M", unit)
        self.assertNotIn("--disable-security-middleware", unit)
        self.assertNotIn("WantedBy=", unit)
        self.assertIn("ProtectSystem=strict", unit)
        self.assertIn("UMask=0077", unit)

    def test_projection_and_backup_are_bounded_oneshot_services(self) -> None:
        projection = (SYSTEMD_ROOT / "ordivon-evaluation-project.service").read_text(
            encoding="utf-8"
        )
        backup = (SYSTEMD_ROOT / "ordivon-evaluation-backup.service").read_text(encoding="utf-8")
        self.assertIn("Type=oneshot", projection)
        self.assertIn("Type=oneshot", backup)
        self.assertIn("ordivon-eval-data project", projection)
        self.assertIn("ordivon-eval-data mirror", projection)
        self.assertIn("--tracking-uri sqlite:////", projection)
        self.assertIn("--artifact-location file:///", projection)
        self.assertNotIn("Requires=ordivon-mlflow.service", projection)
        self.assertIn("RestrictAddressFamilies=AF_UNIX", projection)
        self.assertIn("ordivon-eval-data backup", backup)
        self.assertIn("ordivon-eval-data restore-check", backup)
        self.assertIn("/var/lib/ordivon/analytics/restic-cache", backup)
        self.assertNotIn("workspace.exec", projection + backup)

    def test_operator_commands_are_executable(self) -> None:
        for name in ("install-local", "status", "ui", "stop-ui"):
            path = PACKAGE_ROOT / "scripts" / name
            self.assertTrue(path.is_file())
            self.assertTrue(path.stat().st_mode & os.X_OK)

    def test_installer_keeps_mlflow_ui_stopped(self) -> None:
        installer = (PACKAGE_ROOT / "scripts" / "install-local").read_text(encoding="utf-8")
        self.assertIn("disable --now ordivon-mlflow.service", installer)
        self.assertNotIn("enable --now ordivon-mlflow.service", installer)
        self.assertIn("ordivon-evaluation-project.service", installer)
        self.assertIn("ordivon-evaluation-backup.service", installer)
        self.assertIn("RESTIC_CACHE_DIR=$restic_cache", installer)

    def test_installer_builds_the_virtual_environment_at_its_final_path(self) -> None:
        installer = (PACKAGE_ROOT / "scripts" / "install-local").read_text(encoding="utf-8")
        move_index = installer.index('mv "$release_temporary" "$release"')
        sync_index = installer.index('--project "$release/source"')
        self.assertLess(move_index, sync_index)
        self.assertNotIn('--project "$release_temporary/source"', installer)
        self.assertIn(
            '"$release/source/.venv/bin/ordivon-eval-data" --help',
            installer,
        )

    def test_timers_are_persistent_and_bounded(self) -> None:
        projection = (SYSTEMD_ROOT / "ordivon-evaluation-project.timer").read_text(encoding="utf-8")
        backup = (SYSTEMD_ROOT / "ordivon-evaluation-backup.timer").read_text(encoding="utf-8")
        self.assertIn("OnUnitActiveSec=30min", projection)
        self.assertIn("OnCalendar=*-*-* 04:15:00", backup)
        self.assertIn("Persistent=true", projection)
        self.assertIn("Persistent=true", backup)


if __name__ == "__main__":
    unittest.main()
