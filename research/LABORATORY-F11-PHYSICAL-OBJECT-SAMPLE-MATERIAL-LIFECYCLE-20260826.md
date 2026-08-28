# Ordivon Laboratory F11 — Physical Object, Sample, Material and Consumable Identity/Lifecycle v0.1

Status: **CURRENT FAMILY AUDIT / INSTANCE + STATE + LINEAGE, NOT GLOBAL OBJECT REGISTRY**  
Date: 2026-08-26  
Parent: `research/LABORATORY-PHYSICAL-FALSIFIER-MAP-20260826.md`  
Previous: `research/LABORATORY-F10-FABRICATION-FIXTURES-ASSEMBLY-REWORK-20260826.md`  
Host continuity: `task:ordivon-laboratory-capability-atlas-20260826@21`

## 0. Referent

F11 asks:

> Which physical things need identity, state-history and lineage strongly enough that replacement, modification, consumption, contamination, overload or destruction cannot silently inherit old experimental standing — and what is the smallest local mechanism that preserves this without building a LIMS or universal Object Registry?

F11 is **not**:

- a universal physical-object ontology;
- a Laboratory inventory system;
- a LIMS implementation;
- an ELN replacement;
- a sample-holder standard;
- a global barcode/QR programme;
- a requirement that every screw has an ID;
- a requirement that every object receive a global persistent identifier;
- a second device-identity owner competing with F05;
- a second fixture-geometry owner competing with F10;
- a calibration owner competing with F12;
- a procurement/stock-management system.

The residual is narrower:

```text
physical thing relevant to experiment
→ identify instance/material relation only as strongly as needed
→ preserve current physical-state generation where history matters
→ preserve lineage events that change interpretation
→ bind attempt to the actual thing/state used
```

## 1. Owner subtraction first

F11 should **not own every physical noun** in the Laboratory.

### 1.1 Devices remain F05

Examples:

```text
Pico A
Pico B
NEMA-8 motor M1
load cell L1
camera C1
AD3 A1
```

Their exact physical device identity, attachment generation, provider realization and operational serviceability are already F05 concerns.

F11 consumes those identities when a device becomes part of sample/object lineage, but does not duplicate them.

### 1.2 Fixture geometry remains F10

Examples:

```text
lever radius
hard-stop position
load-cell support geometry
specimen clamp geometry
camera mount pose
```

These are F10 fixture-generation/currentness coordinates.

F11 only adds lineage where a physical fixture part is replaced, modified, damaged or associated with a specimen history in a way that affects evidence.

### 1.3 Measurement qualification remains F12

Examples:

```text
load cell overloaded
reference resistor heated/damaged
DMM calibration expired
```

F11 records the physical event/state transition.

F12 decides whether the measurement chain remains fit for purpose.

### 1.4 Experiment identity remains F04

The experiment attempt manifest should reference the exact specimen/object state used.

F11 does not become an Experiment service.

### 1.5 Therefore the genuine F11 residual

After subtraction, F11 primarily owns planning for:

```text
specimen / coupon identity
material / batch relation
consumable state
object modification lineage
object destruction / discard state
container/holder association where identity is otherwise weak
```

This is much smaller than “all physical objects”.

## 2. Mature external baseline

### 2.1 NIST autonomous-lab sample management is still an active standards problem

NIST's ongoing modular/autonomous laboratory programme identifies four standards areas:

1. sample management;
2. instrument control/communication;
3. data/knowledge management;
4. algorithm/model integration.

For materials R&D, NIST highlights solid sample handling as a special challenge and proposes sample-holder interchange standards spanning:

- sample form factor;
- dimensions;
- number of samples;
- temperature;
- atmosphere;
- instrument compatibility.

Sources:
- https://www.nist.gov/programs-projects/development-standards-support-modular-and-autonomous-laboratory-ecosystem
- https://www.nist.gov/publications/towards-composable-modular-laboratory-ecosystem-autonomous-materials-research-and

Transfer:

```text
universal sample-holder interoperability
= active external standardization problem
```

Therefore Ordivon should not invent its own universal sample-holder protocol for E1.

### 2.2 ASTM E1578-18(2026) — laboratory informatics is broader than one LIMS

The current ASTM E1578-18(2026) guide explicitly treats the laboratory-informatics landscape as including:

- LIMS;
- LES;
- LIS;
- ELN;
- SDMS;
- CDS;
- integrations with external systems.

It also states that selecting an informatics solution requires detailed laboratory requirements rather than simply choosing a product category.

Source:
https://store.astm.org/e1578-18r26.html

Transfer:

```text
need sample traceability
!= automatically need LIMS
```

A small laboratory should earn the informatics layer from workload pressure.

### 2.3 IGSN / DataCite — mature global persistent IDs for physical samples

DataCite currently defines IGSN IDs as globally unique persistent identifiers for physical/material samples.

They can identify:

- an individual sample;
- an aggregation of samples;
- a feature-of-interest.

They connect samples to:

- data;
- publications;
- instruments;
- grants;
- people;
- organizations.

Sources:
- https://support.datacite.org/docs/igsn-ids
- https://support.datacite.org/docs/using-igsn-ids

Important F11 lesson:

```text
physical sample identity can be globally persistent
without the physical sample existing forever
```

### 2.4 IGSN explicitly supports ephemeral / destroyed samples

Current DataCite IGSN guidance explicitly notes that samples may:

- be destroyed during analysis;
- be discarded after testing;
- degrade over time;
- exist only temporarily during synthesis/experiment.

The sample's metadata should make its current status clear.

Source:
https://support.datacite.org/docs/igsn-id-use-cases

This strongly supports:

```text
PhysicalExistenceEnded
!=
HistoricalIdentityEnded
```

and:

```text
DestroyedSample
can remain a valid historical referent
```

### 2.5 IGSN PID layer != full local sample metadata layer

DataCite explicitly distinguishes generalized persistent-identifier metadata from richer institution/domain-specific sample metadata layers.

Source:
https://support.datacite.org/docs/harmonizing-datacite-schema-metadata-and-disciplinary-sample-metadata

Transfer:

```text
global PID
!= local complete sample record
```

and conversely:

```text
local experiment sample ID
!= need for global PID
```

### 2.6 Chain of custody is mature when custody matters

FDA laboratory practice treats chain of custody as a sample-handling/identity/integrity process. Current FDA materials require documentation of sample collection/transfer, handling, storage and integrity where regulated evidence demands it.

Sources:
- https://www.fda.gov/science-research/field-science-and-laboratories/field-science-laboratory-manual
- https://www.fda.gov/media/166532/download

NIST's glossary similarly defines chain of custody around tracking movement/handling through collection, safeguarding and analysis.

Source:
https://csrc.nist.gov/glossary/term/chain_of_custody

Transfer:

```text
chain-of-custody discipline
= mature high-assurance mechanism
```

but:

```text
E1 compliant strip on one bench
!= regulated evidence chain by default
```

Do not import forensic bureaucracy without custody pressure.

## 3. Strong F11 distinctions

### 3.1 Logical role != physical instance

```text
specimen = "soft strip"
```

is not enough when two strips have different histories.

### 3.2 Physical instance != material/batch

Two coupons cut from the same polymer sheet may share:

```text
material source / batch
```

but remain different physical instances.

Thus:

```text
SameBatch
!= SameSpecimen
```

### 3.3 Physical instance != physical-state generation

The same coupon can undergo:

```text
pristine
→ loaded
→ plastically bent
→ heated
→ scratched
→ contaminated
→ cut shorter
```

without becoming a different metaphysical object.

But experiment interpretation may require a new state generation.

Thus:

```text
SamePhysicalInstance
!= SameExperimentalState
```

### 3.4 Location != identity

```text
slot 3
bag A
left clamp
bench drawer 2
```

are locators/containers, not the object itself.

### 3.5 Label/fiducial != object

A QR code, AprilTag, handwritten mark or barcode is evidence for identity association.

It is not the physical sample.

### 3.6 Same nominal part != same evidence history

Two M3 levers cut to nominally the same dimensions can differ in:

- exact radius;
- material;
- damage;
- mounting hole placement;
- prior loading.

### 3.7 Consumed != nonexistent history

A resistor that burns out or coupon that breaks can still be referenced by prior attempts.

### 3.8 Inventory equality != experiment equivalence

```text
10 × same part number in drawer
```

does not prove any individual unit is interchangeable for a target after prior use/history.

