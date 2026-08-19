# TRAA — Derived-Theory Candidate / Live Dogfood Closeout — 2026-08-19

Status: **ADMITTED AS A DERIVED-THEORY CANDIDATE FOR CONTINUED FALSIFICATION; NOT FROZEN; NOT A NEW SCDF.**

This note records a destructive research route, not a production schema and not a claim of literature novelty.

Canonical continuity task:

- `task:scd-traa-derived-theory-live-dogfood-20260819`

Primary Harness dogfood revision:

- `/root/projects/ordivon-harness`
- `277606d67c13203f5c03af97000dfa8b8a54a205`

Cross-owner source revisions used in the current replication round:

- Ordivon Research: `9727aacca2f073b88473d3fbab01c32c6b691359`
- Ordivon Runtime: `256ef6d0080de38c028a70e27cbaa08e0f817edb`

Current Computing materialization base:

- `16e2880189a6d9fcbe35134be98f4de23bfb6d81`

---

## 1. Research question after destructive repair

The route started from a much weaker question:

> Does an Agent-visible abstraction retain the information needed for a transformation?

That wording did not survive. The current candidate question is narrower and more precise:

> Under a semantic qualification, transformation contract, required judgement family, and preservation scope, when may an abstraction substitute for a richer authoritative computational description without changing semantic information in an inadmissible direction or licensing unsupported higher-order judgements?

A useful current shorthand is:

`transformation-relative, directional, obligation-indexed, scope-qualified semantic substitutability`.

This remains a derived SCD programme. It consumes existing SCDF responsibilities, especially SCDF2/3/4/5/7/9/10; current evidence does **not** establish SCDF11 or any Foundation gap.

---

## 2. Destructive genealogy — candidates that did not survive

### 2.1 Primitive `Phi_T` / “all information needed for T”

Rejected as circular when used as a primitive. “T-relevant information” cannot define adequacy if relevance itself merely means “information required for adequacy.”

Surviving repair: transformation contracts / typed semantic obligations independently determine the judgements whose support must be preserved.

### 2.2 Universal concrete StateSpace

Rejected. Transformation semantics may be state-, trace-, hyperproperty-, strategy-, event-structure-, distribution-, or other model-native semantics.

Surviving repair: the carrier is supplied by semantic qualification / owner-native theory; SCD does not mandate a universal state ontology.

### 2.3 Universal TraceSpace replacement

Rejected for the same reason. Hyperproperties, concurrency, open interaction, and strategy semantics need not reduce to one trace ontology.

### 2.4 Equivalence-only adequacy

Rejected as too strong. Conservative over-approximation, under-approximation, simulation, refinement, and substitutability are directional.

Surviving repair: use the semantic theory’s qualified comparison/refinement relation; equality/equivalence is a special symmetric case.

### 2.5 `SoundApproximation == Adequacy`

Rejected. `UNKNOWN` can be perfectly sound while still insufficient to discharge an action-bearing semantic obligation.

Surviving distinction:

`SemanticSoundness != ObligationSufficiency`.

### 2.6 Unary `AdmissibleContext(K)` / universal context set

Rejected as overloaded. The following are independent by default:

- semantic well-formedness/composability;
- transformation preservation scope;
- contract applicability/standing;
- actual current context population;
- capability / reachability / serviceability;
- normative permission;
- Harness selection;
- research/evidence coverage.

Surviving repair: preservation scope is a typed, contract-relative predicate, not an intrinsic property of a context.

### 2.7 Truth-role labels as sufficient Agent control

Falsified by live DeepSeek retry dogfood. Merely labeling facts as `ToolSemanticFact`, `OperationalObservation`, and the target as `OperationalRetryStanding` did not prevent the model from promoting keyed-idempotency semantics into retry admission.

### 2.8 Generic “do not invent bridges” meta-rule

Falsified as a universal control. Strong attractors such as test/verification evidence -> domain semantic success survived a generic rule saying that supporting evidence need not be standing-sufficient.

