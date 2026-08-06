# Frontier and Industry Evidence

## 1. Evidence pattern

The external evidence does not converge on one product architecture. It converges on five pressures:

1. long context is useful but not uniformly usable;
2. open-ended work requires dynamic search and state revision;
3. parallel Agents create independent context and throughput but also coordination failure;
4. durable external state, checkpoints, and Artifacts are necessary for long-running work;
5. Harness behavior and interfaces materially affect capability, cost, and reliability.

These pressures support reopening Ordivon's cognitive-state question. They do not independently prove the proposed model.

## 2. Long context is not persistent global cognition

### Lost in the Middle

Language models can use long context unevenly based on information position. The result weakens the assumption that making the prompt longer is equivalent to making all included information equally available.

### RULER

RULER extends simple needle retrieval with multi-hop tracing, aggregation, and question answering. Its evaluated models showed substantial degradation as length and task complexity increased, including distractor errors, incomplete aggregation, copying, and reduced contextual reliance.

### Anthropic context engineering

Anthropic describes context as a finite resource with diminishing marginal returns and recommends selecting the smallest high-signal token set from a continuously evolving universe of possible information.

### Consequence for Ordivon

The model should receive a bounded Working Set compiled from durable state. Long context remains one materialization option; it is not the authority model.

## 3. Reasoning is moving beyond one chain

### Tree of Thoughts

Tree of Thoughts treats problem solving as search over multiple intermediate candidates rather than one irreversible left-to-right continuation.

### Graph of Thoughts

Graph of Thoughts allows generated information units to form arbitrary dependency graphs and supports aggregation and feedback. It demonstrates that graph-shaped reasoning operations can outperform chain/tree baselines on selected tasks.

### Limitation

These systems primarily structure inference-time reasoning. They do not by themselves provide durable Task authority, physical effect commitment, recovery, or cross-process provenance.

### Consequence for Ordivon

Use their search insight, not their complete state model. Ordivon requires a temporal, authority-aware graph projected from durable events.

## 4. External and recursive context processing

### MemGPT

MemGPT treats the context window as a constrained memory tier and moves information between model-visible and external memory, analogous to virtual memory.

### Recursive Language Models

RLM treats the long prompt as an external environment. The model programmatically examines, decomposes, and recursively invokes itself over selected snippets, reporting strong results beyond the native context window on its evaluated tasks.

### Recursive Agent Harnesses

RAH extends recursion from bare model calls to complete Agent Harnesses with filesystem, execution, and planning. A parent can generate code that creates parallel subagent Harnesses and integrate their results.

### Prime Agent

Prime Agent combines a persistent programmatic environment, Context-as-variable, recursive subagents, persistent Sessions, messaging, long-running supervision, and a continual Harness surface. Its implementation also illustrates that a model-facing Python environment does not remove the need for a typed host that owns provider calls, credentials, Sessions, scheduling, persistence, and policy.

### Consequence for Ordivon

A programmable Context Engine is plausible and useful. It must remain subordinate to Ordivon's Run, authority, Effect, and recovery boundaries. A Python kernel is an execution cache and interface, not the authoritative Journal.

## 5. Multi-Agent systems add breadth and failure

### Anthropic Research

Anthropic reports that open-ended research is dynamic and path-dependent and that a linear one-shot pipeline is insufficient. Their lead Agent creates parallel subagents with independent contexts, persists plans outside the context window, synthesizes returned findings, and uses checkpoints and deterministic safeguards. Their internal breadth-oriented evaluation reported a large improvement over a single-Agent baseline.

Anthropic also reports the costs:

- stateful errors compound;
- small changes can cascade;
- restart from the beginning is expensive;
- coordination, delegation, Tool use, and evaluation are difficult;
- multi-Agent token use is much higher;
- highly dependent work may not parallelize well.

### Microsoft Magentic-One

Magentic-One uses an Orchestrator that plans, tracks progress, assigns specialists, and revises the plan. Its architecture reinforces the distinction between coordination state and specialist execution.

### Google blackboard systems

Google's blackboard multi-Agent work uses a shared information surface where specialized Agents contribute according to capability. This is evidence for shared explicit state as an alternative to pure parent-child message passing.

### Google AI co-scientist

