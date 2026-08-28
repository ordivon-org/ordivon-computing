# Ordivon Laboratory F02 — Physical Safety, Authority and Energy Isolation v0.1

Status: **CURRENT FAMILY AUDIT / ENERGY-CLASS-RELATIVE SAFETY PLANE**  
Date: 2026-08-26  
Parent: `research/LABORATORY-PHYSICAL-FALSIFIER-MAP-20260826.md`  
Previous family: `research/LABORATORY-F01-FACILITY-UTILITIES-BENCH-20260826.md`  
Host continuity: `task:ordivon-laboratory-capability-atlas-20260826@11`

## 0. Referent

F02 asks:

> When Ordivon can cause a physical effect, which safety conditions must constrain or veto energy/effect independently of Agent intent, Runtime liveness and ordinary device-control success?

F02 is **not**:

- a universal Safety semantic owner;
- Security renamed for machines;
- Normative permission translated into wires;
- a requirement that every experiment have an emergency-stop button;
- a PLC/safety-PLC procurement plan;
- a claim that de-energization is the safe state for every future machine;
- occupational-safety legal advice;
- a substitute for device/cell/domain-specific hazard analysis.

Its current responsibility is a planning projection over **physical effect admission**:

```text
what energy/effect can this rig produce?
→ what hazards remain after upstream reduction?
→ what physical safety functions are required?
→ which of those must survive Agent/Runtime/controller failure?
→ what evidence establishes current safety readiness?
```

The safety plane is operation-relative and energy-class-relative.

## 1. Existing Ordivon standing — no new foundational theory needed

### 1.1 Normative subtraction

Current Ordivon Normative standing already preserves:

```text
permission
!= capability
!= control
!= normative power
```

and keeps operational authorization/lifecycle separate from normative truth.

Therefore:

```text
Domain/Human says "this experiment is permitted"
```

does not establish:

```text
physical system is safe to energize now
```

F02 must not mint a new normative authority merely because an experiment has safety constraints.

### 1.2 Security subtraction

Security already provides strong owner-native evidence for:

```text
proposal
!= authority/admission
!= backend effect
!= independent world verification
```

and real interrupted-effect/recovery cases where independent world observation prevents duplicate mutation.

Security's `RangeAuthority`, quarantine, containment and adversarial truth are not general machinery-safety semantics.

Transfer:

```text
Security admission pattern
may inform separation discipline
but
Security != machine safety owner
```

### 1.3 Runtime / Harness / World subtraction

Runtime can durably execute a physical command and retain an exact Attempt/Artifact receipt.

Harness can mediate Agent intent and tool effects.

World can preserve bounded observation/consequence/currentness semantics.

None of these imply:

```text
Runtime alive
or
Agent authorized
or
device command accepted
⇒
physical action safe
```

### 1.4 Workstation vNext safety standing

Current Workstation Laboratory vNext already contains the correct boundary for hazardous motion/energy:

```text
Domain/Human authorization
        ↓
Agent bounded proposal
        ↓
Runtime dispatch
        ↓
device/control command
        ↓
independent safety controller/interlock
        ↓
physical effect
        ↓
independent readback
```

and explicitly preserves:

1. software authorization never proves physical safety;
2. safety readiness is independently observed where applicable;
3. emergency stop / safe state must not require Agent, Host or Runtime liveness;
4. physical response loss enters UNKNOWN + reconciliation;
5. blind retry is forbidden for potentially crossed physical effects;
6. hazardous action semantics remain device/cell-specific until repeated pressure justifies a shared abstraction.

F02 therefore operationalizes an existing seam. It does not reopen it.

## 2. Mature external baseline

### 2.1 ISO 12100 — risk assessment and risk reduction first

ISO 12100:2010 specifies basic terminology, principles and methodology for machinery safety and explicitly centers risk assessment and risk reduction in design.

Transfer:

```text
identify hazard
→ estimate/evaluate risk
→ reduce risk at source / by design
→ add protective measures where residual risk remains
```

not:

```text
install E-stop
→ declare safe
```

Source:
https://www.iso.org/standard/51528.html

### 2.2 Singapore WSH risk-management baseline

Singapore MOM states that workplaces must conduct regular risk assessments, control/monitor risks and communicate those risks. WSH Council guidance prioritizes the Hierarchy of Control: elimination, substitution and engineering controls are upstream of administrative controls and PPE.

