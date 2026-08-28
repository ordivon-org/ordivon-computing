# Ordivon Laboratory F06 — Electronics and Embedded Instrumentation v0.1

Status: **CURRENT FAMILY AUDIT / FIRST PHYSICAL FALSIFICATION SUBSTRATE**  
Date: 2026-08-26  
Parent: `research/LABORATORY-PHYSICAL-FALSIFIER-MAP-20260826.md`  
Previous: `research/LABORATORY-F05-DEVICE-INTEROPERABILITY-IDENTITY-LIFECYCLE-20260826.md`  
Host continuity: `task:ordivon-laboratory-capability-atlas-20260826@15`

## 0. Referent

F06 asks:

> What minimum electronics/embedded instrumentation set gives Ordivon its first repeatable, independently checkable Physical Reality contact and enough compositional closure to execute E0-A..E0-E — without buying a traditional bench by category and without collapsing stimulus, observation, reference, power and control into one unchallengeable device?

F06 is the first family where exact products are allowed to re-enter the analysis, but only after capability derivation.

F06 is **not**:

- a professional electronics lab completeness list;
- a shopping exercise driven by instrument count;
- RF/high-voltage/power-electronics infrastructure;
- precision metrology theory (F12);
- motion/mechatronics (F09);
- general sensing (F07);
- fabrication beyond basic electronics fixture/rework support (F10);
- a license to treat an integrated instrument's internal readback as independent evidence;
- a decision to automate every instrument from day one.

## 1. F01–F05 inherited constraints

F06 cannot be designed in isolation.

### F01

First bench is a bounded low-energy work zone, not a dedicated laboratory room. No new circuit, rack, bench UPS, isolation transformer or special utility is currently earned.

### F02

E0 is hazard-reduction-first:

```text
low energy
+ source/fault limiting
+ no exposed mains
+ reachable manual de-energization
```

E-stop / safety PLC / safety relay are not earned for E0.

### F03

Use existing Workstation for reasoning/orchestration and local MCU/instrument hardware for deterministic IO/timing. Host hard real time, PLC and FPGA are not earned.

### F04

One experiment attempt may be one Runtime Job or a thin immutable attempt manifest across several native operations. No Experiment Service is required.

### F05

Use mature native device/provider interfaces and bind exact physical identity/attachment/provider realization. No Device Registry or universal lifecycle.

These constraints rule out a large amount of conventional bench-building by default.

## 2. E0-derived capability requirements

The physical falsifier campaign, not electronics tradition, determines the first requirements.

### E0-A — independent physical readback

Need:

```text
one bounded command/stimulus source
+ one independent physical observation path
+ raw result retention
```

The independent path must not merely read the command generator's own internal register/readback when PF-01 is the target.

### E0-B — passive electrical system identification

Need:

```text
bounded stimulus
+ two simultaneous analog observations on one acquisition clock
+ raw waveform export
+ adequate trigger/sample control
+ passive RC/RLC components/fixture
```

For the first RC/RLC scales, tens of MHz are unnecessary. Stable two-channel common-time acquisition matters more than headline bandwidth.

### E0-C — physical effect with lost response

Need:

```text
MCU/local controller
+ low-consequence persistent state
+ independent state observation
+ ability to intentionally break/lose response path
```

A relay/contact/indicator class effect is enough; motor/heater/high-current loads are rejected for the first test.

### E0-D — generation replacement

Need:

```text
at least two replaceable realizations of one cheap role
+ stable enough per-device identity evidence
+ re-enumeration/rebinding path
```

A pair of inexpensive MCU boards is an unusually high-value way to test this without buying duplicate oscilloscopes.

### E0-E — measurement adequacy / traceability discriminator

Need:

```text
measurement path A
+ sufficiently independent path B/reference/check
+ known target tolerance
+ later F12 qualification/uncertainty comparison
```

This does not require a metrology lab. It requires a second path whose failure mode is not identical to the first.

## 3. Minimum F06 capability families inside the family

The first F06 substrate needs only seven sub-capabilities.

### C1 — deterministic digital/controller stimulus

- bounded GPIO/trigger output;
- hardware-timed pulse/PWM/sequence where needed;
- firmware identity;
- USB/serial recovery/status;
- two physical instances desirable for E0-D.

### C2 — flexible analog stimulus

Useful for:

- system identification beyond one digital step;
- sine/sweep/chirp;
- impedance/network experiments;
- actuator/sensor excitation later.

Not strictly required for the cheapest E0-B if Pico digital step is sufficient, but high reuse value makes it an OWN-EARLY capability.

### C3 — two-channel common-clock analog observation

Required for E0-B's strongest timing simplification:

```text
observe actual input + actual output
on one sample clock
```

