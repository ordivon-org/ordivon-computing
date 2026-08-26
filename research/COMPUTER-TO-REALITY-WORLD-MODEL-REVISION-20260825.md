---
schema_version: 1
id: computing.research.computer-to-reality-world-model-revision-20260825
title: From Agent-Native Computer to Computational Embodiment in Reality
type: research
profile: research
lifecycle: active
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-25
summary: Working world-model revision that reinterprets the historical Ordivon Computer line under later Reality, representation, continuity, capability-pressure, Workstation, and laboratory research.
evidence_status: mixed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-project-family
related:
  - computing.research.computer-agent-native-lineage-20260724-20260825
  - computing.stack
  - computing.foundations
  - computing.research.world-model-loop
---
# From Agent-Native Computer to Computational Embodiment in Reality

> **Working shared world-model revision, not current product or hardware authority.** This note revises how the historical Ordivon Computer problem is represented. It does not create a new Lab owner, hardware roadmap, universal physical-control plane, or Core foundation. Current owner-native facts and exact product repositories remain authoritative.

## Why reopen the Computer question now

The original Ordivon Computer line began from a strong but still recognizably software-centric question:

```text
If Agents become primary planners, programmers, and operators,
which inherited computing abstractions remain valid,
and which Agent-native responsibilities must be rebuilt?
```

That question generated useful distinctions, then contracted under evidence from Semantic Core to classical substrate + a thin durable responsibility band, and later to owner-native Situation, First Interface, and Representation Environment work.

The later research programme has changed the surrounding world model enough that the old question is no longer the strongest formulation. Several new pressures now exist simultaneously:

- Reality research separates represented, claimed, observed, current, historical, and physically consequential state;
- SCD / Media / Representation work shows that representation can change search, discrimination, error detection, and action capability rather than merely package information;
- Host / Atlas / Harness continuity work separates storage from the ability of future finite intelligence to resume valid action;
- Interlocus / Security work makes identity, binding, provenance, currentness, authority, and adversarial migration first-class;
- Workstation practice increasingly crosses Windows, drivers, power state, BIOS-exposed facts, device firmware, equipment, and external connectivity;
- the laboratory horizon introduces direct sensing, actuation, experimentation, robotics, instrumentation, and fabrication;
- Computational Possibility raises the stronger question of whether an intelligence's reachable hypothesis/action space changes when its representations, instruments, and physical interfaces change.

The revised question is therefore:

> **How should a finite intelligence externalize computation, observation, intervention, continuity, and evidence across digital and physical Reality without turning one central Computer layer into universal truth or control authority?**

This is a broader problem than an Agent-native operating system and narrower than “Ordivon should build every layer itself.”

---

## 1. What the old Computer model got right

The historical line should not be discarded. Several of its deepest results become more important, not less, once physical systems enter the loop.

### 1.1 Mature mechanics should remain with their strongest owner

The original rule survived every contraction:

```text
own irreducible semantics
reuse mature mechanisms
```

A future Ordivon laboratory does not imply replacing Linux, Windows, USB, Ethernet, oscilloscopes, robot controllers, MCU toolchains, BMC firmware, databases, CAD systems, or scientific instruments merely because Ordivon uses them. A mature carrier remains preferable when it preserves the required invariant with lower recurring ownership cost.

### 1.2 Intent, attempt, evidence, verification, and completion are distinct

The early Semantic Core distinguished:

```text
Effect != Dispatch
Observation != Fact
Artifact != Verification
Process exit != semantic completion
UNKNOWN != failure
```

These distinctions become even more important for physical work. A command to heat a sample is not evidence that it reached the requested temperature. A robot motion acknowledgement is not evidence that the intended object was grasped. A firmware flash process exiting zero is not evidence that the target device is now functioning correctly.

### 1.3 Response loss and uncertainty require reconciliation

The old recovery law:

```text
lost response
→ reconcile the original effect/request identity
→ do not blindly redispatch
```

is directly transferable to physical operations, where blind retry can duplicate motion, dosing, power cycling, fabrication, or other irreversible effects.

### 1.4 Owner-native truth should not be centralized for convenience

The later Situation experiments established:

> unified consumption does not require unified state, currentness, or authority.

That remains the correct direction for physical systems. A future laboratory should not create one giant `PhysicalState` object that silently overrules instrument owners, device controllers, World semantics, domain completion criteria, or human authority.

### 1.5 First Interface is an environment problem