## 4. Four identity strengths instead of one universal object-ID policy

F11 should not give every physical thing the same identity burden.

### ID-0 — class/stock identity only

Use when individual history does not matter.

Examples:

- unused M3 washer;
- generic jumper wire;
- untouched resistor from a loose assortment used only as a rough DUT;
- disposable cable tie.

Evidence may be:

```text
part class / stock bin / nominal value
```

No unique object ID required.

### ID-1 — attempt-local instance identity

Use when individual instance matters inside one experiment/campaign but not globally.

Examples:

- compliant coupon C03;
- lever L02;
- spring S01;
- one reference resistor used across E0 checks.

Identity can be:

```text
human-readable local label
+ photo
+ attempt/BOM association
```

This is the default first F11 mechanism.

### ID-2 — durable local identity

Use when the object persists across many attempts and history affects future decisions.

Examples:

- repeatedly used load fixture;
- reference component;
- specimen under cyclic tests;
- calibration artifact;
- expensive sample;
- shared custom fixture part.

Possible carrier:

```text
stable local ID
+ physical label/container/fiducial where practical
+ persistent local lineage record
```

### ID-3 — globally persistent/citable sample identity

Use when the sample must survive institutional/project boundaries or enter public research records.

IGSN is a mature candidate for material samples.

Current E1 does **not** justify ID-3.

## 5. Object categories are operational, not universal ontology

For E1 planning, only a few categories matter.

### O1 — durable apparatus component

Examples:

- motor;
- load cell;
- hub;
- camera;
- driver board.

Mostly F05/F10-owned.

### O2 — fixture part / geometry carrier

Examples:

- lever;
- stop bracket;
- specimen clamp;
- base plate.

Mostly F10-owned; F11 preserves replacement/modification lineage when needed.

### O3 — specimen / coupon / material sample

Examples:

- polymer strip;
- spring;
- elastomer coupon;
- foam piece;
- cantilever specimen.

This is F11's strongest early object class.

### O4 — reference object/material

Examples:

- known resistor;
- calibration weight/mass;
- dimensional scale;
- reference coupon;
- reference thermometer later.

History/qualification often matters more strongly.

### O5 — consumable

Examples:

- solder;
- flux;
- adhesive;
- heat-shrink;
- wire;
- abrasive;
- cleaning material.

Usually batch/stock-level identity is enough until chemistry/age changes the target.

### O6 — waste / retired / destroyed object

Physical usefulness ended, but lineage/history may remain important.

These categories are planning aids, not a persisted global type system.

## 6. E1 specimen identity — the first real F11 consumer

Suppose E1 uses several compliant strips:

```text
C01 soft polymer
C02 soft polymer
C03 metal strip
C04 elastomer
```

The key question is not whether all four deserve a permanent database row.

It is:

> Can the experiment later recover which exact physical response history belonged to which specimen?

For early E1:

```text
local specimen label
+ source/material note
+ dimensions when target-relevant
+ photo
+ attempt references
```

is enough.

## 7. Batch/material identity versus specimen identity

A useful two-level relation is:

```text
Material/Stock source
       ↓
individual specimen/coupon
```

Example:

```text
polycarbonate sheet batch/stock P01
→ coupon C01
→ coupon C02
→ coupon C03
```

If C01 is bent repeatedly and C02 remains pristine:

```text
same source material
!= same physical history
```

This allows later inference to distinguish:

```text
between-specimen variation
vs
within-specimen evolution
```

without a LIMS.

## 8. Specimen creation lineage

When a coupon is cut from parent stock, preserve only the lineage needed for the target.

Conceptually:

```text
parent stock/material
→ cut/fabrication event
→ specimen C03
```

Relevant coordinates may include:

- source stock/batch;
- cut dimensions;
- orientation relative to parent material if relevant;
- fabrication method;
- date/attempt;
- photo.

For isotropic hobby material under qualitative E1, orientation may be irrelevant.

For later anisotropic composites/printed parts, orientation may become essential.

Do not universalize it now.

## 9. Modification event versus replacement event

### Replacement

```text
C01 removed
C02 installed
```

New physical instance.

### Modification

```text
C01 cut shorter
```

Same physical lineage, new physical-state generation.

### Damage

```text
C01 cracks
```

