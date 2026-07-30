# ANC-ORG-002 — Causal Pluralism and Perspective-Preserving Judgment

## Question

How should an Agent-native organization represent multicausal reality, situated perspectives, factual disagreement, value conflict, and unequal evidence quality without collapsing them into one linear narrative, treating all claims as equally true, or erasing participants whose views differ from the current majority?

## Current hypothesis

A useful system separates five objects:

```text
Participant standing
Perspective and information access
Claim and scope
Causal model and prediction
Commitment and world consequence
```

Participants receive equal standing to contribute reasons, evidence, experience, and criticism. Claims receive weight according to evidence, causal adequacy, scope, predictive performance, and revision behavior. Commitments receive authority only from participants or institutions entitled to bind the affected resources and consequences.

Disagreement should be compiled into a structured comparison rather than summarized as one blended answer:

```text
shared observations
+ model-specific observations
+ competing causal graphs
+ definitions and contrast classes
+ value commitments
+ predictions and counterfactuals
+ falsifiers and revision conditions
+ unresolved conflicts
```

## Why this matters for Ordivon

Models and Agents are powerful narrative compressors. They can turn a heterogeneous evidence field into a fluent monocausal explanation and erase minority models during summarization, context compaction, delegation, or Artifact Join.

This failure affects:

- multi-Agent research synthesis;
- project and portfolio decisions;
- adversarial opponent modelling;
- evaluation and judge disagreement;
- human–Agent collaboration;
- long-running goals whose participants possess different information and consequences;
- institutional memory that may preserve conclusions while discarding the defeated evidence path.

A perspective-preserving system may improve judgment by retaining alternatives until evidence, intervention, or consequence resolves them.

## First experiment

Select one real Ordivon decision with substantial disagreement or causal ambiguity, such as project success attribution, architectural trade-offs, or whether an observed failure belongs to Host, Harness, Runtime, World, network, or operator state.

Run at least four independent analyses:

1. dispositional or component-local explanation;
2. structural and institutional explanation;
3. historical and path-dependent explanation;
4. dynamic-system explanation with feedback and interaction.

Each branch must emit:

```text
Claim set
Causal graph or equivalent model
Evidence references
Scope and contrast class
Predictions
Counterfactual intervention
Known uncertainty
Revision conditions
```

Join the branches using two methods:

- ordinary prose summarization;
- perspective-preserving structured synthesis.

Then test both syntheses against held-out evidence, participant review, and a later real outcome.

## Evidence

- minority evidence survives Join and context compaction;
- the synthesis distinguishes factual conflict from value conflict and definitional mismatch;
- independent participants recognize their strongest position in the merged representation;
- the structured model produces better predictions or interventions than the linear summary;
- confidence changes when new evidence targets a specific causal edge;
- the system can reject a claim without degrading the standing of its contributor;
- unresolved alternatives remain actionable rather than becoming permanent paralysis;
- the additional structure creates measurable decision value greater than its attention and representation cost.

## Falsifiers and deletion tests

- If causal graphs add terminology without improving prediction, intervention, or error discovery, use simpler scoped prose.
- If perspective objects merely duplicate Claims and Evidence, remove the independent type.
- If structured disagreement consistently delays reversible action without preserving useful information, narrow it to high-uncertainty or high-consequence decisions.
- If independent branches converge without information loss under ordinary Artifact Join, retain the simpler Join.
- If participant recognition cannot be measured reliably, rely on explicit claim coverage and evidence preservation instead.

## Initial implementation direction

Start as a research and evaluation convention rather than a platform-wide protocol. A candidate minimal schema is:

```text
PerspectiveRef
ClaimRef
scope
contrast_class
causal_model_ref
EvidenceRefs
value_commitments
predictions
revision_conditions
confidence_by_claim
```

Promote fields into Host, Knowledge, or organization protocols only after two materially different workloads demonstrate that their absence causes real information loss or inferior decisions.

## Related material

- [`../../knowledge/institutions/causal-pluralism-and-epistemic-equality.md`](../../knowledge/institutions/causal-pluralism-and-epistemic-equality.md)
- [`../../knowledge/institutions/plural-intelligence-organization.md`](../../knowledge/institutions/plural-intelligence-organization.md)
- [`../../studies/2026-agent-system-concept-system/04-goals-tasks-graphs-loops-and-state.md`](../../studies/2026-agent-system-concept-system/04-goals-tasks-graphs-loops-and-state.md)
- [`ANC-ORG-001-agent-native-organization.md`](ANC-ORG-001-agent-native-organization.md)
- [`ANC-SECURITY-004-opponent-modeling-and-deception.md`](ANC-SECURITY-004-opponent-modeling-and-deception.md)
