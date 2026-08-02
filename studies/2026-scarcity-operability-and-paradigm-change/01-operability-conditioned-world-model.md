# An Operability-Conditioned World Model

## 1. Reality and the usable model are different objects

Let `X` denote the possible states of the relevant world. A concrete participant never has direct, complete access to `X`. It has a bounded capability set at time `t`:

```text
Pi_t = available observations, inferences, memory, coordination,
actions, and recovery operations.
```

Define two states as operationally equivalent for that participant when no currently available procedure can distinguish them in a way that changes an admissible decision or outcome:

```text
x ~_t y
```

The participant therefore operates on a compressed effective space:

```text
X / ~_t
```

This is not a claim that unobserved distinctions are unreal. It says that they are not yet represented as usable degrees of freedom in the participant's current action system.

## 2. Capability growth refines the partition

When capability expands:

```text
Pi_t is contained in Pi_(t+1)
```

some states that were previously indistinguishable become distinguishable. The effective partition becomes finer.

Examples:

- microscopy made microorganisms operational variables in medicine;
- cheap computation made high-dimensional simulation usable in engineering;
- version control and snapshots made destructive software exploration recoverable;
- Agents make more repository branches, candidate implementations, and research routes affordable;
- durable state and compaction make long-horizon cognition materially different from repeated stateless calls [O03].

The new dimension was not necessarily created by the tool. The tool made the distinction observable and actionable at sustainable cost.

## 3. Higher-dimensional does not mean more complicated by default

A higher-dimensional representation preserves distinctions that a lower-dimensional representation collapses.

Examples of low-dimensional compression:

```text
one Task → one next step
one project → one owner
one run → success or failure
one research effort → one paper
one Agent → one transcript
one safety decision → allow or deny
```

Possible refinements include:

```text
one Task → a Ready Frontier of admissible branches
one project → changing participants, dependencies, and commitments
one run → trajectory, environment, artifacts, uncertainty, and consequence
one research effort → claims, attempts, evidence, counterexamples, and open branches
one Agent → replaceable cognition over durable Task state
one safety decision → reversible exploration plus a narrow consequence boundary
```

The refined representation is justified only when preserving the added dimensions improves decisions or recovery more than it adds maintenance and cognitive cost.

## 4. Three kinds of constraint

This lens separates constraints that are often mixed together.

### Hard constraints

These arise from physical, logical, or externally enforced reality:

- finite energy and compute;
- irreversible time;
- physical damage;
- mathematical inconsistency;
- third-party ownership;
- legal and financial commitment;
- adversarial action;
- unique data loss.

Capability can sometimes reduce their cost but cannot make them disappear by declaration.

### Soft technical constraints

These arise from current implementation capability:

- slow code generation;
- expensive environment reconstruction;
- weak observability;
- limited context retention;
- high integration friction;
- inability to compare many branches.

They can change rapidly and should not be frozen into permanent architecture without evidence.

### Institutionalized historical constraints

These are rules, roles, and concepts created to manage earlier hard or soft constraints:

- approval chains;
- fixed reporting structures;
- document rituals;
- compatibility obligations without active consumers;
- permanent ownership boundaries inherited from an earlier implementation topology.

They may still be useful. Their origin no longer proves their current value.

## 5. Operability is participant-relative and purpose-relative

Two participants may inhabit different effective spaces because they have different:

- Tools and credentials;
- memory and Context;
- models and expertise;
- legal authority;
- recovery mechanisms;
- risk exposure;
- purposes.

A cloud provider, a solo developer, a public institution, and an autonomous laboratory do not share the same useful abstraction boundary.

Therefore this study does not derive one universal organizational form. It derives a recurring audit question:

> Which distinctions are currently actionable for this participant, under this purpose, with this consequence and recovery structure?

## 6. Epistemic caution

Increasing operability can reveal structure and also create systematic blindness:

- an evaluator exposes measurable dimensions but can hide unmeasured value;
- a knowledge graph preserves relations but can encourage false ontological confidence;
- a formal proof certifies derivation under definitions but not importance, novelty, or faithful problem formulation;
- large-scale search finds high-scoring candidates but may exploit the scoring function;
- Agent-generated output can increase both useful results and plausible error volume.

Higher operational resolution is not identical to truth. It is a larger intervention and observation surface that still requires judgment and independent evidence.
