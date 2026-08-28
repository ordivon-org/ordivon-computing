# Ordivon Laboratory — E0/E1 Physical Falsification Programme v1.0 FROZEN

Date: 2026-08-27  
Status: **PROGRAMME FROZEN FOR INVENTORY/BUILD DELTA; reopen only on evidence**  
Current locality: mainland China / Anhui region; exact site not required for programme semantics.  
Inputs: Physical Falsifier Map; F01–F15; 15-family Cross-Audit; Evidence Ecology / Historical Reachability correction.

## 0. Freeze purpose

This document stops experiment-list expansion and fixes the first Reality-pressure sequence strongly enough that current inventory can be inspected **without allowing available hardware to redesign the research question**.

The programme is:

```text
E0-A independent readback
→ E0-B hidden passive-system identification
→ E0-C lost response with bounded persistent electrical effect
→ E0-D controller generation replacement
→ E0-E measurement-fitness discriminator
→ E1 low-energy compliant electromechanical system
```

E0 isolates evidence/binding/currentness semantics before mechanics.
E1 deliberately recomposes the same laws under persistent multi-physics consequence.

No additional E0 experiment is admitted before these run unless a required receipt is impossible to create safely with the frozen sequence.

## 1. Evidence Ecology discipline

For every trial preserve:

```text
Question
Rival claims
BeforeBlocker
Designed pressure
Evidence ceiling
Expected receipts
UNKNOWN / contradiction handling
Stop / promotion / reopen rule
```

Use designed intervention rather than waiting for accidental failure.

Physical observation remains required for realized physical claims; simulation/formal/historical evidence can shape or falsify other claim classes within their ceilings.

## 2. Common T0/T1 substrate

The E0 sequence is intentionally compositional.

Common physical capabilities:

```text
existing Workstation / Runtime
1 × MCU controller initially
2nd same-class MCU by E0-D
bounded 3.3/5 V low-voltage power
compact two-channel mixed-signal observer/stimulus (AD3-class candidate)
credible independent static DMM/reference path
breadboard / jumper leads
LED + resistor or equivalent bounded visible/electrical load
R/C passive components
raw data files + one Attempt Evidence Capsule per attempt
manual power removal
```

Exact products remain inventory/procurement-layer except where a prior family already fixed a carrier class.

## 3. E0-A — Independent Physical Readback

### Question

Can Ordivon distinguish controller-reported/commanded state from the **actual realized electrical output** through an independent physical observer?

### Rival claims

```text
H0: command/acknowledgement is sufficient evidence of realized output.
H1: realized output must be independently observed; command/ack can disagree with Reality.
```

### BeforeBlocker

Current Ordivon standing says:

```text
ReportedState != PhysicallyRealizedState
Command/Ack != PhysicalEffect
```

but Ordivon-controlled V4 physical evidence is missing.

### Designed pressure

Primary path:

```text
Runtime/host command
→ Pico GPIO low/high or bounded pulse
→ LED/resistive load node
→ AD3 ChA actual GPIO/output node
→ optional ChB load-side node
```

Run at least:

- static LOW;
- static HIGH;
- bounded pulse/toggle sequence.

Deliberately include one safe mismatch where firmware/config commands one logical state but the output/load path is intentionally disconnected or altered so software intent does not imply realized load-side effect.

### Evidence ceiling

This can establish the realized low-voltage electrical state of the observed node/load path for this attempt.

It does **not** prove all future device effects, mechanical consequences or general sensor truth.

### Expected receipts

- exact controller/device binding;
- command/dispatch receipt;
- raw ChA/ChB waveform or static samples;
- configuration/source/firmware reference;
- contradiction if command and load-side observation differ;
- Attempt Evidence Capsule.

### UNKNOWN / contradiction

If observer is absent, saturated, disconnected or timing relation ambiguous:

```text
physical output = UNKNOWN
```

Do not inherit command state.