Target-relevant properties:

- >=2 analog channels;
- simultaneous/common acquisition timebase;
- raw samples export;
- trigger/configuration control;
- sufficient resolution/dynamic range for passive low-voltage circuits;
- documented automation/API.

### C4 — independent reference/check measurement

At least one physically independent voltage/resistance/continuity path.

Initial automation is optional.

Its scientific role is not high-rate waveform capture; it is to challenge another instrument/control path.

### C5 — bounded power / fault-energy support

Need enough to power:

- Pico/controller;
- passive/low-power circuits;
- relays/small sensor/logic modules later.

F02 specifically requires fault-energy limiting.

A supply without useful current limiting may still be used with deliberate series resistance/fusing for E0, but should not be mistaken for a general current-limited bench source.

### C6 — digital observation/debug

Useful for:

- UART/SPI/I2C/protocol debugging;
- trigger/sequence verification;
- MCU/controller diagnosis;
- later sensor/actuator integration.

An integrated logic analyzer is enough initially; a high-end standalone logic analyzer is not earned.

### C7 — electronics fixture/rework basics

Need:

- solderless breadboard or stable prototyping substrate;
- jumper/wire set;
- resistor/capacitor assortment with known nominal values;
- basic connectors/headers;
- simple soldering/rework capability when F10/F06 pressure requires durable fixture;
- probes/leads/grabbers appropriate to low-voltage work.

A PCB mill, reflow oven or full rework station is not required for E0.

## 4. Product reality — 2026-08-26 current external cut

### 4.1 Digilent Analog Discovery 3

Current Digilent listing/specification:

```text
MSRP                       USD 379
analog inputs              2 differential
ADC resolution             14 bit
sample rate                up to 125 MS/s per channel
input range                ±2.5 V / ±25 V
scope bandwidth            9 MHz with flywires
                            30+ MHz with BNC adapter
analog outputs             2 × 14-bit AWG
AWG range                  ±5 V
AWG bandwidth              ~12 MHz with BNC adapter
Digital IO                 16 channels
programmable supplies      +0.5..+5 V and -0.5..-5 V
supply output              up to 800 mA or 2.4 W/channel with AUX,
                            whichever limit is reached first
software                   WaveForms Windows/macOS/Linux
SDK                        C/C++/Python and others
USB                         USB-C physical connector, USB 2.0 data
```

Current Singapore RS listing observed:

```text
S$650.27 excl. GST
```

Important F02 limitation:

The AD3 built-in supplies expose voltage and a **total power limit / protection system**, but current documentation does not present them as a normal per-channel programmable constant-current bench supply. For E0 fault-current limitation, use explicit source resistance/fusing/low-power topology or a genuinely current-limited external source when required.

AD3 power protection/eFuses and integrated readback improve robustness; they do not make its own supply readback an independent observer of itself.

Sources:
- https://digilent.com/shop/analog-discovery-3/
- https://files.digilent.com/datasheets/Analog-Discovery-3-Datasheet.pdf
- https://files.digilent.com/manuals/WaveForms/3.24.3/start10.html
- https://files.digilent.com/manuals/WaveForms/3.24.3/supplies10.html
- https://sg.rs-online.com/web/b/digilent/

### 4.2 Raspberry Pi Pico 2 / RP2350

Current official/local cut:

```text
CPU                         dual Cortex-M33 or Hazard3 @150 MHz
SRAM                        520 KB
flash                       4 MB on Pico 2
GPIO                        26 exposed multifunction GPIO
ADC                         12-bit ADC on RP2350, Pico exposes ADC-capable pins
PWM                         hardware PWM
PIO                         12 state machines
USB                         USB 1.1 host/device
SWD                         exposed debug port
RP2350 OTP                  includes pre-programmed unique device identifier
official starting list      USD 5
Element14 Singapore         S$6.80 excl GST / S$7.41 incl GST observed
production commitment       at least January 2040
```

This combination makes **two Pico 2 boards** unusually attractive: they cost little enough that replacement/generation testing is not an artificial expense, and RP2350 provides per-device identity material at silicon level.

Sources:
- https://www.raspberrypi.com/products/raspberry-pi-pico-2/
- https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf
- RP2350 OTP datasheet section on unique device identifier
- https://sg.element14.com/raspberry-pi/raspberry-pi-pico-2/mcu-board-rpi-pico-2-520kb-150mhz/dp/4531086

### 4.3 RIGOL DHO804

Current official cut:

