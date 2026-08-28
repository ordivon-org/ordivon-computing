# Ordivon Laboratory — Physical Falsifier Map v0.1

Status: **CURRENT WORKING RESEARCH / PHYSICAL-PRESSURE ADMISSION SURFACE**  
Date: 2026-08-26  
Host continuity: `task:ordivon-laboratory-capability-atlas-20260826@9`  
Source fence: `ordivon-computing@561ce47fc5c57b6f8d164a68f896f4757a31e4be` plus current owner-source audits listed below.

## 0. Purpose and claim ceiling

This document does **not** create a Laboratory semantic owner, universal Experiment object, Device registry, Sample registry, Measurement service, Safety owner, or procurement roadmap.

Its purpose is narrower:

> For already-established Ordivon standings that become materially consequential in physical Reality, identify the strongest existing evidence, subtract mature external mechanisms, identify the missing Ordivon-native physical evidence, and name the cheapest independent physical discriminator that could falsify or narrow the standing.

The workflow is:

```text
existing Standing
→ strongest current internal evidence
→ strongest mature external baseline
→ exact missing physical evidence
→ cheapest admissible independent discriminator
→ falsification / narrowing condition
→ only then capability / apparatus pressure
```

This reverses procurement-first planning:

```text
buy instrument
→ find a use
```

is rejected in favor of:

```text
claim remains physically under-tested
→ discriminating Reality pressure identified
→ apparatus requirement derived
→ mature/shared/owned carrier compared
```

## 1. Current source / owner cut

Current source revalidation used in the 2026-08-26 Physical Reality Validation Audit:

- Computing: `561ce47fc5c57b6f8d164a68f896f4757a31e4be`
- World: `9aa2b82a2273a1e011f74bcf6e2a436536c8d504`
- Interlocus: `2da7eb39554fb47f4ab2ef2b26e8b72b5b3ae05c`
- Security: `63f0636aca579ce95df0ff3c34713fe00e8cba5d`
- SCD: `ff793dcf1a5c98552094a906abb97d95ef1ac1da`
- Computational Possibility: `73fee950832c0c91a4a9f74b7196f3811903b219`
- current Workstation observation cut opened from current `main` during the audit.

Important owner subtraction already established:

```text
World
  owns bounded external Reality / consequence / observation-currentness semantics

Interlocus
  owns qualified cross-locus capability / binding / realization / serviceability

Runtime
  owns durable admitted physical execution / Job / Attempt / Artifact evidence

Workstation
  owns one node's local substrate / ToolBinding / future narrow attachment realization

SCD
  owns computational-description semantics, not physical realizability

Computational Possibility
  owns regime-relative computational possibility, not physical realizability

Security
  owns security/adversarial truth where applicable, not general machine safety

Laboratory
  currently owns no semantic truth because no global Laboratory owner is admitted
```

## 2. Temporary evidence ladder for this audit

This is an **audit projection only**, not a persisted ontology.

```text
V0  conceptual / standing only
V1  Ordivon software, synthetic or controlled digital evidence
V2  strong mature external physical / scientific / standards evidence
V3  Ordivon natural physical event or real external consequence
V4  Ordivon controlled physical experiment
    + independent observation
    + declared measurement procedure / provenance
    + explicit falsifier
V5  heterogeneous physical recurrence / later reuse / replacement transfer
```

Current overall shape:

```text
V0/V1 = dense
V2    = strong across many seams
V3    = real but sparse
V4/V5 = major gap
```

Therefore the present Laboratory research frontier is not general theory expansion. It is **physical adjudication density**.

## 3. PPD admission contract for physical tests

A candidate physical test is admitted only if it answers all of the following.

### Problem

Which exact standing or decision remains under-constrained?

### Pressure

What two or more action-distinct physical worlds remain compatible with current evidence?

### Prior subtraction

Can mature metrology, controls, device middleware, simulation, external facility access, or a simpler owner-local mechanism already answer the question?

### Discriminator

What is the cheapest observation/intervention that separates the rival worlds?

### Independence

Is the discriminator sufficiently independent of the mechanism whose claim is being tested?

### Effect boundary

