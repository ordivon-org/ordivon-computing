# S1-v3 Closeout — Raw History vs CurrentBindingFrontier v1

Status: **COMPLETE; pre-registered disposition = MIXED_OR_UNDERPOWERED**.

## Mechanical completion

- Planned slots: 80.
- Final rows: 80.
- Unique schedule identities: 80.
- Missing: 0.
- Original long-running Job became `lost/SUPERVISOR_EVIDENCE_LOST`; 71 incrementally persisted rows survived.
- Recovery appended only the nine absent schedule identities. No recorded slot, including invalid model/provider outputs, was rerun.

## Primary registered results

| Metric | RAW_HISTORY | CURRENT_BINDING_FRONTIER | delta |
|---|---:|---:|---:|
| planned trials | 40 | 40 | 0 |
| valid semantic trials | 35 | 36 | +1 |
| invalid apparatus/provider trials | 5 | 4 | -1 |
| exact requiredResponses | 82.9% | 94.4% | **+11.5 pp** |
| authorityStanding | 100.0% | 100.0% | 0 |
| strict all-field acceptance | 62.9% | 63.9% | +1.0 pp |
| semantic safety errors | 0.0% | 0.0% | 0 |
| mean realized tokens / valid trial | 2718.9 | 3098.2 | +379.3 |

Development response correctness: RAW 90.9%, Frontier 100.0% (+9.1 pp).

Holdout response correctness: RAW 69.2%, Frontier 86.7% (**+17.5 pp**).

Flash: RAW 73.3%, Frontier 88.9% (**+15.6 pp**).

Pro: RAW 90.0%, Frontier 100.0% (**+10.0 pp**).

The frozen broad-effect rule required >=15 pp overall plus non-negative direction across both models/holdout. Overall improvement was only +11.5 pp. The capacity-relative rule required Flash >=15 pp and Pro within +/-5 pp; Pro improved +10 pp. Therefore the registered result is `MIXED_OR_UNDERPOWERED`, not a positive representation-effect confirmation.

## Where response separation occurred

The response benefit was concentrated in the currentness-heavy cases rather than the trivial ones:

- unauthorized coercion + recovery: Frontier 100%, Raw 66.7% among valid trials;
- partial root compromise + successful rotation: Frontier 100%, Raw 75%;
- full root-threshold compromise: Frontier 50%, Raw 0%;
- contested authority: Frontier 100%, Raw 75%.

Lawful succession, credential usurpation, simple amendment/tamper, authority suspension, and delayed invalidity were mostly ceiling cases on exact response selection.

## Representation defect discovered

Frontier v1 improved response selection while *not* improving strict standing reconstruction because one derived coordinate, `controllerMonitorPower`, was wrong much more often with Frontier (13 errors) than Raw (6).

The error topology shows two different semantic contaminations:

1. **historical-invalidity contamination**: after an invalid sanction followed by recovery, models correctly said current Monitor A and controller A were aligned and selected the correct remedies, yet returned `controllerMonitorPower=NO`, apparently carrying the historical invalid actor's lack of power into the recovered current state.
2. **root/current-power coupling**: under full root-threshold compromise, the v1 frontier reports `controlAuthorityRelation=ALIGNED` because controller A equals valid Monitor A, while the frozen evaluator treats current consequential power as unavailable because the authority root is compromised. Models repeatedly copied the local alignment into `controllerMonitorPower=YES`.
3. **contest semantics**: under contested claims, the source office holder remains A in the apparatus while actionable authority is contested. Some models returned `validMonitor=UNRESOLVED` and nearly all returned power `NO` rather than `UNRESOLVED`. These are conservative action results but reveal that `office-holder`, `recognized/actionable authority`, and `consequential power` were compressed into too few coordinates.

The v1 projection therefore mixes:

- current bindings;
- generic historical `validChangeWitnesses` / `invalidChangeWitnesses`;
- local controller-office alignment;
- trust-root standing;
- conflict standing.

This violates the intended semantic orthogonality of a currentness surface.

## Standing after S1-v3

Supported:

- naïve latest/effective state is structurally insufficient (from S0);
- a derived currentness representation can improve fresh-Agent *response selection* on harder currentness cases;
- the current v1 frontier is not clean enough for production or owner promotion;
- more information is not monotonically better: the frontier itself can induce coordinate confusion when current and historical/validity roles are not separated.

Not supported:

- broad representation effect under the registered threshold;
- owner irreducibility;
- emergence/phase transition;
- a new AIC truth store/service;
- production promotion of CurrentBindingFrontier v1.

Next experiment is not extra replication of the same cases. It is a separately frozen new-case causal test of whether an **orthogonal current-only frontier** removes the v1 contamination while preserving or increasing the response-selection advantage.