```text
analog channels              4
vertical resolution          12 bit
bandwidth                    70 MHz
real-time sample rate        1.25 GSa/s
memory depth                 up to 25 Mpts
waveform capture rate        up to 1 Mwfms/s
interfaces                   USB + LAN + HDMI
remote control               USB-TMC / LAN / SCPI programming
US official listed price     USD 459
China official listing       around RMB 2,899 before/without temporary promos in observed cut
```

The DHO804 is much stronger than E0 strictly requires in bandwidth/depth/channel count, but its four independent analog channels, standalone hardware/UI, long memory and SCPI/USB/LAN control make it a strong **independent observer** and useful later E1/E7/E9 substrate.

Sources:
- https://www.rigolna.com/products/rigol-digital-oscilloscopes/dho800/
- https://www.rigol.com/intl/products/oscilloscope/DHO800.html
- DHO800 User Guide remote-control section

### 4.4 SIGLENT SDM3045X

Current official cut:

```text
reading resolution          4.5 digit / ~60–66k count family description
max reading rate            150 rdgs/s
DCV one-year accuracy       datasheet range-dependent; current 600mV/6V/60V rows
                            show ±(0.06% of reading + 8 counts)
functions                    DCV/DCI/ACV/ACI/R/Cap/Freq/Period/Temp etc.
interfaces                   USB Device + USB Host + LAN; GPIB optional on some listings
remote automation            SCPI
US official listed price     USD 399
```

The SDM3045X is a credible independent automated reference path with good F05 properties. But E0-A/B do not require 150 rdgs/s, network automation or a bench DMM. Its strongest early justification is **E0-E + F12 automation/repetition**, not first-contact waveform work.

Sources:
- https://siglentna.com/product/sdm3045x/
- https://www.siglent.com/na/products-overview/sdm3045x/
- https://int.siglent.com/u_file/download/23_02_21/SDM3045X_DataSheet_E04A.pdf

### 4.5 SIGLENT SPD3303X / SPD3303X-E

Current official cut:

```text
CH1                        32 V / 3.2 A
CH2                        32 V / 3.2 A
CH3                        2.5 / 3.3 / 5.0 V / 3.2 A
total power                220 W
outputs                    3 independently controlled / isolated family description
resolution                 1 mV / 1 mA (model-dependent display/spec distinction)
remote programming         SCPI / PC software
mains                      100/120/220/230 V compatible
retailer observed price    about USD 459 for SPD3303X-E in one current US listing
```

This is a capable long-lived bench supply, but its 220 W capability is far beyond E0 needs. F02's first principle is to **reduce available fault energy**, not maximize it. A large programmable supply is useful later when many low-voltage loads, sensors and E1 mechatronics appear, but it is not required for the first passive electrical falsifiers.

Sources:
- https://www.siglent.com/int/products-overview/spd3303x-x-e/
- https://int.siglent.com/u_file/download/22_11_25/SPD3303X_DataSheet_E03A.pdf

## 5. Capability fit against E0

### 5.1 Analog Discovery 3

| E0 need | AD3 fit | Caveat |
|---|---|---|
| bounded analog stimulus | **Excellent** | AWG and software-native |
| digital stimulus | **Excellent** | pattern/digital IO |
| two-channel common-clock observation | **Excellent** | exactly matches E0-B architecture |
| raw data / automation | **Excellent** | WaveForms SDK |
| logic/protocol debug | **Excellent** | 16 digital IO |
| low-power rails | **Good** | useful, but not a general CC bench supply |
| independent evidence path | **Weak by itself** | integrated stimulus/readback shares device/software failure domain |
| physical device identity | **Good candidate** | WaveForms SDK supports enumeration/device info; exact serial behavior to verify on real unit |
| future E1 force/position capture | **Good** | 2 analog channels may become limiting with multimodal capture |

Conclusion:

```text
AD3 = very high compositional closure
but not sufficient as the only epistemic observer
```

### 5.2 Pico 2

| E0 need | Pico 2 fit |
|---|---|
| deterministic step/pulse | **Excellent** |
| trigger output | **Excellent** |
| response-loss controller | **Excellent** |
| device replacement test | **Exceptional when buying two** |
| low-level protocol work | **Excellent** |
| analog measurement authority | **Poor / not primary** |
| independent reference | **No** |

Conclusion:

```text
2 × Pico 2 = highest information-per-dollar first purchase candidate
```

### 5.3 DHO804

| E0 need | DHO804 fit |
|---|---|
| two-channel common-clock capture | **Excellent** |
| independent observer from Pico/AD3 | **Excellent** |
| raw remote capture | **Excellent** |
| channel headroom | **Excellent** (4 ch) |
| stimulus | **None** |
| digital protocol debug | **Separate/option dependent** |
| portability/desk burden | **Moderate** |
| performance over E0 minimum | **Large** |

Conclusion:

```text
DHO804 = strongest early independent observer upgrade,
not required for the cheapest E0 start
```

### 5.4 SDM3045X

| E0 need | SDM3045X fit |
|---|---|
| independent DC/reference check | **Excellent** |
| resistance/continuity | **Excellent** |
| automated E0-E/F12 work | **Excellent** |
| waveform/system identification | **No** |
| standalone independence | **Excellent** |
| early utilization | **Moderate** |

Conclusion:

```text
SDM3045X = strong second-stage metrology/reference tool,
not a prerequisite for first E0-A/B
```

### 5.5 SPD3303X-E

| E0 need | SPD3303X-E fit |
|---|---|
| current-limited programmable power | **Strong** |
| multiple future rails | **Strong** |
| E0 passive RC power need | **Over-capable** |
| F02 low-energy-first philosophy | **Requires disciplined limits** |
| later E1 / sensor/actuator use | **High future value** |

Conclusion:

```text
SPD3303X-E = OWN-EARLY/LATER when repeated powered-load pressure appears,
not a first-contact requirement
```

## 6. Integrated versus independent bench architectures

### Architecture A — compact integrated core

```text
2 × Pico 2
+ Analog Discovery 3
+ independent simple DMM/reference
+ passive components/fixture
```

**Strengths**

- lowest apparatus burden for E0-A..E0-E;
- extremely high compositional closure;
- AWG + scope + logic + digital + supply in one SDK;
- ideal for Agent-driven scripting;
- small physical footprint;
- fast experiment formation;
- inexpensive duplicate controller identity test.

**Weaknesses**

- AD3 stimulus + observation share hardware/software failure domain;
- only two analog channels;
- modest flywire bandwidth and buffer relative to benchtop scope;
- its supply is not the same thing as a full programmable CC bench PSU;
- integrated convenience can hide dependence if F05/F14 provenance is sloppy.

### Architecture B — independent benchtop observer first

```text
2 × Pico 2
+ DHO804
+ simple independent DMM
+ low-voltage power source / explicit limiting
+ passive components
```

**Strengths**

- DHO804 gives a strong standalone observer independent of controller;
- four channels leave much more room for E1/multimodal electrical observations;
- long memory / high sample rate / SCPI/LAN/USB;
- evidence path is less coupled to stimulus source.

**Weaknesses**

- flexible analog stimulus missing unless Pico approximations or later AWG added;
- logic/protocol instrumentation less unified;
- higher desk footprint;
- more separate adapters/software over time;
- first E0 does not need 70 MHz/1.25 GSa/s.

### Architecture C — compact core + independent benchtop observer

```text
2 × Pico 2
+ Analog Discovery 3
+ DHO804
+ simple DMM/reference
```

**Strengths**

- strongest first physical falsification substrate;
- AD3 can be stimulus/logic/flexible exploratory tool;
- DHO804 can be independent four-channel observer;
- same stimulus can be observed by both for cross-instrument evidence;
- substantial future headroom.

**Weaknesses**

- buys more than the cheapest E0 requires;
- cost roughly doubles observer instrumentation;
- may delay learning whether AD3-only + simple independent reference was already sufficient.

### Architecture D — conventional full bench immediately

```text
DHO804
+ SDM3045X
+ SPD3303X-E
+ separate AWG
+ MCU/debug tools
+ logic analyzer
```

**Strengths**

- professional familiar form;
- independent instruments;
- durable specialized capabilities.

**Weaknesses**

- highest cost/space/software burden;
- several devices underutilized by E0;
- much larger maintenance/currentness surface;
- violates capability-pressure sequencing;
- does not inherently produce stronger epistemology unless independence is deliberately designed.

Current disposition:

```text
D = REJECT NOW
```

## 7. Strongest current first-stage recommendation

F06 currently favors a **two-layer architecture**:

```text
Layer 1 — compositional exploration core
2 × Pico 2
+ Analog Discovery 3

Layer 2 — independent reference path
one physically independent DMM / reference meter
```

This is stronger than AD3 alone and cheaper/smaller than a full traditional bench.

### Why two Pico 2 boards?

Because the second board is not a spare in the ordinary sense. At Singapore observed pricing it adds very little cost while directly enabling:

- PF-06 same-role/different-generation test;
- F05-F1 replacement;
- F05-F2 re-enumeration comparison;
- firmware-version/currentness tests;
- controller failure/recovery experiments;
- later independent trigger/controller roles.

This is a rare case where intentional duplication is justified by experimental discriminability.

### Why AD3 first?

Because one small device materially creates:

```text
analog stimulus
+ common-clock two-channel observation
+ digital IO
+ logic analysis
+ protocol analysis
+ raw-data automation
+ low-power supplies
```

