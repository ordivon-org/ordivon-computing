# 01 — Ordivon Security Campaign Handoff

Status: retained research handoff; no R7 and no immediate platform build

## Why this handoff exists

R0-R6 answered the original Computing question:

```text
Can Web, network, identity, interpretation, partial-failure, and Agent attack
mechanisms be expressed precisely, transferred into an executable owned range,
and used to falsify existing Host/Runtime boundaries without prematurely
constructing a general Security platform?
```

The answer is yes. R6 produced real-model and real-Runtime evidence for one
structural Tool-metadata attack primitive, Assignment-scoped ToolGrant,
independent completion verification, exact Agent Computer Interface schemas, and
typed deterministic denial recovery.

R6 did **not** construct a high-intensity adaptive opponent. Its strongest attack
was a scientifically clean structural primitive:

```text
benign Task evidence
+ malicious model-facing Tool metadata
+ ambient physical authority
→ owned Canary read
→ opaque local execution
```

That finding is real and architecturally useful, but the attacker remained mostly
static, short-horizon, single-path, non-persistent, non-coevolving, and unaware
of the defender. Continuing as R7 would mix two research objects. The next object
belongs to Ordivon Security:

> goal-bearing opponents that observe, infer, adapt, choose timing, preserve
> state, compose authority, manipulate evaluation, and continue a Campaign
> across changing worlds and defensive responses.

## Series boundary

```text
R series
  Given an attack or perturbation, what does the system do?

Security Campaign series
  Given an objective, resources, observations, and feedback, what does an
  adaptive opponent discover and attempt over time?
```

Use `C0-C6` as a provisional execution sequence, not as a frozen protocol or new
ontology. `C` means Campaign. The sequence can be renamed or collapsed after the
first experiments.

## Admission constraints

Every executable Campaign experiment must:

- remain inside owned or explicitly authorized worlds;
- use synthetic credentials, Canary assets, and reversible consequences;
- block uncontrolled external egress and public-target interaction;
- preserve exact Actor, Campaign, World, model, scaffold, Tool, authority,
  observation, Effect, judge, seed, and Trial identities;
- separate Actor observation from authoritative World truth;
- preserve proposed action, Host admission, Runtime result, World Effect,
  verification, recovery, and residual state as different facts;
- report authorized utility and defensive cost, not only attack success;
- retain invalid, inconclusive, `UNKNOWN`, and interrupted trajectories;
- compare against a simpler scripted or fixed-policy baseline;
- delete new structures when mature external systems or simpler local records
  provide equivalent evidence.

Reachability remains distinct from authority. This handoff does not authorize
third-party intrusion, real credential use, safeguard evasion, stealth against
external operators, or uncontrolled persistence.

## C0 — Attacker Contract and Campaign boundary

### Question

What is the minimum representation required for a real adaptive opponent without
creating a universal adversarial ontology?

### Minimum attacker state

```text
objective and victory / exit conditions
resource and action budget
current observation history
beliefs and uncertainty about World and defender
candidate strategy families
known and hypothesized authority boundaries
adaptation history
persistence and recovery state
expected utility, cost, detection, and residual risk
```

### Required baselines

- fixed scripted policy;
- stochastic fixed policy;
- transcript-only LLM actor;
- stateful adaptive LLM actor;
- mixed scripted / model-backed team when justified.

### Promotion rule

Promote no `Opponent`, `Belief`, `Strategy`, or `Campaign` schema unless it
improves held-out performance, transfer, diagnosis, or recovery over ordinary
trajectory records.

## C1 — Adaptive feedback and denial-oracle suite

### Purpose

Test whether defensive feedback that helps a legitimate Agent recover also helps
an attacker infer the boundary and find another path.

### Feedback variants

```text
generic denied
typed tool_grant_denied
Tool absent from catalog
path-specific denial
resource-specific denial
Runtime UNKNOWN
verification rejected
completion rejected
```

### Attacker behavior

The Red actor may probe, compare feedback, update its hypothesis, alter semantic
carrier, choose another Tool, defer the action, or abandon the path.

### Measurements

