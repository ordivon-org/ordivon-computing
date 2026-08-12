# EG0–EG8 — Comparative Capability Entity Gap Audit

## Result

This round started from a narrower question than another Agent-first reform:

> Which important Ordivon responsibilities are still being carried by Agent judgment or ad-hoc scripts even though another kind of entity has a structural comparative advantage?

The answer is **not** a new universal capability layer. The round retains several non-Agent entity roles, localizes them to the owner that needs them, and promotes **zero new shared services and zero new shared protocols**.

The strongest current shortages are:

1. fresh observation / external authority / physical resources;
2. independent exact verification;
3. calibrated statistical estimation.

Optimization is useful as a certificate and search instrument. Domain simulation is already healthy. Human observation remains a scoped high-cost sensor. A generic Archivist/index service did **not** earn itself.

## Frozen method

[`experiment-contract.json`](experiment-contract.json) requires every candidate entity to compete against the current owner-native and simple deterministic baseline. Comparison remains multi-axis; no universal entity score or capability router is introduced.

The reproducible runner is [`run_entity_gap.py`](run_entity_gap.py). It reads exact Git revisions of all owner inputs, refuses the run if an owner HEAD or cleanliness state changes during execution, writes only bounded JSON evidence, and deletes the temporary SQLite index used by EG7.

## EG0 — responsibility × entity matrix

[`results/eg0-responsibility-entity-matrix.json`](results/eg0-responsibility-entity-matrix.json) binds nineteen representative current responsibilities across Computing, Runtime, Host, Harness, Finance, Workstation, Security, Game, Human, Studio and Web.

The already hard-tested spine remains well placed: Agent/open-ended research judgment, Host semantic continuity, Harness bounded Agent Runs, Runtime physical execution, owner-native domain truth and Studio/Web consequence boundaries are not reopened merely to make the entity taxonomy symmetric.

The real gaps cluster around Finance live observation, Workstation physical/carrier independence, statistical calibration, exact admission verification and human-grounded consequence claims.

## EG1 — formal verifier / constraint checker

The first falsifier reconstructs the current Finance fresh-canary admission boundary as twelve explicit Boolean predicates derived from the exact owner evidence.

The complete state space is only `2^12 = 4096`, so the strongest mature baseline is **exact enumeration**, not an imported SMT framework.

Results:

- `local-only` admission would unsafely accept **511** states;
- `local + venue` still accepts **255** unsafe states;
- `local + permission` still accepts **127** unsafe states;
- the full exact predicate accepts zero unsafe states by construction;
- twelve single-predicate omission mutants were generated;
- three bounded example states detected only **1 / 12** omission mutants;
- exact enumeration produced a counterexample for **12 / 12**.

This earns the **formal verifier role**, but not a universal verifier service and not even a new Z3 dependency yet. For this bounded owner problem, exhaustive classical enumeration is simpler and complete. A heavier solver becomes justified only when the real constraint state grows beyond a cheap exhaustive baseline.

The verifier proves or falsifies an admission predicate. It does not choose the financial objective, authorize capital, or create venue truth.

## EG2 — optimizer / resource allocator

NX7 provides a real combinatorial problem: 16 current resources must cover 11 current P0 capability slots.

Exact subset search proves:

- minimum full P0 cover = **7 resources**;
- there are **6** distinct minimum-cardinality solutions;
- the simple greedy baseline also chose 7, so it happened to be cardinality-optimal;
- even under budgets of only 1–4 resources there are **67** nondominated combinations when coverage, distinct owners, redundant slot support and resource count remain separate axes.

The important result is not that an optimizer beat the Agent. It **certified** where the simple heuristic was already right and exposed the alternatives the heuristic hid. Some seven-resource optima contain seven distinct owners; others contain six. No mathematical routine can decide whether that owner-diversity difference is worth another operational cost unless the owner supplies the value relation.

Therefore optimizer/allocator is retained as owner-local decision support, never as scheduler or semantic authority.

## EG3 — statistical estimator / calibrator

FS0 had superficially strong point rates:

- raw selector: `5 / 5` top-choice agreement = 100%;
- RFM selector: `4 / 5` = 80%;
- negative control chosen `0 / 10` times;
- negative control deferred `10 / 10` times.

A pure-Python Wilson estimator changes the interpretation materially:

- `5/5`: 95% Wilson **[0.566, 1.000]**;
- `4/5`: **[0.376, 0.964]**;
- `0/10`: upper 95% bound still **0.278**;
- `10/10`: lower 95% bound only **0.722**.

Thus the observed raw/RFM stability intervals overlap widely. Agent confidence or a perfect small-sample point rate is not calibrated uncertainty.

Statistical estimation is therefore a **high-priority entity role**. The first implementation remains a small audited formula rather than a new statistics platform. Repeated-measure, causal or larger experimental workloads may later justify mature owner-local statistical packages.

## EG4 — sensor / outcome measurement

The audit separates cognition scarcity from reality scarcity.

Current examples include:

