# Resource Utilization — RU0–RU10

## Objective

Ordivon is no longer primarily resource-poor. The dominant problem is conversion:

```text
Reality
→ Resource
→ Actionable Resource
→ Option
→ Capability
→ Effect
→ Evidence
→ Knowledge
→ better acquisition / composition / retirement
```

This RU series audits that conversion without creating a global Resource Registry, Capability Manager, universal scheduler, or scalar resource-value score. World remains the canonical owner of the Resource→Option→Capability doctrine; Computing owns this bounded cross-owner utilization study.

## Admission rule

A resource receives stronger utilization credit only when current owner-native evidence shows that it changes a real downstream workload. `resource exists`, `reachable`, `installed`, `configured`, and `available capability` are all weaker claims than `expanded useful work`.

Every RU card must therefore name:

- native owner and currentness boundary;
- current conversion stage;
- real or candidate consumer;
- deletion consequence;
- conversion bottleneck;
- important complements;
- revalidation condition;
- evidence that consumption compounds into knowledge or future resources.

## RU0 — Complete Resource Census

Freeze only a bounded observation snapshot of currently possessed or already-qualified resources. Do not create an ambient inventory service. The census is useful only as evidence for the current audit and must be refreshed from owners when currentness matters.

## RU1 — Compute Utilization

Current live evidence from the WSL execution world:

- WSL exposes 8 logical CPUs on AMD Ryzen 9 8940HX;
- WSL memory is about 7.76 GiB with 6 GiB swap;
- the WSL root block device is about 1.08 TB, with about 795 GB available at observation time;
- RTX 5060 Laptop GPU is directly visible to WSL, 8151 MiB VRAM, and was at 0% GPU utilization at observation time;
- Node, Python, uv, Go, Rust/Cargo, pnpm and Git are directly executable in the WSL world.

The first live `windows_native` attempt exposed a provider/Core version mismatch: an installed `windows_native_launcher_v2` emitted `providerContract` while current Runtime main had intentionally contracted that field and rejected it under `deny_unknown_fields`. The current-main launcher independently passed the full Windows launcher acceptance suite, so the stale deployed provider was replaced by a content-addressed binary compiled from current main and Runtime was restarted. A subsequent real `windows_native` Job succeeded with Windows-start evidence and re-observed Bellator N176, Ryzen 9 8940HX, 16 physical cores / 32 logical processors and 16,412,348,416 bytes physical RAM. The Windows Reality→Actionable Resource bridge is therefore restored; the durable lesson is that provider/Core release alignment is part of resource actionability.

Do not simply maximize WSL CPUs. RAM remains a likely complement/binding constraint: more parallel CPU work can reduce capability when memory pressure, thermal pressure, browser/Docker contention, or interactive latency dominates.

## RU2 — Network & Provider Utilization

Current Finance/Workstation dogfood proves why path count is not capability.

The Finance executor remains healthy, disabled, and bound to exact `finance-okx` authority/profile identity. After the WSL interruption, the pool initially projected `UNKNOWN`, `listenerReachable=false`, `watchdogDisposition=no-eligible-member`. Fresh Surfpath discovery found one currently qualified JP/Tokyo WireGuard path on `native-b`; the stale `surf-okx-b-r3` generation was explicitly stopped, re-admitted from that exact fresh observation/path, republished as `finance-okx-b`, and the stable `finance-okx` pool was republished. It returned to `AVAILABLE` on the same authority digest with `finance-okx-b` as the single eligible member. Finance executor current-egress binding then matched again, and an authenticated fixed-GET account observation succeeded with zero write-like tools exposed. The former Singapore/OpenVPN member did not requalify in the fresh discovery and remains absent, so pool availability is restored but two-member redundancy is not yet restored.

Workstation observation also returned HTTP 401 during the earlier pass, exposing a separate Agent→Workstation authority/interface problem. Keep these failure classes distinct:

```text
candidate/path universe
!= current eligible member
!= listener currentness
!= Agent observation authority
!= Finance semantic capability
```

No new nodes should be acquired merely to increase cardinality. First restore one exact current eligible member and observation path, then let real failures decide whether additional independent options are valuable.

## RU3 — Tool & Equipment Utilization

Blender, REAPER, OBS, Resolve, Figma and other professional tools are valuable only when ordinary Studio/Game/Web/etc. production consumes them. Prior E8 dogfood already established real native state/action surfaces for Blender, REAPER and OBS. RU therefore treats the next bottleneck as ordinary workload consumption, not tool discovery.

Figma remains an example of an authority gap where installed software plus configured integration does not equal an actionable native design capability until required consent/authority is current.

Do not create a generic Equipment Manager.

## RU4 — Information Resource Utilization

OpenAlex, Crossref, SEC EDGAR, OSV, CISA KEV, NVD and other already-observed structured sources should graduate only by changing real research, hypothesis formation, falsification, or decisions. Provider discovery alone is R1/R2 evidence.

The next useful experiment is ordinary consumer substitution: compare a real research workload that relies on ad-hoc web search against one that consumes the relevant structured corpus, with owner-native outcome criteria such as source coverage, reproducibility, false-positive reduction, changed hypothesis, or reduced acquisition friction.

## RU5 — Model Intelligence Utilization

Treat models as heterogeneous intelligence resources with different cost, latency, context, Tool access, reliability and failure modes. Do not create a static global model ranking. Specialization should be workload-derived:

