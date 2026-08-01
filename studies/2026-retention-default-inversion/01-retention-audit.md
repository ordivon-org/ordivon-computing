# Retention audit

## 1. The minimum question

A retention audit asks:

> What current value is lost if this structure leaves the active system now?

It does not begin with “what could go wrong if we delete it?” because any sufficiently imaginative future can defend any structure. The relevant comparison is the current system, current consumers, current consequence, and current recovery cost.

## 2. Retention evidence

A structure earns active retention only when the answer is concrete enough to support judgment across these dimensions:

| Dimension | Required evidence |
|---|---|
| Current consumer | A real product path, workload, participant, external contract, or active experiment—not hypothetical future use |
| Purchased capability | The behavior, continuity, verification, coordination, expression, or consequence control that would be lost |
| Protected failure | A realistic trajectory, its severity, and why ordinary recovery or local repair is insufficient |
| Narrowest sufficient form | Why a smaller local mechanism, generated artifact, temporary adapter, or archive cannot provide the same value |
| Recurring net value | Benefit after latency, CI time, cognitive load, compatibility cost, maintenance, Context pollution, and suppressed alternatives |
| Review horizon | The consumer, condition, or evidence change that causes the structure to re-enter audit |

Historical investment, test count, documentation volume, implementation maturity, repository appearance, and generalized industry custom are context. They do not satisfy the audit by themselves.

## 3. Dispositions

### Retain

Keep the structure in the active path when current value is clear, the responsibility is owned, a narrower form is insufficient, and recurring net benefit remains positive.

Examples include an authoritative World reducer, exact Command identity under response loss, stale-revision admission, resource conservation, or an externally consumed contract with current dependents.

### Localize

Keep the capability but narrow its scope, frequency, or ownership.

Examples:

- a global coverage gate becomes a local semantic test for a high-consequence reducer;
- a universal approval plane becomes one domain-specific consequence admission rule;
- a schema version remains only on persisted or cross-process objects;
- a full release verification leaves the pull-request path and runs only at release.

### Archive

Remove the structure from active execution and default Context while preserving historical evidence or a reconstructable reference.

Examples include milestone plans, historical evaluation JSON, superseded designs, old benchmark scripts, and prior compatibility implementations that no current path consumes.

### Delete

Remove the current implementation when it has no current consumer or independent capability, duplicates another owner, costs more than it protects, or remains recoverable through Git and reconstruction.

## 4. Uncertainty

Under the old default, uncertainty supported retention. Under the new default:

```text
cannot demonstrate current active value
→ remove from the active path
→ archive when historical learning is worth preserving
→ restore only after a real consumer or failure appears
```

This is rational because active retention has recurring cost while Git-backed removal is usually reversible.

## 5. Audit sequence

```text
enumerate active structures touched by the decision
→ place each in the removal candidate set
→ identify current consumers and consequence owners
→ reproduce the capability or failure that may rescue it
→ compare the narrowest alternatives
→ count recurring cost, including attention and change propagation
→ retain, localize, archive, or delete
→ record only the judgment needed for later reconstruction
```

The process begins with the negative set. It does not construct a ceremonial “keep list” around every repository object.

## 6. Proportional evidence

The audit itself must not become another governance system.

- A small local helper may need one sentence in a code review.
- A CI gate may need one reproduced failure and a timing comparison.
- A public protocol may need consumer evidence, migration analysis, and compatibility planning.
- A legal or participant-rights record follows its domain authority rather than this engineering heuristic.

No mandatory retention object, approval committee, universal YAML schema, expiration daemon, or audit service is implied. Judgment and evidence scale with consequence.

## 7. Review horizon, not permanent legitimacy

Passing one audit grants a current disposition, not permanent status. Re-audit is triggered when:

- the last consumer disappears;
- a replacement becomes active;
- reconstruction becomes cheaper;
- a second workload contradicts the abstraction;
- a gate accumulates false blocks or material delay;
- a compatibility path survives only through its own tests;
- the protected failure becomes recoverable through a narrower mechanism;
- participant purpose changes.

At that point retention must be proved again.
