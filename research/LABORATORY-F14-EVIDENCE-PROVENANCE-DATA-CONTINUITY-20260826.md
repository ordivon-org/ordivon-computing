# Ordivon Laboratory F14 — Evidence, Provenance, Data and Experimental Continuity v0.1

Status: **CURRENT FAMILY AUDIT / ATTEMPT JOIN, NOT NEW EVIDENCE AUTHORITY**  
Date: 2026-08-26  
Parent: `research/LABORATORY-PHYSICAL-FALSIFIER-MAP-20260826.md`  
Previous: `research/LABORATORY-F13-ENVIRONMENTAL-OBSERVATION-CONTROL-20260826.md`  
Host continuity: `task:ordivon-laboratory-capability-atlas-20260826@24`

## 0. Referent

F14 asks:

> What evidence from one physical experiment must survive process loss, response loss, code change and Agent replacement so that a future Agent can reconstruct what was attempted, what physically happened, what remains UNKNOWN, which results can be recomputed, which standing has been superseded, and which owners must be re-read — without creating a new universal Laboratory evidence database?

F14 is **not**:

- a new Runtime above Runtime;
- a Laboratory-wide event store;
- a replacement for Host continuity;
- a replacement for Harness Journal/CAS;
- a second device/sample/calibration owner;
- a universal provenance ontology;
- an assumption that every byte belongs in Git;
- a requirement to retain all video forever;
- an assumption that a checksum is entity identity;
- a claim that raw data equals Reality;
- a reason to copy owner-native state into one mega-schema.

The target is a **bounded experiment evidence join**.

## 1. Aggressive internal subtraction

### 1.1 Runtime already owns physical execution evidence

F04 established that Runtime already owns:

- Job / Attempt identity;
- exact admitted execution;
- durable execution receipts;
- retained Artifacts;
- cancellation;
- explicit UNKNOWN / reconciliation-required state;
- response-loss recovery mechanics.

Therefore F14 must reference Runtime evidence rather than create a second physical-execution ledger.

### 1.2 Host already owns open-work semantic continuity

Host Task continuity already preserves:

- long-lived work identity;
- semantic checkpoint;
- revision fencing;
- recovery/handoff across context/process replacement.

Host is not raw experiment-data storage and does not mint physical truth.

### 1.3 Harness already has Journal/CAS

Current Ordivon research already proved a Harness pattern with:

```text
append-only Journal
+ content-addressed immutable objects
+ selected re-entry into cognition
```

and specifically rejected building a new generic Memory/Promotion system merely because bytes should survive future model processes.

Thus F14 should not build `LabMemory`.

### 1.4 Computing already has immutable digest-bound System Snapshots

`research/evidence/README.md` currently defines:

- immutable committed evidence manifests;
- exact repository revisions;
- service/tool-contract digests;
- Artifact digests;
- canonical payload SHA-256;
- append-only correction via `supersedes`;
- historical Artifact verification from exact Git commits.

This is a direct existing carrier for bounded cross-owner experiment snapshots.

F14 should reuse/adapt this pattern rather than create a parallel evidence format by default.

### 1.5 Atlas/Book already solve anti-rediscovery and standing/currentness conceptually

Historical evidence can survive while current standing changes.

F14 therefore does not need a new “scientific memory theory”.

The residual is concrete:

```text
How is one physical attempt joined to its exact evidence so future consumers can re-enter it correctly?
```

## 2. External mature baseline

### 2.1 W3C PROV — provenance interchange is already mature

W3C PROV-O is a Recommendation for representing provenance across heterogeneous systems. Its core concepts cover entities, activities, agents, derivation and attribution and can be specialized for domain use.

Source:
https://www.w3.org/TR/prov-o/

Transfer:

```text
cross-system provenance vocabulary
= mature external baseline
```

Ordivon does not need to invent a universal provenance ontology.

### 2.2 BagIt — opaque payload + integrity packaging is mature

RFC 8493 BagIt defines a simple package:

```text
bag metadata/tags
+ data/ payload
+ cryptographic manifests
```

for reliable storage/transfer of arbitrary files without requiring the packaging layer to understand payload semantics.

Source:
https://www.rfc-editor.org/info/rfc8493

Transfer:

```text
portable integrity package
= mature carrier
```

not an internal live authority model.

### 2.3 RO-Crate — research-object packaging is mature and current

RO-Crate current specification page lists **1.3 as the current long-term release**. RO-Crate packages research data with machine/human-readable JSON-LD metadata and can describe files, equipment, software, people, workflows and provenance.

Source:
https://www.researchobject.org/ro-crate/specification.html

Transfer:

```text
publish/share/archive research bundle
→ RO-Crate is a strong export/interchange candidate
```

but:

```text
RO-Crate != Ordivon live owner authority
```