- generator;
- critic/reviewer;
- falsifier;
- coding executor;
- cheap observer;
- high-context synthesizer.

A specialization earns retention only if it improves a later independent workload relative to a strong baseline. Multi-model cardinality alone is not Capability.

## RU6 — Knowledge Capital Utilization

Host history, repository history, failed experiments, falsifiers, tests and closeouts are already-paid search trajectories. Current Host integrity observation after recovery reports 224 Tasks, 1120 Events and 2221 validated objects.

That history should not become a Host-owned intelligence engine. Computing may consume it on demand for concrete problems such as duplicated work, repeated friction, abandoned hypotheses, failure mining, or portfolio analysis. Historical evidence remains historical and does not establish current owner state.

## RU7 — Economic Resource Utilization

Finance currently possesses a substantial capital-decision/execution substrate even though the current scoped egress is not healthy enough for authenticated venue work. Infrastructure capability and capital amount remain distinct.

GVA is the larger unexploited external-effect frontier: software bounties, authorized security rewards, competitions, forecasting, prizes and other value-acquisition worlds. Existing discovery/research infrastructure earns economic Capability credit only when it produces a real external value effect under the relevant authority and terms.

No financial write is required by RU.

## RU8 — Human Scarce-Resource Allocation

Human attention, judgment, long-timescale integration, goal/value authority, legal/social identity and real-world consequence ownership are scarce participant resources. Routine log inspection, repeated command execution, exhaustive diff reading and implementation-detail synchronization should normally be delegated when Agent/runtime evidence can preserve the needed control.

Human attention should concentrate on purpose, boundary changes, high-consequence anomaly, unresolved normative choice, and information that materially changes long-horizon world models. This is a participant-allocation rule, not an automatic Human scheduler.

## RU9 — Complementarity & Bottleneck Map

The most important current complementarity candidates are:

1. **RAM × CPU/GPU/browser/Docker concurrency** — more memory can unlock already-owned compute capacity; pure CPU expansion can be counterproductive if memory remains binding.
2. **Runtime Windows bridge × Windows CPU/tools/equipment** — one contract bridge determines whether a large native resource world is actionable by Agents.
3. **Workstation current member × Finance executor/venue authority** — executor health alone cannot create venue capability when scoped egress currentness fails.
4. **Structured data × model/Harness research loop** — data access becomes more valuable when cognition can query, compare and falsify cheaply; model capability becomes more valuable when evidence is structured and reproducible.
5. **Host history × selective retrieval/Computing analysis** — retained search trajectory compounds only when a real future problem can cheaply retrieve the relevant evidence.

Do not assign one universal complementarity score. A complement is real when removing or restoring it changes a downstream capability under a named workload.

## RU10 — Resource Compounding Flywheel

The strategic operating loop is now:

```text
Observe resource
→ establish owner truth/current access
→ qualify one demand-scoped option
→ compose with complements
→ consume in ordinary work
→ observe attributable Effect
→ preserve positive and negative Evidence
→ update Knowledge
→ prefer / retire / reacquire / expand
```

The acquisition objective changes accordingly:

```text
maximize marginal useful Capability / Optionality / Information
subject to authority, maintenance, coordination, risk and attention cost
```

not:

```text
maximize resource count
maximize utilization percentage
maximize installed tools
maximize provider/node count
```

## Current intervention order

### Closed P0 — Windows conversion bridge

The stale v2 provider/current-Core mismatch was reproduced and repaired by realigning the deployed content-addressed launcher to current Runtime main. A real `windows_native` host probe succeeded afterward. Reopen only if provider/Core release ownership drifts again or a new Windows workload fails at this boundary.

### Closed P0 / residual redundancy gap — `finance-okx`

Workstation MCP observation recovered after the WSL restart. One exact JP WireGuard member was freshly rediscovered/re-admitted and the stable pool returned to `AVAILABLE`; Finance read-only authenticated observation succeeded through the unchanged authority digest. The residual gap is redundancy, not present availability: `finance-okx-a` is still absent because the fresh Singapore/OpenVPN candidates failed qualification. Do not manufacture a replacement merely for cardinality; rediscover/re-admit another member when a currently qualified path exists or a real failure makes the additional option valuable.

### P1 — Consume structured information in ordinary research

Use OpenAlex/Crossref/EDGAR/etc. on real Computing/Finance/Security research questions and measure whether they change coverage, falsification, latency or decision quality.

### P1 — Consume GPU/professional tools in ordinary workloads

Let Studio/Game/Security/Computing workloads naturally demand GPU/Blender/REAPER/OBS capability. Do not manufacture benchmark workloads solely to raise utilization.

### P2 — Mine Host knowledge only on real retrieval pressure

When a concrete duplicated-work/repeated-friction/abandoned-hypothesis problem occurs, compare direct full-history/manual search with a bounded Computing retrieval method. Promote nothing if the historical corpus does not change a decision.

## Deletion tests

The RU method should itself be deleted or contracted if any of the following becomes true:

- ordinary owner work already exposes the same conversion evidence with less overhead;
- the cards become stale inventory rather than decision-changing evidence;
- resource utilization scoring starts rewarding activity/cardinality instead of downstream effects;
- the audit duplicates F14 option-retention field-study authority or contaminates its future oracle;
- a central service begins owning resource truth that native owners can already establish.

The desired output of RU is therefore not a permanent catalog. It is a smaller set of repaired bridges, proven consumers, retired dead resources and better acquisition decisions.
