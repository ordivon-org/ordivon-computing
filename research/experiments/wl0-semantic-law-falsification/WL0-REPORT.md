# WL0 — Semantic Law Falsification Report

## Question

Do the five compressed cross-project laws represent independent failure boundaries, or are they merely attractive restatements of existing Ordivon vocabulary?

The candidates under test were:

1. **L1 Reality–Representation Separation**
2. **L2 Binding Law**
3. **L3 Partial Observation**
4. **L4 Scoped Authority**
5. **L5 Causal Non-Collapse**

WL0 deliberately does not ask whether these laws are philosophically universal. It asks a narrower engineering-scientific question: can removing each distinction independently create a reproducible wrong conclusion or unauthorized consequence in a world model structurally similar to current Ordivon workloads, and does restoring only that distinction eliminate the failure without blocking ordinary benign work?

## Baseline

The exact Computing source under test is `bb4c56e4d5c7d86471330f1ec413ed0f73c92e03` in Runtime Workspace `computing-wl0-law-falsification-20260810`.

A first attempt to execute the documented `python3.12` reproduction assumption failed because the current Runtime service PATH contains no `python3.12`. The physical interpreter was then resolved explicitly and the current Semantic Kernel suite was run with:

- exact interpreter `/usr/local/libexec/ordivon/python/cpython-3.12.13-ordivon-pyc1-linux-x86_64-gnu/bin/python3.12`;
- `PYTHONPATH=src:../../../packages/ordivon-protocol/src`;
- result: **100/100 tests passed**;
- Runtime Job: `job-019febee-893b-7922-b124-e63560cf0533`.

This failed first attempt is not counted as WL0 evidence, but it usefully demonstrates the reason owner-native current observation outranks a documented execution representation.

During WL0, Computing owner main advanced independently to `3ea6e21fcc59b48b7bb10c3969209046aa980104`. A path-overlap check found no concurrent changes to `core/foundations.md`, the experiment index, or the new WL0 directory, so the experiment commit was cleanly cherry-picked onto that owner revision as `9609fad`. On the rebased exact source, WL0 tests again passed **7/7** (Runtime Job `job-019febf4-ef85-7611-8651-94284d21a134`) and the full Computing conformance gate again passed (Runtime Job `job-019febf5-19db-7d03-aaa4-4597f46535b3`). This second acceptance includes the concurrently advanced Crosscut P5 surface rather than the earlier P0–P4 set.

## Experiment design

Each law receives an isolated world in which the other four distinctions are held non-problematic.

| Law | Distinction removed | Isolation property |
|---|---|---|
| L1 | omitted representation field is treated as a reality value | static world; no temporal drift, authority, or effect |
| L2 | old/foreign evidence is reused from payload equality | current reality is known; only entity/revision binding differs |
| L3 | no visible event is interpreted as no world change | initial observation is accurate and correctly bound |
| L4 | Agent selection/mechanical reachability is treated as authority | current state is known; no stale evidence or uncertain effect |
| L5 | mechanical success is treated as semantic completion | capability, selection, admission, and execution are all valid |

For every law, acceptance requires: a non-empty hazard set, a concrete naive error, zero guarded errors on the hazard set, and successful guarded operation on benign cases. This prevents an always-reject implementation from passing.

## Primary campaign

The deterministic campaign ran **20,000 trials per law, 100,000 trials total**. Receipt: `evidence/wl0-law-falsification.json`; receipt digest `sha256:e9349c7e2397ec90d605f05c436449dac175ac767917be08b71185e44899a14a`; Runtime Job `job-019febef-d883-7d22-9945-13471647b0cc`.

| Law | Hazard trials | Naive errors | Guarded errors | Guarded benign successes |
|---|---:|---:|---:|---:|
| L1 | 4,438 | 4,438 | 0 | 10,995 |
| L2 | 4,443 | 4,443 | 0 | 11,026 |
| L3 | 5,985 | 5,985 | 0 | 14,015 |
| L4 | 13,398 | 13,398 | 0 | 6,602 |
| L5 | 8,951 | 8,951 | 0 | 11,049 |

The randomized tests are not a probability estimate for production failures. The distributions are deliberately synthetic. Their role is counterexample search and guard ablation.

## Seed robustness

