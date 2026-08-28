# Ordivon Laboratory F05 — Device Interoperability, Attachment, Identity and Lifecycle v0.1

Status: **CURRENT FAMILY AUDIT / THIN DEVICE-BINDING SEAM**  
Date: 2026-08-26  
Parent: `research/LABORATORY-PHYSICAL-FALSIFIER-MAP-20260826.md`  
Previous: `research/LABORATORY-F04-EXPERIMENT-ORCHESTRATION-EXECUTION-20260826.md`  
Host continuity: `task:ordivon-laboratory-capability-atlas-20260826@14`

## 0. Referent

F05 asks:

> When an experiment names a role such as `observer`, `stimulus`, `controller`, `positioner` or `camera`, how does Ordivon recover which exact physical device generation currently realizes that role, through which native provider/transport, with which callable features and lifecycle state, without building a universal device ontology or confusing reachability with scientific validity?

F05 is **not**:

- a universal Device Registry;
- a laboratory inventory database;
- a device-class ontology;
- calibration/measurement validity (F12);
- machine safety readiness (F02);
- experiment orchestration (F04);
- real-time control (F03);
- scientific sample/object identity (F11);
- a requirement that every instrument speak one protocol;
- an attempt to replace SCPI/VISA/IVI/SiLA/LADS/EPICS/Ophyd/ROS/vendor SDKs.

The target is a narrow **binding seam**:

```text
experiment-local role / requirement
        ↓
exact currently selected physical realization
        ↓
physical identity evidence
+ attachment/locator generation
+ provider/driver realization
+ feature/capability surface required by this consumer
+ native lifecycle / serviceability observation
        ↓
native command/run identity
```

The binding is evidence about one realization, not ownership of the device's scientific meaning.

## 1. Existing Ordivon standing — internal subtraction

### 1.1 Workstation current source fence

Current source fence:

```text
workstation-lab@8f7ddc7dbb29a36d885d1221db48a344d495cdcb
```

Workstation vNext already states:

```text
NodeAttachmentBinding
!= InstrumentCapability
!= CalibrationValidity
!= MeasurementValidity
!= SafetyAuthorization
!= ExperimentAdmission
```

and proposes a future consumer-driven local attachment projection only for node-local transports such as USB, serial, PCIe or Windows device interfaces.

That local projection may establish:

- node identity;
- transport kind;
- stable physical identity evidence;
- current endpoint/access mode;
- driver/provider/firmware evidence when relevant;
- observed attachment generation/currentness;
- binding digest.

It explicitly must **not** own calibration, scientific capability or experiment semantics.

Therefore F05 does not need a second node-local attachment authority.

### 1.2 Workstation ToolBinding versus physical attachment

Current `equipment_binding.py` has already been recast semantically as ToolBinding / ExecutableBinding.

It proves things such as:

```text
exact executable/provider bytes
provider identity
binding digest
```

It does not prove that a USB oscilloscope is physically attached or that a sensor is serviceable.

Thus:

```text
ToolBinding
!=
PhysicalAttachmentBinding
```

Both can be referenced by one experiment when a vendor driver executable/API is part of the physical realization.

### 1.3 Interlocus current source fence

Current source fence:

```text
ordivon-interlocus@2da7eb39554fb47f4ab2ef2b26e8b72b5b3ae05c
```

Its frozen currentness standing already establishes:

```text
IdentityCurrent
!= HealthCurrent
!= BindingCurrent
!= AdmissionStanding
!= Reachable
!= Serviceable
```

and:

```text
VerifiedCapability ⇏ Reachable
Reachable ⇏ Serviceable
Rebinding != ContinuityPreservation
```

Generation/path/binding changes can begin new exact claim epochs even when stable public names remain unchanged.

Therefore F05 should consume this discipline for remote/cross-locus devices where applicable rather than create `DeviceCurrentnessTheory`.

### 1.4 F04 experiment consumer

F04 has already established:

```text
ExperimentAttempt
!= DeviceRun
```

and requires the attempt manifest to refer to exact current device/object bindings rather than own their lifecycle.

F05 is therefore a provider of **binding evidence to F04**, not an experiment owner.

### 1.5 F12 / F02 boundaries

F05 can say:

```text
device operationally serviceable for feature X
```

without saying:

```text
measurement scientifically valid
or
physical action safe
```

For a measurement instrument:

```text
F05 serviceable
+ F12 measurement qualification
```

may both be required.

For effectful machinery:

```text
F05 serviceable
+ F02 safety readiness
```

may both be required.

Do not collapse these into one `DeviceReady` field.

## 2. Mature external baseline

### 2.1 SCPI — command language independent of transport

The IVI Foundation maintains SCPI as a common software command language between computers and test instruments. SCPI is hardware-independent and can be carried over different instrument interfaces including GPIB, RS-232 and LAN.

Transfer:

```text
instrument command semantics
!=
transport mechanism
```

