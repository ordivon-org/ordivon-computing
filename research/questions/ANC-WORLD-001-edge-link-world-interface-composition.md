# ANC-WORLD-001 — Edge/Link World-Interface Composition


> **Completed composition question:** the repository and research objects were unified as `ordivon-world`; active research continues in [`ANC-WORLD-002`](ANC-WORLD-002-task-to-world-interaction-continuity.md) and Computing #78.
## Status

- Epistemic status: active cross-boundary research question
- GitHub issue: #68
- Parent program: Agent-Native Responsibility Overlay
- Research owners: `ordivon-computing`
- Implementation owners: `ordivon-edge`, `ordivon-link`, `ordivon-host`
- Related questions: `ANC-EDGE-001`, `ANC-LINK-001`, `ANC-IR-001`,
  `ANC-EFFECT-001`, `ANC-SECURITY-002`

## Question

What is the minimum composition between Task-to-execution placement and
Task-to-connectivity binding, and when should Edge and Link remain independent,
share a thin binding, or collapse into Host-local policy?

## Orthogonal axes

```text
Edge axis: where and through which external body does an Effect execute?
Link axis: which logical relationship, identity, and path realize communication?
```

A body may exist without special Link management. A logical relationship may
exist without an Edge body. One Edge body may use multiple paths; one Link path
may connect multiple bodies and services. Composition is therefore expected,
but merger is not assumed.

## Candidate composition

A future combined view may need only references:

```text
WorldBindingView
  Task / Attempt / Effect references
  Placement Binding reference
  Connectivity Binding references
  capability and consequence revision
  Artifact and Observation dependencies
  invalidation conditions
  residual closure state
```

This is not a proposed universal schema. It is a question about the minimum
cross-boundary relation needed by Host, Security, and evidence systems.

## Critical trajectories

1. Local execution with path replacement but no body replacement.
2. Body replacement with ordinary provider networking and no Link decision.
3. Local path failure causing a remote Edge placement.
4. One remote body using multiple logical relationships and paths.
5. Path or identity change invalidating evidence produced by an unchanged body.
6. Body generation replacement requiring reattachment but preserving Task and
   relation identity.
7. Parallel bodies contributing path-conditioned Artifacts to one Task join.
8. Destruction of bodies and paths with independent residual evidence.

## Research tasks

- derive ownership and cardinality from the trajectories rather than from
  repository names;
- compare an explicit cross-project Binding against Host-owned references;
- test whether one immutable binding digest is sufficient or whether independent
  placement and connectivity revisions are required;
- prevent Edge lifecycle authority from entering Link and prevent route/path
  authority from entering Edge;
- determine which changes invalidate execution results, connectivity evidence,
  both, or neither;
- measure whether Security is a genuine second consumer or merely an
  orchestration demonstration;
- decide repository boundaries only after real Host consumption.

## Merge and split criteria

Keep Edge and Link separate when their state, privilege, failure domain,
provider lifecycle, release cadence, and consumers remain materially different.
Consider a shared package only when a narrow reference contract has at least two
real consumers. Consider repository merger only when most real workloads always
require both, release and operations are synchronized, and separate ownership
creates measured duplication or recovery failure.

## Falsifiers

- no workload requires an explicit cross-boundary object beyond ordinary foreign
  references;
- Host-local composition is clearer and cheaper than a shared contract;
- one merged object obscures independent revision and invalidation semantics;
- Security remains the only consumer and provides no new operational need;
- the proposed relation duplicates existing Effect Binding or provenance
  structures without additional failure prevention.
