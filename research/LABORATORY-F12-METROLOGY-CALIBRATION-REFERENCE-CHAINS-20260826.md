# Ordivon Laboratory F12 — Metrology, Calibration and Reference Chains v0.1

Status: **CURRENT FAMILY AUDIT / TARGET-RELATIVE MEASUREMENT AUTHORITY**  
Date: 2026-08-26  
Parent: `research/LABORATORY-PHYSICAL-FALSIFIER-MAP-20260826.md`  
Previous: `research/LABORATORY-F11-PHYSICAL-OBJECT-SAMPLE-MATERIAL-LIFECYCLE-20260826.md`  
Host continuity: `task:ordivon-laboratory-capability-atlas-20260826@22`

## 0. Referent

F12 asks:

> What measurement uncertainty and reference strength are actually required for E1 to distinguish the physical states we care about, how should those requirements reshape the apparatus itself, and when does a measurement chain remain current after remounting, overload, replacement, environmental change or software/provider change?

F12 is **not**:

- a pursuit of maximum precision;
- a metrology-lab completeness project;
- a universal Calibration Registry;
- an assumption that a calibrated instrument yields a valid result in every use;
- a requirement for SI traceability on every exploratory measurement;
- a fixed annual recalibration schedule;
- an assumption that datasheet accuracy equals experimental uncertainty;
- an attempt to make Ordivon a national metrology institute;
- a reason to buy precision bench instruments before the target uncertainty is known.

The operational chain is:

```text
scientific / engineering decision
→ define measurand and decision boundary
→ choose target measurement uncertainty
→ choose measurement model / geometry
→ choose reference and calibration/check method
→ execute with current physical chain
→ produce value + uncertainty / adequacy evidence
→ admit target-relative measurement standing
→ invalidate/recheck on relevant change
```

This order matters.

## 1. Strong external metrology baseline — do not rediscover it

### 1.1 VIM: measurement begins from intended use and target uncertainty

JCGM VIM 2.1 defines measurement as experimentally obtaining quantity values that can reasonably be attributed to a quantity. Its Note 3 is unusually important for Ordivon: measurement presupposes a quantity description commensurate with intended use, a measurement procedure and a calibrated system; the annotation explicitly says one first chooses a **target measurement uncertainty**, then chooses procedure/system so as not to exceed it.

Source:
https://jcgm.bipm.org/vim/en/2.1.html

Transfer:

```text
InstrumentSpecification
is downstream of
DecisionNeed / TargetUncertainty
```

not the other way around.

### 1.2 VIM: calibration is a relation, not an adjustment button

VIM 2.39 defines calibration as an operation that first establishes, under specified conditions, a relation between reference values/uncertainties and indications/uncertainties, then uses that relation to obtain a measurement result from an indication.

It explicitly warns:

```text
calibration != adjustment
calibration != calibration verification
```

Source:
https://jcgm.bipm.org/vim/en/2.39.html

This directly rejects the common embedded-device language where `calibrate()` merely stores a zero or gain setting.

### 1.3 VIM: measurement result normally includes uncertainty

VIM 2.9 says a measurement result is a set of quantity values attributed to a measurand together with relevant information; it is generally expressed as a measured quantity value and measurement uncertainty.

Source:
https://jcgm.bipm.org/vim/en/2.9.html

Thus:

```text
Force = 0.423 N
```

is incomplete as a strong measurement claim when uncertainty is decision-relevant.

### 1.4 Traceability is a property of the result, not the instrument sticker

VIM 2.41 defines metrological traceability as a property of a **measurement result** whereby it can be related to a reference through a documented unbroken calibration chain, each calibration contributing to uncertainty.

Critically, Note 5 says traceability does not ensure the uncertainty is adequate for a purpose and does not ensure absence of mistakes.

Source:
https://jcgm.bipm.org/vim/en/2.41.html

NIST's current policy repeats this directly:

```text
traceability alone does not signify or guarantee fitness for purpose
```

and assigns responsibility for determining adequacy to the user/provider of the measurement result.

Source:
https://www.nist.gov/calibrations/traceability

Therefore the already-established Ordivon standing is externally exact:

```text
Traceability != FitnessForPurpose
```

### 1.5 NIST: merely calibrating an instrument is not enough

Current NIST traceability guidance says merely having an instrument calibrated, even by NIST, is insufficient by itself to make later measurement results traceable; the actual system, procedure, references, uncertainty and measurement assurance must be controlled.

Source:
https://www.nist.gov/metrology/metrological-traceability

This maps directly onto F05/F10/F11 currentness:

```text
calibrated serial number
+ changed fixture/readout/conditions
!= automatically current calibrated measurement chain
```

### 1.6 NIST: no universal recalibration interval

NIST's current calibration-interval guidance does not prescribe one universal interval. It says intervals depend on accuracy need, regulation/contract, inherent stability and environment, and recommends internal measurement assurance/cross-comparison data to establish/refine intervals.

Source:
https://www.nist.gov/calibrations/recommended-calibration-interval

Transfer:

```text
calendar age alone
!= calibration currentness
```

and:

```text
physical event / drift evidence
can be a stronger recalibration trigger than time
```

### 1.7 Singapore already has the external national reference layer

A*STAR National Metrology Centre is Singapore's national metrology institute and maintains/disseminates national measurement standards. Current services include Mass & Force, Electrical, Length & Dimensional, Temperature & Humidity, Optical, Time/Frequency and other areas under ISO/IEC 17025 quality systems and international comparisons.

Sources:
- https://www.a-star.edu.sg/nmc
- https://www.a-star.edu.sg/nmc/Service-Consultancy/CMS
- https://www.a-star.edu.sg/nmc/Research-and-Development/Labs/ML

Current NMC published calibration services include:

- standard mass/dead weights;
- load cells/force transducers/force gauges;
- digital calipers/steel rules/dimensional standards;
- electrical meters/standards;
- temperature/humidity instruments;
- optical and vibration measurements.

Source:
https://www.a-star.edu.sg/docs/librariesprovider20/calibration-and-measurement/website_list-of-services.pdf

Therefore Ordivon does not need to locally own the top of every reference chain.

## 2. Ordivon theory transfer — where F12 genuinely adds value

F12 should consume, not restate, existing Ordivon theory.

### 2.1 Responsibility-relative primacy

For one measurement operation, the relevant primacy is:

```text
Target decision / measurand
first in deciding required uncertainty
```

not:

```text
most accurate owned instrument
first in defining the measurement
```

A ±0.01 °C thermometer does not become primary to E1 if temperature cannot change the decision.

### 2.2 PPD

Metrology pressure should be discovered by asking:

```text
Which measurement ambiguity is currently preventing a discriminating experiment?
```

Then use the cheapest independent Reality pressure that resolves it.

This means the first E1 may require much less absolute accuracy than a future material-property experiment.

### 2.3 Representation as capability

A measurement model is a representation of Reality.

Changing the representation can remove uncertainty sources.

Example:

```text
angle measurement × lever-radius model
→ inferred tip displacement
```

versus:

```text
direct visual tracking of actual tip/contact point
→ displacement
```

If displacement is the target, the second representation may delete:

- shaft-center uncertainty;
- lever-radius uncertainty;
- angle-to-linear propagation;
- some backlash interpretation.

Thus:

```text
better measurement representation
→ shorter causal/model chain
→ potentially lower uncertainty and lower maintenance burden
```

### 2.4 CCE / environment construction

Calibration burden can be reduced by changing apparatus geometry.

This is important enough to alter F09/F10.

If the E1 force axis is arranged so the mounted load-cell chain can be loaded vertically by known masses along its intended sensing axis, we avoid:

```text
hanging mass
→ pulley
→ string
→ friction
→ off-axis transfer
→ load cell
```

and instead obtain:

```text
known mass
→ gravity
→ intended load-cell contact axis
```

This is a concrete case of:

```text
Environment / fixture construction
→ metrological capability change
```

### 2.5 Chapter 4 currentness/history/recovery

Calibration standing has a currentness problem:

```text
historical calibration
!= current valid relation
```

because the current relation can be changed by:

- overload;
- remounting;
- readout replacement;
- wiring/excitation changes;
- camera focus/resolution/mount changes;
- reference damage;
- temperature/environment drift;
- software scaling/filter changes.

F12 makes this physical.

## 3. Measurement authority ladder — audit notation only

This is not a new ontology.

### M0 — discriminative indication

Purpose:

```text
Does state A differ from state B strongly enough to choose the next action?
```

Requirements:

- measurand relation plausible;
- monotonicity/zero/repeatability checked;
- obvious gross errors challenged independently;
- no strong SI-traceability claim.

Example:

```text
load-cell counts distinguish free vs blocked
```

### M1 — target-qualified measurement

Purpose:

Quantitative result is adequate for one declared target/decision.

Requirements:

- measurand explicitly defined;
- calibration/check relation;
- bounded uncertainty or evidence of adequacy;
- relevant influence quantities controlled/observed;
- current chain identity;
- uncertainty small enough for the decision.

### M2 — metrologically traceable result

Purpose:

Result is related to an external reference/SI through documented chain and uncertainty.

Use when:

- publication/inter-lab comparison;
- externally defensible quantitative claim;
- calibration of other references;
- downstream decision needs it.

### M3 — reference/standards-level capability

National/primary/high-order standard role.

Current Ordivon does not need this locally. NMC/external metrology institutions are stronger carriers.

## 4. Decision-relative adequacy, not precision prestige

The correct relation is:

```text
measurement uncertainty
< enough of the decision margin
that classification/conclusion is robust
```

There is no universal magic ratio for every experiment.

ILAC G8 provides mature guidance on decision rules/guard bands for conformity decisions; the decision rule should reflect uncertainty and the risk of false acceptance/rejection rather than assuming exact values are perfectly known.

Source:
https://ilac.org/publications-and-resources/ilac-guidance-series/

### F12 planning heuristic

For exploratory E1, use this sequence:

1. define the states/hypotheses to discriminate;
2. run repeated observations;
3. estimate within-state spread + calibration/model uncertainty;
4. estimate the smallest decision-relevant separation;
5. if uncertainty bands overlap enough to change the conclusion, improve the measurement geometry/reference;
6. if they do not, **stop buying precision**.

A 4:1 or similar uncertainty-to-tolerance ratio can be used as a conservative engineering heuristic in some contexts, but F12 does **not** promote it as a universal metrological law.

## 5. E1 target decisions before numeric precision

E1-v0 wants to discriminate at least:

```text
free motion
contact onset
compliant loading
blocked/missed-step
slip/coupling loss
loading/unloading hysteresis
post-reset/current-state recovery
```

The first measurement need is therefore not:

```text
force known to ±0.001 N
```

It is:

```text
force / displacement evidence sufficiently stable
that these state transitions cannot be confused by measurement error
```

Only after real response distributions exist should the final target uncertainty be locked.

## 6. F09 mechanical scale constrains metrology

The current reference NEMA-8 + lever geometry estimated nominal tangential interaction around:

```text
20 mm lever → ~0.88 N
30 mm lever → ~0.59 N
40 mm lever → ~0.44 N
```

before intentional current reduction and real dynamic effects.

Therefore the main E1 region is sub-newton class, even though the 500 g-force load-cell full scale is about 4.9 N.

Critical consequence:

```text
sensor full-scale range
!= required calibration range
```

F12 should initially calibrate/check the region E1 actually uses, roughly the lower ~0–1 N class, rather than spending effort characterizing all the way to 4.9 N merely because the load cell can survive it.

## 7. Force chain — first concrete measurement model

Current chain:

```text
physical contact force
→ load-cell elastic deformation
→ strain bridge differential signal
→ NAU7802-class PGA/ADC
→ Pico reading
→ calibration relation
→ force result
```

Potential uncertainty/influence sources:

```text
reference load
local gravity model
air buoyancy (small here)
load alignment / off-axis loading
contact point / fixture compliance
mounting torque / support geometry
bridge excitation/readout behavior
ADC noise/resolution/filtering
zero drift
creep
hysteresis
repeatability
temperature
calibration-model fit
```

F12 should not assume the ADC's 24-bit word length yields 24-bit force accuracy.

## 8. NIST force-calibration baseline strongly supports chain identity

NIST currently calibrates force transducers by applying known forces and recording deformation. It explicitly notes that when a customer's readout is supplied, the **transducer and readout are calibrated as a system**, and that calibration is valid only when they are used together.

Source:
https://www.nist.gov/programs-projects/calibration-force-transducers

NIST deadweight force uncertainty includes:

- mass determination;
- local acceleration due to gravity;
- air density.

This validates two F12 principles:

```text
load cell serial alone != calibrated force chain
```

and:

```text
known mass != exact force without a gravity/model statement
```

## 9. First force reference — small documented masses are enough

OIML R 111 remains the mature standard for weights; the current OIML publication is R 111:2004 including Amendment 2025.

Source:
https://www.oiml.org/en/publications/recommendations/en/files/pdf_r/r111-e04_update25.pdf

For the 2004 R111 table, class M1 maximum permissible errors are already tiny relative to E1 force effects, e.g. approximately:

```text
5 g    ±1.6 mg
10 g   ±2 mg
20 g   ±2.5 mg
50 g   ±3 mg
100 g  ±5 mg
200 g  ±10 mg
500 g  ±25 mg
```

Source:
https://www.oiml.org/en/files/pdf_r/r111-1-e04.pdf

A current commercial 500 g OIML M1 weight, for example, publicly lists 25 mg OIML tolerance, consistent with the standard.

Source:
https://igel.kern-sohn.com/en/showproduct?productid=370169

### Consequence

For a 100 g M1 mass, a ±5 mg mass tolerance corresponds to only roughly tens of micronewtons of force uncertainty under Earth's gravity — far below likely first E1 fixture/repeatability uncertainty.

Therefore:

```text
premium E1 force uncertainty
will not be bought by purchasing E1/E2-class weights
```

The dominant problems are likely fixture/load alignment, hysteresis, repeatability, zero and mechanical state.

### Current recommendation

A small durable reference set in the rough range:

```text
5 g
10 g
20 g
50 g
100 g
(optional 200 g)
```

of documented OIML M1-class or equivalent known masses is a strong first reference-capital candidate.

Exact vendor is procurement-level.

## 10. Local gravity — do not silently use standard gravity as site truth

A hanging/calibration mass creates force:

```text
F = m g
```

The conventional standard acceleration `g_n = 9.80665 m/s²` is not Singapore's actual local gravitational acceleration.

A normal-gravity calculation at Singapore's latitude gives roughly **9.780 m/s² near sea level**; exact site gravity also depends on elevation and local geology.

Therefore using 9.80665 as though it were local measured `g` introduces about a **0.27% scale difference** in force.

For 100 g, that is only about 2.6 mN — probably negligible for first E1 state classification, but not conceptually zero.

### F12 rule

For E1-v0:

```text
state the gravity model used
```

and either:

- report equivalent applied mass / gram-force for exploratory calibration; or
- convert to newtons using an explicit approximate local-g model.

