# ACS9 — Agent Consumption Surface Closeout

Status: **research round complete; earned owner changes are integrated and their available distribution paths are closed; one ChatGPT Runtime connector publication refresh remains outside owner code.**

This round started from a DeepSeek Harness comparison and tested a narrower hypothesis: Ordivon often already owns the right capability/invariant, but a fresh Agent pays unnecessary mechanical cost to discover, select, interpret, or recover it.

The surviving rule is:

> **Eliminate repeated mechanical reconstruction; preserve semantic choice and owner-native truth.**

The round did **not** earn a universal Ordivon Agent API, central capability registry, global scheduler/router, mutable plugin host, or shared `AgentSurfaceManifest` protocol.

## 1. Experimental result

### Pre-implementation capability-selection campaign

The first campaign compared raw owner surfaces with compact semantic projections before product mutation.

| Model | Raw exact next-operation selection | Compiled exact next-operation selection | Raw tokens | Compiled tokens |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash, 3 replicates/cell | 9 / 21 | 19 / 21 | 30,302 | 29,521 |
| DeepSeek V4 Pro, 1 replicate/cell | 2 / 7 | 7 / 7 | 9,877 | 9,731 |

The gain did not require more total tokens. The evidence supported **selective semantic externalization**, not wrapper inflation.

### Post-implementation consumer-entry campaign

A second campaign used pre-ACS README/entry material as the ablation baseline and the actually documented post-ACS entry material as treatment. It included Host and World unchanged as positive controls.

| Model | Pre-ACS/raw exact selection | Post-ACS/current exact selection | Raw tokens | Current tokens |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash, 3 replicates/cell | 5 / 24 | 22 / 24 | 31,010 | 31,163 |
| DeepSeek V4 Pro, 1 replicate/cell | 2 / 8 | 7 / 8 | 10,414 | 10,297 |

The raw successes are almost entirely the unchanged Host/World controls. Security, Studio, Finance, Harness telemetry, Web currentness, and Workstation surface were intentionally absent from their pre-ACS entry packets.

The single V4-Pro Workstation miss was attacked with a targeted 5-replicate holdout:

- raw: **0 / 5** exact selections, 6,575 tokens;
- current `task network:surface`: **5 / 5** exact selections, 6,508 tokens.

That follow-up is sufficient to retain the Workstation projection without promoting it into a cross-owner protocol.

## 2. Post-implementation falsification

`validate_post_implementation.py` exercised the six changed owners directly from their current main working trees.

Result: **22 / 22 checks passed**.

The checks deliberately target wrong-wrapper failure modes rather than visual/API cleanliness:

- Security taxonomy remains a read-only classifier and runs no experiment.
- Studio reports Git relation while leaving semantic applicability `not-evaluated`.
- Finance exposes candidate operations but does not select a plan or scheduler result.
- Harness cache counters remain `measurement-only`; `inspect` remains the exact evidence escape hatch.
- Web reports source-envelope relation/review obligation while leaving semantic applicability and publication mutation unevaluated.
- Workstation network surface contains no automatic selection, default-route mutation, system proxy mutation, or TUN mutation.
- invalid inputs fail closed on the tested Security/Studio/Finance/Web paths;
- Harness missing-Run failure is machine-readable JSON;
- all six owner repositories remained clean after read-only validation.

## 3. Recovery falsification

Runtime was tested as a response-loss/reconnect substrate rather than by reading its implementation.

Procedure:

1. admit one `workspace.exec` with `waitMs=0`, so the initial projection is non-terminal;
2. recover the durable Job only through exact `clientRequestId` using `task.list`;
3. inspect terminal convergence through `task.get`;
4. read stdout through exact Job + Artifact identity.

Observed:

- one dispatch;
- zero duplicate dispatches;
- terminal `succeeded`;
- `deliveryDisposition=committed`;
- `recoveryRequired=false`;
- `mechanicallyConverged=true`;
- `semanticCompletionEvaluated=false`;
- exact retained stdout digest verified.

This means the native Runtime recovery surface already satisfies the relevant ACS requirement. No new recovery facade is earned.

Harness recovery/UNKNOWN semantics are covered by the telemetry tests: paused Runs use durable remaining-budget snapshots, Provider `unknown` remains unknown, and unresolved unknowns are projected rather than converted into retry permission.

## 4. Survivor matrix

