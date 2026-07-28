# Classical Assumptions That No Longer Suffice

The following assumptions are not universal truths about older computing. They are practical contracts that worked because humans and application code resolved most ambiguity before runtime. Agent systems move ambiguity into runtime and expose the boundary.

## 1. “The input is an executable request”

### Classical form

A system receives a command, API request, SQL statement, Pod template, or workflow input whose operational meaning is already defined.

### Agent-era pressure

The input may be:

```text
Find the most important architectural drift and fix it.
```

The system must discover objects, construct criteria, create tasks, and revise the path.

### Required change

Separate open Goal semantics from the concrete Effect selected at one moment.

### Counterexample

A fixed support workflow with enumerated actions may need no new Goal layer. Using an LLM to classify the request does not automatically make the whole system Agent-native.

---

## 2. “The process or Job is the work”

### Classical form

A process, batch Job, or durable Workflow represents one declared unit of execution. Kubernetes and Temporal already preserve this identity across physical failures [C06][C08].

### Agent-era pressure

One human task can span multiple model sessions, processes, workspaces, candidate plans, and failed Attempts. The task definition itself may change after evidence arrives.

### Required change

Preserve semantic work identity above replaceable execution instances.

### Important narrowing

Generic Task durability is not new. The changed responsibility is the continuity of an open and revisable work frontier whose semantics cannot be reduced to one predeclared workflow execution.

---

## 3. “Program output has the authority of the program”

### Classical form

Application code and policy were reviewed before deployment. A successful function return normally carries the authority granted to that program path.

### Agent-era pressure

A model generates a novel action at runtime. The action was not individually reviewed when the application was deployed.

### Required change

Treat model output as a candidate and bind the admitted Effect to current policy, world version, capability, budget, and consequence scope.

OpenAI Tool guardrails demonstrate pre- and post-execution checks around generated Tool calls [A04], but SDK guardrails are one implementation path rather than the universal contract.

---

## 4. “Identity and access control are enough authorization”

### Classical form

Users, roles, processes, credentials, ACLs, and capabilities determine access.

### Agent-era pressure

A process may possess broad write authority while the Agent is delegated only one bounded purpose. Valid credentials do not imply that every generated action is intended.

### Required change

Authorization may need to bind:

```text
principal
+ Goal or delegated purpose
+ target object and current version
+ Effect semantics
+ consequence envelope
+ budget and expiry
+ approving policy or human decision
```

### Counterexample

If the user explicitly requests one low-risk read operation and the Tool is read-only, ordinary identity and Tool access may be sufficient. Not every call needs a new authority ceremony.

---

## 5. “A retry repeats the intended operation”

### Classical form

Well-designed APIs declare idempotency keys, transaction identity, or retry behavior. Kubernetes warns that the same program can still be started more than once [C06]. Distributed systems already treat duplicate delivery as a normal failure mode.

### Agent-era pressure

The model may forget the first attempt, change the payload while reusing the human intent, or interpret a lost response as failure. A semantic Effect and its concrete Dispatch can diverge.

### Required change

Separate:

```text
Effect identity
  the stable intended external change

Dispatch identity
  one concrete boundary attempt

idempotency semantics
  whether and how the backend deduplicates

reconciliation
  how current reality resolves an unknown response
```

An Effect does not become idempotent merely because it has a stable identifier.

---

## 6. “Persisted data is accepted application truth”

### Classical form

The application validates data before a transaction. The database atomically persists the declared update [C04].

### Agent-era pressure

Models produce claims, summaries, inferred causes, and plans that may be plausible but unsupported.

### Required change

Distinguish:

```text
Observation  immutable reading of reality
Claim        proposition proposed for evaluation
Inference    derived interpretation with assumptions
Evidence     observation or artifact used in evaluation
Verification recorded decision under a method
Fact         claim admitted by the relevant authority
```

### Counterexample

A deterministic API response may be accepted directly as a domain event if the API is authoritative for that field. Not every datum requires a model-independent review Agent.

---

## 7. “Logs explain the run”

### Classical form

Logs and traces record program events. OpenAI's Agents SDK extends tracing across model turns, Tool calls, handoffs, and guardrails [A05].

### Agent-era pressure

