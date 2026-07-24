# 15 — Products, Collaboration, and Institutions

The final layer organizes Agent cognition and execution into human value.

## From chat to workspace

Chat is an effective interface for expressing open goals and feedback. Long-running work also needs visible persistent objects:

```text
Conversation
+ Goal
+ Task Graph
+ Workspace
+ Execution Timeline
+ Artifacts
+ Current Facts
```

The conversation carries semantic negotiation. The workspace carries continuity.

## Human–Agent division

People contribute values, direction, importance judgments, social meaning, and responsibility for consequences. Agents contribute large-scale reading, candidate construction, repeated execution, observation, and cross-tool coordination.

```text
human direction
+ Agent exploration
+ shared world feedback
```

## Multi-Agent patterns

- **Pipeline** — research, design, implementation, testing, integration;
- **Parallel exploration** — independent candidates from a shared base;
- **Specialist routing** — Tasks go to the best capability and context;
- **Blackboard** — Agents coordinate through shared Goals, Facts, Tasks, and Artifacts;
- **Manager–worker** — one Agent maintains global coherence while others execute subgraphs.

The value comes from real decomposability and low-cost artifact joins, not from Agent count alone.

## Organization as a computation graph

A traditional hierarchy emphasizes reporting lines. An Agent-native organization can also be represented through:

```text
Goal Graph
Task Graph
Capability Graph
Artifact Graph
Dependency Graph
```

People, models, Tools, and services dynamically bind to work based on capability, state affinity, and availability.

## Handoff and memory

A Task Capsule transfers Goal, current state, world bindings, facts, artifacts, capabilities, and next work. Organizational memory is distilled:

```text
raw events
→ artifacts
→ facts
→ knowledge
→ current system
→ core principles
```

Saving every message is not the same as preserving a usable world model.

## Feedback and evaluation

Metrics shape behaviour. Commit count, test success, speed, and cost are partial signals. Evaluation should remain connected to Goal progress, world outcome, reusable knowledge, continuity, and resource use.

Errors expose mistaken assumptions, missing abstractions, weak interfaces, and poor task boundaries. The organization learns by constructing, running, observing, and revising.

## Economic shift

As routine code and information production become cheaper, scarcity moves toward:

```text
important questions
unique data and world access
verification
trust and distribution
persistent execution infrastructure
responsibility for consequences
```

## Complete loop

```text
human value and goal
→ Agent task and effect
→ model and machine execution
→ world change
→ observation and artifact
→ organizational learning
→ revised goal
```

This closes the fourteen-layer stack from physical state to institution.
