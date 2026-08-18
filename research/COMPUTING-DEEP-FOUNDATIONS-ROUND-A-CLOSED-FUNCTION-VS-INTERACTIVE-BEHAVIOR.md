---
schema_version: 1
id: computing.research.deep-foundations.round-a.closed-function-vs-interactive-behavior
title: Ordivon Computing Deep Foundations — Round A: Closed Function / Effective Procedure vs Interactive / Reactive Behavior
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: First destructive post-atlas Computing tournament. It attacks the universal equation Computation = closed input-to-output function/effective terminating procedure against Turing computability, persistent Turing machines, reactive systems, CSP/process semantics, I/O automata, long-lived services, databases, controllers and Agent loops. The pass rejects both closed-function monism and interaction monism. Interaction does not establish hypercomputability; its strongest surviving burden is behavioral rather than function-computability power. A broader unnumbered foundation candidate emerges: Computation must expose its computational boundary and the observation semantics under which result, trace, continuation and termination claims are made. Closed function evaluation is a special case; interactive/reactive computation is another. No CDF0 is admitted.
evidence_status: strong-local
readiness: ROUND_A_COMPLETE_STRONG_UNNUMBERED_CANDIDATE_ROUTE_UNSELECTED
---
# Ordivon Computing Deep Foundations — Round A

## Closed Function / Effective Procedure vs Interactive / Reactive Behavior

## 0. Admission discipline

This round is **not `CDF0`**.

The initial whole-Computing atlas ranked interactive/ongoing computation highly because it is nearly absent from current Computing Core/Knowledge and can pressure a common hidden assumption:

```text
Computation
= receive fixed input
→ execute a finite effective procedure
→ terminate
→ return output.
```

But high information gain does not imply that `Interaction` itself is a foundation primitive.

Round A therefore attacks both sides:

```text
M1  Function evaluation monism
M4  finite effective-procedure monism
M6  interactive-process monism
```

and asks what remains after owner subtraction and counterexamples.

---

# 1. Source pressure

## 1.1 Turing 1936 — function/calculation target

Turing's 1936 construction concerns computable numbers and extends naturally to computable functions/predicates. It remains the canonical foundation for effective function computation.

Important boundary:

```text
Turing-computable function
is a claim about effective calculation.
```

It does not by itself imply that every useful semantics of a long-lived system must collapse to one finite initial input and one final output.

## 1.2 Persistent Turing machines / interactive transition systems

Goldin, Smolka, Attie and Sonderegger model a persistent Turing machine as an infinite sequence of ordinary TM computations with a work tape retained across input/output interactions. They prove an isomorphism between PTMs and a general class of effective interactive transition systems, and show persistence changes behavioral expressiveness relative to amnesic PTMs.

The useful pressure is:

```text
behavioral semantics of an ongoing system
!= necessarily one extensional input-output function.
```

The stronger claim sometimes made in this literature—interaction being "more powerful" than Turing machines—must be scope-qualified. It is an expressiveness claim under observational/stream behavior semantics, not automatically a proof that interaction computes non-Turing-computable mathematical functions.

## 1.3 Reactive systems

Harel/Pnueli and later reactive-system theory distinguish systems whose meaningful correctness concerns ongoing response to environmental events rather than production of one terminal value. Operating systems, controllers and concurrent components may be intended not to terminate.

Therefore:

```text
termination
!= universal success condition.
```

## 1.4 CSP / process semantics

Hoare/Brookes/Roscoe-style communicating-process theory treats patterns of interaction as first-class semantics. Two processes can be distinguished by traces/failures/deadlock behavior even when a terminal-return-value view would erase that distinction.

## 1.5 I/O automata

Lynch/Tuttle I/O automata explicitly model asynchronous concurrent components through input/output/internal actions and are used across communication algorithms, concurrent databases, shared objects and dataflow architectures.

This is a direct pre-Agent example in which:

```text
component behavior at an interaction boundary
```

is a computational object of analysis.

---

# 2. First deletion — `Computation = final function value`

## A-F1 — same final value, different observable interaction

Two systems eventually return the same final value.

System A emits:

```text
ready
progress(50%)
commit
result(7)
```

System B emits:

```text
ready
rollback
retry
commit
result(7)
```

For an extensional function query:

```text
A == B.
```

For a protocol/behavior query:

```text
A != B.
```

Therefore:

```text
SameFinalOutput
!= SameComputationalBehaviorByIdentity.
```

