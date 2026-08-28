# Laboratory E0-B Synthetic ↔ Physical Bridge Preregistration v0.3 — 2026-08-28

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

Current exact ngspice 47 v0.2 predictions are frozen before physical data at nominal 3.3 V input: Model A gives `t63 = 1.000 ms`, Model B gives `t63 = 4.700 ms`. With a 1% resistor and a documented ≤10% film capacitor, the conservative preregistered τ bands are approximately `0.891–1.111 ms` and `4.188–5.222 ms`; they are intentionally far apart.


## Pre-data carrier revision

The first preregistration used AD3 AWG as the stimulus and SDS824X HD as the independent observer. Before any physical data existed, a deletion audit found a cheaper equally discriminating split: Pico 2 supplies the independent 3.3 V digital stimulus while AD3 supplies two-channel analog observation. The RC hypotheses, tolerance bands, classification rule and negative-result semantics are unchanged; only the carrier allocation and nominal amplitude changed. The v0.1 model artifacts remain retained and explicitly marked superseded rather than erased.

## Planned physical path

```text
Pico 2 GPIO LOW -> HIGH (~3.3 V)
→ breadboard RC candidate
→ AD3 independently captures Vin + Vout raw waveforms
→ derive normalized t63
→ classify against the frozen A/B bands
→ only then reveal/check resistor identity with UT61E+ or another admitted static reference
```

The commanded GPIO HIGH is not accepted as physical input truth: `Vin` must be captured alongside `Vout`. The primary statistic is `t63` computed from measured pre/post output levels, so ordinary small amplitude error does not become a false model difference.

## Fail-closed outcomes

- `t63` inside exactly one preregistered band → candidate model selected; physical identity is revealed only afterward.
- `t63` outside both bands → `MODEL_OR_MEASUREMENT_MISMATCH`; do **not** tune R/C after seeing the waveform.
- missing instrument identity, probe/config metadata, raw waveform, or adequate sample rate → measurement not admitted.
- received capacitor lacks documented identity or exceeds the preregistered ≤10% tolerance → do not silently widen the criterion.
- no arrival/identity/binding receipt → physical execution remains blocked.

## Minimal acquisition dependency

This experiment deliberately does **not** require soldering, exhaust infrastructure, custom PCB, the programmable PSU, or E1 mechanics. The minimum physical carriers are one Pico 2 with headers as stimulus, the AD3 Pro Bundle as an independent two-channel analog observer, an independent static reference such as UT61E+, breadboard, known 1% 1 kΩ/4.7 kΩ resistors, one documented ≤10% 1 µF film capacitor and suitable data/test leads. The SDS824X HD remains valuable long-horizon capital but is no longer deletion-essential to this first contact.

## What a successful bridge would mean

A success would establish one bounded relation:

```text
frozen synthetic candidate consequence
↔ exact instrumented physical waveform
↔ post-classification physical component identity
```

It would **not** establish general circuit-model truth, universal instrument validity, or autonomous-laboratory competence. A physical mismatch is scientifically useful evidence and must remain visible rather than being repaired away.

The post-delivery admission ladder is frozen separately in `LABORATORY-E0B-ARRIVAL-REENTRY-CONTRACT-20260828.md`; physical execution remains unauthorized until its arrival/identity/binding/measurement gates can be observed from real carriers.

The measurement-information contrast is frozen in `LABORATORY-E0B-MEASUREMENT-INFORMATION-CONTRAST-20260828.md`: the blinded classifier must first establish `STATIC_AMBIGUOUS` before dynamic waveform evidence is exposed; otherwise the intended active-information-gain claim is falsified rather than assumed.
