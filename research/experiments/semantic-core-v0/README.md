# Semantic Core v0

An executable Agent-native semantic layer built on mature classical runtime and storage mechanisms:

```text
Reality and Evidence
→ Identity and Causality
→ Outcome Algebra
→ Effect Semantics
→ Atomic Semantic Transactions
→ Durable Journal and Replay
```

The semantic model is independent of model providers, conversation history, and concrete Tool transports. The reference implementation uses Python 3.12.13 and standard-library SQLite. Ordivon integration remains in adapters and does not define the core semantics.

## Run

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
PYTHONPATH=src python3.12 -m compileall -q src tests scripts
ruff check src tests scripts
```

Live durable recovery:

```bash
set -a
source /etc/ordivon/ordivon-mcp.env
set +a
PYTHONPATH=src python3.12 scripts/live_ordivon_journal_restart.py   --source-revision <exact-commit>
```

Live scripts never print the Bearer token and close temporary Workspaces.

## Implemented semantic objects

- typed `SemanticId` identities;
- versioned `WorldObjectRef` targets;
- immutable `EffectSpec` intent;
- independent `DispatchRecord` attempts with STARTED / ADMITTED / UNKNOWN / REJECTED state;
- ordered `EffectEvent` causality;
- immutable `Observation` and `Artifact` evidence;
- `Claim → Verification → Fact` admission;
- optimistic revisions and invariant scanning;
- single-command and multi-command semantic atomicity;
- append-only `JournalKernel` persistence and deterministic replay.

## Critical rules

- an Effect is not a Tool call;
- beginning a Dispatch does not prove backend admission or completion;
- response loss becomes `UNKNOWN`, never implicit failure;
- `UNKNOWN` reconciles and cannot blindly redispatch;
- Adapter projection is all-or-nothing;
- terminal outcomes are immutable;
- accepted Verification must satisfy the Effect's declared evidence plan;
- independent evidence may cross Effects only for the same WorldObject/version and valid time order;
- a Fact cannot predate or bypass accepted Verification;
- journal corruption and stale writers fail closed.

## Current maturity

- **M0:** semantic constitution v0 complete;
- **M1:** Ordivon Adapter and failure semantics v0 complete;
- **M1.5:** Kernel atomicity closure complete;
- **M2:** local durable semantic journal v0 complete;
- **verification:** 53 tests, bytecode compilation, ruff, and real process-restart recovery pass;
- **next:** M3 external Effect IR;
- **not claimed:** replication, distributed consensus, compaction, public schema compatibility, or production readiness.

The internal journal codec is intentionally not the public Effect IR.

See [`SPEC.md`](SPEC.md), [`JOURNAL.md`](JOURNAL.md), [`DECISIONS.md`](DECISIONS.md), [`TEST-REPORT.md`](TEST-REPORT.md), and [`ROADMAP.md`](ROADMAP.md).
