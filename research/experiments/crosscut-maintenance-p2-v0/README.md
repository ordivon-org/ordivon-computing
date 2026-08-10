# Cross-cut maintenance P2 v0

P2 asks whether the P0/P1 maintenance substrate can reduce the amount of direct owner inspection and repeated work an Agent needs, without turning the cross-cutting layer into a new authority.

The experiment has five fronts:

1. **Delivery is three independent observations, not one deployment boolean.** Source Git truth, remote publication truth, and active physical release truth can move in different orders. The projection records equality/gaps without claiming ancestry or taking release authority.
2. **Cross-Workspace compiler reuse requires stable presentation identity, not shared mutable build state.** Private Cargo target backings exposed through one stable presentation path reproduced sccache hits across fresh backings. Production promotion requires Runtime-owned per-execution namespace/bind presentation; the experiment does not promote its serial symlink simulator.
3. **Temporary equipment is a lease on intent, not another package manager.** Workstation owns a narrow lease that binds purpose, Host Task, exact pacman version and expiry. Active leases temporarily protect a forbidden package from automatic substrate cleanup; expiry/release restores the permanent policy. pacman remains installation truth.
4. **Maintenance should usually follow owner events with targeted reobservation.** Known release/publish/equipment/workspace events map to the few signals they invalidate. Unknown events do not create a generic loop, and no event authorizes a central effect.
5. **Agent-facing projection sufficiency is evaluated separately from owner truth.** A small challenge exposes only maintenance facts and allowed actions; Agent decisions are then verified against an owner-truth oracle. Passing this test means the projection was sufficient for those actions, not that the projection became authoritative.