A second campaign changed seed and repeated **64 seeds × 2,000 trials × 5 laws = 640,000 additional trials**.

Every seed for every law produced hazard cases, every law retained benign success, and every guarded hazard error count remained zero.

| Law | Trials | Hazard / naive errors | Guarded errors |
|---|---:|---:|---:|
| L1 | 128,000 | 28,774 | 0 |
| L2 | 128,000 | 28,531 | 0 |
| L3 | 128,000 | 38,330 | 0 |
| L4 | 128,000 | 84,907 | 0 |
| L5 | 128,000 | 57,664 | 0 |

Evidence: `evidence/wl0-robustness-sweep.json`; Runtime Job `job-019febf0-7eb4-7433-9a3d-addf7b53aaf7`.

## Physical probes

The primary receipt also includes five small physical probes:

- **L1:** a real selected JSON projection reports `service=ready` while the represented object additionally contains `latent_compromised=true`; the naive absent-field default produces `safe`.
- **L2:** two physically distinct owner-bound files (`runtime.state`, `finance.state`) contain byte-identical payloads and therefore identical SHA-256 digests. Content identity alone does not collapse entity/owner identity.
- **L3:** a file is observed as `revision-1`, then physically becomes `revision-2` with no event transport. The cached observation is stale despite absence of an event.
- **L4:** mechanically writable targets exist for two owner labels. Filesystem reachability by itself carries no semantic owner authority.
- **L5:** exact `/usr/bin/true` exits zero while a domain target remains `before` instead of the semantic goal `after`.

These probes are intentionally small. They show that the distinctions are not artifacts of the randomized state machines.

## Existing Semantic Core corroboration

WL0 did not change the existing Semantic Core. Six current owner-native boundary tests were selected because they independently protect the same failure classes:

- transport loss remains UNKNOWN rather than FAILED;
- cancellation request is not terminal cancellation;
- observation cannot bypass verification into Fact;
- a role-specific signer cannot escalate to another role;
- Effect and Binding separation survives Journal restart;
- Dispatch identity cannot cross Effects.

All **6/6 passed** on the same exact source. Runtime Job: `job-019febf0-c4cc-7fc2-92f3-74fa5fb3fd8e`.

The complete pre-existing Semantic Core suite also remained **100/100 green**. The WL0 experiment itself passed **7/7 tests**, Runtime Job `job-019febf0-049b-74d3-9813-49a908ee55dd`, and its source compiles cleanly, Runtime Job `job-019febf1-3c8e-7ee2-b570-764e579fcf4a`.

The full Computing conformance gate passed after the WL0 files and experiment index were added. It covered compileall, ruff, content checks, foundational docs, world-model loop, research method, responsibility map, research portfolio, protocol, external contract, Semantic Core, task continuation, Track-R, evidence/conformance, Crosscut P0–P4, and Rust canonical vectors. Runtime Job: `job-019febf3-0a63-7270-91bc-56242aba41d4`. Content remains advisory `DEGRADED` with **0 blocking failures**; WL0 introduced no release blocker.

## Cross-project corroboration

Current owner work independently exposes the same boundaries without using WL0's experiment implementation:

- **L1:** Security Task `task:security:cage-structured-uncertainty-retention-20260810` revision 2 records that Harness can retain unresolved unknowns while a Security adapter currently collapses them to an empty list. This is an active representation-integrity defect, not a synthetic example.
- **L2/L3:** Crosscut Task `task:ordivon:crosscut-rsi-foundations-20260810` revision 7 records `binding_changed` for old Runtime evidence after the owner revision moved, and experimentally establishes that owner events are acceleration hints rather than completeness evidence.
- **L4:** Finance Task `task:finance:l0-live-capital-20260810` revision 8 requires an independently administered C2 executor principal and purpose-separated authority/effect signers before high-assurance capital activation. Agent knowledge or local execution reachability is deliberately insufficient.
- **L5:** the same Finance task preserves ambiguous outcome/replay-before-world requirements; Game Task `task:game:station-zero-v3-playtest-validation-20260809` revision 10 keeps registration/deletion decisions unresolved even after mechanical substrate validation because the required human evidence is still 0/11.
- **L5/C1 boundary:** Harness+Host Task `task:harness-host:rsi-p4-20260810` revision 3 has already falsified two Agent-selected target hypotheses after 203 observation rounds and is correcting the experiment runner so `no causally demonstrated target` can terminate without manufacturing a mutation.