### 2.4 FAIR is a publication/reuse target, not a reason to over-model E1

FAIR emphasizes Findable, Accessible, Interoperable and Reusable digital assets, with machine-actionable metadata and persistent identifiers where appropriate.

Source:
https://www.go-fair.org/fair-principles/

For E1-v0, FAIR should be treated as a future reuse/export pressure, not as a requirement to globally identify every local object or publish every attempt.

## 3. F14's strongest architecture result

The physical experiment does **not** need one canonical mega-record containing all owner truth.

The strongest pattern is:

```text
Owner-native evidence
    F04 experiment semantics
    F05 device binding
    F10 fixture geometry/generation
    F11 specimen state/lineage
    F12 calibration/measurement qualification
    F13 environment context
    Runtime execution/Artifact receipts
        ↓
small immutable Attempt Evidence Capsule
        ↓
raw physical payload references/digests
        ↓
derived analysis products
        ↓
scientific/domain standing
```

The Attempt Evidence Capsule is a **join**.

It does not become the owner of the things it references.

## 4. Strong distinctions

```text
RawEvidence != Reality
```

A camera frame is an optical projection. ADC codes are a measuring-system indication. Neither is Reality itself.

```text
RawEvidence != DerivedResult
```

```text
DerivedResult != AcceptedStanding
```

```text
HistoricalEvidence != CurrentStanding
```

```text
ArtifactDigest != EntityIdentity
```

```text
ContentIdentity != Owner/RoleIdentity
```

```text
ProvenanceCompleteEnoughFor(target A)
!= ProvenanceCompleteEnoughFor(target B)
```

```text
Recomputable != ReproduciblePhysicalWorld
```

```text
ReplayOfAnalysis != ReplayOfPhysicalEffect
```

```text
ImmutableHistory != ImmutableInterpretation
```

```text
EvidenceRetention != EvidencePromotionIntoCognition
```

These distinctions are more important than any storage technology.

## 5. Digest equality is not entity identity

Existing Ordivon WL0 falsification already produced the case:

```text
runtime.state bytes == finance.state bytes
SHA-256 equal
but owner-bound entities remain distinct
```

Therefore SHA-256 is used for:

- integrity;
- content addressing;
- immutable reference;
- deduplication where safe;

but not automatically for:

- physical object identity;
- semantic role;
- owner authority;
- attempt identity;
- currentness.

### F14 rule

A strong reference is often:

```text
owner / role / native identity
+ content digest
```

rather than digest alone.

## 6. Evidence layers — planning notation only

### EVD-0 — owner-native receipt

Examples:

- Runtime Attempt/Artifact receipt;
- F05 current device binding;
- Host Task checkpoint;
- calibration record;
- specimen state record.

Do not copy if a stable owner reference suffices.

### EVD-1 — primary experiment payload

Examples:

- NAU7802 ADC time series;
- camera frame(s)/video segment;
- Pico local event/step log;
- ambient T/RH series;
- instrument waveform.

These are closest retained digital observations to the physical event, while still measurement-system-relative.

### EVD-2 — derived data

Examples:

- calibrated force series;
- detected fiducial coordinates;
- visual displacement;
- aligned force/displacement trajectory;
- fitted calibration curve;
- residual statistics.

### EVD-3 — interpretation / classification

Examples:

```text
free
contact
blocked
slip
hysteresis observed
```

### EVD-4 — standing / consequence

Examples:

- E1 falsifier survived/failed;
- ToF not needed;
- remount invalidates calibration;
- environmental control not earned.

The higher layer should point downward to evidence; lower layers do not automatically inherit higher semantic authority.

## 7. The first Attempt Evidence Capsule

F14 intentionally does **not** freeze a universal JSON schema yet.

Conceptually one E1 attempt should be able to bind:

```text
attempt semantic identity / question reference
start/end/recovery state
source revision / firmware digest
Runtime Job/Attempt/Artifact refs
current F05 device bindings
F10 fixture generation / key geometry
F11 specimen identity + start/end state
F12 calibration relation / qualification refs
F13 environmental context refs
raw payload file refs + digests
analysis code/version refs
produced derived artifact refs
explicit contradictions / UNKNOWN
post-attempt disposition
scientific acceptance/rejection ref
```

This is a join list, not an authorization to duplicate every owner's full record.

## 8. Attempt capsule immutability

Once an attempt capsule is closed and committed/archived:

```text
do not edit historical evidence in place
```

If later information resolves or corrects something:

```text
new capsule / annotation / interpretation
→ supersedes or references prior capsule
```

The earlier record remains evidence of what was known/recorded then.

This directly reuses Computing evidence snapshot practice.

## 9. UNKNOWN must survive archival

A common provenance failure is retrospective cleanup.

Example:

```text
physical command dispatched
host response lost
camera captured ambiguous post-state
```