A trace can show that a model said “tests passed” without showing that tests ran, or that a Tool returned data without showing that the data supports the conclusion.

### Required change

Observability must be joined with semantic identity and evidence provenance:

```text
Goal → Task → model invocation → Effect → Dispatch
→ backend receipt → Observation / Artifact → Verification
```

### Important narrowing

This does not require a new tracing transport. OpenTelemetry or existing logs may carry the data. The new responsibility is the semantic relation between records.

---

## 8. “Correctness can be specified before execution”

### Classical form

Unit tests, type systems, invariants, protocol schemas, and acceptance tests encode expected behavior.

### Agent-era pressure

Open-ended tasks can have multiple acceptable results, unknown intermediate paths, and qualitative requirements. Agents also modify the environment over many turns.

Anthropic notes that Agent evaluations must match multi-turn trajectories and environment-changing behavior [A11].

### Required change

Combine several evaluators:

- deterministic tests and invariants;
- independent world observations;
- replay and provenance checks;
- counterexample search;
- model graders where appropriate;
- human judgment for value or consequence;
- later real-world outcomes.

### Counterexample

Coding tasks with complete tests may remain ordinary program synthesis. Agent involvement does not invalidate deterministic verification when the specification is genuinely sufficient.

---

## 9. “Resource scheduling is the main scheduling problem”

### Classical form

Operating systems and clusters allocate CPU, memory, devices, and Nodes [C02][C06].

### Agent-era pressure

The system must also decide:

- which model or Agent has the right capability;
- which context should be loaded;
- whether to branch or continue;
- whether another candidate is worth its cost;
- when verification has higher value than generation;
- when uncertainty requires human attention;
- when to stop despite remaining possible work.

### Required change

Introduce cognitive work scheduling above resource scheduling. The output is not merely placement on a machine; it is selection of the next information-producing or world-changing Attempt.

### Counterexample

Static routing among a few specialist prompts can remain an application policy. A general scheduler is justified only by repeated cross-domain evidence.

---

## 10. “More workers create more throughput”

### Classical form

Independent work can be parallelized when dependencies and merge semantics are known.

### Agent-era pressure

Multiple Agents may duplicate exploration, inherit the same wrong assumption, contaminate one another's context, or produce incompatible artifacts. Anthropic reports both large breadth-first gains and substantially higher token cost, while noting weak fit for tightly coupled tasks [A10].

### Required change

Coordination should make independence and joining explicit:

```text
shared Goal
→ bounded independent Attempts
→ stable Artifacts and Claims
→ explicit comparison or Join
→ accepted result
```

Multi-Agent conversation is not itself a coordination substrate.

---

## 11. “Human approval scales with action count”

### Classical form

Interactive tools ask a user before consequential operations.

### Agent-era pressure

High-frequency approval prompts cause fatigue. Anthropic reports that users approved most prompts and invested less attention as prompts accumulated; stronger environment boundaries reduced the need for per-action approvals [A13].

### Required change

Treat human attention as a scarce resource:

- pre-authorize bounded reversible classes;
- contain physical reach;
- escalate uncertainty, novelty, or irreversible consequence;
- present evidence and alternatives at decision points;
- avoid asking the human to simulate a policy engine repeatedly.

### Counterexample

A rare, high-consequence operation may still require explicit per-effect human approval.

---

## 12. “The application boundary is stable”

### Classical form

The program, workflow, and Tool set change through explicit deployment.

### Agent-era pressure

Remote Tools can change contracts, repositories can change while a task runs, memory can be poisoned across sessions, and models or harnesses can be replaced. MCP uses capability negotiation because client and server features evolve independently [P01]. Anthropic warns that persistent Agent state creates new persistence and trust-escalation attack surfaces [A13].

### Required change

Bind decisions to versioned world and contract observations, then detect drift before committing durable effects.

## Result

The common pattern is not “Agents are nondeterministic, therefore add guardrails.” It is more precise:

> A learned policy now creates operationally novel proposals from selected and potentially incomplete context. Existing deterministic layers can execute and persist those proposals, but they do not own the proposal's purpose, current authority, evidential status, or continuing work semantics.

Those unowned responsibilities define the candidate Agent-native overlay.
