# Probabilistic Work Control Loop

## Model output is a proposal

A model is useful because it can interpret, infer, plan, compare, and generate under incomplete context. Those outputs are not automatically durable system state.

```text
model output
≠ authorized Effect
≠ external Observation
≠ accepted Fact
≠ completed Task
```

The surrounding Host and Runtime convert useful proposals into controlled work.

## Loop

```text
Goal
→ bind current world
→ compile bounded context
→ invoke model or other cognitive worker
→ receive candidate plan, claim, or action
→ apply structural and authority admission
→ bind one Effect to one Tool contract
→ dispatch through classical execution
→ retain Observation and Artifact evidence
→ verify Claims and update work state
→ continue, branch, wait, complete, or escalate
```

Each arrow is a boundary where identity or meaning can be lost.

## Why context is a system object

Durable state can exceed the model's usable context. The system chooses a working set from instructions, task state, source versions, facts, claims, Tool catalogs, and Artifacts.

Context should therefore be bound to:

- source identities and revisions;
- policy and Tool-catalog versions;
- selection or compression method;
- invalidation conditions;
- the resulting model invocation.

The exact retrieval algorithm may change. The stable responsibility is that critical authority and execution history do not exist only because they remain in the prompt.

## Why the Task outlives the run

A process, provider session, or Agent run is one execution episode. Open work can survive:

- failed Attempts;
- model or provider replacement;
- context reset;
- Host or Runtime restart;
- world drift;
- revised hypotheses;
- human redirection.

The durable Task state preserves current semantic work, not an unfiltered transcript.

## Why effects need commitment semantics

A candidate action becomes a durable Effect only after it is bound to current world and authority.

```text
Effect
  stable intended observation or change

Dispatch
  one physical attempt to cross the boundary

backend Job
  execution object owned by the concrete substrate
```

A lost response produces uncertainty. It does not prove failure. Stable Effect identity allows reconciliation without allowing a new model episode to invent what physically happened.

## Why the loop remains hybrid

The model provides flexible probabilistic search over possible next steps. Deterministic mechanisms preserve identity, authority, physical effects, and evidence. Removing either side loses the main benefit:

```text
fixed workflow only
  reliable but cannot revise open paths freely

model loop only
  flexible but cannot establish durable reality safely

hybrid control loop
  flexible proposal inside persistent commitment and evidence
```

See [`task-context-authority-effect-evidence.md`](task-context-authority-effect-evidence.md) and [`capability-externalization-and-responsibility-placement.md`](capability-externalization-and-responsibility-placement.md).