and therefore:

```text
same SCPI-capable instrument feature
can be reached through different transport realizations
```

without requiring Ordivon to invent its own universal command vocabulary.

Source:
https://www.ivifoundation.org/About-IVI/scpi.html

### 2.2 VISA — resource/session/transport abstraction, not complete physical identity

VISA provides standardized instrument I/O/resource management. A VISA resource descriptor identifies a resource/session endpoint. For USBTMC, the resource string may include vendor ID, product ID and serial number; other descriptors such as serial ports or TCP/IP resources are primarily location/session descriptions.

Examples in the current VISA Library specification include:

```text
ASRL1::INSTR
TCPIP::...::INSTR
USB::vendor::product::serial::INSTR
```

Transfer:

```text
VISA resource descriptor
may contain strong identity evidence
but
resource locator/session identity
!= universally sufficient physical identity
```

The device's own identification, OS attachment evidence and provider state may still matter.

Sources:
- https://www.ivifoundation.org/specifications/default.html
- https://www.ivifoundation.org/downloads/VISA/vpp43_2024-01-04.pdf

### 2.3 IVI drivers — interchangeability is a feature, not identity continuity

The IVI Foundation maintains standardized driver architecture and instrument classes. Its current specification page includes **Generation 2026**, and in February 2026 the Foundation completed an IVI Python specification as part of that generation.

Current IVI instrument classes include common laboratory/test categories such as:

- DMM;
- oscilloscope;
- arbitrary waveform/function generator;
- DC power supply;
- switch;
- power meter;
- spectrum analyzer;
- digitizer;
- counter/timer.

Transfer:

```text
common class API
→ can reduce software change when replacing instruments
```

but:

```text
interchangeable API
!= same physical device
!= same metrological characteristics
!= automatic continuity of calibration/evidence
```

Sources:
- https://www.ivifoundation.org/specifications/default.html
- https://www.ivifoundation.org/2026/02/26/PythonComplete.html
- https://www.ivifoundation.org/About-IVI/Instrument-Classes.html
- https://www.ivifoundation.org/About-IVI/Driver-Architecture.html

### 2.4 OPC UA LADS — Hardware View versus Functional View

LADS v1.0.0 explicitly models two primary views.

**Hardware View** includes:

- devices/components;
- nameplates;
- installation;
- condition monitoring;
- calibration/validation status;
- maintenance-related information.

**Functional View** includes:

- functions;
- sensors/controllers/actuators/timers;
- programs;
- functional units;
- device-level orchestration/result lifetime.

Transfer:

```text
physical asset identity/lifecycle
!=
functional capability surface
```

LADS is a mature candidate when a future analytical/laboratory device supports it. Ordivon should adapt it, not mirror the complete information model into a second ontology.

Source:
https://reference.opcfoundation.org/specs/OPC-30500-1/4.1.2

### 2.5 SiLA 2 — feature-oriented laboratory interoperability

SiLA 2 organizes interaction around Servers and Features. Features expose Commands and Properties and can be dynamically added/removed.

Transfer:

```text
device type taxonomy
<
consumer-relevant feature surface
```

for many automation decisions.

A SiLA Server can therefore be treated as one native provider whose exact Features/Commands are referenced by F05/F04 rather than translated into a universal Ordivon Device class tree.

Source:
https://sila-standard.com/standards/

### 2.6 Ophyd — high-level hardware abstraction above control protocols

Ophyd explicitly describes itself as a hardware abstraction layer between an underlying control communication protocol and Bluesky.

Its interface groups low-level Signals into logical Devices and exposes higher-level operations such as:

- trigger;
- read / describe;
- stage / unstage;
- set / stop;
- configure / read_configuration;
- asynchronous Status;
- flyer kickoff/complete/collect.

Transfer:

```text
protocol-specific driver details
→ adapter-local

experiment-facing operation surface
→ small semantic hardware interface
```

This strongly supports F05 keeping device-specific details behind adapters rather than exposing raw SCPI strings or PV names to every experiment.

Source:
https://blueskyproject.io/ophyd/architecture.html

### 2.7 EPICS asyn / StreamDevice — device type protocol separated from port/bus realization

The current asynDriver documentation (R4-46, July 30 2026) describes asyn as a layer between device-specific code and low-level drivers.

Key distinctions:

```text
port
= physical/logical communication path

device
= instrument connected through a port

device support
= code that interacts with the device

driver
= code that communicates with the port/device
```

StreamDevice goes one step further for message-based instruments: its protocol file describes **one device type's functions** and deliberately does not contain the identity of the individual device or the communication bus. The bus/port/address are bound separately in EPICS records.

Transfer:

```text
device-type protocol semantics
!=
individual physical instance
!=
transport port/address
```

This is almost exactly the distinction F05 needs.

Sources:
- https://epics-modules.github.io/asyn/asynDriver.html
- https://paulscherrerinstitute.github.io/StreamDevice/protocol.html

