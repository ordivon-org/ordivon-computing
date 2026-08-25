# S3 Closeout — Agent Replacement / Environmental Inheritance

Status: **COMPLETE; pre-registered disposition = EXTERNALIZATION_SUFFICIENCY**.

## Mechanical completion

- 8 held-out replacement scenarios.
- 4 inheritance arms: RESET_EFFECTIVE, PREDECESSOR_NOTE, RAW_LEDGER, GOVERNED_FRONTIER.
- 2 successor models x 2 replicates = 128 planned successor trials.
- Final combined evidence: 128 rows / 128 unique schedule identities.
- Recorded provider/Harness invalids were retained and never retried.
- Predecessor notes were produced before post-replacement shocks and were not oracle-corrected.

## Overall results

| Arm | valid | exact response | consequence authority | strict | safety errors | mean tokens |
|---|---:|---:|---:|---:|---:|---:|
| RESET_EFFECTIVE | 30/32 | 76.7% | 90.0% | 63.3% | 2 | 3662.4 |
| PREDECESSOR_NOTE | 32/32 | 71.9% | 81.2% | 59.4% | 0 | 3778.6 |
| RAW_LEDGER | 31/32 | 83.9% | 96.8% | 80.6% | 1 | 3799.3 |
| GOVERNED_FRONTIER | 31/32 | **83.9%** | **100.0%** | **83.9%** | **0** | **3340.7** |

Registered deltas:

- Governed vs Reset response: +7.2 pp.
- Governed vs Predecessor Note response: +12.0 pp.
- Governed vs Raw response: 0.0 pp.
- Governed vs Raw consequence-authority: +3.2 pp.
- Governed vs Raw realized token reduction: **12.1%**.

The stronger `GOVERNED_INHERITANCE_CAPABILITY` rule did not trigger because Governed response accuracy was below 90% and its advantage over RESET_EFFECTIVE was below 15 pp.

`GOVERNANCE_OVER_PROSE` did not trigger because the overall response advantage over predecessor prose was 12 pp (<15 pp) and the prose arm had no registered semantic safety error overall.

`RAW_HISTORY_NEEDED` did not trigger.

The only registered disposition is **EXTERNALIZATION_SUFFICIENCY**: Governed Frontier stayed within 5 pp of Raw Ledger on response and consequence-authority accuracy while reducing mean tokens by >=10%.

## Interpretation

S3 supports a bounded claim:

> A deterministic owner-derived current-binding artifact can cross complete Agent/context replacement and substitute for the full pre-handoff raw ledger on these held-out histories without measured response loss, while reducing consumption cost.

This is stronger than ordinary memory persistence because the successor receives neither predecessor conversation nor predecessor hidden state. It is weaker than a general inheritance capability claim because RESET_EFFECTIVE remains competitive on many ceiling/easy scenarios and Governed still has response-policy residual errors.

## Important failure topology

1. **Predecessor prose propagates semantic error.** The predecessor misdescribed refoundation/succession in some handoff notes, and successors inherited those mistakes. This directly demonstrates error propagation through Agent-authored memory.
2. **Raw history is not an oracle.** Full ledgers still produced authority/response errors and one semantic safety error; complete evidence does not eliminate the finite reconstruction problem.
3. **Governed currentness is not a policy oracle.** Governed had 100% consequence-authority correctness but only 83.9% exact response accuracy. CorrectNow != SafeNext remains supported.
4. **Reset can succeed accidentally or by local inferability.** Aggregate reset accuracy is too high for a broad dominance claim, so future tests should target invariants and continuity-sensitive perturbations rather than averaging many low-information cases.

## Standing

Supported:
- environmental externalization can substitute for full history across fresh-Agent replacement in this bounded apparatus;
- governed representation can reduce continuity-consumption cost;
- prose handoff can propagate predecessor semantic errors;
- history sufficiency, currentness sufficiency, and response-policy sufficiency are distinct.

Not supported:
- universal superiority of governed inheritance over reset;
- production promotion;
- owner irreducibility;
- institutional emergence;
- open-world legitimacy;
- a new truth store.

Next stage: S4 metamorphic/property falsification over continuity laws before any broader architecture promotion.
