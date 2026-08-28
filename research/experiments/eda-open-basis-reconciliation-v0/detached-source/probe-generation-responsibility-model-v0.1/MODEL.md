# Probe Generation Responsibility Model v0.1 — Grammar-bounded generation vs open invention

## EDA transfer

The previous schematic overconstraint counterexample used a manually authored `label-equivalent` mutation. EDA Mutation Probe Generation v0.1 removes that hand-authored location from the generation path.

Starting from the admitted correct KiCad schematic, a bounded mutation grammar enumerated:
- one fresh local label at every unique existing wire endpoint;
- removal of every existing wire.

This yielded 96 real single-edit candidates (55 label placements + 41 wire removals). Every candidate was executed through KiCad 10.0.5 and observed for ERC electrical cleanliness, R1.1/U1.1/U1.7 connectivity, and target-net naming.

Six generated label mutations preserved ERC + functional connectivity while changing only the target net name. They therefore separate:

`H_connectivity_semantic`
from
`H_exact_net_name`.

The generator independently rediscovered the prior hand-authored witness and five additional equivalent endpoints on the same electrical net.

## Generation is itself layered

```text
Open Research Pressure
       ↓
Mutation / Experiment Grammar
       ↓
Bounded Candidate Enumeration
       ↓
Provider Execution / Outcome Model
       ↓
Relation Projection
       ↓
Hypothesis Separation
       ↓
Outcome Equivalence / Cost
       ↓
Probe Selection Compiler
```

Once the mutation grammar and provider-observable consequences are explicit, both generation and selection may be deterministic.

The true unresolved frontier is therefore not generically “generate a probe.” It is:

- construct/extend the mutation grammar;
- expose the right domain features;
- predict or obtain outcome models where provider execution is expensive/unsafe;
- invent experiments outside the current action vocabulary.

## Negative boundary

With the same EDA evidence but a grammar restricted to `remove_wire`, Probe Generation Compiler returns:

`no_discriminator_in_generation_basis`.

It does not conclude that no discriminator exists and does not ask an Agent to choose among zero witnesses. This distinction is essential:

`no candidate in current basis != impossibility in Reality`.

The next responsibility is basis expansion/hypothesis generation.

## Equivalence family

All six generated label probes are consequence-equivalent for the current responsibility projection. Their coordinates/source-wire identities differ, but each yields:

- ERC clean;
- target functional connectivity preserved;
- target net name changed;
- opposite predicted outcome under the two current hypotheses.

Therefore source-level probe identity is not the selection ontology. A stable deterministic representative may be chosen once the operation authorizes any equal-cost equivalent discriminator.

## Cross-domain assimilation evidence

Capability Assimilation now has a second, non-Boolean form:

1. Boolean relation synthesis: Agent crossed a search frontier, then the complete finite grammar search was assimilated.
2. KiCad EDA probe generation: a previously hand-authored discriminator is regenerated as one member of a provider-verified mutation family from a bounded domain grammar, with no Agent required for enumeration or selection.

This is still insufficient for a universal law. Both positive cases rely on a declared bounded grammar. What generalizes more strongly is the methodological pressure:

> whenever a frontier action becomes representable as a bounded searchable grammar with trustworthy consequence evidence, reevaluate whether repeated Agent cognition should remain responsible for it.

## Boundary

No claim is made that arbitrary EDA experiments are enumerable, that current mutation grammar is complete, or that owner contract meaning can be derived from KiCad. Owner/domain adjudication remains separate. Physical probes remain outside this evidence.
