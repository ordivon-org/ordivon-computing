# The Classical Computing Contract

## 1. Classical computing is not merely “deterministic code”

Classical systems already contain concurrency, partial failure, clocks, random-number generators, distributed races, nondeterministic scheduling, user input, and uncertain networks. Calling the entire older stack deterministic is therefore imprecise.

The stronger distinction is contractual:

> Classical infrastructure expects software authors to define the operational object, legal transitions, and completion conditions before the infrastructure executes or persists them.

A scheduler need not know why a process matters. A database need not know whether a row expresses a justified belief. A workflow engine need not infer the business goal from an incomplete natural-language request. Their power comes from enforcing a narrower contract exactly.

## 2. Process and thread

POSIX defines process and thread-level interfaces and treats a thread as a flow of control within a process [C01]. Linux scheduling then places runnable tasks on CPUs and balances load across scheduling domains [C02].

These mechanisms own:

- execution contexts;
- CPU eligibility and placement;
- address-space and resource relationships;
- synchronization and termination interfaces;
- operating-system accounting.

They do not own:

- the human goal behind a process;
- whether the process is the latest valid attempt;
- whether its output satisfies an open-ended task;
- whether a model should have proposed the process at all.

A process can terminate successfully while the human task remains incomplete. Conversely, one persistent task can span many processes.

```text
process identity  = operating-system execution identity
Task identity     = semantic continuity of work
```

The distinction is useful only above the process layer. It does not reduce the authority of the operating system over actual execution.

## 3. Isolation and resource boundaries

Linux namespaces provide mature isolation mechanisms for views of resources [C03]. Containers and virtual machines compose namespaces, cgroups, filesystem boundaries, hypervisors, and network policy. These remain the correct place to enforce what code can physically reach.

Agent-specific policy does not replace isolation. An Agent may need a semantic grant for one Effect, but the executing process still needs a deterministic environment boundary. Anthropic's containment experience reinforces this: model safeguards shape tendencies, while sandboxes, VMs, credential placement, and egress policy cap actual blast radius [A13].

Therefore:

```text
semantic authorization without containment = excessive physical reach
containment without semantic authorization = bounded but potentially wrong action
```

Both may be required, but they are different layers.

## 4. Transactions and durable bytes

SQLite implements atomic commit so that a transaction appears all-or-none even across crashes or power loss [C04]. Databases additionally provide indexing, locking or concurrency control, query processing, and storage recovery.

This is sufficient for writing an Agent event journal safely at the byte and transaction level. It is not sufficient for deciding the meaning of the records.

A transaction can atomically store:

```text
"the deployment is healthy"
```

while that statement remains false or unsupported. Database correctness answers:

```text
Were the declared writes committed according to the transaction contract?
```

Epistemic correctness asks:

```text
What observation supports the claim?
Who verified it?
Under which world and policy version?
Can the claim be admitted as a current Fact?
```

The second problem is not evidence that databases are deficient. It is a different responsibility above them.

## 5. Content identity and versioned artifacts

Git is fundamentally a content-addressable object system [C05]. It already supplies durable content identity, tree structure, commits, and references. Agent systems should reuse these properties for source revisions, candidate workspaces, and artifacts rather than inventing weaker identity schemes.

Git does not decide:

- whether a commit advances a Goal;
- whether a generated patch was authorized;
- whether tests are sufficient verification;
- whether two candidates should be joined;
- whether a branch should be abandoned.

Those are work-control and judgment questions. The underlying content identity remains classical and reusable.

## 6. Jobs and controllers

Kubernetes Jobs represent declared one-off tasks that run to completion, retry Pods, support parallel completion policies, and record terminal success or failure [C06]. Kubernetes controllers observe current state and act toward a declared desired state [C07].

These systems already demonstrate that:

- a Job can outlive one process or Pod;
- execution can be retried after machine failure;
- desired and observed state can be separated;
- completion can be a durable control-plane fact;
- duplicate physical starts are possible and applications must handle them [C06].

Therefore none of the following are uniquely Agent-native:

```text
durable Job identity
retry
reconciliation loop
desired-versus-observed state
parallel workers
terminal conditions
```

The unresolved Agent question is different. A Kubernetes Job receives a Pod template and completion policy. It does not infer or revise the task definition from evidence gathered by a statistical model.

## 7. Durable workflows

Temporal explicitly provides durable execution across crashes, network failures, and infrastructure outages [C08]. It persists Workflow history and reconstructs execution through replay [C09]. Activities isolate failure-prone external effects from replay-safe workflow logic.

This invalidates a broad claim that “work surviving a process” is a new Agent-layer invention.

Temporal's contract, however, depends on workflow semantics being encoded in replay-compatible program logic. A model call is generally treated as an external Activity or otherwise recorded, because replaying a nondeterministic model call can produce a different result. The workflow can durably preserve the result, but the application still decides:

- what context the model should receive;
- whether the result is a proposal, decision, or fact;
- what Effect it may authorize;
- how to evaluate open-ended completion;
- how a changed goal invalidates the previous plan.

A useful boundary is:

```text
Temporal-like durability
= preserve and resume declared control logic

Agent-native semantic continuity
= preserve and revise the meaning, evidence, and authority
  of work whose path is not fully declared in advance
```

Ordivon may reuse durable workflow ideas or implementations. It should not claim ownership of generic durability.

## 8. Protocols

RPC, HTTP, JSON-RPC, MCP, and A2A define how parties exchange typed messages, capabilities, tasks, and artifacts. MCP separates Host, Client, and Server responsibilities [P01]. Its experimental Tasks provide durable request handles and deferred result retrieval [P02]. A2A defines interoperable remote-Agent Task and Artifact objects [P03][P04].

Protocols can make state transferable. They do not automatically establish which state is authoritative inside a product.

```text
wire Task      ≠ internal Goal truth
Tool capability ≠ semantic authorization for one Effect
Artifact payload ≠ accepted result
successful RPC  ≠ verified world outcome
```

This distinction prevents Ordivon Protocol from expanding into a universal internal ontology merely because similar words appear in an external standard.

## 9. The classical foundation that Ordivon should inherit

Ordivon should continue to delegate:

| Responsibility | Classical owner |
|---|---|
| CPU scheduling and process lifecycle | operating system |
| isolation and resource boundary | container, VM, kernel, network policy |
| transactional byte durability | database and filesystem |
| source and artifact content identity | Git or object store |
| network transport and cryptography | mature protocols and libraries |
| replay of declared durable workflows | workflow engine when adopted |
| compiler and test execution | existing toolchains |

The Agent-native system should add semantics only where these mechanisms intentionally stop.

## 10. Result

The classical world did not fail to anticipate Agents. It optimized for a different boundary: once a program, policy, or workflow has been expressed, execute and preserve it reliably.

The new problem begins before and around that boundary:

```text
underspecified purpose
→ selected context
→ statistically generated proposal
→ changing plan
→ durable consequence
→ evidence-based acceptance
```

The rest of this study asks which parts of that path require stable system responsibility.
