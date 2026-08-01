# 08 — Agent Hijacking: External Data to Legitimate Tool and Identity

## Evidence boundary

NIST describes Agent hijacking as an indirect prompt-injection class in which an
attacker places malicious instructions in data—such as email, files, websites,
or repositories—that an Agent processes while performing a legitimate task.
[R20]

NIST's 2025 evaluation found that adaptive attacks and repeated attempts matter;
in one five-task illustration, average measured success increased from 57% for a
single attempt to 80% over repeated attempts. [R20]

NIST's 2026 large-scale red-teaming analysis reinforces that Agents processing
external data remain vulnerable to adversarial instructions and that evaluation
must model active attackers. [R21]

OWASP's Agentic Threats Navigator identifies reasoning, memory, tools, identity,
human oversight, and multi-Agent interaction as distinct attack surfaces. [R22]

## Causal graph

```text
A1 Agent must ingest external data and use Tools
→ T1 natural-language data and instruction share one model Context
→ W1 no reliable semantic separation between evidence and imperative content
→ V1 attacker controls task-relevant external resource
→ P1 external content changes action selection
→ I1 Agent retains legitimate user/session/Token/Tool authority
→ C1 invokes valid Tool or browser action
→ N1 retries, adaptation, generated Tools, memory, and multi-Agent propagation
→ O1 unintended message, disclosure, code execution, transfer, or deletion
→ D1 transcript/Tool/World contradiction
→ R1 stop, revoke, delete, reconcile, restore affected resources
→ X1 sent messages, copied data, generated Tools, memory, Tokens, external Effects
```

## The model is not the only boundary

Agent hijacking can be influenced by:

- model behavior;
- system/developer instructions;
- Host Context compilation;
- Tool descriptions;
- Tool grants;
- browser sessions;
- identity and Token scope;
- memory and retrieval;
- deterministic Tool validation;
- World Effect verification.

A model refusal may block one attempt, but it does not prove the complete system
is secure against adaptive alternatives.

## Legitimate authority is the amplifier

The dangerous transition is:

```text
malicious data affects cognition
→ legitimate Tool executes deterministic action
```

The Tool can be functioning exactly as designed. The browser can attach a valid
session. The API can accept a valid Token. The provider can return success.

Failure lies in the chain from participant purpose to action admission.

## Repeated attempts

Probabilistic systems require distributional evaluation. An attacker can:

- retry the same injection;
- vary wording and placement;
- choose different external resources;
- exploit task-specific Tool paths;
- learn which defense caused refusal;
- construct a generated Tool;
- delegate to another Agent;
- poison reusable memory.

One-shot success or failure is therefore insufficient.

## Safety-prompt confound

A strong safety policy can reduce observed attacks and is part of the deployed
system. R4 nevertheless records it separately because:

- malicious or open-weight models may not share it;
- direct deterministic Tools bypass language-generation constraints;
- generated code can realize capabilities after benign-looking planning;
- future model revisions can change behavior;
- lower-layer vulnerabilities remain even if the current model refuses them.

The correct result format is:

```text
policy blocked model output
Tool was not admitted
no network action observed
World unchanged under this configuration
```

not:

```text
attack impossible
```

## Defensive breakpoints

### B1 — label external content as evidence

Preserve source and trust status through Context compilation.

### B2 — Task-scoped Tool grants

Grant exact resources, actions, identities, lifetime, and onward-delegation
limits.

### B3 — consequence-specific Effect admission

A model proposal is not sufficient authority for high-impact world changes.

### B4 — separate browsing and acting identities

Do not expose broad authenticated sessions to unrestricted external-content
navigation.

### B5 — generated Tool provenance and admission

Build and test in a disposable credential-empty environment before granting
external authority.

### B6 — repeated adaptive evaluation

Test held-out attacks, several attempts, changed defenses, and task-specific
outcomes.

### B7 — independent World verification

Deterministic provider or object evidence must establish the result.

## Recovery and residual closure

After hijacking, inspect:

- Tool calls and external objects;
- sent messages and downstream recipients;
- browser sessions and Tokens;
- generated code and dependencies;
- memory and retrieval indexes;
- delegated Agents and child Tasks;
- provider callbacks and queued jobs;
- deleted or modified resources.

## Ordivon lesson

This case directly validates Host ownership of Context, ToolGrant, Effect, and
completion; Runtime ownership of local execution; World/provider ownership of
external facts; Security ownership of adaptive attack and residual interpretation;
and Game as a deterministic laboratory. It does not earn a universal policy
engine.