The later Computer lineage already moved beyond “more tools” toward operation-relative affordance recompilation. A physical laboratory strengthens that conclusion: a finite Agent should see the instruments, measurements, controls, identities, uncertainty, and safety boundaries relevant to the current operation, not the complete device API universe.

---

## 2. What was still immature

The earlier Computer framing was strong for software architecture but too weak for a system that may eventually operate in physical Reality.

### 2.1 The stack diagram was mistaken for too much of the ontology

The old three-band representation was useful:

```text
flexible cognition
↓
durable responsibility boundaries
↓
classical substrate
```

But a physical component cannot always be classified merely as “lower substrate.” The same GPU, EC, sensor, robot, power supply, or PCB may be different things relative to the current operation:

- **substrate** — a mechanism being relied upon;
- **instrument** — a means of observing or changing another object;
- **experimental object** — the thing being investigated;
- **authority boundary** — the component that actually admits or enforces an effect;
- **consequence surface** — where an irreversible or safety-relevant effect occurs;
- **evidence source** — a producer of observations whose provenance and calibration matter.

Therefore a layer stack remains a useful engineering projection, but it is not a complete world model.

### 2.2 “Physical substrate” was treated as mostly passive and inherited

`core/stack.md` correctly delegates hardware and operating-system mechanics to classical owners for today's software workloads. The immature inference would be:

```text
hardware is lower
therefore hardware is merely infrastructure
```

Once hardware itself becomes the target of diagnosis, experimentation, modification, fabrication, or scientific inquiry, that inference fails. Physical Reality can be both carrier **and** object of knowledge/action.

### 2.3 Equipment was initially represented mainly as extra Tool capability

The E0 professional-equipment work made an important step: equipment is not semantic authority, and the Agent surface should expose operations such as `packet.decode` rather than CLI folklore. But most E0 equipment was still software or software-projected instrumentation.

A laboratory forces a stronger abstraction:

> An instrument is not merely a Tool executable. It is a controlled transduction relation between Reality and representation/action.

That relation includes sensor placement, calibration, sampling, timing, physical coupling, uncertainty, range, failure mode, actuator authority, and provenance.

### 2.4 Observation was too easy to imagine as retrieval

Software systems encourage a retrieval-shaped mental model:

```text
state already exists
→ query API
→ receive representation
```

Physical science often requires a different loop:

```text
unknown property
→ choose an observation geometry
→ configure / place / calibrate instrument
→ perturb or expose Reality
→ obtain signal
→ interpret signal under an instrument model
→ decide whether competing hypotheses became distinguishable
```

Observation is therefore sometimes an **active capability construction problem**, not a read operation.

### 2.5 Continuity was mainly digital

The mature Host/Atlas work already separates memory from continuity. A laboratory extends what must persist:

- specimen identity;
- wiring and fixture configuration;
- firmware/hardware revision;
- calibration state;
- instrument configuration;
- physical location and orientation;
- environmental conditions;
- partially completed physical process;
- safety state;
- unresolved physical Effect;
- causal binding between digital Artifact and physical object.

Saving logs without preserving these bindings is storage, not experimental continuity.

---

## 3. Revised world model: Computer is a relation to Reality, not only a stack

The strongest current representation is no longer:

```text
Agent
→ Computer
→ OS
→ hardware
```

A better working model is:

```text
                         Reality
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
      objects/state      constraints       consequences
          │                 │                 │
          └──────────┬──────┴──────┬──────────┘
                     │             │
                 observation   intervention
                     │             │
              instruments / transducers
                     │
              representations
                     │
              finite cognition
                     │
        hypothesis / selection / proposal
                     │
              authority admission
                     │
             physical realization
                     │
                  evidence
                     └──────────────↺
```

“Computer” in this model is best understood as the research area of **computational embodiment**: the mechanisms and responsibility boundaries through which finite intelligence acquires stable computational, observational, and intervention capability in Reality.

This does **not** make Computing the semantic owner of all embodiment. Computing studies the cross-owner relation and shared failure classes; Workstation, Runtime, World, Security, domain owners, instrument controllers, and future owners retain their own facts and consequence semantics.

---

## 4. Five roles of a physical component

Future architecture should classify a physical component relative to an operation, not once globally.

### Role A — substrate

The component supplies mature mechanics and should usually be inherited.

Examples: CPU arithmetic, DRAM, PCIe transport, filesystem, robot motor controller executing a bounded trajectory.

