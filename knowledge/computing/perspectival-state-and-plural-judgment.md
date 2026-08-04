# Perspectival State and Plural Judgment

## Concept

A plural-intelligence system should not assume that every participant acts from one shared, complete, and current representation of the world.

The same external world can produce materially different conclusions because participants may differ in at least four ways:

1. **observation** — they receive different signals or lose different information;
2. **interpretation** — they apply different causal models to the same evidence;
3. **commitment** — they pursue different purposes, bear different costs, or hold different authority;
4. **strategic expectation** — they reason about what other participants know, believe, conceal, or intend.

These differences are not automatically errors. Some are correct consequences of bounded access, role, responsibility, or value. Others arise from stale Context, deception, model failure, prejudice, or incompatible objectives. A useful system must preserve enough structure to distinguish them.

## The classical shared-state assumption

Many ordinary programs are designed as though one authoritative state can be read and every component should converge on it:

```text
authoritative state
→ read by every component
→ deterministic transition
→ one accepted result
```

This remains appropriate where a database, file system, simulator, or transaction owner really does provide the relevant state contract.

Plural intelligence introduces a different shape:

```text
one changing world
→ participant-specific access and observation
→ participant-specific Context and interpretation
→ different Claims, proposals, and judgments
→ negotiation, conflict, verification, or coordinated action
```

The world may still have domain-owned facts. The system should not confuse those facts with any participant's current view of them.

## Minimum distinctions

### World occurrence or domain state

What happened or currently holds according to the domain authority.

In a simulator this may be directly readable as ground truth. In an open physical or social world, complete real-time truth may not exist for the system; only later adjudication or bounded Facts may be available.

### Observation

An immutable reading available to one observer through one path at one time.

An Observation should preserve source, time, scope, revision, omissions, and integrity where available. It does not automatically establish a causal explanation.

### Perspective

The bounded view from which one participant or role reasons. A perspective is not merely a username. It may bind:

```text
participant or role
+ selected Observations and Artifacts
+ Context-selection method and omissions
+ current commitments and authority
+ time and world revision
+ known uncertainty
```

This is a candidate explanatory structure, not yet a promoted shared object.

### Belief or hypothesis

A revisable interpretation of possible world states, causes, opponent policies, or future outcomes. Competing hypotheses may remain simultaneously useful.

### Claim

A proposition communicated by a participant, Tool, document, service, or institution. A Claim may be honest, mistaken, strategic, deceptive, or unverifiable.

### Judgment

A choice about what matters, what evidence is sufficient, what risk is acceptable, or which action should be proposed under one participant's commitments and consequence exposure.

Two participants can agree on observations and probabilities yet reach different judgments because they own different resources, duties, risks, or purposes.

### Verification and Fact

Verification evaluates a bounded Claim using a declared method and authority. A Fact is admitted only for the declared domain, version, and scope. Fact admission can reduce disagreement about what holds without erasing legitimate disagreement about what should be done.

## Four kinds of divergence

### Informational divergence

Participants receive different evidence.

Example: one defensive Agent observes a sensor alert while another has access to an independent management-plane receipt.

### Interpretive divergence

Participants receive materially similar evidence but infer different causes.

Example: one Agent interprets a failed connection as ordinary fault; another assigns probability to an opponent countermeasure.

### Commitment divergence

Participants agree about likely world state but hold different objectives, authority, or loss exposure.

Example: an operator responsible for service continuity and an evaluator responsible for experimental purity can rationally prefer different next actions.

### Strategic divergence

A participant acts partly to change what another participant observes, believes, or expects.

Example: a decoy is valuable not because it directly changes the protected asset, but because it redirects the opponent's inference and resource allocation.

These divergence classes should not be collapsed into one generic disagreement field.

## Why this matters for Agent systems

### Context is perspective-bound

Context is already a compiled view rather than durable truth. In plural systems, the Context binding should also preserve whose view it represents and what was omitted from that participant.

A universal Context assembled from all available evidence may improve a central evaluator while invalidating an experiment intended to measure a bounded Actor.

### Joins need not force consensus

An Artifact Join may produce:

- one accepted result;
- several bounded conclusions under different assumptions;
- a verified factual core plus unresolved judgment conflict;
- a DecisionRequest routed to the owner of the missing commitment;
- an explicit declaration that evidence is insufficient.

Convergence is one possible result, not the definition of coordination.

### Evaluation must identify the observer

A trajectory cannot be interpreted without knowing which participant saw which evidence. Replay that gives a replacement model more information than the original Actor changes the evaluated system.

### Authority changes the meaning of the same proposal

The same proposed external change may be reasonable for one resource owner, prohibited for another participant, and inadmissible for an evaluator. Perspective therefore includes responsibility and consequence, not only information.

## Cyber and future adversarial worlds

Cyber Contest evidence makes the issue visible:

```text
world or simulator state
≠ Red observation
≠ Blue observation
≠ sensor telemetry
≠ evaluator evidence
```

Intelligent opposition can deliberately shape those differences. Future network conflict may therefore be determined not only by who controls more compute or Tools, but by who can:

- obtain useful observations;
- preserve uncertainty without paralysis;
- detect manipulated evidence;
- understand another actor's likely perspective;
- coordinate without leaking every view;
- revise beliefs faster than the opponent can exploit them;
- preserve command intent through Context loss and participant replacement.

The same structure may appear in games, organizations, markets, scientific collaboration, and human–Agent decision systems without the adversarial component.

## Design implications

For now, Ordivon should prefer composition over a new universal perspective database:

```text
ParticipantRef or role
+ ContextSelection
+ Observation / Artifact references
+ Claims and hypotheses
+ commitments and Authority
+ explicit time and uncertainty
```

A shared `PerspectiveState` primitive is not admitted until at least two materially different workloads demonstrate one non-bypassable invariant that cannot remain in Host Context, domain Actor state, or evaluation records.

Potential invariants to test include:

- observer identity must survive model and Harness replacement;
- omitted evidence must be reconstructible enough to reproduce the decision boundary;
- unresolved disagreement must survive Join without transcript replay;
- actor-specific views must remain isolated while independent evaluation retains broader evidence;
- a perspective swap or evidence equalization must change behavior in predicted ways.

## Boundaries

Perspectival computation does not imply that every statement is equally valid or that external facts do not exist. It requires stronger attribution:

```text
who observed or claimed what
from which access path and Context
under which commitments and authority
with what uncertainty
before which world change
```

It is also not a justification for autonomous high-consequence action. Domains retain their own authority, law, verification, and human responsibility requirements.

## Research path

The first evidence comes from Ordivon Security's actor-specific Contest and CAGE Range. A second non-adversarial workload should come from Game or Host, where two participants receive bounded views or share facts but differ in commitments. If existing Observation, Claim, Verification, Fact, ContextSelection, and domain-local Actor state explain both workloads without a new object, the research should be absorbed rather than promoted.

See:

- [`state-computation-and-memory.md`](state-computation-and-memory.md);
- [`../agents/task-context-authority-effect-evidence.md`](../agents/task-context-authority-effect-evidence.md);
- [`../../research/questions/ANC-EPISTEMIC-001-perspectival-state-and-plural-judgment.md`](../../research/questions/ANC-EPISTEMIC-001-perspectival-state-and-plural-judgment.md);
- [`../../research/questions/ANC-SECURITY-004-opponent-modeling-and-deception.md`](../../research/questions/ANC-SECURITY-004-opponent-modeling-and-deception.md).
