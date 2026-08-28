# Ordivon Laboratory — First-Order Needs → Carrier Map v0.1

Date: 2026-08-27  
Status: **PRODUCT-TO-NEED EXPLANATION / FIRST-ORDER SEMANTIC MAP**

## 0. Purpose

Explain why each first-order purchase exists in the Ordivon Laboratory. The unit of reasoning is not product category but:

```text
Need
→ Carrier
→ Experiment / consumer
→ failure or uncertainty it protects against
→ why this carrier is persistent rather than JIT/shared
```

A product may satisfy several needs; a need may deliberately have several independent carriers.

## 1. Need families represented in the first order

The first order serves six recurring Laboratory needs:

```text
N1 Observe Physical Reality independently
N2 Stimulate / act on Physical Reality programmatically
N3 Measure quantitatively with repeatable evidence
N4 Maintain currentness / identity / recovery across failures and replacement
N5 Adapt and construct physical apparatus locally
N6 Preserve safe, reconstructible Human↔Agent operation
```

These cut across F01–F15 and are not new families.

## 2. Major electrical carriers

### SDS824X HD — independent waveform Reality observer

Primary needs:

```text
N1 independent physical observation
N3 time-domain quantitative evidence
N4 current-state/readback/recovery
N6 Human + Agent dual consumption
```

First consumers:

```text
E0-A commanded/reported electrical state vs physically realized waveform
E0-B stimulus/response observation on hidden passive systems
E0-C independent observation after response loss
E0-E waveform-vs-average measurement-fitness discriminator
future E1 PWM/STEP/DIR/power/transient observation
```

Protects against:

```text
Command/Ack == Reality
PSU/MCU self-report treated as independent evidence
DMM average reading hiding pulse/timing behavior
AD3 being the only observer of an experiment it also stimulates
```

Why persistent:

- very broad cross-experiment observer;
- slow technical depreciation;
- four simultaneous analog channels matter for common-timebase causality;
- 200 MHz headroom reduces early replacement probability;
- programmable SCPI/raw waveform path gives strong Agent Realizability while front panel preserves Human fallback.

Role statement:

```text
SDS824X HD = independent waveform authority / adjudicator
```

It is **not** primarily bought because E0 needs 200 MHz. It is bought because waveform observation is a durable Laboratory primitive.

### Analog Discovery 3 Pro Bundle — Agent-native experimental I/O

Primary needs:

```text
N2 programmable stimulus
N1 compact mixed-signal observation
N3 raw experiment buffers
N4 scripted repeatability / successor re-entry
```

First consumers:

```text
E0-A bounded stimulus + automated acquisition
E0-B AWG/response experiment and parameter sweep
E0-E PWM/pulse generation
future protocol/logic/pattern experiments
```

Protects against:

```text
manual knob-by-knob experiments that cannot be exactly replayed
GUI-only stimulus generation
separate low-use AWG + logic-analyzer capital
Human acting as the orchestration bridge for every repeated sweep
```

Why persistent:

- high Agent controllability via WaveForms SDK;
- combines AWG + logic + pattern + mixed-signal acquisition;
- complements rather than replaces the bench scope;
- Pro Bundle makes physical connection capability immediately realizable.

Role statement:

```text
AD3 = programmable experiment actor / compact observation carrier
```

### SDM3055X-E — programmable quantitative metrology channel

Primary needs:

```text
N3 repeatable electrical measurement
N2 automated acquisition/logging
N4 queryable configuration and evidence continuity
```

First consumers:

```text
E0-A static voltage/current readback
E0-B RC/static reference checks
E0-C post-UNKNOWN quantitative reconciliation where appropriate
E0-E compare static/average measurement against waveform-sensitive observation
future long-duration logging / sensor characterization
```

Protects against:

```text
manual transcription errors
unknown range/function/configuration
only having a waveform instrument for slow/high-precision quantities
Human remaining inside every repeated measurement loop
```

Why persistent:

- slow-depreciating general measurement infrastructure;
- LAN/USB/VXI-11/USBTMC gives strong automation path;
- complementary to scope and handheld DMM.

Role statement:

```text
SDM3055X-E = programmable metrology observer
```

### UT61E+ — independent/manual electrical observer