### 2.8 ROS 2 / ros2_control — managed hardware lifecycle when robotics requires it

ROS 2 managed nodes provide a known lifecycle interface. ros2_control's Resource Manager loads hardware components, manages their lifecycle and exposes state/command interfaces.

Current ros2_control documentation distinguishes states such as unconfigured, inactive and active; active hardware may expose energized/movable command capability, while lifecycle management remains explicit.

Transfer:

```text
process exists
!=
hardware configured
!=
hardware active
```

But ROS lifecycle is a mature robotics-specific carrier, not a universal lifecycle that must be imposed on a DMM or USB camera.

Sources:
- https://design.ros2.org/articles/node_lifecycle.html
- https://control.ros.org/rolling/doc/ros2_control/controller_manager/doc/userdoc.html
- https://control.ros.org/humble/doc/ros2_control/hardware_interface/doc/hardware_components_userdoc.html

## 3. The main F05 subtraction result

There is no missing universal interoperability theory.

External mature systems already cover different cuts:

```text
SCPI          command language
VISA          resource/session I/O
IVI           driver/class interchangeability
LADS          laboratory asset + function model
SiLA          feature/service-oriented lab interface
Ophyd         scientific hardware abstraction
EPICS asyn    port/driver/device-support separation
StreamDevice  device-type protocol separate from bus/instance
ROS2 control  robotics hardware lifecycle/control resources
vendor SDK    device-specific advanced capability
```

Therefore F05 should **compose/adapt**, not replace.

The residual is:

> For one current experiment role, select and bind one exact physical realization strongly enough that replacement, re-enumeration, driver/firmware changes and feature/lifecycle changes cannot silently reuse stale evidence.

## 4. Device identity is not one string

F05 rejects all of these as universal physical identity by themselves:

```text
COM4
/dev/ttyACM0
USB bus path
IP address
DNS name
VISA resource alias
Ophyd Python object name
SiLA server display name
ROS node name
logical role name "scope"
```

Some may be useful locators. They do not universally establish the exact physical unit.

### 4.1 Stable physical identity evidence

Depending on device type, useful evidence may include:

- manufacturer/vendor;
- model/product identifier;
- hardware serial number;
- USB VID/PID + serial;
- device-native UUID;
- controller silicon unique ID;
- certificate/device key identity;
- SCPI/IEEE identification response;
- manufacturer asset identifier.

The strongest available identity should be used **only to the strength required by the target operation**.

A low-consequence disposable sensor may not justify cryptographic identity.

### 4.2 Locator/attachment evidence

Examples:

- USB device path / Windows PnP InstanceId;
- `/dev/ttyACM0` / serial symlink;
- VISA resource descriptor;
- COM port;
- TCP/IP/HiSLIP endpoint;
- EPICS asyn port/address;
- SiLA discovery endpoint;
- ROS hardware plugin/resource path.

A locator answers:

> Where/how can this realization currently be reached?

not necessarily:

> Which immutable physical object is this?

### 4.3 Provider/driver realization

The same physical device can be operated through materially different software realizations:

- vendor SDK;
- SCPI over raw socket;
- SCPI over VISA;
- IVI driver;
- EPICS/StreamDevice;
- Ophyd wrapper;
- SiLA server;
- ROS hardware plugin.

Therefore current device use may depend on exact:

```text
provider/adapter identity
version/digest
configuration
transport realization
```

Workstation ToolBinding can prove exact local executable/provider bytes where those bytes are execution-critical.

### 4.4 Firmware realization

Firmware may alter:

- command semantics;
- bugs;
- timing;
- calibration storage;
- device lifecycle;
- feature availability.

A firmware update need not create a new physical identity, but it can create a new **realization generation** whose old serviceability/evidence does not silently carry forward.

## 5. Use separate identity and generation concepts

F05 should avoid one overloaded `deviceVersion`.

Conceptually distinguish:

```text
PhysicalDeviceIdentity
```

from:

```text
CurrentAttachmentGeneration
CurrentProvider/FirmwareRealization
```

Example:

```text
scope serial S123
USB unplug/replug
same scope serial S123
new Windows PnP path / VISA session
```

Possible interpretation:

```text
physical identity continuity       preserved
exact attachment binding          replaced
```

Another example:

```text
scope serial S123 removed
scope serial S456 attached
logical role still "observer"
```

Then:

```text
physical identity continuity       NOT preserved
role may be rebound after validation
old attempt evidence remains S123 history
```

This is a concrete physical realization of Interlocus:

```text
Rebinding != ContinuityPreservation
```

## 6. Feature/capability surfaces should be consumer-relative

F05 should not answer:

> What can this device do in every possible sense?

It should answer:

> Does this current realization expose the features required by this experiment role?

Example E0 observer requirement:

```text
two analog input channels
common acquisition clock
sufficient bandwidth/sample rate for target
hardware or reliable trigger
raw waveform export
known vertical/time configuration
```