For stronger traceability/precision:

- obtain a stronger local gravity/reference route through metrology/geodetic data or external calibration;
- include uncertainty accordingly.

Do not pretend a nominal mass alone creates exact SI force.

## 11. Apparatus redesign: make gravity calibration direct

This is a high-value F12 → F09/F10 feedback.

### Poor geometry

```text
horizontal force axis
known hanging mass
→ string
→ pulley
→ friction / angle
→ load cell
```

This adds uncertain transfer elements.

### Stronger geometry

Configure E1 so:

- NEMA-8 shaft is horizontal;
- lever moves in a vertical plane;
- contact/reaction force on the load-cell chain is substantially vertical;
- calibration masses can be applied to the same intended contact/load axis with the load-cell mount left intact.

Then:

```text
known mass
→ gravity
→ same load path / same mounted load cell
```

This can materially shorten the calibration chain.

### Current recommendation

F10 should favor a force-sensing module whose **measurement-critical mount remains unchanged during calibration and E1 use**.

If the entire module must be removed/remounted to calibrate, remount repeatability itself enters uncertainty/currentness.

## 12. Force calibration procedure — E1-v0

### Step F0 — define the measurand

Do not merely say `force`.

First target:

> quasi-static contact force transmitted through the defined E1 specimen/load-cell contact axis after each step-settle state.

This deliberately excludes high-frequency impact/transient force.

### Step F1 — warm/current-state preparation

- fixed load-cell/readout/fixture generation;
- stable power/excitation;
- allow short settling where observed necessary;
- record ambient T/RH as context;
- inspect no overload/damage/currentness conflicts.

### Step F2 — zero sequence

Record repeated unloaded indications rather than one zero sample.

Capture:

- mean/median zero;
- noise/spread;
- short-term drift.

### Step F3 — ascending known-load points

Apply several points across the target region, e.g. nominal:

```text
0
~0.05 N
~0.10 N
~0.20 N
~0.49 N
~0.98 N
```

from the 5/10/20/50/100 g reference-mass class under explicit local-g model.

### Step F4 — descending points

Remove loads in reverse order.

This exposes:

- hysteresis;
- zero return;
- creep/path dependence.

### Step F5 — repeats

Repeat selected points enough to estimate repeatability and placement sensitivity.

### Step F6 — fit only the necessary calibration model

Begin with a linear relation if residuals support it.

Do not fit high-order polynomial merely because software can.

### Step F7 — hold-out check

Use at least one mass/combination not used to fit the relation as an independent check.

### Step F8 — post-zero

Return to zero and observe whether the chain recovered.

### Step F9 — preserve raw readings + relation

Keep raw calibration indications, reference identities and fit residuals, not only gain/offset coefficients.

## 13. First force uncertainty budget should be empirical, not datasheet theatrical

Potential components can be grouped:

### Reference contribution

- mass value/tolerance;
- local-g model;
- buoyancy if later material.

### Apparatus contribution

- load alignment;
- contact geometry;
- mount compliance;
- off-axis sensitivity;
- fixture remounting.

### Sensor/readout contribution

- repeatability;
- zero drift;
- creep;
- hysteresis;
- ADC noise;
- excitation/readout scaling;
- temperature dependence.

### Model contribution

- calibration residual;
- nonlinearity in target range;
- interpolation.

For first E1, measure actual repeatability/hysteresis/zero and compare their scale with reference uncertainty before buying better standards.

## 14. Force adequacy criterion

Do not set an arbitrary universal `±0.01 N` requirement now.

After the first rig exists:

1. collect repeated free/contact/compliant/blocked trajectories;
2. determine the smallest state separation that changes diagnosis;
3. estimate force result uncertainty in that region;
4. if uncertainty makes two states practically indistinguishable, improve the chain;
5. otherwise preserve the current chain.

Expected likely result:

```text
M1-class reference mass uncertainty << fixture/sensor uncertainty
```

so improvements should first target geometry, mounting and repeatability rather than reference class.

## 15. Displacement/geometry measurement — simplify the measurand

F08 originally allowed:

```text
camera → angle
angle × lever radius → tip displacement
```

F12 recommends a simpler first path if physical displacement is the target:

```text
camera
→ directly track actual lever tip/contact fiducial in the motion plane
→ planar displacement
```

This can delete lever-radius uncertainty from displacement.

### If angle is the actual target

Use marker/shaft/lever pose and calibrated camera geometry.

### If torque is later needed

Then lever radius becomes a measurement input and must carry its own uncertainty/currentness.

Do not calculate torque before a consumer asks for it.

## 16. Camera metrology — calibration is configuration-relative

Current OpenCV already provides camera calibration and ChArUco/pose methods.

Sources:
- https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html
- https://docs.opencv.org/4.13.0/df/d4a/tutorial_charuco_detection.html

The quantitative visual chain includes:

```text
camera identity
resolution/crop mode
lens/focus state
mount pose
intrinsic calibration
lens-distortion residual
fiducial/scale dimensions
target-plane relation
pixel localization
lighting/exposure state when material
```

### First E1 visual adequacy test