Primary needs:

```text
N1 independent check
N3 continuity/resistance/static electrical diagnosis
N6 Human fallback and epistemic redundancy
```

First consumers:

```text
E0-A independent static check
E0-C physical reconciliation independent of controller/bench-DMM software path
E0-E deliberately different measurement modality
construction/debugging throughout E0/E1
```

Protects against:

```text
shared-software/shared-network failure across all instruments
bench instrument configuration error
cable/continuity faults
false confidence from one programmable measurement stack
```

Why persistent:

- very low capital;
- portable/battery-powered independent failure path;
- frequent troubleshooting role.

Role statement:

```text
UT61E+ = independent manual epistemic fallback
```

Its lower automation is intentional, not a procurement defect.

### SPD4323X — programmable bounded energy actuator

Primary needs:

```text
N2 deliver/control electrical energy
N4 query/reconcile commanded state
N6 bounded/safe experiment power
```

First consumers:

```text
E0 low-voltage rails
E0-C lost-response + persistent electrical-effect experiment
future brownout/startup/power-cycle/voltage-current sweeps
E1 electronics/sensor/controller multi-rail power
```

Protects against:

```text
fixed-wall-adapter experiments with no programmable action surface
manual power cycling as hidden Human state
unbounded source behavior
single-rail limitations as systems become multi-voltage
```

Why persistent:

- reusable across almost every electrical/embedded/mechatronic experiment;
- four rails create option value for 3.3V/5V/analog/actuator logic combinations;
- programmable List/Sense/current limiting increase experimental action space.

Critical boundary:

```text
PSU self-readback != independent physical evidence
```

Role statement:

```text
SPD4323X = Agent-programmable energy actuator inside a bounded safety envelope
```

### Raspberry Pi Pico 2 with headers / SC1632 ×4 — deterministic local controllers and generation redundancy

Primary needs:

```text
N2 local physical control/timing
N4 identity/generation/replacement experiments
N6 cheap reconstructibility and spare capacity
```

First consumers:

```text
E0-A commanded output
E0-C latched/persistent state + response-loss experiment
E0-D controller generation A→B replacement
E0-E PWM generation
E1 STEP/DIR controller
```

Protects against:

```text
Agent/network latency being mistaken for realtime control
logical role being confused with physical generation
one broken/flashed board blocking the experiment path
replacement silently inheriting historical standing
```

Why four:

```text
A = active controller
B = generation replacement
C = parallel/fixture controller
D = immediate spare/destructive/recovery carrier
```

At current cost, availability/replacement value dominates carrying cost.

Role statement:

```text
Pico 2 with headers / SC1632 pool = deterministic local control substrate + identity/recovery test carriers
```

## 3. Local adaptation / apparatus-building carriers

### QUICK TS1200A — electrical apparatus adaptation

Primary needs:

```text
N5 solder / repair / adapt interconnections
N6 repeatable and ESD-aware local physical construction
```

Consumers:

```text
moving from breadboard to stable wiring
headers/connectors/leads/fixtures
repair and reversible iteration during E0/E1
```

Protects against:

```text
loose temporary connections becoming hidden experiment variables
outsourcing every trivial wiring change
poor thermal recovery damaging boards/components or creating inconsistent joints
```

Why persistent:

- extremely high expected use frequency;
- slow depreciation;
- low reacquisition benefit compared with having it immediately at the bench.

Role statement:

```text
TS1200A = local electrical adaptation capability
```

Computer management is optional extra value; it is not why the tool exists.

### KNIPEX 78 03 125 ESD — precision material removal

Need:

```text
N5 precise lead/wire/component cutting
```

Protects against poor cuts, board damage, and abusing one generic cutter for precision work.

A separate robust cutter carries thicker/general cutting so precision-edge lifetime is preserved.

### ENGINEER PA-14 — repeatable fine-wire preparation

Need:

```text
N5 expose conductor without nicking/damaging fine electronics wire
```

Protects against hidden conductor damage, inconsistent strip length/quality, and slow knife-based preparation.

### Mitutoyo 500-171-30 — durable dimensional reference + machine-readable measurement path

Primary needs:

```text
N3 dimensional measurement
N5 fixture/mechanical construction
N4 stable zero/currentness across repeated use
```

