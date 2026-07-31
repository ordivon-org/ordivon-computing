# Ordivon Experiment Ledger

This chapter summarizes admitted measurements. Exact receipts remain authoritative.

## 1. Task Continuation v0

### Question

Can a fresh Host process continue a bounded Task without loading the original transcript or retaining a Provider Session?

### Frozen comparison

| Input condition | Serialized bytes | Result boundary |
|---|---:|---|
| Full transcript | 3,894 | comparison baseline |
| Manual handoff | 945 | compact human-authored baseline |
| No memory | 147 | insufficient Task state |
| TaskCapsule complete | 2,604 | sufficient in frozen path |
| TaskCapsule without decision Artifact | 2,420 | rejected |
| TaskCapsule without accepted Fact | 2,454 | rejected |

The manual handoff was 24.2% of transcript size. Size alone was not the result: omitted decision or Fact fields caused explicit failure even when the remaining object was larger than the manual handoff.

### Live evidence

- fresh Codex and isolated Hermes processes consumed the same Capsule and compiled Context;
- neither loaded the original transcript;
- neither retained a Provider Session as Task state;
- both selected the same admitted action identity and completed the same semantic Effect in the bounded fixture;
- world drift changed the allowed action to `refresh-world` rather than being treated as ordinary model failure.

### Supported conclusion

Bounded semantic state can carry one Task across fresh model processes. A transcript and Provider Session are useful cognitive state, not authoritative continuation state.

### Limit

The fixture contained one guarded mutation and a narrow action set. It did not establish a universal memory schema.

## 2. Core Work System Round 1

### Deterministic matrix

The matrix contained 16 isolated variants across continuity, Context, Effect, and attention.

| Family | Trials | Passed | Failed |
|---|---:|---:|---:|
| Continuity | 4 | 3 | 1 |
| Context | 4 | 2 | 2 |
| Effect | 4 | 3 | 1 |
| Attention | 4 | 2 | 2 |
| **Total** | **16** | **10** | **6** |

This is an inventory, not a leaderboard. Strong baselines were allowed to retain the same application semantics.

### Durable-work baselines

LangGraph SQLite checkpoints and Temporal Workflow state recovered the tested work correctly. The experiment therefore rejected a separate Ordivon Task Runtime.

Selected measured representations:

| Variant | Result | Measured state bytes | Measured elapsed ms |
|---|---|---:|---:|
| LangGraph SQLite | passed | 32,768 SQLite-file bytes | 266 |
| Temporal Workflow | passed | 1,826 serialized application-checkpoint bytes | 12,133 |

These byte and timing measures are not normalized framework benchmarks. Temporal timing includes local test server and Worker startup; LangGraph bytes include SQLite representation.

### Context variants

| Variant | Result | Context bytes | Estimated tokens | Stale source | Unsupported claim |
|---|---|---:|---:|---|---|
| Full transcript | failed | 384 | 96 | yes | yes |
| Current-revision retrieval | passed | 416 | 104 | no | no |

Current retrieval matched the tested source-bound requirement. The result retained enforceable provenance/invalidation metadata and rejected a generalized Context Kernel.

### Live Provider-replacement gauntlet

Six physical trials completed:

| Order | Trials | Accepted | Mean elapsed ms | Range ms | Hermes-reported tokens | Hermes-reported cost USD |
|---|---:|---:|---:|---:|---:|---:|
| Codex → Hermes | 3 | 3 | 42,143 | 37,232–49,458 | 4,733 | 0.01011114 |
| Hermes → Codex | 3 | 3 | 37,828.667 | 36,416–39,281 | 5,625 | 0.01234356 |
| **All** | **6** | **6** | **39,985.833** | **36,416–49,458** | **10,358** | **0.02245470** |

Only Hermes usage was captured in these token/cost fields. No conclusion about comparative model efficiency is permitted.

All six trajectories:

- used no original transcript;
- used no retained Provider Session;
- preserved one Effect identity;
- preserved `UNKNOWN` until reconciliation;
- produced no duplicate Effect;
- reached the frozen repository acceptance state.

### Supported conclusion

Provider replacement is a Host-state property. The experiment established portability of bounded state, not equivalence of model reasoning or quality.

## 3. Host Harness H1

H1 introduced strict content-addressed objects and deterministic transitions:

- `TaskAttemptDescriptor`;
- `HarnessAssignment` with generation;
- `HarnessRunReceipt`;
- `CompletionProposal` and `CompletionDecision`;
- capability manifest;
- four Task events and operator handoff projection.

Eight deterministic lifecycle areas covered:

- strict codec round trips and unknown-field rejection;
- capability admission;
- fresh Context on replacement;
- stale proposal retention and rejection;
- missing Artifact rejection;
- unresolved `UNKNOWN` rejection without terminating the Task;
- exactly-once accepted completion;
- fresh Host reload of proposal and decision.

No Assignment, Run, or Proposal SQL table was introduced.

## 4. Host/Runtime H2

One live request used four opaque Runtime foreign references:

```text
task
task_attempt
assignment
harness_run
```

The trajectory proved:

- exact replay returned the original Job;
- changed generation/digest conflicted under the old request identity;
- terminal evidence retained all references;
- a fresh client recovered the Job;
- Runtime made no semantic-completion claim;
- Host recorded the Runtime Job in the Run receipt.