Instead of assuming a pixel-to-mm number:

1. fix the camera as best possible;
2. place a printed/physical scale in the E1 motion plane;
3. move a marker through known coarse positions or compare to ruler/caliper-separated positions;
4. measure repeatability and residual error;
5. test after camera/lid/mount perturbation;
6. decide whether visual displacement is adequate.

If not, promote external UVC / ToF / AS5600 according to the failure mode.

## 17. Printed fiducial geometry is not an exact length standard

A home/office printer can introduce:

- scale error;
- nonuniform scaling;
- paper distortion;
- print-driver scaling;
- humidity effects.

Therefore:

```text
PDF says 20 mm
!= printed marker is exactly 20 mm
```

For quantitative use:

- measure the actual printed scale/board with a suitable ruler/caliper or better reference;
- or use a dimensionally stable manufactured target if accuracy pressure earns it.

For E1 coarse visual displacement, direct calibration against a known physical scale in the same plane may be stronger than trusting nominal print geometry.

## 18. Caliper/ruler role

A 150 mm digital caliper and steel rule are first fixture-measurement tools, not automatically reference standards.

Use them for:

- lever/contact dimensions;
- fiducial/scale checks;
- specimen thickness/length;
- fixture positions.

If their uncertainty is small relative to the target, no external calibration is required.

If a later conclusion depends on sub-0.1 mm geometry, promote dimensional reference/calibration through stronger standards/NMC.

NMC currently provides calibration for digital calipers, steel rules, gauge blocks, dimensional scales and non-contact coordinate measurement.

Source:
https://www.a-star.edu.sg/docs/librariesprovider20/calibration-and-measurement/website_list-of-services.pdf

## 19. Electrical reference path

F06 intentionally retained an independent DMM/reference path.

F12 now clarifies its authority.

### E0/E1 exploratory use

A decent standalone DMM can provide independent checks of:

- supply voltage;
- resistor value;
- static GPIO state;
- continuity;
- load-cell/bridge sanity where appropriate.

It does not need SI-traceable annual calibration merely to falsify an AD3 self-report.

### Target-qualified use

If absolute electrical quantity enters a scientific conclusion:

- use instrument specification/current calibration;
- verify with reference resistor/source where appropriate;
- include lead/contact/source uncertainty;
- upgrade to SDM3045X-class automated meter if repeated logging/uncertainty demands it.

### Traceable use

Singapore NMC provides electrical calibration routes. Use external calibration rather than constructing primary electrical standards locally.

## 20. Reference resistor — cheap but useful local check

A stable metal-film resistor with documented tolerance/temperature coefficient can be a durable local **check artifact**.

But:

```text
0.1% resistor datasheet
!= calibrated resistance standard
```

Its first role is:

- detect gross DMM/ADC/drift errors;
- compare channels;
- monitor change over time.

Promote to calibrated/reference resistor only when resistance accuracy itself becomes decision-critical.

## 21. Ambient T/RH measurement remains context-first

SHT4x-class factory-calibrated T/RH is currently an influence/context observer.

F12 does not require external humidity calibration until:

```text
variation in T/RH changes the target result enough to matter
```

Then options include:

- second independent sensor;
- local comparison chamber/reference;
- external NMC temperature/humidity calibration.

NMC currently maintains national T/RH standards and provides hygrometer/thermometer calibration services.

Source:
https://www.a-star.edu.sg/nmc/Research-and-Development/Labs/TL

## 22. Calibration should follow the realized system, not precede it abstractly

Do not calibrate a bare load cell and later assume the same relation after:

```text
new mount
new contact button
new ADC
new excitation
new filter
new wiring
```

The most valuable first calibration occurs after the E1 force module reaches a stable enough **measurement-critical physical realization**.

This is why F10 and F12 are coupled.

## 23. Recalibration/requalification triggers — event-driven first

### Force chain strong triggers

- overload / unexpected impact;
- load-cell replacement;
- readout/ADC replacement;
- excitation/reference change;
- load-cell remounting or support/contact geometry change;
- wiring repair that changes bridge/readout relation;
- visible damage;
- zero/span control check fails;
- abnormal hysteresis/creep/drift;
- large temperature excursion if sensitivity is material.

### Vision chain strong triggers

- camera replacement;
- resolution/crop mode change;
- focus/zoom/lens change;
- camera mount/laptop-lid pose change for quantitative geometry;
- fiducial/scale replacement or deformation;
- calibration check residual increases.

### Dimensional/reference object triggers

- drop/damage;
- wear;
- modification;
- reference-object history becomes UNKNOWN;
- control comparison fails.

### Weak trigger by itself

```text
one year elapsed
```

Time may matter, but it is not a universal sufficient reason.

This follows NIST's current interval guidance.

## 24. Measurement assurance is more useful than ritual recalibration

For an E1 campaign, a tiny internal measurement-assurance routine can be stronger than an arbitrary annual certificate.

### Force campaign check

Before/after campaign:

```text
zero
+ one low known mass
+ one mid/high known mass
```

Compare residuals to the accepted historical envelope.

### Vision campaign check