and therefore can execute much of E0 immediately.

It also matches F03's strategy of keeping host non-real-time while using instrument hardware timebases.

### Why an independent DMM/reference path at the same stage?

Because AD3 alone is too self-referential for several of the claims we explicitly want to attack.

The independent reference path can test:

- AD3 supply/output versus external voltage reading;
- resistor nominal/actual values;
- continuity/wiring state;
- Pico GPIO/static output state;
- measurement adequacy disagreements.

A battery-powered/manual DMM can actually be **more epistemically independent** than another PC-controlled instrument for the first falsifier, even if it is less automatable.

## 8. Exact DMM decision — defer one layer, not the capability

F06 can already say:

```text
independent DMM/reference capability = EARNED
```

but does not yet need to choose:

```text
handheld DMM
vs
SDM3045X benchtop DMM
```

### Handheld/manual path is favored if

- the first use is occasional reference/check;
- independence from PC/software is valuable;
- budget/space should stay minimal;
- E0-E automation is not yet repeated.

### SDM3045X is favored if

- E0-E/F12 is promoted immediately;
- automated logging/repetition is frequent;
- LAN/USB/SCPI integration is useful;
- a stable bench reference path has many later consumers.

Thus SDM3045X remains a **strong OWN-EARLY candidate**, not a first-contact prerequisite.

## 9. DHO804 promotion rule

DHO804 should move from `DEFER` to `OWN-EARLY` when any of the following becomes true:

1. AD3's two analog channels constrain a real E1/F07 experiment;
2. 9 MHz flywire / 30+ MHz BNC AD3 bandwidth is insufficient for a target;
3. long-memory acquisition or standalone UI materially improves recovery/inspection;
4. a second independent waveform observer changes scientific confidence/action;
5. Agent/SDK independence requires a standalone instrument failure domain;
6. current Singapore/local pricing makes the incremental cost unusually favorable and F06/F07 backlog has several consumers.

It should **not** be bought only because four channels/70 MHz look professional.

## 10. SPD3303X-E promotion rule

A true bench supply becomes earned when:

- powered circuits/sensors are repeated consumers;
- F02 needs explicit programmable current limit rather than passive source resistance;
- E1 actuator/sensor rails need stable separate outputs;
- experiments need supply sequencing/logging;
- AD3's ±5 V / power limits constrain the target;
- one supply can replace multiple improvised adapters/battery sources and reduce identity/recovery ambiguity.

At that point SPD3303X-E class is strong because it is programmable, multi-channel and future-proof.

But the first E0 RC experiment can intentionally use:

```text
Pico/AD3 low-voltage source
+ series resistance / small-energy topology
```

which is safer and more discriminating.

## 11. AWG decision

No standalone AWG is currently earned.

Why:

- AD3 already provides two analog waveform outputs;
- Pico provides deterministic digital stimulus;
- E0-B first system identification can use a step/pulse;
- DHO804 observer-first architecture could still use Pico for the earliest tests.

Promote a standalone AWG only when:

- voltage/frequency/output-drive constraints block real experiments;
- isolation/reference characteristics matter;
- multi-channel phase-coherent generation beyond AD3 is required;
- instrument-native sweep/burst/modulation becomes a repeated consumer.

## 12. Logic analyzer decision

No standalone logic analyzer is currently earned.

AD3's 16 digital IO/logic/pattern/protocol capability plus Pico local logging covers early embedded pressure.

Promote Digital Discovery / Saleae / other dedicated logic tool only when:

- channel count;
- long digital capture;
- 100+ MHz digital timing;
- protocol-decoder depth;
- concurrent analog+digital constraints

produce a real failure.

## 13. Debug probe decision

Pico 2 supports drag-and-drop USB programming and exposes SWD.

For E0, a dedicated debug probe is not mandatory if firmware remains simple and observable over USB/serial.

Promote an SWD debug probe when:

- controller reset/fault diagnosis is materially blocked;
- boot/reset-cause experiments require debugger access;
- firmware development rate makes printf/serial diagnosis inefficient;
- recovery requires exact low-level memory/register inspection.

Again:

```text
debug capability path = preserved
exact probe purchase = conditional
```

## 14. Prototyping / passive component set

This is one area where inexpensive breadth creates immediate experiment generativity without major maintenance burden.

### OWN/NOW minimum

- quality solderless breadboard(s) for E0;
- jumper wires / short solid-core wire;
- grabbers/alligator leads as appropriate;
- resistor assortment emphasizing common E-series values;
- capacitor assortment emphasizing pF/nF/µF passive RC ranges;
- LEDs + small signal diodes/transistors where useful;
- a few low-power relays/latching mechanisms only after E0-C exact design;
- pin headers/connectors;
- USB cables appropriate to Pico/AD3;
- simple storage/labeling from F01.

