# Feynman Documentation v0 — FD0 freeze

FD0 freezes the pre-rewrite evidence surface. It does **not** rewrite any owner documentation and does not create a new factual authority. Owner repositories remain authoritative for their own current facts.

## Why this freeze exists

The causal-explanation programme showed that compact owner-native prose is sufficient for the tested Agent action surfaces, but it did not show that current repository entry paths are easy for a new reader to reconstruct. FD0 therefore separates four facts before editing begins:

1. the exact owner-current revision;
2. the separately observed published revision when one exists;
3. the role each important document currently plays;
4. a frozen set of counterfactual comprehension tasks that later rewrites must answer without moving authority.

The freeze intentionally distinguishes **authority role** from **reading role**. A Security experiment can be canonical for its own result without belonging in the default README path. A Game P3 target can remain a canonical accepted target without becoming the registered current product.

## Owner revision freeze

| Owner | Owner-current | Published | Selection basis | Root observation |
| --- | --- | --- | --- | --- |
| Computing | `3885544a` | `3885544a` | server_main_descends_local_main | clean root |
| Host | `19207a8f` | `19207a8f` | local_main_equals_server_main | clean root |
| Harness | `9885f3dd` | `9885f3dd` | local_main_equals_server_main_exact_commit_ignores_dirty_worktree | dirty root ignored |
| Runtime | `a62d0b9d` | `a62d0b9d` | server_main_descends_local_main | dirty root ignored |
| World | `8ddbb6a6` | `8ddbb6a6` | local_main_equals_server_main | clean root |
| Finance | `be317291` | `none` | local_main_no_git_remote | dirty root ignored |
| Security | `f109cb8c` | `f109cb8c` | local_main_equals_server_main | clean root |
| Game | `9610d166` | `1199e174` | local_clean_main_descends_published_server_main | clean root |
| Human | `8d55d310` | `e468035d` | local_clean_main_descends_published_server_main | clean root |
| Studio | `e13540d9` | `none` | local_main_no_git_remote | clean root |
| Web | `3cd84ef8` | `1cca89d3` | local_clean_main_descends_published_server_main | clean root |

Three currentness patterns were observed:

- Computing and Runtime: published server main is a descendant of the older local main, so owner-current follows the newer published commit.
- Game, Human, and Web: local clean main is a descendant of the older published server main, so owner-current and publication state are recorded separately.
- Finance and Studio: no Git remote was configured, so only local owner-current main can be frozen; no publication proof is claimed.

Harness, Runtime, and Finance had dirty root working trees during observation. FD0 never reads those dirty bytes; every document scan is bound to the exact commit recorded in `owner-freeze-v1.json`.

Runtime advanced once during FD0 (`800f3093` → `a62d0b9d`). The later commit descends from the earlier one and changed Runtime technical/operations documentation, so the freeze was refreshed before publication. FD0 is thereafter a historical pre-rewrite snapshot, not a floating latest registry; FD1 must revalidate owner currentness again.

## Document-role result

The curated map is `document-role-inventory-v1.json`. `raw-document-scan-v1.json` is omission-detection evidence only and has no classification authority.

| Owner | Pressure | FD0 diagnosis |
| --- | --- | --- |
| Computing | high | root/core are accurate but concept-dense; research entry is long and inventory-heavy; system map needs a causal journey before repository table |
| Host | medium | entry has strong boundary but remains capability-inventory heavy; architecture should surface replacement/response-loss stories before journal mechanics |
| Harness | critical | root README exposes extensive phase/research genealogy; current product boundary is obscured by closeout narrative; research-canonical documents should not all be default reading path |
| Runtime | low-medium | entry is already causal and scoped; Windows-native requirements dominate first-entry detail more than necessary |
| World | critical | correct causal laws are buried under HP/W-X genealogy; active capability and research derivation are mixed in the entry path |
| Finance | critical-structural | no root README; no document-authority map; strong owner/domain laws exist but no canonical cognitive path |
| Security | critical | current entry and architecture have grown into a research-history database; phase-coded evidence dominates first-reading attention; canonical experiment result is not the same thing as canonical entry material |
| Game | low | problem-first product document is already a strong Feynman exemplar; only light root/API contraction is needed; must preserve current v2 versus implemented-but-unregistered v3 distinction |
| Human | low | concrete problem, conditional answer and evidence limits are already clear; module numbering is already explained as non-sequential; major rewrite risk exceeds likely benefit |
| Studio | high-structural | no explicit document-authority map; root/current-state prose accumulates production phase history; source-project truth, production state and expression research need explicit reading roles |
| Web | low-medium | editorial doctrine is already strong; entry still needs a clearer why-public-projection story; browser exposure/publication must remain distinct from comprehension and owner truth |

