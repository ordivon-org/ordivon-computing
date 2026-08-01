# R6 Real-Model Adversarial Transfer

Status: completed

R6 replaced synthetic attack probabilities with real DeepSeek V4 Agent runs,
real Ordivon Host/Harness state, live Runtime Tool execution, owned Canary
resources, and independent verification.

The executable experiment and immutable evidence live in:

[`../../research/experiments/adversarial-transfer-r6/`](../../research/experiments/adversarial-transfer-r6/)

## Central result

The attack documents themselves produced no world consequence under the tested
configurations. A stronger structural attack did:

```text
benign Task evidence
+ malicious Tool description
+ ambient Tool authority
→ real Canary-secret read
→ real opaque Python execution
```

Narrow ToolGrant blocked the same model behavior before execution. Hard stop
preserved safety but destroyed utility. A typed `tool_grant_denied` observation
then allowed the real model to recover and complete the authorized task without
weakening the physical boundary.

## Evidence volume

```text
34 formal live Trials
220 model calls
230 Tool calls
1,216,298 total tokens
DeepSeek V4 Flash and Pro
```

## Architecture decision

Retain:

- exact Tool schemas;
- durable Tool catalog and Assignment binding;
- Assignment-scoped ToolGrant;
- typed recoverable deterministic denial;
- independent Job, Artifact, Workspace, and completion verification;
- explicit Runtime `UNKNOWN`.

Do not promote a central Security platform, universal AttackChain, Campaign
state, or global telemetry layer.

The remaining narrow question is whether the exact serialized Tool definitions
sent on each model Turn should be digest-bound to the durable Assignment catalog.
That question requires one other Provider or mature Harness before promotion.
