# Research

Research stores open questions, competing hypotheses, prototypes, experiments, immutable evidence manifests, and unresolved evidence.

## Structure

- [`portfolio.json`](portfolio.json) — authoritative research status, maturity, blockers, next falsifiers, and WIP lines;
- [`PORTFOLIO.md`](PORTFOLIO.md) — generated human-readable portfolio and Ready Frontier;
- [`map.yaml`](map.yaml) — stable typed relations among construction tracks and research questions;
- [`questions/`](questions/) — one durable page per file-backed question, including historical questions;
- [`experiments/`](experiments/) — executable artifacts and experiment records;
- [`evidence/`](evidence/) — immutable cross-repository System Snapshots and their validator;
- [`charters/`](charters/) — durable missions and responsibility boundaries for cross-project research fabrics;
- [`capability-gaps/`](capability-gaps/) — evidence-oriented missing-capability registers, not implementation roadmaps;
- [GitHub Issues](https://github.com/zycxfyh/ordivon-computing/issues) — active construction tracks, dependencies, discussion, and Ready Frontier.

Durable question pages preserve hypotheses, baselines, falsifiers, and evidence criteria. `portfolio.json` owns current portfolio status and WIP. GitHub Issues carry discussion, implementation history, and repository-local execution. Product repositories and `experiments/` carry executable artifacts. `evidence/` binds exact historical revisions, services, contracts, and Artifact digests; it is not a mutable deployment registry.

Research may contain alternatives, failed experiments, changing terminology, and incomplete models. Results move into [`../knowledge/`](../knowledge/) when they become reusable. Only compact, stable, cross-workload responsibilities that survive strong classical counterexamples may enter [`../core/`](../core/).

## Construction program

The cross-layer construction program is [#1 — Construct the Agent-Native Machine](https://github.com/zycxfyh/ordivon-computing/issues/1). Its tracks and typed relations are indexed in [`map.yaml`](map.yaml). The program is not a commitment to reimplement the whole computing stack: [`ANC-STACK-001`](questions/ANC-STACK-001-classical-to-agent-native-transition.md) determines which responsibilities should remain inherited, researched, or constructed.

## Current Ready Frontier

The canonical current view is [`PORTFOLIO.md`](PORTFOLIO.md), generated from [`portfolio.json`](portfolio.json). This overview intentionally does not repeat active line identifiers, question statuses, or next actions.

## Historical comparisons

- `ANC-EDGE-001`, `ANC-LINK-001`, and `ANC-WORLD-001` are superseded by `ANC-WORLD-002`;
- `ANC-SECURITY-002` remains completed Phase 0 substrate evidence and is superseded by the unified World and strategic-Security programs;
- Semantic Core, Effect IR, Task continuation, Host boundary, and original Game/Host convergence are completed or frozen evidence, not open construction promises.

Portfolio maintenance commands:

```bash
python3 scripts/check_research_portfolio.py
python3 scripts/render_research_portfolio.py --check
```

The primary-source derivation for `ANC-STACK-001` and the cross-paradigm validation program live in [`../studies/2026-classical-to-agent-native-computing/`](../studies/2026-classical-to-agent-native-computing/).

The strategic adversarial-systems reorientation, source comparison, insertion map, and research program live in [`../studies/2026-agent-native-adversarial-systems/`](../studies/2026-agent-native-adversarial-systems/).

The R0 Web and network adversarial foundation—terminology, causal graph, evidence method, real-case validation, Agent amplification, and World/Security insertion rules—lives in [`../studies/2026-web-network-adversarial-foundations/`](../studies/2026-web-network-adversarial-foundations/). It is a completed knowledge baseline, not an authorization for offensive execution or a new active implementation line.

The R1 Web identity study—origin and site, browser authority, Cookies and ambient authority, CSRF/CORS, OAuth delegation, workload and Agent identity, generated Tool authority, and maximal adaptive attack/defense chains—lives in [`../studies/2026-web-identity-origin-delegation/`](../studies/2026-web-identity-origin-delegation/). It records model, Host, and policy behavior as experimental configuration rather than proof that lower-layer attack capability is absent.

The R2 semantic-differential study—HTTP framing and transitions, URL and encoding order, field and routing metadata, content typing and HTML parsing, cache equivalence, downstream interpreters, Agent differential discovery, and defensive graph cuts—lives in [`../studies/2026-web-semantic-differentials/`](../studies/2026-web-semantic-differentials/). It treats refusal and normalization by one client or Host as local observations, not proof that the underlying differential or a lower-level realization is absent.

The R3 network-truth study—DNS and DNSSEC, BGP/RPKI and route leaks, IP/NAT and address-family selection, TCP/UDP delivery limits, current TLS 1.3 and service identity, QUIC migration and 0-RTT, proxy/VPN composition, timeout/retry ambiguity, and Agent path adaptation—lives in [`../studies/2026-network-truth-partial-failure/`](../studies/2026-network-truth-partial-failure/). It records model and Host refusals as configuration observations while keeping naming, route, transport, channel, response, and verified Effect claims distinct.

The R4 cross-layer case study—Capital One cloud authority, Exchange exploitation, proxy request smuggling, BGP/DNS/TLS failure, SolarWinds systemic identity compromise, cache persistence, Agent hijacking, and retry duplication—lives in [`../studies/2026-cross-layer-attack-chains/`](../studies/2026-cross-layer-attack-chains/). It reconstructs official evidence as typed causal chains, keeps model/Host policy as a configuration variable, and separates patching from Campaign and residual closure.
