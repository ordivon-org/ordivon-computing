# OFR4 — Representation Competition Results

## Verdict

OFR4 does **not** promote a Theory Unit representation.

The frozen holdout selector mechanically returned `full_eight_role`, but the scientific disposition is `NO_THEORY_UNIT_PROMOTION`. Two independent problems prevent promotion: the action/reopen target was semantically invalid, and the full representation's perfect survivor score came from only 4/12 accepted holdout trials covering 3/6 holdout cases.

| Treatment | Accepted | Overall role | Critical role | Raw reopen accuracy* | Unsupported | Overgeneralized | Mean prompt tokens | Physical acceptance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full eight-role | 4/12 | 1.000 | 1.000 | 1.000 | 0 | 0 | 1557.0 | 33.3% |
| causal kernel | 10/12 | 0.800 | 0.840 | 0.500 | 10% | 10% | 1480.3 | 83.3% |
| minimal causal chain | 8/12 | 0.906 | 0.938 | 0.625 | 0 | 0 | 1385.0 | 66.7% |
| winner only | 11/12 | 0.517 | 0.482 | 0.364 | 9.1% | 9.1% | 1224.2 | 91.7% |

`*` The reopen-decision column is retained as raw evidence but is **invalid for selection**; see the measurement diagnosis.

## What the compression experiment actually falsified

### Winner-only is not enough

The negative control realizes easily, but it destroys the causal search boundary. On the broadest accepted holdout coverage it retained only ~0.48 critical-role fidelity. Keeping only the winner/invariant therefore makes future Agents reconstruct rejected alternatives and failure boundaries from guesswork.

### Retained consequence is not safely externalizable

`causal_kernel` kept rival+attraction, falsifier, counterfactual, boundary and reopen condition but omitted a dedicated retained consequence. Holdout retained-consequence fidelity fell to **0.50**. A future Agent needs not only why the rival lost but what concrete engineering/product responsibility survived.

### Minimal causal chain is promising but not non-inferior

The aggressive chain cut mean packet words from ~282 to ~182. Conditional holdout critical-role fidelity remained 0.938, but decisive-falsifier fidelity was 0.75 and overall role fidelity 0.906, outside the frozen 0.03 non-inferiority band. It therefore remains a research candidate, not a promoted default.

## Compression moved cost instead of simply deleting it

Packet-word reduction overstated real Provider savings because fixed instructions/schema remain and the model must reconstruct omitted semantics.

Holdout mean prompt-token savings versus full:

- causal kernel: **4.9%**;
- minimal chain: **11.1%**;
- winner only: **21.4%**.

Yet successful causal-kernel runs used **1115 mean completion tokens** versus **906** for successful full packets. The shorter packet made the receiver do more work. This is direct Ordivon evidence for receiver-conditioned compression: omission can move complexity from Context into inference/output rather than remove it.

## Realization reliability is a separate axis

Across holdout, every non-accepted trial failed in generation realization; valid generated answers always reached a valid independent judge. `full_eight_role` produced 8/12 `no_progress` outcomes and completely missed Harness, Finance and Workstation. `winner_only` realized 11/12.

This is operationally real but not yet a clean causal law about length. The sample is small and case/treatment interactions remain. We therefore keep two coordinates:

```text
Semantic Sufficiency != Realization Reliability
```

A representation can be semantically richer and mechanically harder for the current Provider/Harness surface to realize.
