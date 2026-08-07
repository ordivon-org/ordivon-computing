# Capability Externalization and Responsibility Placement

## Core thesis

Computing progress repeatedly moves stable work out of an intelligent actor and into external structure. Arithmetic becomes hardware; repeated procedures become software; fragile operator memory becomes durable state; repeated protocol reasoning becomes a Tool or adapter.

For Agent systems the useful question is therefore not which subsystem name sounds future-facing. It is:

> Which responsibility is still being reconstructed inside probabilistic inference, transient Session state, or human operational memory even though it is repeated, formalizable, persistent, shared, verifiable, or precision-sensitive?

Externalization is a candidate optimization, not a default architectural good. Stronger future models should increase the amount of work that can remain cognitive. Ordivon should retain only external structures whose responsibility remains valuable even when the model, Provider, Context window, and reasoning quality improve materially.

## Future-model robustness test

A shared Ordivon responsibility is durable when at least one of these remains true for a much stronger model:

- the fact must survive model, process, Session, or Provider replacement;
- multiple actors or owners require the same identity or current state;
- an external Effect can be duplicated, lost, partially observed, or become `UNKNOWN`;
- authority, budget, ownership, privacy, or consequence must be enforced outside model preference;
- a Claim requires evidence or independent verification before becoming accepted truth;
- an external object, Tool contract, source, policy, or capability can drift after Context was compiled;
- deterministic precision or mechanical lowering is cheaper and more reliable than repeated reasoning;
- a failure must be recoverable without reconstructing an old hidden cognitive state.

A structure is model-contingent when its only justification is that a current model cannot reason far enough, remember enough, call a low-level API accurately enough, or search a large enough space. Such a structure may still be useful as a Tool or experiment, but it does not earn permanent Core status from that limitation alone.

## Responsibility placement

For every repeated burden, identify:

```text
responsibility
+ current carrier
+ failure when that carrier disappears
+ strongest existing lower owner
+ smallest candidate externalization
+ measurable benefit
+ permanent cost
+ deletion trigger
```

The preferred placement order is:

1. keep flexible judgment in the strongest available cognition when no durable invariant is required;
2. use mature classical substrate when it already owns the mechanism;
3. add an Agent-friendly semantic adapter when the substrate is correct but the calling surface wastes cognition;
4. add durable Agent-native state only when a stable responsibility otherwise has no owner;
5. promote to a shared protocol or lower layer only after multiple workloads need the same invariant.

## Durable conclusions from earlier Ordivon research

### Classical substrate stays classical

Operating systems, filesystems, databases, Git, networks, containers, VMs, queues, durable workflows, compilers, model serving, metrics, and tracing remain authoritative for their established mechanical responsibilities. Agent use can amplify their importance without making them Agent-native inventions.

### Model output is a proposal

A generated token sequence is not automatically a Task update, authorized Effect, Observation, Fact, or semantic completion. Stronger models improve proposal quality; they do not erase the distinction between proposal and committed reality.

### Work identity outlives cognition episodes

A Goal or Task may survive a model call, Provider Session, Harness Run, process, or machine. Durable work state should preserve the minimum current semantics needed for continuation. Raw transcript, Provider Session identity, and hidden reasoning are replaceable implementation state rather than universal work authority.

### Context is a compiled view

Context is selected input to one cognitive episode. Source identity, revision, provenance, and invalidation matter because a stronger model can still reason correctly over stale or unauthorized input. The stable responsibility is selection and binding, not one retrieval algorithm or one permanent memory product.

### Semantic intent should lower into reliable mechanics

When an Agent repeatedly reconstructs exact ranges, request envelopes, retry semantics, or backend-specific syntax, the system should test whether a semantic Tool plus deterministic lowering removes that burden. This is why an exact-replace editing action can coexist with a lower-level patch primitive: the substrate remains authoritative while the Agent-facing interface moves mechanical precision out of token space.

### Effect and Dispatch are different

A stable intended observation or change is not the same object as one physical attempt to perform it. Response loss produces uncertainty rather than proof of failure. Reconciliation before redispatch remains necessary regardless of model intelligence.

### Evidence is not narrative confidence

Observation, Artifact, Claim, Verification, and accepted domain Fact have different roles. Better reasoning can improve interpretation but should not silently replace owner-native evidence or an independent verifier where consequence or evaluation requires one.

### Host, Harness, and Runtime are responsibility boundaries, not a fixed product stack

Current Ordivon uses a useful split:

```text
Host      durable work and semantic commitment
Harness   one cognitive execution environment and Agent loop
Runtime   physical execution facts and recovery
```

The names or deployment packaging may evolve. The durable rule is single ownership of authoritative facts and replaceability across boundaries. If a future system can merge implementations without merging authority or losing recovery, the packaging may shrink.

### Reversible exploration and durable consequence should have different friction

Private, isolated, reversible work should be broad and cheap. Shared, irreversible, public, financial, privacy-sensitive, or otherwise high-recovery-cost Effects require stronger external commitment and evidence. Stronger Agents make this distinction more useful because they can explore more widely before crossing a consequence boundary.

### Existing structures do not inherit legitimacy

Git history preserves cheap implementation history. Current code, research documents, tests, schemas, compatibility paths, and governance survive only when they have a current consumer and positive recurring value. The default re-audit candidate is removal from the active path.

## Conditional hypotheses, not durable architecture

The following remain legitimate research candidates but must not be treated as inevitable layers:

- Temporal Cognitive Graphs and typed relational cognitive state;
- persistent Run Actors;
- Prime-style programmable cognition, recursive model calls, and bounded Child Runs;
- multi-Agent branch/join infrastructure beyond ordinary Tasks and Artifacts;
- a general memory runtime;
- a universal Agent VM or cognitive scheduler;
- a shared World layer beyond direct provider/domain adapters and Effect bindings;
- a generic organization layer;
- continual self-modification or self-training infrastructure.

Each should be tested only after a stronger and simpler baseline fails. As models improve, some of these candidates may become less necessary; others may become more useful because stronger cognition can exploit richer external structure. The experiment decides.

## What earlier research can leave the active tree

Detailed derivations, broad taxonomies, dated source audits, superseded Edge/Link decompositions, historical phase plans, and model-era architecture narratives do not need to remain in the current cognitive path after their stable conclusions, exact evidence, and open falsifiers have been extracted.

Git provides exact archaeology. Current Research should instead contain:

```text
live question
+ current baseline
+ next falsifier
+ exact evidence refs
+ bounded experiment
```

Knowledge contains reusable conclusions. Core contains only compact responsibilities that have survived deletion and stronger-baseline tests.

## Research loop

The operational method is [`../../research/research-method-v1.json`](../../research/research-method-v1.json):

```text
observe Agent burden
→ place responsibility
→ propose minimum externalization
→ test strong simpler baseline
→ run bounded experiment
→ retain / narrow / defer / delete
→ sink proven capability into the narrowest reusable layer
```

This keeps Ordivon compatible with both weak current models and substantially stronger future Agents without rebuilding the system from the bottom every time the intelligence frontier moves.
