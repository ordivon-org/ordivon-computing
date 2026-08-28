# ngspice Circuit-Simulation Current Reconciliation v0

## Standing

`P5 ROLE_VALIDATED — HEADLESS BOUNDED CIRCUIT SIMULATION`

The small 2026-08-27 RC transient fixture is replayed under the current exact ngspice 47 binary rather than transporting its old standing by prose. The current validation receipt is byte-identical to the historical receipt: `t63 = 1 ms`, `v(out@1ms) = 3.1606 V`, and `v(out@5ms) = 4.96631 V` remain within the independently computed first-order RC analytic tolerances.

The exact ngspice executable is also exposed through the current Workstation managed-equipment binding. A separate canonical KiCad→ngspice P6 experiment exercises a different AC high-pass network and analytic oracle; that gives useful cross-operation evidence without widening this P5 role to arbitrary models.

Historical validator bytes are retained as `.py.archive` so closed apparatus does not re-enter live executable research surface.

This standing is synthetic only. It does not establish real component behavior, instrument truth, arbitrary SPICE model-library correctness or full ECC83 simulation-model closure.