### Role B — instrument

The component changes what Reality can be observed or controlled.

Examples: oscilloscope, thermal camera, logic analyzer, current probe, robotic manipulator, programmable PSU.

### Role C — experimental object

The component's behavior is itself unknown or under revision.

Examples: EC firmware during a suspend/resume failure, a PCB under thermal stress, a battery pack under a new charging policy.

### Role D — authority / safety boundary

The component enforces whether an effect can physically occur.

Examples: hardware interlock, BMC/EC power controller, robot safety controller, emergency stop, current limit.

### Role E — evidence source

The component produces a signal that may support a claim, subject to provenance and measurement validity.

Examples: calibrated temperature probe, current shunt, camera, device telemetry channel.

A single physical device may occupy several roles simultaneously. That is a reason to preserve explicit owner and operation-relative relations rather than flattening it into a layer label.

---

## 5. Instrumentation is representation made physical

The Representation / SCD result now gains a physical interpretation.

A representation is not only text, schema, diagram, or Tool output. Sensors and measurement apparatus determine which distinctions in Reality become available to cognition.

For a hidden state `R`, an Agent does not receive `R` directly. It receives something closer to:

```text
R
→ physical coupling
→ sensor / transducer
→ acquisition process
→ calibration / filtering / timing
→ representation
→ finite observer
```

Changing this chain can change:

- which hypotheses are distinguishable;
- which failures become observable;
- which causal ordering can be recovered;
- which actions can be verified;
- which state can be reconstructed after interruption.

Therefore:

> **Instrumentation is a capability variable because it changes the observer's reachable evidence space.**

This is the physical analogue of the newer representation-capability hypothesis.

---

## 6. From information consumer to evidence producer

The laboratory horizon introduces one of the largest capability changes in the Ordivon world model.

Current digital workflows often have the form:

```text
existing external information
→ retrieval
→ interpretation
→ decision
```

A laboratory enables:

```text
uncertainty / competing hypotheses
→ choose discriminating experiment
→ construct observation/intervention geometry
→ execute
→ produce new evidence
→ revise belief
```

This is not merely “better data access.” The system can intentionally create evidence that did not previously exist.

The new capability should be represented as:

> **evidence production** — the ability to select and realize bounded interventions/observations whose outcomes discriminate among current hypotheses or validate a required consequence.

Evidence production is neither generic cognition nor generic Runtime execution. It is a cross-owner capability requiring domain experiment semantics, physical realization, measurement, provenance, safety, and revision.

---

## 7. The black-screen class exposes the old model's limit

Recent Workstation diagnosis provides a small but important example.

The current Windows hardware observation surface can inspect:

- GPU and display driver state;
- BIOS/version and platform identity;
- power scheme and processor policy;
- battery and ACPI-exposed thermal state;
- OEM services and provisioning packages.

That is useful evidence, but it remains a projection exposed through software/firmware interfaces. A visible-screen failure can still leave a gap between:

```text
Windows claims display path exists
!=
GPU/driver reports healthy
!=
firmware/EC power state
!=
actual panel power/signal state
!=
photons visible to the user
```

The revised lesson is not “add more diagnostics.” It is:

> **observed software state and physical realized state are different Reality coordinates.**

When those coordinates can diverge and different next actions follow, the system needs an independent observation path or must retain `UNKNOWN`.

A future laboratory could add panel power-rail measurement, signal capture, EC trace, external camera observation, and synchronized timing. That would change the diagnosable hypothesis space rather than merely increase log volume.

---

## 8. Physical currentness needs a richer state distinction

For consequential physical systems, at least the following states must remain separable when relevant:

```text
commanded state
reported state
observed state
inferred latent state
historical state
current accepted state
unknown / conflicting state
```

Example:

```text
command: display ON
reported: GPU active
observed: camera sees black panel
inferred: display pipeline failure after GPU
accepted current truth: unresolved until stronger evidence
```

This is a direct extension of World / Interlocus / Security currentness work. Physical state should not be made “current” because one control plane says so.

---

## 9. Physical continuity extends Host and Atlas without making them hardware owners

A future Agent replacement experiment in a laboratory should ask whether a new Agent can recover:

- what physical object is being worked on;
- its exact revision and provenance;
- the current experimental configuration;
- which Effects have definitely occurred;
- which Effects are uncertain;
- what instruments were calibrated and how;
- what observations are comparable;
- which safety constraints are still active;
- which hypothesis was being discriminated;
- what next physical action is admissible.

