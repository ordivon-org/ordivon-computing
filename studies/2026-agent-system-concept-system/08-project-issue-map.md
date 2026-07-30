# Project Issue Map

This map turns the concept system into bounded repository responsibilities. It deliberately reuses existing Issues where they already own the work and creates only the missing high-value boundaries.

## Parent research

- [`ordivon-computing#83`](https://github.com/zycxfyh/ordivon-computing/issues/83) — validate Harness, Host, Runtime, extension, lifecycle, and cross-Harness continuation boundaries.

Computing owns taxonomy, mature baseline comparison, experiments, falsifiers, promotion, and deletion decisions. The Issue authorizes research and bounded spikes, not a new repository.

## Product and laboratory Issues

| Repository | Issue | Owned question | Priority |
|---|---|---|---|
| Ordivon Host | [`#14`](https://github.com/zycxfyh/ordivon-host/issues/14) | Host–Harness ownership, capability manifest, Assignment generation, CompletionProposal, and cross-Harness continuation | P0 |
| Ordivon Runtime | [`#64`](https://github.com/zycxfyh/ordivon-runtime/issues/64) | Host Task/Task Attempt versus Runtime Job/Runtime Attempt; correlation, evidence, and naming migration test | P1 |
| Ordivon Game | [`#58`](https://github.com/zycxfyh/ordivon-game/issues/58) | Deterministic Session, compaction, replacement, Hook, and completion-boundary ablations | P1 experiment |
| Ordivon Security | [`#19`](https://github.com/zycxfyh/ordivon-security/issues/19) | Adversarial Harness, Context, Hook, lease, completion, and evaluator-boundary attacks | P1 experiment |
| Ordivon World | [`#2`](https://github.com/zycxfyh/ordivon-world/issues/2) | Capability negotiation and provider rebinding without a universal broker | P1 after W1 |
| Ordivon Web | existing [`#30`](https://github.com/zycxfyh/ordivon-web/issues/30) | Publish accepted project matrix only after implementation and evidence | deferred publication |

## Existing Issues retained rather than duplicated

### Host

- `#2` remains the compact cross-session handoff capsule.
- `#6` remains Context provenance, trust, and invalidation.
- `#13` remains persistent provider Session evidence.
- New `#14` integrates their boundary without replacing their individual experiments.

### Runtime

- `#56` remains the strong comparison against plain MCP Tools, idempotency, audit, and durable Activities.
- New `#64` is narrower: terminology, foreign identity, and Host-facing execution contract.

### Game

- `#39` and `#41` remain convergence on one logical Host and deletion of duplicate Host paths.
- `#40` remains equal-budget multi-Agent coordination.
- New `#58` isolates Harness lifecycle and continuation rather than opening another Game architecture program.

### Security

- `#10` remains deception through Context, Tool, memory, and delegation.
- `#12` and `#13` remain evaluation validity and repeated-trial foundations.
- New `#19` targets the newly explicit control and completion boundaries.

### World

- `#1` remains the first complete Host-to-World interaction.
- New `#2` begins only after or as an evidence-driven extension of W1.

## Execution order

```text
Computing #83 freezes experiment contracts and baselines
        ↓
Host #14 defines the smallest experimental Harness boundary and CompletionProposal
        ↓
Runtime #64 binds physical execution identity without semantic Task ownership
        ↓
Game #58 runs low-cost deterministic continuation and compaction ablations
        ↓
Security #19 attacks the retained boundaries and evaluators
        ↓
World #2 tests external capability negotiation and rebinding
        ↓
Computing decides retain / localize / shrink / delete / promote
        ↓
Web #30 publishes only accepted and implemented roles
```

Game and Runtime work may proceed in parallel once Host publishes the experimental contract. Security should consume actual retained mechanisms rather than hypothetical fields. World capability routing remains after W1 or another real provider-rebinding failure.

## Stop conditions

- no separate `ordivon-harness` repository before the promotion gate;
- no generic Hook engine, Event Bus, Plugin SDK, memory service, or provider broker;
- no Runtime API rename without a real consumer and measured benefit;
- no Game/Security shadow Host or Harness;
- no Protocol promotion from documentation or one synthetic workload;
- no Web project page for Harness while it remains a candidate boundary.

## Promotion evidence

The Harness boundary may be extracted only after:

```text
two live materially different Harness adapters
two consuming workloads or repositories
one successful mid-Task Harness replacement
stable lifecycle and capability contracts
independent release/test value
measurable duplicate-code reduction
no Host or Runtime authority leakage
```

A negative result is useful: it may prove that Host-local adapters and mature provider Harnesses are the correct final architecture.