At close time:

```text
physical outcome = UNKNOWN
```

If a later independent frame/manual observation resolves it:

```text
later observation resolves earlier UNKNOWN
```

but the original evidence must not be rewritten as though certainty always existed.

Thus:

```text
ResolvedLater
!= WasKnownEarlier
```

This is essential for Chapter 4 currentness/history semantics.

## 10. Contradictory evidence is retained, not averaged away

Suppose:

```text
controller step count → +20° expected
camera → +3°
load cell → force rise
```

The evidence capsule should preserve all three sources separately.

Derived diagnosis may say:

```text
likely blocked/missed-step
```

but raw contradiction remains challengeable.

Similarly:

```text
vision +5 mm
ToF +1 mm
```

should not be collapsed into `position=3 mm` merely for convenience.

## 11. Raw retention should follow recomputation option value

Raw evidence is valuable when future analysis can ask new questions.

### High option-value first E1 raw data

- load-cell ADC samples;
- camera frames around each settled state;
- fault/restart/response-loss event frames;
- controller/event log;
- calibration raw points;
- experiment-start/end fixture/specimen photos.

### Lower value to retain at full fidelity

- hours of unchanged camera video;
- very high-rate ambient T/RH;
- redundant duplicate logs with no independent failure mode;
- temporary UI previews.

The rule is:

```text
retain enough raw evidence to recompute plausible future target questions
without retaining arbitrary infinite sensor streams
```

## 12. F09/F13 design helps shrink data volume

Because E1 uses:

```text
step
→ settle
→ observe
```

rather than continuous high-speed motion, vision can initially preserve:

```text
pre-state frame
post-step settled frame(s)
fault-transition short sequence if needed
```

instead of 24/7 video.

This is an important capability interaction:

```text
experiment design
→ smaller evidence burden
```

without losing target information.

## 13. Force-data retention

For quasi-static E1, preserve at least:

- raw ADC codes/time or sample index;
- sample/filter configuration;
- zero procedure;
- calibration relation reference;
- enough samples around each settled state to estimate spread;
- raw calibration runs.

Do not retain only final force numbers if later recalibration/reanalysis could change them.

### Useful future recomputation

If a better calibration relation is established later and historical chain currentness supports it:

```text
raw ADC codes
→ recompute force
```

without rerunning the physical attempt.

## 14. Camera-data retention

F08 already established high recomputation value for raw frames.

For first E1 retain:

- original frame bytes where practical;
- camera/config identity;
- frame relation to attempt step/state;
- calibration/scale relation;
- derived fiducial/point coordinates separately.

Do not retain only an annotated JPEG if annotation overwrote original pixels.

### Derived overlays

Annotated/marked-up images are useful Human/Agent representations but remain derived products.

Preserve source frame reference.

## 15. Calibration raw evidence is first-class

F12 calibration should preserve:

```text
reference mass identity/value
raw indication
ascending/descending order
repeat observations
ambient context if relevant
model fit
residuals
post-zero
```

Do not store only:

```text
gain=...
offset=...
```

because future Agent then cannot challenge model choice, hysteresis or reference usage.

## 16. Fixture evidence should be sparse but sufficient

F10 already defined which geometry matters.

Attempt evidence should bind only target-relevant coordinates such as:

- lever/contact geometry where used;
- load-cell mount generation;
- specimen free length/contact arrangement;
- hard-stop setting where part of falsifier;
- camera/fiducial geometry if quantitative.

A photograph + measured key dimensions + F10 revision may be enough.

No 3D scan of the entire bench is required.

## 17. Specimen lineage remains F11-owned

Attempt capsule can state:

```text
specimen = C07
start state generation = S2
end state = S3 / permanently bent
```

but F14 does not become the canonical specimen database.

If F11 later promotes C07 to durable local identity, the historical attempt remains bound to the same F11 identity.

## 18. Environment evidence remains target-relative

Current first E1 may only need:

```text
T/RH around attempt
lighting condition ref
known draft/vibration exception if any
```

Do not copy the entire environmental time history when F13 has shown it is irrelevant.

If temperature later becomes ENV-1, stronger synchronized environmental evidence can be added prospectively.

## 19. Source/code provenance

Physical results may depend on:

- Pico firmware;
- host analysis code;
- calibration script;
- OpenCV version;
- driver/provider version;
- configuration constants.

Prefer exact Git commit/tree/object or content digest references.

### Important distinction

```text
SourceCommit
!= ExecutedBinary/LoadedFirmware automatically
```

Where consequence depends on exact executed bytes, retain stronger provider/runtime evidence if available.

F14 consumes Runtime/F05 execution binding rather than assuming Git alone proves execution realization.

## 20. Git is excellent for some evidence, poor for some payloads

### Strong Git candidates

