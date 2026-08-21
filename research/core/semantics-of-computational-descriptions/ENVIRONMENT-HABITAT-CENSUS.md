# SCD Environment / Habitat Census — Rounds 1–2

Status: **EMPIRICAL / EXPLANATORY / NON-AUTHORITATIVE**.

This document records where Semantics of Computational Descriptions (SCD) has actually become load-bearing in current Ordivon systems, where the relevant distinction is already correctly realized by another owner, and where current evidence says not to materialize anything. It is a consumption/navigation artifact, not a new SCD Foundation, ontology, service, schema, environment object, or owner-wide migration plan.

The census does not define `Habitat` as a new SCD primitive. The term is only a convenient name for a real description-mediated consumer situation under audit.

## 1. Empirical scope rule

A subsystem does not enter SCD scope merely because it stores or transforms descriptions. A candidate locus becomes SCD-relevant only when a computational description or representation is asked to carry semantic responsibility for a named judgement and a semantic distinction is load-bearing for the downstream consequence.

Operationally, ask:

1. What description or representation is consumed?
2. What transformation/projection/recovery step mediates it?
3. What exact judgement is the consumer trying to establish?
4. What consequence, continuation or recovery decision depends on that judgement?
5. Which distinction could be deleted while keeping ordinary mechanical facts unchanged?
6. Does deletion change the justified judgement/consequence, or does the existing owner boundary already prevent the invalid inference?

A positive deletion result admits a local SCD consumption pressure. A correct `NO_CHANGE` is also a valid result when the existing consumer/owner already preserves the distinction.

The earlier working coordinates — authority, description, transformation, qualification/context, consumer, judgement, consequence and recovery — remain observation coordinates only. They are not promoted to a universal record type.

## 2. Round-1 current source fences

The census revalidated the current repository heads used by this round:

- Computing / SCD: `acc44e932fd70c2df368f0f27dddaa7eebe297cf`;
- Harness: `b14df3e0aa5764f9661c4b0881774f4434b8353a`;
- Atlas: `dab5fb1d7561b7278f681b8f97e16b3127c058a9`;
- Runtime: `fa7c5bbf4b9fae661bd7588f6d7e8f68c216e469`;
- Security: `910c6541b830945c889dd31d784c701d59a960f7`.

These are source fences for this census, not permanent semantic currentness claims.

## 3. Habitat classes

The census uses four empirical classes:

- **ADMITTED NATURAL POSITIVE** — a real consumer and deletion/control evidence show a semantic distinction changes a justified judgement, consequence or required recovery.
- **ALREADY-SUNK / NEGATIVE CONTROL** — the pressure is real but the current owner/consumer already preserves the distinction; SCD consumption therefore says `NO_CHANGE` rather than add machinery.
- **CANDIDATE** — a plausible current description-mediated judgement boundary exists, but no natural deletion-essential consumer result has yet been demonstrated.
- **REOPEN-ONLY** — the regime is already representable by current SCD standing; reopen only if a new counterexample defeats that representation.

These labels are census statuses, not owner semantic standing.

## 4. H1 — authority-fenced semantic source recovery

Class: **ADMITTED NATURAL POSITIVE**.

Observed path:

`owner publication -> exact authority/version/digest/subject projection -> Research Agent standing -> continuation decision`.

Current Harness implements an application-local observation surface in which caller-supplied source-authority evidence is bound into the Tool Grant and execution binding. An authority-statement projection is admitted only when the complete source digest equals the bound `AuthorityVersionRef`. Harness explicitly records `harnessMintsOwnerTruth=false`.

The decisive evidence is the frozen First-Look control/treatment pair. Under the same query, source, model and bounded budget, search-only did not recover the required Human owner standing, while exact authority-fenced bounded source read/projection recovered `HISTORICAL_PRESERVED` and completed the candidate.

SCD significance:

- exact bytes/readability do not by themselves establish owner semantic authority;
- search matches do not by themselves establish the target standing;
- source authority/currentness and target judgement are load-bearing distinctions;
- the successful carrier is local caller binding + Tool/source fence + deterministic projection, not a global SCD service and not generic prompt prose.

This is the first round-1 habitat in which deletion evidence establishes positive consumer value.

## 5. H2 — Runtime execution projection to semantic completion

Class: **ALREADY-SUNK / NEGATIVE CONTROL**.

Observed path:

`Runtime Job/Attempt evidence -> Agent/upper-layer consumer -> Task/domain completion judgement`.

Current Runtime exposes exact mechanical execution state, including `executionDisposition`, delivery/recovery fields and result availability, while its Agent-facing contract explicitly fixes `semanticCompletionEvaluated=false`. Runtime documentation and public Tool descriptions state that successful execution and retained artifacts do not imply Task/domain semantic completion.

SCD significance:

`RuntimeSuccess != SemanticCorrectness` and `ExecutionSuccess != SemanticCompletion` are already physically represented at the owner boundary. There is no current deletion-essential reason to add an SCD field, Runtime semantic-completion authority, or cross-owner standing service.

Consumption result: **NO_CHANGE**. Any future consumer that collapses execution success into domain completion would create a new local consumer defect; it would not justify moving semantic completion into Runtime.

## 6. H3 — owner publication to Atlas projection/navigation

Class: **ALREADY-SUNK / NEGATIVE CONTROL**.

Observed path:

`owner current publication -> Atlas source-fenced generated projection -> research/navigation consumer`.

Current Atlas explicitly states that it is not semantic truth authority. It verifies owner `AuthorityVersionRef`, immutable publication digest, current-recovery locator and source fence, and emits generated projections carrying those qualifications. Missing explicit result classification stays `UNKNOWN` rather than being fabricated. Curated synthesis is explicitly non-authoritative.

SCD significance:

`Projection != OwnerTruth`, `Navigation != SemanticAuthority`, and `SharedTransport != SharedOwner` are already preserved by the actual consumer surface.

Consumption result: **NO_CHANGE**. Centralizing owner truth into SCD or adding a generic semantic layer above Atlas would erase a boundary the current design already gets right.

## 7. H4 — Host lifecycle / semantic links / richer handoff

Class: **ALREADY-SUNK / NEGATIVE CONTROL** at the current evidence boundary.

Host archaeology tested typed semantic links, richer handoff pressure and generic source-binding. Typed links sometimes improved exact identity/navigation recovery, but did not produce stable decision/control gain. No natural richer-Handoff failure was found. Generic ContextSourceBinding was historically removed after a real-consumer audit, while current owner-specific dependency/currentness mechanisms solve the concrete stale-evidence cases.

SCD significance:

Host continuity state and semantic owner standing are different facts, but this distinction does not currently require new Host schema. `Completed != Achievement/Value/CurrentSemanticAuthority` is already preserved by the owner architecture.

Consumption result: **NO_CHANGE**. Do not materialize persistent semantic links, WorkingCheckpoint v2, Journal v6 or a richer Handoff merely to make SCD visible.

## 8. H5 — Security evidence current applicability

Class: **INDEPENDENT CROSS-OWNER POSITIVE PRESSURE SHAPE**; Security retains source-domain authority.

Security EC1 demonstrates a distinct but structurally useful locus:

`retained evidence/derivation -> exact semantic dependency/current-authority comparison -> applicability judgement -> defensive decision`.

A retained projection can remain byte/integrity-valid while becoming `STALE_NOT_APPLICABLE` because a constitutive semantic dependency advanced. A metadata-only source advance can remain applicable. If current authority cannot be observed, applicability becomes `UNKNOWN` rather than guessed from age. A coarse repository-revision rule would create false staleness.

SCD significance:

This is independent evidence that semantic currentness is judgement/dependency-relative rather than equivalent to artifact integrity or repository freshness. But Security owns the actual evidence/applicability semantics; SCD should not centralize them. SCD's role is the qualified description-to-judgement boundary and the cross-owner non-entailment discipline.

