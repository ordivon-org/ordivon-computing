# TM3 — Compiled Evidence vs Iterative Agent Search Report

## Question

TM2 showed that two deterministic owner-evidence searches can locate every hidden required file for both Harness and Security, but the iterative Agent still consumes almost the complete observation budget.

TM3 tested the contraction:

> for exact diagnostic/symbolic, retrieval-dominated research questions, can deterministic evidence compilation followed by one semantic synthesis call replace iterative Agent discovery?

The accepted TM2 `evidence_first` trials were frozen as the iterative comparator rather than re-run.

TM3 used the same owner revisions and the same two literal-search anchors. Candidate files were ranked mechanically by distinct anchor match count, hit count, then path. Bounded windows were compiled up to the same maximum eight physical evidence observations. The model received that packet once and had only a `submit` Tool.

Accepted receipt: `evidence/tm3-live-v1.json`.

Receipt digest:

`sha256:113282437d80e0fb9e45e0fac2f63e612b0c90b810b6653923e17c02c64ff142`

## Harness — localized diagnostic topology

TM3 was decisively positive on `H-NOTOOL`.

| Measure | TM2 iterative evidence-first | TM3 compiled one-shot |
|---|---:|---:|
| Successful causal localizations | 2/3 | **3/3** |
| Mean score / 6 | 4.00 | **6.00** |
| Mean physical observations | 8 | **5** |
| Mean source bytes | 27,537 | **13,955** |
| Provider tokens | 181,027 | **14,721** |
| Provider calls | many iterative turns | **3 total, one per replicate** |

Relative to the accepted TM2 comparator, compiled one-shot used about:

- **91.9% fewer Provider tokens**;
- **49.3% fewer source bytes**;
- **37.5% fewer physical observations**;

while improving success from 2/3 to 3/3.

All three trials independently produced the full owner-local causal chain:

```text
loop.py conclusion-correction branch
→ bind_run_state()
→ SQLiteHarnessAgentBridge.bind_run_state
→ no-Tool guard rejects non-empty Tool observation / Tool Call identity state
```

The deterministic compiler needed only five observations because the exact failure string and correction phrase concentrated the relevant causal structure in three read windows: `loop.py`, `sqlite_agent_bridge.py`, and the conclusion-correction test.

For this topology the iterative Agent loop was unnecessary overhead.

## Security — distributed representation/dataflow topology

The same method failed completely on `S-UNKNOWN`.

| Measure | TM2 iterative evidence-first | TM3 compiled one-shot |
|---|---:|---:|
| Successful causal localizations | **3/3** | **0/3** |
| Mean score / 6 | **5.00** | 1.33 |
| Mean physical observations | 8 | 8 |
| Mean source bytes | 29,692 | **16,511** |
| Provider tokens | 215,786 | **19,932** |
| Search required-file coverage | 2/2 | 2/2 |
| Read required-file coverage | adaptive | **1/2** |

Compiled one-shot was roughly 90.8% cheaper in Provider tokens and 44.4% cheaper in source bytes — and still scientifically worse.

This is an important L5-style result for research itself:

```text
cheaper research execution
!=
trusted semantic progress
```

The two literal searches did identify both hidden required files in their match lists, but the mechanical candidate ranking read `host_assigned.py` plus high-frequency surface/import files and never read the remote `AgentTurnEvidence` definition in `agent_stack.py`. The one-shot model correctly noticed the hard-coded empty list and prompt restriction but did not reconstruct the full type→prompt→driver→persistence loss path.

One trial even mislabeled the Security-local `agent_stack.py` rule as a Harness-core semantic rule. The packet therefore preserved textual evidence while losing the ownership/dataflow relation required for the correct world model.

By contrast, TM2's adaptive Security Agent could follow the representation relation across source locations and reached 3/3 successful localizations.

## Why the domains differ

Both pressures contain exact symbols and both seed searches have 2/2 hidden required-file coverage. The difference is not simple retrieval success.

### Harness topology

```text
exact runtime error
→ local guard
↕ nearby caller/correction path
```

The causal relation is spatially and symbolically concentrated. Literal identity-preserving retrieval plus bounded local context is sufficient.

### Security topology

```text
representation type
→ prompt constraint
→ returned evidence projection
→ durable lifecycle record
```

The defect is a **distributed relation across semantic carriers**. A file-frequency or anchor-frequency compiler can find every relevant filename yet still fail to reconstruct the relation.

The correct operator therefore depends on evidence topology.

## World-model update

TM3 falsifies the broad hypothesis:

```text
exact symbols present
→ deterministic compilation should replace iterative research
```

and narrows it to:

> **Localized diagnostic topology:** when an exact diagnostic/symbol binds to a small local causal neighborhood, deterministic retrieval + bounded compilation + one semantic synthesis is strongly tractable and can dominate iterative Agent search.

For distributed representation/dataflow topology, adaptive semantic relation-following remains necessary unless a deterministic dataflow operator has independently earned the same semantics.

This is the first prospective evidence that research tractability is **operator-conditional** rather than a fixed property of the question.

## Disposition

- **Retain/localize:** compiled one-shot as a research pattern for localized exact-diagnostic questions.
- **Reject as universal:** deterministic evidence compilation for all symbolic/source questions.
- **Retain:** adaptive Agent search for distributed representation/dataflow questions where the needed relation is not locally recoverable from match frequency.
- **Do not promote:** compiler service, universal retrieval planner, or new shared Tool layer.
- **Assimilate:** update the Research Frontier Model from a list of generic taste maxims toward conditional evidence-topology → operator-policy priors.