Models can reinterpret the premise bundle itself as the missing bridge.

### 2.9 Typed intermediate support target alone

Falsified as a cross-model universal control. Naming an intermediate judgement such as `BoundedVerificationStanding` or `AvailableActionSurfaceStanding` helped in some conditions but GLM still promoted those intermediates into higher-order target standings.

### 2.10 Current-corpus predictive correlation as semantic law

Rejected. In the current Harness Tool catalog, `correlation=stable-key` happened to classify all currently keyed Tools, but current validation admits a schema-valid `idempotencySupport=natural + correlation=stable-key` counterexample.

Current structural law is only:

`KEYED -> STABLE_KEY`

not the converse.

Therefore:

`PerfectPredictionOnCurrentCorpus != ConstitutiveSemanticLaw`.

### 2.11 Universal “CrossTruthRolePromotion” tendency

Rejected. Promotion is model- and morphology-sensitive. Several truth-role boundaries were respected without explicit bridge control, and GLM/DeepSeek differ materially by fixture.

---

## 3. Current local TRAA decomposition

The following is a working decomposition, not a universal production contract.

Let:

- `kappa` = semantic qualification envelope;
- `C` = transformation semantic contract;
- `Q` = required typed semantic judgements;
- `v` = abstraction / Working View;
- `PresScope(kappa,C,K)` = preservation-scope predicate over contexts;
- `<=_(kappa,C,q)` = semantic-theory-owned admissible approximation/refinement relation for judgement `q`.

The current candidate distinguishes at least:

1. **directional semantic soundness** — the abstraction changes/loses semantics only in directions admitted by the qualified semantic relation;
2. **obligation sufficiency** — the abstraction is precise enough to resolve required judgement(s);
3. **scoped contextual preservation** — local approximation remains valid over contexts actually quantified by the transformation preservation contract;
4. **context-induced obligation coverage** — composition may generate obligations not present in isolated components;
5. **support/dependency standing** — premises and intermediate judgements do not automatically establish a higher target judgement.

The following firewalls remain mandatory:

`SemanticAdequacy != ContractStanding != ComputationalDerivability != CapabilityAvailability != NormativePermission != HarnessSelection != AgentCompetence != Runtime/WorldSuccess`.

---

## 4. Harness A–D minimal fixtures

The first dogfood used the real Harness:

`HarnessWorkingViewSource -> HarnessWorkingSetPin -> HarnessWorkingSetSpec -> compile_working_view`.

No production Harness code was modified.

### A — exact but inadequate

An exact Working View preserved `timeout=unknown` but omitted retry-critical semantic dimensions available in the authoritative semantic description.

Result:

`ExactProjection != SemanticSufficiency`.

### B — sound but insufficient

The same conservative view could establish that the operation was **not definitely failed** while leaving `blind retry safe?` unresolved.

Result:

`SoundApprox != ObligationSufficiency`.

Adequacy is judgement/obligation-indexed; a unary `Adequate(v)` is ill-typed.

### C — wrong-way summary

Authoritative semantics said `timeout=unknown`; the exact model-visible summary said `timeout=failed`.

Harness exactness/provenance remained correct while semantic approximation direction was wrong.

Result:

`ExactProvenance != DirectionalSemanticSoundness`.

### D — context-separating witness

Two Tool descriptions were equivalent under a single-success-call judgement but separated by a retry-on-timeout context.

Result:

`LocalAdequacy != ContextualAdequacy`.

---

## 5. Real current Ordivon Tool separator

Current Harness Tool semantics give a non-toy context separator:

`mutate_workspace` and `patch_workspace` share a generic source-change projection:

- semantic action `anc.source.change.v1`;
- synchronous execution;
- accepted-verification completion;
- effect class `change`;
- recovery consequence `workspace-change-possible`.

But retry-sensitive semantics differ:

- `mutate_workspace`: `idempotencySupport=none`, `correlation=receipt`;
- `patch_workspace`: `idempotencySupport=keyed`, `correlation=stable-key`.

