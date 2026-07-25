# Semantic Core v0

An executable reference model for the first Agent-native semantic layer:

```text
Reality and Evidence
→ Identity and Causality
→ Outcome Algebra
→ Effect Semantics
```

The reference kernel uses only the Python standard library at runtime. It is intentionally independent of Linux process state, model providers, conversation history, and concrete Tool transports. Ordivon integration lives in a separate adapter and does not define the core semantics.

## Run

Reference tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Live local Ordivon slice:

```bash
set -a
source /etc/ordivon/ordivon-mcp.env
set +a
PYTHONPATH=src python scripts/live_ordivon_exec.py \
  --source-revision <exact-commit>
```

The live script never prints the Bearer token and always attempts to close its temporary Workspace.

## Implemented semantic objects

- typed `SemanticId` identities;
- versioned `WorldObjectRef` targets;
- immutable `EffectSpec` intent;
- independent `DispatchRecord` boundary attempts;
- ordered `EffectEvent` causality;
- immutable `Observation` and `Artifact` evidence;
- `Claim → Verification → Fact` admission;
- optimistic revisions and invariant scanning.

## Critical rules

- an Effect is not a Tool call;
- beginning a Dispatch does not prove acceptance or completion;
- response loss becomes `unknown`, never implicit failure;
- `unknown` must reconcile and cannot blindly redispatch;
- terminal outcomes are immutable;
- accepted Verification must satisfy the Effect's declared evidence plan;
- independent evidence may cross Effects only when it targets the same WorldObject and version and predates Verification;
- a Fact cannot predate or bypass its accepted Verification.

## Current maturity

- **M0 semantic reference kernel:** implemented and covered by reusable conformance scenarios;
- **M1 Ordivon adapter:** asynchronous execution, versioned read, atomic mutation, Artifact projection, and Fact admission passed through the public MCP contract;
- **live proof:** command execution remained single-dispatch; mutation results were independently re-read by separate Effects; two file Facts were admitted; stale-digest mutation was rejected without changing final content;
- **remaining M1 work:** injected response loss, cancellation races, adapter restart continuity, and Tool-contract drift;
- **durability:** semantic journal remains in-memory;
- **wire format:** intentionally deferred until more backend semantics agree.

See [`SPEC.md`](SPEC.md), [`LIVE-REPORT.md`](LIVE-REPORT.md), [`DECISIONS.md`](DECISIONS.md), and [`ROADMAP.md`](ROADMAP.md).