Could the probe itself create a consequential physical state? If yes, what prevents blind retry or unsafe continuation?

### Measurement validity

What procedure, reference, calibration/validation, timing and influence conditions are necessary for the result to bear on the target claim?

### Falsifier

What observation would actually weaken, narrow or reject the candidate standing?

### Stop rule

If the mature baseline already resolves the decision, or the experiment cannot discriminate the hypotheses, stop. More equipment is not an identification method.

## 4. External mature baseline — current subtraction

The following external systems are treated as mature carriers / constraints, not novelty targets.

### Modular autonomous laboratories — NIST

NIST's current modular-autonomous-laboratory programme separates standardization pressure into:

1. sample management;
2. instrument control and communication;
3. data and knowledge management;
4. algorithm and model integration.

It also states that materials R&D still lacks a standardized autonomous-experimentation ecosystem. The key transfer is **modularity + standards + off-the-shelf components**, not one bespoke Laboratory control plane.

Source: https://www.nist.gov/programs-projects/development-standards-support-modular-and-autonomous-laboratory-ecosystem

### Device identity versus function — OPC UA LADS

LADS explicitly separates a Hardware View from a Functional View. Hardware carries device/component/nameplate/installation/condition/calibration/validation concerns; the Functional View models functions, sensors, controllers, actuators and programs.

Transfer:

```text
physical identity / attachment
!=
functional capability
```

Source: https://reference.opcfoundation.org/specs/OPC-30500-1/4.1

### Feature-oriented interoperability — SiLA 2

SiLA 2 is HTTP/2 based and emphasizes functionality rather than device type. Servers expose Features; Features expose Commands and Properties. Feature evolution can occur independently of one fixed device taxonomy.

Transfer:

```text
consumer-needed feature surface
>
universal device-class ontology
```

Source: https://sila-standard.com/standards/

### Hardware abstraction / scientific plan separation — Ophyd / Bluesky

Ophyd provides hardware abstraction over underlying control protocols through Devices/Signals and semantic read/set/trigger/configuration interfaces. Bluesky Plans and RunEngine operate above that hardware abstraction.

Transfer:

```text
device adapter
!=
scientific plan
!=
execution lifecycle
!=
measurement/evidence interpretation
```

Source: https://blueskyproject.io/ophyd/architecture.html

### Managed hardware lifecycle — ROS 2 / ros2_control

ros2_control explicitly manages hardware component lifecycle and command/state interfaces. A process or endpoint being reachable is not equivalent to a component being configured/active/admissible.

Transfer:

```text
process alive
!=
hardware active
!=
action safe/admissible
```

Source: https://docs.ros.org/en/ros2_packages/rolling/api/hardware_interface/doc/hardware_interface_types_userdoc.html

### Metrology — BIPM VIM

Metrological traceability belongs to a **measurement result** and relates it to a reference through a documented unbroken calibration chain in which each calibration contributes uncertainty. Traceability alone does not prove the uncertainty is adequate for a particular use or that mistakes were absent.

Transfer:

```text
instrument reading
!=
measurement result

traceable
!=
fit for this target
```

Sources:
- https://jcgm.bipm.org/vim/en/2.41.html
- https://jcgm.bipm.org/vim/en/2.42.html

### Autonomous-laboratory safety

Current SDL safety research explicitly argues that safe robots/instruments alone are insufficient: AI-generated intent must be transformed into executable experiments, monitored actions and trustworthy evidence through an autonomy safety harness.

Transfer:

```text
Agent intent
!=
physical safety authorization
```

Source: https://www.nature.com/articles/s44160-026-01120-6

### Provenance-complete experimentation

Current SDL review literature identifies scalability, generalizability and provenance-complete experimentation as interdependent requirements for the next phase of autonomous laboratories.

Transfer: Ordivon's existing Runtime / Harness / Host / Atlas evidence boundaries are plausible reusable substrate, but this must still be tested on physical measurement and object continuity.

Source: https://www.nature.com/articles/s41570-026-00847-2

## 5. Claim-level Physical Falsifier Map

### PF-01 — Reported state is not physically realized state

**Existing standing**

```text
reported / controller / software state
!=
physically realized state
```

**Current Ordivon evidence**