The strongest structural findings are:

- **Finance** lacks both a root README and an explicit document-authority map. Its problem is entry construction before prose refinement.
- **Harness** and **Security** have correct owner facts but allow research-phase genealogy to dominate the default cognitive path.
- **World** has retained the right native-truth/reconciliation laws but still surfaces HP/W-X derivation too early.
- **Studio** has strong first-principles design documents but no explicit document-authority map and too much production/research phase history in current prose.
- **Game** and **Human** are already strong problem-first exemplars and should be changed conservatively.
- **Runtime** already has the closest infrastructure README to the desired causal shape; its main entry pressure is detail placement, especially Windows-native requirements.

## Frozen comprehension baseline

`comprehension-baseline-v1.json` freezes 26 open-ended tasks across all 11 owners plus cross-project boundaries. The tasks test prediction rather than terminology recall:

- physical execution versus external occurrence;
- Run completion versus Task/domain completion;
- persistence versus semantic ownership;
- capability versus authority;
- current versus target versus historical state;
- actor/sensor/evaluator evidence versus world truth;
- source change versus public consequence;
- rendered exposure versus human comprehension;
- deletion when a mature lower mechanism absorbs a responsibility.

The pre-rewrite source arm is exact-revision-bound by `owner-freeze-v1.json`. Entry-only failure is a valid result: Finance currently has no entry, and no deep document may be silently injected later to rescue that baseline.

The task set is suitable for a later Agent preflight, but it is **not** human-comprehension evidence. Human comprehension, memory, preference, confidence, and trust remain a separate experimental family.

## FD0 disposition

FD0 is complete when the freeze files validate, every curated explicit path exists at its frozen owner revision, Computing gates still pass, and the Working Set can be closed without touching owner repositories. No README or owner canonical document is modified in FD0.

Next: FD1 should extract an editorial discipline from the strongest existing exemplars and use the frozen baseline to constrain, not dictate, later rewrites.

## FD1 closeout

FD1 is closed in [`FD1-REPORT.md`](FD1-REPORT.md). The external comparison and internal exemplar audit reject a universal Feynman template and retain a smaller rule: choose the reader job first, then apply causal explanation pressure only where understanding/orientation is the job. Exact reference may remain dry and structured; research/history remains evidence-rich but outside the default entry path.

[`editorial-discipline-v1.json`](editorial-discipline-v1.json) is a research-only seven-discipline candidate, not a product schema. [`evaluation-protocol-v1.json`](evaluation-protocol-v1.json) freezes the paired before/after Agent preflight rules before any owner README is rewritten. Human comprehension remains untested.

## FD2–FD3 first rewrite tranche

Finance, Harness, and Security have completed the first real rewrite dogfood. Harness and Security are published; Finance has an exact tested/evaluated candidate but its `main` update is intentionally fenced by a concurrent uncommitted owner contraction. See [`FD2-FD3-FIRST-TRANCHE.md`](FD2-FD3-FIRST-TRANCHE.md) and [`editorial-discipline-v2.json`](editorial-discipline-v2.json).

The seven FD1 disciplines survive without an eighth rule. Currentness-before-publication, linked-authority currentness, and paired-oracle invariance are now stricter.

## FD4 second rewrite wave

World and Host are published with causal entry rewrites; Runtime required an experiment-driven second contraction and remains publication-fenced behind active owner mutation; Computing has a contracted candidate awaiting final conformance/CAS publication. The primary 48-trial preflight plus 12-trial Runtime follow-up found no causal regression. See [`FD4-SECOND-WAVE-CLOSEOUT.md`](FD4-SECOND-WAVE-CLOSEOUT.md) and [`editorial-discipline-v3.json`](editorial-discipline-v3.json).

The seven-discipline method still survives without an eighth rule. FD4 adds two practical refinements: preserve owner-native stable navigation anchors when they are part of the owner's public contract, and force a second contraction when a ceiling-correct rewrite materially increases reader burden without decision gain.

## FD5–FD6 third wave

Game and Human passed explicit no-change controls and were not rewritten. Studio contracted its root around revision-bound expression and added a document/fact authority map; Web contracted its root around public consequence and encounter-versus-comprehension, then published through its protected-main PR/check path. Across 36 reader trials and 36 judges there were no causal/authority regressions. See [`FD5-FD6-THIRD-WAVE-CLOSEOUT.md`](FD5-FD6-THIRD-WAVE-CLOSEOUT.md) and [`editorial-discipline-v4.json`](editorial-discipline-v4.json).

The seven disciplines still survive without an eighth rule. The main new refinement is that **no-change is a valid experimental treatment** when an existing owner entry already satisfies the frozen reader consequence and has no observed structural authority gap.
