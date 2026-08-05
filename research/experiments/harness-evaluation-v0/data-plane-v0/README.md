# Local Evaluation Data Plane v0

Status: accepted Phase 1 design. Implementation must preserve the authority and comparison boundaries established by Harness Evaluation v0.

## Decision

Build one single-host, operator-owned evaluation data plane from mature local tools instead of extending the P0 JSON scripts into a bespoke experiment platform.

The data plane consists of:

1. a deterministic Ordivon evaluation projection into Parquet and DuckDB;
2. an idempotent downstream mirror into a loopback-only MLflow Tracking Server;
3. verified restic snapshots of the analytical state and MLflow state;
4. repository-owned installation, validation, projection, backup, and restore-check commands.

Every component is replaceable and rebuildable. None becomes an authority for Task completion, Harness Run state, Runtime physical truth, comparison eligibility, or evidence integrity.

## Why this exists

P0 established a strict evaluation control plane, but routine use still requires hand-written JSON traversal, aggregation, experiment browsing, and backup operations. Phase 1 removes that operational friction without creating a second execution plane or weakening P0 claims.

The implementation should make these common questions cheap:

- Which Tasks, Trials, Results, and Failures exist?
- Which configuration, model, Provider, Harness, verifier, and System Manifest produced a Trial?
- Which Trials are accepted, rejected, not adjudicated, or blocked from comparison?
- What are the latency, token, cost, Tool-call, intervention, recovery, and failure distributions?
- Which evidence and Artifacts support one result?
- Has the analytical state been backed up and can a snapshot be restored and validated?

## Authority boundary

| Fact | Authority | Data-plane treatment |
| --- | --- | --- |
| Task and semantic outcome | Host or domain verifier | Read-only reference |
| Harness Run, Provider Call, Tool Step, Snapshot, and trajectory | Harness | Read-only reference or bounded projection |
| Workspace, Job, Attempt, process result, Artifact, and physical uncertainty | Runtime | Read-only reference; Artifact bytes are not copied by default |
| Evaluation Task, Trial, Result, Failure, Suite, System Manifest, and comparison policy | Computing Harness Evaluation v0 | Validated source records |
| Parquet tables and DuckDB database | Local data plane | Rebuildable analytical projection |
| MLflow experiments, Runs, tags, metrics, and mirrored Artifacts | Local data plane | Rebuildable browsing and feedback projection |
| restic snapshots | Operator backup system | Recovery copy, never live authority |

A downstream tool may display or aggregate an Ordivon decision, but it may not make that decision. In particular, an MLflow Run marked successful does not complete a Host Task, prove a Runtime Effect, or make a Trial comparison-eligible.

## Data flow

```text
committed P0 records and curated evaluation evidence
    |
    | validate schemas, integrity, references, and P0 policy
    v
atomic projection staging directory
    |-- Parquet tables
    |-- projection manifest with source and table digests
    `-- DuckDB analytical database
            |
            | idempotent mirror keyed by Ordivon Trial identity
            v
        MLflow experiment and Run UI

verified analytical and MLflow snapshots
    |
    v
restic repository
```

The projection is one-way. Editing DuckDB, Parquet, or MLflow never writes back to committed evaluation evidence.

## Repository layout

Phase 1 implementation remains inside this directory:

```text
data-plane-v0/
  README.md
  pyproject.toml
  uv.lock
  src/ordivon_eval_data/
  tests/
  scripts/
  packaging/systemd/
```

The package exposes bounded commands for projection, MLflow mirroring, validation, installation, backup, and restore verification. Generated state never enters Git.

## Installed layout

The initial trusted-local deployment uses:

```text
/opt/ordivon/evaluation-data-plane/
  venv/
  current/                 installed package and operational scripts

/var/lib/ordivon/analytics/
  evaluation/
    current/               atomic current projection
      parquet/
      evaluation.duckdb
      projection-manifest.json
    generations/           retained completed projections
  mlflow/
    mlflow.db
    artifacts/
  backup-staging/          verified temporary backup inputs

/root/.config/ordivon/secrets/
  restic-evaluation-data-plane

/root/backups/ordivon-evaluation-data-plane-restic/
  restic repository
