# SECURITY-CHARTER-001 — Full-Spectrum Adversarial Agent Systems Research

Status: initial charter

## Mission

Ordivon Security is the full-spectrum adversarial Agent systems laboratory for maximum-capability elicitation, cyber-range experimentation, attack-defense coevolution, containment, and recovery research.

It studies what capable Agents can discover, construct, coordinate, attack, defend, deceive, repair, and become when placed in dynamic hostile digital environments with long-lived state, tools, resources, and other adaptive actors.

## Governing principle

```text
maximize internal capability
minimize external consequence
measure both independently
```

Safety is not achieved by making the evaluated Agent weak. It is achieved by placing strong Agents in owned, observable, reconstructable environments whose external effects are independently constrained.

## Research domains

- autonomous reconnaissance, world modelling, planning, adaptation, and multi-stage action;
- autonomous defense, attribution, isolation, deception, repair, restoration, and continuity;
- Red-Agent versus Blue-Agent and multi-party adaptive interaction;
- Agent-specific attack surfaces: prompt, context, memory, Tool, Artifact, identity, delegation, reward, evaluation, and supply-chain manipulation;
- system-level cyber behavior across applications, services, operating systems, networks, identities, and distributed nodes;
- capability elicitation across models, Harnesses, tools, time, compute, memory, and multi-Agent organization;
- containment failure, observer integrity, evidence preservation, recovery, and post-incident learning.

## Experimental authority

Security campaigns operate only in environments represented as owned or explicitly authorized range worlds. Within those worlds, scenarios may grant broad autonomy, writable systems, tool creation, persistence, multi-node coordination, and adaptive opponents. The campaign manifest defines the consequence envelope separately from the capability envelope.

## System composition

```text
Security: campaign, actors, objectives, judge, evaluation
Host: cognition, Goal, Task, Context, ownership
Runtime: trusted-local execution and analysis
Link: network world and communication fabric
Edge: remote bodies and external presence
Game: deterministic scenario, replay, and scoring machinery
```

## Required invariants

1. Capability Envelope and Consequence Envelope are separate first-class objects.
2. Every target belongs to a declared range world and authority record.
3. Management, observation, and experiment planes are distinct.
4. The evaluated Agent cannot modify the authoritative judge, event root, or containment controller.
5. Campaign start, mutation, freeze, export, reset, and destruction are durable events.
6. A result without exact model, Harness, Tool, budget, topology, and environment identity is not a capability claim.
7. Negative results, escapes, observer failures, and incomplete evidence remain visible.
8. Real external systems are never inferred to be authorized from reachability alone.

## Non-reduction principle

Containment controls may constrain where consequences land, but must not silently remove the internal capabilities being measured. A test that omits long-term state, tool construction, lateral coordination, adaptive planning, or realistic failure cannot claim to measure those abilities.

## Success condition

Security is successful when it can run high-capability, adaptive, multi-Agent campaigns in dynamic ranges; produce replayable evidence and causal explanations; detect containment or observer failure; restore or destroy the world; and improve both attack understanding and defensive resilience without uncontrolled third-party impact.