### Pass / stop rule

E0-A passes when a fresh consumer can determine actual output from independent evidence without consulting controller self-report as authority.

No additional sensor is promoted if AD3-class observation is sufficient.

## 4. E0-B — Hidden Passive-System Identification

### Question

Can active instrumentation reveal a hidden physical relation and produce a model whose held-out predictions survive repeated measurement?

### Rival claims

```text
H0: nominal component description / prior model is enough.
H1: active stimulus + independent input/output observation changes discriminability and can identify which physical model is realized.
```

### BeforeBlocker

Instrumentation-as-representation and active evidence-production standing exists, but lacks Ordivon-controlled physical discrimination evidence.

### Designed pressure

Build two low-energy passive networks that are externally similar but have materially different time constants. Minimum:

```text
Network A: R_A × C_A
Network B: R_B × C_B
```

Keep exact values hidden from the analysis step until prediction is frozen, or otherwise label them only in a builder-side record.

Stimulus:

```text
Pico or AD3 step
```

Observation:

```text
ChA = actual stimulus
ChB = network response
same acquisition clock where possible
```

Procedure:

1. acquire one or more response trajectories;
2. estimate time constant / choose between rival models;
3. freeze predicted response at a held-out condition or time point;
4. repeat physical measurement;
5. reveal construction/reference values only after prediction comparison.

### Evidence ceiling

Supports the target passive low-voltage system model in the tested range.

Does not validate extrapolation, untested nonlinearities or general “system identification” claims.

### Expected receipts

- raw ChA/ChB time series;
- network local identity A/B;
- stimulus conditions;
- model/parameter estimate;
- frozen held-out prediction;
- residuals/repeated measurement;
- builder/reference reveal after prediction.

### UNKNOWN handling

If stimulus itself is not observed cleanly, model inference remains UNKNOWN rather than blaming the DUT.

### Pass / stop rule

Pass when independent physical traces discriminate the hidden networks/model and a frozen prediction survives within a declared exploratory residual envelope.

Do not promote better scope/DAQ if the current observer already resolves the distinction.

## 5. E0-C — Lost Response with Bounded Persistent Electrical Effect

### Decision on prior unresolved

**Freeze route A, but with no separate solenoid/relay hardware.**

Use a latched low-voltage GPIO/LED/electrical node on the existing E0 substrate.

This preserves E0-before-E1 semantic isolation while avoiding a new carrier family.

### Question

After a command may have physically executed but the host response is deliberately lost, can Ordivon represent the effect as UNKNOWN and reconcile from independent Reality rather than retry blindly?

### Rival claims

```text
H0: no response means action failed / safe to retry.
H1: response loss leaves effect state UNKNOWN; reconciliation must inspect independent physical evidence before retry.
```

### BeforeBlocker

Runtime/Book/Interlocus already have response-loss/UNKNOWN semantics. Missing evidence is a real persistent physical effect under deliberately lost response.

### Designed pressure

Firmware command:

```text
SET_LATCHED_OUTPUT(HIGH)
```

Effect:

```text
GPIO + LED/load remains HIGH until explicit RESET or power removal
```

Host/transport layer intentionally discards/withholds the success response **after dispatch**.

Independent observer:

```text
AD3/DMM reads actual output/load node
optional visual LED observation
```

Control variants:

- dispatch reaches device; response intentionally lost;
- command intentionally not dispatched / rejected, where mechanically possible to discriminate control path.

### Required semantics

Immediately after response loss:

```text
command outcome = UNKNOWN
```

No blind retry.

Reconciliation sequence:

```text
independent physical readback
+ device-native state/query if available
→ establish realized state
→ decide whether reset/retry is admissible
```

### Evidence ceiling

Proves response-loss semantics for a bounded low-voltage persistent electrical effect.

Does not prove mechanical consequences or general distributed exactly-once semantics.

### Expected receipts