This is a stronger continuity test than restoring conversation or Task text.

Host remains a continuity carrier, Atlas remains a knowledge/standing carrier, and physical/domain owners remain truth authorities. The new requirement is a recoverable binding among them.

---

## 10. Physical action strengthens the old Effect model

For physical intervention:

```text
semantic intent
!= admitted command
!= controller dispatch
!= actuator motion
!= physical world transition
!= intended consequence
!= verified consequence
```

The old Effect/Dispatch distinction was therefore not an over-engineered software abstraction. It anticipated a much broader class of reality-changing uncertainty.

However, no universal physical Effect schema is admitted by this note. Different domains may require different semantics. The shared invariant is only that the distinctions remain recoverable when collapsing them creates unsafe retry, false completion, or lost accountability.

---

## 11. Safety is not a final wrapper

A laboratory also corrects a possible software-era bias: safety cannot be added only at the last API call.

Physical autonomy may require safety at several levels:

```text
hypothesis / experiment design
→ material/process admissibility
→ authority and participant rights
→ instrument operating envelope
→ controller limits
→ interlocks / emergency stop
→ live monitoring
→ anomaly response
→ recovery and post-event evidence
```

This is compatible with Ordivon's existing consequence-boundary principle but makes the carrier more heterogeneous. Some safety constraints belong to domain owners, some to physical controllers, some to institutions/law, and some to independent interlocks. No single Agent policy should be assumed sufficient.

---

## 12. Capability pressure, not layer ambition, decides expansion

The laboratory horizon must not become a “build the whole stack” reversal of the 2026-08-10 Computer contraction.

The expansion law is:

```text
important capability goal
→ identify the blocking Reality relation
→ test strongest mature carrier / instrument / provider
→ measure residual observation, action, recovery, authority, or learning gap
→ build only the narrow missing interface or mechanism
→ re-test
```

A lower layer is entered only when ownership of that layer, or a new interface to it, produces otherwise unavailable capability.

Examples:

- do **not** build a custom EC because EC firmware is interesting;
- consider custom EC/BMC-like control if independent recovery/telemetry is deletion-essential and current devices cannot provide it;
- do **not** build an oscilloscope because measurement matters;
- build a custom instrument only when available instruments cannot expose a required signal, timing relation, automation contract, or provenance boundary;
- do **not** fabricate custom compute hardware for symbolic completeness;
- fabricate when the physical architecture itself is the shortest path to a required capability.

This preserves A1/A11/A13 rather than contradicting them.

---

## 13. Revised owner implications

### Computing

Owns cross-domain research into computational embodiment, instrumentation, capability pressure, and responsibility placement. It does not become hardware/world authority.

### Workstation

Current best interpretation remains execution-node substrate and physical realization/binding authority for the local machine. Its future scope may deepen into firmware/equipment telemetry where real node operations require it. It should not become a universal laboratory owner by analogy.

### Runtime

A natural future extension is exact admitted physical-attempt realization and retained execution evidence: instrument runs, controller calls, firmware flashes, robot operations, calibration procedures, and bounded experiment steps. Runtime still must not infer domain scientific completion from physical process success.

### Harness

Should expose operation-relative capabilities and current affordances rather than raw instrument catalogs. It may help cognition choose experiments, but domain truth and safety authority remain external.

### World

Physical Presence/currentness becomes more important. World may represent current owner-qualified relations among Subjects, Bodies, locations, instruments, observations, and physical state without becoming a sensor daemon or global device database.

### SCD / Media

Representation research extends into scientific visualization, synchronized multimodal experiment views, measurement geometry, and observer-relative exposure. Instrumentation itself becomes partly a representation problem.

### Interlocus

Physical/digital binding becomes a first-class target: specimen ↔ design revision ↔ firmware ↔ instrument run ↔ Artifact ↔ claim ↔ current physical location/state.

### Security

Trust expands from credential/software integrity toward measurement integrity, firmware provenance, sensor/actuator identity, calibration, physical access, supply chain, and safe authority. “Who said the temperature is 82.3°C?” becomes a provenance question about the whole measurement chain.

### Host / Atlas

Continuity expands from digital work/history into recoverable physical experiment state and causal lineage. Neither becomes the physical truth owner.

### Game / Normative