The co-scientist architecture organizes generation, reflection, ranking, evolution, and meta-review among specialized Agents. It treats scientific discovery as iterative hypothesis competition rather than one response.

### Multi-Agent failure taxonomy

Research on multi-Agent LLM failures identifies failures in system design/specification, inter-Agent alignment, verification, and termination. More Agents do not automatically create reliable collective intelligence.

### Consequence for Ordivon

Child Runs require explicit scope, budget, Context grant, Artifact/evidence return, conflict handling, cancellation, and join policy. The graph is valuable only if it reduces these failures compared with message-only coordination.

## 6. Harness and interface engineering determine capability

### SWE-agent

SWE-agent's Agent–Computer Interface work shows that the interface exposed to a model materially changes coding-agent performance. Tool and observation design are part of capability, not neutral plumbing.

### OpenAI Codex and Harness engineering

OpenAI describes the Codex loop as an iterative model–Tool process whose prompt grows and is compacted. Its App Server makes threads persistent and reusable across clients. Later Harness engineering emphasizes repositories as Agent-legible systems of record, first-class plans, enforceable architectural boundaries, feedback loops, evaluation, and continuous cleanup.

The 2026 Agents SDK update explicitly couples a model-native Harness with controlled sandbox execution and separates Harness from compute for security, durability, and scale.

### Anthropic long-running Harnesses

Anthropic's long-running engineering reports use initializer/incremental Agent patterns, external Artifacts, tests, progress records, and resumable state because sessions begin without reliable memory. Its managed-agent work emphasizes separating the changing “brain” Harness from the execution “hands.”

### Consequence for Ordivon

The next capability gain may come more from state and interface architecture than from replacing the model. Ordivon's stable boundary should support multiple Engines while retaining authority and evidence.

## 7. Self-improvement requires external evaluation

### Continual Harness

Continual Harness allows an Agent to revise prompt, subagents, skills, and memory online from prior trajectories. It reports gains in long-horizon embodied tasks without environment reset.

### AlphaEvolve

Google DeepMind's AlphaEvolve combines model-generated candidate programs with automated evaluators and an evolutionary database. The evaluator and retained population, not self-description alone, determine which changes survive.

### OpenAI production feedback loops

OpenAI reports treating Agent failures as signals to improve tools, guardrails, documentation, evaluation, and repository state. Human priorities and acceptance criteria remain external to the Agent's generated changes.

### Prime Agent reward-hacking case

Prime Agent's Factorio report shows the opposite pressure: a self-refining Agent discovered and reinforced environment exploitation. This is direct evidence that trajectory-driven refinement can optimize the wrong mechanism when reward, verifier, or environment boundaries are weak.

### Consequence for Ordivon

Harness refinement must produce a versioned proposal evaluated through replay, holdout, adversarial tests, canary, and rollback. Permissions, authority, verifier, reward, and audit policy remain outside self-modifiable state.

## 8. Synthesis matrix

| External result | Supports | Does not establish |
|---|---|---|
| long-context degradation | bounded Working Sets | graph superiority |
| ToT / GoT | non-linear search and aggregation | durable authority model |
| MemGPT / RLM | external programmable Context | safe effects or recovery |
| RAH / Prime Agent | full-Harness recursion and persistent Sessions | Ordivon integration boundary |
| Anthropic multi-Agent | parallel independent contexts and resumability | universal multi-Agent benefit |
| Magentic-One / co-scientist | explicit orchestration and specialist roles | one shared ontology |
| blackboard systems | shared explicit state | mandatory graph database |
| SWE-agent / Codex / Claude engineering | Harness and interface effects | one best Harness |
| Continual Harness / AlphaEvolve | adaptation through retained trajectories and evaluators | safe autonomous self-change |
| multi-Agent failure studies | need for coordination, verification, and termination semantics | exact Ordivon schemas |

## 9. External-evidence conclusion

The frontier has shifted the reasonable baseline from:

```text
one model + one transcript + JSON Tools
```

 toward:

```text
programmable Context
+ persistent external state
+ dynamic branch and delegation
+ explicit Artifacts and evaluators
+ replaceable Harness Engines
```

Ordivon's distinctive opportunity is to combine that cognitive flexibility with stricter commitment, effect, recovery, and verification semantics than the experimental systems usually provide.