These references remain owner-native facts; this report does not take authority over their domain state.

## Independence verdict

All five laws survive the first independence attack.

### L1 survives independently

The minimal counterexample is static. There is no stale cache, no authority decision, and no intervention. A selected representation can simply omit a property that exists in reality. Binding or causal-stage laws do not repair an inference that invents a value for an omitted property.

### L2 survives independently

L1 alone is insufficient. Even when an evidence payload is represented exactly and its value is correct for its source entity, reusing it for another entity/revision can be wrong. Binding is therefore not reducible to representation/reality separation.

### L3 survives independently, with a narrower scope

The initial representation and binding can both be correct. The failure appears only when the world changes without a complete observation signal. The sharper law is therefore conditional: **absence of observed change may imply no change only when a complete observation contract has itself been established for the relevant transition class.** Ordivon's current owner event surfaces do not generally provide that completeness.

### L4 survives independently

A caller can know current reality exactly and choose an appropriate effect while still lacking authority to perform it. Epistemic correctness cannot manufacture institutional or resource authority.

### L5 survives independently, with an equivalence escape hatch

A mechanically successful operation can fail to cause the intended world transition or can cause a transition that does not satisfy the domain goal. The sharper law is: **causal stages must remain distinct unless a domain contract proves a specific equivalence.** Pure deterministic functions may legitimately collapse some stages; external-effect systems may not assume that collapse.

## Law wording after falsification pressure

WL0 keeps five laws but narrows their wording:

1. **L1 — Representation distinction:** a representation and the reality it represents are distinct semantic objects; omission, projection, or inference cannot silently manufacture represented fact.
2. **L2 — Applicability binding:** an actionable mutable-world Claim or Evidence item is valid only under the identity/scope/revision/conditions it established, unless a stronger domain contract proves broader applicability.
3. **L3 — Observation completeness:** absence of observed change is evidence of no change only under a proven complete observation contract for that transition class; otherwise revalidation or uncertainty remains necessary.
4. **L4 — Scoped authority:** knowledge, selection, or mechanical reachability does not grant authority; authority over truth admission or consequence is explicit and scope-bound.
5. **L5 — Causal non-collapse:** possibility, selection, admission, intervention, transition, observation, and semantic consequence remain distinct unless the relevant domain contract proves an equivalence.

## Rejected new laws

WL0 does **not** promote additional laws for:

- `Unknown != false/empty/absent` — this is a consequence of L1 + L3;
- `Capability != consequence`, `Selection != authority`, `Intervention != transition`, or `Mechanical success != semantic success` — these remain useful project-level formulations but are compressed by L4/L5;
- `Abstention is valid` — retained as an Agent constitution principle, not a descriptive law of reality;
- `Shared semantic law != shared implementation` — retained as an architecture principle, not a world law.

## Effect on the semantic substrate

WL0 strengthens, but does not prove universally, the current candidates:

- **Representation** remains necessary because L1–L3 require a first-class distinction between Reality and Agent-held/projected semantic state.
- **Dynamics** remains useful because L5 needs a distinction between possible/admissible transitions and transitions that actually occur.

No new primitive is earned by this round.

## Core assimilation decision

**Do not modify `core/foundations.md` in WL0.**

The current Core already contains the required foundations in A2, A6, A7, A9, and A10, and the prior portfolio reconciliation explicitly found the cross-project pattern derivable without forcing a new World Model round. WL0 adds adversarial evidence and a smaller five-law compression; it does not yet prove that replacing or rewriting the existing canonical foundations would improve Agent work.

This is deliberate contraction: preserve the falsifiers and evidence first; change Core only if the compressed law form later reduces real retrieval, reasoning, or reform friction in a separate ablation.

## Verdict

WL0 **supports all five laws within their narrowed applicability domains**. None was falsified or merged away in this round. More importantly, the experiment found limits on two over-broad wordings: observation incompleteness is conditional on lack of a completeness proof, and causal non-collapse permits explicitly proven domain equivalences.

The result is therefore not “five timeless axioms.” It is a smaller, sharper set of cross-project invariants with executable counterexamples, guard ablations, physical probes, current owner corroboration, and explicit escape conditions.