First major consumer is E1 fixture geometry rather than E0 electrical work.

Protects against:

```text
fixture dimensions becoming undocumented assumptions
manual ruler estimates being treated as adequate geometry
repeated zero/re-reference friction
```

Why bought before E1:

- slow-depreciating buy-once tool;
- immediate use in bench/fixture/component inspection;
- current official model table confirms SPC measurement-data output, creating a future machine-readable ingestion path;
- unlike the IP67 500-7xx coolant-proof family, current Laboratory pressure does not justify paying specifically for coolant/dust ingress protection;
- unlikely to be invalidated by E0 outcome.

Role statement:

```text
Mitutoyo caliper = persistent local dimensional reference, not precision-metrology authority for every claim
```

### Godox P260C Pro — controlled illumination / observation environment

Primary needs:

```text
N1 visual observation quality
N3 repeatable image formation
N6 Human task visibility
```

Consumers:

```text
bench documentation
wiring/currentness photographs
E1 visual displacement observation
future camera-based measurement
```

Protects against:

```text
ambient room light becoming an uncontrolled imaging variable
shadows/poor color rendering hiding wiring/component state
camera evidence varying because illumination changed arbitrarily
```

Role statement:

```text
P260C Pro = controllable observation illumination, not decorative lighting
```

Bluetooth/App is not yet an Agent API.

### NANCH precision driver + SATA metric hex

Need:

```text
N5 reversible mechanical/electronic assembly
```

Consumers:

```text
enclosures
instrument accessories
PCB/fixture hardware
E1 mechanisms
```

Protect against:

```text
wrong-bit damage
irreversible/improvised assembly
high-friction teardown/rebuild cycles
```

They are persistent because reversible assembly is a universal apparatus capability.

## 4. Support carriers

### ESD mat / wrist / grounding path

Need:

```text
N6 reduce uncontrolled electrostatic damage risk during electronics handling
```

This is F01/F02 support, not a measurement system.

### Clear side-protection eye protection

Need:

```text
N6 preserve Human physical safety during soldering and cutting
```

The whole-order horizontal audit exposed this as a real residual: soldering can eject hot solder and cutters can eject wire/lead fragments. Current external safety guidance explicitly calls for eye protection for soldering and for flying-particle wire-cutting hazards.

First-order boundary:

```text
existing current/fit clear impact eye protector with side protection
→ reuse after receipt

otherwise
→ acquire at least one operator-fit protector meeting current GB 14866-2023
   or a recognized equivalent standard
```

This is PPE at the end of the control chain. It does not substitute for fume source capture, bounded energy, correct tool use or stable workholding. Welding/splash/laser protection remains hazard-promoted.

### Quality leads / grabbers / BNC / USB data cables

Need:

```text
N1/N2 reliable physical binding between instruments and DUT
```

Protect against intermittent contacts and cable ambiguity becoming false experimental phenomena.

### Tip geometries + solder/flux/wick/cleaning

Need:

```text
N5 make the soldering station actually adaptable across component geometries and repair states
```

The station without compatible tips/process consumables is nominal rather than realized capability.

The process identity is larger than the station SKU:

```text
TS1200 / TSS02 carrier
+ tip geometry
+ temperature regime
+ solder alloy + diameter
+ flux chemistry
+ cleaning / rework path
= repeatable soldering process capability
```

Keep the first process deliberately narrow: one known solder alloy/diameter, one compatible no-clean flux family, a small wick set and one cleaning path. Do not create multiple solder/flux chemistries before a real material/process consumer requires them.

Different tip geometries are complementary rather than redundant because thermal transfer and physical access change with joint geometry. A small/medium chisel, fine bent/precision tip and larger thermal-mass tip provide the initial coverage; further tips remain pressure-driven.

### Breadboards / protoboards

Need:

```text
N5 rapid reversible apparatus construction
N4 substrate currentness / retirement discipline
```

The two substrates carry different lifecycle roles:

```text
breadboard = reversible exploration substrate
perfboard/protoboard = stabilized intermediate apparatus substrate
PCB / fixture / documented wiring = later persistent apparatus where pressure requires it
```

