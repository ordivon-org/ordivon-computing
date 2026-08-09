---
schema_version: 1
id: computing.research.world-model-a10-world-presence
title: World Model A10 World Presence Experiment v0
type: experiment
profile: research
lifecycle: active
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-09
summary: Second-domain A10 falsifier using World owner-defined Presence semantics to test historical/current relation admission and query-coordinate evidence reduction.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-world
  - ordivon-harness
related:
  - computing.research.world-model-loop
  - computing.foundations
---
# World Model A10 World Presence Experiment v0

## Claim

Core A10 predicts that historical evidence does not automatically establish a later current relation. World independently defines Presence as an owner-observed, scope-bound relation rather than a durable Subject or Body property.

This experiment asks whether a live Agent can preserve that distinction across historical embodiment, materialization, Body lifecycle, scope change, observation failure, and multi-Body evidence. It also tests whether a deterministic query-coordinate relation index reduces false current certainty without becoming a new World truth authority.

## Setup

- Computing base revision: `e4e463eda1f2fa245f56c3e8340389a94f0dd97c`.
- World source revision: `2f9645113538b15e51ce4546f0942b45d10fda29`, frozen in `world-wml-a10-presence-source-20260809`.
- Harness equipment revision: `f09c3795fc811c5a564a5285cf227b2a44283cf5`, frozen in `harness-wml-a10-world-equipment-20260809`.
- Provider/model: configured `deepseek-v4-flash` profile.
- Owner-native grounding: W5-A A4 Presence acceptance, W5-B B0 current-relation acceptance, and W5-B B1 second-active-destination acceptance.
- No World provider call, Entity migration, Game action, Security KVM action, or external effect occurs.

All eight evaluator answers are directly admitted by committed World owner laws. Computing does not invent a Presence invalidation rule.

## Procedure

Each case is executed under two treatments with identical underlying facts:

1. **RAW_OWNER_RECORDS** — the Agent receives owner-native records with Subject, Body, owner, scope, query, lifecycle, admission, and observation facts.
2. **QUERY_RELATION_INDEX** — the same records plus a deterministic index that groups record IDs by exact query-coordinate relation: exact query/body/scope matches, historical evidence, different-Body evidence, different-scope evidence, current owner observations, current scoped bindings, and failed current observations.

The index contains no Presence answer, no `fresh/stale` boolean, and no independent truth. It can be reconstructed from the records and query coordinates.

Two Provider replicates per treatment are predeclared. Treatment order reverses on replicate 2. Each completed decision is saved independently so Provider/process failure cannot erase already observed decisions.

Primary errors are false current certainty, false absence, and false abstention. Token use is apparatus evidence only.

## Results

Both RAW_OWNER_RECORDS and QUERY_RELATION_INDEX completed 16/16 correct decisions. The additional index changed no paired answer and increased Provider token use, so the experiment supports Core A10 across World while rejecting promotion of a shared temporal relation index. See [`RESULTS.md`](RESULTS.md) for the accepted interpretation.

## Limitations

- The experiment consumes World's existing bounded Presence semantics; it does not prove a universal Presence protocol.
- Query-coordinate indexing is experiment-local and carries no action authority.
- Two replicates expose failure existence and treatment sensitivity but do not establish population-level model reliability.
- The experiment does not test remote A2A, robots, browsers, persistent ambient Presence, or untrusted-relay authentication.
- It does not imply that every Agent decision needs a Presence query.

## Artifacts

- [`run.py`](run.py) — live Provider runner with durable progress records.
- `RESULTS.md` — created after accepted execution.
- machine receipts under `../../evidence/` — created after accepted execution.