This is used here as mature risk-management practice. Whether a particular personal/home research setup is legally a regulated workplace depends on facts outside this audit.

Sources:
- https://www.mom.gov.sg/workplace-safety-and-health/safety-and-health-management-systems/risk-management
- https://www.tal.sg/wshc/topics/risk-management/conducting-risk-assessments
- https://www.tal.sg/wshc/topics/machinery-safety/preventing-machine-hazards

### 2.3 ISO 13850 — emergency stop is a specific safety function, not a universal ritual

ISO 13850:2015 defines functional requirements and design principles for machinery emergency-stop functions, independent of the type of energy used. Its scope excludes machines where providing an emergency stop would not lessen the risk.

Transfer:

```text
E-stop is earned when it can materially reduce risk
```

not:

```text
every physical experiment needs a red mushroom button
```

Source:
https://www.iso.org/standard/59970.html

### 2.4 ISO 13849-1 — when control functions become safety-related

ISO 13849-1:2023 specifies methodology and requirements for design/integration of safety-related parts of control systems performing safety functions, including software.

Transfer:

If a future rig relies on a control function to prevent unacceptable harm, then the architecture/reliability of that safety-related control path becomes a separate engineering responsibility. Ordinary MCU code, Runtime checks or Agent policy are not automatically equivalent to a safety-related control system.

Source:
https://www.iso.org/standard/73481.html

### 2.5 IEC 60204-1 — machinery electrical-equipment baseline

IEC 60204-1:2016 applies to electrical/electronic/programmable electronic equipment and systems of machines not portable by hand while working. The standard covers the machine electrical-equipment domain beginning at the supply connection.

Transfer:

As Ordivon progresses from passive low-voltage fixtures to real machines/cells, electrical-equipment safety should consume mature machinery standards rather than become an Ordivon-specific electrical-safety theory.

Source:
https://webstore.iec.ch/en/publication/26037

### 2.6 2026 autonomous-laboratory safety pressure

A July 2026 Nature Synthesis comment argues that industrial self-driving laboratories need more than safe robots and instruments: they need an autonomy safety harness defining how AI-generated intent becomes executable experiments, monitored actions and trustworthy evidence.

Transfer:

```text
safe component
!=
safe autonomous experiment trajectory
```

but this does not imply the AI safety harness should replace independent hardware safety functions.

Source:
https://www.nature.com/articles/s44160-026-01120-6

## 3. Safety is not one scalar

F02 rejects a global `SAFE=true` bit.

At minimum, separate:

```text
HazardPresent
RiskReducedFor(operation)
SafetyFunctionRequired(function)
SafetyFunctionReady(function, current-generation)
ExperimentAuthorized
ExperimentOperationallyAdmitted
PhysicalEffectAllowedNow
EmergencyStopRequired
EmergencyStopAvailable
PostEffectStateKnown
```

These are not one authority.

Examples:

```text
experiment authorized
+ safety function not ready
→ NO EFFECT ADMISSION
```

```text
interlock healthy
+ experiment not scientifically/normatively authorized
→ NO EFFECT ADMISSION
```

```text
Runtime process dead
+ hazardous energy still present
→ hardware safety function must still work where required
```

## 4. First campaign energy/effect classes

F02 starts from the planned falsifier campaign rather than generic machinery categories.

### EC0 — Passive / observational, extra-low-energy electronics

Examples:

- passive RC network;
- DMM resistance check;
- scope observation of small voltage waveforms;
- unpowered fixture replacement.

Hazards are primarily:

- accidental short/overcurrent when powered during setup;
- small component heating;
- instrument/probe misuse;
- ESD damage to electronics;
- trip/physical clutter from leads.

No hazardous motion.

### EC1 — Controlled low-voltage stimulus

Examples:

- MCU step/pulse into passive network;
- low-voltage AWG stimulus;
- programmable source under current limit.

Added hazards:

- continuous fault current;
- wiring heating under short/fault;
- wrong polarity/connection damaging DUT/instrument;
- stored charge if capacitance later increases.

For the first E0 campaign the rig should deliberately constrain itself to a conservative bounded DC/low-frequency envelope and exclude mains-exposed circuitry, high-energy batteries, large capacitive storage and high-power loads.

### EC2 — Low-energy persistent effect

Needed for PF-05 response-loss testing.

