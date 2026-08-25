# WS5 — Open-World Failure Attribution / PPD Synthesis v0

Status: **research-only**, detached Computing workspace, 2026-08-25. This is a method synthesis and falsification result. It creates no production diagnosis layer, global causal graph, Representation owner, or automatic adaptive controller.

## 1. Problem

The residual Representation problem is not generic adaptation.

It is:

> A finite observer sees an outcome that violates an expected/required behavior, but there is no perfect concrete oracle telling it whether the discrepancy came from Reality/source observation, the semantic projection, Encounter Geometry G, Operational Grammar R, Responsibility Allocation A, the observer/model, Tool/Runtime/environment support, the evaluator/expectation, an adversary, several faults at once, or an unmodeled cause. What representation intervention, if any, is causally warranted?

The earlier sequential `Representation-Causality Gate` is rejected. A layer-by-layer `source OK? -> semantics OK? -> representation?` procedure can force a false attribution when probes are weak, multiple faults coexist, or the diagnostic model is incomplete.

## 2. Pressure

The problem is forced by at least eight independent pressures.

1. **Multiple faults** — one observed discrepancy can require a compound explanation.
2. **Observational equivalence** — different causal loci can generate identical evidence under the current observation interface.
3. **Model approximation** — the diagnostic model itself can omit physical dependencies, environmental inputs, changed conditions or hidden assumptions.
4. **Unknown fault classes** — a closed hypothesis universe forces novel causes into familiar labels.
5. **Active information acquisition** — passive evidence can be insufficient; distinguishing probes may be needed.
6. **Probe consequence** — diagnostic probes can consume authority, change Reality, repair the problem, destroy evidence or introduce new faults.
7. **Mitigation pressure** — high-consequence systems may need containment/degradation before root cause is identified.
8. **Resource/authority constraints** — the most informative probe may be unsafe, unauthorized, too costly, stale or irreversible.

## 3. Domain / mature-solution subtraction

### Reiter / consistency-based Model-Based Diagnosis

Reiter's first-principles diagnosis treats an unexpected observation as a discrepancy relative to a system description and computes the diagnoses that can explain it, including principles for further measurements that discriminate competing diagnoses. The generic concept `failure -> competing explanations -> discriminating measurement` is mature prior art.

### de Kleer & Williams / GDE

GDE explicitly diagnoses **multiple faults**, represents candidates as minimal sets of violated assumptions, updates incrementally, separates behavior prediction from diagnosis, and uses sequential measurements/probability/information theory to localize faults. Therefore set-valued and multi-fault diagnosis is not a new Representation contribution.

### Diagnosability / isolability

Fault-diagnosis theory distinguishes whether a fault can in principle be detected/isolated under the observation/interface structure. An unresolved diagnosis can therefore be structural/model-relative rather than merely a low-confidence guess.

### Active fault diagnosis / experiment design

Nominal observations may contain insufficient diagnostic information. Active diagnosis designs system inputs to separate competing fault-model predictions. Mature variants are probabilistic, set-based and uncertainty-aware. Thus active probe selection itself is prior art.

### Model invalidation / model uncertainty

Control literature explicitly asks whether observed input/output data are consistent with an admissible model family and studies detectability under uncertainty. This subtracts novelty from a generic `is our model still adequate?` step.

### MBD's own model-misspecification problem

Pill & de Kleer (DX 2024) explicitly identify `models are approximations`: an omitted physical dependency, unmodeled environmental input, inappropriate abstraction, missed environmental change or hidden assumption can make MBD identify a downstream victim rather than the root cause. They also note that the nominal system description/model itself may be faulty or incomplete. This is almost exactly the open-world attribution pressure found here.

### Open-set / open-world recognition and reject option

Open-set recognition assumes incomplete class knowledge and requires systems to handle unseen classes rather than force every case into known labels. Selective classification/reject-option traditions already legitimize abstention. Therefore `UNKNOWN` / novel cause handling is mature, not a new Ordivon primitive.

### Open-world adaptive agents

HYDRA (Mohan et al.) already monitors divergences from expectations in evolving open worlds, characterizes novelties, and uses diagnosis/repair ideas plus heuristic model-change search to adapt planning models. Generic `detect novelty -> diagnose -> repair model -> continue` is therefore directly subtracted as prior art.

## 4. Ordivon internal subtraction

### Verify / Track R already owns failure-attribution research

`VERIFY-CHARTER-001` already gives Computing/Track R responsibility for:

- research questions and competing hypotheses;
- comparison design and falsification;
- failure attribution;
- deciding which part of the model-to-world system caused an observed result;
- explicit UNKNOWN and independent verification.

`ANC-VERIFY-001` already defines the evaluated unit as:

`Task × model × Harness × Context strategy × Tool contract × budget × environment`

and defines research-only Failure Records rather than a production diagnosis plane.

Therefore open-world failure attribution does **not** create a new Representation owner or subsystem. Representation becomes one candidate causal locus inside existing evaluation/research responsibility.

### World / source owners

Own actual observation, current capability/support and external Reality premises. Computing cannot diagnose `source fault` by rewriting source truth.

### SCD

Can supply semantic discriminants/preservation facts when the hypothesis concerns a representation collapsing distinctions required by a named judgement. It does not own root-cause diagnosis globally.

### Media

Can generate/test G/R mediation interventions. It does not own source/model/evaluator failures.

### Harness

Can realize bounded Context/probe/action/reconfiguration and preserve operational use-contract obligations. It does not mint domain root-cause truth.

### Runtime / Security / Interlocus / other owners

Retain physical execution, adversarial, reachability and other owner-native premises when they are candidate loci or probe constraints.

## 5. Diagnostic Situation — research notation only

For one case, a useful notation is:

`D = <U, OBS, H, Pred, P, Adm, B, t>`

where:

- `U` = frozen expected behavior / target / verifier / bounded use obligation;
- `OBS` = owner-qualified observations and discrepancy evidence;
- `H` = case-local candidate hypotheses, including compound hypotheses and an UNKNOWN/MODEL-INadequate escape;
- `Pred(h,p)` = declared possible observation/effect predictions if hypothesis h holds and probe/intervention p is applied;
- `P` = candidate observations/probes/interventions;
- `Adm(p)` = owner authority, safety, currentness, reversibility and semantic admission for p;
- `B` = resource/horizon constraints;
- `t` = currentness/history coordinates where load-bearing.

This is **not** proposed as a universal schema. Only coordinates needed by the current discriminating decision should be represented.

## 6. Set-valued Diagnostic Frontier

Given evidence `E`, keep:

`Gamma(E) = { h in H | h remains compatible with E under the declared diagnostic model }`.

Do not force a single label merely because one is needed by a classifier/UI.

Important standings:

- one surviving known hypothesis -> `IDENTIFIED_WITHIN_MODEL`, not absolute root-cause truth;
- multiple live hypotheses -> `AMBIGUOUS/UNRESOLVED`;
- no known hypothesis fits -> `UNKNOWN / MODEL_INADEQUATE` rather than nearest-class forcing;
- multiple hypotheses remain observationally equivalent under every admissible probe -> `NON_DIAGNOSABLE_UNDER_CURRENT_MODEL_AND_INTERFACE` if that non-diagnosability can actually be established;
- inability to establish diagnosability itself -> ordinary `UNKNOWN`.

No global enum is required in production.

## 7. Deterministic falsification results

### Sequential gate rejected

`sequential_gate_probe.py` constructs source, G, and source+G hypotheses with the same passive failure. A shallow `source AVAILABLE` check falsely clears an actually bad source. A raw-source crosscheck removes G in one case but source and source+G remain indistinguishable under the available probes.

Law:

`LayerAvailable != LayerCorrect`.

`PassiveFailure != SingleCausalLocus`.

### Single-fault attribution rejected

`multiple_fault_probe.py` uses two conflict sets `{source,G}` and `{G,evaluator}`. Minimal diagnoses are `{G}` **or** `{source,evaluator}`. A single-fault assumption forces G and deletes an equally valid multi-fault explanation.

Law:

`SingleFaultAssumption can manufacture Representation attribution`.

### Successful repair does not identify cause

`repair_attribution_probe.py` starts with a faulty source. A representation-side compensator makes one target query exactly correct but fails a second query because the source remains wrong.

Law:

`SuccessfulRepresentationRepair != RepresentationWasRootCause`.

Treatment value and root-cause identification are separate.

### Unknown/model-inadequate cause must remain expressible

`unknown_fault_probe.py` produces a signature that matches no known source/G/R/A hypothesis. A forced closed-set classifier picks G at distance one; an open-set treatment returns `UNKNOWN_MODEL_INADEQUATE`. Later owner-qualified evidence permits a new evaluator/protocol hypothesis.

Law:

`KnownHypothesisUniverse != CauseUniverse`.