A physical multi-agent environment can turn rules, incentives, authority, adversaries, and institutions into materially consequential experiments. Normative constraints become part of real action admissibility rather than only simulated rules.

### Future laboratory carrier

No new `Lab` semantic owner is created here. A laboratory may emerge as a composition of Workstation/Runtime/domain owners/instrument controllers, or later earn its own narrow owner if repeated workloads expose a non-bypassable unowned invariant.

---

## 14. External reality comparison

This revision aligns with several mature external trajectories without treating them as Ordivon authority.

### Cyber-Physical Systems

NIST's CPS work explicitly treats interacting digital, analog, physical, and human components as integrated systems and highlights sensing, actuation, trustworthiness, timing, data, composition, boundaries, and lifecycle. This supports replacing a purely software-stack ontology with an operation- and relation-sensitive cyber-physical model.

Source: NIST SP 1500-201, *Framework for Cyber-Physical Systems: Volume 1, Overview*; NIST CPS/IoT Foundations.

### Self-driving laboratories

The 2026 Nature Reviews Chemistry synthesis characterizes self-driving laboratories as autonomous experimentation + robotics + AI and identifies scalability, generalizability, and provenance-complete experimentation as central requirements for shared scientific infrastructure. That maps closely to Ordivon's continuity/provenance concerns and reinforces that experimentation infrastructure is more than a collection of Tools.

Source: Canty & Abolhasani (2026), *The past, present and future of self-driving laboratories*, Nature Reviews Chemistry.

### A-Lab

Berkeley Lab's A-Lab demonstrates the practical distinction between automation and adaptive research: robots synthesize and characterize materials in a closed loop, with the system choosing what to try next from results rather than repeating a fixed manufacturing sequence. This is a concrete example of evidence production as capability.

Source: Lawrence Berkeley National Laboratory, *Meet the Autonomous Lab of the Future* (2023), plus subsequent A-Lab/FORUM-AI work.

### Physical autonomy safety

Recent self-driving-laboratory safety work argues that safe instruments alone are insufficient and that AI-generated intent must be converted into monitored, constrained, evidence-producing experiments through explicit safety architecture. This closely matches the historical Ordivon separation of intent, admission, physical attempt, evidence, and completion.

Source: Nature Reviews Chemistry (2025), *Steering towards safe self-driving laboratories*; Nature Synthesis (2026), *Self-driving laboratories need an autonomy safety harness*.

### Out-of-band machine embodiment

OpenBMC shows a mature real-world pattern in which machine management, telemetry, power/reset, and recovery can remain available outside the host operating system. This does not imply Ordivon should build a BMC, but it is a strong external counterexample to the assumption that OS-visible state is the only meaningful machine observation/control plane.

Source: OpenBMC project, open-source BMC firmware stack for heterogeneous enterprise/HPC/telco/cloud systems.

---

## 15. Shared world-model standing after this revision

The strongest current working standing is:

### WM-COMP-R1 — Layer diagrams are projections, not complete ontology

The software/OS/firmware/hardware stack remains useful, but the relevant role of a component is operation-relative. Physical objects may be substrate, instrument, experimental object, authority boundary, consequence surface, or evidence source.

### WM-COMP-R2 — Computer should be studied as computational embodiment

The Ordivon Computer question is better represented as how finite intelligence obtains reliable computational, observational, intervention, and recovery capability in Reality, not merely how to redesign a software stack for Agents.

### WM-COMP-R3 — Instrumentation changes epistemic reachability

Measurement and actuation interfaces can change which hypotheses and failures are distinguishable and therefore can change effective intelligence capability.

### WM-COMP-R4 — Evidence production is a distinct capability

A system that can design and execute discriminating experiments has a capability unavailable to a pure information consumer, even with the same reasoning model.

### WM-COMP-R5 — Physical realized state is not identical to software-reported state

Where control-plane state and physical state can diverge, independent observation or explicit uncertainty is required before consequential inference.

### WM-COMP-R6 — Continuity must eventually include physical bindings

Long-lived experimental capability requires recoverable identity, configuration, calibration, effect, evidence, and location relations across Agent/process/device replacement.

### WM-COMP-R7 — Physical autonomy strengthens owner/admission boundaries

The move into Reality increases, rather than decreases, the need to separate cognition, authority, physical attempt, evidence, verification, safety, and completion.

### WM-COMP-R8 — Expansion remains capability-pressure driven