Examples:

- latching relay state;
- mechanically retained low-force flag;
- other bounded persistent state whose consequence can survive a lost response.

The test must make the effect persistent enough to reconcile, but not make persistence itself hazardous.

### EC3 — Low-energy electromechanical motion (E1)

Examples:

- small servo/stepper/linear actuator;
- compliant strip deformation;
- low-force load-cell/position experiment.

Added hazards:

- pinch/trap points;
- unexpected motion;
- actuator stall/overheating;
- retained spring/compliance energy;
- mechanical end-travel collision;
- restart after software/controller recovery;
- wiring entanglement.

This is the first current campaign class where an independent motion-energy veto is likely to be earned.

### EC4+ — Future higher-energy classes

Not admitted now:

- mains-exposed experimentation;
- high voltage;
- high-current/high-power battery work;
- large stored capacitive/inductive energy;
- high-force/fast robots;
- pressure/vacuum hazards;
- hot processes/high-temperature furnaces;
- lasers requiring controlled safety zones;
- hazardous chemicals/biological agents.

These require separate domain/cell/facility pressure and may require professional/shared facilities rather than local ownership.

## 5. Upstream risk reduction before safety-control complexity

The primary F02 design law is:

```text
reduce hazard at source
before
adding complex protective control
```

For the first campaign this means:

### E0

Prefer:

- passive components;
- low-voltage isolated/OEM supplies;
- bounded current;
- small stored energy;
- no exposed mains;
- no high-energy battery;
- no hazardous motion;
- no unattended long-duration energized experiment initially.

This eliminates most need for sophisticated safety logic.

### E1

Prefer:

- deliberately low force/speed;
- low-mass moving parts;
- compliant mechanics;
- short stroke;
- current/torque limiting;
- mechanical geometry that minimizes pinch access;
- end stops that prevent destructive overtravel;
- de-energized safe state where the specific rig supports it;
- no heavy payload or sharp tooling.

If the scientific question can be answered by a safer small rig, do not use a larger robot merely because one is available.

## 6. F02 minimal safety set for E0-A/B/D/E

### F02-E0-C1 — Explicit low-energy envelope

Every first E0 physical run should declare an energy envelope rather than relying on informal "low voltage" language.

The exact numerical envelope is apparatus-dependent, but the first campaign should normally remain in the small SELV-like laboratory-electronics regime using isolated OEM/bench supplies and current limiting, without treating any specific voltage number in this research note as a regulatory safety threshold.

Required declared coordinates:

```text
maximum intended voltage
maximum source current limit
expected load range
maximum relevant stored energy / capacitance if nontrivial
expected run duration
whether any exposed conductive part can carry mains/hazardous voltage
```

If these cannot be stated, E0 is not admitted.

### F02-E0-C2 — Current/energy limiting as the first engineering control

For E0, the most useful safety function is usually not emergency stop. It is preventing a wiring/DUT mistake from accessing large energy in the first place.

Use one or more appropriate mature mechanisms:

- programmable/current-limited bench source;
- source-side current limiting;
- appropriately selected fuse/polyfuse where useful;
- series resistance where scientifically compatible;
- small-capacity source rather than large battery;
- bounded component ratings.

The exact mechanism is derived from F06 apparatus selection.

### F02-E0-C3 — Manual all-energy removal

A Human/operator must be able to remove experiment energy quickly and unambiguously without needing:

- Agent response;
- network;
- Host;
- Runtime;
- application software.

For E0 this can be as simple as:

```text
reachable supply output-off / power switch
or
reachable low-voltage disconnect
```

provided it actually removes the experiment's relevant energy and the system has no hazardous retained energy.

Do not call an ordinary switch an `Emergency Stop` unless the function is actually designed/validated as one.

### F02-E0-C4 — Setup/de-energize discipline

For first E0:

```text
wire / change fixture
while de-energized
→ inspect
→ apply bounded power
→ observe
→ remove power before topology changes
```

This is an administrative procedure supporting upstream engineering controls, not a substitute for them.

### F02-E0-C5 — No unattended hazard promotion

The first E0 campaign should not introduce unattended energized operation merely to demonstrate autonomy.

Automation can run while a Human is not continuously interacting, but only after the energy/fault envelope demonstrates that loss of supervision cannot create a materially hazardous state.

### E0 conclusion

For E0-A/B/D/E:

