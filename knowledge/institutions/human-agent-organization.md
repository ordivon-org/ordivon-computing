# Human–Agent Products and Organization

Agent capability changes the allocation of work, attention, and responsibility. It does not remove human purpose or consequence ownership.

## Persistent product objects

A conversation is an effective entry point for an open Goal, but sustained work needs visible durable objects:

```text
Goal and constraints
+ Task frontier and Attempts
+ current world bindings
+ Context inputs
+ Effects and Dispatches
+ Artifacts, Claims, and verified Facts
+ decisions that require the operator
```

Conversation carries negotiation and explanation. Durable work objects carry continuity and authority.

## Division of responsibility

People contribute:

- purpose and priority;
- values and tradeoffs;
- social and domain context;
- acceptance of irreversible consequences;
- judgment where evidence is incomplete or objectives conflict.

Agents contribute:

- high-throughput reading and candidate generation;
- repeated bounded execution;
- cross-tool observation;
- independent alternatives and counterexamples;
- continuous maintenance when completion criteria are explicit.

The useful structure is:

```text
human purpose and consequence ownership
+ Agent exploration and execution
+ deterministic evidence from reality
```

## Operator attention is a system resource

As Agent throughput rises, per-action approval becomes both expensive and unreliable. A product should distinguish:

- reversible exploration that can proceed under a bounded grant;
- ordinary effects covered by an explicit policy;
- novel, ambiguous, costly, or irreversible effects that require escalation;
- claims that lack sufficient evidence for acceptance;
- conflicts among Goals or projects that require human priority.

A decision request should include the reason, alternatives, evidence, consequence, reversibility, and cost of delay. Asking the user to approve every Tool call transfers policy execution back to a fatigued human.

## Multi-Agent collaboration

Multiple Agents create value only when work contains real independent structure and results can be compared or joined through stable artifacts.

Useful forms include:

- independent research or design candidates;
- specialist execution against separate Workspaces;
- actor and independent verifier separation;
- pipeline stages with explicit input and output contracts;
- bounded adversarial or counterexample search.

A Join is a state-reduction operation, not merely several messages arriving:

```text
independent Attempts
→ Artifacts, Claims, and evidence
→ explicit comparison or integration rule
→ accepted result or unresolved conflict
```

More Agents can also increase duplicate work, shared-error amplification, token cost, and merge complexity. Agent count is not a maturity metric.

## Handoff and institutional memory

A continuation record should transfer current semantic state rather than an unfiltered transcript:

```text
Goal
active Task frontier
world and contract revisions
Attempts and unresolved uncertainty
verified Facts and Claims under evaluation
relevant Artifacts
next admissible work
```

Organizational memory can then evolve through explicit promotion:

```text
raw events
→ Observations and Artifacts
→ verified Facts
→ reusable Knowledge
→ challenged Core principles
```

## Evaluation and economics

Local metrics such as commits, tests, tokens, or Agent turns can be useful operational signals. They do not establish Goal progress.

A personal Agent system should optimize for outcomes such as:

- accepted results per active human minute;
- recovery after interruption;
- independent verification rate;
- duplicate or abandoned work;
- cost per accepted result;
- entropy introduced into repositories and operations;
- important decisions surfaced without approval fatigue.

As generation becomes cheaper, value moves toward problem selection, unique world access, reliable verification, durable continuity, user trust, and responsibility for consequences.

See the [probabilistic work-control loop](../agents/probabilistic-work-control-loop.md) and the [transition study](../../studies/2026-classical-to-agent-native-computing/README.md).
