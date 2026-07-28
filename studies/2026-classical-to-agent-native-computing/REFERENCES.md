# Primary-Source Ledger

Accessed 2026-07-29. The identifiers in this study are stable local references; publication pages and living specifications may continue to evolve.

## Classical substrate

### C01 — POSIX.1-2024 Base Definitions

- Source: The Open Group Base Specifications, Issue 8, Definitions.
- URL: <https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap03.html>
- Supports: standard meanings of process, thread, file, command, and system interfaces.
- Does not support: claims about Agent goals, model cognition, or epistemic authority.

### C02 — Linux scheduler domains

- Source: Linux Kernel documentation, Scheduler Domains.
- URL: <https://www.kernel.org/doc/html/latest/scheduler/sched-domains.html>
- Supports: CPU/runqueue load balancing and task placement are operating-system scheduling responsibilities.
- Does not support: semantic task selection or model routing.

### C03 — Linux namespaces

- Source: Linux Kernel documentation, Namespaces.
- URL: <https://www.kernel.org/doc/html/latest/admin-guide/namespaces/index.html>
- Supports: mature kernel mechanisms isolate views of system resources.
- Does not support: complete sandbox safety or Agent-specific authorization.

### C04 — SQLite atomic commit

- Source: SQLite, Atomic Commit In SQLite.
- URL: <https://www.sqlite.org/atomiccommit.html>
- Supports: all-or-none transactional writes and recovery across crashes or power loss.
- Does not support: whether stored claims are true or effects were semantically authorized.

### C05 — Git objects

- Source: Pro Git, Git Internals — Git Objects.
- URL: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>
- Supports: Git is fundamentally a content-addressable object store with stable object identity.
- Does not support: task completion, model memory, or artifact acceptance semantics.

### C06 — Kubernetes Jobs

- Source: Kubernetes documentation, Jobs.
- URL: <https://kubernetes.io/docs/concepts/workloads/controllers/job/>
- Supports: one-off tasks, Pod retries, parallel completions, success and failure policies; duplicate physical starts remain possible and applications must handle them.
- Does not support: open-ended goal interpretation or verification of model-generated plans.

### C07 — Kubernetes controllers

- Source: Kubernetes documentation, Controllers.
- URL: <https://kubernetes.io/docs/concepts/architecture/controller/>
- Supports: control loops reconcile observed state toward a declared desired state.
- Does not support: deciding what the desired state should mean under an underspecified human goal.

### C08 — Temporal durable execution

- Source: Temporal Platform documentation.
- URL: <https://docs.temporal.io/>
- Supports: durable workflow state and continuation across process, network, and infrastructure failure.
- Does not support: the claim that all task continuity is Agent-native.

### C09 — Temporal workflow lifecycle

- Source: Temporal service architecture, Workflow Lifecycle.
- URL: <https://github.com/temporalio/temporal/blob/main/docs/architecture/workflow-lifecycle.md>
- Supports: event history, durable writes, Workflow Tasks, commands, and replay-oriented lifecycle.
- Does not support: unrestricted nondeterministic decisions inside replay-safe workflow code.

## OpenAI

### A01 — Harness engineering

- Source: OpenAI, “Harness engineering: leveraging Codex in an agent-first world,” 2026-02-11.
- URL: <https://openai.com/index/harness-engineering/>
- Supports: human attention becomes scarce; repository legibility, feedback loops, testing, review, and garbage collection become central at high Agent throughput.
- Limitation: one software-engineering environment, not a universal computing specification.

### A02 — Agents SDK Agent and Runner boundary

- Source: OpenAI Agents SDK, Agents.
- URL: <https://openai.github.io/openai-agents-python/agents/>
- Supports: an Agent is a configured LLM while the Runner owns turns, tools, guardrails, handoffs, and sessions.
- Limitation: SDK design, not proof that these are universal primitives.

### A03 — Agents SDK Sessions

- Source: OpenAI Agents SDK, Sessions.
- URL: <https://openai.github.io/openai-agents-python/sessions/>
- Supports: conversation history can persist across runs, and session memory is distinct from server-managed continuation mechanisms.
- Limitation: conversational memory is not equivalent to durable task truth.

