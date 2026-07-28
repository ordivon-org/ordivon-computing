# Open Questions and Falsifiers

A foundational theory should expose where it can be wrong. The following questions remain open even after the responsibility overlay is accepted as a useful working model.

## 1. Is open-work continuity really distinct from durable workflow?

### Working claim

A durable workflow preserves predeclared control semantics. Open-work continuity preserves a task frontier whose decomposition, hypotheses, and completion evidence are revised through probabilistic cognition.

### Falsifier

Implement the same long-running research or software-maintenance workload in a conventional durable workflow without external Task semantics. If model/provider replacement, goal revision, unknown Effects, and evidence-based completion remain equally understandable and recoverable, the distinct R2 layer should be reduced or removed.

### Experiment

Run one frozen workload through:

1. raw model session;
2. Temporal-style durable Activity loop;
3. Host Task state plus replaceable models.

Measure accepted completion, recovery time, duplicate work, state size, and operator intervention.

## 2. What is the minimum durable cognitive checkpoint?

### Working claim

Conversation replay is neither necessary nor sufficient. A checkpoint needs Goal, active work, world bindings, uncertainty, evidence, Artifacts, and next admissible work.

### Falsifier

If a significantly smaller state reliably transfers work across different model families and fresh Hosts, remove the extra fields. If raw conversation performs as well under bounded context and drift, the structured checkpoint is over-designed.

### Open issue

The checkpoint must preserve enough provenance to avoid converting an old summary into current truth without forcing every future model to reread the entire history.

## 3. Is context compilation a kernel or a replaceable policy?

### Working claim

The responsibility to select, bind, and invalidate context is stable, while retrieval and summarization algorithms are replaceable.

### Falsifier

If future models can directly and economically consume the complete authoritative state without selection, context compilation may collapse into ordinary storage access. The version and provenance boundary may remain, but the active-selection layer could shrink substantially.

## 4. Is a general cognitive scheduler necessary?

### Working claim

Agent systems eventually need to allocate model calls, branches, verification, and human attention based on capability, information value, risk, and cost.

### Falsifier

If simple local policies consistently match or outperform a shared scheduler across Host, Game, Finance, and research workloads, keep routing inside applications.

### Required evidence before implementation

- repeated misrouting or premature stopping in at least two domains;
- measurable benefit from a common state model;
- a stable contract that does not encode one provider's limitations.

## 5. How should authority bind to purpose?

### Working claim

Credentials and OS permissions are necessary but too broad for dynamically generated durable Effects.

### Open questions

- Is Goal binding enforceable without interpreting natural language at commit time?
- Which consequences can be classified mechanically?
- How should approval survive plan revision?
- When must world state or policy be refreshed before commit?
- How can revocation propagate to active Attempts?
- Can a compact capability token carry enough semantic binding without becoming an application ontology?

### Falsifier

If scoped Tool interfaces and classical capability systems prevent the same failure classes with lower complexity, a separate universal authority kernel is unnecessary.

## 6. What is the minimum epistemic structure?

### Working claim

Observation, Claim, Verification, and Fact are meaningfully distinct across software, finance, game, and security workloads.

### Open questions

- Must `Inference` be a first-class object or a typed Claim relation?
- Is confidence part of a Verification, a Claim, or domain policy?
- How are Facts invalidated by world drift?
- Can contradictory Facts coexist under different scopes or authorities?
- How much provenance is needed for practical replay?

### Falsifier

If domain systems cannot share even a small common relation without losing essential meaning, keep the structure in Knowledge rather than Protocol.

## 7. When is multi-Agent coordination better than one larger run?

Anthropic reports strong benefits for breadth-first research but high token cost and weaker fit for tightly coupled work [A10].

### Required variables

- decomposability;
- shared-context requirement;
- branch independence;
- cost of duplicate work;
- join complexity;
- model and Tool latency;
- verification independence;
- task value.

### Falsifier

If the gain is explained almost entirely by additional token budget, an architecture may need scalable compute allocation rather than persistent social roles.

## 8. How should operator attention be scheduled?

### Working claim

The system should escalate novelty, irreversible consequence, ambiguous authority, or insufficient evidence rather than every physical action.

### Open questions

- What is an attention budget?
- How should multiple projects compete for it?
- How can the system explain why a decision is required without overwhelming the operator?
- Which approvals can be cached, and when do they expire?
- How is approval fatigue measured?

### Falsifier

If strong containment plus simple policy makes operator scheduling unnecessary for independent developers, keep attention management in the product interface rather than Core.

## 9. Which model limitations are temporary?

Potentially transient problems include:

- context anxiety and premature stopping;
- weak long-horizon planning;
- poor delegation;
- sensitivity to Tool descriptions;
- brittle context compression;
- unreliable self-evaluation.

Stable architecture must not assume these remain forever. Each mechanism should identify the model limitation it compensates for and the deletion test when models improve [A12].

## 10. Can classical infrastructure absorb the overlay?

The overlay may ultimately be implemented as extensions to existing systems:

- Temporal Activities and Search Attributes;
- Kubernetes custom resources and controllers;
- database schemas and policy engines;
- MCP or A2A extensions;
- Git and CI metadata;
- tracing and evidence stores.

That outcome would not falsify the semantic responsibilities. It would falsify the need for separate Ordivon product components.

## 11. Core deletion tests

Before any statement is retained in `core/`, ask:

1. If deleted, what realistic Agent trajectory becomes unrepresentable or unsafe?
2. Does a mature classical layer already guarantee it?
3. Is this a stable responsibility or a current harness workaround?
4. Is the statement supported by evidence beyond one Ordivon implementation?
5. Can a smaller formulation generate the same downstream decisions?

If no specific failure follows from deletion, the statement belongs in Knowledge or Research.

## 12. Near-term experiment program

The most informative next experiments are:

1. **durable-workflow comparison** — Host continuity versus a Temporal-style baseline;
2. **context invalidation** — stale summary, changed Tool contract, changed repository, and memory-poisoning cases;
3. **commit-time authority** — approval or capability becomes stale between cognition and Effect commitment;
4. **verification portability** — one Claim/Evidence/Verification relation across code, finance, and Game without sharing domain policy;
5. **cognitive scheduling ablation** — single Agent, fixed multi-Agent roles, and dynamic branch/verify/stop policy;
6. **operator attention measurement** — accepted result per active human minute, intervention count, and missed consequence.

These experiments should precede new universal packages or repositories.