```text
independent safety PLC      NOT EARNED
safety-rated relay          NOT EARNED
E-stop function             NOT EARNED by current risk
light curtain               NOT EARNED
guarded robot cell          NOT EARNED
```

The first safety architecture is largely **hazard minimization + current limiting + reachable manual energy removal**.

## 7. E0-C response-loss experiment: safety-specific design

PF-05 requires a real effect to occur while delivery/response becomes uncertain.

This could be a dangerous experiment if implemented with significant motion/heat/energy. Therefore F02 imposes a stronger constraint:

> The persistence mechanism must be informationally useful but physically low-consequence.

Preferred examples:

```text
latching relay contact state observed at low voltage
small mechanical indicator with negligible stored energy
non-hazardous retained electrical logic state plus independent physical/electrical observation
```

Avoid using for first response-loss test:

- heater;
- high-current load;
- motor that continues moving;
- pressurized actuator;
- high-force latch;
- any effect where uncertainty itself creates a hazard.

This preserves the epistemic pressure while aggressively minimizing safety burden.

## 8. F02 minimal safety set for E1 electromechanics

E1 is different because the physical effect continues into motion and mechanical interaction.

### F02-E1-C1 — Independent actuator-energy enable

The actuator power path should contain a physical enable/cut mechanism that does not depend on the Agent/Runtime command path.

Conceptually:

```text
Agent/Runtime command path
        ↓
controller command
        ↓
actuator driver
        ↓
[ independent energy-enable / cut path ]
        ↓
actuator
```

The independent path may be simple for a low-energy rig; it does not automatically require a safety PLC.

What matters is:

```text
Agent says MOVE
+ safety energy-enable absent
→ actuator cannot receive hazardous motion energy
```

### F02-E1-C2 — Default safe state under software loss

For the intended E1 compliant rig, choose mechanics/driver behavior so loss of command or Agent/Runtime death tends toward a low-risk state.

Likely first-rig target:

```text
controller/command loss
→ no new motion command
→ actuator de-energized or bounded hold
→ no uncontrolled restart
```

But F02 does **not** generalize `de-energized = safe` to all future machinery. A vertical axis, heavy payload, brake or process system may require controlled stop/holding before power removal.

### F02-E1-C3 — Force/speed/travel limiting

The experiment should physically limit consequence through:

- low motor current/torque;
- deliberately low motion speed;
- short stroke/travel;
- mechanical end stops where scientifically compatible;
- compliant coupling;
- low moving mass;
- no sharp tooling.

These are preferred before complex detection/guarding.

### F02-E1-C4 — Pinch / access geometry

If a finger can enter a pinch/trap zone that can cause harm, either:

- redesign geometry to eliminate/reduce the pinch;
- reduce force/energy until the hazard becomes acceptably bounded;
- or add guarding/interlock appropriate to the residual risk.

A software warning is not equivalent to physical hazard reduction.

### F02-E1-C5 — Manual motion-energy removal

The first E1 rig should expose a reachable manual actuator-power cut independent of Agent/Runtime.

This is the first family point where a dedicated physical stop control is likely worth owning.

But terminology remains precise:

```text
manual actuator-power cut
```

is not automatically:

```text
ISO 13850 emergency-stop function
```

If the later risk assessment shows an emergency stop materially reduces risk, then design an actual E-stop function to the applicable standard and safety-related control architecture.

### F02-E1-C6 — Restart inhibition / re-admission

After:

- controller restart;
- Runtime restart;
- Agent replacement;
- interlock opening;
- manual power cut;
- detected end-stop/fault condition;

motion must not silently resume because a historical command remains queued/current.

Require:

```text
fresh physical state observation
+ current safety readiness
+ fresh effect admission
```

before new motion.

### F02-E1-C7 — Independent post-effect observation

Safety and scientific evidence share a useful structure but not necessarily the same sensor authority.

A motion command receipt is insufficient.

At least one suitable observation should establish relevant physical state, such as:

- position/encoder;
- force/load;
- motor current where useful;
- independent vision/displacement.

This supports PF-01/PF-04/PF-05 recovery but is not, by itself, a safety-rated sensor.

## 9. When an actual E-stop becomes earned

F02 uses the following admission question:

> If a hazardous event begins, does an emergency-stop function materially reduce the risk beyond ordinary stop/manual disconnect and the upstream safeguards already present?