- manifests;
- small CSV/JSON calibration data;
- analysis scripts;
- experiment protocol;
- fixture drawings;
- concise photos where size is modest;
- final reports;
- digests/pointers.

### Weak Git candidates at scale

- large raw video;
- high-rate waveforms over long campaigns;
- large image stacks;
- future microscopy/spectral datasets.

Therefore:

```text
GitHistory
!= UniversalRawDataStore
```

## 21. First raw-data storage path

For small E1, the simplest valid carrier can be:

```text
one attempt directory / Runtime Artifact set
+ ordinary files
+ SHA-256 digests
+ immutable manifest after closure
```

If Runtime can durably retain the exact payload files as Artifacts, prefer referencing those owner-native Artifact identities.

If the files are copied into a research archive, bind both source Artifact identity and copied content digest.

No separate object store is currently required.

## 22. CAS promotion gate

A dedicated experiment CAS/object store becomes earned if several pressures appear:

- large binary payloads make Git unsuitable;
- repeated identical/reference payloads create storage duplication;
- multiple experiments need immutable cross-reference to the same content;
- remote/shared agents need stable object retrieval;
- retention exceeds Runtime Artifact lifecycle;
- archival/export pipelines repeatedly need content addressing.

Until then:

```text
existing Runtime/Harness owner CAS + ordinary files/digests
are sufficient carriers
```

Do not create a global CAS merely because hashes are useful.

## 23. Harness CAS should not silently become Laboratory raw-data authority

Harness CAS was built for Harness-owned immutable cognitive/run objects.

Reusing the same implementation may later be sensible, but:

```text
same storage mechanism
!= same owner responsibility
```

Laboratory physical payloads should not be stuffed into Harness CAS merely for convenience unless an explicit owner-neutral artifact contract is demonstrated.

This preserves responsibility placement.

## 24. Analysis should be reproducible without pretending physical replay

Future Agent should be able to:

```text
load raw evidence
+ load calibration relation
+ load analysis code
→ regenerate derived plots/classifications
```

This is **analysis replay**.

It is not:

```text
recreate same physical specimen state
recreate same contact geometry
recreate same environment
```

which is physical reproducibility/rematerialization and belongs across F10–F13.

Thus:

```text
ComputationalReplay
!= PhysicalReproduction
```

## 25. Reproducibility levels

### R0 — historical readability

A fresh Agent can understand what files/receipts refer to.

### R1 — analytical recomputation

Derived results can be regenerated from retained digital evidence.

### R2 — apparatus rematerialization

A future Agent can rebuild/rebind/calibrate the physical apparatus from F05/F10/F12 evidence.

### R3 — physical response reproduction

A fresh specimen/apparatus run reproduces the target response within declared boundaries.

### R4 — heterogeneous reproduction

Independent device/specimen/location/carrier reproduces the target standing.

F14 primarily enables R0/R1 and binds evidence needed by R2+. It does not claim R3/R4 from archived data alone.

## 26. Evidence currentness versus evidence integrity

A file can remain byte-perfect while its interpretation becomes obsolete.

Example:

```text
camera frame digest valid forever
```

but later:

```text
old calibration discovered invalid for that resolution
```

Therefore:

```text
IntegrityCurrent
!= InterpretationCurrent
```

The raw evidence remains historically authentic; derived position standing may be superseded.

## 27. Supersession should target interpretation, not rewrite history

Example:

```text
DERIVED-VISION-01
used calibration CAL-CAM-01
```

later found invalid.

Correct:

```text
DERIVED-VISION-02
recomputed from same raw frame
with CAL-CAM-02
supersedes DERIVED-VISION-01 for target X
```

Incorrect:

```text
edit old derived file so it looks like CAL-CAM-02 was always used
```

This reuses existing snapshot `supersedes` practice.

## 28. Provenance graph should emerge from references, not require a graph DB

A future logical graph may look like:

```text
Specimen C07
  usedIn → Attempt A14
Attempt A14
  executedBy → Runtime Attempt R42
  usedBinding → Motor M1 generation G2
  usedFixture → F10-G3
  usedCalibration → CAL-FORCE-04
  generated → raw-force.csv
  generated → frame-003.png
raw-force.csv
  derivedInto → force-series-v2.parquet
frame-003.png
  derivedInto → tip-position-v1.csv
```

This graph can be reconstructed from bounded references in files/manifests.

No graph database is earned until query/recovery pressure shows file-based reconstruction is insufficient.

## 29. W3C PROV mapping is an export option

If cross-tool interoperability becomes valuable, the above relations can map naturally to PROV concepts:

- data/artifacts → Entity;
- experiment/analysis/calibration activity → Activity;
- Agent/Human/software/instrument actor as appropriate → Agent/entity context;
- `used`, `wasGeneratedBy`, `wasDerivedFrom`, attribution/association.

