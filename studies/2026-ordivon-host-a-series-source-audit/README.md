# Ordivon Host A-Series Source Audit

> **Historical audit:** findings are scoped to the revisions below. They do not describe current Host state unless confirmed in the owning repository; the remediation plan is not a current Computing roadmap.

This study applies Ordivon Computer foundations A0–A16 to the post-Harness-extraction `ordivon-host` source tree.

## Audited revisions

- Ordivon Host: `efb2850472e15651412a7dc569beb26e8f4aace8`
- Ordivon Computer: `be5fe779267f0225dd37c570932c7d71ee5223a7`
- Audit date: 2026-08-01

The Host repository remained read-only during this audit. Findings were reproduced with isolated temporary state roots and adversarial in-memory Runtime/Executor fixtures.

## Route

1. [Method and baseline](00-method-and-baseline.md)
2. [Verified findings](01-verified-findings.md)
3. [A0–A16 assessment](02-a-series-assessment.md)
4. [Remediation and deletion gates](03-remediation-plan.md)
5. [Machine-readable evidence ledger](evidence-ledger.json)

## Current conclusion

The post-extraction macro-boundary is materially better: Host no longer imports Harness and the SQLite/CAS/revision-CAS substrate is generally sound. The current implementation is not yet an optimal or fully trustworthy authority plane.

The audit reproduced six correctness failures in durable admission or concurrency semantics:

- an expired lease holder can commit after another owner acquires the lease;
- extension EventKind construction is namespace-permissive and concurrently identity-unstable;
- a failed generic Effect can be completed successfully without verification;
- code-change verification can commit against a Workspace changed after evidence collection;
- a terminal Task can be reopened under the same identity;
- a rejected joint Verification can still advance a Task through a succeeded result item.

Additional architecture debt includes dangling causal provenance, insecure default state permissions, a generic Effect lifecycle with no external consumer or unified recovery integration, and durable surfaces with no production consumer.

The next action should be a narrow P0 correctness series, not another architecture expansion.
