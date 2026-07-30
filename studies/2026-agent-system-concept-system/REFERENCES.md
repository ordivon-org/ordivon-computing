# References

Primary and mature implementation sources reviewed for this study. Retrieved 2026-07-30 unless otherwise stated.

## Agent Harnesses and products

- OpenAI, “Unrolling the Codex agent loop.” 2026-01-23. https://openai.com/index/unrolling-the-codex-agent-loop/
- OpenAI, “Unlocking the Codex harness: how we built the App Server.” 2026-02-04. https://openai.com/index/unlocking-the-codex-harness/
- OpenAI, “Harness engineering: leveraging Codex in an agent-first world.” 2026. https://openai.com/index/harness-engineering/
- OpenAI Agents SDK documentation. https://openai.github.io/openai-agents-python/
- OpenAI Agents SDK lifecycle hooks. https://openai.github.io/openai-agents-python/ref/lifecycle/
- OpenAI Agents SDK tracing. https://openai.github.io/openai-agents-python/tracing/
- OpenAI Agents SDK handoffs. https://openai.github.io/openai-agents-python/handoffs/
- Anthropic, Claude Code documentation. https://code.claude.com/docs/en/overview
- Anthropic, Claude Code Hooks reference. https://code.claude.com/docs/en/hooks
- Anthropic, Claude Code feature overview. https://code.claude.com/docs/en/features-overview
- Anthropic, Claude Agent SDK overview. https://platform.claude.com/docs/en/agent-sdk/overview

## Protocols and capability negotiation

- Model Context Protocol, Lifecycle specification. https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle
- Model Context Protocol specification index. https://modelcontextprotocol.io/specification/

## Durable workflows and distributed control

- Temporal documentation. https://docs.temporal.io/
- Temporal Python message passing. https://docs.temporal.io/develop/python/message-passing
- Kubernetes, Leases. https://kubernetes.io/docs/concepts/architecture/leases/
- Kubernetes, Operator pattern. https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
- Kubernetes, Coordinated Leader Election. https://kubernetes.io/docs/concepts/cluster-administration/coordinated-leader-election/

## Graph execution and persistence

- LangGraph, Persistence. https://docs.langchain.com/oss/python/langgraph/persistence
- LangGraph, Interrupts. https://docs.langchain.com/oss/python/langgraph/interrupts
- LangGraph, Time travel. https://docs.langchain.com/oss/python/langgraph/use-time-travel

## Observability

- OpenTelemetry Semantic Conventions. https://opentelemetry.io/docs/specs/semconv/
- OpenTelemetry, General Semantic Conventions. https://opentelemetry.io/docs/specs/semconv/general/
- OpenTelemetry, “Inside the LLM Call: GenAI Observability with OpenTelemetry.” 2026. https://opentelemetry.io/blog/2026/genai-observability/

## Ordivon internal evidence

- [`../../core/stack.md`](../../core/stack.md) — classical substrate and Agent-native responsibility overlay.
- [`../../core/primitives.md`](../../core/primitives.md) — current primitive and ownership boundaries.
- [`../../knowledge/agents/goal-task-effect.md`](../../knowledge/agents/goal-task-effect.md) — Goal, Task, Attempt, Context, ActionProposal, Effect, and Dispatch.
- [`../../knowledge/agents/execution-kernel.md`](../../knowledge/agents/execution-kernel.md) — execution and recovery responsibilities.
- [`../../knowledge/agents/tool-contracts-and-world-interfaces.md`](../../knowledge/agents/tool-contracts-and-world-interfaces.md) — Tool Contract and external-world boundaries.
- [`../../research/experiments/semantic-core-v0/`](../../research/experiments/semantic-core-v0/) — closed semantic commitment experiment.
- [`../../research/experiments/task-continuation-v0/`](../../research/experiments/task-continuation-v0/) — model replacement and Task continuation evidence.
- [`../../research/experiments/external-semantic-contract-v0/`](../../research/experiments/external-semantic-contract-v0/) — Effect IR, Tool Contract, Binding, and backend portability evidence.

## Interpretation rule

References establish mature mechanisms and product boundaries. They do not by themselves validate an Ordivon abstraction. Promotion still requires real Ordivon workloads, equal-budget comparison, failure injection, cost measurement, and deletion tests.
