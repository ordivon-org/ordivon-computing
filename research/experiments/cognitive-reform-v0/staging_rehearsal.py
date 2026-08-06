#!/usr/bin/env python3
"""Run the A4 Host/Harness deployment rehearsal on staging-only state roots.

The script deliberately imports product packages only inside ``run_rehearsal`` so
its receipt and path guards remain testable without installing the release graph.
It never writes the production Host or Harness state roots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import time
import uuid
from typing import Any

PRODUCTION_ROOTS = (
    Path("/var/lib/ordivon/host"),
    Path("/var/lib/ordivon/harness"),
)
STAGING_PARENT = Path("/var/lib/ordivon/staging")
_REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
_DIGEST_A = "sha256:" + "a" * 64
_DIGEST_B = "sha256:" + "b" * 64
_DIGEST_C = "sha256:" + "c" * 64
_DIGEST_D = "sha256:" + "d" * 64


def _canonical_digest(value: dict[str, Any]) -> str:
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


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _validate_staging_root(path: Path) -> Path:
    resolved = path.expanduser().resolve(strict=False)
    staging_parent = STAGING_PARENT.resolve(strict=False)
    if not _inside(resolved, staging_parent) or resolved == staging_parent:
        raise ValueError(
            f"A4 staging root must be a child of {staging_parent}: {resolved}"
        )
    for production in PRODUCTION_ROOTS:
        production_resolved = production.resolve(strict=False)
        if (
            resolved == production_resolved
            or _inside(resolved, production_resolved)
            or _inside(production_resolved, resolved)
        ):
            raise ValueError("A4 staging root overlaps a production authority root")
    if path.exists() and path.is_symlink():
        raise ValueError("A4 staging root cannot be a symlink")
    return resolved


def _exact_revision(value: Any, label: str) -> str:
    if not isinstance(value, str) or _REVISION_RE.fullmatch(value) is None:
        raise ValueError(f"{label} must be an exact 40-character Git revision")
    return value


def _load_vector(path: Path) -> tuple[dict[str, Any], dict[str, str]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("kind") != "ordivon.system-version-vector":
        raise ValueError("A4 input is not an Ordivon System Version Vector")
    integrity = value.get("integrity")
    if not isinstance(integrity, dict) or integrity.get("payloadDigest") != _canonical_digest(
        value
    ):
        raise ValueError("A4 System Version Vector integrity differs")
    repositories = value.get("repositories")
    if not isinstance(repositories, dict):
        raise ValueError("A4 System Version Vector repositories are missing")
    revisions = {
        "computing": _exact_revision(
            repositories.get("computing", {}).get("revision"), "Computing revision"
        ),
        "host": _exact_revision(
            repositories.get("host", {}).get("revision"), "Host revision"
        ),
        "harness": _exact_revision(
            repositories.get("harness", {}).get("revision"), "Harness revision"
        ),
        "harnessImplementation": _exact_revision(
            repositories.get("harness", {}).get("verifiedImplementationRevision"),
            "Harness implementation revision",
        ),
        "runtime": _exact_revision(
            repositories.get("runtime", {}).get("revision"), "Runtime revision"
        ),
        "protocol": _exact_revision(
            repositories.get("protocol", {}).get("revision"), "Protocol revision"
        ),
    }
    if repositories["harness"].get("hostPin") != revisions["host"]:
        raise ValueError("A4 Harness Host pin differs from the selected Host revision")
    if repositories["harness"].get("protocolPin") != revisions["protocol"]:
        raise ValueError(
            "A4 Harness Protocol pin differs from the selected Protocol revision"
        )
    return value, revisions


def _mode(path: Path) -> str:
    return f"{stat.S_IMODE(path.stat().st_mode):04o}"


def _repository_revision() -> str:
    repository = Path(__file__).resolve().parents[3]
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        text=True,
        encoding="utf-8",
    ).strip()
    return _exact_revision(revision, "A4 rehearsal implementation revision")


def _run_contract(*, run_id: str, created_at_ms: int):
    from ordivon_harness.core_contracts import HarnessBoundReference, HarnessRunContract

    return HarnessRunContract(
        harness_run_id=run_id,
        harness_implementation_id="ordivon-harness@a4-staging",
        caller_id="caller:a4-staging",
        caller_run_ref=f"trial:a4:{run_id}",
        objective_ref=HarnessBoundReference(
            f"objective:a4:{run_id}", "objective", _DIGEST_A
        ),
        context_refs=(
            HarnessBoundReference(f"context:a4:{run_id}", "context", _DIGEST_B),
        ),
        provider_id="provider:a4-fixture",
        adapter_id="adapter:a4-fixture-v1",
        requested_model_id="model:a4-fixture",
        tool_catalog_digest=_DIGEST_C,
        tool_grant_digest=_DIGEST_D,
        budget={"maxModelCalls": 1, "maxToolCalls": 0},
        completion_contract={"mode": "a4-staging"},
        system_manifest_ref=HarnessBoundReference(
            f"system-manifest:a4:{run_id}", "system-manifest", _DIGEST_A
        ),
        created_at_ms=created_at_ms,
    )


def run_rehearsal(
    *,
    vector_path: Path,
    staging_root: Path,
    keep_state: bool,
) -> dict[str, Any]:
    from ordivon_host.ops import (
        create_backup as create_host_backup,
        doctor_state,
        restore_backup as restore_host_backup,
        verify_backup as verify_host_backup,
    )
    from ordivon_host.storage import HostStorage
    from ordivon_harness.cutover import (
        HarnessStoreMode,
        activate_cutover,
        assert_legacy_writer_allowed,
        build_cutover_inventory,
        cutover_status,
        rollback_cutover,
    )
    from ordivon_harness.sqlite_store import SQLiteHarnessStore
    from ordivon_harness.store_ops import (
        backup_harness_store,
        restore_harness_backup,
        verify_harness_backup,
    )

    vector, revisions = _load_vector(vector_path)
    root = _validate_staging_root(staging_root)
    if root.exists():
        raise FileExistsError(f"A4 staging root already exists: {root}")
    root.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if root.parent.is_symlink():
        raise ValueError("A4 staging parent cannot be a symlink")

    production_before = {str(path): path.exists() for path in PRODUCTION_ROOTS}
    started_at_ms = time.time_ns() // 1_000_000
    cleanup = {"requested": not keep_state, "completed": False}
    receipt: dict[str, Any] | None = None
    try:
        root.mkdir(mode=0o700)
        seed = root / "seed"
        seed_host = seed / "host"
        seed_harness = seed / "harness"
        with HostStorage(seed_host):
            pass
        with SQLiteHarnessStore.initialize(seed_harness):
            pass

        seed_host_doctor = doctor_state(seed_host, check_history=True)
        with SQLiteHarnessStore(seed_harness) as store:
            seed_harness_doctor = store.doctor(full=True)
        if seed_host_doctor.get("healthy") is not True:
            raise RuntimeError("A4 seed Host Doctor is unhealthy")
        if seed_harness_doctor.get("healthy") is not True:
            raise RuntimeError("A4 seed Harness Doctor is unhealthy")

        backups = root / "backups"
        host_backup = backups / "host"
        harness_backup = backups / "harness"
        host_backup_manifest = create_host_backup(
            seed_host, host_backup, created_at_ms=10_000
        )
        host_backup_verified = verify_host_backup(host_backup)
        harness_backup_report = backup_harness_store(
            seed_harness, harness_backup, created_at_ms=10_001
        )
        harness_backup_verified = verify_harness_backup(harness_backup)

        allowed = root / "scenarios" / "rollback-allowed"
        allowed_host = allowed / "host"
        allowed_harness = allowed / "harness"
        restore_host_backup(host_backup, allowed_host)
        restore_harness_backup(harness_backup, allowed_harness)
        allowed_inventory = build_cutover_inventory(
            allowed_host, allowed_harness, generated_at_ms=20_000
        )
        if not allowed_inventory.can_activate:
            raise RuntimeError(
                "A4 clean restored roots unexpectedly block activation: "
                + ", ".join(allowed_inventory.blockers)
            )
        allowed_activation, _ = activate_cutover(
            allowed_host, allowed_harness, created_at_ms=20_001
        )
        legacy_guarded = False
        try:
            assert_legacy_writer_allowed(allowed_host)
        except RuntimeError as error:
            legacy_guarded = "legacy Host-backed" in str(error)
        if not legacy_guarded:
            raise AssertionError("A4 activation did not disable the legacy writer")
        allowed_rollback, _ = rollback_cutover(
            allowed_host, allowed_harness, created_at_ms=20_002
        )
        allowed_status = cutover_status(allowed_host)
        if allowed_status.selected_mode is not HarnessStoreMode.LEGACY_HOST:
            raise AssertionError("A4 safe rollback did not restore legacy selection")
        assert_legacy_writer_allowed(allowed_host)

        fenced = root / "scenarios" / "rollback-fenced"
        fenced_host = fenced / "host"
        fenced_harness = fenced / "harness"
        restore_host_backup(host_backup, fenced_host)
        restore_harness_backup(harness_backup, fenced_harness)
        fenced_activation, fenced_inventory = activate_cutover(
            fenced_host, fenced_harness, created_at_ms=30_000
        )
        if not fenced_inventory.can_activate:
            raise AssertionError("A4 fenced scenario could not activate from clean roots")
        run_id = "harness-run:a4-post-activation"
        with SQLiteHarnessStore(fenced_harness) as store:
            store.create_run(_run_contract(run_id=run_id, created_at_ms=30_001))
        rollback_error: str | None = None
        try:
            rollback_cutover(fenced_host, fenced_harness, created_at_ms=30_002)
        except RuntimeError as error:
            rollback_error = str(error)
        if rollback_error is None or run_id not in rollback_error:
            raise AssertionError("A4 rollback did not fence post-activation work")
        fenced_status = cutover_status(fenced_host)
        if fenced_status.selected_mode is not HarnessStoreMode.INDEPENDENT:
            raise AssertionError("A4 failed rollback changed the selected mode")
        fenced_host_doctor = doctor_state(fenced_host, check_history=True)
        with SQLiteHarnessStore(fenced_harness) as store:
            fenced_harness_doctor = store.doctor(full=True)
        if fenced_host_doctor.get("healthy") is not True:
            raise RuntimeError("A4 fenced Host Doctor is unhealthy")
        if fenced_harness_doctor.get("healthy") is not True:
            raise RuntimeError("A4 fenced Harness Doctor is unhealthy")

        receipt = {
            "schemaVersion": 1,
            "kind": "ordivon.cognitive-reform-a4-staging-rehearsal",
            "vectorId": vector["vectorId"],
            "vectorPayloadDigest": vector["integrity"]["payloadDigest"],
            "rehearsalImplementationRevision": _repository_revision(),
            "status": "passed",
            "revisions": revisions,
            "staging": {
                "rootClass": "/var/lib/ordivon/staging/<ephemeral>",
                "rootMode": _mode(root),
                "productionActivated": False,
                "productionRootsObservedBefore": production_before,
            },
            "seed": {
                "hostDoctorHealthy": True,
                "harnessDoctorHealthy": True,
                "hostRootMode": _mode(seed_host),
                "harnessRootMode": _mode(seed_harness),
            },
            "backup": {
                "hostKind": host_backup_manifest["kind"],
                "hostCreatedAtMs": host_backup_manifest["createdAtMs"],
                "hostFiles": len(host_backup_verified["files"]),
                "harnessPayloadDigest": harness_backup_report["payloadDigest"],
                "harnessVerifiedPayloadDigest": harness_backup_verified[
                    "payloadDigest"
                ],
                "harnessRuns": harness_backup_report["runs"],
                "harnessEvents": harness_backup_report["events"],
            },
            "rollbackAllowed": {
                "initialCanActivate": True,
                "activationReceiptDigest": allowed_activation.digest,
                "legacyWriterRejectedWhileActive": legacy_guarded,
                "rollbackReceiptDigest": allowed_rollback.digest,
                "receiptChainLength": len(allowed_status.receipts),
                "finalMode": allowed_status.selected_mode.value,
            },
            "rollbackFenced": {
                "initialCanActivate": True,
                "activationReceiptDigest": fenced_activation.digest,
                "postActivationRunId": run_id,
                "rollbackRejected": True,
                "rollbackErrorClass": "post_activation_independent_work",
                "finalMode": fenced_status.selected_mode.value,
                "hostDoctorHealthy": True,
                "harnessDoctorHealthy": True,
            },
            "cleanup": cleanup,
            "startedAtMs": started_at_ms,
            "finishedAtMs": time.time_ns() // 1_000_000,
        }
    finally:
        if not keep_state and root.exists():
            shutil.rmtree(root)
            cleanup["completed"] = not root.exists()
        elif keep_state:
            cleanup["completed"] = False

    if receipt is None:
        raise AssertionError("A4 rehearsal ended without a receipt")
    production_after = {str(path): path.exists() for path in PRODUCTION_ROOTS}
    receipt["staging"]["productionRootsObservedAfter"] = production_after
    receipt["staging"]["productionRootsUnchanged"] = production_after == production_before
    receipt["cleanup"] = cleanup
    receipt["finishedAtMs"] = time.time_ns() // 1_000_000
    if not receipt["staging"]["productionRootsUnchanged"]:
        raise AssertionError("A4 rehearsal observed a production-root state change")
    if cleanup["requested"] and not cleanup["completed"]:
        raise AssertionError("A4 staging cleanup did not complete")
    receipt["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evidence-json-v1",
        "payloadDigest": _canonical_digest(receipt),
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--vector",
        type=Path,
        default=Path(__file__).with_name("system-version-vector-v1.json"),
    )
    parser.add_argument("--staging-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--keep-state", action="store_true")
    args = parser.parse_args()

    root = args.staging_root or (
        STAGING_PARENT / f"cognitive-reform-a4-{uuid.uuid4().hex}"
    )
    receipt = run_rehearsal(
        vector_path=args.vector.resolve(),
        staging_root=root,
        keep_state=args.keep_state,
    )
    encoded = json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
        os.chmod(args.output, 0o600)
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
