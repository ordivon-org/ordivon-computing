# Book Capability Exposure Falsifier v0 — Result

Status: CLOSED — representation effect established; action-capability delta not identified
Date: 2026-08-26

## Standing

The current seven-chapter Book already contains constructive capability content, but a fresh Agent does not recover it with stable organization. Adding one bounded chapter-end capability gestalt per chapter, without moving or deleting any existing distinction/non-claim prose, makes the seven capability families reliably recoverable in this Agent/model/operation.

This establishes a **capability-exposure / self-model-recovery representation effect**. It does **not** establish new underlying Ordivon capability, universal reader benefit, or action-quality gain.

## Frozen source fences

- Media: `9aa03e1eef97093af772c9020e66bee231ad1cfe`
- Book baseline SHA-256: `799af49c40d0e4162cc0c7cfdeebf563b0c915157a97fd789004ea388fff23b1`
- Computing: `561ce47fc5c57b6f8d164a68f896f4757a31e4be`
- Harness: `684333be5146d4f705a91edb396e83c6a1150e1f`
- Workstation current evidence fence: `8f7ddc7dbb29a36d885d1221db48a344d495cdcb`
- Finance current evidence fence: `5aa298ebc8ca6b9f7c6f376b1eeb89164e379641`

## Arms

- BASELINE — exact Book bytes.
- REORDER — moves Chapter 2–7 non-claim landing before existing final constructive/minimal-model block; no semantic additions.
- GESTALT — REORDER + one bounded capability gestalt per chapter.
- GESTALT_ONLY — exact BASELINE order + the same seven capability gestalts.

GESTALT_ONLY is the minimal successful arm. REORDER is therefore rejected as unnecessary.

## Corrected v1c capability-recovery result

Fresh `deepseek-v4-flash`, one call, no Runtime Tools, same question and carrier. Metric is whether the answer spontaneously organizes the Book into the seven already-earned capability families.

| Arm | Replicate family coverage | Mean | Prompt tokens | Delta vs baseline |
|---|---|---:|---:|---:|
| BASELINE | 4/7, 7/7, 4/7 | 5.0/7 | 34727 | — |
| REORDER | 5/7, 6/7, 7/7 | 6.0/7 | 34727 | 0 |
| GESTALT | 7/7, 7/7, 7/7 | 7.0/7 | 35194 | +467 (1.34%) |
| GESTALT_ONLY | 7/7, 7/7, 7/7 | 7.0/7 | 35194 | +467 (1.34%) |

Book bytes: 167,429 → 169,922, +2,493 bytes (1.49%).

The lexical counts in `v1c-metrics.json` are diagnostics only. They show that REORDER alone actually increased crude negative-marker frequency, while GESTALT/GESTALT_ONLY exposed all seven capability families. The result is not interpreted as a global positive-vs-negative word-count law.

## Action/authority safety control

A 12-case owner-grounded routing battery tested current Workstation, Finance and Harness boundaries plus effect/currentness/composition cases. Three replicates per arm:

- NOBOOK: 36/36
- BASELINE: 36/36
- REORDER: 36/36
- GESTALT: 36/36
- GESTALT_ONLY: 36/36

This is a ceiling control. It establishes **no observed routing/boundary regression**, but cannot establish action gain because NOBOOK already reaches 100%.

A harder 10-case synthetic far-transfer smoke also yielded NOBOOK 10/10, so that battery is likewise rejected as an efficacy measure rather than used to manufacture a positive result.

## Apparatus falsification

The first structured-result pilot produced GESTALT 3/3 and REORDER 2/4 conclusion failures. A retained Harness trace identified `conclusion_rejected.argumentError=invalid_json` after Provider `finishReason=tool_calls`. The same GESTALT under the corrected record/summary carrier completed normally.

Therefore the structured pilot is `INVALID_FOR_EFFICACY`: it demonstrates a representation × carrier/conformance interaction, not worse semantic cognition. See `structured-carrier-failure-evidence.json` and `APPARATUS-CORRECTION.md`.

## Interpretation

Supported:

```text
Underlying Book capability content
  -> chapter-end capability organization
  -> more stable fresh-Agent capability recovery
```

Not supported:

```text
capability gestalt
  -> new owner capability
  -> better action outcome
  -> universal writing law
```

The best model is not Positive vs Negative. It is:

```text
Discrimination
-> Organization
-> Construction
-> Exposure
-> Uptake
```

The current Book is strong at Discrimination and contains Construction, but under-exposes the organized capability gestalt. GESTALT_ONLY repairs Organization/Exposure while preserving the existing anti-collapse boundaries.

## Admission decision

`ADMIT_GESTALT_ONLY_REPRESENTATION_REPAIR`

Admit only:

1. one bounded chapter-end capability gestalt for each current chapter;
2. a Book Constitution requirement that mature chapters state what capability/reachability is constructed or recovered, with scope/maturity/non-claim boundary;
3. a Fresh-Agent consumer question asking what the system can now reliably distinguish/build/recover/route/reach that was not stable before.

Reject:

- moving existing non-claim sections;
- deleting distinction language;
- positive/marketing rewrite;
- global Capability ontology/registry/service;
- claiming action-capability improvement from this experiment.

## Reopen conditions

Reopen efficacy, rather than representation recovery, when a non-ceiling downstream task exists: different model family, Human reader test, low-context Agent, real operation choice with ambiguous evidence, or longitudinal evidence that capability exposure changes action selection or consequence.

## Canonical EOF normalization verification

The Media validation gate rejected the initially generated treatment bytes only because `git diff --check` detected a terminal blank line. The final output normalizes the file to one trailing newline. The resulting exact Book digest is `sha256:14e5e15b9223cf6beee4ce3981eebc197c837f899948140e6daf96cfca6597c4` (169,921 bytes).

This exact normalized byte sequence was rerun under the corrected v1c carrier for three fresh replicates. Result: `7/7, 7/7, 7/7` capability-family recovery, all `candidate_completed`, with the same 35,194 prompt-token count. Therefore EOF normalization does not change the admitted representation effect, and `14e5e15b...` is the canonical tested Book output digest.
