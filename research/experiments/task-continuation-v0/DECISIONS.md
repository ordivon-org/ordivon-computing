# Task Continuation v0 decisions

## C1 — Freeze a workload before defining memory

The Capsule schema is evaluated against one bounded, repeatable continuation failure. Fields are retained because removing them causes an observed loss of execution safety, provenance, decision fidelity, or next-action quality.

## C2 — References, not copied semantic state

Effects, Bindings, Dispatches, Facts, and Artifacts remain owned by their existing semantic layers. `TaskCapsule` stores content-addressed references and validates them on recovery.

## C3 — Decisions are Artifacts

A consequential decision is retained as a small decision Artifact. The Capsule references it rather than introducing a second inline decision truth.

## C4 — Reread the world before cognition

The Host observes current world state before compiling model context. World drift changes the allowed action set to `refresh-world`; it is not treated as ordinary execution failure.

## C5 — The model chooses; the Host constrains

A model receives bounded compiled context and returns one structured decision. The Host permits only an exact compiled action and independently enforces semantic identity, world version, Binding, and execution invariants.

## C6 — Same-provider fresh Host precedes provider comparison

The deterministic adapter establishes reference behavior and Codex supplies manual real-model evidence. Multi-provider comparison remains #32 and begins only after the same Capsule/Host path is stable.

## C7 — No transcript replay

Fresh-process evidence records `originalTranscriptLoaded=false`. The transcript baseline exists only for comparison and is never an input to the Capsule Host path.
