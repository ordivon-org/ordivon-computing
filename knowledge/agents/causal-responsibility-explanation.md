# Causal Responsibility Explanations

A useful Agent-facing system explanation does not need a complete ontology. It needs enough causal structure to prevent the next wrong action.

The stable default is **compact owner-native causal prose**: state the exact fact that matters, identify the authority that can prove it, separate that fact from nearby semantic or execution responsibilities, and state any dangerous inference that the evidence does not justify.

## The smallest useful explanation

A strong explanation often fits in one paragraph:

> Runtime proves that the local process completed. The external provider still owns whether the outside effect occurred. Because the provider receipt is missing, occurrence remains UNKNOWN; recover against the original external identity instead of inferring success or issuing a blind retry. Host may preserve the recovery Task, but that persistence does not make Host the provider-truth authority.

Nothing is gained by filling unrelated slots merely because a schema contains them.

## Ask questions only when something is actually uncertain

When the correct boundary is not obvious, use these as diagnostic questions rather than mandatory prompt context:

1. What happened?
2. Who can prove it?
3. Who decides what it means?
4. Who owns the durable semantic state?
5. Who merely carries or executes?
6. What does this evidence **not** prove?
7. What breaks if this component or relation is deleted?

Once the uncertainty is localized, compress the answer back into ordinary language.

## Five distinctions that repeatedly prevent wrong actions

### Proof is not meaning

An executor can prove a process ran without deciding what that result means to a domain. A provider can prove an external occurrence without deciding whether Finance should accept it as reconciled. A browser can prove exposure without deciding whether a person understood the page.

### Meaning is not persistence

A domain may own the semantics of a record while Host carries durable Task continuity for it. Physical storage or recovery does not transfer semantic ownership.

### Capability is not authority

An Agent or Tool may be able to perform an operation while the domain still refuses to admit the consequential action. Permission is separately bound to current subject, target, purpose, world state, and policy.

### Authority is not consequence truth

Admitting an action does not prove that an uncontrolled outside system performed it. Consequence truth returns through the owner-native observation or receipt boundary.

### Completion is scoped

Harness can complete a bounded Run, Runtime can complete a local Attempt, and a provider can finish a request while the Host Task or domain objective remains unresolved. Completion must always be read with its owner and scope.

## Current Ordivon map

**Computing** synthesizes cross-project evidence and revises the shared world model. It does not replace owner repositories as current truth.

**Host** keeps durable semantic work identity, commitments, verification, and Task-level outcome continuity.

**Harness** keeps the bounded structure of Agent cognition and Provider/Tool interaction. Provider-specific continuation state can be structurally necessary without becoming Agent-visible cognition.

**Runtime** proves exact admitted local execution and recovery. It does not generically prove outside-world effects or domain success.

**World** handles cross-owner external observations, connections, transfer identities, and reconciliation. Native domains/providers keep native occurrence and current-state truth.

**Finance, Security, Game, and Human** own their domain judgments. Shared infrastructure may execute or persist their work without acquiring those semantics.

**Studio and Web** own expression, rendering, publication, and encounter mechanics. They do not become a second source of product facts or human-response truth.

## Negative proof boundaries

These statements are especially useful because they prevent overreach:

- local execution success **does not imply** external effect occurrence;
- durable persistence **does not imply** semantic ownership;
- a successful Agent Run **does not imply** domain or Task completion;
- authenticated message delivery **does not imply** destination knowledge;
- historical materialization **does not imply** current Presence;
- implemented/tested target **does not imply** current product registration;
- effect-correctness evidence **does not imply** hostile-admin credential isolation or live authorization;
- another valid credential **does not imply** fitness of the exact credential installed in an executor;
- richer context or more search **does not imply** better untouched outcomes;
- a later correct conclusion **does not erase** an earlier admitted effect;
- a durable checkpoint **does not imply** unchanged current physical state;
- a framework that models a person **does not gain** authority over that person;
- Agent-observer success **does not imply** human comprehension or preference;
- randomized browser exposure **does not imply** comprehension or factual correctness;
- a projection or inspector hint **does not become** current owner authority;
- capability **does not imply** permission or verified consequence.

Each claim remains scoped. New evidence can narrow, strengthen, or falsify it.

## Causal history, navigation, and compression

