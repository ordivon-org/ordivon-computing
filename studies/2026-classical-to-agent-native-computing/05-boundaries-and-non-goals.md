# Boundaries, Non-Goals, and the Implementation Threshold

## 1. Research scope is wider than implementation scope

Ordivon can study any layer of computing: chips, memory, operating systems, storage, networks, model architectures, organizations, and future machine contracts. Research can reveal constraints and inspire simulations without obligating the series to own production implementations.

```text
researchable
≠ Agent-changed
≠ Ordivon responsibility
≠ immediate repository
```

These four decisions must remain separate.

## 2. Default inheritance rule

Ordivon should inherit a mature classical mechanism when it already owns the physical or deterministic invariant and can be composed through a stable boundary.

Default inherited layers include:

- commodity CPU, GPU, memory, storage, and networking hardware;
- UEFI, Linux, Windows, and WSL;
- process, thread, filesystem, namespace, and scheduler mechanisms;
- containers, VMs, seccomp, cgroups, and mature sandbox components;
- SQLite, PostgreSQL, object storage, and Git;
- TLS, QUIC, DNS, SSH, WireGuard, and mature transport libraries;
- compilers, package managers, build systems, and test frameworks;
- model training and inference services;
- durable workflow systems where their programming model fits.

OpenAI's separation of long-horizon Agent harnesses from native sandbox compute illustrates the same boundary: cognition and orchestration can evolve without absorbing the isolation and execution substrate [A06].

Anthropic's containment experience provides a practical warning: mature hypervisors, syscall filters, and container runtimes often held while newly built surrounding components failed [A13]. Reimplementation increases risk unless the classical contract is demonstrably insufficient.

## 3. When a classical layer becomes a valid research target

A lower layer deserves Agent-era research when at least one condition holds:

1. the workload creates a measurable bottleneck not removable above the layer;
2. the layer's current interface hides information necessary for safe Agent control;
3. a simulated alternative can test a cross-layer hypothesis;
4. emerging hardware or model architecture changes the cost structure materially;
5. the research clarifies why an upper-layer abstraction is or is not necessary.

Examples include:

- semantic working-set placement across model context and durable state;
- data movement for long-context and multi-Agent inference;
- hardware support for verification, provenance, or isolation;
- simulated Agent-native instruction or event models;
- storage layouts for large causal and evidence graphs.

These can remain Studies or Experiments indefinitely.

## 4. When implementation is justified

A new Ordivon implementation should pass all five gates.

### Gate A — Real failure

At least one actual workload fails, becomes unsafe, or imposes repeated high friction without the mechanism.

### Gate B — Wrong owner

The missing invariant is not already the explicit responsibility of Linux, a database, a workflow engine, a protocol, or a provider.

### Gate C — Cross-workload leverage

The mechanism benefits at least two materially different paths, or one path with sustained E6 evidence and no suitable external component.

### Gate D — Non-bypassable boundary

The mechanism can be placed at a boundary where callers cannot silently bypass its guarantee.

### Gate E — Cost advantage

Building and maintaining the component has clearly greater expected value than adapting or contributing to a mature external project.

Failure at any gate keeps the idea in research or local application code.

## 5. When a new repository is justified

A conceptual responsibility does not require a repository. A repository is justified only when it has:

- independent release or deployment lifecycle;
- a stable public or cross-project contract;
- authoritative state or a distinct executable;
- separate operational failure and recovery;
- at least one real consumer;
- enough implementation to avoid becoming a document shell.

Otherwise the work belongs in:

- `ordivon-computing` research;
- an existing project's internal module;
- an experiment;
- a protocol package only after a second consumer exists.

## 6. What Ordivon should not claim

### Not a replacement operating system

Runtime owns trusted-local Effect execution above Linux. It does not own CPU scheduling, memory, filesystem, or untrusted-code isolation.

### Not a new database

Host and Runtime define semantic journals and projections. SQLite owns transactional storage. Ordivon owns the meaning and replay rules of its records.

### Not a generic durable workflow invention

Kubernetes and Temporal already preserve declared work [C06][C08]. Ordivon's distinct question is open-work semantics under probabilistic revision.

### Not a model runtime by default

Provider adapters and model invocation records do not make Ordivon a training or inference engine.

### Not a universal truth oracle

Evidence and Verification remain domain-bound. The system can preserve provenance and authority without pretending to resolve every disputed claim.

### Not a universal multi-Agent society

Multiple Agents are an execution strategy whose benefit must be measured. A2A interoperability [P03][P04] may be used without adopting a permanent hierarchy, identity, or social ontology.

### Not safety by prompt

Prompts, classifiers, and guardrails can reduce risky behavior. Physical containment and scoped credentials remain required where the consequence demands them [A13].

## 7. Stable versus transient architecture

The following are likely stable responsibilities:

- identity across replacement;
- version-bound context and world state;
- explicit Effect and Dispatch history;
- current authorization at durable commit;
- evidence provenance and verification;
- human consequence ownership;
- recovery independent of model memory.

The following are more likely transient mechanisms:

- exact prompt templates;
- one specific Agent role hierarchy;
- fixed context-window reset schedules;
- model-specific retry instructions;
- arbitrary numbers of reviewers or subagents;
- provider-specific Tool-call formats;
- current weaknesses such as premature stopping.

Anthropic's Managed Agents work explicitly warns that harness assumptions can become stale as models improve [A12]. Ordivon should isolate these mechanisms behind stable interfaces rather than elevate them into Core axioms.

## 8. Domain projects as laboratories

Finance, Game, and Security should test candidate semantics under different truth and consequence structures:

- Finance stresses authority, data lineage, reconciliation, and irreversible decisions;
- Game stresses dynamic worlds, role-local context, replay, coordination, and scoring;
- Security stresses capability versus consequence, independent observers, containment, and adversarial adaptation.

A pattern should move from a domain project to Computing only after the domain-specific names are removed and a second workload demonstrates the same failure.

## 9. The implementation frontier

The current frontier is not hardware, kernel, storage engine, or universal distributed compute. It is the incomplete Agent-native overlay:

- durable but revisable open work;
- context selection with provenance and invalidation;
- cognitive routing and stopping;
- authority bound to purpose and consequence;
- general evidence and verification relations;
- operator attention and decision surfaces.

Even here, the correct next artifact may be a measurement or experiment rather than a new product service.
