# 04 — Failure, Invalidation, and Rebinding

## Failure trajectories

1. Request delivered and provider committed, response lost.
2. Path changes while the same provider operation continues.
3. Provider changes and returns a new endpoint, identity and callback channel.
4. Endpoint or credential rotates while accepted work remains pending.
5. Artifact bytes reach remote storage but Receipt persistence fails.
6. Callback reaches an old Host generation.
7. Provider A sends directly to B, while local state remains uncertain.
8. Parallel interactions finish under different path/provider conditions.
9. Body/session is destroyed while external writes or queued callbacks remain.
10. Participant is replaced without explicit responsibility handoff.

## Invalidation

A change should invalidate only dependent state:

- path change may invalidate locality or reproducibility Claims;
- provider build change may invalidate capability assumptions;
- identity rotation may invalidate authority but not historical Artifacts;
- endpoint replacement may require delivery reconciliation;
- body replacement may require reconstruction but not a new Task;
- policy change may fence pending work;
- expired Observation may require remeasurement without deleting the relation.

## Rebinding hierarchy

```text
same provider and operation identity: reconcile or resume
same target/capability, new path or endpoint: rebind communication
same semantic method, new provider/body: rebind execution
same Goal, different method or participant: Host replans and records handoff
```

World supplies facts and correlation. Host makes semantic strategy decisions.