- Runtime/World effect separation;
- real 2026-08-25 display-power incident gave natural physical mitigation/path-replacement evidence;
- Security has real host/KVM/network-namespace effects whose control-state and substrate-state can diverge.

**Missing evidence**

A controlled physical test in which controller-reported success and independently observed physical state deliberately diverge.

**Cheapest discriminator**

Low-voltage commanded output with an independent electrical observer. Example: controller commands a line/state; separate acquisition measures the actual voltage/current/response.

**Falsifies/narrows if**

Across strong heterogeneous cases, controller/report state plus existing software telemetry always predicts the target physical state sufficiently for the relevant decisions, and independent observation never changes a decision or failure diagnosis.

**First candidate**: E0-A.

---

### PF-02 — Instrumentation can change reachable discriminability

**Existing standing**

Instrumentation may be a capability variable because it can alter the evidence space available to a finite observer.

**Current evidence**

- strong Representation results in software;
- Computer-to-Reality world-model revision;
- mature external scientific practice.

**Missing evidence**

Same physical Reality + same Agent/model + same prior information, with and without one independent physical measurement channel.

**Cheapest discriminator**

Hide one parameter/fault in a simple electrical network; compare diagnosis/model selection with software/control telemetry only versus telemetry + independent analog measurement.

**Falsifies/narrows if**

The extra physical measurement channel adds no reliable hypothesis discrimination, action-selection or recovery advantage across appropriately chosen cases.

**First candidate**: E0-B.

---

### PF-03 — Evidence production is a distinct capability from evidence retrieval

**Existing standing**

A system able to choose and realize a discriminating observation/intervention may possess a capability unavailable to a passive information consumer.

**Current evidence**

PPD and world-model research support the distinction, while active diagnosis and SDLs provide mature external examples.

**Missing evidence**

An Ordivon case where the required evidence does not already exist and a selected physical probe creates the distinction needed for a decision.

**Cheapest discriminator**

Present two model-equivalent passive observations but allow one bounded stimulus whose response separates the models.

**Falsifies/narrows if**

Strong passive historical/external evidence or an equally cheap mature carrier resolves the same decision, or probe selection adds no decision-relevant information.

**First candidate**: E0-B.

---

### PF-04 — Command / acknowledgement does not prove physical effect

**Existing standing**

```text
intent
!= dispatch
!= device acknowledgement
!= physical effect
```

**Current evidence**

Very strong digital/external-effect evidence from Runtime, Finance, World and Security.

**Missing evidence**

Controlled low-energy physical dispatch where acknowledgement can be decoupled from target physical consequence.

**Cheapest discriminator**

Controller toggles a physical output that drives an observable load; independently measure load-side state rather than relying on controller status.

**Falsifies/narrows if**

For the admitted operation class, controller acknowledgement is itself physically authoritative and independent observation adds no target-relevant distinction.

**First candidate**: E0-A; stronger in E1.

---

### PF-05 — Response loss after physical dispatch requires UNKNOWN + reconciliation

**Existing standing**

If a potentially effectful dispatch may have crossed the consequence boundary and the response is lost:

```text
missing response
!=
effect failed
```

Blind retry is invalid until the exact effect is reconciled.

**Current evidence**

Strong Runtime / Finance / World digital and external-service evidence.

**Missing evidence**

A controlled physical effect where the effect occurs but the response path is intentionally lost.

**Cheapest discriminator**

A low-energy persistent physical state (latching relay, mechanically displaced flag, retained actuator position, charged/discharged observable state) plus independent readback. Drop the controller response after dispatch and require recovery from Reality.

**Falsifies/narrows if**

The selected operation is intrinsically idempotent/reconcilable such that blind retry is safe under all target-relevant states; standing must then remain operation-class relative rather than universal.

**First candidate**: E0-C or E1.

---

### PF-06 — Same logical name does not imply same physical generation/binding

**Existing standing**

```text
same logical identity
!=
same physical generation
```

**Current evidence**

Strong Interlocus and Workstation currentness/binding research; real software/provider replacement cases.

**Missing evidence**

Physical device detach/re-attach/replacement under the same logical role.

**Cheapest discriminator**