Observe the same physical scale/fiducial and one known displacement/reference geometry.

### Electrical campaign check

Reference resistor/source sanity check if electrical accuracy matters.

### Ambient

Cross-sensor or known-environment check only when ambient accuracy is material.

If repeated data accumulate, simple control charts can reveal drift and eventually determine evidence-based recalibration intervals, consistent with NIST guidance.

## 25. Reference hierarchy should be intentionally shallow

For first E1:

```text
external national/SI layer (available, not locally reproduced)
        ↑
optional purchased documented mass/reference
        ↑
local working reference/check artifact
        ↑
experiment measurement chain
```

Do not add intermediate calibration tiers without uncertainty/reuse pressure.

### Example force chain

```text
OIML-documented mass set
+ explicit gravity model
→ local force calibration/check
→ load cell + NAU7802 + fixture
→ E1 force results
```

If later external traceability is required:

```text
NMC / accredited calibration
→ calibrated mass / force transducer/reference
→ local chain
```

## 26. Reference independence matters

A reference path should not simply repeat the same failure mode.

Examples:

### Weak

```text
AD3 output
→ AD3 internal readback
```

### Stronger

```text
AD3 output
→ independent DMM
```

### Force

```text
load-cell gain
checked only against previous load-cell reading
```

is weak.

Known masses create an independent physical reference mechanism.

### Vision

```text
camera pose inferred only from the same image algorithm
```

can be challenged by:

- physical ruler/scale;
- fixture geometry;
- alternate marker;
- later ToF/encoder.

This directly consumes PPD's preference for independent Reality pressure.

## 27. Model complexity is an uncertainty source

If a target can be measured directly, avoid unnecessary inference.

Examples:

### Prefer

```text
direct contact-point displacement
```

before:

```text
angle × uncertain lever radius
```

when displacement is the target.

### Prefer

```text
load-cell force
```

before:

```text
motor current × torque constant × microstep model × lever geometry
```

when contact force is the target.

### Prefer

```text
known static mass calibration
```

before constructing a motor-based force reference.

This is a metrological form of Ordivon's anti-overrepresentation principle:

```text
Do not introduce latent variables that the decision does not consume.
```

## 28. Repeatability can matter more than absolute accuracy

E1 first asks comparative questions:

```text
same specimen before/after cycles
soft vs stiff specimen
free vs blocked
current-limit A vs B
loading vs unloading
```

For these, a stable biased measurement may be more useful than a nominally more accurate but unstable chain.

However:

```text
repeatability != accuracy
```

The role must be explicit.

M0/M1 comparative standing can be strong without overclaiming absolute SI accuracy.

## 29. Hysteresis/creep are not always “sensor errors” to subtract blindly

The measured force path can contain hysteresis from:

- specimen;
- load cell;
- fixture friction;
- contact geometry;

If E1's target is specimen hysteresis, apparatus hysteresis must be bounded independently.

If target is only state discrimination, total system hysteresis may be acceptable if repeatable and small relative to state separation.

This is another target-relative decision.

## 30. Measurement-system currentness is composite

A strong current force result may depend on:

```text
load cell physical identity/current state
+ ADC/readout realization
+ excitation/config
+ fixture/load geometry
+ calibration relation
+ reference currentness
+ ambient/influence conditions
+ measurement procedure
```

No one owner should collapse this into `calibrated=true`.

F12 instead provides the qualification relation consumed by F04/domain decisions.

## 31. Measurement result provenance

For target-relevant E1 measurements preserve enough to reconstruct the result.

### Force result

- raw bridge/ADC readings;
- zero handling;
- calibration data/relation;
- reference mass IDs/values;
- gravity model/value used;
- fixture generation;
- load-cell/readout identities;
- ambient context where relevant;
- result + uncertainty/adequacy statement.

### Vision result

- raw frames;
- calibration/fiducial source;
- camera/config/mount identity;
- raw detected points/pose if useful;
- derived displacement;
- residual/uncertainty evidence.

### Do not preserve only

```text
force = 0.423
x = 4.2
```

without the chain that created them if those quantities drive conclusions.

F14 will generalize evidence/provenance storage; F12 defines what a measurement needs semantically.

## 32. Calibration relation itself has generation/currentness

Suppose:

```text
CAL-FORCE-01
```

was established for:

```text
L1 load cell
+ ADC A1
+ fixture G3
```

Then fixture becomes G4.

The calibration artifact can remain historical, but:

```text
CAL-FORCE-01 currentFor(G4)
```

is not automatically true.

This is exactly Chapter-4 currentness applied to calibration.

## 33. Software transformations can invalidate measurement standing

Examples:

- firmware changes ADC gain/filter rate;
- sign/scaling constant changes;
- camera pipeline changes undistortion/resolution;
- averaging window changes dynamic measurand;
- timestamp alignment changes synchronized trajectory interpretation.

Physical serials may all be unchanged.

Therefore F05 provider/firmware realization is part of F12 current qualification when it changes the measurement relation.

## 34. First E1 force target does not justify external load-cell calibration

NIST force-transducer services begin at forces far above our sub-newton E1 reference region in the published current overview, and high-order force calibration would vastly exceed the information need.