No Runtime Task or Assignment object was added.

## 5. Codex App Server H3

### Live Run

| Field | Value |
|---|---|
| Codex CLI protocol revision | 0.145 |
| Model | `gpt-5.6-sol` |
| Provider messages | 259 |
| Total reported tokens | 27,325 |
| Tool items | 1 successful command read |
| Runtime status | succeeded / terminal clean |
| Host Task state | waiting |
| Receipt payload digest | `sha256:d7f048b4c24f4aa0c6897a7711640a3d32736c12a7d144888e69bc1262f58558` |

Codex retained Thread, Turn, Item/Tool lifecycle, usage, interrupt capability, and raw-event digest. Process success did not produce TaskOutcome.

## 6. Hermes ACP H4

### Live Run

| Field | Value |
|---|---|
| Hermes Agent | 0.18.0 |
| Protocol | ACP v1 JSON-RPC stdio |
| Model | `deepseek:deepseek-v4-pro` |
| Provider messages | 689 |
| Thought chunks | 449 |
| Message chunks | 234 |
| Usage updates | 2 |
| Total reported tokens | 35,992 |
| Tool items | 1 read |
| Tool completion update | not observed |
| Runtime status | succeeded / terminal clean |
| Host Task state | waiting |
| Receipt payload digest | `sha256:4ac6a76266c860bf623f3c7f90b87ad8eb9d702c693dc9736af283f5a5b5cad7` |

The live trajectory showed that successful Hermes Tool use may end without a later `tool_call_update`. Thought text was excluded; counts and digests were retained.

## 7. Cross-provider driver audit

| Measure | Codex direct driver | Hermes direct driver |
|---|---:|---:|
| Approximate lines | 841 | 947 |
| Exact-line Jaccard similarity | \- | 0.275 across both |

Most repeated lines were subprocess, queue, parsing, validation, serialization, and receipt mechanics. Material lifecycle semantics differed:

- Codex: Thread/Turn/Item, explicit Turn terminal event, structured output;
- Hermes: JSON-RPC Session/Prompt, bidirectional requests, thought stream, optional Tool completion update, final assistant text may be absent.

The measured overlap did not justify a shared lifecycle implementation.

## 8. H5 bidirectional replacement

The frozen repository repair ran four real Provider invocations in two orders.

### Trajectory A — Codex diagnosis → Hermes repair

| Run | Tokens | Provider messages | Thought events | Tool items | Canonical final source |
|---|---:|---:|---:|---:|---|
| Codex diagnosis | 44,255 | 86 | n/a | 2 | Provider structured response |
| Hermes repair | 242,276 | 2,329 | 1,728 | 11 | verified Artifact |

Accepted final source digest:

`sha256:1fb2d560fa109be2673b3d1834df8a441b6c88541b47fdd3c214a3bfd6095ebd`

### Trajectory B — Hermes diagnosis → Codex repair

| Run | Tokens | Provider messages | Thought events | Tool items | Canonical final source |
|---|---:|---:|---:|---:|---|
| Hermes diagnosis | 136,907 | 1,151 | 696 | 6 | verified Artifact |
| Codex repair | 69,856 | 106 | n/a | 4 | Provider structured response |

Accepted final source digest:

`sha256:d751a39f77c35bdb0f23cf91cc4da0410be54a740a53a4c5ecb60e9d689136e7`

### H5 aggregate Provider usage

| Provider | Total reported tokens |
|---|---:|
| Codex | 114,111 |
| Hermes | 379,183 |
| **Combined** | **493,294** |

These are protocol-local observed usage values, not a normalized benchmark.

### Fault F1 — stale Assignment

Both generation-1 completion claims were rejected as `stale_assignment`. The verifier did not run and no Runtime work was dispatched by stale adjudication.

### Fault F2 — physical success without Artifact

A real Runtime process exited zero and produced terminal evidence but no required `completion.json`. Host rejected `missing_artifact`, skipped acceptance verification, and left the Task `waiting`.

### Fault F3 — ambiguous response

The Codex→Hermes repair response was deliberately dropped. A fresh Host recovered exactly one original Runtime Job:

```text
dispatchCalls = 1
matchingJobs = 1
responseLost = true
```

No blind redispatch occurred.

### Final-text result

Both Codex Runs returned usable structured final responses. Both Hermes Runs produced valid Artifacts and passed independent verification with no usable ACP final assistant text.

Canonical completion therefore came from verified Artifacts when Provider text was absent.

## 9. What the ledger proves

Within the frozen workloads:

- explicit durable state can carry work across fresh processes and Providers;
- Provider Session is evidence for a Run, not the Task identity;
- Assignment generation prevents stale completion;
- process success and Provider prose are insufficient completion evidence;
- Runtime correlation needs identities and digests, not Host semantics;
- Provider-faithful drivers preserve capabilities better than a shared internal lifecycle;
- the first-party Ordivon Harness question is distinct from cross-Provider normalization.

## 10. What the ledger does not prove

- general model quality or Provider ranking;
- equal-budget performance across Codex and Hermes;
- robustness under malicious Harnesses or poisoned Artifacts;
- multi-Agent branch/join correctness;
- long-duration compaction or persistent Session value;
- that Ordivon Harness v0 will outperform mature Harnesses;
- that the retained objects are optimal for every workload.
