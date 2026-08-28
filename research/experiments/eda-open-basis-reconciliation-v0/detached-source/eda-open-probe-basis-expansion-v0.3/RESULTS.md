# EDA Open Probe Basis Expansion v0.3 — Results

v0.3 moved already-solved KiCad Standing extraction out of the Agent. `BASELINE-STANDING.json` exposed current ERC cleanliness, target net membership/name, unique target-pin coordinate bindings and directly incident wire witnesses, but no mutation operator or known separator.

All three clean-Agent processes still reached the 360s episode limit and none produced the required `proposal.json`. Delivery-contract score is therefore 0/3.

However hidden provider verification finds a decisive semantic difference from v0.2:

- trial 1 changed only `ecc83-pp_v2.kicad_sch` and produced a **valid discriminator**;
- trial 2 and trial 3 left the project unchanged.

Trial 1 independently inserted one local KiCad label:

```text
(label "GRID_A"
  (at 157.48 58.42 0)
  ...)
```

That mutation kind/name/location were not present in the frozen Standing or task. Hidden KiCad 10.0.5 verification established:
- schematic remains provider-parseable;
- electrical ERC remains clean apart from the admitted footprint-link class;
- `R1.1/U1.1/U1.7` remain one connected net;
- the exact target net name changes from `Net-(U1A-G)` to `/GRID_A`;
- therefore `H_connectivity_semantic` predicts accept while `H_exact_net_name` predicts reject.

So trial 1 is a **semantic basis-expansion witness despite delivery failure**:

`Effect succeeded != Delivery succeeded`.

Session reconstruction shows the Agent reached the `GRID_A` source mutation at roughly 161 seconds after first model usage. It then spent the remaining budget on ad-hoc verification/reconstruction, including several failed attempts to create/validate a baseline copy with the wrong file-extension/context. The hidden deterministic verifier later established the candidate consequence cleanly.

This means the next architectural move is not prompt-tuning for faster termination. The successful frontier mutation should be tested for grammar assimilation, while consequence verification/lowering should remain deterministic/provider-owned.

Boundary: 1/3 semantic witness is evidence of capability, not evidence of reliable Agent default execution. The operator is useful only after independent provider verification and bounded grammar extraction.
