# ACS2 — Agent Consumption Surface Gap Matrix

Status: evidence-backed working classification, not owner truth.

Observed owner revisions were revalidated on 2026-08-13 during this round. Workstation advanced to `22a0db5857ebf3e65d6ae44a996240099fa01202`; the 11 registered projects remained at the revisions recorded by the ACS0 census. Revalidate before using these hashes as currentness claims.

## Classification vocabulary

- **GOOD_SURFACE** — the current native surface was already sufficient in the tested journey; do not wrap merely for uniformity.
- **HIDDEN_CAPABILITY** — an earned owner-native capability exists but is not readily discoverable from the consumer surface.
- **PUBLICATION_CURRENTNESS_GAP** — owner-native capability exists in the live service/source, while one published consumer catalog is stale or incomplete.
- **UNDER_PACKAGED** — the right primitive exists but its semantic role is expensive to infer from names/command ecology.
- **SURFACE_INFLATION** — research/acceptance/compatibility apparatus overwhelms the stable consumption path.
- **PROJECTION_CURRENTNESS_GAP** — a useful derived projection carries stale applicability/source metadata.
- **DOMAIN_ENTRY_GAP** — a strong domain-native Agent surface exists, but a fresh Agent can miss it among lower-level domain commands/docs.
- **NEEDS_TARGETED_TEST** — evidence is insufficient to justify mutation.

## Matrix

| Owner/substrate | Current evidence | Primary classification | Earned action | Explicit non-action |
| --- | --- | --- | --- | --- |
| Runtime | Deployed MCP catalog has 22 tools including read-only `runtime.describe`; current ChatGPT Runtime connector exposes 19 and omits `runtime.describe`, `release.get`, `release.apply`. Fresh-Agent raw affordance task: 0/3 Flash + 0/1 Pro; compiled `runtime.describe`: 3/3 + 1/1. | **PUBLICATION_CURRENTNESS_GAP** | Repair publication/registration currentness so the existing owner-native description surface reaches Agents. Preserve `runtime.describe` as Runtime truth projection. | Do not create a duplicate capability registry or new Runtime architecture for facts already projected by `runtime.describe`. |
| Host | Live six-tool MCP surface. Resume journey: raw 3/3 Flash + 1/1 Pro. Compact treatment did not improve Flash and had one no-progress. `task.resume` already states Runtime/Git hints are not owner truth. | **GOOD_SURFACE** | Keep current native surface; use it as an ACS positive control and grammar source. | No universal Host facade, no wrapper merely to match other owners. |
| Harness | `ordivon-harness capabilities` already gives pre-run profile/digests/commands. Raw capability journey 3/3 Flash; one Pro raw abstention while compiled succeeded. Backend receipts already retain detailed provider usage. | **GOOD_SURFACE** for pre-run discovery; **NEEDS_TARGETED_TEST** for telemetry/operator projection | Preserve `capabilities`; separately test telemetry/inspection before changing product. | Do not infer that Harness needs a general wrapper from this campaign; do not copy a mutable plugin registry. |
| Finance | Current `design/AGENT-SURFACE.md`, `finance-context-compile`, AgentOperation/Capability/obligation semantics, `--describe`, availability/authority/effect metadata. Raw command ecology: 0/3 Flash + 0/1 Pro exact selection; compiled Agent Surface: 3/3 + 1/1. | **DOMAIN_ENTRY_GAP** with a **GOOD_INTERNAL_AGENT_SURFACE** | Make the existing Agent Surface/context compiler the canonical, easy-to-discover entry. Test one live navigation journey before any new abstraction. | No new Finance scheduler/router; no duplicate capability state. |
| Security | Existing `security_surface_manifest()` classifies constitution/profile/integration/research-apparatus, while 27+ CLI entrypoints and many acceptance/KVM commands dominate discovery. Raw taxonomy: 0/3 Flash + safe abstain Pro; manifest treatment: 2/3 Flash + 1/1 Pro. | **HIDDEN_CAPABILITY + SURFACE_INFLATION** | Expose the existing owner-native read-only surface classification through a stable discoverable public entry if targeted tests confirm. | Do not promote research apparatus to stable product surface; no experiment chronology in reusable substrate. |
| World | `ordivon-world-doctor` is a clear read-only currentness/health entry; STATUS distinguishes proof limits. Health journey raw and compiled both 3/3 Flash + 1/1 Pro. | **GOOD_SURFACE** for tested health journey | Leave doctor path alone; test other observation/connection/action journeys independently. | No wrapper earned from health task; no inference that provider success equals task/domain completion. |
| Workstation | Sophisticated `network:matrix` already exists and returns point-in-time truth role, but `agent:contract` is a large raw TOML and the command ecology is dense. Raw comparison selected narrower `network:profile-probe` or no-progress; compiled semantics selected `task network:matrix` 3/3 Flash + 1/1 Pro. | **UNDER_PACKAGED + SURFACE_DENSITY** | Derive a compact machine-readable consumption projection from existing contract/Task surfaces; make `network:matrix` semantic role discoverable without hiding explicit profile probes/effect paths. | Do not auto-select routes, enable global proxy/TUN, or replace explicit network authority. |
| Web | `pnpm agent:context` is a useful machine-readable captured-publication projection, but it does not label its own applicability/currentness role. Web's existing owner-native `compare-public-projection.mjs` re-probed the current public-document envelopes and classified Harness and Security as stale while Game remained current; this correctly demonstrates that currentness is about the admitted public-source envelope, not owner HEAD equality. | **PROJECTION_CURRENTNESS_GAP** | Surface projection truth role/applicability in `agent:context` and make the existing compare/regeneration path directly consumable. | Web must not become owner truth for source maturity/state, and HEAD inequality alone must not be treated as public-projection staleness. |
| Game | `mission-control/projection.ts` and replay projections already exemplify deep state → compact perception/action evidence. | **GOOD_PROJECTION_PATTERN + NEEDS_TARGETED_TEST** | Use as an ACS3 positive exemplar; run fresh-Agent game-state/action-selection task before mutation. | Do not force Game into Finance/Runtime object grammar. |
| Studio | Many production/media commands and project structure; no ACS fresh-Agent journey yet. | **NEEDS_TARGETED_TEST** | Test material → operation → artifact/review discovery journey. | No surface redesign from command-count aesthetics alone. |
| Human | Deliberately research/method/problem oriented, not a machine-control plane. | **NEEDS_TARGETED_TEST / NON-UNIFORM_OWNER** | Test problem/trajectory/intervention navigation without forcing executable API semantics. | Do not impose `invoke()`-style uniformity. |
| Computing | Strong Start-here/system map and mature research on capability externalization/tool contracts; research density is high but it is not a product control plane. | **GOOD_SYSTEM_NAVIGATION + RESEARCH_DENSITY** | Own ACS vocabulary, evidence, conformance research only. | No central registry/router/scheduler/truth store. |