### Diagnostic action authority

`active_probe_selection.py` gives the most information-rich probe a live write effect that is unauthorized/unsafe. A less informative read-only crosscheck is the best admissible probe.

Law:

`DiagnosticInformationValue != ActionAuthority`.

Hard authority/safety/currentness admission precedes probe optimization.

### Diagnosability is interface-relative

`diagnosability_probe.py` gives two hypotheses identical predictions under every admissible probe; only a privileged unavailable tap can separate them.

Law:

`MoreObservationsOfSameProjection != MoreDiagnosability`.

### Mitigation can precede diagnosis

`mitigation_without_diagnosis_probe.py` shows source and G hypotheses both make writes unsafe while a read-only degradation is safe under either. The diagnostic set remains unchanged after successful containment.

Law:

`Mitigation != Diagnosis != RootCauseRepair`.

### Broad recovery can erase attribution evidence

`probe_effect_probe.py` shows a combined Tool restart + representation rebuild succeeds under both candidate causes, while surgical one-locus probes separate them.

Law:

`SuccessfulBroadRecovery can reduce later diagnosability`.

Diagnostic probes are state-changing Effects unless proven observational.

### Information gain is prior-relative

`prior_sensitivity_probe.py` shows expected information gain selects different probes when arbitrary source-vs-R priors are reversed. When no owner/evidence-grounded prior exists, a uniform prior is fabricated knowledge.

Law:

`UnknownPrior != UniformPrior`.

Use set-based discrimination / worst-case partition / decision-specific Pareto criteria unless probabilistic premises are actually justified.

## 8. Representation-Causality Gate is replaced, not upgraded

Reject:

`source OK? -> semantics OK? -> G/R/A?`

Retain:

1. constitute the discrepancy relative to U and owner-qualified OBS;
2. construct the smallest case-local competing hypothesis set that can change the next decision;
3. include compound and model-inadequate/unknown alternatives when pressure exists;
4. preserve all hypotheses still compatible with evidence;
5. ask whether current admissible observations already discriminate them;
6. if not, consider an owner-authorized, semantically valid, risk-bounded discriminating probe;
7. if no useful admissible discriminator exists, remain ambiguous/non-diagnosable/UNKNOWN;
8. if consequence requires it, mitigate/degrade safely without pretending mitigation identifies cause;
9. only then choose a root-cause repair or representation intervention whose causal claim matches the evidence;
10. verify consequence and preserve transition/probe lineage because the probe itself may change the system.

This is **research discipline**, not a new automatic diagnosis service.

## 9. G/R/A after WS5

G/R/A survives only as a sparse **representation-side hypothesis/repair vocabulary**:

- G — Encounter Geometry;
- R — Operational Grammar;
- A — Responsibility Allocation.

It is not exhaustive even of representation-related failure, and certainly not of system failure.

A G/R/A diagnosis has standing only relative to:

- a frozen discrepancy/target;
- competing non-representation hypotheses;
- a diagnostic model and evidence;
- ideally a discriminating intervention/deletion witness.

If G/R/A adds no repair-selection value in a future natural holdout, contract it further or delete it.

## 10. Adaptive Representation is now a downstream policy, not a theory root

The generic adaptive loop:

`observe failure -> revise representation -> retry`

is rejected.

A safer research pattern is:

`discrepancy -> diagnostic frontier -> admissible discrimination/mitigation -> cause-relative minimal intervention -> verify -> retain/revert`.

The action set must include:

- source/observation repair;
- semantic qualification/projection repair;
- G repair;
- R repair;
- A repair;
- Tool/environment/support repair;
- evaluator/target correction;
- mitigation/graceful degradation;
- NO_CHANGE;
- UNKNOWN / request evidence / stop.

Representation adaptation is selected only when evidence warrants it. Generic open-world model repair is already mature prior art (e.g. HYDRA); Ordivon's contribution, if any, would be owner-preserving evidence/admission composition rather than a new adaptation algorithm.

## 11. Causal and operational distinctions that must survive

