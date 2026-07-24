# Human–Agent Products and Organization

The final layer of the stack turns Agent cognition and execution into sustained human value.

## Product objects

A chat message is an effective entry point for open goals, but long-running work needs visible persistent objects:

```text
Conversation
+ Goal
+ Task Graph
+ Workspace
+ Execution Timeline
+ Artifacts
+ Current Facts
```

Conversation carries meaning and negotiation. The workspace carries continuing work.

## Human and Agent strengths

People contribute direction, values, social context, importance judgments, and responsibility for consequences. Agents contribute high-throughput reading, candidate generation, repeated execution, cross-tool coordination, and continuous observation.

The useful division is not “human commands, Agent obeys,” but:

```text
human direction and meaning
+ Agent exploration and execution
+ shared feedback from reality
```

## Multi-Agent collaboration

Multiple Agents create value when the Task Graph contains real independent structure and results can be joined through stable artifacts. Common patterns include:

- pipelines across research, implementation, testing, and integration;
- parallel candidate exploration in isolated workspaces;
- specialist routing by task capability;
- a shared blackboard of Goals, Tasks, Facts, and Artifacts;
- manager–worker decomposition for coherent large goals.

A join is not merely waiting for several messages. It is a state-reduction step that combines independently produced artifacts into a new task context.

## Handoff and institutional memory

A Task Capsule can transfer:

```text
Goal
current state
world bindings
verified facts
relevant artifacts
available capabilities
next ready work
```

This is more useful than transferring an unfiltered conversation history.

Organizational memory grows through layers:

```text
raw events
→ artifacts
→ facts
→ reusable knowledge
→ current system models
→ core principles
```

## Feedback and evaluation

What a system measures shapes Agent behaviour. Local metrics such as number of commits or tests passed are useful signals but do not fully represent Goal progress. Evaluation should remain connected to actual world outcomes, reusable knowledge, continuity, and resource cost.

Errors are organizational learning inputs. Repeated friction can reveal an incorrect world model, a missing abstraction, a poor task boundary, or a weak interface.

## Economic implication

As code and information production become less scarce, value shifts toward:

- selecting meaningful problems;
- unique data and world access;
- reliable verification;
- user trust and distribution;
- stateful execution networks;
- responsibility for long-term consequences.

Agent-native organizations therefore coordinate Goals, capabilities, execution, artifacts, and feedback rather than only fixed reporting lines.

See the [products and institutions study](../../studies/2026-computing-stack-walkthrough/15-products-and-institutions.md).