- dispatch evidence;
- explicit missing response condition;
- recorded UNKNOWN interval;
- independent physical output observation;
- reconciliation event/evidence;
- final resolved state;
- no blind duplicate effect.

### Pass / stop rule

Pass only if archive preserves:

```text
UNKNOWN at T1
resolved at T2
```

rather than retrospectively rewriting T1.

### E1 repetition

E1 later repeats the same law with **motor displacement/force** as a richer persistent consequence. This is cross-physics recurrence, not a replacement for E0-C.

## 6. E0-D — Controller Generation Replacement

### Question

Can the same logical controller role be rebound to a different physical device generation without false continuity of identity/current state?

### Rival claims

```text
H0: same logical name/port/firmware role means same device state.
H1: physical identity/generation must change explicitly and current state must be re-established.
```

### Designed pressure

Use two same-class MCU boards:

```text
Controller A
Controller B
```

Prefer a class with a device-unique hardware identifier where available.

Procedure:

1. bind logical role `stimulus-controller` to A;
2. execute a small E0-A/B-like observation and close attempt;
3. disconnect A;
4. connect B, preserving logical role and preferably same firmware;
5. enumerate/bind B;
6. verify prior A attachment/currentness is not silently inherited;
7. execute same bounded output test.

Optional perturbation:

- alter port/USB enumeration while preserving role;
- later reverse A/B.

### Evidence ceiling

Proves generation/binding semantics for these controller instances and host path.

Does not prove universal hot-swap semantics for all instruments.

### Expected receipts

- physical ID evidence for A and B;
- old/new attachment generation;
- firmware/provider realization;
- role continuity separated from device identity;
- re-established serviceability/readback;
- historical attempts remain bound to A, new attempts to B.

### Pass / stop rule

Pass when fresh recovery cannot confuse A history with B current state even if role/firmware are identical.

No Device Registry is promoted if thin binding evidence suffices.

## 7. E0-E — Measurement Fitness Discriminator

### Question

Can Ordivon distinguish a **plausible indication** from a measurement procedure that is actually fit for the target question?

### Frozen first discriminator

Use one bounded PWM/pulsed 3.3 V signal and two measurement procedures:

```text
Path A: handheld DMM / static-average style reading
Path B: AD3-class waveform observation
```

Target question:

> Is the physical output a static intermediate voltage, or a pulsed/PWM signal with a particular high level and duty/timing structure?

A DMM may return a plausible average value while being incapable of answering waveform timing/shape. The waveform path can answer the target if bandwidth/timing are sufficient.

### Rival claims

```text
H0: plausible numeric reading is sufficient.
H1: fitness depends on measurand/question/procedure; a plausible average can be invalid for waveform claims.
```

### Designed pressure

Generate at least two signals with similar or intentionally related average values but different temporal structure, e.g.:

```text
static intermediate level where feasible/reference source permits
vs
3.3 V PWM with selected duty
```

If generating a precise static comparison adds unnecessary hardware, use multiple PWM frequencies/duties and ask a timing/duty question for which average DMM indication is explicitly insufficient.

Observe with both paths.

### Evidence ceiling

Establishes target-relative measurement fitness for these electrical signals/procedures.

Does not establish SI traceability of either instrument or a universal DMM/scope hierarchy.

### Expected receipts

- same physical signal identity/time;
- DMM indication/procedure;
- waveform raw data;
- target measurand/question;
- explicit adequacy conclusion;
- no claim that “more digits” equals fit.

### Pass / stop rule

Pass when a fresh Agent can explain why both readings may be honest indications while only one procedure answers the target.

Do not promote a bench DMM/scope if current paths already discriminate this.

## 8. E0 closure gate before E1

E1 may start when E0 establishes at minimum:

```text
independent electrical readback works
raw time-series capture is trustworthy enough
response-loss preserves UNKNOWN until reconciliation
controller generation can be rebound without false continuity
measurement fitness is target-relative in practice
Attempt Evidence Capsule can preserve source re-entry
```