Laboratory ambitions do not repeal the removal-first Computer reform. Ordivon descends into firmware/electronics/robotics/fabrication only when a measured missing capability cannot be obtained through a mature narrower carrier.

---

## 16. What changes now, and what does not

### Changes now

- the historical Computer question should be recalled through the stronger “computational embodiment in Reality” frame;
- future Computer/Workstation/laboratory research should classify physical components by operation-relative role rather than layer alone;
- instrumentation and evidence production become explicit world-model concepts;
- physical/digital currentness and binding become first-class falsification targets;
- the laboratory horizon is admitted as a legitimate future capability environment rather than a collection of optional devices.

### Does not change yet

- no new Core foundation is admitted;
- no new permanent shared service is admitted;
- no universal PhysicalState / Equipment / Lab registry is admitted;
- no custom firmware/hardware roadmap is authorized;
- no owner boundaries are silently transferred to Computing;
- `core/stack.md` remains valid for current software execution responsibilities, but its “classical substrate” language should be treated as an operation-scoped architecture projection, not the full ontology of future physical Reality.

The existing A1, A2, A7, A8, A9, A10, A11, A13, A18 foundations currently survive this revision and in several cases gain broader support.

---

## 17. Falsifiers and next experiments

This revision should remain challengeable.

### F1 — software-only sufficiency

If materially different physical diagnostic/experimental workloads can achieve the same hypothesis discrimination, recovery, and verification using existing software telemetry alone, the claimed importance of independent instrumentation should narrow.

### F2 — instrumentation does not change capability

Hold Agent/model/domain knowledge constant and vary only representation/instrument access. If hypothesis quality, error localization, reachable actions, or experimental efficiency do not change across strong workloads, WM-COMP-R3 should weaken.

### F3 — evidence production adds no distinct capability

Compare an Agent restricted to existing data with the same Agent allowed to select bounded experiments. If the second condition does not resolve otherwise unresolved decision-relevant uncertainty, WM-COMP-R4 should narrow.

### F4 — physical continuity can be reconstructed cheaply from ordinary logs

Perform Agent replacement during a bounded physical experiment. If a fresh Agent can reliably recover current physical state, unresolved effects, configuration, and next admissible action without explicit physical bindings, WM-COMP-R6 is overstated.

### F5 — existing mature laboratory middleware owns the whole missing responsibility

Before constructing an Ordivon-specific physical-control layer, compare against mature lab automation, robotics middleware, device protocols, BMC/Redfish-class management, workflow engines, and domain instrumentation. If the mature owner preserves required semantics with lower total cost, inherit it under A1.

### Minimum future physical experiment

Do not begin with a large laboratory. A sufficiently strong first experiment could be:

```text
one MCU or controllable device
+ one independently measured physical variable
+ one actuator or state transition
+ exact firmware/config identity
+ bounded Runtime execution
+ owner-qualified observation
+ Agent replacement in the middle
+ reconciliation after one deliberately uncertain response
```

The experiment should test whether explicit physical binding/instrumentation produces a capability or recovery improvement that cannot be reproduced by software logs alone.

---

## 18. Reopen / promotion rule

Promote any part of this note toward reusable Knowledge or Core only after at least two materially different owner workloads show that deleting the distinction causes a recurring failure or capability loss.

Possible promotion candidates are the narrow relations, not the nouns:

```text
reported state != physically realized state
instrument access changes discriminability
physical Effect != controller acknowledgement
physical continuity requires recoverable configuration/provenance
```

Do not promote `Lab`, `Embodiment`, `PhysicalState`, `InstrumentGraph`, or another architecture noun merely because the research direction is strategically important.

## Current conclusion

The old Ordivon Computer programme asked whether Agents require a rebuilt computing stack. That question was productive but increasingly too software-centric.

The stronger current model is:

> **A finite intelligence's effective computational capability is partly constituted by the representations, instruments, authority boundaries, continuity structures, and physical interfaces through which it can observe and intervene in Reality. Ordivon Computer should study and stress-test this computational embodiment while continuing to inherit mature mechanics and refusing universal ownership without evidence.**

The future laboratory is therefore not merely an expansion below the software layer. It is a candidate environment in which Ordivon's existing research on Reality, representation, currentness, consequence, evidence, continuity, Security, and Computational Possibility can become directly testable against the physical world.


---

## Post-revision PPD correction — capability environment and infrastructure capital

