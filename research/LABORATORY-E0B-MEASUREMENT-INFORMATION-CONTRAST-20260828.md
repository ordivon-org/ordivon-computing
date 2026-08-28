# Laboratory E0-B Measurement-Information Contrast — 2026-08-28

## Standing

**PRE-DATA CONTRAST FROZEN — STATIC AMBIGUOUS / ACTIVE DYNAMIC DISCRIMINATING**

E0-B should not merely show that a waveform can be measured. The stronger useful question is whether the selected measurement **contains information that changes the reachable classification**.

## Loading check before Reality contact

Analog Discovery 3 specifies two analog input channels with `1 MΩ || 24 pF` input impedance. Adding that observer model to the two RC candidates gives approximately:

```text
A: nominal τ = 1.000 ms  -> loaded τ ≈ 0.9990 ms
B: nominal τ = 4.700 ms  -> loaded τ ≈ 4.6781 ms
```

Both remain comfortably inside the already-frozen bands `0.891–1.111 ms` and `4.188–5.222 ms`. The observer therefore perturbs the target slightly without erasing the distinction.

At nominal 3.3 V, the same 1 MΩ input resistance predicts loaded steady outputs of about `3.2967 V` and `3.2846 V`, only ~`12.1 mV` apart. That is smaller than the conservative planning accuracy bound obtained from the AD3 datasheet around this voltage. Static DC is therefore not preregistered as a reliable A/B classifier. The real run must still qualify its actual range/configuration; this planning calculation is not a calibration receipt.

## Frozen information contrast

### Baseline: `STATIC_ONLY`

The blinded classifier may receive the opaque candidate id and admitted steady LOW/HIGH scalar `Vin/Vout` summaries, but not the waveform shape or resistor identity. It must commit:

```text
STATIC_AMBIGUOUS
```

unless the real admitted static measurements unexpectedly provide a valid unique discriminator. In that case the preregistered assumption has been falsified and E0-B may **not** claim that the dynamic measurement created the missing discriminability.

### Intervention: `ACTIVE_DYNAMIC`

Add only the Pico LOW→HIGH transition and simultaneous raw AD3 `Vin/Vout` time series. `t0` comes from the observed `Vin`, not the GPIO command. For the simple-step `t63` classifier, measured `Vin` 10–90% rise time must be ≤`44.55 µs` (5% of the lower edge of the A-band). A slower edge returns `MEASUREMENT_NOT_ADMITTED` unless a new pre-data contract explicitly models the observed input dynamics.

The active classifier then commits one of the already-frozen outcomes:

```text
MODEL_A
MODEL_B
MODEL_OR_MEASUREMENT_MISMATCH
MEASUREMENT_NOT_ADMITTED
```

## What a positive information result requires

```text
STATIC_ONLY -> STATIC_AMBIGUOUS
AND
ACTIVE_DYNAMIC -> unique preregistered model
AND
post-classification reveal agrees
```

Only that sequence supports the bounded claim that **time-resolved active measurement produced decision-relevant discrimination unavailable under the admitted static measurement grammar**.

This is intentionally stronger than “more sensors are better.” It uses the same observer and changes the information relation. More hardware, more samples or more relations do not earn capability credit unless they change the target decision.