### Component quality rule

E0-E specifically needs to distinguish nominal from measured values. Therefore cheap assortments are acceptable as DUTs, but a small subset of known/reference components should have sufficiently documented tolerance/stability for the target comparison.

## 15. Soldering/rework

A soldering iron/station is **OWN-EARLY**, not strictly required before the first breadboard E0-A/B.

It becomes earned quickly because:

- Pico header variants / fixture connectors;
- stable low-noise wiring;
- repeatable relay/fixture construction;
- strain relief;
- sensor integration;
- F10 fixture work

will outgrow loose breadboards.

The first soldering capability does not imply hot-air/BGA/reflow infrastructure.

## 16. Independence matrix

A crucial F06 design criterion is **failure-domain diversity**, not just instrument count.

| Pair | Hardware independence | Software/provider independence | Timebase independence | Best use |
|---|---:|---:|---:|---|
| AD3 AWG → AD3 Scope | Low | Low | shared | efficient system ID / same-clock capture |
| Pico → AD3 Scope | Medium-high | High | observer owns timebase | command vs realized stimulus |
| AD3 supply → AD3 readback | Low | Low | n/a | internal operational monitoring |
| AD3 output → handheld DMM | High | High | n/a | static independent check |
| Pico → DHO804 | High | High | scope timebase | strong independent physical observer |
| AD3 AWG → DHO804 | High | High | independent | cross-instrument waveform validation |
| DHO804 ↔ SDM3045X | High | Medium-high | independent | dynamic vs static/precision cross-check |

This is why the ideal first bench is not either “all-in-one” or “all-independent”. It uses both strategically.

## 17. E0 mapping to recommended first substrate

Assume:

```text
2 × Pico 2
+ AD3
+ independent DMM/reference
+ passive/prototyping kit
```

### E0-A

```text
Pico output command
→ DMM static readback
or
→ AD3 scope independent of Pico
```

PF-01 can be tested without trusting Pico acknowledgement.

### E0-B

```text
Pico or AD3 stimulus
→ AD3 Ch1 measures actual input
→ AD3 Ch2 measures actual output
→ same acquisition clock
```

### E0-C

```text
Pico A controls low-energy persistent state
→ host response path deliberately lost
→ AD3/DMM independently observes final state
```

### E0-D

```text
Pico A bound as controller
→ replace with Pico B
→ same logical role
→ new physical/attachment/firmware evidence
```

This is directly enabled by buying two inexpensive boards.

### E0-E

```text
AD3 voltage/resistance-derived path
versus
independent DMM/reference
```

Later promote SDM3045X if automation/metrology repetition earns it.

## 18. Why AD3 + DHO804 should not be bought automatically together

The combination is attractive and technically strong, but PPD asks whether the extra observer changes an action now.

First run E0 with:

```text
Pico + AD3 + independent static reference
```

Then ask:

- Did two channels limit the experiment?
- Did AD3 bandwidth/depth limit the experiment?
- Did integrated failure-domain coupling leave a consequential ambiguity?
- Did an external waveform observer change a diagnosis?

If yes, DHO804 becomes earned with **direct evidence**.

If no, defer it until E1/F07/F09 creates pressure.

This makes the eventual DHO804 purchase more defensible, not less likely.

## 19. Why SDM3045X and SPD3303X-E are different from “nice-to-have”

Both have strong eventual roles:

### SDM3045X

Likely future carrier for:

- F12 metrology/calibration checks;
- automated DC/resistance/temp logging;
- long-duration sensor/reference work;
- independent evidence path;
- E0-E repetition.

### SPD3303X-E

Likely future carrier for:

- E1 sensors/actuators;
- multi-rail embedded systems;
- current-limited fault experiments;
- power sequencing;
- repeatable programmable supply conditions.

They are **deferred because their consumer set is not yet active**, not because they are bad purchases.

## 20. Approximate first-stage cost envelope — current public prices only

Prices are volatile and regional; this is not a purchase quote.

### Minimal controller layer

```text
2 × Pico 2 in Singapore
≈ 2 × S$7.41 incl GST at observed Element14 listing
≈ S$14.82
```

### AD3 layer

```text
US MSRP               USD 379
Singapore RS observed S$650.27 excl GST
```

### Optional second-stage benchtop instruments

```text
DHO804 official US       USD 459
SDM3045X official US     USD 399
SPD3303X-E observed US   ~USD 459 retailer cut
```

The point is not currency optimization; it is that one immediately buying all three benchtop instruments would add roughly another USD 1.3k class before accessories/shipping/tax, while most first E0 capability already exists in the compact layer.