Same physical identity may remain, but prior “intact specimen” standing no longer applies.

### Ambiguous change

If uncertain whether a specimen was altered:

```text
state currentness = UNKNOWN
```

Do not silently assume pristine continuity.

## 10. Irreversible experimental history matters

Some experiments leave the specimen materially changed.

Examples:

- plastic deformation;
- fatigue/cyclic damage;
- thermal aging;
- abrasion;
- fracture;
- adhesive curing;
- chemical exposure;
- contamination.

Therefore:

```text
ExperimentAttempt
can produce
ObjectStateTransition
```

The experiment is not only reading Reality; it may consume or transform the object.

This is one reason sample lineage cannot be reduced to inventory location.

## 11. Pristine is a claim, not a default

A newly purchased object may be assumed unused only at an appropriate strength.

After:

- loading;
- overheating;
- dropping;
- contamination;
- visible damage;
- unknown custody;

one cannot silently restore:

```text
pristine=true
```

by moving the object back into its storage box.

## 12. Load cell overload is a cross-family example

Suppose load cell L1 experiences an unexpected overload.

F11 consequence:

```text
same physical device L1
+ overload event retained
+ post-event state generation differs / may be UNKNOWN
```

F05 consequence:

- device identity still L1;
- attachment may remain current.

F12 consequence:

- prior calibration/measurement validity may need re-check.

This is exactly why one `DeviceReady=true` bit would be wrong.

## 13. Motor/actuator overload/damage similarly separates owners

NEMA-8 motor M1 may:

- stall;
- heat;
- have shaft slip/damage;
- accumulate wear.

F11 only records decision-relevant physical event/state lineage.

F09/F05 decide continued actuation serviceability.

No universal health model is required.

## 14. Lever replacement / revision

F10 already says lever radius affects force geometry.

F11 adds:

```text
lever L1 rev/state A
→ hole redrilled / contact point moved
→ lever L1 state B
```

or:

```text
lever L1 removed
lever L2 installed
```

The first is lineage modification; the second is replacement.

Both can invalidate prior geometry assumptions.

## 15. Fiducial labels are useful but not authoritative alone

For E1 specimens, labels may be:

- handwritten ID;
- small printed QR/DataMatrix;
- AprilTag/ArUco if visually useful;
- container label when specimen itself is too small.

But labels can:

- detach;
- move;
- be copied;
- be placed on the wrong object.

Therefore a strong local association can combine:

```text
label
+ photo
+ physical geometry/context
+ attempt history
```

rather than trusting one sticker as metaphysical truth.

## 16. Tiny/unlabelable specimens

When direct labeling would alter the specimen or is impractical:

use:

```text
labeled container / holder / slot
+ photo/map of position
+ controlled transfer event when moved
```

This is where container identity becomes useful.

Again:

```text
container slot
!= specimen identity
```

but it can be strong evidence when custody is controlled.

## 17. Container/holder identity

For E1-v0, sample holders should remain simple:

- bag/envelope;
- small labeled box;
- clamp position;
- tray slot;
- specimen rack if later useful.

A holder needs durable identity only when:

- multiple specimens can be confused;
- holder geometry influences measurement;
- transfer between instruments occurs;
- contamination/storage state matters.

NIST's work shows universal holder interoperability is a much larger unsolved standards problem; E1 should not pretend to solve it.

## 18. Location currentness

Physical location is useful operationally but should not bear identity authority.

Example:

```text
C03 last known location = tray slot B4
```

If a Human moves it:

```text
identity C03 remains
location becomes stale
```

If slot B4 now contains C04:

```text
slot equality
!= identity continuity
```

This is the physical analogue of F05 locator != identity.

## 19. Consumables — batch identity only when target-relevant

A Laboratory can drown in consumable metadata.

For early E1:

### likely no unique identity

- cable tie;
- M3 screw;
- generic jumper wire;
- solder length;
- heat-shrink piece.

### batch/source may matter later

- adhesive;
- flux;
- solder alloy;
- polymer filament;
- resin;
- chemical reagent;
- calibration/reference material.

Rule:

```text
record batch/lot only when batch variation / age / storage can change target conclusions
```

Do not barcode each washer.

## 20. Reference components deserve stronger treatment

A reference object is not merely another specimen.

Examples:

- resistor used to check measurement chain;
- known mass used to check force sensor;
- printed dimensional scale;
- gauge/reference coupon.

Its history matters because future experiments use it to challenge other evidence.

Therefore many reference objects should enter at least ID-2 durable local identity.

Possible retained fields:

- stable local ID;
- source/model/nominal value;
- stronger calibration/qualification reference in F12;
- damage/overload/aging events;
- storage condition when material;
- replacement history.

## 21. Destructive test lineage

Suppose specimen C05 is loaded until fracture.

Correct representation:

```text
C05 existed
→ attempts A1..A4 loaded C05
→ A5 fractured C05
→ physical intact specimen no longer available
→ fragments may or may not receive child identities if future work uses them
```

Historical data remains tied to C05.

This matches IGSN's explicit support for destroyed/ephemeral samples.

## 22. Child/derived sample lineage

A derived object needs a new identity only if it becomes a separately manipulable experimental object.

Example:

```text
parent coupon C05
→ cut into two pieces
→ C05-A and C05-B
```

if both are later tested separately.

But microscopic debris that is discarded does not need object identities.

Likewise:

```text
parent stock P01
→ coupon C01
```

is useful lineage.

Do not build infinite material genealogy.

## 23. Aggregation identity

Sometimes the experimental object is an aggregation:

- bag of powder;
- batch of screws used statistically;
- set of coupons;
- collection of fragments.

IGSN supports sample aggregations globally, confirming this is a mature identity pattern.

For Ordivon local E1, aggregation identity is only needed if the group itself is the unit of inference.

## 24. Contamination as a state transition

Contamination can matter even when no object is visibly damaged.

Examples:

- oil on compliant strip;
- adhesive residue on contact surface;
- solder flux affecting electrical reference;
- dust on optical fiducial;
- foreign material on load-cell contact.

If contamination could alter the target:

```text
clean-state standing no longer transfers automatically
```

Possible responses:

- clean and requalify;
- mark contaminated state;
- retire specimen;
- use as a deliberate perturbation.

## 25. Cleaning is also a physical transformation

A cleaning procedure may:

- remove contamination;
- alter surface;
- add solvent residue;
- change mass/moisture;
- damage labels.

Therefore:

```text
cleaned
!= automatically pristine
```

This becomes important later in chemistry/materials/biology, but E1 can keep it lightweight.

## 26. Storage matters only when it changes the object

Do not create a universal environmental-storage system for every object.

Storage becomes F11/F13 relevant when:

- humidity affects material;
- temperature affects reference material;
- light ages sample;
- battery charge/state matters;
- contamination risk matters;
- expiry/shelf life matters.

For inert E1 aluminum/steel hardware, ordinary labeled storage is enough.

For polymer/elastomer coupons, ambient history may later become an influence quantity if experiments become quantitative.

## 27. Attempt-local object manifest is currently sufficient

The first E1 campaign can use a small immutable object section in the attempt manifest or adjacent artifact.

Conceptually:

```text
role
localObjectId
instance/batch/source relation where relevant
stateGeneration / state note
fixture relation
label/photo refs
parent/derived relation where relevant
known damage/modification events
post-attempt disposition
```

This is a **conceptual minimum**, not a recommendation for a universal schema.

## 28. Example — E1 attempt object cut

```text
controller       → Pico A / F05 binding
actuator         → motor M1 / F05 binding
force observer   → load cell L1 / F05+F12
lever            → lever L02 / F10 geometry rev 3
specimen         → coupon C07 / source P01 / state pristine-at-start
reference object → mass R01 / F12 qualification
```

After experiment:

```text
C07 state → cycled-20x / visible permanent bend
L02 state → unchanged
L1 state  → no overload observed
```

Next attempt must not silently call C07 pristine.

## 29. Local label strategy

Current recommendation:

### Human-readable first

Use short IDs:

```text
C01, C02... specimens
L01... levers
R01... references
F01... fabricated fixture parts when needed
```

Avoid collision with device identities by context/role.

### Machine-readable optional

Use QR/DataMatrix/AprilTag only when:

- repeated scanning/vision association helps;
- Human transcription error becomes material;
- object transfer count rises;
- visual pose/identity already benefits from fiducials.

Do not add scanner infrastructure before this pressure exists.