| Owner/substrate | Decision | Surviving surface | Why it survives |
| --- | --- | --- | --- |
| Runtime | **no new primitive** | existing `runtime.describe` + native Job/Workspace recovery | desired affordance projection already exists; remaining issue is ChatGPT publication currentness |
| Host | **leave unchanged** | `task.resume`, `task.observe`, `task.list`, `task.adopt`, `task.checkpoint` | fresh-Agent control already strong; another facade adds no causal capability |
| Harness | **keep** | `ordivon-harness telemetry RUN_ID` | compact operator projection earned by gap analysis; exact `inspect` remains escape hatch |
| World | **leave unchanged** | `ordivon-world-doctor` | raw/current positive control already selects correctly; no wrapper earned |
| Finance | **keep / make default** | `finance-context-compile <goal-id>` defaults to current Context v15 / Agent Surface v13 | mature internal Agent surface existed but normal entry still defaulted to historical context |
| Security | **keep** | `ordivon-security-surface` | makes constitution/profile/integration/research-apparatus taxonomy addressable without running experiments |
| Studio | **keep** | `ordivon-studio production-context <production-root>` | collapses repeated mechanical manifest joins while refusing to infer semantic source staleness |
| Web | **keep** | `agent:context:currentness` + explicit captured-snapshot truth role | currentness/review obligation becomes explicit without turning Web into upstream owner truth |
| Workstation | **keep, narrow scope** | `task network:surface` | cross-model follow-up supports it; surface is observation-only and deliberately omits selector/effect operations |
| Game | **leave unchanged** | Mission Control / replay projections | already a strong internal exemplar; no additional wrapper earned |
| Human | **leave non-uniform** | research questions / methods / falsifiers / reopening gates | machine-control grammar would be category error |
| Computing | **research/conformance only** | ACS evidence and grammar | must not become central runtime/capability truth owner |

## 5. Implementation receipts

Integrated owner commits at closeout observation:

- Security: `7f257ce33b7497fb62e109da526ee81a859ad2b9` — `security: expose agent surface taxonomy`
- Studio: `e02151d7458665437a0eca66e09c5c4fc0c9c685` — `studio: expose production context projection`
- Finance: `0c9a62914531d4aeb56004c0d06eed85420a8d61` — `finance: default Agent context to current surface`
- Web feature commit: `e278ad113e58813f8f4d202ecafbe91e22c93931` — `web: expose projection currentness context`; repository-policy PR #59 passed required `check`, merged, and current Web main is `25f9207fccf66e13a72d344b0106a630f9e285bb`.
- Workstation: `30428d48f91766ae399fd6970dd3e8a50a087804` — `net: expose bounded observation surface`
- Harness feature commit `b672c41ff704660da8ff4caf734a37f0151906cf`; after incorporating concurrent upstream GitHub Actions updates, current Harness main is `49f4d4fc098864f1049333443884d3a38d11d499`.

Security, Harness, and Web are synchronized to their public remotes. Web was distributed through repository-policy-compliant PR #59 after the required `check` passed, then local main was advanced to the exact merged `origin/main` and revalidated. Studio, Finance, and Workstation have no configured Git remote, so local main is their available source authority in this environment.

## 6. Runtime publication gap

The local deployed Runtime MCP currently reports **22 tools** and catalog digest:

`sha256:72b7d5e43c14044b4b5de4aa66d8aaefaa320fab8c3a51faba71e606d1caa2bc`

including:

- `runtime.describe`
- `release.get`
- `release.apply`

The Ordivon Runtime connector published into this ChatGPT conversation exposes **19 tools** and omits exactly those three.

This is the cleanest ACS example of:

> **capability exists → owner publishes it → one consumer registration remains stale.**

No Runtime code change is justified. The remaining action is a ChatGPT connector refresh/re-registration so the consumer catalog is rebuilt from the already-live 22-tool MCP service.

## 7. Error-surface conclusion

The round observed two qualitatively different error classes:

1. **Owner-native/mechanical errors** — increasingly good. Runtime schema bounds, Studio/Finance argument failures, Web unknown currentness, Harness missing-Run JSON, Runtime response-loss recovery, and Runtime `CONCURRENCY_LIMIT` (`commitState=not_started`, `retryClass=safe_same_request`, explicit `retryAfterMs`) provide enough structure for mechanical correction/recovery.
2. **Connector transport failure** — one transient `UNKNOWN / ExceptionGroup: unhandled errors in a TaskGroup` was observed earlier. It did not expose whether owner truth was reached, effect possibility, or retry disposition. The failure did not reproduce during ACS9 and local Runtime/Host surfaces remained healthy, so no owner-code mutation is earned from it. Treat it as connector-layer evidence, not as Runtime/Host semantic failure.

## 8. What was explicitly rejected

ACS contraction removes several tempting but unsupported designs:

- no universal `AgentSurfaceManifest` protocol yet;
- no central mutable capability registry;
- no global action router or scheduler;
- no owner-independent semantic `nextActions` recommender;
- no hidden route/provider/tool auto-selection;
- no replacing exact native primitives with facade-only APIs;
- no forcing Human/Game/Studio/Finance/Runtime into one object grammar;
- no using cache locality as cognition/semantic policy;
- no treating repository HEAD inequality as public-projection semantic staleness.

## 9. Stable result

The cross-owner structure that survives is smaller than the implementation candidates:

```text
strict owner-native truth / invariant
        ↓
exact owner-native primitive
        ↓
small derived consumption projection when evidence earns it
        ↓
Agent sees capability + currentness + effect + authority + recovery distinctions
        ↓
Agent retains semantic selection
        ↓
exact native evidence remains reachable as escape hatch
```

The practical design law for future Ordivon work is therefore:

> **Internally stricter; externally simpler. Surface mechanically knowable distinctions. Do not convert convenience into new authority.**

ACS0–ACS9 can now be treated as a closed research round. Future surface changes should reuse the same per-owner loop—fresh-Agent observation → simpler/native baseline → minimum projection → cross-model falsification → recovery/wrong-wrapper tests → keep, narrow, or delete—rather than reopening a universal redesign by default.
