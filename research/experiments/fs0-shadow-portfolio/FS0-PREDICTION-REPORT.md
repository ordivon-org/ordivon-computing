# FS0 — Shadow Portfolio Prediction Freeze

## Status

FS0 prediction stage is complete and frozen. Owner work was not influenced by the selector.

Accepted prediction receipt:

`evidence/fs0-predictions-v1.json`

Receipt digest:

`sha256:bb406bf0907e9bb23fa41c9306c876b5f44b0dfe388008b9eb5c1deb776f89fc`

The cohort was frozen before accepted selector calls. No owner checkpoint newer than the cohort cards was read until after the receipt converged.

## Cohort

Primary candidates:

- `H-P6` — Harness recursive-discovery token utilization;
- `R-P5` — Runtime physical-foundation closeout;
- `G-AF3` — Game cross-encounter prior generalization;
- `HOST-PKG` — Host package/import dependency surface;
- `F-C2-BLOCKED` — Finance remote C2 activation, deliberately included as admission-blocked negative control.

Crosscut HP was excluded from primary scoring because it is itself testing TM/RF operator-policy priors and would contaminate the method evaluation.

## Raw selector

Five independent same-model replicates produced exactly the same complete ranking:

```text
G-AF3 > R-P5 > HOST-PKG > H-P6 > F-C2-BLOCKED
```

Top choice:

```text
G-AF3 5 / 5
```

The raw selector consistently reasoned that Game AF003 is the only unblocked candidate whose next unit primarily creates **new discriminating evidence** rather than mechanically closing or packaging an already-established mechanism. It predicted the key discriminator as whether AF002 priors survive materially different encounter variants or collapse into fixed-encounter overfit.

Raw selector Provider tokens: `15,562` total.

## RFM-informed selector

Five independent replicates produced:

```text
R-P5 top choice 4 / 5
G-AF3 top choice 1 / 5
```

Mean ranking:

```text
R-P5        1.2
G-AF3       1.8
HOST-PKG    3.0
H-P6        4.0
F-C2        5.0
```

The RFM selector weighted **current closability, exact validation path, authority already present, and bounded release semantics** more strongly. It treated Runtime P5 as a near-terminal owner-mechanism-change opportunity: selected physical mechanisms already survived hard attacks and the remaining path was final gates → exact commit → structured self-release.

RFM selector Provider tokens: `17,178` total, about 10.4% more than raw. Wall-time totals are not interpreted as cognition cost because Provider/network latency differed substantially between treatments.

## Negative control

Both treatments passed the admission-awareness check:

```text
F-C2-BLOCKED top choice: 0 / 10
F-C2-BLOCKED deferred:   10 / 10
mean rank:               5.0 in both treatments
```

Thus the compact RFM did not earn unique credit for recognizing this obvious blocker; the raw selector already did so perfectly.

Harness P6 also remained fourth in both treatments. Raw deferred it in 3/5 runs; RFM deferred it in 4/5. Both recognized that an external DeepSeek DNS dependency prevented the immediate live utilization experiment from closing at the frozen boundary.

## Deterministic baselines

Frozen simple choices:

```text
newest-task       → H-P6
narrowest-scope   → HOST-PKG
closest-to-closure→ R-P5
```

The RFM consensus therefore currently coincides with the simple `closest-to-closure` baseline. If Runtime later dominates, FS0 cannot claim the RFM was uniquely responsible without showing an advantage beyond that baseline.

## The key prospective disagreement

FS0 has created a useful future falsifier:

```text
RAW:
  prioritize new information / prior generalization
  → choose Game AF003

RFM:
  prioritize closability / verified mechanism graduation
  → choose Runtime P5
```

This exposes an objective-level distinction that FS0 must not erase after outcomes arrive.

Research value remains a vector. A successful Game result may provide high prior-generalization value at higher experimental breadth; a successful Runtime result may provide lower epistemic novelty but stronger immediate mechanism closure. If neither outcome Pareto-dominates the other, FS0 must record them as **incomparable under the current non-scalar value model** rather than manufacturing a universal winner.

## First post-freeze observation

After the prediction receipt was durable, owner checkpoints were re-observed.

Runtime P5 advanced from frozen revision 4 to revision 5. The owner reports source main / P5 Workspace at `8ce1ee696ec16fb472e6b6b37ae889bbca87a7a8`, after a documentation-only truth correction naming the exact Windows immutable-input root. Fresh exact local acceptance had progressed; production rollout remained gated by unrelated active Runtime Jobs before a fresh structured self-release could be admitted.

This is directionally consistent with the RFM's **closability** prediction, but it is not yet a terminal outcome and does not establish selection superiority. It also supports the raw selector's warning that much of the remaining Runtime work is closeout/validation rather than a new research frontier.

At the same observation boundary:

- Game remained at revision 12 with AF003 still next, so no post-freeze Game outcome exists yet;
- Harness remained at revision 4, still waiting for the live P6 trajectories after DNS recovery;
- Host packaging remained at revision 2;
- Finance remained at revision 9 with the independent-host admission blocker unchanged.

Therefore **selection regret is not yet identifiable**. FS0 must remain a prospective cohort rather than pretending one early Runtime checkpoint is the portfolio outcome.


## P0-C statistical calibration

The frozen selector counts are now accompanied by a sampling-uncertainty calibration in [`statistical-calibration-v1.json`](statistical-calibration-v1.json). The prediction receipt itself is unchanged and is not rerun.

Using 95% Wilson score intervals:

```text
raw G-AF3 top choice      5 / 5   point 1.00   interval [0.566, 1.000]
RFM R-P5 top choice       4 / 5   point 0.80   interval [0.376, 0.964]
negative-control chosen   0 / 10  point 0.00   interval [0.000, 0.278]
negative-control deferred 10 / 10 point 1.00   interval [0.722, 1.000]
```

The raw and RFM top-choice intervals overlap materially. Therefore the small replicate set does **not** establish that one treatment is intrinsically more stable than the other. Likewise, `0/10` and `10/10` remain useful observations but are not zero-error / perfect-reliability claims.

This estimator has deliberately narrow authority: it calibrates stochastic evidence. It does not choose research value, identify selection regret, decide between the raw/RFM objectives, or turn selector frequency into semantic truth.