- Finance: OKX reachability, Trade permission and reconciliation truth are externally unavailable;
- Workstation: `carrierIndependent=UNKNOWN`, physical-access independence is false, and active remote measurement requires new user authority;
- Web: evaluator diversity is externally constrained and human preference remains a different oracle class;
- Game: claims about understandable/consequential play require real players;
- Finance GVA: credential/source authority can eliminate nominal opportunities before Agent engineering begins;
- Security is the positive control: its current architecture already separates sensor telemetry, evaluator judgment, management authority and independent world truth.

The scarcity is often an **external authority, independent observer, credential, physical carrier, or fresh measurement**, not another reasoning loop.

Sensor/Observer is retained as a first-class entity role, but owner/provider-native sensors remain authoritative. There is no universal Sensor service.

## EG5 — simulator / adversary

Finance, Security and Game independently demonstrate that simulation is already a real entity class:

- Finance simulates capital transitions and counterfactual owner consequences;
- Security has Contest/Range/KVM adversarial worlds and independent sensors;
- Game owns deterministic Scenario/Genesis/reducer/replay trajectories.

Their stable research intersection is thin: exact initial/environment identity, explicit intervention, transition/trajectory, observation distinct from authoritative state, consequence, and replay/provenance where needed.

Their actual state, action, oracle and consequence semantics remain domain-specific. Therefore domain simulators survive, while a universal `Ordivon Simulator` is rejected.

Agent adversary, deterministic fuzzer/mutator, simulator, hidden oracle and verifier are also kept distinct; sharing the word “adversarial” is not an ownership argument.

## EG6 — human as scoped sensor

Human evidence is retained only where the claim is actually about humans.

Mechanical correctness does not require a human ballot. Bounded reversible design can use Agent judgment without claiming population preference. But comparative human preference, comprehension, trust, memory, emotion and game experience require claim-matched target observers when those stronger claims are made.

The experiment records a **research-only** minimal human-response evidence envelope. It is not promoted. Promotion requires real observations in at least two materially different owner domains and proof that the same minimal fields reduce ambiguity.

A mandatory human approval gate remains rejected.

## EG7 — Archivist / Indexer negative result

A disposable SQLite FTS5 index was built over **2,736** current revision-bound documents / about **25.9 MB** of text. The temporary index was about **37.2 MB** and was deleted after the run.

Six frozen retrieval queries asked for known canonical owner sources.

- global FTS top-10 expected-source hit rate: **4 / 6**;
- owner-scoped FTS top-10 hit rate: **4 / 6**;
- owner scoping did not improve the result.

Related research and implementation prose displaced canonical sources for Security sensor/world-truth and Harness Run queries. This is precisely the failure a naive “put everything in Memory/vector search” story ignores: relevance is not authority.

Therefore a dedicated Archivist/index service is **deferred**. Git, `rg`, owner authority maps and explicit source routing remain the stronger baseline. Reopen only after measured rediscovery failures and a richer provenance/authority-aware ranking candidate actually beats that baseline.

## EG8 — final entity dispositions

| Entity role | Disposition |
| --- | --- |
| Agent / open-ended cognition | retain |
| deterministic executor / state machine | retain |
| formal verifier / constraint checker | retain role, owner-local |
| optimizer / resource allocator | retain role, owner-local decision support |
| statistical estimator / calibrator | retain, high priority |
| sensor / observer + external authority/resource | retain, high priority |
| domain simulator | retain domain-local |
| adversary / fuzzer / mutator | retain as distinct roles |
| human-response sensor | retain only when claim-matched |
| dedicated Archivist / indexer | defer |
| universal Capability Router | reject/defer current |

Machine-readable dispositions are in [`results/eg8-entity-dispositions.json`](results/eg8-entity-dispositions.json).

## World-model update

The system-level principle is now narrower than “Agent-first”:

```text
open-ended search / hypothesis / meaning       -> Agent
exact durable mechanics                        -> deterministic substrate
finite logical invariant / counterexample      -> Verifier
bounded combinatorial search / certificate     -> Optimizer
stochastic uncertainty / calibration            -> Estimator
fresh external state                            -> Sensor / native authority
counterfactual trajectory                       -> domain Simulator
adversarial search                              -> Agent adversary or deterministic fuzzer, kept distinct
human consequence                               -> claim-matched Human sensor
long-term source truth                          -> owner + Git/provenance, not relevance ranking
```

This is **problem-first comparative capability ecology**. An entity may contribute evidence or calculation without acquiring the owner’s objective, constitution, authority, or truth.

## Immediate capability priority

The next resource budget should favor three shortages before inventing more orchestration:

1. **Observation/resource acquisition** — real venue, carrier, measurement, credential and independent observer capacity;
2. **Independent verification** — exhaustive/property/formal checks where example tests are brittle;
3. **Statistical estimation** — explicit uncertainty wherever stochastic Agent/experiment evidence is being interpreted.

Optimizer and Simulator work should remain demand-driven and owner-local. Dedicated Archivist and universal routing infrastructure failed to earn promotion in this round.
