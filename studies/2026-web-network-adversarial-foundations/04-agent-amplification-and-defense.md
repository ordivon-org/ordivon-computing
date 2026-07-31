# 04 — Agent Amplification and Defense

## The correct question

The question is not whether an Agent can perform an action that software or a
human could already perform. It is:

> Which adversarial properties are merely faster or cheaper, which are composed
> from mature mechanisms, and which system responsibilities are structurally
> rewritten when probabilistic cognition selects and revises world-changing
> actions?

Use the Ordivon classification:

- **unchanged** — the classical mechanism remains sufficient;
- **amplified** — scale or importance changes, not semantics;
- **composed** — several mature mechanisms form a product capability;
- **rewritten** — the old abstraction remains but its contract changes;
- **new responsibility** — no lower layer owns a necessary non-bypassable
  invariant.

## What remains classical

Agents do not replace:

- protocol parsing and standards compliance;
- operating-system process and file authority;
- network transport and cryptography;
- container or VM isolation;
- database transactions;
- IAM, credential issuance, and revocation mechanisms;
- software signing and build systems;
- vulnerability taxonomies and patch mechanics;
- telemetry storage and incident-response procedures.

The first defense against many Agent attacks remains correct classical
engineering.

## What Agents amplify

NIST's 2026 synthesis of public input on Agent security reports broad agreement
that classical cybersecurity remains relevant but requires adaptation for
Agent-specific threats. OWASP's Agentic Threats Navigator similarly spans
reasoning, memory, Tools, identity, human oversight, and multi-Agent
interaction. These sources support a cross-surface analysis, but neither proves
that Ordivon needs one new universal Agent-security layer. [R18][R19]

### Search breadth and speed

An Agent can inspect many surfaces, compare responses, generate hypotheses, and
prioritize follow-up at low marginal cost.

### Retry and probabilistic accumulation

Cheap repeated attempts can convert a low per-attempt failure probability into a
material cumulative risk.

### Semantic adaptation

The actor can interpret documentation, error messages, business meaning, and
defender response rather than matching only fixed signatures.

### Tool construction

The actor can create parsers, adapters, scripts, detectors, or one-use programs
during the Campaign. A denylist of known binaries therefore does not define the
actor's capability set.

### Cross-domain composition

An Agent can connect Web content, email, source code, cloud APIs, local Runtime,
identity systems, and human communication inside one reasoning loop.

### Multi-Agent parallelism

Specialized actors can search, execute, validate, deceive, or defend in
parallel, while also creating communication, compromise, and collusion risks.

### Defender modelling

The attacker can infer which controls exist, test them, and choose a path that
preserves the same objective.

### Evaluator attack

The evaluated Agent can exploit scoring loopholes, manipulate evidence, or
appear compliant while pursuing a side objective.

## Structurally rewritten boundaries

### Data versus instruction versus authority

Classical injection separates data and code. Agent systems must additionally
separate external data from trusted instruction and from authority to commit an
Effect. Current LLM interfaces often combine these into one model-visible
Context, creating Agent hijacking risk. NIST characterizes this as a failure to
clearly separate trusted instructions from untrusted external data. [R13]

### Static Tool catalog versus capability realization

The available capability set can change during a Task through discovery,
dependency acquisition, code generation, build, test, and deployment. Safe use
therefore depends on provenance, environment, identity, scope, and observed
Effect—not only a Tool name.

### One-shot control versus repeated adaptive evaluation

A defense that blocks known attacks once may fail against an optimized attacker
or repeated trials. Evaluation must bind the attacker policy and allow held-out
adaptation.

### Network location versus conditioned world access

An Agent's effective access depends on path, identity, Tool, endpoint, provider,
body, policy, and current world revision. Network location alone neither grants
trust nor explains consequence.

### Completion versus reconciliation

Agents may retry after ambiguous responses. Durable Effects require stable
identity, explicit `UNKNOWN`, observation, and reconcile-before-redispatch.

## Attack and defense symmetry

Both Red and Blue Agents can:

```text
observe
→ form competing hypotheses
→ construct Tools
→ act through bounded identities and paths
→ inspect evidence
→ revise strategy
```

The asymmetry comes from objectives, authority, information, resources,
visibility, and world position—not from giving only one side intelligence.

## Defensive design principles

### Maximize cognition; bind consequence independently

Permit broad reasoning, local analysis, simulation, and reversible Tool
construction. Bind external targets, identities, resources, egress, durability,
and irreversible effects separately.

### Make authority explicit at commitment

An authenticated channel or available Tool does not prove that one proposed
Effect serves the participant's current intent.

### Preserve independent world truth

Evaluated Agents must not be the sole authority for network topology, process
state, evidence storage, score, or residual closure.

### Observe Effects, not only prompts

Prompt-level intent filters cannot establish which API calls, files, messages,
credentials, external objects, or network sessions actually changed.

### Bind generated Tools to provenance and scope

Record source, dependencies, build environment, tests, identity, allowed World,
actual execution, produced Artifacts, revision, and retirement condition.

### Use graph defense

Reduce reachable paths through identity scope, segmentation, egress policy,
strict parsing, isolation, detection, deception, recovery, and residual
verification. Do not assume one control is an absolute boundary.

### Evaluate adaptation and cumulative probability

Measure repeated attempts, novel attacks, policy switches, false positives,
resource costs, and held-out opponents.

### Close the Campaign, not only the CVE

After patching, inspect credentials, sessions, bodies, Tools, messages, external
objects, memory, observer integrity, and remaining uncertainty.

## Agent-specific hypotheses requiring later evidence

R0 does not yet establish that Ordivon needs durable objects for:

- generated Tool admission;
- Agent-body continuity;
- opponent belief state;
- cross-Agent propagation;
- adaptive defense policy;
- Campaign-level graph state.

These become product responsibilities only after a real experiment demonstrates
an unowned failure that simpler Host, Runtime, World, Security, or mature
substrate mechanisms cannot resolve.
