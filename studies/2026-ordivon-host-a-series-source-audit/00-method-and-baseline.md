# 00 — Method and Baseline

## Scope

The audit inspected the complete post-Harness-extraction Host package rather than reviewing only public APIs or architecture documents.

Primary layers:

```text
Task/Event domain
→ immutable CAS + SQLite Journal
→ HostStorage + HostKernel
→ Context / cognition admission
→ Effect / Runtime dispatch lifecycles
→ read / mutation / code-change workloads
→ Goal coordination / recovery / operations
```

## A-Series method

Each A0–A16 foundation was translated into four source questions:

1. Which component owns the responsibility?
2. Which code path enforces it?
3. Which adversarial trajectory falsifies it?
4. What is the deletion condition if no real consumer exists?

A passing existing test was treated as evidence only for the exact property checked, consistent with A15.

## Static baseline

- Python source: 13,510 lines.
- Deterministic tests: 154.
- Test files: 28.
- Largest workload modules:
  - `engine/code_change/host.py`: 952 lines;
  - `engine/mutation/host.py`: 750 lines;
  - `effects/lifecycle.py`: 645 lines;
  - `engine/read_task.py`: 609 lines;
  - `cognition/turn.py`: 585 lines.
- Ruff: passed.
- compileall: passed.
- Three complete test runs: 154/154 each.
- Runtime: 21.7–22.5 seconds per run.
- Peak child-process RSS: approximately 39 MiB.

No third-party coverage, property-testing or type-checking package was installed for the audit. A standard-library trace pass was used only to identify unexercised regions, not as a quality score.

## Coverage interpretation

The trace pass showed that central function bodies were only partially exercised:

- Journal: roughly 63%;
- Storage: roughly 61%;
- Kernel: roughly 51%;
- generic Effect lifecycle: roughly 57%;
- deterministic read: roughly 53%;
- mutation: roughly 65%;
- code change: roughly 67%;
- recovery: roughly 49%.

The aggregate statement figure was 46.9%, but this undercounts import and class-definition execution because test discovery occurred before tracing. The useful conclusion is narrower: recovery, failed completion, concurrency and malformed-history branches were materially under-tested. The reproduced failures came from those gaps.

## Structural baseline

The CAS/Journal substrate preserves several strong properties:

- canonical object bytes and SHA-256 addressing;
- fsync of new object file and parent directory;
- SQLite WAL with `synchronous=FULL`;
- event revision CAS;
- immutable event payload containing the resulting Task projection;
- startup validation of admitted object metadata and current Task heads;
- conservative UNKNOWN handling in mutation and code-change delivery.

The audit does not recommend replacing SQLite, CAS, revision CAS, explicit Dispatch identity or the Host/Harness/Runtime ownership split.