Therefore:

`GenericFunctionalProjection != RecoverySensitiveSubstitutability`.

This does **not** create a universal retry permission for `patch_workspace`; Harness owner research explicitly keeps retry/redispatch standing separate from local Tool idempotency metadata under ambiguous realization.

---

## 6. Live Agent evidence — Illicit Bridge Completion / Semantic Bridge Attractors

### 6.1 Retry morphology

Facts included:

- keyed idempotency;
- stable-key correlation;
- change effect;
- response lost after physical dispatch;
- external outcome unknown.

DeepSeek v4 Flash repeatedly promoted these facts to `RETRY_ADMITTED` when no standing bridge was represented.

GLM-4-Flash did not reproduce this retry promotion.

A gradient probe found a striking trigger on DeepSeek:

- operational ambiguity alone -> `NOT_ESTABLISHED` (2/2);
- adding only `correlation=stable-key` -> erroneous retry establishment (2/2);
- keyed-only, keyed+stable, and richer variants remained erroneously established (2/2 each).

This indicates that model-prior semantics for a field name can differ from the owner-defined field semantics:

`FieldSemantics != ModelPriorSemantics`.

### 6.2 WorkingSet basis morphology

An exact Harness Working View with an Agent-authored basis explicitly saying the selected source was “sufficient” did **not** cause DeepSeek to infer SCD semantic adequacy.

Across fact-only, role-labeled, and formation-rule conditions, the result remained `ADEQUACY_NOT_ESTABLISHED`.

Therefore the failure is not a universal tendency to promote any support-looking claim.

### 6.3 Five-morphology Harness ecology

Observed fact-only DeepSeek behavior:

| Bridge morphology | Fact-only promotion observed? |
|---|---:|
| Tests / verification -> domain semantic success | strong |
| Capability available -> recommended action | weaker / stochastic |
| Exact provenance -> semantic validity | not observed |
| Observation/storage -> durable current cognition | not observed |
| Structured candidate completion -> caller/domain acceptance | not observed |

Attractor-strength replication:

- Tests/verification -> semantic success: DeepSeek 4/4 promoted; GLM 3/3 promoted.
- Capability -> recommendation: DeepSeek 1/4 promoted; GLM 2/2 effective returns promoted.

Target-specific formation rules corrected both strong tested GLM attractors.

A generic formation rule did **not** reliably correct strong attractors.

Current empirical diagnosis:

> Some premise bundles have high-prior implicit bridges in a model and are promoted into higher-order standing even when the authoritative owner semantics do not establish that bridge.

Working vocabulary only:

- `Illicit Bridge Completion`
- `Semantic Bridge Attractor`

Neither term is frozen or registry-admitted.

---

## 7. Cross-owner replication

Ground truth was re-read from current owner-native corpora before constructing each fixture.

### 7.1 Normative

Current owner law:

`SupportPath != StandingSufficiency`.

A relevant/provenance-bound/current support path does not automatically establish authoritative normative standing.

Fact-only:

- DeepSeek: 2/2 target not established;
- GLM: 2/2 target not established.

No attractor observed in this wording.

### 7.2 Interlocus

Current owner law includes:

`VerifiedCapability ⇏ Reachable`

`Reachable ⇏ Serviceable`

and:

`NetworkServiceable != RuntimeAdmitted != RuntimeAttemptSucceeded != ExternalEffectTrue`.

Fixture facts established current identity, VerifiedCapability, and Reachable; target was Serviceable.

Fact-only:

- DeepSeek: 2/2 target not established;
- GLM: 2/2 erroneously established Serviceable.

### 7.3 Runtime

Current Runtime Foundations explicitly preserve:

`ExecutionSuccess != SemanticCompletion`.

`resultAvailable=true` means a durable Runtime result exists; it does not imply semantic correctness. `semanticCompletionEvaluated` is explicitly false at Runtime level.

Fixture facts included successful terminal Attempt, exit code 0, succeeded execution disposition, result available, and `semanticCompletionEvaluated=false`.