Use two controller/sensor instances assigned the same logical experiment role; replace one between runs and require re-binding by serial/device evidence rather than name/path alone.

**Falsifies/narrows if**

The physical transport/device ecosystem already provides a stable identity primitive that makes replacement impossible to confuse for the target workload without extra Ordivon binding semantics.

**First candidate**: E0-D.

---

### PF-07 — Attachment / reachability / capability / serviceability are distinct

**Existing standing**

```text
attached
!= reachable
!= verified capability
!= serviceable for target
```

**Current evidence**

Strong Interlocus theory and Workstation vNext boundary; LADS/SiLA/ROS external support.

**Missing evidence**

A real attached device that is visible but not usable for the target because of wrong generation, mode, calibration, firmware, range, safety state or configuration.

**Cheapest discriminator**

Keep device enumeration constant while changing one target-relevant serviceability condition.

**Falsifies/narrows if**

A mature device substrate already exposes target-complete serviceability with sufficient authority/currentness, eliminating any Ordivon-specific residual.

**First candidate**: E0-D.

---

### PF-08 — Instrument indication is not yet a valid measurement result

**Existing standing**

A reading becomes scientific evidence only relative to procedure, device identity, reference/calibration/validation, units/range, uncertainty/quality, timing and relevant influence conditions.

**Current evidence**

Strong mature metrology; current Ordivon standing but no laboratory receipt.

**Missing evidence**

Same nominal indicated value produced under measurement conditions that imply materially different decision validity.

**Cheapest discriminator**

Measure a known resistance/voltage with two paths; intentionally include a range/reference/contact/configuration condition that changes uncertainty or validity while the displayed nominal result may remain plausible.

**Falsifies/narrows if**

The target experiment's tolerance is so loose that the omitted metrology coordinates provably cannot change the decision. Then those coordinates should not be universalized.

**First candidate**: E0-E.

---

### PF-09 — Traceability does not imply fitness for purpose

**Existing standing**

```text
traceable measurement
!=
adequate measurement for target decision
```

**Current evidence**

Directly supported by BIPM VIM.

**Missing evidence**

Ordivon-native decision where a traceable/valid measurement is still too uncertain, too slow, wrong-range or otherwise inadequate for the target.

**Cheapest discriminator**

Set a target tolerance narrower than one measurement path's justified uncertainty and wider than another's; require the consumer to distinguish `valid but inadequate` from `invalid`.

**Falsifies/narrows if**

No current Ordivon physical decision is sensitive to the difference; in that case retain external metrology only and avoid materializing extra structure.

**First candidate**: E0-E, possibly later.

---

### PF-10 — Physical capability does not mint authority or safety admission

**Existing standing**

```text
can physically do X
!=
may do X
!=
X is safe to do now
```

**Current evidence**

Strong Normative/Security/Runtime/Finance distinction; mature robotics/machine safety.

**Missing evidence**

A physical rig where an Agent/controller is capable and live but an independent interlock/safe-state condition blocks effect.

**Cheapest discriminator**

Low-energy actuator circuit with a hardware enable/interlock path independent of Agent/Runtime. Software requests action while hardware enable is open.

**Falsifies/narrows if**

The operation class is intrinsically non-hazardous and no independent safety invariant exists; do not invent a safety plane merely for symmetry.

**First candidate**: E1, not required for passive E0.

---

### PF-11 — Latent physical affordance is not realized current capability

**Existing standing**

```text
asset exists
or constructor exists
or supplier exists
!=
current target capability
```

**Current evidence**

Constructive Capability Environment and isolated-equipment research; current product/hardware inventory observations.

**Missing evidence**

Physical rematerialization/reconstruction after device removal, replacement or dormant storage.

**Cheapest discriminator**

Remove a small experiment attachment after successful use, preserve only reconstruction evidence, then later require a fresh Agent to rematerialize and re-qualify it.

**Falsifies/narrows if**

Keeping the capability continuously active is strictly cheaper/more reliable for the target usage pattern, or mature plug-and-play discovery makes reconstruction semantics trivial.

**First candidate**: later reuse of E0.

---

### PF-12 — External/shared capability can substitute ownership, but the substitution has a contract