## 30. When a local object gets a durable record

Promotion from attempt-local ID to durable local identity should happen if several conditions hold:

1. reused across multiple attempts;
2. individual history affects interpretation;
3. replacement would invalidate standing;
4. the object is expensive/scarce/slow to recreate;
5. calibration/reference history matters;
6. state transitions accumulate over time;
7. multiple Agents/Humans need to recover its history;
8. it travels across fixtures/loci.

Otherwise leave it attempt-local or batch-level.

## 31. When IGSN becomes useful

IGSN should be considered only if Ordivon begins producing/holding material samples that need:

- citation in papers/data;
- cross-institution exchange;
- durable public discovery;
- long-lived identity beyond one local Laboratory;
- explicit links to datasets/publications/instruments/people.

That is a future materials/chemistry/biology/domain pressure.

Current E1 coupons do **not** need IGSN.

## 32. LIMS promotion gate

A LIMS or LIMS-like persistent sample substrate becomes earned when attempt-local artifacts stop being enough.

Potential triggers:

- dozens/hundreds of live samples;
- repeated transfers between instruments/loci;
- scheduling based on sample state;
- custody/access constraints;
- storage/expiry monitoring;
- aliquot/derivation trees;
- contamination/cleanroom constraints;
- high-throughput automation;
- regulated/quality-system needs;
- many concurrent campaigns;
- Humans/Agents repeatedly fail to reconstruct sample history from attempt-local records.

Until then:

```text
LIMS = NOT EARNED
```

## 33. Sample holder standard promotion gate

A local standardized holder/interface becomes useful when multiple instruments/robots must consume the same physical sample without bespoke remounting.

Triggers:

- same specimen repeatedly moves camera ↔ force rig ↔ microscope ↔ other instrument;
- remounting changes geometry/contamination enough to dominate error;
- robotic handling needs graspable standardized interfaces;
- sample transfer latency becomes a bottleneck;
- holder must preserve temperature/atmosphere/orientation.

This should follow mature external standards as they emerge rather than pre-empt them.

Current E1:

```text
one clamp + one specimen geometry
```

is enough.

## 34. Physical-object identity is evidence-relative

A scratched handwritten mark may be sufficient for one local strip.

A serial number may be sufficient for a motor.

A container label may be sufficient for powder.

A globally registered IGSN may be appropriate for a published material sample.

Thus:

```text
IdentityStrength
should match
ConsequenceOfConfusion
```

not technological elegance.

## 35. F11 falsifiers

### F11-F1 — same batch, different specimen

Cut C01 and C02 from the same stock.

Load C01 repeatedly; leave C02 pristine.

Expected:

```text
same material source
but different specimen histories
```

No evidence transfer from C01 damage to C02 state or vice versa.

### F11-F2 — same specimen, changed state

Use C01 for repeated loading until permanent deformation appears.

Expected:

```text
same object identity
new state generation
```

and old pristine standing does not remain current.

### F11-F3 — replacement at same location

Put C01 in clamp slot, then replace with C02 without changing fixture role/location.

Expected:

```text
location unchanged
object identity changed
```

### F11-F4 — label swap

Safely move/swap labels between two noncritical test objects.

Expected:

identity resolution should not trust the label alone if photo/context/history contradicts it.

### F11-F5 — destruction

Fracture/discard C03 after its final experiment.

Expected:

```text
physical object unavailable
historical identity/data remain resolvable
```

### F11-F6 — load-cell overload event

Create only a bounded safe overload test if F12/F02 later approve the exact protocol, or use an equivalent non-destructive qualification perturbation.

Expected conceptually:

```text
same device identity
but qualification state no longer inherited blindly
```

Do not deliberately damage expensive hardware merely to satisfy the falsifier if a safer surrogate exists.

### F11-F7 — container/location mismatch

Move one labeled specimen to another slot/container.

Expected:

```text
object identity survives
location currentness changes
```

### F11-F8 — derived sample

Cut one specimen into two pieces and use both later.

Expected:

```text
parent relation preserved
child instances distinct
```

only if both pieces become real future experimental objects.

### F11-F9 — object-record deletion test

Run first E1 using only attempt-local labels/photos/BOM + F05/F10 identities.

If a fresh Agent can recover object history without a persistent shared service:

```text
Object Registry / LIMS remains deleted
```

### F11-F10 — durable-ID promotion

Reuse one reference specimen/object across enough attempts that reconstructing its accumulated history from attempt records becomes materially burdensome.

Only then promote it to durable local identity.

## 36. OWN / LOCAL / GLOBAL / DEFER disposition

| Capability | Current disposition | Reason |
|---|---|---|
| attempt-local specimen IDs | **OWN / FIRST** | E1 exact specimen history |
| material/source/batch relation | **OWN WHEN TARGET-RELEVANT** | separates batch vs instance effects |
| specimen state-generation notes | **OWN / FIRST when irreversible history matters** | same specimen can change meaning |
| photos/visual labels | **OWN / FIRST** | low-cost identity evidence |
| QR/DataMatrix/AprilTag scanning | **OPTIONAL / POD** | promote on repeated identification burden |
| durable local reference-object IDs | **OWN-EARLY** | repeated cross-attempt adjudication |
| container/slot IDs | **CONDITIONAL** | only when transfer/confusion pressure exists |
| persistent local object/sample service | **DEFER** | attempt-local evidence currently enough |
| LIMS | **DEFER / NOT EARNED** | no sample fleet/high-throughput/regulatory pressure |
| universal sample-holder standard | **REJECT LOCAL INVENTION / FOLLOW EXTERNAL** | active NIST/external standards problem |
| IGSN global persistent IDs | **DEFER / DOMAIN-PUBLICATION PATH** | mature mechanism, no current E1 need |
| forensic-style chain of custody | **DEFER / REQUIREMENT-DRIVEN** | only if custody/integrity consequence demands it |
| barcode/RFID infrastructure | **DEFER** | no throughput/confusion pressure |

## 37. Positive capability language

### Physical Specimen Continuity Capability

Ordivon can preserve which exact material specimen participated in each experiment and distinguish shared material source from individual physical history.

### Physical-State Lineage Capability

The same object can remain identifiable while its experimentally relevant state changes through loading, damage, modification, contamination, cleaning, aging or consumption.

### Destructive-History Persistence Capability

A sample can be fractured, consumed, discarded or otherwise cease to exist physically while remaining a recoverable historical referent for data and conclusions.

### Replacement Without False Continuity Capability

A new specimen/component can occupy the same role, holder or location without silently inheriting the previous object's evidence or state.

### Identity Escalation Capability

Object identity can progress from stock-level → attempt-local → durable-local → global persistent ID only as confusion consequence, reuse and collaboration pressure increase.

### Sample-Informatics Escalation Capability

Attempt-local manifests remain the default until real throughput/transfer/storage/custody/lineage pressure earns a shared sample substrate or mature LIMS.

## 38. F11 standing

The strongest first mechanism is **not a database**.

For E1:

```text
specimen local ID
+ source/material relation if relevant
+ state-generation note
+ photo/label
+ attempt association
+ parent/derived relation only when real
```

is enough.

Devices continue to use F05 identity.
Fixtures continue to use F10 geometry/currentness.
Measurement validity remains F12.

### Strongest retained distinctions

```text
PhysicalInstance != MaterialBatch
PhysicalInstance != ExperimentalStateGeneration
Location != Identity
Label != Identity
SameRole != SameObject
SameObject != SameQualification
Consumed/Destroyed != HistoricalIdentityLost
Inventory != Lineage
LocalSampleId != GlobalPID
```

### Strongest anti-overbuild result

```text
Physical sample lineage capability
!=
LIMS ownership
```

and:

```text
E1 sample management
= attempt-local evidence first
```

## 39. Next family boundary

F12 — Metrology, Calibration and Reference Chains can now consume concrete F11 object/state identities rather than treating calibration as metadata on device names.

It should answer:

```text
What does it mean for the 500 g load-cell chain to be good enough for E1?
How do we calibrate/check force with known masses without pretending NIST-grade traceability?
How do DMM/reference resistor, camera scale, lever dimensions and ambient influence quantities form target-relative uncertainty?
When does calibration expire or become invalid after overload, remounting or replacement?
Which references should be local, purchased calibrated, or external/shared?
```

F12 should preserve the earlier standing:

```text
Traceability != FitnessForPurpose
```

and make it operational for the first physical experiment.
