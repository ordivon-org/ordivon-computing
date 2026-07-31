# Web and Network Adversarial Foundations

Status: R0 foundational study completed

## Purpose

This study establishes the epistemic and causal foundation for Ordivon's next
Web, network, World, and Security learning route. It asks a narrower question
than a vulnerability catalog:

> Which indispensable properties make modern Web and network systems useful,
> which structural tensions follow from those properties, how do weaknesses
> become composable capabilities and adversarial Campaigns, and what changes
> when adaptive Agents can observe, construct Tools, retry, coordinate, and
> attack the evaluator?

The objective is deep mechanism recognition before any range exercise. The
study analyzes standards and real incidents without exploit code, payloads,
target-selection guidance, or instructions for acting against public systems.

## Central result

A vulnerability is not the correct top-level unit for adversarial reasoning.
The useful unit is a typed causal graph:

```text
indispensable affordance
→ structural tension and trust assumption
→ weakness or exposure
→ concrete vulnerability
→ exploit primitive
→ cross-component attack chain
→ adaptive Campaign
→ world outcome, evidence, and residual state
```

The graph is not necessarily linear. One weakness can enable several primitives;
one primitive can be supplied by several vulnerabilities; identity, routing,
Tool, and business-logic conditions can join the graph; defenses can remove an
edge without removing every node; and an adaptive opponent can search for a new
path after one edge is blocked.

## Why the distinction matters

- CWE weakness chains describe causal relationships among software weaknesses.
- CVE records identify concrete publicly disclosed vulnerabilities.
- CVSS communicates vulnerability severity characteristics; a Base score is not
  deployment risk.
- ATT&CK tactics and techniques describe why and how adversaries act.
- A real Campaign also contains actor objectives, resources, identities,
  information state, timing, adaptation, evidence pressure, and residual state.

Collapsing these layers causes predictable errors: treating a patch as complete
incident closure, treating a high CVSS score as the highest local risk, treating
a successful Tool call as an objective outcome, or treating a fixed technique
list as a model of adaptive opposition.

## Study structure

1. [`00-method-and-scope.md`](00-method-and-scope.md) — method, evidence hierarchy,
   safety boundary, and Ordivon A-series admission rules;
2. [`01-terminology-and-levels.md`](01-terminology-and-levels.md) — canonical
   distinctions among affordance, weakness, vulnerability, primitive, chain,
   Campaign, severity, risk, and evidence;
3. [`02-causal-graph-grammar.md`](02-causal-graph-grammar.md) — the typed graph and
   attack/defense dual;
4. [`03-truth-evidence-and-evaluation.md`](03-truth-evidence-and-evaluation.md) —
   authoritative world truth, observation, claims, repeated trials, uncertainty,
   and case-dossier requirements;
5. [`04-agent-amplification-and-defense.md`](04-agent-amplification-and-defense.md)
   — what remains classical, what Agents amplify, and which responsibilities are
   structurally rewritten;
6. [`05-real-case-validation.md`](05-real-case-validation.md) — non-operational
   validation against HTTP parser disagreement, Log4Shell, Exchange chaining,
   SolarWinds, and Agent hijacking;
7. [`06-ordivon-insertion-and-next-route.md`](06-ordivon-insertion-and-next-route.md)
   — World, Security, Host, Runtime, and Game implications plus the R1 gate;
8. [`REFERENCES.md`](REFERENCES.md) — primary-source ledger and limitations.

## Resulting learning rule

Every later Web or network topic is studied through five simultaneous views:

```text
mechanism
causal weakness graph
adaptive attacker
adaptive defender
Ordivon responsibility and deletion test
```

This does not make every protocol topic a Security implementation task. Most
mechanisms remain inherited classical substrate. A product responsibility is
admitted only when a concrete failure is unowned, non-bypassable, reusable
across workloads, and cheaper than leaving the failure unresolved.

## Next route

R1 studies Web identity, origin, delegation, sessions, ambient authority, and
browser/Agent confused-deputy behavior. It remains a knowledge and architecture
track; controlled range execution stays deferred until the World, consequence,
observer, reset, and residual-evidence boundaries are independently established.