### A04 — Agents SDK Guardrails

- Source: OpenAI Agents SDK, Guardrails.
- URL: <https://openai.github.io/openai-agents-python/guardrails/>
- Supports: model input, output, and Tool calls can pass through separate pre/post checks and tripwires.
- Limitation: many built-in or hosted tools use different enforcement paths.

### A05 — Agents SDK Tracing

- Source: OpenAI Agents SDK, Tracing.
- URL: <https://openai.github.io/openai-agents-python/tracing/>
- Supports: Agent workflows generate structured traces across model turns, tools, handoffs, and guardrails.
- Limitation: trace presence does not establish correctness or fact admission.

### A06 — Harness and compute separation

- Source: OpenAI, “The next evolution of the Agents SDK,” 2026-04-15.
- URL: <https://openai.com/index/the-next-evolution-of-the-agents-sdk/>
- Supports: long-horizon Agent harnesses and native sandbox execution can be separated for security, durability, and scale.
- Limitation: product architecture can evolve and is not a general standard.

## Anthropic

### A07 — Building effective agents

- Source: Anthropic, “Building effective agents,” 2024-12-19.
- URL: <https://www.anthropic.com/engineering/building-effective-agents>
- Supports: simple composable patterns, explicit Agent–computer interfaces, measurement, and adding complexity only when it improves outcomes.
- Limitation: engineering guidance rather than a formal model.

### A08 — Context engineering

- Source: Anthropic, “Effective context engineering for AI agents,” 2025-09-29.
- URL: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Supports: context is a finite selected token state that must be curated across instructions, tools, history, and external data.
- Limitation: context-selection methods remain model- and workload-dependent.

### A09 — Long-running Agent harnesses

- Source: Anthropic, “Effective harnesses for long-running agents,” 2025-11-26.
- URL: <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
- Supports: compaction alone is insufficient; incremental progress and explicit artifacts bridge context-window and session boundaries.
- Limitation: demonstrates one harness pattern, not a universal Task schema.

### A10 — Multi-Agent research system

- Source: Anthropic, “How we built our multi-agent research system,” 2025-06-13.
- URL: <https://www.anthropic.com/engineering/multi-agent-research-system>
- Supports: open research is path-dependent; parallel Agents can add breadth but introduce coordination, evaluation, reliability, and cost tradeoffs.
- Limitation: results are strongest for breadth-first research and do not generalize automatically to tightly coupled coding work.

### A11 — Agent evaluations

- Source: Anthropic, “Demystifying evals for AI agents,” 2026-01-09.
- URL: <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- Supports: multi-turn agents modify environments and require grading strategies matched to trajectory and outcome complexity.
- Limitation: evaluation does not itself confer operational authority.

### A12 — Managed Agents and stale harness assumptions

- Source: Anthropic, “Scaling Managed Agents: Decoupling the brain from the hands,” 2026-04-08.
- URL: <https://www.anthropic.com/engineering/managed-agents>
- Supports: harness assumptions about model limitations become stale; stable interfaces should survive model and harness replacement.
- Limitation: hosted-service architecture is not a universal decomposition.

### A13 — Agent containment

- Source: Anthropic, “How we contain Claude across products,” 2026-05-25.
- URL: <https://www.anthropic.com/engineering/how-we-contain-claude>
- Supports: probabilistic safeguards cannot stand alone; sandbox, VM, filesystem, credential, and egress boundaries cap blast radius. Mature classical isolation remains valuable.
- Limitation: specific incidents and product architectures should not be generalized without preserving their threat models.

### A14 — Trustworthy agents in practice

- Source: Anthropic, “Trustworthy agents in practice,” 2026.
- URL: <https://www.anthropic.com/research/trustworthy-agents>
- Supports: an Agent directs its own process and Tool use in a plan–act–observe–adjust loop, with human control and transparency remaining system concerns.
- Limitation: normative product principles, not an executable protocol.

## Agent protocols

### P01 — MCP architecture

- Source: Model Context Protocol specification, Architecture, revision 2025-06-18.
- URL: <https://modelcontextprotocol.io/specification/2025-06-18/architecture>
- Supports: Host, Client, and Server separation; capability negotiation; servers expose focused resources, prompts, and tools while Hosts retain orchestration and user authorization responsibilities.
- Limitation: MCP does not define a complete Agent Host or task semantics.

