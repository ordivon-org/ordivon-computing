# Cross-cut maintenance P3 v0

P3 tests whether the P0–P2 maintenance projection remains safe when its facts are not stationary.

The main falsifier is stale truth. A projection can be perfectly faithful when built and still become unsafe input after an owner-side release, publish, lease, lifecycle or other state transition. P3 therefore treats owner events as **invalidation hints**, not as replacement truth: a matching event after a snapshot blocks substantive action until that owner signal is reobserved.

P3 deliberately does **not** introduce a central event daemon, global TTL, writable observation database, or crosscut effect authority. Freshness bounds remain producer/owner-local. Unknown events do not invalidate unrelated facts. Missing freshness bounds do not silently count as fresh.

Evaluation emphasizes failure modes rather than average accuracy: stale-trust rate, wrong-owner rate, over-action rate, direct-crosscut-effect rate, unnecessary-reobserve rate and under-action rate. A separate legacy ablation approximates P2 behavior without freshness metadata so the value of event invalidation can be measured independently from Agent quality.
## Accepted result

- Real Workstation lease acquire/release transitions invalidated both error and healthy snapshots before their local 60-second age bound, preventing 48.407 s and 25.339 s of stale decision window respectively.
- A shuffled 32-case adversarial holdout passed 32/32 with freshness-aware projection input: wrong-owner, stale-trust, unnecessary-reobserve, direct-crosscut-effect, over-action and under-action rates were all 0.
- The same cases through a P2-style semantic projection ablation without freshness passed 19/32 (59.375%); stale-trust was 100% on cases requiring reobservation and over-action was 31.25%.
- Immutable evidence is not given a global TTL. P2 stable-build evidence remains applicable while its Runtime revision binding matches and becomes `binding_changed` if that identity changes.
- A real active Security MSI task did not prove a current `msitools` dependency: no `msitools`, `msiinfo`, `msiextract` or `libmsi` references were found in the current Security repo or its fixed research Workspace. Topic similarity therefore does not authorize lease acquisition or package removal.

The earned mechanism is a read-only temporal validity overlay: known owner events invalidate matching older snapshots, identity changes invalidate bound evidence applicability, and substantive action waits for targeted owner reobservation. It does not create a central event store, daemon, global freshness TTL, or effect authority.

