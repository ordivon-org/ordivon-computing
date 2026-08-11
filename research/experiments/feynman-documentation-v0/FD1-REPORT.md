# FD1 — Feynman editorial discipline closeout

FD1 asks a narrower question than “how should every Ordivon document look?”:

> Which writing and information-architecture moves repeatedly help a reader reconstruct the right responsibility, currentness, and next action, and which content should remain precise reference or research evidence instead of being rewritten as causal explanation?

## Result

The external comparison and internal exemplar audit converge on a **reader-job separation plus seven editorial disciplines**, not a universal README template.

The main contraction is:

```text
orientation / explanation  → causal, problem-first, owner/currentness explicit
action                     → goal-first, short, outcome + troubleshooting
reference                  → exact, dry, scan-friendly
research / history         → result-first, evidence-rich, outside default entry
```

The reusable candidate is `editorial-discipline-v1.json`. It remains research-only until real owner rewrites dogfood it.

## What external practice changed in our plan

1. **Do not rewrite as causal explanation everything.** Diátaxis, GitHub, and Kubernetes all make content type depend on reader need. Runtime Tool reference and exact contracts should remain reference-like.
2. **README is orientation, not encyclopedia.** GitHub's README guidance reinforces that the first surface should answer what/why/how-to-begin rather than preserve the whole research genealogy.
3. **Use-case/goal routing belongs in action docs.** Stripe's quick-start guides are a model for Finance/Runtime/Host getting-started paths, not for replacing causal system explanation.
4. **Actor clarity matters more here than in ordinary docs.** Google's active-voice rule is elevated in Ordivon because actor identity constrains proof and authority.
5. **Judgment first, derivation later.** Microsoft's scan-friendly structure guidance matches Human and Security: state the retained conclusion before its research history.
6. **Multiple reading paths are legitimate.** Rust's concept/project split supports giving “understand first” and “try first” routes rather than one compulsory sequence.
7. **Currentness is a correctness property.** Write the Docs' source/currentness principles align with FD0's owner-current/published distinction and strengthen the prohibition on duplicated current facts.

## Internal principles that survived external comparison

- compact owner-native causal prose remains the default explanation form;
- negative proof boundaries are useful when they prevent a nearby wrong action;
- problem/decision before taxonomy;
- one concrete causal journey before large inventories;
- current before target before history;
- reader-specific next paths;
- deletion/linking over duplicated detail.

## Things FD1 rejects

FD1 rejects a universal README template, a mandatory Diátaxis folder structure, a seven-question checklist in every page, conversational rewrites of exact reference, phase-code deletion for its own sake, and readability scoring based primarily on length or heading count.

## Evaluation contract

`evaluation-protocol-v1.json` preregisters the later before/after Agent preflight. It uses the 26 FD0 tasks but pairs each owner rewrite with its exact pre-rewrite parent so fact drift is not mis-scored as prose improvement. Frozen oracles are immutable; a genuinely stale task is marked not applicable and versioned separately rather than edited.

The strongest gate is per-task: an old-correct → new-wrong causal/currentness decision, or a new critical over-inference, blocks the rewrite until fixed. Equal correctness with more default-path burden does not count as an improvement.

No live Provider campaign is run in FD1. The point of this phase is to freeze the editorial and evaluation discipline **before** the first owner rewrite can influence it.

## Currentness note

FD1 revalidated all 11 owners. Finance advanced from the FD0 `be31729` snapshot to `391c11b`; the new commits close QB3b/QB4 and modify `design/QUANT-BEDROCK.md`, while the root README/authority-map gap remains. Other owner-current/publication patterns relevant to FD1 remain as recorded in `fd1-currentness-v1.json`.

## Next

The next admissible phase is the first real rewrite tranche, beginning with fresh owner inspection rather than template rollout:

1. Finance — construct the missing cognitive entry and owner-native document authority map;
2. Harness — contract the research-history overload from the default README path;
3. Security — compress the causal/constitutional model while preserving exact experiment evidence behind it.

After those three materially different cases, stop and audit the editorial discipline before rolling it across the remaining owners.