OFR3–OFR6 add a second requirement to compact causal explanations: **the current winner is not the whole theory**. When future transfer, deletion, or reopening decisions matter, enough negative causal history must remain recoverable to explain why the current structure survived.

A useful recoverable causal case usually preserves:

```text
current invariant
+ strongest attractive rival
+ why the rival was attractive
+ decisive discriminator / falsifier
+ retained consequence
+ what restoring the rival would break
+ negative-transfer boundary
+ reopen condition
+ exact owner evidence escape hatch
```

This is a semantic recoverability target, not an eight-field storage schema. OFR4 strongly falsified winner-only summaries on held-out causal reconstruction, while compressed fixed packets did not earn a universal canonical representation. Ordinary work should still load only the causal material its decision actually needs.

### Reopen conditions are not action triggers

A theory sentence such as “reopen this question if X becomes possible” does not itself establish that X happened or authorize a mechanism change. Keep four responsibilities distinct:

```text
Theory.reopenCondition
!= Evidence.sufficientToClaimConditionObserved
!= Research.reopenQuestion
!= Owner.admitRivalOrAction
```

OFR4 discovered this boundary by invalidating its own one-bit reopen metric. The measurement failure is part of the evidence: a compact decision variable was too small because it collapsed theory, evidence, research policy, and owner authority.

### A map is not the territory or its owner

A compact index can be excellent at locating the right causal case without carrying that case's rival, falsifier, history, or current owner truth. Likewise, a cross-owner shared law can explain a recurring invariant without replacing the owner-local causal history that established a concrete product decision.

```text
index != causal theory
shared invariant != owner-local causal history
frozen theory != current owner truth / evidence authority
```

Navigation therefore keeps exact owner/revision references as escape hatches. If a current decision depends on present truth, revalidate with the owner rather than treating a frozen research reconstruction as live authority.

### Project mechanically known boundary facts

When an owning surface already knows a revision, truth role, currentness marker, or authority relation exactly, expose that fact mechanically rather than asking a model to infer it again from prose. OFR5's post-holdout diagnostic is narrow but instructive: a read-only Tool observation carrying explicit `truthRole`, currentness, and false evidence/research/admission/action-authority flags eliminated the authority overclaims seen in prose-only treatments on that bounded corpus.

This is not a universal metadata schema. Only mechanically owned facts should be projected; evidence sufficiency, semantic meaning, and domain judgment stay with the relevant owner.

### Compression is receiver-conditioned

Shorter sender payloads do not automatically reduce total cognitive cost. Compression can shift work into receiver reconstruction, extra model turns, longer conclusions, search, or failure recovery.

```text
useful compression
= fewer transmitted distinctions
  while preserving decision-relevant structure
  and reducing total accepted-work cost
```

EX3–EX7 showed strong compact prose can beat richer representations on bounded action reconstruction. OFR4 showed that deleting causal roles can reduce fidelity or shift token cost into reconstruction. OFR5 showed a 514-word Atlas index could still approach eager-full failure-adjusted prompt cost when navigation, hydration, and a second answer turn were counted. Evaluate the **whole consumption loop**, not word count alone.

## When to create a shared Ordivon layer

Start with mature classical infrastructure and the owner-domain implementation. Add a new Ordivon responsibility only when a recurring residual problem remains that those owners cannot correctly hold. Then ask the deletion question: if the proposed layer disappears, what materially breaks across more than one real workload?

If nothing important breaks, keep the layer deleted or local.

## Evidence for this explanation style

The EX3–EX7 programme in `research/experiments/ex3-ex7-causal-comprehension-v0/` preregistered five independent surfaces across 17 responsibility families. Across 1,326 accepted DeepSeek Flash action decisions, all accepted decisions matched the frozen oracle. Richer causal cards, typed relations, and explicit four-/seven-question scaffolds never improved exact action accuracy over strong compact prose and consistently consumed more reported Provider tokens. On the untouched EX7 surface, compact prose therefore won the preregistered smallest-non-inferior rule.

This is evidence about **Agent action reconstruction on the tested tasks**, not about human comprehension. Human-response claims require human-response evidence.

## Reopen condition

Do not elaborate this explanation model because a richer taxonomy is aesthetically appealing. Reopen it when reality supplies pressure: a fresh Agent repeatedly makes a consequential error under strong compact owner-native prose, a deletion/transfer workload breaks the boundary, a materially different model family fails recurrently, or multiple domains reveal the same genuinely unowned responsibility.