A device can be a perfectly good oscilloscope but fail this particular role if it has only one usable channel or cannot export the required raw data.

Thus:

```text
DeviceClass(scope)
!=
ServiceableFor(E0-B observer requirement)
```

SiLA Features, IVI class capabilities, Ophyd protocols and device-specific adapters are useful ways to expose such surfaces.

## 7. Reachability, connection and serviceability

A robust F05 chain is:

```text
identity evidence current?
        ↓
attachment/binding current?
        ↓
provider/session reachable?
        ↓
native lifecycle allows required operation?
        ↓
required feature surface present?
        ↓
operationally serviceable for this role?
```

Even then:

```text
operationally serviceable
!= F12 measurement valid
!= F02 safe/admissible
!= F04 experiment scientifically admitted
```

### Examples

#### Reachable but not serviceable

```text
*IDN? succeeds
but scope acquisition subsystem errors
```

#### Attached but not reachable

```text
USB device appears in PnP
but vendor driver/session cannot open it
```

#### Reachable and serviceable but not measurement-qualified

```text
DMM reads normally
but required calibration/current uncertainty basis is absent
```

#### Active but safety-blocked

```text
robot controller active
but F02 independent safety veto is open
```

## 8. No universal device lifecycle state machine

Different mature carriers have different lifecycle semantics.

### Simple SCPI/VISA instrument

May effectively be:

```text
discovered
→ session open
→ identified
→ configured
→ operation/query
→ session close
```

### SiLA

Uses Server/Feature/Command-specific lifecycle and asynchronous Command Execution identities.

### LADS

Provides device status/state machinery, functional units and programs.

### Ophyd

May expose connected state plus stage/unstage, trigger/read, set/stop and Status completion.

### ROS2/ros2_control

May have formal:

```text
unconfigured
→ inactive
→ active
→ finalized
```

The F05 rule is:

> Preserve and reference the strongest **native lifecycle** of the selected carrier. Project only the consumer-relative question `can this exact realization currently perform the required feature?`

Do not translate every device into one Lab-wide lifecycle enum.

## 9. Native command/run identities should remain native

F04 has already established that one ExperimentAttempt can reference device-native operation identities.

Examples:

- SiLA Command Execution UUID;
- Bluesky/Ophyd Status/Run identity as applicable;
- LADS Program Run/result identity;
- Runtime Job/Attempt wrapping a SCPI/VISA script;
- controller local sequence/run identifier;
- vendor SDK acquisition handle/run ID.

F05 should expose/reference these identities when they matter for recovery.

It should not create:

```text
UniversalDeviceCommandId
```

on top of every native execution identity unless repeated ambiguity proves it necessary.

## 10. Provider selection ladder

No one external standard covers every future Ordivon device.

Use the mature provider with the smallest semantic translation burden.

### P0 — direct mature standardized device interface

Examples:

- SCPI instrument;
- SiLA server;
- LADS OPC UA device;
- mature ROS/EPICS device interface.

Prefer when sufficient.

### P1 — standardized driver layer

Examples:

- VISA + SCPI;
- IVI driver/class;
- EPICS asyn/StreamDevice;
- Ophyd adapter.

Prefer when it materially improves portability, lifecycle, data integration or replacement.

### P2 — vendor SDK

Use when the standard interface does not expose required features or the device is inherently SDK-driven.

Examples can include USB mixed-signal instruments or cameras with rich native APIs.

Bind exact provider/version where decision-relevant.

### P3 — narrow Ordivon/local adapter

Write only when:

- no mature adapter already exists;
- the target feature is concrete;
- a small stable semantic surface will be reused;
- adapter can preserve exact device/native evidence;
- it does not silently create a second device ontology.

### P4 — custom transport/protocol stack

Last resort, justified only when control of that lower layer itself unlocks capability.

Do not descend because raw USB/serial is intellectually attractive.

## 11. SCPI/VISA is likely first-class for conventional bench instruments

For future conventional benchtop instruments such as:

- oscilloscopes;
- DMMs;
- programmable supplies;
- AWGs;
- electronic loads;

SCPI/VISA or a vendor-supported equivalent should be the first interoperability candidate where supported.

Advantages:

- mature cross-vendor command conventions;
- transport independence;
- widespread Python/C/.NET tooling;
- resource/session abstraction;
- existing replacement/interchangeability ecosystem through IVI.

But F05 should not require VISA/SCPI if:

- a device's best supported API is vendor SDK;
- direct socket SCPI is simpler and equally strong for the exact consumer;
- IVI driver adds no useful abstraction;
- a higher-level SiLA/LADS/Ophyd/EPICS integration already exists.

No standard is mandatory by symmetry.

## 12. Current local Reality — negative baseline

A fresh 2026-08-26 observation found:

### WSL device endpoints

```text
/dev/ttyUSB*   none
/dev/ttyACM*   none
/dev/usbtmc*   none
```