## 21. F05 interoperability scorecard

### Analog Discovery 3

**Strong**

- WaveForms cross-platform application;
- documented SDK with Python/C/C++ paths;
- device enumeration/info APIs;
- raw waveform access;
- queryable instrument config;
- stable product ecosystem.

**Watch**

- exact per-unit serial/physical identity behavior should be captured on the real unit;
- USB/provider reconnect semantics must be tested;
- one integrated device can become a hidden single failure domain.

### Pico 2

**Strong**

- open SDK/docs;
- USB/SWD;
- RP2350 per-device identity material;
- firmware fully under our control;
- cheap duplicate generation.

**Watch**

- USB serial identity should be deliberately configured/bound rather than inferred from COM number;
- firmware reset/boot identity must be explicit for F03/F05 recovery.

### DHO804

**Strong**

- USB-TMC + LAN remote control;
- SCPI programming guide;
- standalone local UI;
- serial/device identity expected in instrument identification path;
- four-channel independent observer role.

### SDM3045X

**Strong**

- USB/LAN;
- SCPI;
- raw/logged measurement path;
- mature DMM semantics;
- independent standalone operation.

### SPD3303X-E

**Strong**

- remote programming/SCPI;
- explicit output channels/modes;
- future power-sequencing automation.

**Watch**

- firmware/hardware revision compatibility matters: current Siglent support pages show hardware-version-specific firmware constraints for some SPD3303X-E revisions. F05 generation binding is therefore directly relevant.

## 22. Physical falsifiers for F06 itself

### F06-F1 — integrated-only evidence insufficiency

Run E0-A using AD3 output and AD3 internal/readback only, then add an independent DMM/observer.

If the independent path can expose a discrepancy or materially alter confidence/action, retain the requirement for an independent reference path.

### F06-F2 — Pico-only stimulus sufficiency

Run the first E0-B with Pico hardware-timed step and AD3 two-channel capture.

If this fully discriminates the target models, a standalone AWG remains unearned despite AD3's AWG being available.

### F06-F3 — DHO804 deletion

Run E0-A/B/E using compact layer plus independent static reference.

If no target decision is blocked by channel count/bandwidth/independent waveform failure domain, DHO804 remains deferred.

### F06-F4 — SDM3045X deletion

Run E0-E with a credible independent manual DMM/reference.

If repetition/uncertainty/automation burden remains low, SDM3045X remains deferred.

### F06-F5 — bench PSU deletion

Run E0-A/B/C with low-energy source plus explicit passive current/fault limiting.

If all F02 envelopes are satisfied and no powered-load experiment is blocked, SPD3303X-E remains deferred.

### F06-F6 — dual-Pico generation test

Bind Pico A as `controller`, execute and retain evidence; replace with Pico B while keeping the logical role.

Old exact binding must not silently revive.

### F06-F7 — host/provider loss

During a bounded controller/instrument run, perturb/lose host/provider transport where safe.

Verify:

- local deterministic action behaves as designed;
- effect uncertainty is reconciled;
- raw device evidence survives where native hardware supports it;
- no blind replay occurs.

### F06-F8 — independent waveform observer promotion

Later compare AD3-measured waveform against DHO804 or equivalent independent scope under the same stimulus.

If disagreements expose an otherwise hidden apparatus/software limitation, the second scope has proven epistemic value rather than prestige value.

## 23. OWN / EARLY / DEFER disposition

| Capability / item class | Current disposition | Reason |
|---|---|---|
| 2 × Pico-2-class controllers | **OWN / FIRST** | E0 timing + response-loss + replacement at negligible cost |
| AD3-class integrated mixed-signal instrument | **OWN / FIRST STRONG CANDIDATE** | highest E0 compositional closure per device |
| independent DMM/reference path | **OWN / FIRST** | necessary independent evidence family; automation optional |
| passive components / breadboard / leads | **OWN / FIRST** | actual DUT/fixture substrate |
| basic soldering capability | **OWN-EARLY** | stable fixtures soon, but not prerequisite for first breadboard run |
| DHO804-class 4ch scope | **OWN-EARLY / CONDITIONAL** | independent waveform observer + future channel headroom |
| SDM3045X-class bench DMM | **OWN-EARLY / CONDITIONAL** | F12/E0-E automation/metrology repetition |
| SPD3303X-E-class bench PSU | **DEFER UNTIL POWERED LOAD PRESSURE** | E0 does not need 220 W; F02 favors low energy |
| standalone AWG | **DEFER** | AD3/Pico already cover current stimulus pressure |
| standalone logic analyzer | **DEFER** | AD3/Pico cover current digital pressure |
| SWD debug probe | **CONDITIONAL** | buy when firmware diagnosis becomes blocked |
| electronic load | **DEFER** | no current power-system consumer |
| RF generator/analyzer | **DEFER** | no RF consumer |
| high-voltage probes/supplies | **DEFER / SHARED-FIRST** | no current hazard/domain pressure |

