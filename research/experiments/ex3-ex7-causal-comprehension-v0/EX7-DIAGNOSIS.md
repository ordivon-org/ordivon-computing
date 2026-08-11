# EX7 diagnosis — final causal compression

EX7 used the untouched E surface and applied the preregistered minimum-non-inferior selection rule. Four Agent-facing representations were compared:

- compact responsibility prose;
- compact prose plus the seven-question grammar;
- compact prose plus a four-question compressed grammar;
- compact prose plus typed relation notation.

All four treatments scored **102/102 exact actions**. Across EX7 there were 408 accepted decisions, 408 physical Provider calls, zero unresolved failures, and 296,653 reported Provider tokens.

Token burden:

- compact prose: 68,677;
- typed relation notation: 73,960 (**+7.69%**);
- seven-question grammar: 76,480 (**+11.36%**);
- four-question grammar: 77,536 (**+12.90%**).

The shorter four-question checklist did not reduce total model burden; explicit checklist prompting itself remained additional context/reasoning work.

One preregistered E-surface metadata defect was known before EX7 live execution but could not be edited under the frozen contract: `run-vs-completion` has oracle `A` and also marks `A` as critical unsafe. Thus every treatment records six raw false unsafe flags. The EX7 unsafe submetric is invalid for cross-treatment selection; exact action accuracy and burden remain valid and identical in scope across all treatments.

The preregistered rule chooses the **smallest representation within one percentage point of the best exact-action accuracy** when no valid evidence establishes a safety advantage. All treatments are tied at 100%; compact prose has the lowest measured token burden. It is therefore mechanically selected.

Disposition: **SELECT COMPACT PROSE.** Typed relation notation remains research-local and optional. Seven- and four-question grammars remain on-demand diagnostic methods rather than default context. No ExplanationService, RelationGraphService, ontology server, mandatory explanation schema, or reasoning ceremony is promoted.
