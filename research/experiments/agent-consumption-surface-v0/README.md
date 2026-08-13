# Agent Consumption Surface v0

Status: **ACS0–ACS9 closed**. See [`ACS9-CLOSEOUT.md`](ACS9-CLOSEOUT.md) and [`FINAL-SUMMARY.json`](FINAL-SUMMARY.json). The only remaining non-owner action is refreshing/re-registering the ChatGPT Ordivon Runtime connector so its published catalog catches up with the already-live 22-tool Runtime MCP.

This experiment asks whether current Ordivon capabilities are missing, or whether already-earned owner-native capabilities are merely expensive for a fresh Agent to discover, invoke, interpret, and recover.

## Boundary

Computing owns only the cross-owner experiment, comparison vocabulary, and derived evidence. Each product/domain owner remains authoritative for its current source, live state, effects, and semantics. This experiment must not create a central capability registry, router, scheduler, or truth store.

The candidate optimization is **capability externalization at the consumption boundary**:

```text
owner-native invariant / truth
→ owner-native primitive
→ derived projection / packaging
→ Agent discovery / invocation / interpretation / recovery
```

A projection is allowed to remove repeated mechanical reconstruction. It must not invent authority, currentness, domain truth, or semantic next actions.

## Questions

1. Which useful capabilities already exist but are hidden or under-packaged?
2. Where does a fresh Agent spend calls/tokens on mechanical navigation rather than semantic work?
3. Which surface debt is cross-owner and which is domain-native?
4. Can a smaller projection/facade reduce friction without hiding exact primitives or becoming a second owner?
5. Does the candidate survive recovery, wrong-wrapper, ablation, and cross-model falsification?

## Evidence stages

- **ACS0** — exact-revision capability/surface census across the 11 registered owner projects plus Workstation.
- **ACS1** — fresh-Agent discovery and invocation tasks over current public surfaces.
- **ACS2** — gap classification: hidden, under-packaged, misplaced, duplicate, leaky, over-abstracted, or good.
- **ACS3** — derive the smallest cross-owner consumption grammar from positive internal examples.
- **ACS4–ACS8** — owner-native implementation only for earned candidates.
- **ACS9** — cross-model, recovery, ablation, and wrong-wrapper falsification; contract or delete weak wrappers.

There is no scalar UX score. Measurements remain separate: discovery calls, wrong-surface selections, schema corrections, internal-detail burden, context bytes, tool calls, dead ends, owner hops, recovery cost, result ambiguity, authority confusion, and time to first useful effect.

## Current constraints

- Strong simpler/native primitive baseline first.
- Exact owner revision is evidence metadata, not copied authority.
- Dirty owners may be observed but cannot be represented as a clean reproducible release state.
- Research/acceptance apparatus is not automatically a product capability.
- Mechanical `nextActions` may be projected only when mechanically entailed; semantic recommendations remain Agent/domain work.
- Native escape-hatch primitives remain available even if a happy path is added.

## Run

```bash
python3 research/experiments/agent-consumption-surface-v0/collect_surface_census.py \
  --output research/experiments/agent-consumption-surface-v0/evidence/surface-census-v0.json
```

The collector reads current local repositories only. It does not mutate owner projects or invoke external effects.

For full falsification/release evidence, also inspect:

- `evidence/post-implementation-validation-v1.json` — 22/22 wrong-wrapper/currentness/effect checks;
- `evidence/post-discovery-flash-r3-eval.json` and `post-discovery-pro-r1-eval.json` — post-implementation fresh-Agent A/B;
- `evidence/workstation-pro-r5-eval.json` — targeted Workstation cross-model holdout;
- `evidence/runtime-response-loss-recovery-v1.json` — Runtime response-loss reattachment evidence;
- `evidence/runtime-owner-surface-v1.json` and `runtime-publication-gap-v1.json` — live 22-tool owner surface versus 19-tool ChatGPT publication.