A breadboard is deliberately easy to change, therefore it should not silently become long-lived authoritative apparatus. Worn contacts, repeated insertion, damaged spring clips or unexplained intermittency demote the board from active-authoritative use even if it still appears usable.

The initial `2 active + 2 spare/value` 830-point policy creates both parallel experiment capacity and immediate substrate replacement. Spares are not merely stock: they are an independent replacement path when a board becomes epistemically suspect.

Small perfboards/protoboards provide the first promotion path when a topology is worth keeping stable but does not yet justify a custom PCB. Promotion should preserve wiring/photo/component identity rather than treating soldering itself as proof of correctness.

```text
Reversible != unreliable
Persistent != authoritative by default
Substrate role must match claim lifetime
```

### Resistors / capacitors / LEDs / diodes / minimal transistors

Need:

```text
N2/N5 create bounded passive/active electrical realities immediately
N3 preserve known-enough passive behavior for discriminating experiments
N4 keep cheap component identity strong enough that future experiments know what physical carrier was actually used
```

Direct E0 consumer: hidden RC systems, pullups, loads, indicators, PWM/conditioning experiments.

The economics are intentionally asymmetric:

```text
common + tiny carrying cost + high expected reuse
=> curated local abundance

unknown dielectric / unknown tolerance / anonymous assortment
=> epistemic liability, even if cheap
```

The resistor stock is approximately 1,700 pieces across 27 1% metal-film values. The capacitor stock is approximately 190 pieces across ceramic, film and electrolytic roles. Quantity abundance is admitted only because identity remains structured.

For capacitors, dielectric/technology is part of the capability identity:

```text
C0G/NP0 = preferred stable small-value ceramic when practical
X7R = ordinary documented general-purpose ceramic / decoupling candidate
film = stable-RC candidate where dielectric behavior matters
electrolytic = bulk energy / filtering carrier
Y5V/Z5U = not default timing/measurement reference stock
```

Nominal capacitance alone is therefore insufficient to define the component's experimental role. Likewise, nominal resistance alone is insufficient to define a safe load role: power rating and actual operating dissipation remain part of admissibility.

### Wire / jumpers / headers / screw terminals

Need:

```text
N5 physical interconnection and reconstructible wiring
N4 reduce topology-recovery cost through stable visual/interface conventions
N6 keep each connection inside a known mechanical/current/safety role
```

The first-order interface vocabulary is intentionally shallow:

```text
2.54 mm jumper/header
→ reversible prototype / inspection binding

2/3-pin screw terminal
→ coarse detachable low-voltage fixture boundary

locking crimp family
→ pressure-promoted persistent interface contract
```

A connector is not defined by pitch/name alone. Its realized capability includes wire range, contact system, locking/keying, electrical regime, board footprint, housing/contact inventory, mating geometry and the assembly/crimp process. Therefore multiple JST/Molex ecosystems are not stocked merely for option count.

Dupont-style 2.54 mm connections are useful because they are cheap, visible and rapidly reconfigurable; those same properties make them poor default persistent motion/vibration or safety-critical bindings. When repeated detachable modules, vibration, polarization, density, current or Human-error pressure appears, the interface should be promoted to a deliberate connector family.

Pre-crimped pigtails/adapters are preferred for sparse device-specific needs because they import an external assembly capability without forcing early ownership of every housing/contact/crimp-tool ecosystem.

Color coding and standardized interfaces support N4 currentness/reconstruction from photos/notes, but representation remains subordinate to actual binding and independent verification.

### Heat-shrink / cable ties / insulation

Need:

```text
N5/N6 safe and reconstructible interconnect stabilization
N4 preserve visible physical-boundary state rather than hiding apparatus changes inside anonymous wraps
```

The materials are complementary:

```text
2:1 thin-wall polyolefin heat-shrink
→ persistent insulation / identification / light termination support

polyimide tape
→ heat-resistant masking / local temporary isolation during soldering and rework

quality PVC electrical tape
→ conformable insulation / repair / irregular-geometry overwrap

cable ties
→ routing and bundle restraint
```

They are not substitutes for one another. A cable tie is not insulation or termination strain relief; tape adhesion is not proof of mechanical fixation; heat-shrink does not by itself make a wire mechanically load-bearing. Where cable motion reaches a connector or solder joint, a real clamp/grommet/backshell/fixture feature must carry that load.

