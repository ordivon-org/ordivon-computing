# TM2 — Research Taste as Operator Selection Report

## Question

After TM1 rejected a static research-taste prompt, TM2 tested a narrower operational hypothesis:

> research taste can improve tractability when it selects a better **observation operator** from the current evidence shape, without adding more methodological prose to the model.

Two materially different owner pressures were frozen before live Provider trials:

- Harness `H-NOTOOL` at `999d7535242b14c432cd14527ec109f2c6749969`;
- Security `S-UNKNOWN` at `f109cb8cc548479e852c8a4dbc914bd7d3e22ce0`.

Each used the same `deepseek-v4-flash` model and the same total budget of eight observations.

- **open:** Agent chooses all observations;
- **evidence_first:** two literal Git searches using anchors already explicit in owner evidence are executed before the first Agent turn. They count as two of the eight observations and their bytes count normally. No TM0 research-taste prose is supplied.

Accepted receipt: `evidence/tm2-live-v1.json`.

Receipt digest:

`sha256:f383db610f40846a4750b085d081abce29e73a0d2ad012d225d3fc22260a5edf`

## Result

### Harness H-NOTOOL

| Measure | Open | Evidence-first |
|---|---:|---:|
| Successful causal localizations | 1/3 | 2/3 |
| Causal submissions | 1/3 | 2/3 |
| Forced budget abstentions | 2/3 | 1/3 |
| Mean score / 6 | 1.67 | 4.00 |
| Mean observations | 8 | 8 |
| Mean source bytes | 22,750 | 27,537 |
| Provider tokens | 225,567 | 181,027 |
| Seed required-file coverage | 0 | 2/2 |

The evidence-first operator improved success while using about **19.7% fewer Provider tokens**. It consumed more source bytes because the deterministic anchors deliberately loaded high-value exact evidence early; that additional byte cost nevertheless reduced model deliberation cost.

Both successful evidence-first submissions explicitly localized the actual owner interaction:

```text
conclusion correction in loop.py
→ bind_run_state()
→ SQLiteHarnessAgentBridge.bind_run_state
→ no-Tool rejection when observations / Tool Call identities are non-empty
```

The no-Tool authority boundary remained intact; neither successful submission proposed enabling arbitrary Tools.

### Security S-UNKNOWN

| Measure | Open | Evidence-first |
|---|---:|---:|
| Successful causal localizations | 2/3 | 3/3 |
| Causal submissions | 3/3 | 3/3 |
| Forced budget abstentions | 0/3 | 0/3 |
| Mean score / 6 | 5.00 | 5.00 |
| Mean observations | 8 | 8 |
| Mean source bytes | 35,791 | 29,692 |
| Provider tokens | 209,949 | 215,786 |
| Seed required-file coverage | 0 | 2/2 |

Evidence-first converted the only sub-threshold open submission into a successful causal localization and reduced source bytes by about **17.0%**, at a small ~2.8% Provider-token increase.

All three evidence-first submissions independently identified the Security-owned loss path: `HostAssignedDeepSeekHarnessTurnDriver` forces candidate-completed unknowns empty in its prompt, discards the Harness conclusion's unknown structure when constructing `AgentTurnEvidence`, and later records `unresolved_unknowns: []` into Host lifecycle evidence. The successful claims did not move the responsibility into Harness core.

### Combined signal

Across both consumers:

- successful localizations improved from **3/6 → 5/6**;
- total Provider tokens fell from **435,516 → 396,813**, about **8.9% lower**;
- aggregate mean source-byte cost was about **2.2% lower**;
- the two deterministic owner-evidence searches had **2/2 hidden required-file coverage for both consumers** before the Agent began open-ended reasoning.

The last point is especially important. The seeds were not chosen from the hidden oracle. They were literal handles already present in owner evidence: an exact error string / correction phrase for Harness, and an owner class name / field name for Security. Yet those simple classical operators collapsed the source search space to include every hidden required file in both materially different consumers.

## Interpretation

TM2 supports a different account of scientific research taste than TM1.

### Taste looks more like conditional operator selection than extra reasoning prose

The useful transformation was not:

```text
Agent + more methodological maxims
```

It was:

```text
shape of current evidence
→ choose a cheap discriminating operator
→ shrink the live search space
→ let Agent reason over the resulting evidence
```

For exact diagnostic/symbolic software pressures, literal search is a mature classical operator with very high leverage. A good research Agent should recognize that topology rather than spend model calls reconstructing it.

This supports TM0 RT4 (strong simpler baseline), RT6 (observability before optimization), and RT12 (questions/observations should change the frontier), while sharpening them into a conditional policy rather than a universal instruction.

### Evidence topology matters

TM2 does **not** prove “always grep first.” It supports a narrower world-model claim:

> when owner evidence contains exact diagnostic strings, stable symbol identities, or field names that bind to source, deterministic identity-preserving retrieval is often a more tractable first operator than open-ended semantic exploration.

Other evidence topologies require other operators: a timing race may require an adversarial physical probe; human product value may require blind play; external-effect ambiguity may require reconciliation rather than source search.

This starts to make research taste look like a mapping:

```text
evidence topology
→ likely high-value observation / intervention operator
```

### The stopping problem remains unsolved

Both open and evidence-first treatments used the full eight-observation budget on average. Even when the two seed searches had already found every hidden required file, the Agent usually continued reading/searching until close to exhaustion.

So operator selection improved **where to look**, but not **when enough evidence has accumulated**.

This is the next tractability bottleneck.

## Disposition

- **Support:** research taste as a conditional operator-selection prior for exact diagnostic/symbolic evidence topologies.
- **Reject:** any conclusion that literal search is a universal research method.
- **Retain:** owner-evidence anchors, exact Git/source binding, per-trial durable evidence, and explicit observation cost.
- **Do not build:** generic query planner, Skill registry, or ResearchTaste service.
- **Next falsifier:** for retrieval-dominated exact-symbol tasks, compare iterative Agent search against deterministic evidence compilation followed by a single semantic synthesis call. If the classical compilation dominates, the correct taste decision is to avoid an Agent loop altogether for that problem class.