If `NO`:

```text
E-stop NOT EARNED
```

If `YES`:

then the future rig must treat E-stop as a real machine safety function, not a UI button.

That implies at least:

- physical function appropriate to the hazard;
- independent operation from Agent/Harness/Runtime;
- known effect on energy/motion;
- reset/restart behavior defined by the machine safety design;
- validation against the relevant machine/control standard;
- current readiness evidence.

At higher risk, ISO 13849-1 / IEC 62061-class safety-related control design may become relevant. This threshold is not reached by E0 and is not automatically reached by low-energy E1.

## 10. Safety authority topology

F02 proposes no global Safety owner. Instead, it distinguishes authorities/functions at the physical effect boundary.

```text
Scientific / domain authorization
  What experiment should be allowed?

Normative authority
  Is the action permitted/valid in the relevant context?

Agent / Harness
  What action is proposed/selected?

Runtime
  What exact command was durably admitted/executed?

Device controller
  How is the command translated to device mechanics?

Safety function / interlock
  Is hazardous energy/effect physically permitted right now?

World / independent observer
  What physical state/effect is currently supported by evidence?
```

The safety function has **veto precedence at the physical effect path** without becoming owner of scientific truth or normative legitimacy.

A useful law is:

```text
SafetyVeto(effect) = true
⇒ effect path blocked/energy removed as designed
```

but:

```text
SafetyReady
⇏ scientifically justified experiment
⇏ normative permission
⇏ successful experiment
```

## 11. Safety readiness is current and generation-bound

A hardware interlock that worked yesterday does not permanently authorize today's rig.

Relevant currentness coordinates may include:

```text
rig / cell generation
safety-function generation
energy source / driver generation
interlock/guard state
manual-stop availability
fault state
safe-state verification
observedAt / freshness
```

Replacement examples:

```text
new motor driver
→ old safety qualification does not silently transfer
```

```text
rewired actuator power path
→ old manual-cut evidence becomes historical
```

```text
same logical E1 rig name, new mechanical fixture
→ pinch/travel analysis may need requalification
```

No global safety freshness period is admitted; currentness is hazard/operation dependent.

## 12. Minimal safety-admission projection

Do not create a universal `SafetyCertificate` yet.

An ephemeral E1 operation projection can be conceptually represented as:

```text
operation                    E1-characterization
rigGeneration                 exact
energyClass                   EC3
hazardReductionEnvelope       QUALIFIED / UNKNOWN
actuatorPowerCutRequired      true/false
actuatorPowerCutReady         QUALIFIED / UNKNOWN / N/A
interlockRequired             true/false
interlockReady                QUALIFIED / UNKNOWN / N/A
travelLimitRequired           true/false
travelLimitReady              QUALIFIED / UNKNOWN / N/A
guardingRequired              true/false
guardingReady                 QUALIFIED / UNKNOWN / N/A
safeStateDefined              true/false
safeStateCurrent              QUALIFIED / UNKNOWN
restartRequiresReadmission    true
emergencyStopRequired         true/false/UNKNOWN
emergencyStopReady            QUALIFIED / UNKNOWN / N/A
```

This is a decision surface, not a persisted global ontology proposal.

## 13. Failure / response-loss / recovery semantics

### 13.1 Agent/Harness death

If Agent/Harness disappears:

```text
scientific selection stops
```

but required hardware safety functions remain active.

### 13.2 Runtime death / transport loss

If Runtime or the device response path disappears after dispatch:

```text
physical outcome = UNKNOWN
```

unless independent Reality evidence resolves it.

Safety action must not depend on Runtime being able to record the outcome.

### 13.3 Controller crash

For E1 the rig must define controller-failure behavior before admission.

Preferred low-energy first-rig behavior:

```text
controller failure
→ no further command generation
→ bounded/de-energized actuator state
→ manual/fresh-agent reinspection
→ explicit re-admission before motion
```

### 13.4 Safety function opened/tripped

A tripped/open interlock or manual energy cut should invalidate current effect admission.

Restoring the physical safety path does not revive an old motion command.

### 13.5 Sensor disagreement

If safety-relevant observations conflict and no authoritative adjudication exists:

```text
UNKNOWN / fail closed for hazardous effect
```

Do not average away a safety-relevant contradiction merely to keep the experiment running.

### 13.6 Power return

