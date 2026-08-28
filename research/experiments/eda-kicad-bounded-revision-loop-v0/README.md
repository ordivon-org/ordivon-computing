# KiCad Bounded Semantic Schematic Revision Loop v0

## Standing

`P5 ROLE_VALIDATED — BOUNDED SEMANTIC SCHEMATIC REVISION`

This is a deliberately narrow KiCad role admission. It does not promote arbitrary schematic creation or PCB geometry authoring.

The owner operation is an exact precondition-fenced revision: add local label `GRID_A` at endpoint `(154.94, 58.42)` of wire `86c097c9-ec0d-4841-90fb-614d7a7ae209`. The baseline schematic digest is part of the contract, so a repeated execution against already-mutated bytes is rejected rather than duplicating the edit.

The realized candidate preserves provider-observed target connectivity (`R1.1`, `U1.1`, `U1.7`) while changing the effective target net name from `Net-(U1A-G)` to `/GRID_A`. KiCad then passes the bounded whole workflow: electrical ERC, PCB DRC/unconnected/parity, BOM, Gerber, drill and PCB-body STEP.

Recovery is part of the admission rather than an afterthought. The inverse operation removes exactly one inserted label under a unique-match fence. The recovered schematic SHA-256 and the full project content-tree digest equal the baseline exactly, and provider ERC re-entry remains electrically clean.

## Why P5 is narrow

The Laboratory P5 rule validates one representative task for the **claimed role**. The claimed role here is not `KiCad = full electronic-design authoring`; it is only:

```text
structured bounded semantic schematic revision
→ deterministic provider artifact
→ machine-checkable semantic/electrical/fabrication consequence
→ stale-precondition rejection
→ exact recovery/re-entry
```

Still open: new schematic creation, broader component/value/topology operations, PCB geometry authoring, component-complete 3D assembly, full-schematic simulation-model closure and physical circuit evidence.

## Retained evidence

- `operation-contract.json` — exact operation/precondition/non-claims.
- `candidate-ecc83-pp_v2.kicad_sch` — exact realized candidate bytes.
- `semantic-verification.json` — current provider semantic relation check.
- `erc.json`, `drc.json`, `bom.csv` — current machine-readable lowering evidence.
- `result.json` — whole-loop receipt including fabrication artifact digests, stale-precondition rejection and exact recovery.
