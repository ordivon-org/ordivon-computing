# Cross-cut maintenance P4 v0

P4 attacks the temporal-validity assumptions retained after P3. The target is not more freshness machinery; it is the boundary between detectable staleness and staleness no projection can know about.

P4 tests five pressures:

1. real non-Workstation owner changes, especially the Runtime release from `053adf74...` to `8aa036b8...`;
2. sparse event delivery: absent, delayed, duplicated, conflicting and out-of-order hints;
3. false-positive invalidation from P3's key-only matching across different owners;
4. event results that prove `no_change`, which must not invalidate merely because an operation ran;
5. a second materially different temporal consumer in World.

The candidate refinement is deliberately narrow. Invalidation identity becomes owner-scoped `(owner, key)`. Event occurrence and event availability are separate coordinates. Exact event replay is deduplicated by stable event identity; conflicting reuse of one event identity fails closed. `no_change` results do not invalidate. Events still only accelerate invalidation: absence of a visible event never proves that owner state has not changed, so owner-local freshness/revalidation remains necessary.

World is used as an independent consumer/falsifier rather than as a dependency. Its existing foreign-egress/effect-path contracts already distinguish historical evidence, owner freshness windows, unknown validity horizons and action-time owner revalidation. P4 may assimilate shared laws from that evidence, but no shared temporal package is promoted unless exact implementation reuse is independently earned.

## Accepted result

- A real Computing no-op publish (`Everything up-to-date`) against six fresh live signals reproduced P3 key-only over-invalidation: four source-delivery signals would be reobserved. P4 owner-scoped `(owner, key)` matching plus `changeDisposition=no_change` requires zero reobservations.
- Holding the same publish event shape but counterfactually marking Computing as changed isolates owner scope: P3 invalidates all four source-delivery owners, three falsely; P4 invalidates only Computing, with zero cross-owner false positives.
- Real source+remote reobservation cost is material in the current environment. Median observations were about 6.49 s Computing, 4.87 s Runtime, 6.26 s World and 3.34 s Host. P3 key-only no-op handling would spend about 20.96 s; P4 spends 0. A genuinely changed Computing publish avoids about 14.47 s of unrelated owner reobservation.
- Sparse-event falsification proves event hints are acceleration, not completeness. With a 60 s owner bound and an actual owner change 11 s after observation, no hint leaves 49 s of stale exposure, a delayed hint leaves 13 s, and an immediate hint leaves 1 ms. No event never proves no owner change; no event plus no owner bound is not actionable.
- Event occurrence and event availability are separate coordinates. An event cannot invalidate before it becomes available to the projection. Exact replay is deduplicated by stable event identity; conflicting semantic reuse fails closed; an old delayed event cannot invalidate a newer owner observation.
- The real Runtime release from `053adf74...` to `8aa036b8...` is a non-Workstation owner event and correctly invalidates the historical Runtime delivery snapshot. That old snapshot was already beyond its owner-local age bound, so this particular event adds no extra stale-window reduction; the two mechanisms remain complementary.
- The same Runtime revision advance turns the P2 stable-build evidence from `immutable_bound` into `binding_changed`. The historical experiment remains true but cannot be promoted to the new Runtime without owner revalidation.
- World is a materially different second temporal consumer. Its owner-native frozen Python 3.12 environment passed 22 focused tests covering reference expiry, reobservation, historical-vs-current evidence, effect-time owner freshness and separate provider/World availability coordinates. World independently supports the semantic temporal laws while using different domain mechanisms.
- Two consumers therefore earn shared **semantic temporal-validity laws**, not a shared implementation. No cross-project temporal package, event broker, global TTL or global time ontology is promoted by P4.
