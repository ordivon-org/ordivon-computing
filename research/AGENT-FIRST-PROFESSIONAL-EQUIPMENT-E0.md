# Agent-first Professional Equipment E0 — Non-Studio Round

Date: 2026-08-13

## Question

After excluding the Studio M/E-series media equipment program and tools already present on the workstation, which professional tools materially improve Game, Web, Security, Finance, or cross-cutting Agent work?

The acceptance rule is deliberately stricter than software popularity:

> A tool earns retention only when a real Ordivon workload shows either a capability gap without it, or a material reduction in observation/verification/recovery friction that cannot already be obtained from the current substrate at comparable cost.

Professional tools remain **equipment**, not semantic authorities. Game/Web/Security/Finance continue to own domain meaning; Workstation owns machine equipment availability; Runtime owns exact physical execution and retained artifacts; Harness owns Agent-run cognition/tool interaction.

## Frozen starting revisions

The round revalidated current local repository heads before opening clean Runtime workspaces:

| owner | revision |
| --- | --- |
| Game | `db5852dc54460435793b6cd5f277421e01d061f3` |
| Web | `25f9207fccf66e13a72d344b0106a630f9e285bb` |
| Security | `7f257ce33b7497fb62e109da526ee81a859ad2b9` |
| Finance | `0c9a62914531d4aeb56004c0d06eed85420a8d61` |
| Computing | `2be6e8fad24f53e981f7e73e567a95fcecd31988` |
| Workstation | `30428d48f91766ae399fd6970dd3e8a50a087804` |

Studio media equipment is intentionally outside this round.

## Existing substrate first

The machine already provided a strong baseline rather than an empty toolbox:

- structure/search: `rg`, `fd`, `jq`, `yq`, `fzf`, `ast-grep` 0.44.1;
- execution/performance: `hyperfine`, `strace`, GDB;
- data: SQLite, DuckDB, PostgreSQL client;
- supply-chain/security: Trivy, Syft, Cosign, OSV-Scanner, Gitleaks, ShellCheck, Actionlint;
- packet capture: `tcpdump`;
- isolation: QEMU 11.0.3 and `swtpm`;
- media substrate: FFmpeg/FFprobe.

The round therefore did not admit replacements for these capabilities merely because another product has broader branding.

## E0-G — Game: mutation pressure earned, Stryker did not yet

### Baseline

A clean Game workspace bootstrapped from the frozen revision and passed the complete native gate:

- TypeScript typecheck;
- browser-source syntax check;
- **258/258 tests**;
- existing `fast-check` state/property tests.

### Mutation ablation

Three source-level mutants were injected into a disposable copy while keeping the existing focused tests unchanged:

| mutant | baseline result |
| --- | --- |
| exact spare-parts boundary `< -> <=` | killed |
| exact battery/power boundary `< -> <=` | **survived** |
| world revision increment `+1 -> +2` | killed |

The surviving battery mutant was a real blind spot: the suite tested insufficient battery and conservation, but did not directly establish that `batteryCharge == powerDraw` remains admissible.

Game now contains an explicit exact-boundary regression. Reinjecting the mutant fails that test, and the final complete Game gate remains **258/258 passing**.

### Disposition

**Retain targeted mutation testing as an experiment instrument.** It demonstrated incremental falsification value over a large property/unit suite.

**Do not add StrykerJS to default dependencies or CI yet.** The first `pnpm dlx` acquisition was blocked by current npm transport/DNS failures, while manual disposable mutants already proved the method. A mutation engine earns permanent integration only when repeated campaigns show automation benefit large enough to justify acquisition/runtime cost.

## E0-W — Web: current browser apparatus remains sufficient

### Baseline

Web already owns:

- Playwright;
- Axe;
- browser-review trajectories;
- static-budget reporting;
- design/publication validation;
- Chromium rendering.

The native `pnpm check` reached and passed build, lint, design/publication, static-budget, and began the existing browser suite without a product failure before the outer Runtime deadline. No source changes were made by this round.