**Existing standing**

Laboratory capability does not imply owned equipment. Remote/shared facilities, contract metrology/fabrication and cloud labs can provide real capability.

**Current evidence**

Strong external reality; Constructive Capability Environment explicitly preserves rent/buy/remote/fabricate as distinct realization routes.

**Missing evidence**

An Ordivon physical question executed once locally and once through a remote/shared carrier, comparing latency, observability, provenance, troubleshooting and re-entry.

**Cheapest discriminator**

A later calibration/fabrication/characterization task where both local and external routes are actually feasible.

**Falsifies/narrows if**

The external route preserves all target invariants with lower recurring cost; then ownership pressure disappears for that capability.

**First candidate**: not day-one E0.

---

### PF-13 — Provenance/re-openability must survive physical experimentation

**Existing standing**

A future consumer should be able to recover what was done, with which exact object/instrument/configuration, what was measured, and what remains uncertain without trusting a narrative summary.

**Current evidence**

Strong Runtime/Harness/Host/Atlas digital evidence architecture; provenance-complete experimentation is an external SDL priority.

**Missing evidence**

An actual physical run whose raw observations, configuration, device identity and transformations can be replayed/reinterpreted by a replacement Agent.

**Cheapest discriminator**

E0 run with immutable raw waveforms/readings, exact config manifest, instrument/controller identity and a later fresh-Agent reconstruction task.

**Falsifies/narrows if**

A mature lab data format/LIMS/ELN plus existing Ordivon references already provides complete recovery with no Ordivon-specific physical lineage requirement.

**First candidate**: mandatory part of E0.

---

### PF-14 — Physical object / sample / fixture continuity may be an independent engineering pressure

**Existing standing**

A physical object used across experiments may require recoverable identity, orientation, fixture, location, state and history relations.

**Current evidence**

Computer-to-Reality / physical-continuity standing; NIST identifies sample management/interchange as an active standardization gap.

**Missing evidence**

Same experiment identity with multiple physical specimens/fixtures, or same specimen moved across measurement contexts, where ambiguity changes the result/decision.

**Cheapest discriminator**

Two visually/nominally similar passive networks or compliant specimens with explicit labels/fixture generations; swap them under controlled conditions and test whether provenance/binding catches the substitution.

**Falsifies/narrows if**

Ordinary local labeling plus owner-native experiment records are sufficient across repeated heterogeneous workloads; then no shared object/sample carrier is earned.

**First candidate**: E0-D or E1.

---

### PF-15 — Experiment-valid does not imply world/scale-valid

**Existing standing**

```text
validated in this apparatus / scale / regime
!=
transported to another target Reality
```

**Current evidence**

Strong World/Standing Transport/PPD discipline and broad external scientific methodology.

**Missing evidence**

A later domain case where a result changes across scale, fixture, environment or population and the transport moderators matter.

**Cheapest discriminator**

Not forced into E0. Introduce only when a real domain experiment has a target beyond the bench.

**Falsifies/narrows if**

The target claim is explicitly apparatus-local; then no transport claim exists and extra scale evidence is unnecessary.

**First candidate**: future domain Pod.

---

### PF-16 — Composition is not automatically a new joint capability

**Existing standing**

A successful physical stack of sensor + actuator + controller + Agent + Runtime does not itself establish joint irreducibility/emergence.

**Current evidence**

Strong COJC subtraction discipline and multiple digital negative controls.

**Missing evidence**

A natural physical blocked outcome where the full composition succeeds, the strongest mature generic composition fails, an identifiable deletion exists, and an independent consequence changes.

**Cheapest discriminator**

Do not manufacture this in E0. Observe natural physical workloads and reopen only when a real residual appears.

**Falsifies/narrows if**

A mature generic control/measurement/workflow composition reproduces the effect under parity.

**First candidate**: natural-pressure only.

---

### PF-17 — True capability formation versus latent capability exposure remains open

**Existing standing**

Capability Dynamics leaves open whether an intervention forms a genuinely new target-relative capability or merely exposes/activates a capability latent in the existing system/environment.

**Current evidence**

Conceptual and digital bounded evidence; no decisive physical discriminator.

**Missing evidence**