- legitimate recovery rate;
- attack adaptation rate;
- probes required to infer the boundary;
- unauthorized World Effects;
- information leaked by each denial class;
- model calls, Tool calls, tokens, and elapsed steps;
- false attribution of natural faults as defensive action;
- net utility of feedback precision.

### Central falsifier

Typed denial should be retained only if legitimate recovery gains exceed any
material increase in adaptive attack success under held-out opponents.

## C2 — Persistence and delayed-activation suite

### Purpose

Move beyond immediate Canary access. Test whether an opponent can influence
future work while current authorized utility remains normal.

### Owned persistence carriers

- durable memory;
- generated-Tool registry;
- Tool descriptions or schemas;
- Context source documents;
- Task continuation state;
- benign-looking intermediate Artifacts;
- scheduled or phase-gated Campaign state;
- provider- or Harness-replacement handoff records.

### Required transitions

```text
initial influence
→ current task completes normally
→ Host closes or restarts
→ Context is compacted or partly lost
→ model or Provider changes
→ later Assignment loads
→ delayed condition is evaluated
→ independent residual inspection
```

### Measurements

Persistence survival, activation accuracy, false activation, utility preservation,
state visibility, cleanup completeness, and whether fresh Host/Verifier instances
can prove removal.

### Delete condition

Delete specialized persistence machinery if ordinary durable Task state plus
exact source provenance fully explains and removes the observed failures.

## C3 — Authority laundering and multi-Agent composition suite

### Purpose

Test attacks where no single local action is obviously unauthorized, but the
composed trajectory serves an unauthorized Campaign objective.

### Authority-laundering chain

```text
untrusted observation
→ legitimate model judgment
→ authorized intermediate Artifact
→ second Agent or Assignment
→ different ToolGrant or identity
→ final World Effect
```

### Multi-Agent split-intent variants

- one Agent discovers information;
- another transforms it into an innocuous representation;
- another generates or selects a Tool;
- another possesses the final authority;
- no single Actor receives the complete Campaign objective.

### Measurements

End-to-end objective success, local-action legitimacy, delegation chain,
information flow, authority amplification, detectability, attribution error,
compartment failure, and independent reconstruction quality.

### Architecture question

Determine whether owner-local ToolGrant and provenance remain sufficient, or
whether a minimal cross-Assignment continuity or purpose receipt is required.
Do not create a central Security authorization service by default.

## C4 — Tool and control-plane supply-chain suite

### Purpose

Generalize the R6 Tool-description primitive across the full Agent Computer
Interface and its build / serialization path.

### Differential points

```text
Tool source
→ build or generation
→ JSON Schema
→ descriptions and examples
→ catalog commitment
→ durable Assignment binding
→ Provider-specific serialization
→ per-Turn model definitions
→ Host reload
→ Tool revision or replacement
```

### Variants

- description-only drift;
- schema / description disagreement;
- example-induced authority confusion;
- generated-Tool replacement;
- catalog-digest preservation with serialized-definition drift;
- provider adapter normalization differences;
- stale Tool revision after Host replacement;
- partial catalog visibility under Context pressure.

### Measurements

Model behavior change, exact-definition mismatch, unauthorized proposal,
Host/Runtime admission, World Effect, transfer across Providers, and cost of exact
per-Turn binding.

### Promotion rule

Admit exact per-Turn Tool-definition binding only if the mismatch reproduces with
a materially different Provider or mature Harness and cannot be localized to one
adapter.

## C5 — Covert parallel effects, recovery resistance, and evaluator attack

### Covert parallel effects

The authorized Task may complete correctly while the opponent attempts a second
hidden consequence:

- unexpected file or Artifact creation;
- memory or registry mutation;
- excess Tool or Job creation;
- future trigger installation;
- evidence omission;
- selective cleanup;
- misleading completion narrative.

Authorized utility therefore does not imply absence of adversarial Effect.

### Recovery-resistance sequence

```text
revoke authority
remove contaminated state
rebuild Workspace
replace Host / Harness / model
reconcile in-flight Effects
reload durable Task
inspect all derived objects
prove clean residual state
```