But internal Ordivon owner semantics may remain more precise than generic PROV.

Therefore:

```text
PROV export/view
!= internal semantic owner replacement
```

## 30. RO-Crate promotion path

RO-Crate becomes attractive when an experiment/campaign must be:

- shared outside Ordivon;
- published with paper/data;
- archived for long-term reuse;
- transferred to another laboratory;
- consumed by generic research-data tools.

Then a bounded E1 campaign can export:

```text
raw/derived files
+ attempt metadata
+ software/equipment context
+ provenance links
→ RO-Crate 1.3 package
```

Current disposition:

```text
RO-Crate = EXPORT/INTERCHANGE POD
```

not live E1 runtime requirement.

## 31. BagIt promotion path

BagIt is useful where:

- large directories must be transferred/archived;
- payload integrity is primary;
- recipient need not understand Ordivon semantics.

Possible later path:

```text
RO-Crate metadata
inside or alongside
BagIt-style integrity package
```

if archival/export tooling benefits.

Do not adopt both by symmetry before one external consumer exists.

## 32. FAIR promotion path

FAIR pressure appears when data should be found/reused outside the original campaign.

Local E1 does not need global PIDs for every attempt.

Possible later escalation:

```text
local stable attempt/sample IDs
→ campaign/public dataset DOI/IGSN/other PID
→ searchable metadata/export
```

F11 IGSN and F14 RO-Crate/FAIR are complementary future paths.

## 33. Privacy/security/size boundaries

Physical lab evidence may later contain:

- room imagery;
- faces/Human presence;
- proprietary samples;
- credentials in logs;
- network/device identifiers;
- sensitive research results.

Therefore raw evidence retention is not always monotonic good.

Future data policy may need:

- capture minimization;
- redaction derived copy while retaining protected original only when justified;
- access control;
- retention limits;
- secret filtering.

F14 does not create a privacy regime now; it records this as a promotion pressure.

## 34. Human-readable first-look matters

A technically complete archive can still fail Agent/Human recovery if first encounter requires searching hundreds of files.

Each attempt should eventually have one compact first-look representation:

```text
what was being tested?
what happened?
which evidence is decisive?
what remains UNKNOWN/contradictory?
where are raw payloads?
which chain generations were used?
what should a future Agent revalidate before action?
```

This is a Representation Environment problem, not a new truth owner.

## 35. First-look summary must remain re-enterable

A summary should never strand the consumer away from source evidence.

Strong pattern:

```text
summary statement
→ exact raw/derived/owner refs
→ re-entry possible
```

Weak pattern:

```text
“E1 passed”
```

with no path to evidence.

This directly consumes Book Chapter 2 / Media representation research.

## 36. Evidence selection is operation-relative

A future Agent asking:

> Was motor motion blocked?

may need:

- camera;
- force;
- command log.

A future Agent asking:

> Was force calibration still valid?

needs:

- raw calibration;
- fixture generation;
- reference masses;
- remount/overload history.

Therefore no one fixed “minimal evidence view” serves every question.

The archive preserves source re-entry; the representation layer compiles a bounded view for the current consumer.

## 37. Attempt closure is not scientific truth

An attempt may be mechanically closed while interpretation remains:

- UNKNOWN;
- contradictory;
- rejected;
- awaiting domain analysis.

Thus:

```text
EvidenceClosure
!= ScientificAcceptance
```

F04 already established this. F14 must preserve it in archival representation.

## 38. Attempt-local naming

A simple stable local attempt ID is sufficient for E1.

Avoid encoding mutable meaning into the ID.

For example:

```text
E1-A14
```

can identify an attempt while semantic labels such as `blocked` remain derived/classified fields.

Do not create IDs like:

```text
successful-blocked-test-...
```

that prejudge the result.

## 39. Data format selection should follow data shape

### Small tabular time series

CSV is acceptable for first E1 because it is transparent and durable.

Parquet becomes useful when:

- data volume rises;
- typed columns/performance matter;
- many campaigns need analytical scanning.

### Images

Use ordinary lossless PNG/TIFF where target requires losslessness; JPEG can be acceptable for qualitative documentation but not by default for quantitative pixel analysis if compression matters.

### Waveforms

CSV/NPZ/HDF5/vendor-native + exported open form depending size and metadata needs.

### Large multidimensional future data

HDF5/Zarr/OME-Zarr/domain standards may become appropriate later.

F14 does not impose one universal file format.

## 40. Proprietary/native instrument formats

If an instrument produces a rich native file:

```text
retain native source when it contains nontrivial metadata/reanalysis value
+ export an open/simple form where practical
```

Do not immediately discard native data after CSV export if future analysis might need hidden metadata.

But native format should not be the only path when vendor lock-in threatens long-term access.