Power restoration after interruption must not itself re-authorize motion/heat/other persistent hazards.

For E1:

```text
power restored
→ safe/restart state
→ physical observation
→ fresh admission
→ new effect only then
```

## 14. OWN / POD / REMOTE / DEFER decisions

| Safety capability | Current disposition | Why |
|---|---|---|
| low-energy design envelope | **CORE / NOW** | cheapest upstream risk reduction |
| source current limiting | **OWN / NOW with F06 apparatus** | directly bounds E0 fault energy |
| reachable manual E0 power-off/disconnect | **OWN / NOW** | independent of software, trivial burden |
| passive protection/fuse where required | **OWN / NOW per circuit** | low cost, failure-contained |
| E0 emergency-stop function | **NOT EARNED** | current hazards do not justify it |
| E0 safety relay/PLC | **NOT EARNED** | no safety-related control burden yet |
| E1 independent actuator-power cut | **OWN-EARLY / REQUIRED for E1** | first genuine physical veto |
| E1 force/speed/travel limiting | **OWN / REQUIRED by rig design** | upstream mechanical risk reduction |
| E1 guard/interlock | **POD / CONDITIONAL** | only if geometry/residual risk earns it |
| ISO-13850-class E-stop | **CONDITIONAL** | only if it materially reduces identified risk |
| safety relay / safety PLC / rated controller | **DEFER** | only when required safety function reliability/risk earns it |
| robot-cell safety architecture | **DEFER** | no robot cell admitted |
| hazardous-energy lockout/tagout system | **DEFER TO ENERGY CLASS / FACILITY** | no current EC4+ system |
| specialist safety assessment | **REMOTE/SHARED-FIRST** for higher risk | external expertise preferable before local hazardous descent |

## 15. Current hardware reality

Current device observations show no laboratory actuator/controller/instrument attached.

Therefore none of the following can presently be claimed:

```text
physical interlock present
manual actuator cut present
safety relay present
E-stop present
safe-state path present
force/speed limit present
```

These are **UNKNOWN / not-yet-applicable**, not software-detectable absences.

F02 should not buy safety components in advance of the actual F06/F09 rig architecture, because the needed safety function depends on:

- source;
- driver;
- load;
- motion geometry;
- retained energy;
- failure mode;
- target hazard.

## 16. Cross-cutting Security boundary

Safety and Security interact but remain distinct.

Security questions:

- can an untrusted process bypass the actuator driver limits?
- can network access reconfigure current limits/safety parameters?
- can firmware replacement silently change safe-state behavior?
- is the safety controller/relay configuration identity known?
- can a malicious/buggy Agent repeatedly request reset/re-arm?

Safety questions:

- does the physical safety function remain effective even if the software is compromised?
- what happens if the controller lies or crashes?
- what physical energy remains after veto?

Desired relationship:

```text
Security helps protect safety configuration/control path
but
Security policy is not the safety function itself
```

For high-consequence future cells, safety-critical configuration should be difficult or impossible for ordinary Agent authority to rewrite during a run.

## 17. Cross-cutting Human/operator role

For the first physical laboratory, Human remains structurally involved in safety because the system does not yet possess enough independent room/rig observation or manipulation to prove safety readiness autonomously.

Human tasks may include:

- inspect wiring/guards/clearance;
- connect/disconnect power;
- verify manual cut works;
- inspect mechanical end stops;
- clear a physical fault;
- reset a safety function when appropriate;
- confirm no body part/tool remains in the motion zone before first energization.

But:

```text
Human says "looks safe"
```

must not become a universal unstructured safety oracle once the rig has machine-checkable safety functions.

The long-term direction is evidence-supported safety readiness, not Human ceremony.

## 18. F02 physical falsifiers

### F02-F1 — Agent veto independence

**Setup**

E1 Agent/Runtime issues a valid motion request while independent actuator-energy enable is open.

**Expected**

```text
command path succeeds mechanically/software-side
but
actuator receives no unsafe motion energy
```

**Failure**

Any Agent/Runtime state can bypass the independent veto under ordinary authority.

This is the primary F02 physical falsifier.

### F02-F2 — Runtime death does not defeat safety state

Kill/lose Runtime while the E1 system is in an admitted bounded state.

Expected safety behavior remains defined without Runtime callbacks.

If the rig requires Runtime liveness to avoid hazard, a stronger independent control layer is required before promotion.