## 9. H6 — performative feedback

Class: **REOPEN-ONLY**.

The hostile consumer in which deploying a predictive description changes the future data-generating distribution was expressible using existing SCD Situation / Context / Change / Support / currentness distinctions. The fixture established `StaticSemanticValidity != ClosedLoopSemanticStability` and `OldSupportStanding != PostDeploymentCurrentStanding` without forcing a new Foundation or core primitive.

Reopen only if a future source-response regime cannot be represented without violating current K0.2 owner/context/support boundaries.

## 10. Candidate not yet admitted — summary / handoff sufficiency

Historical SCD A3/A4 evidence remains informative: an exact revision-fenced reference may preserve recoverability without copying all semantics, while a frontier-only summary may preserve roadmap direction but fail a stronger safe-continuation contract.

However, current Host archaeology found no natural richer-Handoff failure. Therefore P1 remains a **CANDIDATE**, not an engineering backlog item. Do not manufacture a synthetic failure just to complete habitat coverage.

## 11. What Round 1 says about “sinking” SCD

Current evidence favors heterogeneous local carriers rather than one SCD runtime object:

- caller/source-authority binding;
- exact digest and subject projection;
- explicit negative semantic boundary fields;
- owner-qualified currentness/recovery pointers;
- consumer-local admissibility/applicability logic;
- retained richer provenance for recovery while exposing a bounded consumer projection.

The recurring structure is therefore not `call SCD`. It is:

`description -> load-bearing semantic distinction -> qualified judgement -> consequence/recovery`,

with each owner keeping the physical or source-domain truth it already owns.

SCD “sinks” successfully when a semantic distinction becomes part of the local decision boundary while SCD itself does not acquire unrelated execution, capability, permission, source-domain or orchestration authority.

## 12. Current anti-rules and next gate

Round 1 does not justify:

- a global SCD Environment object;
- SCD daemon/service/registry/standing engine;
- universal `scdMetadata`;
- mandatory prompt exposure of semantic distinctions;
- Runtime-owned semantic completion;
- Atlas/Host/Security truth centralization;
- a shared habitat schema inferred from H1 alone.

The next experiment must start from a **current named consumer gap**. The strongest default search target is an Agent-facing exact judgement boundary where a consumer-local owner-qualified standing projection can be deleted against a strong baseline without embedding the answer. If no such natural gap exists, the correct result is to retain the current sparse field rather than manufacture coverage.


## 13. Round 2 — H7 cross-owner description adequacy for normative judgement

Class: **ADMITTED NATURAL POSITIVE**, with current disposition **owner-local preservation / NO NEW SCD COMPONENT**.

Round 2 consumed the independent current Normative actual-consumption line rather than constructing an SCD-specific fixture. Three heterogeneous practical consumers now reproduce the same description-adequacy pressure while retaining their own owner semantics.

### H7-A — protected-artifact mutation

A physical action may remain extensionally the same:

`Delete(x)` over the same path/object bytes,

while the relevant institutional world differs in protected status, owner, role, currentness or provenance. Physical identity, filesystem capability and operation success therefore do not determine whether the deletion is permitted, prohibited or currently unsupported. If the consumer projection preserves only physical identity/action mechanics and deletes the institutional distinctions required by the normative query, it merges source situations that can require different prospective normative standings.

### H7-B — Finance external commitment/currentness

A fresh read-only Finance observation established an owner-native semantic effect contract with `effectClass=READ_ONLY`, no credential access, no environment mutation, no external financial write, no financial submission and no authority mutation. The executor is disabled, the configured venue profile remains `finance-okx`, and the current egress observation is `UNKNOWN` / not-current (`listenerReachable=false`, `watchdogDisposition=no-eligible-member`, `currentEgressMatches=false`).

The load-bearing separations are:

- `CannotCurrentlyObserve(permission) != NoPermission`;
- `CannotCurrentlyObserve(permission) != Prohibited`;
- `CannotSubmitNow != MayNotSubmit`;
- configured venue capability/authorization does not establish a user/domain mandate for a particular action.

Collapsing these states into one boolean permission field would change the justified normative judgement.

### H7-C — Harness delegation/currentness

Current Harness architecture distinguishes Mandate, Strategy, RunContract, Receipt, CompletionProposal and independent StrategyEvidence. Exact prior-attempt evidence is bound to the exact Mandate digest, so a changed same-named Mandate cannot silently inherit historical receipts.

This proves historical delegation/admission/execution lineage but does not establish continued authority after a later revocation or authority change. The current public Harness surface intentionally does not manufacture a first-class Agent-to-Agent revocation lifecycle. Therefore:

- `HistoricalAuthorityEvidence != CurrentStanding`;
- `Capability/Grant != NormativePermission`;
- `Occurrence != ContinuedAuthority`.

When current revocation/authority lineage is absent, a query such as `May Agent B continue?` must remain `UNKNOWN/UNSUPPORTED` rather than inherit permission or prohibition from historical evidence.

### SCD boundary

H7 does **not** make Normative truth SCD-owned. SCD's role is narrower: whether the consumed action/object/authority description preserves the semantic distinctions required for the target judgement. Normative continues to own permission/obligation/prohibition standing; Finance, Harness, Runtime and artifact/domain owners retain their own source truth.

The three consumers therefore establish a second natural positive SCD habitat family without requiring an SCD-branded runtime object.

## 14. Judgement-relative anti-collapse criterion

H1 and H7 share a stable explanatory shape, but current evidence does not justify a shared wire schema.

Let `s` denote a source situation, `J` a named consumer judgement/use contract, and `p(s)` the description/projection actually supplied to the consumer. Let `Gamma_J(s)` denote the target standing/consequence information that is justified for `J` from the full source situation.

A strong exact-standing sufficiency condition is:

`p(s1) = p(s2)  =>  Gamma_J(s1) = Gamma_J(s2)`.

If two source situations are collapsed by the projection while supporting materially different target standings, the projection is semantically too coarse for that judgement unless a guaranteed pre-decision refinement/recovery route can restore the missing distinction.

This is only an explanatory judgement-relative anti-collapse criterion. It is compatible with TRAA, abstraction/refinement traditions, sufficient-state ideas and prior system-level control-distinction conservation; it is **not** claimed as a new SCD theorem, Foundation or novelty result.

H1 instantiates the failure through source-authority/currentness/target-standing recovery. H7 instantiates it through institutional status, effect role, availability/currentness and authority lineage feeding a Normative judgement.

The important consequence is:

`SemanticRequirement != UniversalFieldName`.

A load-bearing distinction may be carried by a caller binding, digest fence, authority pointer, Tool Grant, owner-native currentness observation, negative boundary field, verifier contract or consumer-local institutionalization step. What matters is preservation before the target judgement, not representational uniformity.

## 15. Round-2 ceiling and third-habitat gate

Round 2 does not admit a common SCD/Normative `FactEnvelope`, QRNA ownership transfer, a global currentness schema or any shared standing service. The current Normative line itself freezes QRNA as a consumer-local pull-first pattern and rejects a shared canonical FactEnvelope at present evidence.

Representation-sensitive Computational Possibility research is a strong **candidate pressure**: the same semantic referent can have different computational possibility under different operational presentations or access regimes, and theorem transport requires relation strength appropriate to the target computability/complexity/deployment claim. But the current CP branch has not yet reached its first named actual consumer, so it is not counted here as a third positive SCD habitat.

The next admission gate remains strict: require a current named consumer, exact target judgement/consequence and a natural deletion/control discriminator. If no third independent consumer exists, Environment Formation should phase-hold with H1 and H7 rather than standardize their common shape prematurely.