A physical before/after intervention where candidate latent routes are carefully enumerated/subtracted and later target reachability changes in a way not reducible to visibility/access alone.

**Cheapest discriminator**

Not necessarily E0. First use E0/E1 to establish trustworthy physical capability measurement and reconstruction; only then design a dedicated capability-formation experiment.

**Falsifies/narrows if**

The apparent new capability is reproducible through an already-present route once access/search/representation is normalized.

**First candidate**: later dedicated experiment.

---

### PF-18 — Environment construction can alter future problem/action space

**Existing standing**

Deliberately changing the environment can change effective future capability and which distinctions/actions become reachable.

**Current evidence**

Constructive Capability Environment + Representation + Workstation/Finance cases; mature external apparatus/infrastructure examples.

**Missing evidence**

Controlled physical environment construction whose contribution survives strong mature-baseline subtraction and changes a target-relevant future experiment/action frontier.

**Cheapest discriminator**

A reconfigurable fixture or measurement attachment that makes previously non-identifiable physical hypotheses discriminable; compare against equivalent external/mature carriers.

**Falsifies/narrows if**

The same capability is reproduced by a pre-existing route or only convenience/latency changes while target reachability does not.

**First candidate**: E1 or later.

## 6. Candidate physical falsifier sequence

The sequence is selected for **information density and seam coverage**, not spectacle.

### E0-A — Independent physical readback

```text
controller command
→ physical output/load
→ independent observer
```

Primary pressure:
- PF-01 reported != realized;
- PF-04 acknowledgement != effect;
- PF-13 provenance.

Low hazard. Minimal theory burden.

### E0-B — Electrical system identification under hidden model difference

```text
known stimulus
→ hidden RC/RLC/passive network
→ independent input/output observation
→ model / parameter inference
→ prediction
→ repeated measurement
```

Primary pressure:
- PF-02 instrumentation/discriminability;
- PF-03 active evidence production;
- PF-08 measurement validity;
- PF-13 provenance.

### E0-C — Physical effect with lost response

Use a bounded persistent physical state so the effect can occur even if the controller response is intentionally dropped.

Primary pressure:
- PF-04;
- PF-05 UNKNOWN/reconciliation;
- PF-13.

### E0-D — Device/specimen generation replacement

Swap device or specimen while preserving a logical role/name.

Primary pressure:
- PF-06 generation/binding;
- PF-07 serviceability;
- PF-11 rematerialization;
- PF-14 object continuity.

### E0-E — Measurement adequacy / traceability discriminator

Compare two measurement paths or two procedure conditions whose nominal reading is plausible but whose uncertainty/fitness differs.

Primary pressure:
- PF-08;
- PF-09.

### E1 — Low-energy compliant electromechanical system

Actuator + compliant object + force/position/vision observation + independent stop/safe state.

Primary pressure:
- PF-01/PF-04/PF-05 under persistent motion;
- PF-10 physical safety/admission;
- PF-14 fixture/object continuity;
- PF-18 environment construction.

E1 is retained as the first **multi-physics** stress test, but E0 should precede it because E0 can isolate instrument/evidence/binding failures without mechanical confounding.

## 7. Relative experiment ranking

Ordinal ranking only; no false precision.

| Candidate | Information gain | Independence potential | Safety | Cost/setup | Reuse | Current disposition |
|---|---|---|---|---|---|---|
| E0-A independent readback | High | High | Very high | Very low | High | **FIRST** |
| E0-B system identification | Very high | High | Very high | Low | High | **FIRST** |
| E0-C response-loss physical effect | Very high | High | High | Low–medium | Very high | **EARLY** |
| E0-D generation replacement | High | High | Very high | Low | Very high | **EARLY** |
| E0-E measurement adequacy | High | Very high | Very high | Medium | Very high | **EARLY / after basic measurement path exists** |
| E1 compliant electromechanics | Very high | Very high | Medium–high if energy-limited | Medium | Very high | **AFTER E0** |
| dedicated true-capability-formation test | Potentially extreme | unknown | depends | high conceptual cost | high | **DEFER until measurement substrate is trustworthy** |

## 8. What the first physical bench must therefore enable

