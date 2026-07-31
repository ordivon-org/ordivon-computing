# Industry Reference Map

## 1. Reading rule

Top AI companies use the word **Harness** at different product boundaries. The comparison therefore maps responsibilities rather than relying on names.

A product can combine several logical layers in one binary or service without invalidating the separation:

```text
Surface + interaction Host + Agent Harness + Session + Tool adapters + sandbox
```

Ordivon uses the separation to decide what must survive replacement, not to prescribe company org charts.

## 2. OpenAI Codex

OpenAI describes the Codex Harness as the orchestration around user input, model calls, and Tools. Codex CLI, IDE, Web, and App reuse the same core Harness. App Server exposes the Harness through a bidirectional JSON-RPC protocol with Thread, Turn, and Item events.

### What the OpenAI design demonstrates

- the model and the Agent Loop are separate products of engineering;
- Tool definitions, prompts, Session state, sandbox behavior, and event protocols materially influence model performance;
- one internal Harness can support multiple Surfaces;
- a Provider-specific protocol can preserve richer behavior than a lowest-common-denominator cross-provider protocol;
- Agent Run state can be product-local while a higher system still owns durable work.

### Ordivon implication

Codex should remain a provider-faithful external Harness backend. Ordivon should not reproduce Thread/Turn/Item semantics merely to call Codex. It should bind Codex Runs to Host Assignments and Runtime evidence.

## 3. Anthropic Claude and long-running agents

Anthropic's engineering material distinguishes a model from the surrounding long-running work structure. Its initializer/coding-agent pattern leaves explicit files and progress state for later contexts. Later work describes planner, generator, and evaluator roles, structured handoffs, and workload decomposition. Anthropic repeatedly notes that Harness assumptions should be revisited as models improve.

The parallel C-compiler experiment used many Claude sessions under an external coordination system, demonstrating that long-duration capability depends on decomposition, shared repository state, testing, and explicit coordination—not one uninterrupted conversation.

### What the Anthropic design demonstrates

- compaction alone is not a reliable long-term work database;
- explicit Artifacts and environment state can carry work across contexts;
- evaluator separation can improve result quality without giving the model completion authority;
- workload-specific Harness design can be useful without becoming a universal platform;
- Harness complexity should be ablated as model capability changes.

### Ordivon implication

Ordivon's Artifact-first continuity and independent verification align with the strongest lessons. Ordivon should preserve the ability to use Claude's mature Harness while retaining Task truth above it.

## 4. Microsoft Agent Framework

Microsoft publicly separates model clients, Agents, a batteries-included Harness, explicit Workflows, and Hosting. The Harness includes the model/Tool loop, context persistence and compaction, planning and Todo support, file memory/access, approvals, observability, and optional background Agents or shell. Workflows provide explicit graph control for deterministic multi-step processes.

### What the Microsoft design demonstrates

- Agent Loop and explicit workflow graph are distinct abstractions;
- a Harness can wrap different model clients because it owns the loop;
- Session state can persist planning and history without becoming application Task truth;
- enterprise framework goals justify a broader abstraction surface than a personal thin-core system;
- the simplest pattern should be selected when it suffices.

### Ordivon implication

Ordivon Harness can wrap bare model clients, but it does not need Microsoft-scale middleware, workflow, memory, or hosting scope. Host already owns the durable graph and Runtime owns execution.

## 5. Google ADK and Vertex AI Agent Engine

Google exposes an Agent development framework and a managed deployment platform with Runtime, Sessions, Memory Bank, evaluation, observability, and code execution. ADK also supports explicit graph workflows because deterministic application flow cannot always be delegated to probabilistic orchestration.

### What the Google design demonstrates

- Agent framework, managed Runtime, Session, memory, evaluation, and observability can be independently deployable services;
- model-level flexibility and deterministic workflow control coexist;
- a managed platform may host responsibilities that remain logically distinct;
- graph control becomes useful when application sequencing must be explicit.

### Ordivon implication

Ordivon should continue separating logical ownership even when components are colocated. A future deployment may move parts into cloud services without moving Task authority into the model or physical execution truth into Host.

## 6. Comparison matrix

| Logical responsibility | OpenAI Codex | Anthropic examples | Microsoft Agent Framework | Google ADK / Agent Engine | Ordivon decision |
|---|---|---|---|---|---|
| Model invocation | OpenAI models | Claude API/models | model clients | Gemini/other model adapters | Model Adapter or external Harness |
| Agent Loop | Codex Harness | Claude Code/Agent SDK and experiment harnesses | Harness | ADK agents | Ordivon Harness for bare models; external direct drivers otherwise |
| Provider Session | Thread | Claude/SDK Session | Agent Session | Session service | Harness-local evidence, not Task identity |
| Explicit workflow | product orchestration | workload-specific loops | Workflows | graph workflows | Host Task graph / owning application |
| Tool execution | Codex Tools/sandbox | Claude Tools/environment | Harness Tools | Tools/code execution | Runtime or external provider, linked by Tool Bridge |
| Durable Task truth | product-specific | explicit files/workload state | application/workflow state | application/session services | Ordivon Host |
| Physical process truth | Codex sandbox | execution environment | hosting/tool backend | Agent Engine/code execution | Ordivon Runtime |
| Evaluation | product tests/evals | planner/generator/evaluator | observability/evaluation integrations | evaluation service | independent verifier + Host decision |
| Cross-provider continuity | not Provider objective | not Provider objective | framework abstraction | platform abstraction | explicit Host responsibility |

## 7. Shared conclusion

The industry does not provide evidence that Harness is optional. It provides evidence that:

1. a model requires an Agent Loop before it can iteratively use Tools;
2. the quality of the Loop, Context, Tools, and evaluation materially affects useful capability;
3. long-running work needs explicit state outside a single model context;
4. deterministic workflow and physical execution remain distinct from probabilistic cognition;
5. product packaging varies, so ownership must be derived from failure and replacement boundaries.

Ordivon's distinctive insertion point is not a competing universal Agent framework. It is the combination of:

```text
first-party thin Harness when only intelligence is supplied
+ direct use of mature Provider Harnesses when available
+ Host-owned durable work continuity
+ Runtime-owned physical evidence
```
