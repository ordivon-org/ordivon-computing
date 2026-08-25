# Book Result/Value Compression Falsifier v0

Status: experimental apparatus. No Book mutation is admitted by this specification.

## Question

Does one explicit compact Result/Achievement/Improvement/Value/Consumption/RealizedBenefit representation materially improve fresh-Agent judgments beyond the exact current five-chapter Book?

## Frozen arms

- `BASELINE`: exact five-chapter `book.mdx` only, followed by frozen cases.
- `TREATMENT`: exact `COMPACT-MAP.md`, then exact five-chapter `book.mdx`, then the same frozen cases.

The treatment map is deliberately placed **before** the long Book so a positive result cannot be explained solely by answer-adjacent recency.

Both arms use the same Provider/model, completion schema, budgets, prompt wording, case order and zero-Tool surface. Each run is fresh. Cases and treatment map are hashed before the first semantic run and must remain byte-identical for all accepted runs.

## Batteries

1. `classificationCases` tests strongest-justified semantic classification, including positive admissions as well as overclaim controls.
2. `transferCases` avoids Result-map labels where practical and asks what a consumer should claim/do. This is the primary decision-transfer battery.

## Primary outcome

Exact oracle accuracy by arm and case. Treatment earns correctness-motivated Book integration only if it produces a stable non-trivial improvement on cases where baseline repeatedly fails, without introducing conservative underclaim on positive-control cases.

A ceiling-level baseline is evidence **against** a correctness-motivated Book edit.

## Secondary outcomes

- false-positive overclaim count;
- false-negative / over-conservative count;
- run-reported weak cases;
- ability to reconstruct the distinction family after cases without owner sources;
- whether errors cluster in a reusable semantic boundary rather than random carrier/model noise.

## Non-claims

Agent-only results do not establish Human comprehension, retention, reading quality or pedagogical value. A treatment can fail to improve Agent correctness yet still later deserve a Human-facing representation experiment; that would be a separate claim and Task.
