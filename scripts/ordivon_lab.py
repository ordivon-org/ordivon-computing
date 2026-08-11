#!/usr/bin/env python3
"""Thin Agent-facing scientific instruments for Ordivon RSI experiments.

This module owns no product truth, research priority, semantic score, or action
authority.  It only performs deterministic evidence packing, matrix mechanics,
analytical materialization, and revision-delta packing so an Agent can spend
its context on scientific judgment instead of repetitive plumbing.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import signal
import string
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent
OBSERVATION_SRC = ROOT / "packages" / "ordivon-observation-core" / "src"
for path in (SCRIPTS_DIR, OBSERVATION_SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import ordivon_observation_core as observation  # noqa: E402
from frontier_freshness import classify_revision_relation  # noqa: E402

Json = dict[str, Any]
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SAFE_NAME_RE = re.compile(r"[^a-zA-Z0-9_.-]+")


class LabError(RuntimeError):
    pass


def now_ms() -> int:
    return time.time_ns() // 1_000_000


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def payload_digest(value: dict[str, Any]) -> str:
    payload = dict(value)
    payload.pop("integrity", None)
    return "sha256:" + hashlib.sha256(canonical_bytes(payload)).hexdigest()


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_name(value: str) -> str:
    rendered = SAFE_NAME_RE.sub("-", value).strip("-._")
    return rendered or "value"


def _require_digest(value: str, label: str) -> str:
    if not DIGEST_RE.fullmatch(value):
        raise LabError(f"{label} must be a canonical sha256 digest")
    return value


# ---------------------------------------------------------------------------
# P0: EvidencePack


def build_evidence_pack(
    *,
    pack_id: str,
    bundle_paths: Iterable[Path],
    max_events: int = 1024,
    created_at_ms: int | None = None,
) -> dict[str, Any]:
    if not pack_id or pack_id != pack_id.strip():
        raise LabError("pack_id must be non-empty and trimmed")
    paths = tuple(Path(path) for path in bundle_paths)
    if not paths:
        raise LabError("at least one Observation Export Bundle is required")
    if not 1 <= max_events <= 100_000:
        raise LabError("max_events must be between 1 and 100000")

    sources: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    identities: set[str] = set()
    for path in paths:
        raw = load_json(path)
        bundle = observation.ObservationExportBundle.from_dict(raw)
        event_count = sum(len(batch.events) for batch in bundle.batches)
        producer = bundle.producer_identity
        sources.append(
            {
                "path": str(path),
                "fileDigest": file_digest(path),
                "bundleDigest": bundle.integrity_digest,
                "projectId": producer.project_id,
                "componentId": producer.component_id,
                "instanceId": producer.instance_id,
                "mappingVersion": bundle.mapping_version,
                "ownerRevision": bundle.owner_revision,
                "exporterRevision": bundle.exporter_revision,
                "exportedAtMs": bundle.exported_at_ms,
                "eventCount": event_count,
            }
        )
        for batch in bundle.batches:
            for event in batch.events:
                if event.event_id in identities:
                    raise LabError(f"duplicate event identity across bundles: {event.event_id}")
                identities.add(event.event_id)
                events.append(event.to_dict())
    if len(events) > max_events:
        raise LabError(
            f"EvidencePack has {len(events)} events, above explicit max_events={max_events}; "
            "select a narrower owner export instead of silently truncating"
        )

    events.sort(
        key=lambda item: (
            int(item["occurredAtMs"]),
            str(item["source"]["projectId"]),
            str(item["source"]["streamId"]),
            int(item["source"]["sequence"]),
            str(item["eventId"]),
        )
    )
    sources.sort(key=lambda item: (item["projectId"], item["componentId"], item["instanceId"], item["path"]))
    measurements = sum(len(event.get("measurements", {})) for event in events)
    pack: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.lab.evidence-pack",
        "packId": pack_id,
        "createdAtMs": now_ms() if created_at_ms is None else created_at_ms,
        "sourceBundles": sources,
        "events": events,
        "summary": {
            "sourceBundleCount": len(sources),
            "ownerProjectCount": len({item["projectId"] for item in sources}),
            "eventCount": len(events),
            "measurementCount": measurements,
            "completeForSuppliedBundles": True,
            "truncated": False,
        },
        "inferenceBoundary": {
            "ownerTruthCopied": False,
            "trialValidityInferred": False,
            "semanticCompletionInferred": False,
            "researchPriorityInferred": False,
            "role": "bounded metadata evidence frozen for Agent analysis",
        },
    }
    pack["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evidence-json-v1",
        "payloadDigest": payload_digest(pack),
    }
    return pack


def command_evidence_pack(args: argparse.Namespace) -> int:
    result = build_evidence_pack(
        pack_id=args.pack_id,
        bundle_paths=args.bundle,
        max_events=args.max_events,
    )
    write_json(args.output, result)
    print(f"{args.output}: {result['summary']['eventCount']} events {result['integrity']['payloadDigest']}")
    return 0


# ---------------------------------------------------------------------------
# P1: Experiment Matrix Executor


def _validate_scalar(value: Any, label: str) -> None:
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
            raise LabError(f"{label} contains non-finite float")
        return
    raise LabError(f"{label} must be a JSON scalar")


def _load_matrix_spec(path: Path) -> dict[str, Any]:
    spec = load_json(path)
    if not isinstance(spec, dict):
        raise LabError("matrix spec root must be an object")
    if spec.get("schemaVersion") != 1 or spec.get("kind") != "ordivon.lab.experiment-matrix-spec":
        raise LabError("unsupported matrix spec")
    experiment_id = spec.get("experimentId")
    if not isinstance(experiment_id, str) or not experiment_id.strip():
        raise LabError("matrix experimentId is required")
    factors = spec.get("factors", {})
    if not isinstance(factors, dict):
        raise LabError("matrix factors must be an object")
    for name, values in factors.items():
        if not isinstance(name, str) or not name or SAFE_NAME_RE.search(name):
            raise LabError(f"invalid factor name: {name!r}")
        if not isinstance(values, list) or not values:
            raise LabError(f"factor {name} must contain at least one value")
        for index, value in enumerate(values):
            _validate_scalar(value, f"factor {name}[{index}]")
    replicates = spec.get("replicates", 1)
    if type(replicates) is not int or not 1 <= replicates <= 10_000:
        raise LabError("replicates must be an integer between 1 and 10000")
    command = spec.get("command")
    if not isinstance(command, dict):
        raise LabError("matrix command is required")
    executable = command.get("executable")
    if not isinstance(executable, str) or not Path(executable).is_absolute():
        raise LabError("matrix command.executable must be an absolute path")
    args = command.get("args", [])
    if not isinstance(args, list) or any(not isinstance(item, str) for item in args):
        raise LabError("matrix command.args must be a string array")
    env = command.get("env", {})
    if not isinstance(env, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in env.items()):
        raise LabError("matrix command.env must be a string map")
    cwd = command.get("cwd", ".")
    if not isinstance(cwd, str) or Path(cwd).is_absolute():
        raise LabError("matrix command.cwd must be relative to the spec directory")
    for key, low, high, default in (
        ("timeoutMs", 1, 86_400_000, 120_000),
        ("maxWorkers", 1, 64, 1),
        ("stdoutLimitBytes", 0, 4_194_304, 65_536),
        ("stderrLimitBytes", 0, 4_194_304, 65_536),
    ):
        value = spec.get(key, default)
        if type(value) is not int or not low <= value <= high:
            raise LabError(f"{key} must be an integer between {low} and {high}")
    return spec


def _trial_templates(spec: dict[str, Any]) -> list[dict[str, Any]]:
    names = sorted(spec.get("factors", {}))
    values = [spec["factors"][name] for name in names]
    combinations = itertools.product(*values) if names else [()]
    result: list[dict[str, Any]] = []
    index = 0
    for combination in combinations:
        factors = dict(zip(names, combination, strict=True))
        for replicate in range(1, spec.get("replicates", 1) + 1):
            index += 1
            identity = {
                "experimentId": spec["experimentId"],
                "factors": factors,
                "replicate": replicate,
            }
            suffix = hashlib.sha256(canonical_bytes(identity)).hexdigest()[:12]
            result.append(
                {
                    "trialIndex": index,
                    "trialId": f"trial-{index:04d}-r{replicate:03d}-{suffix}",
                    "factors": factors,
                    "replicate": replicate,
                }
            )
    return result


def _template_context(trial: dict[str, Any]) -> dict[str, str]:
    context = {
        "trialId": str(trial["trialId"]),
        "replicate": str(trial["replicate"]),
        "trialIndex": str(trial["trialIndex"]),
    }
    for key, value in trial["factors"].items():
        context[key] = "" if value is None else str(value)
    return context


def _render_template(value: str, context: dict[str, str]) -> str:
    try:
        fields = [field for _, field, _, _ in string.Formatter().parse(value) if field]
        missing = [field for field in fields if field not in context]
        if missing:
            raise LabError("unknown matrix template field(s): " + ", ".join(sorted(set(missing))))
        return value.format_map(context)
    except ValueError as error:
        raise LabError(f"invalid matrix template {value!r}: {error}") from error


def _tail_and_digest(path: Path, limit: int) -> tuple[str, int, str, bool]:
    size = path.stat().st_size if path.exists() else 0
    digest = file_digest(path) if path.exists() else "sha256:" + hashlib.sha256(b"").hexdigest()
    if limit == 0 or size == 0:
        return "", size, digest, size > 0
    with path.open("rb") as handle:
        if size > limit:
            handle.seek(size - limit)
        data = handle.read()
    return data.decode("utf-8", errors="replace"), size, digest, size > limit


def _run_one_trial(
    *,
    spec_path: Path,
    spec: dict[str, Any],
    spec_digest: str,
    trial: dict[str, Any],
    trials_dir: Path,
) -> tuple[dict[str, Any], bool]:
    record_path = trials_dir / f"{trial['trialId']}.json"
    if record_path.exists():
        existing = load_json(record_path)
        if existing.get("specDigest") != spec_digest or existing.get("trial") != trial:
            raise LabError(f"existing trial record conflicts with current spec: {record_path}")
        if existing.get("terminal") is True:
            return existing, True

    command = spec["command"]
    context = _template_context(trial)
    executable = Path(command["executable"])
    if not executable.is_file():
        raise LabError(f"trial executable is absent: {executable}")
    args = [_render_template(value, context) for value in command.get("args", [])]
    cwd = (spec_path.parent / command.get("cwd", ".")).resolve()
    if not cwd.is_dir():
        raise LabError(f"trial cwd is absent: {cwd}")
    environment = os.environ.copy()
    for key, value in command.get("env", {}).items():
        environment[key] = _render_template(value, context)
    environment["ORDIVON_TRIAL_ID"] = trial["trialId"]
    environment["ORDIVON_REPLICATE"] = str(trial["replicate"])
    environment["ORDIVON_TRIAL_INDEX"] = str(trial["trialIndex"])
    environment["ORDIVON_FACTORS_JSON"] = json.dumps(trial["factors"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    for name, value in trial["factors"].items():
        environment["ORDIVON_FACTOR_" + re.sub(r"[^A-Za-z0-9]", "_", name).upper()] = "" if value is None else str(value)

    started = now_ms()
    timed_out = False
    launch_error: str | None = None
    exit_code: int | None = None
    with tempfile.TemporaryDirectory(prefix="ordivon-lab-trial-") as temp:
        stdout_path = Path(temp) / "stdout"
        stderr_path = Path(temp) / "stderr"
        try:
            with stdout_path.open("wb") as stdout_handle, stderr_path.open("wb") as stderr_handle:
                process = subprocess.Popen(
                    [str(executable), *args],
                    cwd=cwd,
                    env=environment,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    start_new_session=True,
                )
                try:
                    exit_code = process.wait(timeout=spec.get("timeoutMs", 120_000) / 1000)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    os.killpg(process.pid, signal.SIGKILL)
                    exit_code = process.wait(timeout=10)
        except (OSError, subprocess.SubprocessError) as error:
            launch_error = f"{type(error).__name__}: {error}"
        ended = now_ms()
        stdout_tail, stdout_bytes, stdout_digest, stdout_truncated = _tail_and_digest(stdout_path, spec.get("stdoutLimitBytes", 65_536))
        stderr_tail, stderr_bytes, stderr_digest, stderr_truncated = _tail_and_digest(stderr_path, spec.get("stderrLimitBytes", 65_536))

    record: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.lab.matrix-trial-record",
        "experimentId": spec["experimentId"],
        "specDigest": spec_digest,
        "trial": trial,
        "execution": {
            "executable": str(executable),
            "args": args,
            "cwd": str(cwd),
            "startedAtMs": started,
            "endedAtMs": ended,
            "elapsedMs": max(0, ended - started),
            "exitCode": exit_code,
            "timedOut": timed_out,
            "launchError": launch_error,
            "mechanicalSuccess": launch_error is None and not timed_out and exit_code == 0,
            "semanticCompletionEvaluated": False,
        },
        "stdout": {
            "byteLength": stdout_bytes,
            "digest": stdout_digest,
            "tail": stdout_tail,
            "truncated": stdout_truncated,
        },
        "stderr": {
            "byteLength": stderr_bytes,
            "digest": stderr_digest,
            "tail": stderr_tail,
            "truncated": stderr_truncated,
        },
        "terminal": True,
    }
    record["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evidence-json-v1",
        "payloadDigest": payload_digest(record),
    }
    write_json(record_path, record)
    return record, False


def run_matrix(*, spec_path: Path, output_dir: Path) -> dict[str, Any]:
    spec_path = spec_path.resolve()
    spec = _load_matrix_spec(spec_path)
    spec_digest = payload_digest(spec)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "matrix-manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        if manifest.get("specDigest") != spec_digest:
            raise LabError("matrix output directory belongs to another spec digest")
    else:
        manifest = {
            "schemaVersion": 1,
            "kind": "ordivon.lab.matrix-manifest",
            "experimentId": spec["experimentId"],
            "specPath": str(spec_path),
            "specDigest": spec_digest,
            "createdAtMs": now_ms(),
            "scientificJudgmentOwnedByRunner": False,
            "effectRecoveryOwnedByMatrix": False,
            "crashGapBoundary": "a trial process may have produced an external effect before its terminal trial record exists; effectful commands require owner-native durable identity and reconciliation outside the Matrix Executor",
        }
        manifest["integrity"] = {"algorithm": "sha256", "canonicalization": "ordivon-evidence-json-v1", "payloadDigest": payload_digest(manifest)}
        write_json(manifest_path, manifest)

    trials = _trial_templates(spec)
    trials_dir = output_dir / "trials"
    trials_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    resumed = 0
    workers = spec.get("maxWorkers", 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(
                _run_one_trial,
                spec_path=spec_path,
                spec=spec,
                spec_digest=spec_digest,
                trial=trial,
                trials_dir=trials_dir,
            )
            for trial in trials
        ]
        for future in concurrent.futures.as_completed(futures):
            record, replayed = future.result()
            records.append(record)
            resumed += int(replayed)
    records.sort(key=lambda item: int(item["trial"]["trialIndex"]))
    successes = sum(bool(item["execution"]["mechanicalSuccess"]) for item in records)
    timeouts = sum(bool(item["execution"]["timedOut"]) for item in records)
    launch_errors = sum(item["execution"]["launchError"] is not None for item in records)
    receipt: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.lab.matrix-receipt",
        "experimentId": spec["experimentId"],
        "specDigest": spec_digest,
        "trialCount": len(records),
        "resumedTerminalTrials": resumed,
        "newlyExecutedTrials": len(records) - resumed,
        "mechanicalSuccesses": successes,
        "mechanicalNonSuccesses": len(records) - successes,
        "timeouts": timeouts,
        "launchErrors": launch_errors,
        "trialRecordDigests": [item["integrity"]["payloadDigest"] for item in records],
        "semanticCompletionEvaluated": False,
        "scientificOutcomeInferred": False,
        "effectRecoveryOwnedByMatrix": False,
        "terminalReplayBoundary": "only already-recorded terminal trial identities are skipped on rerun; interrupted effectful trials require owner-native reconciliation before any retry",
        "completedAtMs": now_ms(),
    }
    receipt["integrity"] = {"algorithm": "sha256", "canonicalization": "ordivon-evidence-json-v1", "payloadDigest": payload_digest(receipt)}
    write_json(output_dir / "matrix-receipt.json", receipt)
    return receipt


def command_matrix(args: argparse.Namespace) -> int:
    receipt = run_matrix(spec_path=args.spec, output_dir=args.output_dir)
    print(
        f"{args.output_dir}: {receipt['trialCount']} trials, "
        f"{receipt['mechanicalSuccesses']} mechanically successful, "
        f"{receipt['resumedTerminalTrials']} replayed {receipt['integrity']['payloadDigest']}"
    )
    return 0


# ---------------------------------------------------------------------------
# P2: DuckDB / Parquet analysis projection


def _duckdb_version(executable: Path) -> str:
    result = subprocess.run([str(executable), "--version"], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _sql_literal(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def _run_duckdb(executable: Path, sql: str, *, json_output: bool = False) -> str:
    command = [str(executable)]
    if json_output:
        command.append("-json")
    command += [":memory:", "-c", sql]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise LabError(f"DuckDB failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def _factor_column(name: str) -> str:
    return "factor_" + re.sub(r"[^A-Za-z0-9_]", "_", name).lower()


def materialize_matrix_analysis(*, run_dir: Path, output_dir: Path, duckdb: Path) -> dict[str, Any]:
    receipt = load_json(run_dir / "matrix-receipt.json")
    if receipt.get("kind") != "ordivon.lab.matrix-receipt":
        raise LabError("run_dir has no valid matrix receipt")
    records = [load_json(path) for path in sorted((run_dir / "trials").glob("*.json"))]
    if len(records) != receipt["trialCount"]:
        raise LabError("matrix trial record count differs from receipt")
    factor_names = sorted({name for record in records for name in record["trial"]["factors"]})
    rows = []
    for record in records:
        row: dict[str, Any] = {
            "experiment_id": record["experimentId"],
            "trial_id": record["trial"]["trialId"],
            "trial_index": record["trial"]["trialIndex"],
            "replicate": record["trial"]["replicate"],
            "mechanical_success": record["execution"]["mechanicalSuccess"],
            "exit_code": record["execution"]["exitCode"],
            "timed_out": record["execution"]["timedOut"],
            "launch_error": record["execution"]["launchError"],
            "elapsed_ms": record["execution"]["elapsedMs"],
            "stdout_bytes": record["stdout"]["byteLength"],
            "stderr_bytes": record["stderr"]["byteLength"],
            "stdout_digest": record["stdout"]["digest"],
            "stderr_digest": record["stderr"]["digest"],
            "trial_record_digest": record["integrity"]["payloadDigest"],
            "factors_json": json.dumps(record["trial"]["factors"], ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        }
        for name in factor_names:
            row[_factor_column(name)] = record["trial"]["factors"].get(name)
        rows.append(row)
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl = output_dir / "trials.jsonl"
    with jsonl.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    parquet = output_dir / "trials.parquet"
    _run_duckdb(
        duckdb,
        f"COPY (SELECT * FROM read_json_auto({_sql_literal(jsonl)}, format='newline_delimited')) TO {_sql_literal(parquet)} (FORMAT PARQUET, COMPRESSION ZSTD);",
    )
    summary_sql = (
        f"SELECT count(*) AS trial_count, sum(CASE WHEN mechanical_success THEN 1 ELSE 0 END) AS mechanical_successes, "
        f"sum(CASE WHEN timed_out THEN 1 ELSE 0 END) AS timeouts, round(avg(elapsed_ms),3) AS mean_elapsed_ms, "
        f"sum(stdout_bytes) AS stdout_bytes, sum(stderr_bytes) AS stderr_bytes FROM read_parquet({_sql_literal(parquet)});"
    )
    summary_text = _run_duckdb(duckdb, summary_sql, json_output=True)
    summary_rows = json.loads(summary_text or "[]")
    manifest: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.lab.analysis-manifest",
        "analysisKind": "matrix",
        "sourceReceiptDigest": receipt["integrity"]["payloadDigest"],
        "duckdbVersion": _duckdb_version(duckdb),
        "rows": len(rows),
        "factorColumns": {name: _factor_column(name) for name in factor_names},
        "files": {
            "jsonl": {"path": str(jsonl), "digest": file_digest(jsonl)},
            "parquet": {"path": str(parquet), "digest": file_digest(parquet)},
        },
        "summary": summary_rows[0] if summary_rows else {},
        "authorityBoundary": "derived analytical projection; trial records remain evidence and no scientific outcome is inferred",
    }
    manifest["integrity"] = {"algorithm": "sha256", "canonicalization": "ordivon-evidence-json-v1", "payloadDigest": payload_digest(manifest)}
    write_json(output_dir / "analysis-manifest.json", manifest)
    return manifest


def materialize_evidence_analysis(*, pack_path: Path, output_dir: Path, duckdb: Path) -> dict[str, Any]:
    pack = load_json(pack_path)
    if pack.get("kind") != "ordivon.lab.evidence-pack":
        raise LabError("pack_path is not an EvidencePack")
    if pack.get("integrity", {}).get("payloadDigest") != payload_digest(pack):
        raise LabError("EvidencePack integrity differs")
    rows = []
    for event in pack["events"]:
        source = event["source"]
        payload_ref = event.get("payloadRef") or {}
        rows.append(
            {
                "event_id": event["eventId"],
                "occurred_at_ms": event["occurredAtMs"],
                "project_id": source["projectId"],
                "component_id": source["componentId"],
                "instance_id": source["instanceId"],
                "stream_id": source["streamId"],
                "sequence": source["sequence"],
                "native_kind": source["nativeKind"],
                "native_id": source["nativeId"],
                "native_revision": source.get("nativeRevision"),
                "native_digest": source["nativeDigest"],
                "mapping_version": source["mappingVersion"],
                "relations_json": json.dumps(event.get("relations", []), ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                "attributes_json": json.dumps(event.get("attributes", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                "measurements_json": json.dumps(event.get("measurements", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                "outcome_json": json.dumps(event.get("outcome"), ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                "privacy_class": event["privacy"]["class"],
                "payload_owner": payload_ref.get("owner"),
                "payload_kind": payload_ref.get("kind"),
                "payload_native_id": payload_ref.get("nativeId"),
                "payload_digest": payload_ref.get("digest"),
                "event_digest": event["integrity"]["payloadDigest"],
            }
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl = output_dir / "events.jsonl"
    with jsonl.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    parquet = output_dir / "events.parquet"
    _run_duckdb(duckdb, f"COPY (SELECT * FROM read_json_auto({_sql_literal(jsonl)}, format='newline_delimited')) TO {_sql_literal(parquet)} (FORMAT PARQUET, COMPRESSION ZSTD);")
    summary_rows = json.loads(
        _run_duckdb(
            duckdb,
            f"SELECT count(*) AS event_count, count(DISTINCT project_id) AS project_count, min(occurred_at_ms) AS first_ms, max(occurred_at_ms) AS last_ms FROM read_parquet({_sql_literal(parquet)});",
            json_output=True,
        )
        or "[]"
    )
    manifest: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.lab.analysis-manifest",
        "analysisKind": "evidence-pack",
        "sourcePackDigest": pack["integrity"]["payloadDigest"],
        "duckdbVersion": _duckdb_version(duckdb),
        "rows": len(rows),
        "files": {
            "jsonl": {"path": str(jsonl), "digest": file_digest(jsonl)},
            "parquet": {"path": str(parquet), "digest": file_digest(parquet)},
        },
        "summary": summary_rows[0] if summary_rows else {},
        "authorityBoundary": "derived analytical projection; owner-native evidence remains authoritative",
    }
    manifest["integrity"] = {"algorithm": "sha256", "canonicalization": "ordivon-evidence-json-v1", "payloadDigest": payload_digest(manifest)}
    write_json(output_dir / "analysis-manifest.json", manifest)
    return manifest


def command_analyze_matrix(args: argparse.Namespace) -> int:
    result = materialize_matrix_analysis(run_dir=args.run_dir, output_dir=args.output_dir, duckdb=args.duckdb)
    print(f"{args.output_dir}: {result['rows']} rows -> {result['files']['parquet']['path']} {result['integrity']['payloadDigest']}")
    return 0


def command_analyze_evidence(args: argparse.Namespace) -> int:
    result = materialize_evidence_analysis(pack_path=args.pack, output_dir=args.output_dir, duckdb=args.duckdb)
    print(f"{args.output_dir}: {result['rows']} rows -> {result['files']['parquet']['path']} {result['integrity']['payloadDigest']}")
    return 0


def command_query(args: argparse.Namespace) -> int:
    if "{table}" not in args.sql:
        raise LabError("query SQL must contain literal {table} placeholder")
    sql = args.sql.replace("{table}", f"read_parquet({_sql_literal(args.parquet.resolve())})")
    sys.stdout.write(_run_duckdb(args.duckdb, sql, json_output=args.json))
    return 0


# ---------------------------------------------------------------------------
# P3: PressurePack


def _git(repository: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["/usr/bin/git", "-C", str(repository), *args],
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise LabError(f"git {' '.join(args)} failed for {repository}: {result.stderr.strip()}")
    return result.stdout.strip()


def _git_commit_exists(repository: Path, revision: str) -> bool:
    result = subprocess.run(
        ["/usr/bin/git", "-C", str(repository), "cat-file", "-e", f"{revision}^{{commit}}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def _changed_paths(repository: Path, observed: str, current: str, limit: int) -> tuple[list[dict[str, str]], int, bool]:
    if observed == current:
        return [], 0, False
    output = _git(repository, "diff", "--name-status", "--no-renames", observed, current)
    rows = []
    for line in output.splitlines():
        if not line:
            continue
        status, _, path = line.partition("\t")
        rows.append({"status": status, "path": path})
    rows.sort(key=lambda item: (item["path"], item["status"]))
    return rows[:limit], len(rows), len(rows) > limit


def _commit_sample(repository: Path, observed: str, current: str, limit: int) -> tuple[list[dict[str, str]], bool]:
    if observed == current:
        return [], False
    output = _git(repository, "log", "--format=%H%x09%s", f"{observed}..{current}", f"--max-count={limit + 1}")
    rows = []
    for line in output.splitlines():
        revision, _, subject = line.partition("\t")
        if revision:
            rows.append({"revision": revision, "subject": subject})
    return rows[:limit], len(rows) > limit


def build_pressure_pack(
    *,
    frontier_path: Path,
    project_root: Path,
    include_projects: set[str] | None = None,
    changed_path_limit: int = 200,
    commit_limit: int = 20,
    created_at_ms: int | None = None,
) -> dict[str, Any]:
    frontier = load_json(frontier_path)
    if frontier.get("kind") != "ordivon.world-model-assimilation-frontier":
        raise LabError("frontier_path is not the world-model assimilation frontier")
    rows = []
    for item in sorted(frontier["projects"], key=lambda value: value["projectId"]):
        project_id = item["projectId"]
        if include_projects is not None and project_id not in include_projects:
            continue
        repository = project_root / project_id
        if not repository.is_dir():
            rows.append(
                {
                    "projectId": project_id,
                    "observedRevision": item["observedRevision"],
                    "repositoryAvailable": False,
                    "relation": "observed_unavailable",
                    "unknown": ["local repository is unavailable"],
                }
            )
            continue
        observed = item["observedRevision"]
        current = _git(repository, "rev-parse", "HEAD")
        if not _git_commit_exists(repository, observed):
            rows.append(
                {
                    "projectId": project_id,
                    "observedRevision": observed,
                    "currentRevision": current,
                    "repositoryAvailable": True,
                    "relation": "observed_unavailable",
                    "unknown": ["observed revision is not reachable in local Git history"],
                }
            )
            continue
        relation = classify_revision_relation(repository, observed, current)
        changed, changed_total, changed_truncated = _changed_paths(repository, observed, current, changed_path_limit)
        commits, commits_truncated = _commit_sample(repository, observed, current, commit_limit)
        rows.append(
            {
                "projectId": project_id,
                "observedRevision": observed,
                "currentRevision": current,
                "repositoryAvailable": True,
                "relation": relation.state,
                "commitsAhead": relation.commits_ahead,
                "commitsBehind": relation.commits_behind,
                "revisionMoved": observed != current,
                "changedPaths": changed,
                "changedPathCount": changed_total,
                "changedPathsTruncated": changed_truncated,
                "commitSample": commits,
                "commitSampleTruncated": commits_truncated,
                "unknown": [],
            }
        )
    pack: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.lab.pressure-pack",
        "createdAtMs": now_ms() if created_at_ms is None else created_at_ms,
        "frontier": {
            "path": str(frontier_path),
            "fileDigest": file_digest(frontier_path),
            "payloadDigest": frontier.get("integrity", {}).get("payloadDigest"),
        },
        "projects": rows,
        "summary": {
            "projectCount": len(rows),
            "revisionMovedCount": sum(bool(item.get("revisionMoved")) for item in rows),
            "unavailableCount": sum(not bool(item.get("repositoryAvailable")) or item.get("relation") == "observed_unavailable" for item in rows),
        },
        "inferenceBoundary": {
            "worldModelChangeInferred": False,
            "importanceScoreProduced": False,
            "tractabilityScoreProduced": False,
            "topologyClassProduced": False,
            "recommendedActionProduced": False,
            "role": "mechanical owner-revision delta packet for Agent review",
        },
    }
    pack["integrity"] = {"algorithm": "sha256", "canonicalization": "ordivon-evidence-json-v1", "payloadDigest": payload_digest(pack)}
    return pack


def command_pressure(args: argparse.Namespace) -> int:
    include = set(args.project) if args.project else None
    result = build_pressure_pack(
        frontier_path=args.frontier,
        project_root=args.project_root,
        include_projects=include,
        changed_path_limit=args.changed_path_limit,
        commit_limit=args.commit_limit,
    )
    write_json(args.output, result)
    print(
        f"{args.output}: {result['summary']['projectCount']} projects, "
        f"{result['summary']['revisionMovedCount']} moved, "
        f"{result['summary']['unavailableCount']} unavailable {result['integrity']['payloadDigest']}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Thin non-authoritative RSI laboratory instruments for Ordivon Agents"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pack = sub.add_parser("evidence-pack", help="validate owner export bundles and freeze one bounded EvidencePack")
    pack.add_argument("--pack-id", required=True)
    pack.add_argument("--bundle", type=Path, action="append", required=True)
    pack.add_argument("--max-events", type=int, default=1024)
    pack.add_argument("--output", type=Path, required=True)
    pack.set_defaults(handler=command_evidence_pack)

    matrix = sub.add_parser("matrix", help="run or resume a frozen mechanical experiment matrix")
    matrix.add_argument("--spec", type=Path, required=True)
    matrix.add_argument("--output-dir", type=Path, required=True)
    matrix.set_defaults(handler=command_matrix)

    analyze_matrix = sub.add_parser("analyze-matrix", help="materialize matrix trial records as JSONL + Parquet")
    analyze_matrix.add_argument("--run-dir", type=Path, required=True)
    analyze_matrix.add_argument("--output-dir", type=Path, required=True)
    analyze_matrix.add_argument("--duckdb", type=Path, default=Path("/usr/bin/duckdb"))
    analyze_matrix.set_defaults(handler=command_analyze_matrix)

    analyze_evidence = sub.add_parser("analyze-evidence", help="materialize EvidencePack events as JSONL + Parquet")
    analyze_evidence.add_argument("--pack", type=Path, required=True)
    analyze_evidence.add_argument("--output-dir", type=Path, required=True)
    analyze_evidence.add_argument("--duckdb", type=Path, default=Path("/usr/bin/duckdb"))
    analyze_evidence.set_defaults(handler=command_analyze_evidence)

    query = sub.add_parser("query", help="run one DuckDB SQL query against a Parquet projection")
    query.add_argument("--parquet", type=Path, required=True)
    query.add_argument("--sql", required=True, help="SQL containing {table} where the Parquet relation belongs")
    query.add_argument("--json", action="store_true")
    query.add_argument("--duckdb", type=Path, default=Path("/usr/bin/duckdb"))
    query.set_defaults(handler=command_query)

    pressure = sub.add_parser("pressure-pack", help="freeze bounded owner Git deltas without prioritizing them")
    pressure.add_argument("--frontier", type=Path, default=ROOT / "research" / "world-model-frontier.json")
    pressure.add_argument("--project-root", type=Path, default=Path("/root/projects"))
    pressure.add_argument("--project", action="append", default=[])
    pressure.add_argument("--changed-path-limit", type=int, default=200)
    pressure.add_argument("--commit-limit", type=int, default=20)
    pressure.add_argument("--output", type=Path, required=True)
    pressure.set_defaults(handler=command_pressure)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.handler(args))
    except LabError as error:
        print(f"ordivon-lab: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