## 24. First procurement gate — what must be checked before actual order

F06 is now close enough that exact procurement could begin, but not every item has equal maturity.

### For Pico 2

Verify:

- exact non-wireless/header variant desired;
- whether pre-soldered headers reduce first-day friction;
- two distinct physical units available;
- USB cable/connector compatibility with current workstation;
- simplest firmware toolchain path on Windows/WSL.

### For AD3

Verify:

- authorized Singapore distributor stock/landed price;
- whether standard flywires are sufficient for E0 (likely yes);
- BNC adapter is **not** required for low-frequency E0 unless probe mechanics/grounding justify it;
- auxiliary 5V/4A supply is not needed until output-power use earns it;
- exact WaveForms/WaveForms SDK Windows/WSL integration path;
- per-unit serial/device enumeration behavior.

### For independent DMM

Before selecting exact product, define the first E0-E/F12 tolerance target.

Do not buy precision digits without a required uncertainty target.

### For passive kit

Choose quality enough that poor contacts do not dominate the first experiment, but preserve inexpensive interchangeable DUTs for fault/replacement tests.

## 25. The first actual E0 physical configuration

The current preferred first contact can be extremely small:

```text
Pico A
  GPIO step/trigger
      ↓
passive RC network
      ↓
AD3 Ch1 = actual input
AD3 Ch2 = actual output
      ↓
raw waveform artifact
```

plus:

```text
independent DMM
→ measure resistor / supply / static endpoint
```

and later:

```text
Pico A → Pico B replacement
```

This setup is enough to attack a surprisingly large set of existing Ordivon standings without pretending it is a complete Laboratory.

## 26. Positive capability language

### Mixed-Signal Reality Contact Capability

Ordivon can create bounded electrical stimuli and capture actual multi-channel physical responses on a known acquisition timebase.

### Independent Electrical Adjudication Capability

Ordivon can challenge one controller/instrument path with a physically independent measurement route rather than trusting self-report.

### Embedded Physical Control Capability

Ordivon can delegate deterministic physical IO to cheap replaceable MCU generations while retaining exact firmware/device evidence and recovery semantics.

### Rapid Experimental Composition Capability

One compact mixed-signal instrument plus a controller and passive fixture can be recomposed into oscilloscope, AWG, logic/protocol, network-analysis and impedance-style experiments without purchasing one appliance per label.

### Instrument Escalation Capability

When compact instrumentation becomes insufficient, Ordivon has explicit evidence-based promotion paths to independent scope, DMM, bench supply, logic analyzer, AWG and later specialized equipment.

This is positive infrastructure construction without equipment accumulation for its own sake.

## 27. F06 standing

### Current strongest first substrate

```text
2 × Raspberry Pi Pico 2-class controllers
+ Analog Discovery 3-class mixed-signal instrument
+ one independent DMM/reference path
+ passive/prototyping essentials
```

This is the leading **first Physical Falsification Substrate**.

### Strong candidate, not immediate prerequisite

```text
RIGOL DHO804-class independent 4-channel scope
```

Promote after compact substrate demonstrates a real channel/bandwidth/independence residual, or if budget preference intentionally values future headroom enough to accept early ownership.

### Early future tools

```text
SDM3045X-class bench DMM
SPD3303X-E-class programmable current-limited supply
```

are credible future core instruments, but should be admitted by F12/F07/F09 powered-load pressure rather than purchased as a traditional bench bundle now.

### Strongest anti-overbuild conclusion

The first electronics laboratory does **not** need:

```text
scope + DMM + PSU + AWG + logic analyzer + electronic load + FPGA + PLC
```

as seven separate appliances.

It needs:

```text
high compositional closure
+
independent evidence path
+
replaceable deterministic controller
+
low-energy physical DUTs
```

That is the actual capability shape revealed by E0.

## 28. Next family boundary

F07 — General Sensing and Measurement Acquisition should now start from a much stronger base.

F06 owns generic electrical stimulus/observation infrastructure.

F07 should ask:

```text
Which non-electrical physical quantities become observable through transducers?
Which sensor modalities are universal enough to own early?
Which are cheap Pods?
When is sensor output merely an indication versus a measurement?
How should force, displacement, temperature, IMU, light, sound and pressure enter the same evidence discipline without creating a Sensor Registry?
```

F07 should consume AD3/MCU/DAQ paths where suitable rather than buy one dedicated logger for every modality.