`FunctionResult` is one observation projection, not the universal identity of computation.

---

# 3. Nontermination can be correct

## A-F2 — operating system / server

A server that remains available indefinitely can satisfy its contract precisely by **not terminating** while continuing to react correctly.

```text
NonTermination
!= FailureByIdentity.
```

A final-value-only semantics cannot naturally express liveness, responsiveness or service continuity without moving the real property into an external encoding.

## A-F3 — controller

A controller may repeatedly:

```text
observe
→ update internal state
→ emit actuation
→ observe consequences
↺
```

There may be no privileged final output.

Correctness can involve:

```text
always avoid unsafe region
respond within a bound
continue servicing events
```

rather than eventual termination.

Timing itself belongs partly to Runtime/World/resource analysis, but the logical fact that **continuation may be success** survives Computing ownership subtraction.

---

# 4. Future input can depend on past output

## A-F4 — interactive protocol

At time `t0`, the system emits a challenge.
At `t1`, the environment chooses its next input after seeing that challenge.

Therefore:

```text
FutureInput
can be causally dependent on PriorOutput.
```

A model that insists all input be fixed before computation begins must instead encode an entire future environment strategy/oracle as the initial input.

That encoding may be mathematically useful, but it changes the query:

```text
actual ongoing interaction
→ closed evaluation over an encoded environment.
```

These are not the same observational boundary.

## A-F5 — database/service request stream

A long-lived database/service receives later requests chosen from previous results, external events and other actors.

```text
InputSetKnownInAdvance
!= necessary for computation.
```

The service can still be implemented by ordinary Turing-computable steps.

This is crucial:

```text
open input stream
!= hypercomputation.
```

---

# 5. Interaction expressiveness is not function hypercomputability

## A-F6 — scope of PTM expressiveness

PTM literature proves stronger **behavioral** expressiveness under stream/observation semantics.

A critic can instead enlarge the closed machine's initial description to include the environment, oracle or interaction transcript generator.

Then a large composed closed system may be Turing-simulable even though the original component's open behavior was not represented as one finite function input.

Thus:

```text
MoreBehaviorallyExpressive
!= ComputesMorePartialRecursiveFunctionsByIdentity.
```

Round A rejects:

```text
Interaction -> super-Turing function computability.
```

No such law is admitted.

## A-F7 — whole-system closure is boundary-relative

Two components can interact continuously with one another while their composition is considered closed relative to the outside observer.

```text
Interactive(component)
AND
Closed(composition)
```

can both be true.

Therefore:

```text
Closedness / Openness
is query-boundary-relative.
```

This is one of the strongest surviving results.

---

# 6. Interaction itself is not universal

## A-F8 — pure finite algorithm

A pure sorting procedure can be fully described for the relevant query as:

```text
finite input
→ finite computation
→ finite result.
```

Nothing requires ongoing environmental interaction.

Therefore:

```text
Interaction
!= necessary condition for every computation.
```

M6 interactive-process monism fails.

## A-F9 — batch numerical kernel

Matrix multiplication, compression of a fixed buffer, hashing and many numerical kernels can be treated as closed transformations at the chosen boundary.

An implementation may interact with memory/hardware internally, but treating every physical signal exchange as semantically constitutive would destroy useful abstraction.

Therefore:

```text
PhysicalInteractionDuringRealization
!= ComputationalInteractionAtEveryAbstractionLevel.
```

---

# 7. Procedure/program is not computation occurrence

## A-F10 — same program, different interaction history

One server program can realize distinct computations/runs under distinct event histories.

```text
ProgramText
!= ComputationOccurrenceByIdentity.
```

## A-F11 — different implementations, same behavior

Two different process implementations can be equivalent under a chosen behavioral equivalence despite different internal states/steps.

```text
ImplementationIdentity
!= ComputationalBehaviorIdentityByNecessity.
```

This pressures any foundation that equates computation with program bytes.

---

# 8. Trace is not automatically the unique semantics

## A-F12 — trace-equivalent but branching-different systems

Two systems may expose the same set of finite traces but differ in what choices remain possible after a given history, deadlock behavior, fairness or branching structure.

Therefore:

```text
SameTraceSet
!= SameBehaviorUnderEveryObservationSemantics.
```

A universal `Trace` primitive is insufficient.

The observation/equivalence criterion must be explicit.

## A-F13 — internal actions can be abstracted

Process theories often distinguish internal/unobservable steps from externally visible behavior.

