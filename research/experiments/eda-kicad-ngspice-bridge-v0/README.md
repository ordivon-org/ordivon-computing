# KiCad → ngspice Bounded Cross-Provider Bridge v0

## Result

`P6_BRIDGED_BOUNDED_SUBNETWORK`

This experiment establishes one narrow artifact/result bridge without claiming full-schematic simulation. KiCad 10.0.5 freshly exports the archived ECC83 schematic to SPICE text. The owner contract selects exactly `R3` and `C2`; selection is rejected if those references, values or the expected shared-node/GND topology are absent.

Provider export supplies:

```text
R3 Net-_P2-P1_ GND 100k
C2 Net-_P2-P1_ Net-_U1A-K_ 680n
```

The bridge maps KiCad `GND -> 0`, the shared `R3/C2` node to `OUT`, the opposite C2 node to `IN`, and adds an independent AC=1 source. This creates a first-order high-pass network with `R=100k`, `C=680n`, `tau=0.068 s`, and `fc=2.340513869 Hz`.

At exactly the analytic cutoff frequency, ngspice 47 returns `Re(Vout)=0.5`, `Im(Vout)=0.5`, hence `|Vout|=0.7071067811865476` and phase `45°`. The independent analytic oracle gives `1/sqrt(2)=0.7071067811865475` and `45°`; magnitude error is `1.11e-16` and phase error `0°`.

## Responsibility boundary

- KiCad owns the exported component identity/value/topology artifact.
- The bridge owns only explicit reference selection, `GND -> SPICE 0`, node aliases and the testbench source/analysis.
- ngspice owns numerical solution.
- The analytic RC transfer function independently challenges the solver consequence.

The source schematic also exports unsupported/unmodelled `U1/P1...` placeholders. They are deliberately outside this operation. Therefore the result is a bounded cross-provider bridge, **not** proof that the complete ECC83 schematic is simulation-ready.

## Recovery evidence

The first live probe failed because ngspice 47 batch `.meas ac` did not accept `vm()/vp()` expressions and no AC analysis ran. The repair changed only the observation mechanism to supported `.print ac vr(OUT) vi(OUT)`. Circuit, values, node mapping, analysis frequency and oracle were held fixed.

## Files

- `kicad-export.spice` — fresh KiCad provider artifact.
- `selection-contract.json` — explicit subnetwork and responsibility contract.
- `bridge.cir` — deterministic ngspice deck derived from the selected artifact plus testbench.
- `ngspice.log` — exact provider execution evidence.
- `result.json` — machine-readable bridge receipt.