## Cross-model result

The operation-selection campaign is intentionally not a scalar UX benchmark. The vectors matter separately.

### DeepSeek V4 Flash, 3 replicates per cell

- raw: 21 trials, 20 schema-valid, 9 exact task successes, 4 safe abstentions in intentionally missing-capability controls, 2 unsafe guesses, 1 no-progress, 30,302 total tokens.
- compiled: 21 trials, 19 schema-valid, 19 exact task successes, 0 unsafe guesses, 2 no-progress, 29,521 total tokens.

### DeepSeek V4 Pro holdout, 1 replicate per cell

- raw: 7 trials, 7 schema-valid, 2 exact task successes, 2 safe abstentions, 9,877 total tokens.
- compiled: 7 trials, 7 schema-valid, 7 exact task successes, 9,731 total tokens.

The result does **not** support adding wrappers everywhere. It supports selective semantic externalization: when the right capability exists but its role is hidden among commands/docs, a compact owner-native projection can substantially improve next-operation selection; already-good native surfaces should stay native.

## Strongest findings

1. **Runtime is the cleanest packaging/publication falsifier.** The desired capability projection already exists and is live, but one Agent consumer catalog does not publish it.
2. **Finance demonstrates a mature domain pattern.** `obligation → candidate AgentOperation refs → Capability/authority/effect contract` removes navigation burden without becoming a scheduler.
3. **Host and World are controls against wrapper inflation.** Their tested native surfaces already work; ACS should leave them alone.
4. **Security proves taxonomy matters when research apparatus is large.** The classifier already exists; the issue is addressability/discoverability.
5. **Workstation proves names alone are insufficient.** Both `network:matrix` and `network:profile-probe` exist, but the semantic distinction between broad comparison and single-tuple probing must be easy to discover.
6. **Web proves projection usefulness is not enough.** Derived context must expose applicability/currentness so stale projection cannot masquerade as owner truth.

## Failure/recovery axis

ACS0 also observed a transient connector failure reported only as `UNKNOWN / ExceptionGroup: unhandled errors in a TaskGroup`. That response did not identify whether owner truth had been reached, whether an effect was possible, retry safety, or a recovery operation. This is a separate surface axis from capability discovery. Structured parameter errors in Runtime are a positive counterexample because they expose exact schema bounds and allow immediate mechanical correction.

Therefore ACS3 must cover three independent projection needs when applicable:

1. capability/discovery,
2. state/currentness/truth role,
3. failure/recovery disposition.