```

Directories containing state or credentials use owner-only permissions. MLflow binds only to `127.0.0.1` and is not remotely exposed by this phase.

## Analytical contract

The first projection contains normalized tables for:

- `tasks`;
- `trials`;
- `results`;
- `failures`;
- `result_metrics`;
- `result_artifacts`;
- `verifier_assertions`;
- `trial_source_evidence`;
- `system_manifests`;
- `suite_tasks`;
- `projection_records`.

Each table retains stable Ordivon identities and the source record path and payload digest. Nested values that are not required for routine relational analysis remain available as canonical JSON columns rather than being discarded.

Parquet is the durable analytical interchange format. DuckDB is a disposable index over the exact projected Parquet generation. Re-running the projector over identical source bytes must produce the same logical rows and manifest digests.

## MLflow mapping

Use one MLflow experiment for this evaluation domain and one MLflow Run per Ordivon Trial.

The mirror uses stable tags including:

- `ordivon.trial_id`;
- `ordivon.task_id` and `ordivon.task_version`;
- `ordivon.execution_path`;
- `ordivon.provider_id` and `ordivon.model_id`;
- `ordivon.harness_id` and `ordivon.harness_revision`;
- `ordivon.system_manifest_ref`;
- `ordivon.verifier_id` and `ordivon.verifier_revision`;
- `ordivon.acceptance_status`;
- `ordivon.comparison_eligible` when a deterministic summary establishes it;
- source record and payload digests.

Numeric Result metrics are mirrored as MLflow metrics. Canonical Task, Trial, Result, Failure, and bounded projection metadata are mirrored as small Artifacts. Runtime Artifact bytes, raw Provider traffic, reasoning text, secrets, and arbitrary source trees are excluded by default.

Mirroring is idempotent: an existing Run with the same Trial identity is updated only when its source digest set matches the expected Ordivon record set. A conflicting identity fails closed rather than silently overwriting history.

## Backup contract

The backup path must not copy a live SQLite database as an ordinary file and claim a valid snapshot.

A backup run performs:

1. online SQLite backup of `mlflow.db` into a fresh staging generation;
2. completed-copy capture of the current evaluation projection;
3. manifest and SQLite integrity checks;
4. restic snapshot of the verified staging generation;
5. restic repository check using a bounded policy;
6. deletion of temporary staging bytes only after the snapshot succeeds.

The restic password is generated locally, stored outside Git with mode `0600`, and never printed. The initial repository is local so the system works without cloud credentials. The repository can later move or replicate to S3-compatible storage without changing Ordivon record semantics.

## Installation and service boundary

The installation command creates a dedicated virtual environment under `/opt`, installs the exact locked package, creates the owner-only state directories, and installs repository-owned systemd units.

Phase 1 services are:

- `ordivon-mlflow.service`: loopback-only Tracking Server;
- `ordivon-evaluation-project.service`: one-shot deterministic projection and MLflow mirror;
- `ordivon-evaluation-project.timer`: periodic projection;
- `ordivon-evaluation-backup.service`: one-shot verified restic snapshot;
- `ordivon-evaluation-backup.timer`: periodic backup.

Projection and backup services must be safe to rerun. They may fail without changing Host, Harness, or Runtime state.

## Migration path

No Phase 1 storage choice is terminal:

- MLflow SQLite can migrate to PostgreSQL;
- local MLflow Artifacts can migrate to S3-compatible storage;
- Parquet generations remain portable;
- DuckDB can be rebuilt or replaced by another analytical engine;
- restic can use local, SFTP, REST, or object-storage repositories;
- OpenTelemetry, Prometheus, Grafana, DVC, Phoenix, or a remote data warehouse can consume later projections without changing the authority model.

Migration is driven by observed operational need, not anticipated enterprise scale.

## Security and privacy

Phase 1 assumes the existing trusted-local, single-operator authority profile.

It therefore requires:

- loopback-only MLflow binding;
- owner-only state and secret permissions;
- no automatic remote upload;
- no raw Runtime database, Host CAS, Provider secret, bearer token, private prompt, reasoning text, or arbitrary Artifact ingestion;
- explicit allowlisting of mirrored fields and small evidence records;
- retention of source paths and identifiers only where needed for local provenance;
- backups treated as sensitive operator-owned data.

A future remote or multi-user deployment requires an explicit authentication, redaction, tenancy, deletion, and hosted-service privacy contract.

## Acceptance criteria

Phase 1 is accepted only when all of the following hold:

1. the repository package is locked and its tests pass;
2. existing Harness Evaluation v0 validation passes before projection;
3. the projector produces normalized Parquet tables, a DuckDB database, and a digest-bound manifest atomically;
4. the projected P0 dogfood count remains 7 Tasks, 10 Trials, 10 Results, and 6 Failures;
5. a repeated projection over unchanged source records is logically and digest stable;
6. DuckDB integrity and required relational references pass;
7. MLflow starts on loopback, reports healthy, and receives exactly one idempotent Run per projected Trial;
8. rerunning the mirror does not create duplicate Trial Runs;
9. no raw Runtime Artifact bytes or secrets enter MLflow by default;
10. restic creates a verified snapshot from an online SQLite backup and a completed analytical projection;
11. a temporary restore of the latest snapshot passes SQLite and projection validation;
12. the complete Computing conformance gate passes on the exact implementation revision.

## Non-goals

Phase 1 does not add:

- a Repeated Trial Runner or Provider dispatch service;
- a new Task, Harness, Runtime, or Effect authority;
- OpenTelemetry instrumentation;
- Prometheus, Grafana, Loki, or Tempo;
- DVC or a production replay corpus;
- an online A/B testing or traffic-allocation system;
- a model registry or automatic model promotion;
- a global cross-task score;
- automatic deletion, redaction, tenancy, or remote exposure;
- replacement of committed P0 JSON records with MLflow or DuckDB state.

Those capabilities require separate evidence after Phase 1 proves that the local data plane removes real operational friction.