### Firefox/WebKit treatment

Playwright browser provisioning was attempted into the existing shared browser cache. Firefox/WebKit acquisition stalled on external browser-download supply and was cancelled rather than turning a browser cache download into a long-lived background mutation.

The result does **not** claim that cross-browser testing lacks value. It establishes only that multiplying the current suite has not yet earned its local supply/runtime cost.

### Lighthouse treatment

The current machine has no Lighthouse installation. npm registry access was unavailable during the round, while the existing Web gate already covers accessibility, deterministic browser encounter, and static resource budgets. No incremental Lighthouse finding was produced.

### Disposition

- Chromium + Playwright + Axe + current budget gate: **retain**.
- Firefox/WebKit: **defer until a compatibility claim or failure requires them**.
- Lighthouse/LHCI: **defer until a concrete performance/SEO diagnosis exceeds the existing budget/review surface**.
- Storybook/Chromatic: remain **deferred by Web's existing evidence-backed policy**.

## E0-S — Security: independent observation equipment materially helps

Security's native baseline passed **367 tests with 4 skips**. Existing Ruff findings are historical source-style debt and were not counted as equipment discoveries.

### TShark — retain

The machine already had `tcpdump`, so the candidate question was not whether packets could be captured. It was whether immutable packet bytes could be projected into protocol facts without asking an Agent to parse human-oriented capture output.

A deterministic HTTP request was encoded into a 512-byte PCAPNG and decoded by TShark 4.7.2. The structured fields were:

```text
GET|agent.local:18110|/probe
```

A JSON projection also exposed separate frame/Ethernet/IP/TCP/HTTP layers.

A later signed isolated-toolroot replay produced:

```text
GET|signed-toolroot.local:18110|/probe
```

**Retain TShark as on-demand decode equipment.** Capture authority remains separate; a PCAP is evidence bytes, and TShark's decode is an observation/projection rather than independent world truth.

### Nmap — retain narrowly

Nmap 7.99 was tested only against loopback/local fixtures. A bounded TCP-connect scan with explicit timeout and zero retries correctly observed two deliberately open local HTTP ports and emitted XML suitable for deterministic parsing.

An earlier less-constrained scan encountered a WSL kernel/network wait. This is a reason to narrow the profile, not to convert Nmap into a daemon or broad scanner.

**Retain Nmap only as bounded, explicit, on-demand independent surface observation** for owned/authorized ranges. Require explicit target scope and mechanical deadlines. It does not become Security topology truth.

### mitmproxy — conditional retain

A local-only HTTP origin was accessed through mitmproxy 12.2.3. The proxy retained a flow file and a later independent read reproduced the exact request and `HTTP/1.0 200 OK` response. The clean replay passed.

The same treatment was then repeated from a **signed Workstation isolated root**: 49 verified packages, `manifestIntegrity=true`, `environmentValid=true`, about 92 MiB on disk. The exact root again recorded and replayed the local HTTP flow successfully.

This establishes distinct value from TShark/Nmap: application-layer flow record/replay and programmable transport perturbation are useful for response-loss/delay/duplication experiments.

**Retain as conditional experiment equipment, not a default dependency.** Its 49-package Python closure is materially larger than Nmap/TShark, so it should be materialized only for a specific authorized fault experiment. Do not place real Finance trade credentials through it by default.

### Semgrep — defer

Semgrep acquisition through the Python package path failed under current PyPI connectivity. More importantly, the current substrate already has `ast-grep`, Ruff, Trivy, OSV-Scanner, Syft, Cosign, Gitleaks and language-native tests. This round produced no incremental Semgrep finding.

**Defer Semgrep** until a real SAST finding class survives the existing stack or a rule-pack experiment demonstrates a meaningful coverage delta.

## E0-F — Finance: property generation helps; another quant platform does not

Finance remains deliberately small at its computational core: pinned Python 3.12 plus DuckDB/Polars, with SQLite/Parquet/evidence/research-validity and venue-specific execution/reconciliation around it.

