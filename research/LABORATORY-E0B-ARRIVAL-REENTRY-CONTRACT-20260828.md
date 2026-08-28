# Laboratory E0-B Arrival / Re-entry Contract — 2026-08-28

## Current standing

**WAITING FOR PHYSICAL ARRIVAL — NO EXECUTION AUTHORITY**

E0-B v0.2 already has frozen synthetic targets and a minimized first-contact carrier set. This document defines what must become true after delivery before Ordivon may treat the objects as an executable physical experiment. It is deliberately a re-entry recipe, not a new equipment registry.

## The admission ladder

```text
ordered
!= arrived
!= identified
!= attached
!= provider-serviceable
!= measurement-valid
!= fit-for-this-decision
!= experiment-admitted
```

Passing a lower rung never silently satisfies the next one.

### G0–G1 — arrival and exact object identity

For Pico 2, AD3, the static reference and load-bearing RC parts, retain source/transaction evidence, arrival evidence, physical condition/accessory check and enough exact identity to refer to the same object later. AD3 should retain its exact model/SKU and serial or provider-native unique identity when available; components receive bounded object/lot identity rather than remaining anonymous values.

### G2 — Workstation attachment binding

Once the real USB devices exist, Workstation should observe the smallest current local binding needed by the actual carriers: attachment/endpoint/driver/provider generation. That is a natural instance of Workstation's already-stated future USB-instrument responsibility. Workstation still does **not** own calibration, measurement validity, experiment semantics or safety.

Do not implement a speculative generic USB-instrument registry before real arrival reveals the actual endpoint/driver semantics.

### G3 — programmable generation and re-entry

The Pico firmware/source artifact must be digest-bound and reproducibly flashable. The AD3 acquisition path must bind the actual WaveForms/runtime/SDK generation used. A safe reconnect/process-restart check should show that the same physical carrier can be re-entered rather than relying on one lucky live session.

### G4–G5 — static reference and component envelope

The post-classification resistance reference only needs to be demonstrably fit for distinguishing ~1 kΩ from ~4.7 kΩ; that does not require inventing a universal calibration claim. The resistor/capacitor used for the blinded candidate must already lie inside the preregistered tolerance envelope before waveform classification begins.

### G6 — blinding

The hidden resistor must be genuinely hidden from the classification context. A preparation-side record binds an opaque `candidateObjectId` to the resistor identity. The classifier sees the opaque id and allowed setup metadata, not the resistor label/value/inventory record. Reveal occurs only after a classification receipt has been committed.

Without this separation, E0-B collapses into reading the answer from inventory rather than producing discriminating physical evidence.

### G7–G8 — admitted observation and low-energy scope

AD3 must retain simultaneous raw `Vin` and `Vout`, at ≥1 MS/s, with channel/range/coupling/sample metadata and enough unclipped waveform to compute normalized `t63`. The Pico GPIO remains the only excitation for v0.2, in the nominal 0↔3.3 V regime. No bench PSU, soldering, custom PCB or E1 mechanics are required.

`GPIO HIGH` is not physical input truth: the captured `Vin` waveform is.

### G9 — classify before reveal

Only the frozen bands may be used:

```text
Model A: 0.891–1.111 ms
Model B: 4.188–5.222 ms
```

The pre-reveal result must be one of:

```text
MODEL_A
MODEL_B
MODEL_OR_MEASUREMENT_MISMATCH
MEASUREMENT_NOT_ADMITTED
```

No resistor identity is exposed before this receipt exists.

### G10 — reveal and bridge adjudication

After classification, reveal the resistor identity/static-reference result. A positive bounded bridge requires an admitted measurement and agreement between pre-reveal classification and post-reveal physical identity. A mismatch remains a valid negative result; it must not be repaired by tuning R/C after the waveform is known.

## Minimum physical set for re-entry

- Raspberry Pi Pico 2 with headers / SC1632 ×1
- Analog Discovery 3 Pro Bundle / 471-060 ×1
- UT61E+ ×1, or a separately admitted equivalent static reference
- breadboard + known-good test/data leads
- 1 kΩ ≤1% and 4.7 kΩ ≤1% resistor candidates
- documented 1 µF film capacitor ≤10%

SDS824X HD, SPD4323X, soldering/exhaust, custom PCB and E1 mechanics are not prerequisites for this first bridge.

## Re-entry trigger

Do not infer readiness from purchase plans or local USB silence. Reopen physical execution when there is actual arrival + identity evidence for the minimum set, then let the relevant owners observe current bindings and generations.

A separate information-contrast gate now requires `STATIC_ONLY -> STATIC_AMBIGUOUS` before dynamic data are exposed, and requires the captured `Vin` edge to be fast enough for the simple-step `t63` classifier. Measurement validity alone is therefore not treated as information sufficiency.

Current pre-arrival software standing is recorded in `LABORATORY-E0B-PREARRIVAL-SOFTWARE-READINESS-20260828.md`: likely Pico/AD3 SDK surfaces are not currently materialized in the bounded node audit, but installation is deliberately deferred because physical arrival remains the earlier blocking cut.

The deeper safety/device/object/metrology/evidence derivation sources used by this contract are now available in the exact-byte physical foundation kernel reconciled by `LABORATORY-PHYSICAL-FOUNDATION-KERNEL-RECONCILIATION-20260828.md`; their dated status labels do not override this contract or current Reality evidence.