E0 does **not** need publication-grade metrology or a universal device/evidence service.

## 9. E1 — Low-Energy Compliant Electromechanical System

### Question family

Can one bounded physical apparatus expose the separation between:

```text
command
actual motion
contact
force
compliance
blockage/missed step
slip/coupling loss
energy authority
recovery/currentness
```

with independent multimodal evidence?

### Core rival claims

```text
H1a: commanded step count is sufficient evidence of motion.
H1b: actual visual displacement can disagree with command.
```

```text
H2a: position alone is sufficient to infer interaction state.
H2b: force adds irreducible evidence for contact/compliance/blockage.
```

```text
H3a: software stop/driver command is sufficient safety authority.
H3b: independent motor-energy removal remains a separate physical authority.
```

```text
H4a: one calibration/fixture state remains valid across remount/replacement.
H4b: physical generation/currentness must be re-established after relevant change.
```

```text
H5a: response loss means motion failed/safe to retry.
H5b: physical consequence is UNKNOWN until camera/force/device evidence reconciles it.
```

### Frozen first apparatus geometry

See companion `research/LABORATORY-E1-GEOMETRY-FREEZE-20260827.md`.

Core topology:

```text
Pico-class controller
→ STEP/DIR
→ current-limited low-voltage driver
→ small NEMA-8-class stepper
→ horizontal motor shaft
→ 30–40 mm lever initially near horizontal
→ lever moves in a visible vertical plane
→ rounded/contact tip
→ replaceable compliant specimen
→ vertical force path
→ 500 g-class load-cell module kept mounted
```

Observation:

```text
camera orthogonal to lever motion plane
→ direct tip/contact-point displacement

load cell + bridge ADC
→ force trajectory
```

Safety:

```text
low-voltage source
+ driver current limit
+ default disable/sleep where available
+ independent motor-energy cut
+ physical travel hard stops
```

Calibration:

```text
motor/lever retracted or safely disengaged
known masses
→ same load-cell contact axis
→ same mounted force chain
```

No pulley/string calibration chain in first design.

### E1 states / perturbations

#### E1-0 — free motion baseline

Lever moves without specimen/contact load.

Purpose:
- visual motion versus command;
- baseline mechanical backlash/repeatability;
- force near baseline.

#### E1-1 — contact onset

Move until tip just contacts compliant specimen/load path.

Purpose:
- force begins changing while displacement continues;
- identify contact threshold.

#### E1-2 — compliant loading/unloading

Slow step-settle-observe sequence into and out of specimen compression.

Purpose:
- force × displacement trajectory;
- hysteresis/repeatability;
- specimen state lineage.

#### E1-3 — bounded block / missed-step pressure

Use a designed hard/rigid bounded condition within current/force envelope so commanded motion exceeds actual motion.

Purpose:
- command ≠ realized motion;
- force rises;
- missed-step/blocked interpretation.

Do not exceed predeclared force/current/travel bounds merely to create a dramatic stall.

#### E1-4 — response-loss mechanical consequence

Dispatch a small bounded move, intentionally lose host response after dispatch, preserve UNKNOWN, then reconcile with:

```text
camera displacement
+ force state
+ device/controller evidence
```

No blind repeat.

#### E1-5 — independent energy-cut trial

During a bounded state/motion sequence, remove motor energy using the F02 independent cut path.

Observe:
- future commanded energy no longer reaches actuator;
- any passive spring/gravity relaxation;
- final state;
- software/runtime liveness does not restore energy automatically.

`SafetyReset != EffectAuthorizationRevival` remains explicit.

#### E1-6 — fixture/remount currentness

Remove/remount one measurement-critical fixture/load contact element using a reversible procedure.

Run known-mass and visual checks.

Purpose:
- determine whether previous calibration/geometry remains within target envelope;
- preserve historical calibration even if current qualification fails.