Therefore:

```text
EveryPhysicalOrLogicalStep
!= ObservableComputationalEventByIdentity.
```

What counts as behavior depends on the declared abstraction/observation semantics.

---

# 9. State persistence matters, but does not define interaction

## A-F14 — persistent vs amnesic interaction

PTM results show that retaining work state between interaction rounds changes behavioral expressiveness relative to amnesic variants.

So:

```text
PersistentInternalState
can be computationally material.
```

But persistence alone is not interaction:

```text
persistent closed batch process
```

is coherent.

Thus:

```text
Persistence
!= InteractionByIdentity.
```

State/memory remains a separate future foundation continent.

---

# 10. Environment is not one new Computing owner

## A-F15 — World subtraction

The environment may contain physical temperatures, market prices, human choices, files or remote services.

World/domain owners own those facts.

Computing needs only the computationally relevant interface/model:

```text
external event/value reference
+ admissible observation/action relation
```

Therefore:

```text
ComputationalEnvironmentModel
!= WorldTruthStore.
```

## A-F16 — Network subtraction

An interactive process may exchange messages.

Network owns:

```text
reachability
transport
routing
latency/capacity/convergence
```

Computing may still ask:

```text
what input/output event behavior is allowed?
what behavior equivalence/correctness is claimed?
```

Therefore:

```text
InteractionSemantics
!= NetworkTransportByIdentity.
```

## A-F17 — Runtime subtraction

Runtime owns concrete process/Job lifecycle and actual execution truth.

Computing may specify an abstract behavior whose realizations occur across many Runtime Jobs/processes.

Therefore:

```text
ComputationContinuationSemantics
!= RuntimeJobContinuityByIdentity.
```

## A-F18 — Human subtraction

A user can be one source of environment input, but interactive computation also exists between machines and autonomous processes.

```text
Interaction
!= HumanComputerInteractionByIdentity.
```

Human experience remains Human-owned.

---

# 11. Agent-era pressure

## A-F19 — model/tool loop

An Agent turn can be:

```text
Context
→ model output / Tool request
→ external Tool result
→ revised Context
→ next model output
```

The Tool result is not necessarily knowable before the prior model output selects the Tool/action.

This is structurally interactive.

But:

```text
AgentInteraction
!= new Agent-era computation primitive.
```

It instantiates the same open input/output + persistent state + observation semantics already present in pre-Agent interactive systems.

## A-F20 — model session vs durable computation

A long-running Agent task may span multiple model sessions, processes or Provider calls.

Whether that is one computational process depends on the computational/query semantics—not on Provider Session identity.

This aligns with existing Ordivon work-continuity findings without turning Host/Harness identity into Computing ontology.

---

# 12. Nondeterminism, interaction and uncertainty are separate

## A-F21 — nondeterministic closed computation

A scheduler/random source can produce multiple possible trajectories even with no semantically open environment after start.

Therefore:

```text
Nondeterminism
!= InteractionByIdentity.
```

## A-F22 — deterministic interactive computation

A deterministic transducer interacting with a deterministic environment can have a fully determined trace.

Therefore:

```text
Interaction
!= NondeterminismByIdentity.
```

## A-F23 — epistemic uncertainty

An observer may be uncertain about the system despite deterministic behavior.

Therefore:

```text
ObserverUncertainty
!= ComputationalNondeterminism
!= Interaction.
```

Probabilistic computation remains a distinct future continent.

---

# 13. Termination, result and correctness must separate

## A-F24 — terminating wrong program

Termination does not imply correctness.

## A-F25 — nonterminating correct reactive system

Nontermination does not imply incorrectness.

Therefore:

```text
TerminationStatus
!= CorrectnessStatusByIdentity.
```

Likewise:

```text
FinalResult
!= only possible correctness target.
```

Correctness may target:

```text
result
trace property
safety
liveness
refinement
response relation
ongoing protocol conformance
```

Formal correctness itself remains a later continent; Round A only establishes target plurality.

---

# 14. Closed computation is a special boundary case

The strongest unification discovered in Round A is:

```text
closed function computation
```

can be modeled as a process whose chosen computational boundary has:

```text
one initial input episode
no semantically relevant mid-computation external input
one result observation
termination as a relevant completion event.
```

Interactive computation instead permits:

```text
multiple input/output episodes
future inputs contingent on prior outputs
persistent state across episodes
nonterminal correctness obligations.
```

Thus:

```text
ClosedFunctionEvaluation
and
InteractiveProcess
```

are not rival substances.
They are different shapes of a more general computational behavior contract.

---

# 15. Strong surviving candidate — Computational Boundary & Behavior Responsibility

Round A rejects `Interaction` as the new foundation noun.

A broader responsibility survives destructive subtraction:

```text
ComputationalBoundaryAndBehaviorResponsibility
```

For a computational claim, the system must make queryable enough of the following to know what claim is actually being made:

## 15.1 Computational boundary

```text
what is inside the computational system/model for this query?
what is treated as environment/input/source outside it?
```

Closedness is relative to this boundary.

## 15.2 Transition / behavior semantics

```text
what state/configuration changes or action transitions count as admissible computational evolution?
```

This need not expose implementation-level steps.

## 15.3 Interaction interface when present

```text
which input/output/event/action relations cross the boundary?
```

Optional for closed computations.

## 15.4 Observation / equivalence semantics

```text
what counts as the observable result or behavior?
final value?
stream?
trace?
branching behavior?
protocol response?
```

Two computations can be equivalent under one observation and distinct under another.

## 15.5 Continuation / termination semantics

```text
is termination required, allowed, irrelevant or failure?
what continuation/liveness claim is being evaluated?
```

## 15.6 Environment assumptions

```text
what assumptions about allowed external events/failures/timing are part of the computational claim?
```

World/Network/Runtime own the actual external facts; Computing owns only the declared assumptions needed to state the abstract computational claim.

---

# 16. Why this is not merely Runtime

Runtime can tell us:

```text
process X is running
Job Y completed
attempt Z failed
bytes Q were emitted.
```

It cannot, by physical execution truth alone, decide:

```text
whether termination was semantically required
whether two traces are equivalent
whether an input was inside or outside the computational model
whether liveness rather than final result is the correctness target
whether two different implementations realize the same computational behavior.
```

Therefore a Computing-owned semantic burden survives Runtime subtraction.

---

# 17. Why this is not merely Network

Network can tell us whether messages can be transported and under what connectivity/capacity/latency regime.

It does not determine the computational protocol's behavioral equivalence or whether a message is a semantically relevant input/output event.

So:

```text
communication realization
!= computational interaction semantics.
```

---

# 18. Why this is not merely World

Any physical system undergoes state transitions.

If Computing were simply:

```text
physical state changes over time
```

then almost every physical process would be computation, collapsing the referent into World dynamics.

Round A therefore preserves a strong anti-pancomputational constraint:

```text
PhysicalTransition
!= ComputationalTransitionByIdentity.
```

A computational claim requires a declared computational model/interpretation that identifies relevant configurations, transitions and observations.

Exactly how such representation/model grounding works remains unresolved and may belong partly to the later semantics/physical-computation continents.

---

# 19. Term separation frozen by Round A

```text
Algorithm / Procedure
!= Program / Representation
!= ComputationOccurrence
!= RuntimeProcessOrJob

InputValue
!= InputEvent
!= InputStream

OutputValue
!= OutputEvent
!= BehaviorTrace

ProgramIdentity
!= ComputationOccurrenceIdentity

FinalOutputEquality
!= BehavioralEquivalenceByNecessity

TraceEquality
!= BehavioralEquivalenceUnderEverySemantics

Termination
!= Correctness

Nontermination
!= Failure

Persistence
!= Interaction

Nondeterminism
!= Interaction

Uncertainty
!= Nondeterminism

PhysicalInteraction
!= semantically constitutive ComputationalInteraction

InteractionBehaviorExpressiveness
!= HypercomputableFunctionPower

ComputationalEnvironmentModel
!= WorldTruth

InteractionSemantics
!= NetworkTransport

ComputationContinuationSemantics
!= RuntimeJobContinuity
```

---

# 20. Candidate deletion results

Rejected as universal foundation primitives:

```text
FunctionEvaluation
FinalOutput
Termination
Interaction
InputStream
Trace
Program
RuntimeProcess
Environment
```

Each is useful in a scoped regime, but none universally identifies Computing.

---

# 21. Rival-model update

## M1 — Function evaluation

```text
REJECT AS UNIVERSAL
RETAIN AS CLOSED-COMPUTATION SPECIAL CASE
```

## M2 — Controlled state transition

```text
SURVIVES PARTIALLY
```

but still risks pancomputationalism and lacks observation/boundary semantics.