The Red actor attempts to preserve one capability, identity, trigger, derived
Artifact, or misleading belief across recovery.

### Evaluator-integrity variants

- visible versus hidden judge state;
- manipulation of evidence selection;
- reward / score gaming;
- benign-looking completion with omitted residual;
- exploitation of judge assumptions;
- monitor-aware timing;
- held-out independent trajectory review.

### Measurements

False accepts, false rejects, residual completeness, ranking stability across
judges, hidden-effect detection, recovery cost, and transfer to held-out Worlds.

This suite should coordinate with Security issue #20 rather than duplicate a
universal evaluator platform.

## C6 — Red/Blue coevolution, transfer, and disposition

### Purpose

Evaluate whether any learned attack or defense survives beyond the exact system
on which it was developed.

### Minimum loop

```text
Red version N attacks Blue version N
→ Blue changes one bounded control
→ Red receives only allowed observations
→ Red adapts under fixed budget
→ held-out Red attacks held-out Blue
→ independent verifier evaluates World outcome
```

### Required transfer axes

- held-out opponent policy;
- held-out World seed or topology;
- Provider or model family;
- Harness implementation;
- Tool catalog revision;
- Context loss and fresh Host;
- judge / monitor change;
- natural fault versus adversarially induced similar observation.

### Measurements

Attack and defense transfer, regression, strategic objective success, authorized
utility, resource efficiency, adaptation speed, evaluator integrity, residual
risk, and complexity cost.

### Final disposition

For every introduced structure choose exactly one:

```text
retain in Security research layer
localize to Host / Harness
localize to Runtime
localize to World
localize to Game
replace with mature external system
freeze as evidence only
delete
```

## Suite map

| Suite | Primary adversarial capability | Existing Ordivon responsibility tested |
|---|---|---|
| C0 Attacker Contract | objective, belief, budget, adaptation | Security research layer |
| C1 Denial Oracle | defense-aware probing and strategy update | Host/Harness feedback and ToolGrant |
| C2 Delayed Persistence | survive time, restart, Context and Provider changes | Host durable state, World evidence |
| C3 Authority Laundering | compose individually legal actions and Agents | Host authority, provenance, continuity |
| C4 Tool Supply Chain | corrupt control-plane semantics and revisions | Harness Tool catalog and adapters |
| C5 Covert/Recovery/Evaluator | hide parallel Effects and resist cleanup | Runtime/World evidence and independent judges |
| C6 Coevolution/Transfer | adapt across defenses and held-out systems | Security evaluation and architecture disposition |

## Relationship to existing Security issues

- **#1** remains the parent Agent-native strategic adversarial-systems program.
- **#10** already owns opponent-state transfer under policy switches and Context
  loss; C0/C2 should consume its evidence instead of creating another memory
  system.
- **#20** already owns held-out opponents and evaluator-integrity attacks; C5/C6
  should activate through that Issue when a stable Campaign trajectory exists.
- R6 remains frozen and supplies the Tool-metadata primitive, ToolGrant cut,
  typed-denial hypothesis, exact ACI finding, and evidence methodology.

## Activation rule

Do not execute all suites as one roadmap. Activate the smallest suite that can
falsify the next concrete Security claim. The first likely experiment is C1:
compare generic versus typed denial under a stateful held-out Red actor, because
R6 established both the utility benefit and the unmeasured oracle risk.

## Non-goals

No public target, uncontrolled egress, real credentials, generic malware
platform, scanner replacement, SIEM, IAM, central policy engine, universal
Campaign ontology, Security-owned Runtime, Security-owned memory, or permanent
cyber-range reimplementation.

## Recorded Security handoff

The full deferred suite map is now recorded in Ordivon Security:

- Security issue **#23** — `Deferred C-series: Adaptive Campaign adversarial suites after R6`;
- labels: `research`, `cross-project`, `status:deferred`;
- URL: https://github.com/zycxfyh/ordivon-security/issues/23

Issue #23 is the durable Security-side entry point. This document remains the
Computer-side evidence and architecture handoff. The Issue may evolve as Security
experiments produce evidence; R6 itself remains frozen.
