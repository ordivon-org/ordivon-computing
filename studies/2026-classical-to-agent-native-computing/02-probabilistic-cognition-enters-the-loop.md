# Probabilistic Cognition Enters the Loop

## 1. What “probabilistic cognition” means here

The phrase does not mean that every model invocation must use random sampling, or that all surrounding computation becomes probabilistic. Greedy decoding and fixed seeds can reduce run-to-run variation. The stronger issue is semantic:

> A foundation model is a learned statistical policy whose useful behavior is conditioned by selected context and cannot be completely specified as an ordinary program contract.

Its output may be fluent and useful without carrying a proof that it is correct, current, authorized, or complete.

OpenAI's Agents SDK reflects this separation: an Agent is a configured LLM, while a Runner manages turns, Tools, guardrails, handoffs, and sessions [A02]. Anthropic similarly defines an Agent through a plan–act–observe–adjust loop rather than a fixed script [A14].

## 2. The old boundary

In a conventional application, a human or software team has already performed most semantic compression before runtime:

```text
human goal
→ requirement
→ data model
→ program and policy
→ executable request
→ deterministic or bounded-nondeterministic substrate
```

Runtime inputs usually select among behaviors that have already been encoded.

## 3. The new boundary

An Agent system moves part of that semantic compression into runtime:

```text
human goal
→ context selected now
→ model interprets the situation
→ model proposes a next action
→ system decides whether and how to commit it
```

The execution path is path-dependent. New observations can change the task graph, invalidate context, create new hypotheses, or make the original goal impossible.

This is why a linear one-shot pipeline performs poorly on open research: the path cannot be fully hardcoded in advance, and intermediate discoveries alter subsequent search [A10].

## 4. The complete work-control loop

A robust loop separates roles that a conversational interface often compresses:

```text
Goal
  human purpose, constraints, and completion evidence

World binding
  exact repositories, objects, accounts, services, or environments

Context compilation
  bounded information selected for one cognitive episode

Cognition
  interpretation, hypothesis, plan, or candidate action

Admission
  structural, policy, authority, freshness, and budget checks

Effect commitment
  stable semantic identity bound to one concrete execution contract

Classical execution
  process, transaction, Tool, network, or remote service

Observation
  immutable reading or receipt from external reality

Verification
  declared method evaluates a Claim against evidence

Task update
  continue, branch, wait, revise, complete, reject, or escalate
```

The model may participate in several roles, but the system should not collapse their authority.

## 5. Candidate, command, observation, and fact

Four values that can share the same JSON shape still have different meanings:

```text
Candidate
  "Run the migration now."

Command
  an admitted, authority-bound request to a concrete executor

Observation
  "migration process exited 0 at revision X"

Fact
  "migration completed and postconditions passed"
```

A model can produce the first. A Host may admit the second. Runtime evidence can produce the third. Verification and fact authority are required for the fourth.

This is not ceremonial typing. It prevents a model statement from bypassing the physical and epistemic boundaries of the system.

## 6. Context becomes part of execution semantics

Context is the finite token state supplied to the model. Anthropic describes context engineering as repeated curation of the smallest high-signal set drawn from instructions, Tools, history, and external data [A08].

Two invocations against the same world can produce different proposals because they receive different:

- source revisions;
- summaries;
- Tool catalogs;
- examples;
- previous results;
- policies;
- retrieved memory;
- omitted uncertainty.

Therefore a meaningful model-invocation record should bind at least:

```text
model and provider version
+ instruction or policy revision
+ selected context inputs and digests
+ Tool or capability catalog revision
+ relevant world versions
+ output and usage metadata
```

The complete raw prompt is not always the durable truth; it may contain secrets, transient formatting, or redundant history. The system needs a stable record of the semantic inputs sufficient for explanation, comparison, and continuation.

## 7. Conversation continuity is not work continuity

Session mechanisms preserve conversational history [A03]. That is useful but incomplete.

A long-running task may need to survive:

- context compaction;
- provider replacement;
- a new Host process;
- a different model family;
- a changed repository revision;
- failed Attempts;
- user redirection;
- revoked authority;
- external effects with unknown outcomes.

Anthropic's long-running harness work found that compaction alone was insufficient; incremental progress and explicit artifacts were required across sessions [A09].

The durable object must therefore preserve current work semantics, not merely dialogue order.

## 8. Why the loop cannot remain entirely probabilistic

A model can help select checks, interpret evidence, and propose recovery. It should not be the only record of whether an irreversible Effect was dispatched.

Probabilistic context is vulnerable to:

- omission through compaction;
- stale world assumptions;
- repeated action after forgetting;
- plausible but unsupported completion claims;
- prompt injection through external content;
- policy drift across model versions;
- coordination errors between Agents.

The lower boundary must preserve stable identity and physical evidence even when every model episode is lost.

```text
probabilistic cognition may choose
what to attempt next

only deterministic durable state may establish
what was admitted, dispatched, observed, and accepted
```

## 9. Why the loop cannot be entirely predeclared

The opposite reduction also fails. Encoding every possible branch in a fixed workflow removes much of the value of Agents in open problems.

A useful Agent can:

- investigate an unfamiliar system;
- discover that the initial hypothesis is wrong;
- create previously unknown subtasks;
- select different Tools based on evidence;
- compare candidate explanations;
- stop when marginal information value is low;
- ask for human judgment when consequences exceed its grant.

The system therefore needs a deterministic control boundary around a dynamically revised cognitive frontier.

## 10. The changed computer boundary

The Agent-era computer is not a stochastic replacement for the classical machine. It is a hybrid:

```text
probabilistic proposal generation
inside
persistent deterministic control and evidence
above
classical execution and storage
```

Ordivon's subject is this hybrid boundary. Its value depends on preserving the strengths of both sides rather than making either side pretend to be the other.