### Hypothesis treatment

The current PyPI path could not provision Hypothesis into the pinned Python 3.12 environment. Arch's package is built for the system Python 3.14, so the experiment did **not** weaken Finance's runtime contract just to satisfy the tool trial.

Instead, pure Finance normalizers that do not depend on the project DuckDB/Polars ABI were exercised under an isolated system-Python tool environment:

- `normalize_fill`: **250 generated examples** over quantity, price, contract value and trade identity;
- invalid timestamp fallback: **80 generated examples**.

All 330 generated cases passed their declared invariants.

### Disposition

**Retain property-based generation as a high-value falsifier method**, especially for parsers, normalization, ledger conservation, stale-evidence rejection and effect-admission boundaries.

**Do not add Hypothesis to Finance production dependencies yet.** It should enter the pinned project environment only through the normal `uv` authority once Python 3.12 resolution is reliable. Tool usefulness does not authorize runtime-environment drift.

### Marimo and quant platforms

No current Marimo installation or Arch package exists on this node, and no concrete Finance task required notebook-reactivity beyond deterministic scripts + DuckDB/Polars + retained evidence.

**Defer Marimo.** Likewise do not add Qlib, Backtrader, Zipline, vectorbt, MLflow, W&B, ClickHouse or another database/platform merely to enlarge the toolbox. None earned a missing responsibility in this round.

## E0-X — Cross-cutting discovery: isolated signed toolroots

The most important cross-cutting result was not one of the original named tools.

During the round, the global pacman database was legitimately occupied by an unrelated Studio package transaction. Nmap, TShark and Hypothesis experiments still needed temporary professional equipment. Repeated ad-hoc work converged on the same useful mechanism:

```text
pacman read-only closure resolution
        ↓
package archive + detached signature
        ↓
pacman-key verification
        ↓
isolated extraction
        ↓
exact toolroot / absolute executable
        ↓
explicit removal / expiry
```

This is materially different from installing another package globally:

- no pacman database mutation;
- no ambient PATH mutation;
- no competition for the package-manager write lock;
- exact package closure and versions are retained;
- archive and signature SHA-256 values are retained;
- every package must pass the existing Arch/pacman trust authority;
- the result is bound to one Host Task, purpose and expiry;
- Runtime can execute the exact resulting path.

Workstation now has a candidate `isolated-equipment` utility implementing exactly this narrow responsibility. It deliberately does **not** become a package manager or semantic equipment registry.

### Dogfood defects found before promotion

The first signed Nmap materialization exposed a publication bug: the manifest projected staging-directory `binDirs/libraryDirs`, which became stale after atomic rename. A regression was added, the projection was changed to verify bytes in staging while publishing final-root paths, the bad materialization was explicitly removed, and the same identity was rematerialized.

Status was then hardened further: manifest digest + root existence is insufficient. An equipment root is active only when every declared bin/library/Python-site directory exists and resolves beneath the final published root. An outside/stale locator fails closed as `invalid`.

The first `/root/tools/bin` deployment found a second packaging defect: the script's default contract locator was derived from `__file__`, so relocation from the repository into the managed tool directory changed the default from `/root/workstation-lab/workstation.toml` to the nonexistent `/root/tools/workstation.toml`. The deployed surface was therefore unusable without caller folklore. The default contract is now canonical and deployment-location independent.

The same usability pass added compact `list` and conservative `gc` operations. `list` exposes bounded equipment identity/state/purpose/package-count/environment facts instead of entire package manifests. `gc` removes only recognized roots whose signed/integrity-valid state is genuinely expired; invalid or unrecognized roots are retained for explicit operator/Agent judgment rather than silently deleted.

### Live acceptance

Signed `security-nmap-e0`, `security-tshark-e0`, and `security-mitmproxy-e0` roots were created under the Workstation isolated-equipment state root. They currently project respectively 2-, 5-, and 49-package signed closures and all report:

