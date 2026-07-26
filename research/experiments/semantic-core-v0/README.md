> **Track status:** Kernel v0 construction closed at K1–K12 after the minimal external Binding edge. This directory is a frozen reference experiment, not the destination for Effect IR, ToolContract, Binding compiler, Host, Task Runtime, or VM work. Only bug fixes, regression evidence, and newly demonstrated universal Kernel invariants belong here.

# Semantic Core v0

An executable Agent-native semantic layer built on mature classical runtime and storage mechanisms.

```text
Probabilistic cognition
→ signed Effect proposal
→ stable Effect / Dispatch semantics
→ Ordivon or another execution backend
→ Observation / Artifact evidence
→ Verification
→ Fact admission
→ authenticated Journal replay
```

The semantic model is independent of model providers, conversation history, and concrete Tool transports. The reference implementation uses Python 3.12 and standard-library SQLite. P2E runs one semantic conformance suite through Ordivon and a structurally distinct deterministic backend, proving that either backend remains an Adapter concern rather than Kernel semantics.

## Run

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
PYTHONPATH=src python3.12 -m compileall -q src tests scripts
ruff check src tests scripts
```

Canonical real-system Binding evidence is owned by the adjacent external-contract experiment:

```bash
cd ../external-semantic-contract-v0
set -a
source /etc/ordivon/ordivon-mcp.env
set +a
PYTHONPATH=src:../semantic-core-v0/src:../semantic-core-v0/scripts:. \
  python3.12 scripts/live_bound_ordivon_restart.py \
  --source-revision <exact-commit>
```

Live scripts never print the Bearer token and close temporary Workspaces.

## Implemented semantic objects

- typed `SemanticId` identities;
- versioned `WorldObjectRef` targets;
- immutable `KernelEffectProjection` intent;
- independent `DispatchRecord` attempts with STARTED / ADMITTED / UNKNOWN / REJECTED state;
- ordered `EffectEvent` causality;
- immutable `Observation` and `Artifact` evidence;
- `Claim → Verification → Fact` admission;
- optimistic revisions, command-local rollback, and explicit full invariant audit;
- single-command and multi-command semantic atomicity;
- append-only Journal schema v4, v2/v3 migration, and deterministic genesis replay;
- signed role-scoped Authority grants and content-bound Attestations;
- scoped Effect, execution, Verification, Fact, and read-only Kernel Views.

## Source architecture

```text
interfaces.py   public role-scoped read and mutation protocols
authorized.py   signed Authority-backed implementation of those protocols
reducer.py      raw in-memory executable reference reducer
journal.py      raw durable JournalReducer and SQLite command history
provenance.py   read-only execution, recovery, authority, and Fact projections
backend_conformance.py  internal two-backend semantic oracle
simulator.py    internal deterministic second-backend experiment
kernel.py       backward-compatible import facade
```

Adapters depend on `ExecutionView`; Verification and Fact admission depend on separate role protocols. Raw reducers, the deterministic backend, and the portability driver remain below Authority issuance and are not exported from the package root.

## External Binding edge

The Kernel does not parse public Effect IR or Tool schemas. It accepts only a signed `BindingAdmission`, preserves immutable Binding revision history, and records the exact Binding identity/digest on a bound Dispatch. Contract normalization, argument encoding, rebind planning, and Backend lowering live in the separate [`external-semantic-contract-v0`](../external-semantic-contract-v0/) experiment.

## Backend portability evidence

```bash
PYTHONPATH=src python3.12 -m unittest \
  tests.test_backend_portability -v
```

The same versioned I/O, asynchronous execution, uncertainty, reconciliation, cancellation, evidence, Fact, and Authority scenarios produce an identical normalized report for Ordivon and the deterministic second backend. The simulator uses different operation names, status words, IDs, and receipts; no simulator or Ordivon implementation object enters Kernel state.

Exact P2E evidence is retained in [`portability-results/backend-portability-f83764b.json`](portability-results/backend-portability-f83764b.json).

## Performance evidence

```bash
PYTHONPATH=src python3.12 benchmarks/benchmark_semantic_core.py \
  --profile standard \
  --source-revision "$(git rev-parse HEAD)" \
  --output benchmark-results/<revision>.json
```

The harness measures growth on one environment, not cross-machine rankings. Baseline and optimized exact-revision results are stored under `benchmark-results/`.

Exact benchmark values are retained only in immutable receipts indexed by [`EVIDENCE.md`](EVIDENCE.md).

## Kernel responsibility

The Kernel preserves semantic identity, legal transitions, explicit uncertainty, evidence provenance, role-scoped authority, and recoverable history across external action. It is not a model orchestrator, Task scheduler, memory platform, sandbox, or replacement operating system.

## Documentation map

- [`KERNEL-CHARTER.md`](KERNEL-CHARTER.md) — mission, classical foundation, and K1–K12;
- [`SPEC.md`](SPEC.md) — primitive separation, state algebra, evidence graph, and invariants;
- [`AUTHORITY.md`](AUTHORITY.md) — role grants, signers, Attestations, and scoped Views;
- [`JOURNAL.md`](JOURNAL.md) — atomic persistence, integrity, writer conflict, and replay;
- [`ADAPTERS.md`](ADAPTERS.md) — asynchronous execution and versioned I/O boundaries;
- [`FAILURE-MODEL.md`](FAILURE-MODEL.md) — failure classes and required responses;
- [`CONFORMANCE.md`](CONFORMANCE.md) — canonical guarantee-to-test mapping;
- [`EVIDENCE.md`](EVIDENCE.md) — immutable receipt index;
- [`DECISIONS.md`](DECISIONS.md) — retained architecture decisions.

Changing task state and readiness live in GitHub Issues. Construction history lives in Git commits and `DECISIONS.md`; it is not duplicated in a local roadmap or status file.
