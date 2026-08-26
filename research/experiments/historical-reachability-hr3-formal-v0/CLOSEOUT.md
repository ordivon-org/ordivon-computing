# HR3 Formal / Synthetic Countermodel Closeout

## Purpose

HR3 attacks over-strong reachability implications with deliberately constructed formal/synthetic worlds. It is not empirical evidence about how often real-world capability transitions occur.

Claim ceiling:

```text
FormalCountermodel
can refute an unrestricted implication
but
cannot establish that a real target has the modeled path.
```

## Deterministic countermodels

Ten hand-constructed cases survived the corrected run.

1. **Dynamic basis** — a target not reachable from the current basis becomes reachable after admissible fabrication + metrology acquisition.
2. **Hard contradiction** — a contradictory target remains unreachable, preserving a true hard-stop class.
3. **Provider / authority** — supplier existence does not establish current capability; authority + transaction + verification are still required.
4. **Raw-action non-gain** — adding an inadmissible primitive action increases action count without increasing valid reachable state.
5. **Constraint robustness** — removing a destructive action increases robust target reachability under nondeterministic/adversarial first-action choice.
6. **External carrier compression** — external manufacturing compresses a four-step internal construction chain to invoke + verify; verification does not disappear.
7. **Scale boundary** — a locally realized prototype does not imply the scaled system is qualified; scale introduces capacity/safety transitions.
8. **Instrument discrimination** — two worlds indistinguishable under the old observation basis become distinguishable after adding an instrument signal.
9. **Lock-in contraction** — an open-interface state permits later composition while a closed-interface state does not; reachability need not grow monotonically.
10. **Reconstructible option** — an inactive but reconstructible design can recover a future target with extra transition cost; inactive instance is not zero option value.

The important result is not that these ten models are realistic in every detail. It is that the following unrestricted collapses are formally invalid:

```text
CurrentUnreachable => PermanentlyUnreachable
SupplierExists => CurrentCapability
MoreRawActions => MoreValidCapability
LocalQualified => ScaleQualified
PastCapability => MonotonicFutureReachability
InactiveInstance => ZeroFutureOptionValue
```

## Generated DAG stress probe

A seeded generator created 5,000 acyclic capability-construction worlds. Every world began with only `c0`; `c7` was outside the static basis. Candidate actions could add capabilities when their prerequisite capabilities were present.

Result:

```text
static unreachable but dynamically reachable   2422
still unreachable after transition closure     2578
```

The frequency has **no empirical interpretation**. The useful fact is that both classes occur in the same explicit model family:

- many current-nonreachable targets become reachable after basis-changing transitions;
- many remain unreachable even after all modeled transitions are exhausted.

Therefore the strongest formal standing is two-sided:

```text
CurrentNonReachability
!=
PermanentNonReachability
```

and:

```text
CandidateMetaReachability
!=
GuaranteedEventualReachability
```

## Relation to Historical Reachability

HR3 supports keeping `basis-changing transition` as an analysis move while rejecting an optimistic progress law.

The transition basis may change through:

- new prerequisite capability;
- observation/instrumentation;
- external carrier access;
- authority/admission;
- composition/interface;
- constraint/pruning;
- reconstruction;
- scale-specific engineering.

But the formal experiment does **not** justify a global transition graph, dynamic planner, or `Reachability` service.

## Disposition

**HR3: COMPLETE as a formal countermodel programme.**

Promote only the anti-collapses and claim-boundary discipline. Do not promote the toy ontology or generated frequencies.