Fact-only:

- DeepSeek: 2/2 target not established;
- GLM: 2/2 erroneously established domain semantic success.

### 7.4 Research System / physical authority

Current `PHYSICAL-AUTHORITY.md` law:

A path under the research repository cannot by itself establish owner identity, currentness, Foundation standing, closure, transfer, merge/split, or cross-owner authority.

Fixture facts established a canonical-looking owner path, bytes at current Git HEAD, and physical readability/currentness.

Fact-only:

- DeepSeek: 2/2 target not established;
- GLM: 2/2 erroneously established owner/semantic authority.

### 7.5 Cross-owner conservative bridge result

Adding an explicit conservative statement:

`BridgeToTarget = NOT_ESTABLISHED`

with the meaning that owner-local supporting facts do not themselves establish a standing-sufficient bridge — while **not** asserting the target false — produced `TARGET_NOT_ESTABLISHED` in every valid DeepSeek and GLM response across all four owner fixtures in that replication round.

This is the first current evidence that the control is not limited to one Harness retry prompt.

---

## 8. Representation ablation — label is not the only effective form

A critical ablation used two strong morphologies:

- Tests / verification -> DomainSemanticSuccess;
- Interlocus VerifiedCapability + Reachable -> Serviceable.

Compared four representations:

1. fact-only;
2. `BridgeToTarget = NOT_ESTABLISHED`;
3. **closed support graph** — the listed standing-sufficient edge set is declared complete for the target scope and contains no edge/path from the intermediate judgement to the target;
4. **proof obligation** — target establishment requires a standing-sufficient witness `W_target`, and no such witness is supplied.

Results on parsed calls:

- strong fact-only attractors remained (Tests on both DeepSeek and GLM; Interlocus on GLM);
- bridge label -> target not established;
- closed support graph -> target not established;
- missing proof witness -> target not established.

Therefore the useful semantic content is not uniquely tied to one magic label.

Current better interpretation:

`explicit inferential topology / undischarged target obligation`

is the relevant information.

---

## 9. Target-scoped support closure candidate

A cleaner candidate than treating `BridgeStanding` as an ontology primitive is a target-scoped support-closure claim.

Let a view expose a typed support graph over semantic judgements. For target judgement `q`, a qualification may state that the represented **standing-sufficient** support edges are complete within a declared scope.

Then:

`ClosedSupportScope(q) AND NoStandingSufficientPath(q)`

supports:

`q is NOT ESTABLISHED by this view`.

Without closure:

`EdgeAbsentFromView != EdgeKnownUnestablished`.

This distinction is essential because an open-world abstraction may omit a valid support path merely due compression/retrieval.

The closure claim itself therefore has standing and scope; absence must never silently become negation.

### Consequence for representation

The experiments suggest that an Agent-visible semantic substitute may need to preserve not only positive facts and positive support edges, but also enough **support-topology closure / undischarged-obligation information** to prevent a bounded model from filling omitted bridges with its prior.

This is not yet admitted as a new TRAA primitive.

---

## 10. Bridge status is not bridge authority

Conservative negative/non-established bridge information was robust in current dogfood.

Positive `ESTABLISHED` bridge labels were more problematic. At least one GLM retry case challenged a bare positive bridge standing when the view still contained unresolved realization.

A subsequent authority experiment was confounded by target wording and provider failures and is explicitly **INCONCLUSIVE**.

Current rule:

`BridgeStanding != BridgeAuthority != BridgeCurrentness != BridgeApplicability`.

A textual `ESTABLISHED` label must never be treated as self-authenticating authority.

Current hypothesis: positive bridge standing should require an owner-qualified witness / authority reference rather than a naked enum.

---

## 11. `EXTERNAL_REQUIRED` should not yet become a third standing value

Current structure suggests a cleaner decomposition:

- bridge standing: established / not-established / refuted-or-other-owner-native status as applicable;
- discharge locus / dependency: local vs external owner / required authority;
- authority/currentness/applicability qualification: separate.