The subsequent Constructive Capability Environment closeout narrows several speculative parts of this working revision. The full evidence map and falsifiers live in [`CONSTRUCTIVE-CAPABILITY-ENVIRONMENT-CLOSEOUT-20260825.md`](CONSTRUCTIVE-CAPABILITY-ENVIRONMENT-CLOSEOUT-20260825.md).

The most important corrections are:

```text
EnvironmentChange != CapabilityChange
FrontierExpansion != InfrastructureCapital
LatentAffordance != RealizedCapability
MoreRawActions != MoreValidCapability
AssetExists != CurrentCapability(target,time)
CapabilityInstance != CapabilityProductionMechanism != ReconstructibleOption
```

The Atlas × Host × Harness continuity hypothesis was reduced by a strong generic control: indexed retrieval plus a generic typed policy compiler reproduced the tested successor advantage at 33/33. The surviving lesson is not a unique persistent-intelligence substrate but **responsibility-preserving reactivation**: recover current load-bearing premises from their owners, retain history without lifting it into current authority, preserve unresolved effects/obligations, and recompile the next affordance.

The strongest positive infrastructure lineage is instead Workstation `isolated-equipment`: later Game workloads reused and adapted the same signed isolated construction mechanism while individual Security/Game roots were allowed to expire. This supports a reconfigurable-capital model in which durable value may sit in the trustworthy ability to form an environment again, rather than in permanently active instances.

A current Game deletion probe also confirms that constraints can be capability-enabling: Team policy removes a primitive-legal Security pickup that would strand the only sealant on an Actor without `seal_hull`, preserving future joint reachability. Classical safe-state/deadlock-avoidance theory absorbs the general mechanism, so this does not admit a new institutional or Normative theory.

For the laboratory horizon, the resulting correction is:

> **Prefer the smallest trustworthy, source-neutral way to create the observation/action/evidence environment required by the current Reality pressure. Let repeated heterogeneous use decide which reconfiguration, calibration, fixture, fabrication, continuity, or control mechanisms deserve durable infrastructure standing. Allow target-specific realizations to expire when current Reality no longer justifies their carrying cost.**

This correction does not create a Lab owner, Capability Registry, Instrument Graph, global currentness service, or physical-control layer.


---

## Second post-revision correction — civilization-mediated reachability

A subsequent 2026-08-26 world-model audit exposed one remaining software/locality bias that the capability-pressure law did not make explicit enough. The full bounded analysis is recorded in [`CIVILIZATION-MEDIATED-REACHABILITY-WORLD-MODEL-REVISION-20260826.md`](CIVILIZATION-MEDIATED-REACHABILITY-WORLD-MODEL-REVISION-20260826.md).

The correction is not that external services are useful; the Constructive Capability Environment closeout already established source-neutral construction. The stronger correction is a search prior:

```text
Human-civilization-realized capability
→ candidate reachability pressure
```

rather than:

```text
Human-civilization-realized capability
→ current Ordivon capability
```

or:

```text
not locally owned / not in a current owner
→ unreachable
```

Mature make-or-buy / transaction-cost economics, distributed-cognition work, current on-demand manufacturing and remote cloud laboratories strongly subtract novelty from the broad idea that functional capability can cross organizational and ownership boundaries. The Ordivon residual is therefore only a finite-consumer judgment discipline: before closing a target as outside the system, search for source-neutral carrier paths and identify the actual blocker.

This adds one working world-model standing:

### WM-COMP-R9 — Ownership/domain boundaries are not reachability boundaries

For a target already robustly realized somewhere in human civilization, absence of a local implementation is weak evidence of impossibility. Treat the target as a candidate reachable capability, then distinguish:

```text
CandidateReachable
!=
PathQualified
!=
RealizedCurrentCapability
```

and classify the actual blocker: logical/physical/formal, causal-information, computational/resource, knowledge/method, capital/equipment/facility, supply/latency, precision/metrology, interface/integration, authority/safety/legal, or transaction/coordination.

The revised expansion law becomes:

```text
important target
→ reject premature domain/ownership closure
→ search civilization-scale source-neutral carriers
→ classify blockers
→ choose strongest admissible current path
→ construct only the residual
→ verify target consequence
→ preserve the cheapest trustworthy route back
```

This does not create a Reachability owner, Civilization API, global Capability Graph, procurement policy, or guarantee that every human-achievable target is currently affordable, authorized, safe, epistemically recoverable, or computationally tractable.
