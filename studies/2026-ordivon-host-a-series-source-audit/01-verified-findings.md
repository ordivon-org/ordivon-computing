# 01 — Verified Findings

All findings below were reproduced against Host revision `efb2850472e15651412a7dc569beb26e8f4aace8` without changing the repository.

## H-AUD-001 — Lease ownership is not part of event admission

**Severity:** P0

`HostKernel.locked_task()` acquires a lease, but `LockedTask.commit()` admits the event using Task revision CAS only. The active lease token is not checked in the same SQLite transaction.

Reproduced trajectory:

```text
owner A acquires lease revision 1 with TTL 1
→ lease expires
→ owner B acquires lease revision 2
→ owner A commits Task revision 2 successfully
→ owner A exits context
→ release of lease revision 1 raises LeaseConflict
```

Durable state advanced even though the caller received failure.

**A-Series conflict:** A5, A9, A15.

**Required invariant:** event admission must atomically prove the submitting owner still holds the exact live lease generation, or leases must be removed as an authority claim.

## H-AUD-002 — Dynamic EventKind extensions are not fail-closed

**Severity:** P0

`EventKind._missing_()` mutates the global Enum value map at runtime.

Reproduced properties:

- `task.creatd` is accepted as an extension;
- `effect.dispatch-preparedd` is accepted as an extension;
- `cognition.context-compiledd` is accepted as an extension;
- 64 threads constructing one new value produced two distinct objects and names in ten rounds.

This permits core namespace typos and makes identity comparisons unstable under concurrency.

**A-Series conflict:** A1, A5, A10.

**Required invariant:** core event namespaces fail closed; extension values are immutable validated values and do not mutate an Enum class.

## H-AUD-003 — Failed generic Effects can be completed successfully

**Severity:** P0

`EffectLifecycleHost._record_observation()` places failed/rejected delivery in BLOCKED. `complete()` then accepts READY or BLOCKED and maps caller-provided `TaskOutcome.status` directly to terminal state.

Reproduced trajectory:

```text
Observation status = failed
→ Task = BLOCKED at result frontier
→ caller supplies TaskOutcome(status=completed, verificationDigest=null)
→ Host persists COMPLETED
```

No accepted verification is required.

**A-Series conflict:** A2, A9, A10.

**Required invariant:** Host derives allowable outcome from retained Observation and Verification; caller text cannot override failure evidence.

## H-AUD-004 — Code-change verification has a Workspace TOCTOU gap

**Severity:** P0

`CodeChangeHost.verify()` reads planned files and structured diff before taking the Task lease. It later commits verification after checking Task plan and Job identity, but it has no Workspace revision or snapshot token.

Reproduced trajectory:

```text
Host reads correct files
→ Runtime returns correct structured diff
→ Runtime changes src/example.py to VALUE = 999 before return completes
→ Host commits VERIFICATION_ACCEPTED
→ close commits COMPLETED
```

**A-Series conflict:** A5, A10, A15.

**Required invariant:** evidence must bind a stable Workspace generation or commit-time revalidation token. Holding a long lease is not an adequate substitute.

## H-AUD-005 — Terminal Task state is reversible

**Severity:** P0

`GoalCoordinatorHost.transition_task()` accepts an arbitrary next state. A COMPLETED Task can be transitioned back to READY with a new frontier under the same Task identity.

**A-Series conflict:** A4, A5, A9.

**Required invariant:** terminal states are irreversible. Revised work receives a new Attempt or Task identity with explicit provenance.

## H-AUD-006 — Rejected joint verification can advance a Task

**Severity:** P0

`GoalCoordinatorHost.apply_verification_result()` ignores `VerificationReceipt.accepted`. It uses only the selected result item's status.

Reproduced input:

```text
VerificationReceipt.accepted = false
result item for Task = succeeded
```

Result: Task transitions to READY.

**A-Series conflict:** A2, A10.

**Required invariant:** overall receipt acceptance and item semantics must be mutually consistent before any Task transition.

## H-AUD-007 — Causal provenance accepts dangling event identities

**Severity:** P1

`caused_by_event_id` has no foreign key, admission check or History Doctor validation.

A Task event caused by `event:does-not-exist` was persisted and passed full history validation.

**A-Series conflict:** A10, A14.

**Decision:** enforce existence and ordering, or delete the field. Fake provenance is worse than absent provenance.

## H-AUD-008 — Host state is world-readable under ordinary umask

**Severity:** P1

Observed new-state modes:

```text
state root      0755
objects/        0755
host.sqlite3    0644
CAS object      0644
```

Host CAS may contain Context, Observation, proposal, evidence and private repository content. `read_token_file()` also checks size and syntax but not file mode.

**A-Series conflict:** A7, A8, A16.

**Required invariant:** explicit trusted-local single-user mode or enforced private state/token permissions.

## H-AUD-009 — Generic Effect lifecycle has not passed the second-consumer gate

**Severity:** P1 architecture debt

`EffectLifecycleHost` is 645 lines. No repository under `/root/projects/*` imports it outside Host tests. read, mutation and code-change maintain separate lifecycle implementations with substantial repeated mechanics.

Its unified recovery integration is also incomplete: an `effect.outcome-unknown` Game-style workload is reported as `unsupported` by `assess_recovery()` even though `EffectLifecycleHost.reconcile()` can process it.

**A-Series conflict:** A11, A13.

**Decision gate:** either migrate two materially different real consumers and delete duplicated mechanics, or return the generic lifecycle to an experimental study and remove it from the Host public surface.

## H-AUD-010 — Durable surfaces overstate current ownership

**Severity:** P2 cleanup

Production usage is zero for:

- `TaskState.PROPOSED`;
- `EventKind.WAKEUP_SCHEDULED`;
- `StreamKind.GOAL`.

`RUNNING` is referenced only by projection/Kernel validation; no workload transitions into it. `owner_of()` is consumed only by tests. Host owns Goal IDs and Goal-scoped Task aggregation, but no Goal stream or durable Goal commitment object.

`DispatchEnvelope.expectedObservationKind` is persisted, while `ObservationEnvelope` has no corresponding kind field and Host never checks it.

**A-Series conflict:** A3, A11, A13, A14.

**Decision:** narrow claims and delete dead surfaces unless a concrete consumer and protected failure are identified.