Singapore NMC does provide force/load-cell calibration routes, but external force calibration should be consumed when:

- Ordivon starts making externally comparable quantitative force claims;
- local deadweight/reference calibration cannot bound uncertainty sufficiently;
- a reference force transducer is used to calibrate others;
- publication/regulatory/contractual pressure demands traceability.

For E1-v0:

```text
known masses + explicit gravity model + empirical repeatability/hysteresis
```

is the stronger first carrier.

## 35. First E1 measurement programme

### Phase P0 — M0 discriminability

Before formal calibration ambition:

- verify load-cell sign/monotonicity;
- establish zero/noise;
- apply several known masses;
- verify camera sees repeatable motion;
- run free/contact/blocked states slowly;
- retain raw evidence.

Question:

```text
Can the current measurement geometry already separate the physical states?
```

### Phase P1 — M1 target qualification

After the rig is stable:

- force ascending/descending/repeat calibration;
- direct visual displacement calibration/check;
- quantify within-state repeatability;
- estimate target-relevant uncertainty;
- define event-driven requalification triggers;
- freeze the first current chain generation.

### Phase P2 — cross-modal falsification

Compare:

```text
command
vs visual position
vs force
vs optional electrical observation
```

under block/slip/restart/response-loss.

### Phase P3 — only if needed, stronger traceability

Escalate specific chains to purchased calibrated standards / NMC / accredited calibration.

Do not promote all modalities together.

## 36. Force reference-object ownership

F11 established that references deserve durable local identity earlier than disposable specimens.

F12 now identifies a first strong set:

```text
small documented mass/weight set
= OWN-EARLY / durable reference capital
```

Why:

- low cost/carrying burden;
- passive, durable;
- no software/provider dependency;
- useful for load-cell checks;
- useful for balance/scale work later;
- independent Reality pressure;
- easily stored and visually identified.

This is an unusually strong early physical reference asset.

## 37. Exact DMM decision remains conditional

F12 does not overturn F06.

Independent electrical reference capability is earned.

But exact choice remains:

```text
credible handheld DMM
vs
SDM3045X-class automated bench DMM
```

Promote SDM3045X when repeated automated/quantitative electrical measurement has a target uncertainty that the handheld/manual path cannot meet efficiently.

## 38. Exact camera upgrade remains empirical

F12 also does not force a new camera.

Use integrated camera first.

Only promote external UVC/machine vision/ToF/encoder when direct calibration tests show the actual uncertainty/stability failure.

Thus F12 supports the F08 deletion test rather than assuming better optics are needed.

## 39. F12 falsifiers

### F12-F1 — traceability deletion

Run E1 M0/M1 with documented local mass references but without external calibration.

If state decisions remain robust and no external quantitative claim is needed:

```text
external traceability remains deferred
```

### F12-F2 — precision-instrument deletion

Use compact sensor/readout + simple references.

If uncertainty is already small relative to E1 decision separation:

```text
higher-end DMM/DAQ/force gauge remains unearned
```

### F12-F3 — reference-class deletion

Compare the estimated uncertainty contribution from M1-class mass tolerance with actual repeatability/fixture hysteresis.

If reference contribution is negligible:

```text
E1/E2/F1 higher-class weights add no current decision value
```

### F12-F4 — calibration-geometry falsifier

Calibrate load cell in a different mount/orientation than E1, then compare with same-load checks in the actual E1 mount.

If relation changes materially, preserve system/fixture-relative calibration standing.

Prefer safe non-destructive perturbations.

### F12-F5 — remount currentness

Remove and remount the load-cell module.

Run control masses.

If calibration residual shifts beyond accepted envelope:

```text
remount event invalidates prior current qualification
```

### F12-F6 — overload/suspicious-event trigger

After any real or safely simulated event known to threaten the chain, perform control checks before allowing old calibration standing to continue.

Do not deliberately damage hardware solely for this falsifier.

### F12-F7 — camera configuration currentness

Change lid angle/mount/resolution/focus where available.

Repeat known visual scale/displacement.

Old calibration should fail closed if residual exceeds target.

### F12-F8 — direct versus inferred displacement

Compare:

A. camera angle × measured lever radius;
B. direct camera tracking of actual contact point.

If B yields equal/better target discrimination with fewer uncertainty contributors, use B and delete unnecessary model complexity.

### F12-F9 — local-g relevance

Compute force with standard gravity and approximate Singapore local gravity.

If the difference is negligible relative to E1 uncertainty/decision margin, retain simple stated local-g model.

If later target uncertainty approaches that scale, promote stronger gravity/reference treatment.

### F12-F10 — measurement-assurance interval

Perform repeated control-mass checks across campaigns.

If drift is stable, extend check/recalibration interval; if drift/event sensitivity appears, shorten or use event-triggered checks.

### F12-F11 — ambient deletion

Correlate force/vision residuals with T/RH across natural variation.

If no target-relevant effect is detected, ambient remains context and does not enter every uncertainty budget materially.

### F12-F12 — reference damage/currentness