The Physical Falsifier Map does **not** yet name products. It derives capability requirements.

The first bench needs enough support to realize at least E0-A/B/C/D/E:

```text
bounded low-voltage stimulus
+ deterministic controller
+ independent analog observation
+ independent simple reference/check
+ raw time-series/readout capture
+ exact device/config identity
+ deliberate transport/response-loss injection
+ replaceable device/specimen identity
+ passive component/fixture construction
+ low-risk energy limitation
```

This is the reason an electronics/embedded first Pod remains attractive. It is not because electronics is intrinsically the most important science domain; it is because it is a **low-hazard, low-cost, high-discrimination physical carrier** for many existing Ordivon falsifiers.

## 9. Fifteen operational capability families for sequential expansion

The earlier Capability Atlas used 20 entries, but it mixed three different kinds of thing:

1. substrate/capability families;
2. cross-cutting constraints such as Security and Human/operator interface;
3. vertical scientific domains such as materials/chemistry and biology.

For sequential physical planning, normalize them into the following **15 operational families**. This is a planning projection, not semantic ownership.

### F01 — Facility, utilities and bench infrastructure

Space, mains distribution, grounding/ESD, lighting, storage, network, local environmental observation, basic utility discipline.

### F02 — Physical safety, authority and energy isolation

Energy limits, fusing, guarding, safe-state paths, E-stop/interlocks where applicable, manual recovery, hazard boundaries, safety authority independent of Agent/Runtime liveness.

### F03 — Compute, control, timing and low-level interfaces

General/edge compute, MCU-class controllers, buses/transports, timing, deterministic low-level control; FPGA/PLC/real-time descent only under pressure.

### F04 — Experiment orchestration and execution semantics

Experiment intent/plan, resource locking, run admission, lifecycle, pause/abort, response-loss handling, reconciliation, cleanup and replayable execution evidence above Runtime.

### F05 — Device interoperability, attachment, identity and lifecycle

Direct vendor/SCPI/USB/serial/TCP carriers; LADS/SiLA/EPICS/Ophyd/ROS as appropriate; attachment generation, driver/provider identity and device lifecycle without a universal device ontology.

### F06 — Electronics and embedded instrumentation

DMM/scope/logic observation, programmable low-voltage power, signal generation where needed, DAQ/ADC, soldering/rework, MCU programming/debugging and electronic load/RF only under pressure.

### F07 — General sensing and measurement acquisition

Temperature, force/load, displacement, encoder, IMU, light, sound, pressure, strain/resistance and other modular transducers; acquisition is not yet metrological validity.

### F08 — Imaging, optics and multimodal observation

Ordinary cameras, controlled lighting, fiducials and macro imaging first; depth/thermal/microscopy/high-speed/spectroscopy later or shared-first.

### F09 — Actuation, motion and mechatronics

Relays, servos, steppers, DC motors, small linear stages, pumps/valves and compliant mechanisms; robots/high-force/pneumatics only after safety and workload pressure.

### F10 — Fabrication, fixtures and reconfiguration

Hand tools, soldering, jigs, fixture-making, small additive manufacturing where justified; professional PCB/CNC/precision machining usually shared-first until repetition earns ownership.

### F11 — Sample / object handling, identity and physical logistics

Stable object/specimen identity, holder/fixture/orientation references, labeling, storage, location/state lineage and later automated handling where required.

### F12 — Metrology, calibration and reference chains

Measurement procedure, reference hierarchy, calibration/validation, uncertainty, influence quantities, time basis and fitness-for-purpose; external accredited calibration remains first-class.

### F13 — Environmental condition observation and control

Ambient temperature/humidity/light observation first; thermal/humidity/acoustic/vibration/vacuum/inert-gas/pressure/clean-environment control only when hypotheses require it.

### F14 — Evidence, provenance, data and experimental continuity

Immutable raw artifacts/streams, synchronized time/config/device identity, transformations, quality flags, calibration lineage, replay, claim linkage and Agent/device replacement recovery.

### F15 — External/shared capability, simulation and domain expansion

Cloud/shared labs, contract metrology/fabrication, remote instruments, cloud compute, CAD/SPICE/control/physics simulation and later domain Pods such as materials/chemistry/optics/energy/bio only under real programme pressure.

