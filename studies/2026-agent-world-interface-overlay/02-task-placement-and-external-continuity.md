# 02 — Task Placement and External Continuity

## Open-work placement

A Placement Requirement should describe what one current Attempt or Effect
needs, not which vendor product to call. Candidate dimensions include:

- interaction capability: Fetch, browser, shell, GPU, device, background work;
- data inputs and export requirements;
- locality, region, latency, and availability;
- credential and trust domain;
- writable or read-only state;
- lifetime and asynchronous callback requirements;
- reversibility and consequence boundary;
- evidence, Artifact, and reconstruction requirements;
- resource and cost class.

Every field must be justified by at least two workloads.

## Placement Binding

A Binding should preserve the exact relation:

```text
Task / Attempt / Effect / Dispatch
→ requirement revision
→ provider capability observation
→ selected provider and body generation
→ provider execution identity
→ policy and capability revision
→ Receipt and Artifact provenance
```

The semantic Kernel need not store the complete provider schema. A digest-bound
external Binding may be sufficient.

## Continuation without physical cloning

Cross-body continuation should prefer minimum sufficient semantic state:

- source and dependency digests;
- selected Task frontier;
- unresolved Effects and unknown outcomes;
- verified Artifacts and observations;
- generated code and lockfiles;
- environment requirement, not hidden environment state;
- next admissible work.

Whole-machine snapshots remain useful provider mechanisms, but they are not the
definition of Task continuity.

## Persistent presence hypothesis

A durable Agent presence may be required for callbacks, long-lived sessions,
devices, or accountable asynchronous roles. It must not be assumed. Research
must test whether Task identity, participant role, service identity, and
provider object already suffice.