### F02-F3 — Historical command does not resume after safety reset

1. command motion;
2. open manual cut/interlock;
3. restore safety path;
4. do **not** issue fresh motion authorization.

Expected:

```text
no automatic motion resume
```

### F02-F4 — Current limiting changes consequence

Introduce a bounded electrical fault/short through an appropriate test fixture.

Compare unrestricted-available source behavior versus admitted current-limited path **only within a safe test design**.

The purpose is not destructive testing; it is to prove that the chosen limiting mechanism is actually in the effect path and materially bounds fault energy.

### F02-F5 — E-stop deletion test

For E0, ask whether adding an E-stop changes any credible hazard outcome beyond the existing reachable output-off/disconnect and low-energy envelope.

If not:

```text
E-stop remains NOT EARNED
```

This prevents safety theatre.

### F02-F6 — Guard/interlock deletion test

For E1, only admit guard/interlock infrastructure if removing it while holding upstream force/speed/geometry constant creates a material residual risk that cannot be acceptably reduced by simpler design changes.

## 19. Safety promotion ladder

Use a pressure ladder instead of a shopping list.

### S0 — Intrinsically / deliberately low consequence

```text
passive / small-energy E0
```

Mechanisms:
- energy reduction;
- current limit;
- manual disconnect;
- simple procedure.

### S1 — Bounded low-energy motion

```text
E1
```

Adds:
- independent actuator-energy enable/cut;
- force/speed/travel limitation;
- defined safe state;
- restart re-admission;
- guard/interlock only if residual risk requires it.

### S2 — Material hazardous motion/energy

Possible future:
- larger robot;
- higher force/speed;
- significant heating;
- pressure;
- stored energy.

Now safety-related control architecture, actual E-stop design, validated guards/interlocks and specialist risk assessment may become mandatory.

### S3 — Facility/process hazard

Possible future:
- mains/high voltage;
- industrial robot cell;
- hazardous chemistry;
- laser controlled area;
- pressure/vacuum/high temperature.

Default:

```text
shared/professional facility first
```

unless repeated programme pressure justifies owning the facility/safety burden.

## 20. F02 stop rules

Do not add safety infrastructure because:

- it appears on a professional laboratory tour;
- it makes the bench look serious;
- it provides more buttons/relays;
- it is common in robot cells but no robot exists;
- a standard mentions a mechanism outside our current hazard class;
- software can expose a `SafetyReady` field.

Add a safety function only when:

```text
identified hazard
+ residual risk after upstream reduction
+ safety function materially reduces that risk
+ current function can be independently verified
```

## 21. F02 standing

### E0

For E0-A/B/C/D/E:

```text
F02 = MINIMAL / HAZARD-REDUCTION-FIRST
```

Required core:

```text
bounded low-energy envelope
+ current/energy limiting
+ no exposed mains/high-energy storage
+ reachable manual energy removal
+ de-energized topology changes
+ explicit response-loss/recovery semantics
```

Not required by current pressure:

```text
E-stop
safety PLC
safety relay
robot guard
light curtain
industrial LOTO system
```

### E1

For the first low-energy electromechanical fixture:

```text
F02 = FIRST INDEPENDENT HARDWARE VETO
```

Required direction:

```text
independent actuator energy-enable/cut
+ low force/speed/travel
+ defined safe state
+ no silent restart
+ fresh readmission after trip/restart
+ guard/interlock only if residual hazard earns it
```

### Deep architectural conclusion

The important safety property is not:

```text
Agent knows the rule
```

It is:

> **The physical system is constructed so that some unsafe transitions are unavailable to ordinary Agent/Runtime authority.**

That is a genuine capability/authority asymmetry at the Reality boundary.

F02 does not create a new global owner from it. The actual safety function remains rig/cell/domain-specific until heterogeneous repeated consumers prove a shared invariant.

## 22. Next family boundary

F02 now gives F03 a concrete contract.

F03 — Compute, Control, Timing and Low-level Interfaces must provide control capability **without** absorbing the independent safety function.

The first F03 question is therefore:

```text
What belongs in Agent/Runtime/general compute?
What belongs in deterministic MCU/local control?
What timing/current-state functions are needed?
What must remain outside both because it is safety-critical?
```

FPGA/PLC/real-time OS are not presumed; they must be earned by control/timing pressure.