Thus `EXTERNAL_REQUIRED` may be representable as:

`BridgeStanding = NOT_ESTABLISHED locally`

plus:

`DischargeDependency = external(owner, predicate, qualification)`.

This remains a hypothesis pending further counterexamples.

---

## 12. Literature novelty audit — what must NOT be claimed as new

Literature snapshot: 2026-08-19.

### Existing nearby work already covers the following ideas

1. **Claim-evidence warrants** are not new.
   - *WarrantScore: Modeling Warrants between Claims and Evidence for Substantiation Evaluation in Peer Reviews*, arXiv:2601.17377, explicitly argues that evidence presence alone is insufficient and evaluates the logical inference/warrant between claim and evidence.

2. **Relevant evidence can under-warrant a stronger claim** is not new.
   - *Relevant Is Not Warranted: Evidence-Force Calibration for Cited RAG*, arXiv:2605.28044, studies citation/evidence-force overclaiming and shows generic support prompts can badly miscalibrate warrant strength while explicit force-aware prompting improves but does not eliminate the error.

3. **Argument/support/attack graphs and acceptability semantics** are not new.
   - Current computational-argumentation work explicitly represents arguments plus support/attack relations and computes acceptability/strength.

4. **Graph contracts as behavioral commitments for LLMs** are not new.
   - *Do LLMs Follow Their Self-Reported Causal Graphs? A Graph-Contract Audit of Falsifiable Rationales for Trustworthy Decisions* (OpenReview 2026) treats graph structure as a falsifiable behavioral commitment and reports that model behavior can violate graph-implied constraints.

5. **Semantic roles + provenance / authority-aware Agent controls** are not new.
   - *The Granularity Mismatch in Agent Security: Argument-Level Provenance Solves Enforcement and Isolates the LLM Reasoning Bottleneck*, arXiv:2605.11039, introduces provenance-aware capability contracts and semantic argument roles.
   - *ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents*, arXiv:2606.18037, makes source attribution an independent verification axis.

6. **Proof-carrying Agent actions / explicit approval semantics** are not new.
   - *Proof-Carrying Agent Actions: Model-Agnostic Runtime Governance for Heterogeneous Agent Systems*, arXiv:2606.04104, uses portable action certificates with admissibility/approval/evidence checkpoints.

7. **Evidence tracing / execution provenance** is an active research area, not a new SCD invention.
   - *From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents*, arXiv:2606.04990, surveys claim support, provenance relations, tool-use provenance, semantic provenance, audit and recovery.

Therefore TRAA must not claim novelty for generic support graphs, warrants, proof obligations, provenance, role typing, proof-carrying action, or task-relative context sufficiency.

---

## 13. Current novelty-bearing residual — hypothesis only

The currently defensible residual is narrower:

> **For an Agent-visible abstraction intended to substitute for heterogeneous authoritative computational descriptions, must the abstraction preserve owner-qualified inferential standing topology — including target-scoped non-established bridges / undischarged obligations — in addition to positive semantic content, so that the representation does not silently license higher-order judgements across truth-role boundaries?**

Distinctive combination under current evidence:

- transformation-relative semantic substitutability;
- heterogeneous owner-native target judgements rather than one reward/action objective;
- directional semantic approximation;
- typed premise/intermediate/target judgement roles;
- preservation of support-edge standing / target-scoped support closure;
- strict separation from capability, permission, currentness, selection, execution and semantic success;
- explicit study of LLM prior-induced illicit bridge completion under otherwise true facts;
- reopen/currentness implications when support topology or its authority changes.

No single item above is claimed novel. The research question is whether the **combination** defines a stable and useful responsibility not already subsumed by existing warrant-calibration, argumentation, proof-carrying, provenance or context-sufficiency frameworks.

Current answer: **OPEN**.

---

## 14. Important owner boundary after live dogfood

The experiments do not justify moving bounded-model cognitive behavior into SCD semantic truth.

Keep separate:

### SCD / semantic owner side

- what the semantic claims mean;
- which support relations / refinement relations exist;
- whether a bridge has standing under qualification;
- what target-scoped support closure means;
- whether an abstraction is a semantically lawful substitute in scope.

### Harness / Agent empirical side

- what exact Working View the model saw;
- whether a given model reliably consumes omitted/explicit support structure;
- model-specific bridge-attractor behavior;
- cognitive usability of a semantically lawful representation.

Thus:

`SemanticSubstitutability != ModelCognitiveReliability`.

The live experiments motivate an interface; they do not erase the owner split.

---

## 15. Candidate falsifiers for the remaining residual

The residual should collapse or be substantially demoted if any of the following are established:

1. ordinary evidence-force / warrant-calibration methods predict and control all current cross-owner bridge-attractor failures without any additional target-scoped semantic-standing structure;
2. target-scoped support closure adds no predictive or diagnostic value once task relevance / proof obligation / standard argumentation representation is controlled;
3. the observed cross-owner benefit disappears under lexical randomization or alternative models and is explainable as prompt-format compliance only;
4. closed support topology cannot be made owner-authoritative without reintroducing a universal shadow authority or closed-world assumption inappropriate to open research/Agent contexts;
5. positive and negative bridge standing cannot be represented without simply embedding the final answer;
6. mature existing frameworks already provide the same heterogeneous owner-standing/substitutability contract with equivalent empirical coverage.

A negative result is acceptable: TRAA may collapse into an SCD application of existing abstraction/refinement/warrant theory.

---

## 16. Current standing and next work

### Current standing

- TRAA derived-theory route: `CONTINUE / CANDIDATE / NOT_FROZEN`.
- New SCDF/Foundation: `NOT_ADMITTED`.
- Semantic Bridge Attractor vocabulary: `WORKING / NOT_REGISTRY`.
- Target-scoped support closure: `CANDIDATE MECHANISM / NOT_PRODUCTION_CONTRACT`.
- Live Agent failure prediction: `SUPPORTED_IN_SCOPE`, not universal.
- Cross-owner conservative support-topology representation: `SUPPORTED_IN_CURRENT_FIXTURES`.
- Literature novelty: `OPEN / NARROWED`.

### Next investigations

1. lexical/randomized ablation of strong attractors;
2. positive bridge standing with real owner-qualified witness / authority/currentness/applicability;
3. distinguish `NOT_ESTABLISHED`, explicit closed-graph non-edge, and unresolved proof obligation under open-world partial views;
4. determine whether target-scoped support closure is simply a standard argumentation/proof obligation specialization or a useful SCD-specific semantic-substitutability contract;
5. only after that decide whether a minimal technology-neutral reference contract is warranted.

Do **not** implement a universal `BridgeStanding` engine or schema from this note.

---

## 17. Runtime evidence pointers

Important live / structured dogfood Jobs include:

- `job-01a01932-2c86-7442-9251-156feb90e363`
- `job-01a01933-5497-7983-94f3-bab08fc5888b`
- `job-01a01936-3633-7250-94a1-5af019f5c94f`
- `job-01a01937-da51-7c01-96f6-9e5d15db00c2`
- `job-01a0193c-ebf9-77c3-bcca-a2ca982eaf04`
- `job-01a0193e-3912-75c0-9fa8-1d291e6c53ed`
- `job-01a01942-afc4-7873-81db-6345ad0712e5`
- `job-01a01945-ca22-79a0-bd8d-7788d0bdb0a0`
- `job-01a01949-fff7-7012-8b5c-2de722961c29`
- `job-01a01953-1bc3-71d1-8f00-882339275cdc`
- `job-01a01957-0e35-7791-a369-c5227bbe41d5`
- `job-01a01959-46ac-7550-8737-179141a46b37`
- `job-01a0195a-9f11-7c81-916b-4c8f2030bbd8`

Provider protocol failures/timeouts in those Jobs are infrastructure observations only and must not be counted as semantic model answers.