### P02 — MCP Tasks

- Source: Model Context Protocol specification, Tasks, revision 2025-11-25.
- URL: <https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks>
- Supports: experimental durable handles for deferred request execution and result retrieval.
- Limitation: a request-wrapping task state machine is not necessarily a durable open-ended Goal or epistemic work model.

### P03 — A2A announcement and design

- Source: Google Developers Blog, “Announcing the Agent2Agent Protocol,” 2025-04-09.
- URL: <https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/>
- Supports: heterogeneous Agent discovery, task lifecycle, artifacts, messages, and long-running interaction are interoperability concerns.
- Limitation: protocol interoperability does not solve local task truth, authority, or verification policy.

### P04 — A2A specification

- Source: Agent2Agent Protocol specification v0.2.0.
- URL: <https://a2a-protocol.org/v0.2.0/specification/>
- Supports: Agent Card, Message, Task, Part, and Artifact wire concepts.
- Limitation: wire objects do not imply a universal internal Agent kernel.


## Current protocol revision

### P05 — MCP 2026-07-28 release candidate

- Source: Model Context Protocol Blog, “The 2026-07-28 MCP Specification Release Candidate,” 2026-05-21.
- URL: <https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/>
- Supports: the protocol core becomes stateless; explicit application handles replace protocol-session truth; extensions mature independently; Tasks move out of the Core; conformance scenarios and deprecation become governance requirements.
- Limitation: release-candidate architecture and production feedback do not prove that MCP objects should become Ordivon internal authorities.

## External runtimes and research systems

### R01 — LangGraph persistence

- Source: LangChain documentation, “Persistence.”
- URL: <https://docs.langchain.com/oss/python/langgraph/persistence>
- Supports: thread identity, checkpoints, pending writes, replay, time travel, fault tolerance, and durable human interruption are available in a mature Agent orchestration runtime.
- Limitation: arbitrary graph state does not by itself prove or disprove a separate open-work semantic layer.

### R02 — LangGraph human-in-the-loop

- Source: LangChain documentation, “Human-in-the-loop.”
- URL: <https://docs.langchain.com/oss/python/langchain/human-in-the-loop>
- Supports: Tool calls can be interrupted, persisted, approved, edited, rejected, and resumed under policy.
- Limitation: an approval interrupt does not establish optimal operator-attention scheduling or consequence-bound authority.

### R03 — OpenHands platform

- Source: Wang et al., “OpenHands: An Open Platform for AI Software Developers as Generalist Agents,” arXiv:2407.16741, 2024.
- URL: <https://arxiv.org/abs/2407.16741>
- Supports: general software Agents combine code, command-line and browser interaction, sandboxed execution, coordination, and environment-based benchmarks.
- Limitation: one platform architecture does not establish universal Agent-native primitives.

### R04 — MemGPT

- Source: Packer et al., “MemGPT: Towards LLMs as Operating Systems,” arXiv:2310.08560, 2023.
- URL: <https://arxiv.org/abs/2310.08560>
- Supports: virtual-context and memory-tier analogies predate Ordivon and address long-context and multi-session continuity.
- Limitation: operating-system analogy and memory management do not define Effect authority, external commitment, or domain verification.

### R05 — OpenHands Software Agent SDK

- Source: Wang et al., “The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents,” arXiv:2511.03690, 2025.
- URL: <https://arxiv.org/abs/2511.03690>
- Supports: production Agent systems can compose sandbox execution, lifecycle control, model routing, security analysis, and multiple interaction surfaces.
- Limitation: claimed platform completeness does not remove the need for workload-specific comparison or justify duplicating its components.

### R06 — LangGraph Functional API

- Source: LangChain documentation, “Functional API overview.”
- URL: <https://docs.langchain.com/oss/python/langgraph/functional-api>
- Supports: durable Agent execution need not be represented only as an explicit DAG; ordinary functions, tasks, futures, retries, and checkpoints can coexist.
- Limitation: availability of a functional API does not determine the best semantic projection for Ordivon Task readiness.