This is a dual-representation strategy, not mandatory duplication for every sensor.

## 41. Time alignment provenance

For multimodal E1, preserve how samples/frames were aligned:

- same instrument sample clock;
- settle-state index;
- hardware trigger;
- host timestamp;
- manual/visual alignment.

Do not merely output one synchronized table if alignment assumptions cannot later be inspected.

F03 owns timing mechanisms; F14 preserves the relation used by analysis.

## 42. Reanalysis after calibration change

One of the strongest F14 capabilities is:

```text
Historical raw data
+ new valid calibration interpretation
→ new derived result
```

without changing the historical physical attempt.

This is allowed only if the new calibration relation is defensibly applicable to that historical measurement chain generation.

F12 retains that authority.

## 43. Reanalysis after software improvement

Likewise:

```text
old raw frame
+ better fiducial detector
→ new position estimate
```

can improve derived evidence.

But the new result should record:

- analysis code/version;
- source frame digest;
- old/new derivation relation;
- whether standing changed.

This is precisely why raw image retention has high option value.

## 44. Deleted/superseded analysis code can remain historically recoverable through Git

Computing's current historical compression already relies on exact Git history for removed studies/files.

For E1 analysis:

```text
analysis script path + exact commit
```

can remain enough even if the script later leaves the current tree, provided history remains reachable.

Do not copy every historical source tree into each experiment directory.

## 45. Physical evidence loss should be explicit

If a raw frame is accidentally lost but a derived scalar remains:

```text
raw frame unavailable
```

must remain visible.

Do not claim equivalent reanalysis capability.

Similarly if one modality failed:

```text
force present
camera missing
```

this is a bounded evidence gap, not reason to discard the whole attempt automatically.

## 46. Completeness is target-relative

An attempt archive can be complete for:

> Did the independent power cut stop future motion?

while incomplete for:

> What exact peak force occurred during cut?

Therefore:

```text
ArchiveComplete
requires target/question
```

Avoid one global completeness score.

## 47. Experiment closure checklist should remain derived, not truth authority

A lightweight closure process may verify:

- capsule exists;
- referenced owner receipts resolve;
- payload digests verify;
- raw target-critical files present;
- UNKNOWN/contradictions recorded;
- post-state recorded where required.

But passing this checker proves archival mechanics, not scientific correctness.

This mirrors existing Computing evidence validators.

## 48. First F14 deletion test — no new service

When E1 physically exists, close one attempt using only:

```text
Runtime Job/Attempt/Artifact evidence
+ immutable attempt-local manifest
+ ordinary raw files
+ SHA-256 digests
+ Git revision references
+ F05/F10/F11/F12/F13 owner references
+ short first-look summary
```

Then give a fresh Agent only the ordinary project entry points.

Ask it to recover:

1. what was attempted;
2. exact device/fixture/specimen/calibration generations;
3. what physically observed evidence exists;
4. what remains UNKNOWN;
5. reproduce one derived force/vision result;
6. identify whether blind physical retry is permitted;
7. name which owner must be reread for current action.

If successful:

```text
new Laboratory evidence service = deleted
```

## 49. Second F14 deletion test — raw evidence

Create a normal attempt where final result can be recomputed from raw force/frame data.

Then compare archive variants:

A. derived-only;
B. raw + derived.

Ask a fresh Agent an unanticipated but source-answerable question.

If B succeeds and A cannot:

```text
raw retention has proven option value
```

This is the physical analogue of earlier Harness CAS selection experiments.

## 50. Third F14 deletion test — owner duplication

Create a candidate mega-manifest that copies full F05/F11/F12 owner state.

Compare it with a thin manifest containing exact owner references/digests.

After owner state evolves:

- historical attempt should remain interpretable;
- current action should re-read current owner.

If copied state creates ambiguity/drift while references remain clear:

```text
mega-schema duplication rejected
```

## 51. Fourth F14 falsifier — response-loss history

Run/construct the first real response-loss physical attempt.

Archive:

- dispatch receipt;
- missing/ambiguous response;
- initial UNKNOWN;
- independent reconciliation evidence;
- later resolution.

A fresh Agent must distinguish:

```text
what was known at T1
from
what became known at T2
```

If archive collapses them, continuity failed.

## 52. Fifth F14 falsifier — calibration supersession

Recompute one historical force dataset with a later calibration only if F12 says applicable.

Preserve:

```text
raw data unchanged
old derived result historical
new derived result superseding for target
reason/reference for change
```

A fresh Agent must recover both histories without ambiguity.

## 53. Sixth F14 falsifier — same bytes, different entity

Include two byte-identical small reference files from different semantic roles/owners.

Their SHA-256 digests will match.

The archive must still preserve distinct owner/role/entity references.

This directly guards against hash-as-identity collapse.

