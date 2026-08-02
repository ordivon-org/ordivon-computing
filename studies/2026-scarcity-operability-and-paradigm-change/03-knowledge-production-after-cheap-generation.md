# Knowledge Production After Cheap Generation

## 1. The minimal research system

Independent of universities, journals, and current professional roles, research requires a loop:

```text
unknown or anomaly
→ question
→ candidate explanation, construction, or intervention
→ derivation or execution
→ evidence, proof, or counterexample
→ revision
→ integration into reusable state
```

Four capacities constrain the loop:

- **generation** — hypotheses, proofs, algorithms, experiments, and connections;
- **validation** — criticism, proof checking, replication, counterexamples, and attribution;
- **execution** — computation, simulation, laboratory work, and world interaction;
- **integration** — deciding what becomes accepted knowledge, a maintained tool, or a new question.

Agentic systems are increasing generation most rapidly, and are beginning to assist the other three capacities [O01] [O04] [G01].

## 2. Why mathematics and code move first

A domain accelerates when it has a cheap, informative evaluation loop.

Mathematics can sometimes use:

```text
candidate argument
→ formal representation
→ proof-kernel check
→ localized failure
→ revision
```

Algorithm discovery can use:

```text
candidate program
→ execute
→ score
→ retain high-performing variants
→ generate new variants
```

AlphaEvolve explicitly combines model generation, automated evaluators, a program database, and evolutionary selection [G01]. OpenAI's reported mathematics workflow adds manuscript preparation and Lean certification after model-generated arguments [O01].

These loops do not solve novelty, faithful problem formulation, explanatory value, attribution, or community adoption. They make one important class of failure cheaper to detect.

## 3. Empirical science exposes the validation bottleneck

In empirical domains, a high-scoring candidate remains a lead until it survives contact with the world. Physical facilities, sample preparation, replication, ethics, and institutional review remain limited. DeepMind therefore characterizes Agents as conjecture machines while validation remains slow and costly [G02].

The expected pipeline becomes increasingly selective:

```text
large candidate population
→ model and literature screening
→ simulation or proxy evaluation
→ limited physical experiments
→ replication and integration
```

The strategic question moves from `Can we generate an idea?` to `Which experiment has the highest expected information value under limited reality access?`

## 4. The paper becomes a view, not the full state

A paper is optimized for human review, citation, and stable communication. It usually excludes most failed attempts, branch history, intermediate artifacts, and changing hypotheses.

A richer research object may include:

```text
Question
Claim
Attempt
Evidence
Counterexample
Evaluator
Decision
Artifact
Attribution
Open branch
```

The paper can then be treated as:

```text
Publication = Projection(Research State, Audience, Purpose, Time)
```

Other projections may be:

- a formal proof package;
- an experiment report;
- a public article;
- an implementation Issue;
- a negative result;
- an evaluator dataset;
- a compact continuation state for another Agent.

This is a conceptual direction, not a decision to build a universal research-object platform.

## 5. The new admission boundary

When output volume rises, the critical knowledge-system operation becomes admission:

```text
model output
≠ accepted claim
≠ verified fact
≠ important result
≠ maintained capability
```

A robust system preserves these distinctions and the evidence connecting them.

Useful admission questions include:

- What exact claim is being made?
- Which source, proof, test, or observation supports it?
- What would falsify it?
- Is the result novel or independently rediscovered?
- Does the evaluator measure the property that matters?
- Which participant accepts responsibility for downstream use?
- Can the claim be revised or withdrawn without corrupting unrelated state?

## 6. Effective intelligence becomes infrastructural

The ARC-AGI-3 result shows that context retention and compaction materially alter realized capability [O03]. Scientific-software cases show that experts' specification, tests, and stewardship determine whether fast implementation becomes durable scientific value [O02].

Therefore research capability is increasingly a property of an assembled system:

```text
C_effective = f(Model, Harness, State, Tools, Evaluators, World, Budgets)
```

The function is not assumed to be literal multiplication. The key point is complementarity: a severe weakness in one component can suppress the value of the others.

## 7. Resulting design pressure

A post-scarcity-generation knowledge system should favor:

- cheap candidate creation;
- explicit separation between proposal and admission;
- independent verification where possible;
- preserved failed attempts when they reduce repeated work;
- branch allocation based on expected information gain;
- provenance and attribution;
- replaceable cognition over durable research state;
- publication generated from evidence-backed state rather than treated as the state itself.

These pressures help explain Ordivon's existing direction, examined next.