Use heat-shrink as the default persistent small-joint carrier because it makes the insulated boundary visually explicit and does not depend primarily on adhesive. Keep the first stock to ordinary documented 2:1 thin-wall polyolefin sizes; adhesive-lined, high-shrink-ratio, chemically resistant and environmental-seal families remain pressure-driven.

Polyimide/Kapton-class identity must include the adhesive/tape construction, not just amber color or the word `Kapton`. Electrical tape likewise should be a documented electrical product rather than generic PVC tape. Product insulation ratings do not authorize mains or high-energy experiments.

Stabilization is successful only when the resulting apparatus remains inspectable and reconstructible. Wrapping a confused topology until it cannot be seen is negative capability, not protection.

### M3 / M2 / M2.5 hardware / standoffs

Need:

```text
N5 reversible fixture and apparatus assembly
N4 lower apparatus-reconstruction entropy through a small mechanical vocabulary
N6 keep board/fixture clamping inside a known geometry/load regime
```

Mechanical standardization is deliberately asymmetric:

```text
M3×0.5
→ default early fixture / bracket / apparatus fastener language

M2×0.4
→ immediate Pico-class small-board mounting regime

M2.5×0.45
→ secondary common PCB/module mounting regime
```

M3-centric abundance reduces arbitrary fastener entropy while covering most early bench/light-mechatronic work. M2/M2.5 are not competing fixture languages; they are board-interface exceptions where the physical hole geometry requires them.

Raspberry Pi Pico 2 provides 4×2.1 mm mounting holes, so the first-order small-board stock must include M2 realized mounting sets. Retaining some M2.5 sets remains rational because other common modules/boards use that regime; the two must not be conflated merely because both are called `PCB standoffs`.

A standoff capability is not a bag of pillars: matching screw/thread, length, material, nut/retention and clearance must all be known. Material also matters — metal can improve rigidity but introduce unwanted conductive proximity; nylon can provide isolation but changes strength/stiffness. Record enough identity to reconstruct the mechanical boundary.

Washers distribute load but do not automatically belong on every PCB joint. Torque, locking hardware and vibration retention remain pressure-driven. Persistence comes from a controlled mechanical relationship, not from tightening a screw as hard as possible.

### Labels / bins / bags / reorder metadata

Need:

```text
N4 physical object identity, currentness, discoverability and successor re-entry
N6 preserve ESD/MSL/polarity/safety handling metadata where it changes admissibility
```

This is not housekeeping trivia. Anonymous parts create:

```text
Asset Exists
but
Identity / specification / location / current usability UNKNOWN
```

Use identity proportional to consequence:

```text
L1 unique object identity
→ mutable/history-bearing or consequence-bearing objects: instruments, controller generations,
   reference carriers, known-good/suspect/retired substrates/cables, safety-relevant apparatus

L2 lot/bin/specification identity
→ cheap interchangeable stock whose class determines behavior: R/C/semiconductors, wire,
   fasteners, connector parts, tips/consumables

L3 role-only commodity identity
→ low-consequence generic consumables where exact lot/provenance does not alter the claim
```

The purpose is not universal serialization. The purpose is to preserve the smallest identity boundary needed to answer `what is this?`, `where is it?`, `what specification/history matters?`, and `may it be used now?`.

For L2 electronic stock preserve manufacturer/supplier labeling or transcribe behavior-bearing fields such as manufacturer part number/specification class, value/rating/tolerance/dielectric/material, quantity band, source, and ESD/MSL/polarity warnings where relevant. Storage location should be stable and shallow; mutable facts such as exact count should not be encoded into location names.

Reorder metadata represents an admitted specification and substitution boundary, not loyalty to one shop SKU. Exact load-bearing/characterized parts remain exact; ordinary commodity stock may substitute only within the recorded fitness boundary.

Keep ESD-sensitive parts in appropriate protective packaging rather than destroying handling state merely for drawer neatness. Storage becomes capability only when it improves retrieval/currentness without erasing provenance or protection.

## 5. What the first order deliberately does not solve

The first order does **not** attempt to provide all future Laboratory capability.

It intentionally leaves pressure-driven:

```text
high-power loads / electronic load
precision source-measure
RF/VNA/spectrum
thermal/high-speed/machine vision
local fabrication machinery
advanced metrology
environment chambers
robotic manipulation
production soldering/reflow
```

The first order instead establishes a durable base for:

```text
Observe
→ Stimulate
→ Measure
→ Control
→ Build
→ Cross-check
→ Recover
→ Persist evidence
```

## 6. Cross-carrier structure

The most important point is that several apparently overlapping purchases deliberately create independent paths:

```text
AD3 stimulus/observation
        +
SDS824X independent waveform observation
        +
SDM3055X-E programmable static/metrology observation
        +
UT61E+ independent manual observation
```

and:

```text
SPD4323X commanded energy state
        !=
DMM/scope independently observed physical state
```

This is epistemic redundancy, not category duplication.

Likewise:

```text
Pico logical role
        !=
Pico physical generation
```

is made testable by owning multiple same-SKU controllers.

## 7. Current facility standing

Facility completion is the last first-order capability cluster. It has three bounded roles:

```text
workholding
→ keep boards/small objects mechanically stable while Human/instruments act or observe

process heat
→ shrink/shape insulation with controlled hot air rather than a soldering-iron tip

source-capture ventilation
→ keep solder-fume generation out of the breathing zone and remove it from the room
```

### Workholding

First-order workholding is deliberately small:

```text
1 low-profile PCB holder with non-marring/electrically benign jaws
1 small general bench vise with removable soft jaws
2 small F/bar clamps
2 small spring/quick clamps
```

These carriers create reversible holding, not precision fixture metrology. A clamp that keeps a board still does not prove position, force or repeatability. Large extrusion/T-slot and dedicated fixture ecosystems remain pressure-driven.

### Process heat

If the site lacks a suitable heat gun, add one documented adjustable 220–240 V carrier with a low-temperature/low-power regime and stable rest/stand. Current Pro'sKit SS-615-family data provides a useful reference regime. This is a heat-shrink/process-heating carrier, not automatic promotion of SMD hot-air rework capability.

### Direct exhaust

The physical site can support safe direct external exhaust. Therefore first-order support is:

```text
source-capture hood/arm or small partial enclosure
+ short maintainable duct
+ pressure-capable fan selected for the actual system
+ safe outdoor discharge
```

and not QUICK 6601/6611.

HSE manual-solder guidance shows why geometry, not fan-nameplate airflow, is load-bearing: a movable hood reliably captures only within a short zone, typically around 1–2 hood diameters / roughly 50–100 mm in its example, and general LEV guidance uses roughly 0.5–1.0 m/s as a reference capture-velocity range for soldering capture hoods. The outlet must discharge safely without easy re-entry/exposure, replacement air must be available, and sticky residue makes cleaning/maintenance part of capability currentness.

The first-order authority rule is procedural rather than Agent-automated: routine soldering requires extraction operating and visibly capturing the plume away from the breathing zone. Flow/pressure sensing becomes a promotion target if soldering becomes frequent, unattended or automated.

This is a concrete example of source-neutral capability selection: a facility-level carrier substitutes for equipment ownership when it realizes the target capability with lower burden.

## 8. Standing

The item-by-item vertical expansion is closed. A whole-order horizontal audit has now checked overlap/redundancy, missing persistent capability, currentness drift, first-order-vs-JIT placement, budget arithmetic and checkout gates.

Result:

```text
major electrical portfolio      NO_DELETION — overlaps are complementary/independent evidence paths
Pico naming                     CORRECTED — official current name is `Raspberry Pi Pico 2 with headers`, SC1632
SATA low-cost hex identity      SPEC_BOUND — long/extra-long 9pc family selected at current checkout
QUICK 6601/6611                 HISTORICAL_FALLBACK — not active first-order selection
eye protection                  ADD — one real low-cost residual from solder/cutting pressure
E1 target hardware              REMAINS_JIT
direct exhaust hardware         MEASURE_ROUTE_BEFORE_SKU
```

No item should survive procurement merely because it appears on a conventional electronics-lab checklist. After checkout freeze, the next admissible information source is delivery/receipt Reality and E0-A→E0-E, not another category-completeness pass.