#### E1-7 — specimen replacement

Replace compliant specimen C01 with C02 under same logical role.

Purpose:
- same role ≠ same physical instance;
- separate material/source versus specimen history;
- compare response classes.

#### E1-8 — controller reset / no-silent-restart

Reset the controller while the actuator remains inside the low-energy bounded envelope.

Required relation:

```text
controller reset / boot
→ motor driver remains disabled by default
→ observe/recover current physical state
→ fresh admitted operation
→ only then re-enable motor energy
```

Purpose:
- controller/process continuity ≠ physical-authority continuity;
- historical motion intent must not revive automatically;
- reset must not silently continue or repeat a prior effect.

Automatic resumed motion after reset is a hard design failure for this rig generation.

#### E1-9 — manual displacement while de-energized

After independent motor-energy cut, manually move the lever within the physical hard-stop envelope.

Expected relation:

```text
historical software step/position state
!= current physical lever position
```

Purpose:
- Reality can change outside controller authority;
- historical logical position becomes stale;
- fresh physical observation is required before the next motion.

This is the first direct physical currentness/succession test.

### Recommended execution order

```text
E1-0 free motion baseline
→ E1-1 contact onset
→ E1-2 compliant loading/unloading
→ E1-3 bounded block / missed-step pressure
→ E1-4 response-loss mechanical consequence
→ E1-5 independent energy cut
→ E1-8 controller reset / no-silent-restart
→ E1-9 manual displacement / stale position
→ E1-6 fixture/remount currentness
→ E1-7 specimen replacement
```

The order may be split into separate attempts, but later fault/currentness trials require the observer/calibration/safety path to be established first.

### Evidence ceiling

E1 supports laws about this bounded low-energy apparatus and tested perturbations.

It does not establish universal robotics, general material properties, high-speed dynamics or high-energy safety.

### Required raw receipts

At minimum:

- command/step events and controller/device generation;
- raw force ADC around each settled state;
- raw settled camera frames and bounded fault windows;
- force calibration raw data/reference mass IDs;
- visual scale/calibration evidence;
- fixture generation / key geometry;
- specimen identity + start/end state;
- environment context if available;
- energy-cut state;
- explicit UNKNOWN/reconciliation events;
- derived force/displacement trajectories kept separate from raw.

### Stop / promotion rules

Promote a Pod only from an observed blocker:

```text
vision insufficient → ToF/encoder/external camera candidate
force bandwidth/noise insufficient → stronger DAQ/instrument candidate
vibration/dynamics become target → IMU/dynamic sensing candidate
fixture iteration latency → local FDM candidate
ambient influence proven → stronger environment observation/control
bandwidth/channel deficiency → bench scope candidate
repeated automated static metrology → bench DMM candidate
```

No Pod is promoted by category completeness.

## 10. Simulation role before E1

Use only a small frozen prior model for:

- nominal lever force range;
- safe travel/current envelope;
- expected qualitative free/contact/compliant/blocked signatures.

Freeze predictions before selected held-out physical perturbations.

Model discrepancy becomes evidence; do not tune every mismatch away before recording it.

Simulation cannot establish actual slip, missed steps, load-cell currentness or specimen behavior.

## 11. Programme completion criterion

The first programme is complete when:

1. E0-A–E establish physical evidence/binding/UNKNOWN/measurement seams;
2. E1 produces at least one clean free/contact/compliant/blocked contrast;
3. response-loss is reconciled without blind retry in both electrical and mechanical carriers;
4. independent energy removal is physically demonstrated;
5. controller reset does not silently restore motion authority and a de-energized manual move proves historical position can become stale;
6. one remount/replacement currentness trial occurs;
7. raw evidence survives fresh-Agent analytical re-entry;
8. no remaining first-programme decision is blocked by an unowned capability.

At that point, do **not** automatically build E2.

Perform another retrospective audit from physical evidence.