### Windows current PnP cut

Observed relevant devices include:

- integrated USB camera;
- USB hubs/controllers;
- Bluetooth serial COM3 / COM4.

No current lab instrument or MCU attachment was observed.

### Current driver/software carriers

In the current WSL Python environment, the bounded probe found no installed:

```text
pyvisa
pyserial
ophyd
bluesky
sila2
epics Python module
```

The bounded Windows uninstall-registry probe found no matching installed package names for common VISA/NI/Keysight/Tek/RIGOL/SIGLENT/Digilent/WaveForms/Pico/Arduino/STM32/ESP-IDF carrier software.

Interpretation limits:

- absence from this probe does not prove no relevant DLL/portable tool exists anywhere;
- it is sufficient to say there is **no current proven first-path lab driver stack**;
- therefore no driver platform should be installed before F06 exact hardware pressure selects one.

This is a useful clean baseline.

## 13. Minimal F05 binding for F04 O0/O1

The first experiment attempt does not need a shared Device registry.

A local immutable attempt manifest can reference a conceptual binding containing only the target-relevant coordinates.

### 13.1 Role

```text
role = controller / observer / reference-meter / actuator / camera / ...
```

Role is experiment-local meaning, not device identity.

### 13.2 Physical identity evidence

Use the strongest available evidence required for the target:

```text
manufacturer/model/serial
USB VID/PID/serial
native unique ID
SCPI ID response
or equivalent
```

### 13.3 Attachment realization

```text
local node or remote locus
transport kind
current locator/session endpoint
OS/native attachment evidence
observed generation/currentness
```

Node-local USB/serial evidence can be Workstation-owned.

Remote/network device binding may be Interlocus/World/device-owner relative.

### 13.4 Provider realization

```text
adapter/driver type
provider identity/version/digest when relevant
native API/protocol
```

### 13.5 Required feature surface

Record only the features the attempt relies on.

Example:

```text
role: observer
requires:
  - capture_two_analog_channels_common_clock
  - configure_sample_rate
  - configure_trigger
  - export_raw_waveform
```

### 13.6 Current operational serviceability

Evidence that the current realization can provide the required feature at admission time.

This is separate from calibration/safety.

### 13.7 Native operation identity

When a physical device operation is launched, preserve the native run/command identity if it exists and matters to recovery.

## 14. Example — E0 controller binding

Suppose E0 uses a Pico-2-class board.

The attempt role is:

```text
controller
```

A useful F05 binding might establish:

```text
physical board identity / serial or silicon UID if available
current USB attachment generation
firmware digest/version
host-side serial/USB provider binding
required features:
  - one bounded digital stimulus output
  - optional hardware trigger output
  - local sequence number/status query
```

It does **not** need to claim:

- general-purpose MCU capability ontology;
- every peripheral on RP2350;
- scientific validity;
- safety authorization.

## 15. Example — E0 observer binding

Suppose E0 observer is a conventional scope or mixed-signal instrument.

Role requirement might be:

```text
observer
```

with:

```text
two analog channels
common sample clock
sufficient target bandwidth/rate
hardware trigger or equivalent
raw waveform export
queryable acquisition configuration
```

The physical realization may be:

```text
SCPI/VISA scope
```

or:

```text
vendor-SDK USB mixed-signal instrument
```

F04 should not care which transport family is used once F05 provides the exact binding/feature/currentness evidence.

## 16. Example — reference meter can remain manual initially

F05 does not require automation for every instrument.

A simple independent DMM/reference check may initially be:

```text
physical device identity
+ current calibration/qualification reference later from F12
+ manual observation captured as experiment evidence
```

If no repeat/latency pressure exists, there is no reason to integrate its remote API merely for completeness.

This supports:

```text
Interoperability capability
!=
100% device automation
```

## 17. Binding transition cases

### 17.1 Same device, USB re-enumeration

```text
physical identity S123
old endpoint /dev/ttyACM0
unplug/replug
new endpoint /dev/ttyACM1
```

Correct result:

```text
physical identity may remain S123
old exact attachment binding becomes historical/not-current
new binding requires current observation
```

Do not silently edit the old record.

### 17.2 Same logical role, replacement device

```text
observer role
scope S123 removed
scope S456 installed
```

Correct result:

```text
new physical identity epoch
new attachment binding
new provider/serviceability evidence as needed
F12 measurement qualification re-evaluated separately
```

The experiment may accept the replacement if its requirement allows it, but exact continuity is not preserved.

### 17.3 Same physical device, firmware update

```text
serial S123 unchanged
firmware v1 → v2
```

Physical identity remains.

But target-relevant realization may require new:

- feature/serviceability verification;
- provider compatibility check;
- calibration/validation check in F12;
- safety validation in F02 for effectful devices.

### 17.4 Same physical device, driver/provider update

```text
instrument S123
vendor SDK 1 → SDK 2
```