- `manifestIntegrity=true`;
- `environmentValid=true`;
- final, non-staging paths;
- exact signed package closure.

Nmap replay returns `admission=existing` without reinstalling or mutating global state. Ambient `command -v nmap/tshark` and `pacman -Q nmap/wireshark-cli` remain absent while exact toolroot executables work. The managed `/root/tools/bin/isolated-equipment` bytes are identical to the current Workstation source and can invoke `list`, `status`, `gc`, `materialize`, and `remove` without an explicit contract argument.

### Important boundary: isolated roots are not universal ABI containers

osquery 5.22.1 was deliberately used as a falsifier. Its signed 31-package root materialized correctly and `osqueryi --version` launched, but a real `system_info` query aborted with `free(): invalid pointer`. The temporary root was removed.

That result narrows the mechanism correctly:

> isolated equipment is a package-materialization tool, not a claim that arbitrary host-coupled software is relocatable or ABI-isolated.

Tools that depend strongly on host ABI/kernel integration need either normal system installation, a different containment technology, or no admission at all.

## Final disposition matrix

| candidate | decision | reason |
| --- | --- | --- |
| targeted mutation testing | **retain method** | killed two mutants and found one real surviving Game boundary mutant |
| StrykerJS | defer | method proved useful, engine acquisition/runtime has not yet earned permanent cost |
| Playwright Chromium + Axe | **retain existing** | already covers current Web claims |
| Firefox/WebKit | defer | no current compatibility claim; provisioning cost/failure observed |
| Lighthouse/LHCI | defer | no incremental finding beyond existing Web budget/review gate |
| TShark | **retain on-demand** | deterministic PCAP -> structured protocol facts |
| Nmap | **retain bounded on-demand** | independent local surface observation; must be scoped/deadlined |
| mitmproxy | **conditional retain** | local HTTP flow record/replay passed; large closure, experiment-only |
| Semgrep | defer | no incremental finding over existing static/supply-chain stack |
| Hypothesis | **retain method, defer dependency** | 330 generated Finance cases passed; py312 project authority must not drift |
| Marimo | defer | no current consumer and no admitted local supply path |
| osquery | **reject/defer** | host-coupled isolated trial crashed; existing doctor/status already owns needed semantics |
| OpenTelemetry/Prometheus/Grafana | reject/defer | prior P6/A0 experiments still show no continuous-telemetry consumer |
| new quant/database platform | reject | no missing Finance responsibility demonstrated |
| `isolated-equipment` Workstation utility | **promoted** | repeated cross-domain friction, signed fail-closed live dogfood, deployed compact discovery/GC surface, no package/PATH mutation |

## Responsibility model after E0

```text
Domain owner
  Game / Web / Security / Finance
  decides what observation/test means
          ↓
semantic equipment profile
  e.g. packet.decode / network.surface.observe / mutation.audit
          ↓
Workstation
  discovers/materializes machine equipment
  but does not claim domain truth
          ↓
Runtime
  exact executable + immutable inputs + process/artifacts/recovery
          ↓
Harness
  exposes the narrow capability to the Agent
```

Do not expose arbitrary GUI/CLI folklore as the durable interface. Once an equipment profile has repeated consumers, its Agent surface should name the operation (`packet.decode`, `network.surface.observe`, `http.flow.record`, `test.mutation.audit`) and keep the underlying executable replaceable.

## World-model update

The round supports a narrower equipment law than “install more professional tools”:

> The highest-value Agent equipment often does not create a new domain capability. It compresses a fragile multi-step observation, falsification, or transformation into one structured, replayable, inspectable operation. Equipment should be admitted by measured information/friction gain, while semantic authority remains with its owner.

A second law follows from the failed osquery treatment:

> A low-friction materialization mechanism is not a universal execution environment. Supply identity, ABI compatibility, execution authority and domain meaning remain separate questions.

The next equipment expansion should therefore be triggered by a concrete workload, not by a software catalog.
