# P3 Agent Situation / Embodiment — P3-0 owner reality matrix

Baseline revisions:

- Computing `1ff3d8be4be464919a7ba33b9280799d1aaa35dc`
- Host `507589eb1ae602f788913c7a8fdfd7bad355fe6c`
- Harness `6639cf575eb006e8be2864037d9427b9913dd8a3`
- Runtime `761bfe8dd7ca7c5e3e514891657c986eecb204e5`
- World `da4eb2cafc7c33d0905140bceb7e7ceaef7330da`

This audit asks whether a fresh Agent needs one additional source of truth or a thinner composition of existing owner truth. The answer at P3-0 is the latter unless P3-1/P3-3 falsifies it.

| Coordinate | Host | Harness | Runtime | World |
| --- | --- | --- | --- | --- |
| durable identity | Task / Goal / Task revision / frontier | Run / turn / WorkingSet / Provider Call / Tool Step / Snapshot | Workspace / Job / Attempt / clientRequestId | provider dispatch / transfer / message / migration and owner-native identities |
| scope/currentness | exact Task revision; checkpoint meaning only | Contract/Binding + exact AgentTurnRequest; workbench liveness not probed | live Workspace source state; exact Job/Attempt; runtime.describe target availability | Host-revision-fenced owner commitments; external currentness explicitly not claimed by inspector |
| capability | next admissible Host continuity operation | installed → Run-admitted → turn-admitted exact actions | projection-only runtime.describe affordances; new Job rebinds truth | provider/domain capability conditions stay owner-native |
| authority/admission | Task revision/lease/Effect/verification/completion authority | exact Run/turn Tool + cognition action admission | executable/target/profile/input/Windows/operator authority at Job admission | World inspection grants none; destination/provider/domain authority remains native |
| execution locus/body | none implied by checkpoint runtime hint | RuntimeReference / ExecutionBinding are opaque correlation, not physical liveness | Workspace + execution target/profile/provider + Job/Attempt | Body/destination/provider endpoint/world are owner/provider/domain concepts, never a global Body table |
| occurrence/effect evidence | Host Effect/Dispatch/Verification/Outcome | Tool intent/fence/receipt, Provider Call, Run evidence | process/Job terminal evidence, Artifacts, delivery disposition | provider receipt/observation or trajectory receipt; admission != occurrence |
| continuation/recovery | task.resume/handoff/checkpoint; no Runtime validation | Snapshot/recovery/Provider/Tool reconciliation | exact Workspace/Job/clientRequestId reattachment; task.observe may reconcile one committed Job | nextOwnerOperation/reconcile original request; inspector is hint-only and grants no effect |
| semantic completion | Host/domain verification/outcome | only CompletionProposal candidate | explicitly `semanticCompletionEvaluated=false` | never inferred from provider/trajectory terminal evidence |

## Cross-owner laws reproduced

```text
semantic continuity != physical locus
installed capability != live availability != current action authority
admission evidence != occurrence evidence
physical execution success != semantic completion
historical occurrence != current presence/currentness
next-owner-operation hint != authority grant
UNKNOWN != failure != permission to redispatch
```

## W5-B2 falsifier

World W5-B2 previously necessity-tested a six-coordinate bounded-occurrence proof interface:

```text
subjectRef / ownerId / bodyRef / scopeDigest / admissionDigest / occurrenceDigest
```

P3-0 does not promote it unchanged. Operational work supplies a materially different consumer and exposes at least three mismatches:

1. a Host Task can be the continuity anchor without any canonical global Agent `subjectRef`;
2. a Runtime Workspace/Job is an execution locus, not necessarily a domain Body;
3. continuation/recovery and semantic-completion ownership are not encoded by a bounded occurrence proof.

The W5 result therefore survives as evidence for **owner-qualified scope/admission/occurrence proof roles**, not as the P3 Situation schema.

## Observation Plane boundary

`ordivon-observation-core` already owns an earned non-authoritative event/relation contract and rebuildable query projection. It can reconstruct historical Host/Harness/Runtime trajectories. Its relation closure deliberately does not infer Trial validity or current owner truth. P3 Situation may reuse that substrate for historical evidence, but current Workspace availability, Runtime target availability, World reachability/presence and current action authority still require current owner observations.