The device identity is stable, but exact software realization changed.

Workstation ToolBinding/provider evidence should prevent historical provider success from silently proving current serviceability.

### 17.5 Same network device, IP change

```text
stable device identity
old IP → new IP
```

Locator changes.

If device-native identity and secure/current re-resolution prove the same unit, broad physical continuity may remain while exact endpoint binding changes.

### 17.6 Same address, different device

The dangerous inverse:

```text
COM4 / IP / USB bus path unchanged
physical device replaced
```

Locator equality must not preserve exact physical identity.

## 18. Device discovery is not admission

F05 distinguishes:

```text
discovered candidate
!=
identified current realization
!=
bound role
!=
serviceable for operation
```

Examples:

- VISA resource manager lists three devices;
- SiLA discovery finds a Server;
- mDNS finds a scope;
- Windows PnP lists a USB device;
- ROS graph lists a node;
- EPICS PVs respond.

These are discovery evidence.

An experiment should still explicitly bind the selected realization to its role and requirement.

This is directly analogous to Workstation's earlier candidate-discovery versus admission/current-effect distinction.

## 19. Interchangeability and replacement

IVI demonstrates that software interchangeability can be deliberately designed.

F05 should exploit this without overclaiming.

### Syntactic/driver interchangeability can preserve

- high-level API shape;
- common instrument-class operations;
- experiment software structure.

It cannot automatically preserve:

- channel count;
- range/bandwidth;
- noise/accuracy;
- trigger behavior;
- timing latency;
- calibration status;
- fixture interaction;
- exact raw data format;
- safety behavior.

Therefore a role requirement should be **feature/contract relative**, and F12/domain validation should decide whether replacement is acceptable.

## 20. Device capability probing

Do not probe every feature merely because an API allows it.

### Safe/read-only first

Prefer:

- identity query;
- model/firmware query;
- feature/capability enumeration;
- status/health query;
- configuration read;
- non-effectful self-description.

### Bounded operational probe when needed

If feature serviceability cannot be proven without action, use the cheapest low-consequence test that directly exercises the required function.

Example:

```text
scope acquisition role
→ capture a known low-voltage calibration/test signal
```

rather than simply trusting that `*IDN?` works.

### Do not use self-test as universal truth

A device self-test can support device health but does not prove the complete experiment role or measurement validity.

## 21. Serviceability projection — thin and operation-relative

A conceptual F05 decision projection might ask:

```text
roleRequirementId
physicalIdentityCurrent
attachmentBindingCurrent
providerRealizationCurrent
nativeLifecycleState
requiredFeatureSurfaceSatisfied
operationalServiceable
observedAt
```

It should explicitly exclude:

```text
measurementValidity
safetyAdmission
scientificAcceptance
```

This is an ephemeral consumer projection, not a recommendation for a global schema.

## 22. Native lifecycle versus broad serviceability

A mature carrier lifecycle may be necessary but not sufficient.

Example ros2_control:

```text
hardware ACTIVE
```

may be necessary for motion, but F05 may still reject a specific experiment role if:

- wrong device generation;
- required interface absent;
- driver mismatch;
- feature self-check fails.

Conversely a passive measurement device may have no formal `ACTIVE` state at all and still be fully serviceable.

Therefore:

```text
NativeLifecycleState
!=
OperationalServiceabilityFor(role)
```

## 23. Currentness policy should be event/role-driven, not one TTL

No universal `device binding freshness = 30 seconds` is justified.

Revalidation triggers include:

- physical unplug/replug;
- USB/PnP/serial endpoint change;
- network endpoint/re-resolution change;
- provider/driver process restart where material;
- firmware update;
- device reboot;
- Workstation/OS restart if attachment identity can change;
- experiment pause/resume across long interval;
- F04 Agent replacement before new consequence;
- failed operation indicating possible device state drift;
- safety/calibration changes in their own owners.

If none occurs and the native carrier proves stable current session identity, repeated full discovery may be unnecessary.

## 24. Security boundary

Device interoperability adds meaningful attack/authority surfaces.

Questions include:

- can another process send raw SCPI/device commands around the experiment adapter?
- can a network instrument be addressed from untrusted segments?
- can firmware/driver/provider identity change without evidence?
- does an uploaded SiLA/ROS/EPICS component expose broader commands than the admitted role?
- are instrument credentials/certificates scoped appropriately?
- can a stale endpoint be rebound to a different device?
- can a device server advertise a misleading identity/feature surface?

Security may protect transport/provider/authentication/integrity.

But:

```text
securely authenticated device
!=
scientifically valid device
```

and:

```text
SCPI socket reachable
!=
permission to send arbitrary commands
```

Experiment-facing adapters should expose the narrowest needed operation surface where practical.

## 25. Human/operator boundary

Human remains useful for:

- physical serial/nameplate inspection;
- cable/device replacement;
- confirming which physical unit is connected when electronic identity is weak;
- pairing a device with its fixture/probe/accessory;
- resolving ambiguous attachment during first integration.

Human observation should be recorded only at the strength it supports.

Example:

```text
Human visually confirms serial S123
+ device query returns S123
```

is stronger than either weak locator alone.

But Human does not automatically determine serviceability or measurement validity.

## 26. F05 physical falsifiers

### F05-F1 — same logical role, different physical device

Bind `observer` to device S123.

Replace with S456 while keeping the same logical role and, if possible, similar endpoint naming.

Expected:

```text
old exact binding NOT_CURRENT
new binding required
old attempt evidence remains S123 history
```

Any silent continuity is F05 failure.

### F05-F2 — same physical device, new locator

Unplug/replug the same USB device so its OS/VISA/serial locator changes.

Expected:

```text
physical identity may remain continuous
exact attachment generation changes
new current binding formed
```

This tests locator != identity.

### F05-F3 — reachable but not serviceable

Keep communication/identity query working while making one target feature unavailable or invalid at the device-functional layer.

Expected:

```text
Reachable=true
OperationalServiceableFor(role)=false/unknown
```

### F05-F4 — provider/driver replacement

Keep the same hardware but change the adapter/driver version or path.

Expected:

```text
physical identity stable
provider realization generation changes
serviceability revalidated
```

Historical driver success must not transfer silently.

### F05-F5 — firmware update

Update controller/device firmware under the same physical serial.

Expected:

```text
physical identity stable
realization generation changes where target-relevant
feature/serviceability evidence refreshed
```

F12/F02 requalification may also be triggered but remains separately owned.

### F05-F6 — discovery versus admission

Expose at least two discoverable candidate devices.

Experiment must not silently choose based on first enumeration order.

Expected:

```text
explicit requirement-relative binding
```

### F05-F7 — native lifecycle state matters

For a device/controller with explicit lifecycle, keep endpoint reachable while transitioning it to a state where the required operation is unavailable.

Expected:

```text
reachable but not serviceable
```

### F05-F8 — mature carrier parity

Implement one conventional instrument through its mature native stack (e.g. SCPI/VISA or vendor driver) and test whether any proposed Ordivon-specific device layer adds a recovery/currentness capability not already obtained by a thin binding adapter.

If not, delete the extra layer.

### F05-F9 — registry deletion test

Recover E0 after Agent replacement using only:

- attempt manifest;
- current Workstation/Interlocus/device observations;
- native driver/device identity;
- adapter configuration.

If sufficient, a global Device Registry remains unearned.

### F05-F10 — equivalent instrument replacement

Where two instruments satisfy the same role contract, swap devices and test:

```text
experiment software mostly preserved
+ binding/measurement qualification refreshed
```

This distinguishes useful interchangeability from false identity continuity.

## 27. Implementation ladder

### D0 — native device call + attempt-local metadata

Use when one device is simple and stable.

Example:

```text
SCPI script + exact VISA resource/ID + Runtime Job + raw artifact
```

No shared F05 code.

### D1 — narrow adapter + exact binding observation

Use when an experiment repeatedly needs the same semantic features or recovery logic.

Examples:

- `ScopeObserver` adapter;
- `PicoStimulusController` adapter;
- `ProgrammableSupply` adapter.

Adapter hides native protocol details and emits target-relevant identity/currentness/serviceability evidence.

### D2 — mature external hardware abstraction

Use Ophyd/EPICS/SiLA/LADS/ROS/IVI when ecosystem value exceeds a small local adapter.

Do not wrap it again merely for Ordivon naming consistency.

### D3 — shared Ordivon binding carrier

Promote only if **multiple heterogeneous device families** repeatedly require the same node/cross-locus binding mechanism and Workstation/Interlocus/native carrier composition creates real duplicated failure/recovery burden.

This may eventually justify a narrow shared binding object/surface, but not a universal device ontology.

### D4 — device inventory/control plane

Not earned. Requires real fleet/inventory/maintenance/resource-management pressure.

## 28. OWN / ADAPT / DEFER disposition

