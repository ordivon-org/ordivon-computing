# Laboratory E0-B Pre-arrival Software Readiness — 2026-08-28

## Standing

**NOT MATERIALIZED YET — DEFER INSTALL UNTIL PHYSICAL ARRIVAL OR A REAL PRE-ARRIVAL BUILD CONSUMER**

The E0-B physical bridge has a concrete future software need, but that does not make today the right time to install every likely SDK. A bounded node audit found ordinary `cmake`, `ninja` and Python, but no current `arm-none-eabi-gcc`, `picotool`, `pioasm`, known Pico SDK tree, `libdwf`, WaveForms installation path, or Digilent uninstall record in the checked Linux/Windows surfaces.

This is a **current bounded observation**, not an exhaustive absence proof. More importantly, it is not the current minimum blocking cut: E0-B is already waiting for actual physical arrival and identity receipts.

## Why installation is deferred

Installing today's likely SDK versions before the device exists would create a new generation/currentness obligation without proving that the selected carrier/driver path works with the received hardware. The better sequence is:

```text
physical carrier arrives
→ exact object + USB/driver binding observed
→ choose current supported provider path
→ materialize minimum software
→ pin exact generation/digest
→ hardware-backed enumerate/configure/acquire or flash/re-enter receipt
```

### AD3

After arrival, materialize only enough WaveForms/runtime/SDK surface to enumerate the exact AD3, configure simultaneous `Vin/Vout` capture, retain raw buffers and recover after reconnect/process restart. Workstation owns the local attachment/binding fact; Laboratory owns whether the measurement path is valid for E0-B.

### Pico 2

After arrival, choose the smallest deterministic firmware/flash route that can produce the preregistered LOW/HIGH stimulus and be reconstructed from retained source/artifact identity. Do not pre-decide between a full C SDK/toolchain and a smaller admissible route merely because one is conventional.

## Reopen condition

Reopen software materialization before delivery only if a concrete pre-arrival consumer appears — for example, a firmware artifact must be built/tested for a real downstream reason. Even then, keep `software executable` separate from `hardware serviceable`.
