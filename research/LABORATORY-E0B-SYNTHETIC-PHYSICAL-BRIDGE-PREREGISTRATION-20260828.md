# Laboratory E0-B Synthetic ↔ Physical Bridge Preregistration — 2026-08-28

## Standing

**SYNTHETIC TARGETS PREREGISTERED / PHYSICAL EXECUTION BLOCKED BY ACQUISITION + RECEIPT**

The first synthetic engineering floor is closed, but there is not yet an admitted physical carrier. The strongest current first bridge is therefore prepared without pretending it has run. Historical checkout evidence explicitly says `PURCHASE NOT YET EXECUTED`; the current Laboratory continuity surface contains no later arrival/serial/inventory receipt. A fresh local-Linux probe also exposes no Laboratory USB/serial device, but that negative presentation is deliberately not interpreted as proof of non-ownership.

## Why E0-B is first

Use one low-voltage RC network with a hidden resistor choice:

```text
Model A: R = 1 kΩ,   C = 1 µF film  -> τ = 1.0 ms
Model B: R = 4.7 kΩ, C = 1 µF film  -> τ = 4.7 ms
```

The same capacitor should be used when practical. Both worlds settle to essentially the same DC output under a high-impedance observer, so passive steady-state inspection does not identify the resistor. A controlled step and time-resolved physical measurement do. This makes the probe about **evidence production and discriminability**, not instrument spectacle.

Current exact ngspice 47 predictions are frozen before physical data: Model A gives `t63 = 1.000 ms`, Model B gives `t63 = 4.700 ms`. With a 1% resistor and a documented ≤10% film capacitor, the conservative preregistered τ bands are approximately `0.891–1.111 ms` and `4.188–5.222 ms`; they are intentionally far apart.

## Planned physical path

```text
AD3 Pro AWG 0 -> 3 V step
→ breadboard RC candidate
→ SDS824X HD independently captures Vin + Vout raw waveforms
→ derive normalized t63
→ classify against the frozen A/B bands
→ only then reveal/check resistor identity with UT61E+ or another admitted static reference
```

The commanded 3 V level is not accepted as physical input truth: `Vin` must be captured alongside `Vout`. The primary statistic is `t63` computed from measured pre/post output levels, so ordinary small amplitude error does not become a false model difference.

## Fail-closed outcomes

- `t63` inside exactly one preregistered band → candidate model selected; physical identity is revealed only afterward.
- `t63` outside both bands → `MODEL_OR_MEASUREMENT_MISMATCH`; do **not** tune R/C after seeing the waveform.
- missing instrument identity, probe/config metadata, raw waveform, or adequate sample rate → measurement not admitted.
- received capacitor lacks documented identity or exceeds the preregistered ≤10% tolerance → do not silently widen the criterion.
- no arrival/identity/binding receipt → physical execution remains blocked.

## Minimal acquisition dependency

This experiment deliberately does **not** require soldering, exhaust infrastructure, custom PCB, the programmable PSU, or E1 mechanics. The minimum physical carriers are the AD3 Pro Bundle, SDS824X HD, an independent static reference such as UT61E+, breadboard, known 1% 1 kΩ/4.7 kΩ resistors, one documented ≤10% 1 µF film capacitor and suitable leads.

## What a successful bridge would mean

A success would establish one bounded relation:

```text
frozen synthetic candidate consequence
↔ exact instrumented physical waveform
↔ post-classification physical component identity
```

It would **not** establish general circuit-model truth, universal instrument validity, or autonomous-laboratory competence. A physical mismatch is scientifically useful evidence and must remain visible rather than being repaired away.
