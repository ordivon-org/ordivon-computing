# Comparative Capability Ecology — P0 Operationalization

Status: active current gap register, 2026-08-12

This register operationalizes EG0–EG8 without creating a universal capability router, verifier service, sensor daemon, statistics platform, simulator service, or Archivist layer. The unit of work remains a real owner pressure.

## P0-A — Observation / Resource Acquisition

Current evidence: [`../evidence/observations/capability-ecology-p0a-20260812.json`](../evidence/observations/capability-ecology-p0a-20260812.json).

### What is already true

- Direct WSL egress currently resolves to China Mobile `AS9808` / CN.
- Read-only `www.okx.com` public probes time out before Finance can observe a fresh venue world.
- The two current Workstation native proxy users still exit through the same public IP/ASN and do not bypass the OKX path failure.
- Windows has both WLAN and a Remote NDIS interface up, but both currently use `192.168.0.1` and the same observed upstream; this is not evidence of physical/carrier independence.
- Surfshark authority already exists locally: 142 logical nodes / 415 WireGuard/OpenVPN variants. The Windows Surfshark service is running, but its OpenVPN data-channel adapter is currently disconnected.
- Bounded WSL-side manual Surfshark discovery did not yield a fresh qualified path during this round. The transient workers created by those attempts were explicitly stopped.
- Workstation's latest capability universe still reports full coverage of all currently achievable slots, while `ownership.independent-carrier`, `ownership.self-owned-external-root`, active authorized measurement, and authorized relay remain externally blocked.

### Current priority

The next observation budget is not another search loop. It is to obtain one genuinely different observation path and immediately re-run the exact blocked read-only workload.

For Finance, the cheapest next falsifier is a **temporary user-controlled Windows VPN connection** using existing Surfshark authority, followed by automated WSL read-only OKX probes. This tests whether the blocker is path-specific without buying infrastructure or changing Finance authority.

For Workstation root independence, a VPN is insufficient. The stronger claim requires a different physical/carrier upstream or self-owned external root. That is a separate later resource decision and must not be inferred from VPN geography/provider diversity.

## P0-B — Verifier Ecology

EG1 established the role, but current owner code decides whether new machinery is justified.

Finance current verification was re-audited at `fe672dea79b43c0c244d80e2ccb9e53ea58b2a73`:

- 26 focused Python Venue World / F6 boundary tests passed;
- 31 focused Node C2 admission/world/dispatch tests passed;
- these tests cover exact signed authority/effect separation, world-bound commit semantics, stale/historical request rejection, package tamper rejection, replay idempotency, once-only dispatch permission, ambiguous-dispatch no-second-POST behavior, revocation, and physically immutable remote ledgers.

A broader Python execution-binding import was not evaluated in the minimal Runtime environment because `duckdb` is not installed there; this is an environment/toolchain boundary, not a failed Finance invariant.

**Disposition:** do not add Z3/SMT or a new Finance verifier layer now. Continue to use exact enumeration/property/formal techniques where a specific owner boundary demonstrates omission risk beyond the existing strong tests. The current live-capital blocker is reality access, not verification density.

## P0-C — Estimator Ecology

P0-C has an immediate owner-native landing in FS0.

The frozen FS0 prediction receipt is unchanged. New current evidence [`../experiments/fs0-shadow-portfolio/statistical-calibration-v1.json`](../experiments/fs0-shadow-portfolio/statistical-calibration-v1.json) adds 95% Wilson calibration:

- raw `5/5` top-choice agreement: `[0.566, 1.000]`;
- RFM `4/5`: `[0.376, 0.964]`;
- negative-control top choice `0/10`: upper bound `0.278`;
- negative-control deferral `10/10`: lower bound `0.722`.

The intervals prevent point-rate overclaim while preserving the frozen prospective experiment. They do not scalarize research value or identify selection regret.

**Disposition:** estimator/calibration is now active method equipment. Add it only where an active experiment makes a stochastic or population-like claim; deterministic evidence does not need statistical decoration.

## User-action boundary

The system should not ask the user to perform work that an Agent or existing machine authority can do. As of this observation:

### No user action required

- P0-B verifier work;
- P0-C estimator work;
- additional code/test/research integration;
- buying a solver/statistics tool;
- providing API keys or secrets in chat;
- buying a VPS merely to continue this round;
- recruiting human evaluators before a real human-consequence claim needs them.

### One optional high-leverage action to unblock current P0-A/Finance observation

When convenient, connect the existing **Windows Surfshark app** to a working non-CN exit and leave it connected for one verification pass. No credential should be pasted into ChatGPT or source. After the route is active, Ordivon can re-observe WSL public egress and run read-only OKX public/private permission probes under existing Finance authority.

This action tests only path reachability. It does **not** establish independent-carrier ownership.

### Later, only if independent-carrier evidence becomes worth the cost

Expose a truly different physical WAN/carrier to the machine (for example a distinct cellular/hotspot/upstream) or acquire a self-owned external root. Do this only when the value of that failure-domain independence exceeds its operational cost. It is not required for P0-B/P0-C and should not block the rest of the capability-ecology work.

## Stop / reopen rules

- Stop adding verifier machinery when existing owner checks already cover the relevant exact invariants and no mutation/falsifier survives.
- Stop adding estimators when the evidence is deterministic or sample structure cannot support the claim.
- Stop searching for more public resources when the remaining capability slot explicitly requires user authority, a physical resource, an authorized peer, or a purchase.
- Reopen a shared contract only after the same minimal invariant independently appears in at least two owner domains and local implementations create measurable duplication or drift.
