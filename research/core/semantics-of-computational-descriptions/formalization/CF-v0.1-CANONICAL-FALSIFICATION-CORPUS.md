# Canonical Falsification Corpus CF-v0.1

Status: **research fixture corpus**.

The corpus is designed to falsify SCD formalization and boundary claims. A fixture is not merely input/output plus pass/fail: it must carry enough semantic scope to distinguish semantic failure from Runtime, Network, CP, Harness or implementation-local failure.

## Fixture grammar

Each fixture records:

1. fixture id and regime;
2. admission witness `ρ`;
3. source situation `Ss=(Ds,Σs)`;
4. optional target situation `St=(Dt,Σt)`;
5. typed source/target claims `φ`;
6. variation `v`;
7. correspondence `μ` where claim transport is asserted;
8. dependencies `Δs/Δt`, including external owner references;
9. expected static standing and/or standing transition;
10. adversarial perturbation;
11. expected owner classification;
12. SCDF responsibility coverage;
13. falsifier class.

## CD1 — Closed / pure description

### CD1-Z-EQ — positive

- `D1(n)=n−n`, `D2(n)=0`.
- `ΣZ`: exact mathematical integers, output equality observation.
- Claim: `D1 ≡ D2` for admitted `n∈Z`.
- Expected: **stands**.
- Pressure: SCDF3 comparison, SCDF7 satisfaction.

### CD1-IEEE — hostile environment drift

- Keep surface expressions `x−x` and `0`.
- Change environment to IEEE-754 floating semantics admitting NaN and infinities.
- Old unqualified equivalence does not carry forward because `x−x` may be NaN.
- Expected transition: **invalidated or reinterpreted** under the new environment.
- Falsifies: carrier/syntax identity ⇒ unchanged semantic standing.

## CD2 — Stateful description

### CD2-HIDDEN-STATE — positive

- Machine A emits `0` every step while toggling hidden bit `s`.
- Machine B emits `0` every step while keeping `s=0`.
- `Σout` observes only output traces.
- Claim: observational equivalence.
- Expected: **stands**.

### CD2-STATE-VISIBLE — hostile observation change

- Same machines.
- `Σstate` additionally exposes internal state.
- Claim: same equivalence.
- Expected: **fails**.
- Falsifies: one observational equivalence notion is universal.
- Boundary: no actual Runtime occurrence is required for this semantic distinction.

## CD3 — Open / compositional description

### CD3-OPEN-PURE — positive

- Context/open description `C[h]` expects `h:Int→Int` under a purity/interface contract.
- Binding `f(x)=x`.
- Expected: binding admissible; relevant composition claims may stand.

### CD3-IMPURE — near-miss with typed classification

- Binding `g(x)=x` but incrementing external counter `c`.
- On return values, `f` and `g` are extensionally equal.
- If purity is required by `K`, `g` is inadmissible: SCDF6 failure.
- If effects are admitted and the context observes `c`, `f` and `g` are contextually distinguishable: SCDF2/SCDF3 failure.
- Falsifies: return-value equality ⇒ contextual substitutability.
- Demonstrates: the same surface example has different semantic classification under different `Σ`.

## CD4 — Representation transformation

### CD4-BOOL-ENCODE — positive

- Source description computes logical AND over `Bool`.
- Target computes bitwise AND over encoded domain `{0,1}`.
- `e(false)=0`, `e(true)=1`.
- `Σt` restricts target inputs/results to `{0,1}`.
- `μ` maps truth/property claims through the encoding.
- Expected: scoped preservation claim **stands**.

### CD4-DOMAIN-LOOSEN — hostile

- Change target environment to arbitrary machine integers without Boolean-domain admission constraint.
- Old `μ` no longer justifies an unqualified Boolean preservation claim.
- Expected: **unresolved or invalidated**, depending on exact target claim.
- Falsifies: representation-level transformation ⇒ semantic preservation without environment compatibility.

## CD5 — Evolving agent / workflow description

### CD5-PLAN-GROUNDING — positive

`D0` specifies:

1. use dataset `sales@v1`;
2. verify digest `c1`;
3. compute metric `m`;
4. report `m` as grounded in that exact dataset.

Claim `φ0`: result grounded in `(sales@v1,c1)`.

`Δ0` includes the dataset-version authority and digest evidence.

Expected: **stands** while dependencies remain current.

### CD5-LOSSY-SUMMARY — hostile abstraction/currentness

Variation creates:

> compute the metric from the current sales dataset and report it

The summary drops version and digest commitments. An attempted `μ` carrying `φ0` forward has no adequate `Δ1` support.

Expected: grounding claim **not preserved / unresolved**, even if downstream execution succeeds.

Falsifies: successful continuation ⇒ semantic fidelity.

### CD5-BRANCH — hostile linear-currentness assumption

`D0` evolves into:

- branch A retaining `sales@v1/c1`;
- branch B adopting `sales@v2/c2`.

Neither branch is globally superseded merely because one is temporally newer.

Expected: standing is branch/environment/dependency scoped.

Current K0.2 can represent the case without a first-class lineage primitive; this remains a live falsifier target.

## CD6 — Distributed / delegated description

### CD6-DELEGATION — semantic positive

- Source task: compute SHA-256 over blob identity `B` pinned by digest `hB`.
- Delegated target description uses the same interpretation.
- `μ` maps task and grounding claims.
- Expected: semantic transport may **stand** independently of actual delivery.

### CD6-NETWORK-UNAVAILABLE — owner-boundary case

External Network fact: `Reachable(A,B)=false`.

Expected:

- semantic correspondence: may still stand;
- actual delivery/capability: unavailable externally.

Falsifies: semantic transport validity ⇔ actual Network capability.

### CD6-MUTABLE-REFERENCE — hostile semantic mismatch

Target interprets `B` as a mutable path instead of a digest-pinned blob.

Network delivery may succeed while source grounding semantics are not preserved.

Expected: `μ` preservation obligation **fails/unresolved**.

Falsifies: operational delivery success ⇒ semantic transport success.

# Residual fixtures

## R-ALIAS

Positive:

- model says `Alias(r1,r2)=true`;
- variation renames `r1→r3` with explicit entity correspondence;
- `μ` maps alias claim accordingly.

Hostile:

- pure textual/reference rename with no entity correspondence.
- Expected alias claim: **unresolved**, even if syntax transformation succeeds.

Interpretation: expressible in K0.2; not evidence that Reachability/Alias-Separation is reducible or closed.

## R-NAME / GENERATIVITY

Positive:

- `λx.x → λy.y` under alpha-equivalence-aware semantics.
- semantic equivalence may stand while carrier identity differs.

Hostile:

- repeated realization/derivation of a fresh-name-generating description yields distinct fresh tokens `t1≠t2` under generative semantics.
- equivalence of generating descriptions does not imply identity of generated names.

Interpretation: nominal/name theories are mature suppliers; SCD DescriptionIdentity remains unresolved only if a cross-representation/branch/currentness notion survives beyond those theories.

## R-RESOURCE

Description-level specification: `space bound ≤10MB`.

Separate claims:

- meaning/satisfaction/preservation of the annotation: potentially SCD;
- abstract feasibility/complexity: CP;
- actual observed memory usage: Runtime.

A Runtime observation of 12MB can falsify an execution-conformance claim without changing the meaning of the annotation itself.

# Corpus-level negative laws

The following observations never suffice alone for semantic preservation:

- same bytes;
- same file identity;
- successful serialization;
- successful execution;
- Host continuity;
- Network availability;
- consumer compatibility.

Every preservation claim requires an explicit semantic scope and justified correspondence/support.