## 10. Mapping from the earlier 20-family list

The 15-family projection preserves the earlier content rather than deleting it.

```text
earlier 01 Facility / Utilities          → F01
earlier 02 Physical Safety              → F02
earlier 03 Compute / Control             → F03
earlier 04 Experiment Execution          → F04
earlier 05 Device Interoperability       → F05
earlier 06 Electronics / Embedded        → F06
earlier 07 General Physical Sensing      → F07
earlier 08 Imaging / Optics              → F08
earlier 09 Actuation / Mechatronics      → F09
earlier 10 Fabrication                   → F10
earlier 11 Sample / Object Handling      → F11
earlier 12 Metrology                     → F12
earlier 13 Environment Control           → F13
earlier 16 Data / Evidence               → F14
earlier 18 Modeling / Simulation         → F15
earlier 19 External Capability Access    → F15

earlier 14 Materials / Chemistry         → future F15 domain Pod
earlier 15 Biology                       → future F15 domain Pod
earlier 17 Security                      → cross-cutting requirement across F01–F15
earlier 20 Human / Operator Interface    → cross-cutting requirement across F01–F15
```

This removes the false implication that Security is one equipment family or that Biology should be procured at the same abstraction level as power distribution.

## 11. Family-by-family audit contract

Every F01–F15 expansion should use the same structure.

```text
1. Referent
   What capability does this family actually provide?

2. Existing Ordivon standing
   Which owners already cover its semantics?

3. External mature baseline
   Standards, ecosystems, commercial/shared carriers, safety/metrology practice.

4. Current local Reality
   What is physically available now?

5. Capability pressure
   Which current/future bounded experiments would fail without it?

6. Minimal capability set
   Smallest support needed for those experiments.

7. OWN / POD / REMOTE / DEFER decision
   Compare frequency, latency, currentness, automation, safety, calibration, maintenance and external-access cost.

8. Integration seam
   Workstation / Runtime / Harness / World / Interlocus / Security / domain-owner boundaries.

9. Evidence contract
   What receipts prove the capability is real and current?

10. Failure / replacement / recovery
    How does it fail; what becomes UNKNOWN; how is it re-qualified?

11. Falsifier
    What evidence would show the family is overbuilt, unnecessary or wrongly owned?

12. Only then: concrete implementation / product / BOM
```

### Cross-cutting questions for every family

Security:
- trust boundary;
- access/secrets/network/firmware provenance;
- attack/failure surface;
- security != machine safety.

Human/operator:
- what physical maintenance/recovery still requires a person;
- what state must be visible;
- what manual stop/override exists where risk requires it;
- Human != universal scientific evaluator.

## 12. Current stop / promotion rules

Do **not** promote a family into owned infrastructure because:

- it is common in professional laboratories;
- a product is discounted/available;
- a future use can be imagined;
- the architecture should look complete;
- a robot/FPGA/PLC would make the system feel more advanced;
- a standard exists and Ordivon could implement it.

Promotion toward local ownership requires some combination of:

```text
repeated demand
+ low-latency closed-loop need
+ exact local identity/currentness importance
+ meaningful automation benefit
+ manageable safety/calibration/maintenance burden
+ external route would break experiment cadence/recovery
```

Prefer remote/shared when:

```text
use is sparse
or equipment is expensive/specialized
or calibration/maintenance dominates
or facility burden is high
or independent external measurement is scientifically valuable
```

## 13. Current standing after this map

The first Laboratory build should be represented as:

```text
Physical Falsification Substrate
```

before it is represented as:

```text
owned equipment collection
```

The first useful physical bench earns value when it can repeatedly answer questions of the form:

```text
What physical world are we actually in?
What measurement is justified?
What effect actually occurred?
Which device/object generation produced this evidence?
What remains UNKNOWN?
Can a replacement Agent reconstruct the experiment?
Does a new instrument/fixture change target-relative discriminability or reachability?
```

The next sequential work item is **F01 — Facility, utilities and bench infrastructure**, using the 12-step family audit contract above. Product selection remains downstream of that family analysis and of F02/F03/F06 pressure.
