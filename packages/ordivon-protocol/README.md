# Ordivon Protocol

The immutable released line is `0.3.0`. The current source tree carries an explicit **unreleased `0.4.0.dev0` candidate** that removes the zero-current-consumer `ordivon_semantics` implementation while leaving every released 0.3 Schema/vector byte and consumer pin untouched.

It owns:

- strict canonical JSON, content digests, and normative canonical vectors;
- public Effect envelopes, including repository-bound source changes;
- Tool contracts and change classification;
- immutable Effect bindings;
- normative JSON Schemas for those public wire objects;
- the implementation-independent Host workload wire profile and cross-language vectors;
- pure Decision admission for immutable Contexts and current state references;

It does **not** own a journal, Host loop, Runtime client, provider adapter, simulator, authority root, task scheduler, or verification policy.

## Stability boundary

| Module | Status | Rule |
|---|---|---|
| `anc_canonical` | normative core | canonical bytes, digest format, and vectors are protocol truth |
| `anc_protocol_types` | normative core | shared execution/completion enums; public modules re-export them |
| `anc_effect_ir` | normative core | backend-neutral Effect wire object |
| `anc_tool_contract` | normative core | normalized executable interface identity |
| `anc_effect_binding` | normative core | immutable Effect-to-contract binding |
| `ordivon_protocol.host_workload` | normative core | backend-neutral Task, Context, Decision, Dispatch, Observation, Verification, and Outcome wire validation |
| `ordivon_semantics` | **0.3 compatibility only** | absent from the unreleased 0.4 candidate; exact 0.3 bytes remain at the release/consumer revisions |

The Host workload profile deliberately does not define a DAG, scheduler, mailbox runtime, domain policy, or physical executor. It defines only immutable wire objects and pure admission checks that can be implemented by an embedded adapter, a local sidecar, or a remote Host without changing meaning.

`host-workload-v1` is specifically a **bounded candidate-decision profile**. It proves Context identity, stale-state rejection, cross-language admission, Dispatch observation, verification, and outcome transport. It is not the universal open-cognition contract used by the OH3 Ordivon Harness, and it does not standardize free ActionProposal discovery, Tool-loop history, or responsibility routing. The serialized `request-human` candidate remains a v1 compatibility term; future profiles must not assume that every missing commitment is routed only to a person.


## Current candidate

[`candidates/0.4.0.dev0.json`](candidates/0.4.0.dev0.json) describes the only current development candidate. It is **not a release** and upgrades no consumer automatically. The candidate removes `semantic-state-v1` from current package source because the Existence Gauntlet found no current production import and deletion passed the bounded Host/Harness/Game consumer surfaces.

The 0.3 release remains authoritative for every consumer that is still pinned to 0.3. `semantic-state-v1` is therefore historical compatibility, not revoked history. A 0.4 release requires explicit Host owner admission and a new consumer gate. `anc_effect_ir` and `anc_effect_binding` remain in the candidate until Host separately admits any owner-local relocation; Computer does not perform that migration.

## Releases

[`releases/0.3.0.json`](releases/0.3.0.json) is the immutable release manifest for `ordivon-protocol-v0.3.0`. It binds every packaged Schema and conformance vector by digest, records profile-level stability and limitations, names exact Host and Game consumer observations, and declares the protected failure, recurring cost, supersession trigger, and deletion condition required by Core A11.

A package version is not considered released merely because `pyproject.toml` changed. The release manifest, deterministic release check, consumer pins, bounded cross-repository gate, and matching Git tag form one release boundary. The package remains in this repository until an independent release cadence or another materially different consumer makes extraction cheaper than co-versioning with the experiments that produced it.

The existing `anc_*` Python import names and `anc.*` serialized identities are preserved in v0 because they are already covered by cross-language conformance vectors. Renaming them would be a protocol migration, not a source-layout cleanup.

Normative Schemas and vectors ship inside the distribution under `ordivon_protocol`. Research fixtures, live scripts, benchmarks, and conformance campaigns remain under `research/experiments/` and consume those packaged resources rather than maintaining shadow copies.