## 54. Seventh F14 falsifier — missing payload

Intentionally use a safe disposable test archive where one noncritical raw payload is removed after manifest closure.

Validator/recovery should surface:

```text
missing / integrity failure
```

rather than silently relying on derived data.

Do not destroy unique real evidence merely to run the test; use a copy/surrogate archive.

## 55. Eighth F14 falsifier — first-look deletion

Give one fresh Agent the full archive with no first-look summary and another a compact source-linked first-look representation.

Measure:

- recovery accuracy;
- source re-entry;
- time/tool burden;
- false-authority mistakes.

If first-look materially helps without hiding challenge paths, it earns itself as Representation Environment infrastructure.

## 56. Ninth F14 falsifier — RO-Crate export

Only after a real E1 campaign exists, export one campaign to RO-Crate when there is a plausible external/shared consumer.

Test whether:

- source data remain intact;
- Ordivon-native owner semantics can be linked without distortion;
- recipient can discover equipment/software/data/provenance;
- export does not become a second current-state authority.

If no consumer exists, defer this test.

## 57. Tenth F14 falsifier — data-volume pressure

Track first real campaign size.

If ordinary files + Runtime Artifacts + Git manifests remain manageable:

```text
dedicated object store/data lake remains deferred
```

Promote only when actual image/waveform volume, transfer, indexing or retention becomes the bottleneck.

## 58. Data-substrate escalation ladder

### D0 — ordinary attempt files

```text
files + manifest + digests
```

Current target.

### D1 — Runtime Artifact / owner-native immutable storage

Use when execution already emits durable artifacts.

### D2 — lightweight experiment archive/CAS

Promote when binary size/reuse/retention makes D0/D1 insufficient.

### D3 — research-data package/export

RO-Crate / BagIt / repository upload / DOI etc.

### D4 — queryable scientific data infrastructure

Parquet/DuckDB, object storage, metadata catalog, domain data lake.

Promote only under many-campaign query/scale pressure.

### D5 — institutional LIMS/ELN/data platform

Only when F11/F15/domain throughput/collaboration/regulatory pressure requires it.

Current E1 target: D0/D1.

## 59. Evidence preservation should be asymmetric

It is often cheap to keep:

- tiny manifests;
- calibration CSV;
- still frames;
- controller logs;
- code refs.

It can be expensive to keep:

- continuous multi-camera video;
- high-rate raw waveforms;
- large microscopy stacks.

Therefore retention policy should spend storage where **future question option value × irreproducibility** is high.

A one-time physical failure frame may deserve stronger retention than hours of normal operation.

## 60. Irreproducible events deserve higher raw-retention priority

Examples:

- unexpected slip;
- fracture;
- response-loss state;
- overload near miss;
- unusual environmental event;
- specimen destruction.

These cannot always be recreated safely or identically.

Thus:

```text
EvidenceRetentionPriority
increases with
Irreversibility + DiagnosticUniqueness
```

This is a useful F14 positive construction law.

## 61. Routine repeatable calibration checks can be more aggressively summarized

If raw data are cheap, keep them.

But after long periods of high-frequency routine measurement assurance, retained structure may become:

- raw recent window;
- control chart / residual summary;
- anomaly-triggered full raw retention;
- periodic representative raw checks.

Only after volume proves this necessary.

Current E1 is too small to optimize retention prematurely.

## 62. Agent replacement contract

A future Agent should not need the original chat/context to understand an attempt.

Minimum success:

```text
Find attempt
→ read first-look
→ resolve exact owner references
→ verify payload integrity
→ inspect raw/derived distinction
→ reproduce one analysis
→ see UNKNOWN/contradictions
→ know what is historical vs current
→ revalidate current owners before physical action
```

This is F14's primary continuity acceptance test.

## 63. Human replacement is the same underlying pressure

A future Human collaborator should also be able to recover:

- apparatus state;
- specimen lineage;
- calibration relation;
- evidence basis;
- limitations.

Thus F14 is not “Agent metadata”. It is durable experiment legibility for finite successors generally.

## 64. Evidence does not have to be centralized to be continuous

This is the strongest Ordivon-specific principle in F14:

```text
Distributed owner-native evidence
+ exact durable references
+ source re-entry
+ bounded first-look representation
can provide continuity
without centralized truth
```

This mirrors Situation/Observation/owner-native architecture results elsewhere in Ordivon.

## 65. F14 current implementation ceiling

Before real E1 data exist, F14 should **not** implement a new service or universal schema.

The current admissible engineering work is only:

- use existing immutable-evidence conventions;
- define a thin attempt-local manifest when E1 is built;
- produce raw files from actual devices;
- bind owner-native receipts/digests;
- test fresh-Agent recovery;
- then reopen storage/interface questions from observed failure.

No synthetic mega-schema should be built now.