- `ObservedFailure != RepresentationFailure`.
- `ObservedFailure != SingleFault`.
- `FailureRelativeToEvaluator != EvaluatorCorrect`.
- `DiagnosisSoundWithinModel != DiagnosticModelAdequate`.
- `IdentifiedWithinModel != AbsoluteRootCauseTruth`.
- `NoKnownDiagnosis != NoCause`.
- `UNKNOWN != FailedResearch`.
- `SuccessfulRepair != CorrectDiagnosis`.
- `FailedRepair != WrongDiagnosis`.
- `Mitigation != Diagnosis`.
- `Recovery != RootCauseRepair`.
- `Probe != PassiveObservation`.
- `ProbeAvailability != ProbeAuthority`.
- `InformationGain != DecisionValue`.
- `UnknownPrior != UniformPrior`.
- `MoreObservation != Diagnosability`.
- `RepresentationTreatmentEffect != RepresentationRootCause`.

## 12. Owner composition and COJC attribution

For a future natural case:

### Computing / Verify
Owns the research hypothesis set, comparison, failure attribution study, trial validity and falsification.

### Source / World / domain owner
Provides current actual observations and target-relevant external truth.

### SCD
Is **causal** only if a semantic preservation/non-entailment/discriminant supplied by SCD is deletion-essential to distinguish or safely substitute representations. Otherwise it is adjudicative.

### Media
Is **causal** only if a Media-specific G/R intervention beats a generic task-fit information architecture baseline under the same evidence. Otherwise it is supplier/design or null.

### Harness
Is **causal** only if bounded operational probe/reconfiguration/recovery semantics change the real target relative to a direct Provider/source control. Otherwise it is carrier.

This makes the original Media × SCD × Harness triad **insufficient by itself for open-world attribution**: source/World truth and Computing/Verify experiment authority are logically prior. No triad-only diagnosis service is justified.

## 13. Strongest residual after subtraction

Generic diagnosis, multi-fault reasoning, active probing, abstention, open-set novelty handling and open-world model adaptation are all mature prior art.

The remaining Ordivon-specific seam is narrower:

> **Owner-qualified diagnostic composition under incomplete models:** how a finite Agent/Research process assembles just enough owner-native observation, semantic discriminants, representation hypotheses and bounded operational probes to preserve causal ambiguity where necessary, choose safe discriminating actions where possible, and avoid turning a successful compensating representation into false root-cause standing.

This is currently a **research protocol/problem**, not a new theory primitive, owner, service, schema or Foundation.

## 14. Natural prospective falsifier

Wait for one genuinely new natural Ordivon failure where:

- representation is a plausible cause but at least one non-representation locus is also plausible;
- passive symptoms do not trivially identify the cause;
- a real downstream decision depends on diagnosis/repair;
- at least one safe/authorized discriminating probe exists or non-diagnosability itself matters;
- final evidence can independently constrain whether the proposed standing was justified.

Before inspecting implementation history or applying the repair, freeze:

1. target/discrepancy U;
2. current observations and owner boundaries;
3. competing hypotheses including UNKNOWN/model inadequacy;
4. predicted discriminator outcomes;
5. admissible probes and prohibited/risky probes;
6. mitigation policy if consequence requires action under uncertainty;
7. causal promotion conditions.

Compare, in shadow if necessary:

- direct/first-fix guess;
- sequential layer gate;
- set-valued active-diagnosis policy.

Measure:

- false causal promotion;
- preserved ambiguity when justified;
- unnecessary/unsafe Effects;
- discriminating observations required;
- repair/recovery consequence;
- diagnostic overhead;
- whether eventual owner evidence actually changed the earlier decision.

One case can falsify the method. Repeated materially different natural cases are required before promotion.

## 15. Current disposition

### REJECT

- Representation-Causality Gate as a sequential boolean gate;
- universal Representation Diagnosis service/owner/schema;
- G/R/A as exhaustive fault ontology;
- automatic root-cause repair after any performance degradation;
- arbitrary uniform priors for diagnostic ranking;
- repair success as causal proof;
- diagnosis-before-any-action as a universal rule.

### RETAIN

- set-valued competing hypotheses;
- multi-fault and UNKNOWN/model-inadequate escape;
- model/interface-relative diagnosability;
- active discriminating probes under owner authority/safety/currentness;
- mitigation/degradation distinct from diagnosis;
- G/R/A as representation-side repair vocabulary;
- exact probe/intervention lineage;
- natural prospective holdout gate.

### STATUS

`OpenWorldFailureAttributionGenericTheory = MATURE_PRIOR`.

`RepresentationSpecificRootCauseTheory = NOT_EARNED`.

`OwnerQualifiedDiagnosticComposition = STRONG RESEARCH-METHOD CANDIDATE`.

`Media×SCD×Harness JOINT_CAPABILITY = STILL OPEN / NOT PROVEN`.