| Capability | Disposition | Current reason |
|---|---|---|
| physical device identity evidence | **OWN AS ATTEMPT/BINDING EVIDENCE** | needed for PF-06/F04 recovery |
| node-local attachment currentness | **WORKSTATION CONSUMER-DRIVEN** | already correct owner seam |
| cross-locus binding/serviceability | **INTERLOCUS / OWNER-NATIVE AS APPLICABLE** | existing theory/owner |
| SCPI command interface | **CONSUME** | mature T&M standard |
| VISA resource/session I/O | **CONSUME WHEN USEFUL** | mature transport abstraction |
| IVI drivers/classes | **CONSUME SELECTIVELY** | replacement/interchangeability value |
| LADS | **ADAPT IF DEVICE/FACILITY SUPPORTS** | rich lab device model; no need to mirror |
| SiLA 2 | **ADAPT IF DEVICE SUPPORTS** | feature-oriented lab interface |
| Ophyd/Bluesky hardware abstraction | **ADAPT FOR SCIENTIFIC ORCHESTRATION PODS** | mature semantic hardware API |
| EPICS asyn/StreamDevice | **ADAPT FOR FACILITY/CONTROL PODS** | mature port/driver/device-support split |
| ROS2/ros2_control | **ADAPT FOR ROBOTICS PODS** | mature robot hardware lifecycle/control |
| vendor SDK | **CONSUME WHERE BEST NATIVE CARRIER** | many devices require it |
| narrow local device adapter | **OWN ONLY UNDER REPEATED CONSUMER PRESSURE** | acceptable seam, not ontology |
| global Device Registry | **DEFER / NOT EARNED** | no physical fleet/current consumer |
| universal device lifecycle | **REJECT NOW** | native lifecycles differ materially |
| universal device capability taxonomy | **REJECT NOW** | feature/requirement-relative binding is enough |

## 29. Procurement / product-selection consequences for F06

F05 adds several **non-performance** criteria that should influence first instrument selection later.

Prefer hardware with some combination of:

1. stable physical identity (serial/unique ID);
2. documented remote/native API;
3. mature cross-platform driver/provider;
4. raw data export rather than screenshot-only automation;
5. queryable effective configuration;
6. command completion/status semantics;
7. documented error/status model;
8. ability to recover after reconnect without ambiguous hidden effects;
9. standard SCPI/VISA/IVI/SiLA/LADS/EPICS support where useful;
10. provider/software versioning that can be bound reproducibly;
11. vendor lifecycle/support good enough for later replacement;
12. no requirement for cloud-only identity/control when local closed-loop use is sufficient.

These can outweigh marginal headline specifications when the goal is a durable Agent-operated laboratory.

## 30. Current first-device strategy

Because current Reality has no lab instrument/MCU and no first-path lab driver stack, F05 should **not install an interoperability platform now**.

The sequence should be:

```text
F06 selects concrete first controller/instrument realization
→ inspect its strongest native standard/SDK
→ use native provider first
→ bind exact physical identity + attachment/provider generation
→ expose only E0-required features
→ run F05 falsifiers
→ promote shared adapter only if repeated use earns it
```

This preserves a clean system.

## 31. Positive capability language

### Physical Device Binding Capability

Ordivon can determine which exact current physical realization fulfills one experiment role and prevent stale locators/logical names from silently substituting another generation.

### Device Replacement Capability

Ordivon can replace/rebind a physical instrument while preserving protocol/experiment intent where appropriate, without pretending physical identity or measurement qualification continued unchanged.

### Heterogeneous Interoperability Capability

Ordivon can operate devices through different mature native carriers — SCPI/VISA, vendor SDK, SiLA, LADS, Ophyd/EPICS, ROS or narrow local protocols — while exposing a small experiment-facing feature contract rather than forcing one universal protocol.

### Lifecycle-Aware Serviceability Capability

Ordivon can distinguish:

```text
attached
reachable
configured/active where applicable
feature-capable
serviceable for this operation
```

and make current experiment decisions accordingly.

### Adapter Assimilation Capability

A mature external device ecosystem can be incorporated as an Ordivon capability without being rewritten or demoted to raw protocol calls.

## 32. F05 standing

### Core retained chain

```text
ExperimentRole / Requirement
        ↓
PhysicalIdentity evidence
        +
CurrentAttachment / locator generation
        +
Provider / driver / firmware realization
        +
NativeLifecycle observation
        +
RequiredFeature surface
        ↓
OperationalServiceabilityFor(role)
        ↓
Native command/run identities
```

with independent downstream gates:

```text
F12 MeasurementValidity
F02 SafetyAdmission
F04 ExperimentAdmission / MechanicalClosure
```

### Strongest retained distinctions

```text
LogicalRole != PhysicalIdentity
Locator != PhysicalIdentity
PhysicalIdentity != AttachmentGeneration
Attachment != Reachability
Reachability != Serviceability
Serviceability != MeasurementValidity
Interchangeability != IdentityContinuity
NativeLifecycle != UniversalDeviceLifecycle
```

### Current implementation decision

```text
Thin attempt-local binding / narrow adapter = EARNED once first device arrives
Global Device Registry                   = NOT EARNED
Universal capability/device ontology     = NOT EARNED
```

## 33. Next family boundary

F06 — Electronics and Embedded Instrumentation can now select actual first physical carriers without contaminating F05 architecture.

F06 should answer:

```text
Which stimulus/observation/debug/power capabilities are required by E0?
Which should be integrated into one compact device versus independent instruments?
What performance ranges are sufficient for the actual falsifiers?
Which native provider/identity surfaces satisfy F05?
Which measurements need an independent reference path?
```

Only after that should exact products/BOM be promoted from the historical shortlist.