Use a harmless surrogate or naturally damaged reference object to test that a known reference's history state can invalidate its use without deleting its identity.

## 40. OWN / CHECK / EXTERNAL / DEFER disposition

| Capability / reference | Current disposition | Reason |
|---|---|---|
| target uncertainty definition | **CORE / FIRST** | precedes instrument choice |
| load-cell local calibration with known masses | **CORE / FIRST** | E1 force authority |
| ascending/descending/repeatability checks | **CORE / FIRST** | exposes hysteresis/zero/drift |
| small OIML-M1-class mass set | **OWN-EARLY / STRONG** | durable independent passive reference |
| explicit local-gravity model | **CORE when converting mass→N** | avoids silent standard-g assumption |
| same-mount gravity-friendly force geometry | **STRONG F09/F10 REVISION** | shortens uncertainty chain |
| camera calibration + physical-scale check | **CORE if vision is quantitative** | E1 displacement authority |
| direct tip/contact visual tracking | **PREFER where displacement is target** | deletes lever-model terms |
| steel rule / caliper working geometry | **OWN-EARLY** | adequate until target says otherwise |
| independent handheld DMM | **OWN / FIRST capability** | electrical adjudication |
| SDM3045X-class bench DMM | **CONDITIONAL / OWN-EARLY later** | automation/precision consumer needed |
| reference resistor/check artifact | **OWN-EARLY** | low-cost electrical measurement assurance |
| external NMC mass/force/electrical/dimensional calibration | **AVAILABLE / ESCALATION PATH** | stronger traceability when needed |
| fixed annual recalibration | **REJECT UNIVERSAL RULE** | event/stability/need relative |
| force calibration service for E1-v0 | **DEFER** | local mass path enough unless falsified |
| high-class E1/E2 weights | **DEFER** | reference uncertainty already negligible |
| local primary standards lab | **REJECT** | mature NMC/external owner exists |

## 41. Positive capability language

### Target-Relative Measurement Authority

Ordivon can decide how accurate a measurement must be from the physical distinction and consequence it must support, rather than allowing owned instrument specifications to define the science.

### Calibration-Geometry Construction Capability

Ordivon can redesign apparatus geometry so a stronger, shorter and more independent reference chain becomes possible, reducing uncertainty before purchasing precision.

### Measurement-Model Contraction Capability

Ordivon can replace unnecessarily indirect derived quantities with more direct observables when this removes latent variables and lowers uncertainty/maintenance burden.

### Event-Driven Calibration Currentness Capability

Overload, remounting, replacement, software/configuration change and failed control checks can invalidate calibration standing immediately, while stable repeated control evidence can justify longer intervals.

### Independent Reference Adjudication Capability

Known masses, physical scales and independent electrical references can challenge sensor/instrument indications through different failure mechanisms rather than relying on self-report.

### External Metrology Assimilation Capability

When stronger traceability or uncertainty is required, Ordivon can consume Singapore NMC/accredited external metrology as a first-class capability without reproducing the national-standard layer locally.

## 42. F12 standing

The first E1 metrology programme does **not** require high-end calibration infrastructure.

It requires:

```text
explicit measurand
+ target-relative decision need
+ gravity-friendly force geometry
+ documented small mass references
+ load-cell/readout/fixture calibration together
+ repeatability / hysteresis / zero checks
+ direct visual geometry calibration
+ independent electrical check
+ event-driven qualification currentness
+ raw calibration evidence
```

### Strongest revised E1 geometry

Prefer:

```text
horizontal stepper shaft
→ lever moves in visible vertical plane
→ force reaction aligned so known masses can load the same measurement-critical axis
```

where practical.

This should be tested against F10 fixture simplicity before freezing.

### Strongest retained distinctions

```text
Calibration != Adjustment
Calibration != Verification
Traceability != FitnessForPurpose
CalibratedInstrument != TraceableMeasurementResult
ReferenceValue != MeasurementResult
DatasheetAccuracy != MeasurementUncertainty
Repeatability != Accuracy
SensorResolution != MeasurementResolution
HistoricalCalibration != CurrentQualification
SameDevice != SameMeasurementChain
FullScale != RequiredCalibrationRange
TimeElapsed != RecalibrationNecessity
```

### Strongest anti-overbuild result

```text
E1 measurement authority
!=
external calibration certificate
!=
precision bench ownership
```

A small mass-reference set plus a deliberately calibration-friendly apparatus may create more useful first metrology capability than buying a much more precise instrument into a poorly defined geometry.

## 43. Next family boundary

F13 — Environmental Observation and Control can now be audited from real metrology pressure rather than generic climate control.

It should answer:

```text
Which environmental quantities are merely context and which are causal influence quantities?
When does ordinary Singapore indoor T/RH variation actually change E1/F12 conclusions?
Is observation enough, or must temperature/humidity/light/vibration be controlled?
When do enclosure, fan, heater, desiccant, thermal chamber or vibration isolation become earned?
Can environmental variation itself be used as a free falsifier before being suppressed?
```

F13 should begin with the existing SHT4x ambient observation seam and natural environmental variation, then let F12 uncertainty/decision data determine whether active control is needed.
