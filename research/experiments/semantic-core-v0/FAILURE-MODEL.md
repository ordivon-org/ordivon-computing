# Agent Semantic Kernel Failure Model v0

## 1. Purpose

This document identifies which failures are already handled by classical operating systems, which older distributed-system failures become universal under autonomous Agents, and which failures are introduced or amplified by probabilistic cognition.

The Kernel is justified only where lower layers cannot preserve the required semantic distinction.

## 2. Failure domains

### C — Classical mechanism failures

These are inherited and delegated rather than reimplemented.

| ID | Failure | Primary lower-layer owner | Kernel obligation |
|---|---|---|---|
| C1 | process crash | OS / runtime | committed semantic history must survive |
| C2 | partial local disk write | SQLite / filesystem | use atomic transaction and fail closed on corruption |
| C3 | concurrent local writers | SQLite + journal-head CAS | reject stale semantic projection |
| C4 | process/resource exhaustion | OS / Ordivon | preserve semantics; future production implementation needs quotas |
| C5 | file/network/process isolation failure | OS / sandbox / Ordivon | do not claim to replace the lower security boundary |
| C6 | local clock or scheduling delay | OS/runtime | do not infer external completion from elapsed time alone |

### D — Older distributed failures promoted to a universal Agent concern

| ID | Failure | Required semantic response |
|---|---|---|
| D1 | request delivered, response lost | Dispatch becomes `UNKNOWN`; do not mark failed |
| D2 | timeout after possible side effect | reconcile by stable request identity |
| D3 | duplicate delivery after retry | correlate original Dispatch or require explicit new attempt |
| D4 | cancellation races completion | preserve request and observed terminal outcome separately |
| D5 | local process exits while remote Job runs | replay Effect/Dispatch and resume observation |
| D6 | backend says rejected but may have admitted | search for correlated operation before safe retry |
| D7 | remote history expires before reconciliation | remain unresolved or escalate; never invent certainty |
| D8 | Tool contract changes while work is pending | fail closed until contract compatibility is classified |

### A — Agent-native or Agent-amplified failures

| ID | Failure | Required semantic response |
|---|---|---|
| A1 | model dynamically proposes an invalid action | proposal must pass deterministic admission rules |
| A2 | model forgets that an action already occurred | durable Effect/Dispatch identity overrides context memory |
| A3 | model interprets transport failure as world failure | Kernel preserves `UNKNOWN` independently of model belief |
| A4 | model self-attests success | Observation, Verification, and Fact authorities must be separated |
| A5 | Agent autonomously retries or fans out | every attempt must retain causal ownership and budget scope |
| A6 | plan drifts beyond delegated purpose | signed Effect authority records issuer, principal, trust domain, and policy version |
| A7 | context compression drops crucial uncertainty | durable state must not depend on prompt inclusion |
| A8 | Tool description/schema drift changes meaning | contracts and semantic reducers require explicit versions |
| A9 | Agent treats exit code or Tool text as goal completion | completion requires declared verification evidence |
| A10 | multiple Agents reproduce the same faulty source | cross-Effect evidence is not automatically an independent trust domain |

## 3. Fault injection points

The reference implementation injects failures at the following boundaries:

```text
before semantic mutation
inside multi-command semantic transaction
after Dispatch start, before Tool return
after backend admission, with response discarded
inside result projection with malformed evidence
during cancellation race
during process restart and journal replay
during concurrent stale-writer commit
inside journal entry/hash/head integrity
before Verification and Fact admission
```

## 4. Required response classes

Every failure must resolve to one of these classes:

| Class | Meaning |
|---|---|
| `REJECTED` | evidence proves the external operation was not admitted |
| `UNKNOWN` | admission or outcome cannot currently be proved |
| `RECONCILING` | the original operation is actively being located or observed |
| `FAILED` | definitive terminal failure evidence exists |
| `CANCELLED` | definitive cancellation evidence exists |
| `SUCCEEDED` | definitive Effect-level success evidence exists |
| `CORRUPT` | local durable history cannot be safely interpreted |
| `CONFLICT` | current writer or revision is stale |

No exception name, timeout, missing response, or model judgment may bypass this classification.

## 5. Evidence authority path

M2.5 extends the consistency model with role-scoped authority and attestation:

- Effect proposals carry an authenticated proposer;
- Dispatch admission carries an execution authority;
- Observations carry issuer, trust domain, attestation kind, and contract version;
- Verifications carry evaluator authority and policy version;
- Fact admission records the accepting authority and complete evidence path.

These signed records preserve the same Effect, Dispatch, evidence, and Journal primitives while making authority provenance replayable and mechanically verifiable.

## 6. Exit criterion

A claimed guarantee is complete only when:

1. its failure can be injected or reproduced;
2. the forbidden state is mechanically asserted absent;
3. the required state survives replay where relevant;
4. the test is linked from `CONFORMANCE.md`;
5. limitations and trust assumptions remain explicit.