## M3 — Information transformation

```text
NOT RESOLVED THIS ROUND
```

Interaction does not decide what counts as information.

## M4 — Effective procedure

```text
REJECT IF DEFINED AS FIXED CLOSED TERMINATING PROCEDURE
SURVIVES IF GENERALIZED TO ONGOING EFFECTIVE TRANSITION/INTERACTION RULES
```

But the generalized version begins to converge toward M2 + boundary/behavior semantics.

## M5 — Resource-bounded process

```text
NOT TESTED DEEPLY YET
```

## M6 — Interactive process

```text
REJECT AS UNIVERSAL
RETAIN AS GENUINE MAJOR COMPUTATION REGIME
```

## M7 — Physical realization

```text
NOT RESOLVED
```

Round A strengthens the need for a computational-model/interpretation boundary so M7 does not collapse into pancomputationalism.

---

# 22. Round A verdict

```text
InteractiveComputation as independent universal foundation
= REJECTED

ClosedFunctionEvaluation as universal foundation
= REJECTED

FiniteTerminatingEffectiveProcedure as universal foundation
= REJECTED

Interaction implies hypercomputability
= REJECTED
```

Strong surviving unnumbered candidate:

```text
ComputationalBoundaryAndBehaviorResponsibility
```

with minimum current burden:

```text
1. ComputationalBoundary
2. TransitionOrBehaviorSemantics
3. InteractionInterfaceWhenPresent
4. ObservationOrEquivalenceSemantics
5. ContinuationOrTerminationSemantics
6. EnvironmentAssumptions
```

Classification:

```text
STRONG_GENUINELY_FOUNDATIONAL_CANDIDATE
BROADER_THAN_INTERACTIVE_COMPUTATION
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 23. Reopen / owner audit

This round does not modify current Runtime/Harness/Network/World/Human/Security owner truth.

No existing Computing Core claim is yet declared falsified because current Core intentionally does not claim to be a full theory of computation.

However it establishes a future pressure:

```text
if Computing later attempts to define computation only as controlled state transition,
it must additionally solve boundary + observation semantics or trigger a reopen.
```

---

# 24. Information gain

Round A had **high information gain**.

It eliminated a false binary:

```text
Turing/function computation
VS
interactive computation
```

and replaced it with:

```text
computational claim
→ declared boundary
→ process/transition behavior
→ optional interaction
→ declared observation/equivalence
→ continuation/termination criterion.
```

This structure simultaneously accommodates:

```text
pure algorithms
batch jobs
stream processors
databases
servers
reactive controllers
concurrent components
Agent/tool loops.
```

It therefore deserves comparison against the next high-information continents before any numbered admission.

---

# 25. Next frontier — deliberately unselected

Do not automatically continue `Interactive Computation B`.

The newly surviving candidate must be attacked from orthogonal continents:

```text
resource plurality / complexity
program semantics and representation equivalence
numerical/approximate correctness
concurrency/distributed impossibility
physical/unconventional computation
```

Key questions:

```text
Does ComputationalBoundaryAndBehaviorResponsibility survive when resource cost changes what computation means?

Does programming-language semantics already fully own the candidate?

Does approximation force observation semantics to include error/quality rather than exact behavior?

Does physical computation require an additional realization/interpretation relation?
```

Canonical status remains:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 26. Primary source anchors

This round used the following as pressure sources, not ontology authority:

- Alan Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem* (1936).
- Dina Goldin et al., *Turing Machines, Transition Systems, and Interaction*, Information and Computation 194(2), 2004, DOI 10.1016/j.ic.2004.07.002.
- Dina Goldin and Peter Wegner, *Persistence as a Form of Interaction*, Brown CS Technical Report CS-98-07, 1998.
- Nancy Lynch and Mark Tuttle, *An Introduction to Input/Output Automata*, CWI Quarterly 2(3), 1989 / MIT LCS TM-373.
- S. D. Brookes, C. A. R. Hoare and A. W. Roscoe, *A Theory of Communicating Sequential Processes*, JACM 31(3), 1984.
- Harel and Pnueli's reactive-systems line, including *On the Development of Reactive Systems* (1985), together with later formal reactive-system verification work.
- Paul Cockshott, *Are There New Models of Computation? Reply to Wegner and Eberbach*, The Computer Journal 50(2), 2007, DOI 10.1093/comjnl/bxl062, as an explicit counter-pressure against interpreting interaction expressiveness as super-Turing computability.
