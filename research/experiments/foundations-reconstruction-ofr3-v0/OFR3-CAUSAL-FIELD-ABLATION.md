# OFR3 — Causal Field Ablation

## Question

Which information must remain recoverable after theory compression if a fresh Agent is expected to understand *why* an invariant exists, predict what breaks if it is deleted, and know when to reopen a rejected alternative?

This is an **ablation result, not an OFR4 schema**.

| Semantic role | Disposition | Why |
|---|---|---|
| `claim_and_scope` | KEEP | Without the exact invariant plus owner/scope, a local product/resource law is easily mistaken for a universal rule. |
| `strongest_rival_and_attraction` | KEEP | A rejected model without its strongest rationale becomes a strawman; future Agents cannot recognize when changed conditions make it competitive again. |
| `decisive_discriminator_or_falsifier` | KEEP | Without the observation that changed the decision, an invariant is dogma rather than causal knowledge. |
| `retained_consequence` | KEEP | Theory must explain what engineering/product decision survives; otherwise it cannot guide deletion, ownership or implementation changes. |
| `counterfactual_breakage` | KEEP | Predicting what fails if the rejected model returns tests whether the reconstruction actually carries causal leverage rather than historical trivia. |
| `negative_transfer_boundary` | KEEP | A valid local falsifier can be overextended into a false prohibition. The boundary preserves option value and blocks universalization. |
| `reopen_condition` | KEEP | Rejected models are conditional negative knowledge, not constitutional taboos. Reopen conditions turn failure history into a living search boundary. |
| `exact_evidence_and_currentness_refs` | KEEP | OFR0 reproduced that current Git, historical commits, deployed state and semantic checkpoints may be distinct valid time slices. Exact references make the reconstruction auditable and prevent retrospective rewriting. |
| `verbatim_implementation_detail` | EXTERNALIZE | Exact field/class/code names are useful evidence refs but should not be mandatory semantic payload when the invariant can survive implementation change. |
| `full_experiment_apparatus` | EXTERNALIZE | Reproducibility lineage must remain retrievable, but keeping runners/fixtures active is not required for default causal reconstruction. |

## Candidate minimum semantic roles

```text
claim_and_scope
strongest_rival_and_attraction
decisive_discriminator_or_falsifier
retained_consequence
counterfactual_breakage
negative_transfer_boundary
reopen_condition
exact_evidence_and_currentness_refs
```

Two categories can normally remain outside default Context:

```text
verbatim implementation detail
full experiment apparatus
```

They remain exact and rehydratable through Git/evidence references.

## Why the rival needs its attraction

Merely naming a rejected alternative is insufficient. OFR3 repeatedly found that the rejected rival had a real advantage:

- memfd had stronger byte immutability;
- Host generic lifecycle had a cleaner common recovery story;
- automatic Memory/Skill injection reduced explicit cross-Run selection friction;
- stock/family Resource models were simpler/more familiar;
- recurrence-only promotion was cheaper;
- silent path failover increased apparent availability;
- retroactive revocation looked simpler/safer;
- spacing-only Web treatment was the smallest UI edit.

If future theory records only the winner, it trains later Agents to strawman alternatives instead of recognizing changed tradeoffs.

## Why counterfactual breakage is separate from the falsifier

A falsifier says *what defeated the rival then*. Counterfactual breakage says *what we predict would fail now if the rival were restored*.

That second role converts historical archaeology into an actionable deletion/admission test. It is what lets a future Agent answer:

> “Can I simplify this invariant today, or am I about to recreate the old failure?”

## Compression consequence

OFR4 should optimize for **causal reconstructability per token**, not minimum prose length. External evidence can be large; the default semantic representation should stay small enough to load, but must preserve the decision-changing distinctions above.
