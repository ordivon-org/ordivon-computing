# 04 — Task Connectivity and Evidence Continuity

## Connectivity Requirement

Candidate dimensions include:

- logical source and target;
- interaction purpose and direction;
- synchronous, asynchronous, stream, Artifact, or callback form;
- target identity assurance;
- data classification and allowed trust domains;
- locality, latency, availability, and cost;
- session and continuity requirements;
- evidence and reproducibility requirements;
- allowed path, intermediary, and participant replacement.

No field is promoted before two workloads require it.

## Connectivity Binding

A Binding should preserve:

```text
Task / Attempt / Effect
→ logical source and target
→ selected endpoint, path, transport, intermediary
→ identity and policy revision
→ observations used for selection
→ freshness and invalidation conditions
→ communication execution or delivery identity
```

## Path-conditioned evidence

An Artifact or Observation remains valid historical evidence after a path
change, but only under its recorded conditions. A Tokyo Edge screenshot, a
local direct probe, and a VPN-based response may all be correct observations of
different externally conditioned worlds.

The system should distinguish:

- still valid;
- conditionally valid;
- expired;
- superseded;
- requires re-verification.

## Relationship continuity

A connection failure should not erase accepted work. Recovery first determines
whether the original request or Artifact was accepted, processed, or answered.
Only then may the system retry, reroute, switch communication form, or hand off
to another participant.