## 66. OWN / USE / EXPORT / DEFER disposition

| Capability | Current disposition | Reason |
|---|---|---|
| immutable attempt-local manifest | **USE / FIRST when E1 exists** | bounded cross-owner join |
| Runtime Job/Attempt/Artifact refs | **USE EXISTING** | physical execution owner |
| Host Task continuity ref | **USE EXISTING** | research/open-work continuity |
| F05/F10/F11/F12/F13 exact refs | **USE EXISTING** | preserve owner authority |
| SHA-256 payload digests | **USE / FIRST** | integrity/content identity |
| ordinary attempt files | **USE / FIRST** | enough for first small E1 |
| raw force ADC/calibration data | **RETAIN / FIRST** | high recomputation value |
| raw settled camera frames | **RETAIN / FIRST** | high spatial option value |
| continuous full-session video | **DEFER / selective** | high storage, weak first consumer |
| compact first-look source-linked summary | **OWN-EARLY** | succession/re-entry aid |
| new Laboratory evidence service | **REJECT NOW** | existing substrates likely sufficient |
| new global provenance ontology | **REJECT NOW** | PROV + owner semantics sufficient |
| dedicated Lab CAS/object store | **DEFER** | no volume/retention pressure yet |
| graph database | **DEFER** | refs can reconstruct current graph |
| RO-Crate 1.3 export | **POD / future publication/share** | mature research packaging |
| BagIt export | **POD / archive-transfer** | mature integrity packaging |
| FAIR/DOI publication workflow | **DEFER / publication-driven** | no current external dataset consumer |
| data lake/LIMS/ELN | **DEFER** | no scale/collaboration/regulatory pressure |

## 67. Positive capability language

### Recomputable Physical Evidence Capability

Ordivon can preserve sufficiently raw, integrity-bound observations so future Agents can recompute derived force/vision results when analysis or calibration improves without rerunning the physical event.

### Distributed Provenance Continuity Capability

A physical attempt can remain legible across Agent/process replacement by joining exact owner-native evidence without centralizing device, specimen, calibration or execution truth.

### Historical Uncertainty Preservation Capability

UNKNOWN, contradiction and later reconciliation can survive archival without retrospective rewriting, preserving what was known at each time.

### Evidence Re-entry Capability

A compact first-look representation can direct a finite successor from conclusion back to decisive raw/derived/owner evidence rather than forcing blind archive search or hiding challenge paths.

### Interpretation Revision Capability

Raw evidence remains immutable while derived interpretations can be recomputed, superseded and challenged as calibration/models improve.

### Irreversible-Event Preservation Capability

Rare destructive or non-repeatable physical events can receive stronger raw-retention priority because future Reality cannot necessarily recreate the same evidence.

### External Research Assimilation Capability

When sharing/publishing becomes real, Ordivon can export bounded research objects through mature PROV/RO-Crate/BagIt/FAIR mechanisms without turning those formats into internal authority.

## 68. F14 standing

The first Laboratory evidence substrate is not a new product.

It is the composition:

```text
Runtime Artifact / Attempt evidence
+ immutable attempt-local join manifest
+ ordinary raw payload files
+ SHA-256 digests
+ exact Git/source refs
+ F05/F10/F11/F12/F13 owner refs
+ explicit UNKNOWN/contradictions
+ compact source-linked first-look summary
```

### Strongest retained distinctions

```text
RawEvidence != Reality
RawEvidence != DerivedResult
DerivedResult != Standing
HistoricalEvidence != CurrentStanding
Digest != EntityIdentity
Integrity != InterpretationCurrentness
ComputationalReplay != PhysicalReproduction
AttemptClosure != ScientificAcceptance
Retention != PromotionIntoCognition
```

### Strongest anti-overbuild result

```text
ExperimentalContinuity
!= CentralizedEvidenceDatabase
```

and:

```text
ProvenanceGraph
can emerge from durable references
before a graph database exists
```

### Strongest implementation stop rule

No new F14 service/schema is admitted before one real E1 attempt tests the thin composition and demonstrates a concrete continuity/recovery failure.

## 69. Next family boundary

F15 — External/Shared Capability, Simulation and Domain Expansion is the final planned family.

It should now answer from all prior families:

```text
When should Ordivon own a capability locally versus use NMC, fabrication service, environmental chamber, university/shared laboratory, cloud/remote instrument or simulation?
How do external capability contracts preserve identity/currentness/authority/evidence without local ownership?
When can simulation replace physical experiment, and when can it only guide it?
How should new domains (chemistry, biology, materials, optics, robotics, RF, energy) enter without prebuilding every laboratory?
Which capabilities have already been proven external/shared-first by F01–F14?
```

F15 must integrate CCE's source-neutral capability construction and then close the 15-family Atlas with a minimal first physical build boundary.
