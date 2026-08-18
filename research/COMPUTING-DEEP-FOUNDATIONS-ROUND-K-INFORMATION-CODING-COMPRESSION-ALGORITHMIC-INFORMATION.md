---
schema_version: 1
id: computing.research.deep-foundations.round-k.information-coding-compression-algorithmic-information
title: Ordivon Computing Deep Foundations — Round K: Information / Coding / Compression / Algorithmic Information
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-computing
updated: 2026-08-18
summary: Destructive tournament over Shannon information, entropy, mutual information, coding, channel capacity, redundancy, lossless/lossy compression, rate-distortion, side information and algorithmic information. The pass rejects Information, Entropy, MutualInformation, Compression, Redundancy, ChannelCapacity, KolmogorovComplexity, Randomness and DescriptionLength as universal Computing primitives. Shannon pressure separates statistical information from semantic meaning and makes entropy/capacity distribution/model-relative; Hamming pressure shows redundancy can increase recoverability; rate-distortion shows required code rate depends on an admitted distortion criterion; Slepian-Wolf shows coding rate can depend on side information/correlation; Kolmogorov/Chaitin pressure separates individual-description complexity from Shannon ensemble entropy and ties algorithmic information to an effective reference machine while exact shortest-description complexity is not an ordinary computable observable. Most of M3 InformationTransformation reduces into C representation/semantics, B resource/capacity bounds, D distortion/error, F distribution assumptions, H physical carriers, J retention, Network actual transport and generic mathematics. A narrower cross-cutting survivor remains: ComputationalInformationCodingAndRecoverabilityConstraintResponsibility. It governs declared source/object model, information quantity, code/decoder relation, side-information assumptions, recoverability/distortion target and information-theoretic bounds. It is not a clean independent sibling and M3 is rejected as a universal definition of computation.
evidence_status: strong-local-plus-primary-source-pressure
readiness: ROUND_K_COMPLETE_INFORMATION_TRANSFORMATION_REJECTED_CROSS_CUTTING_CODING_CONSTRAINT_SURVIVES
---
# Ordivon Computing Deep Foundations — Round K

## Information / Coding / Compression / Algorithmic Information

## 0. Admission discipline

Round K is not `CDF0`.

The target is the long-unresolved rival:

```text
M3 — Computation = Information Transformation
```

The round asks whether `information` names an independent Computing substrate or whether its major formal roles factor into previously established responsibilities.

---

# 1. Information is not semantic meaning

Shannon's communication theory deliberately treats source statistics, coding and reliable transmission without requiring semantic interpretation of message content.

## K-F1

Two messages can have the same probability/code length while meaning entirely different things.

```text
SameShannonInformation
!= SameSemanticMeaningByIdentity.
```

## K-F2

Two semantically equivalent messages can use different encodings and probability models.

```text
SameMeaning
!= SameShannonInformationByNecessity.
```

## K-F3

Therefore:

```text
InformationQuantity
!= SemanticContentByIdentity.
```

C retains semantic meaning/interpretation.

---

# 2. Shannon entropy is a property of a declared distribution/model

## K-F4

An individual symbol/string does not carry one Shannon entropy value independently of a source distribution.

```text
IndividualMessage
!= ShannonEntropyCarrierByIdentity.
```

## K-F5

The same alphabet can have different entropy under different source probabilities.

```text
SameAlphabet
!= SameEntropy.
```

## K-F6

Two different distributions can have the same entropy.

```text
SameEntropy
!= SameSourceDistribution.
```

## K-F7

Therefore:

```text
EntropyWithoutSourceDistributionSemantics
= underspecified.
```

F supplies distribution semantics where probabilistic source models are used.

---

# 3. Entropy is not physical storage size

## K-F8

A fixed-width representation can use 64 bits even when the modeled source entropy is much lower.

```text
StoredBitLength
!= ShannonEntropyByIdentity.
```

## K-F9

A compressed representation can approach a source-coding limit only under assumptions about source statistics/block regime/code family.

```text
Entropy
!= ObservedCompressedFileSizeByIdentity.
```

## K-F10

Memory/storage footprint remains B/J/H territory rather than entropy identity.

---

# 4. Compression is not computation's essence

## K-F11

Decompression deliberately increases representation length.

```text
Computation
!= CompressionByIdentity.
```

## K-F12

Error-correcting encoders intentionally add symbols.

```text
UsefulComputation
can increase representation redundancy.
```

## K-F13

Sorting, control, theorem checking and state transition can preserve, expand or reduce encoded length depending on representation.

Therefore:

```text
InformationCompressionDirection
!= UniversalComputationDirection.
```

M3 loses its simplest `computation = reducing uncertainty/description` form.

---

# 5. Redundancy is not waste

Hamming-style coding adds carefully structured redundancy so errors can be detected/corrected.

## K-F14

```text
Redundancy
!= UselessDuplicationByIdentity.
```

## K-F15

More transmitted/stored bits can yield greater recoverability of the original message under noise.

```text
MoreBits
!= MoreSourceInformationByIdentity.
```

## K-F16

Compression and error correction can pull representation size in opposite directions while both serving valid computational contracts.

```text
CompressionObjective
!= ReliabilityObjective.
```

D supplies error/recoverability criteria; B supplies resource cost.

---

# 6. Coding is not encryption or semantics

## K-F17

A source/channel code changes representation to improve rate/reliability; it need not hide content.

```text
Coding
!= EncryptionByIdentity.
```

## K-F18

A codeword's decoding relation is not its semantic interpretation relation.

```text
CodewordDecoding
!= SemanticMeaningByIdentity.
```

C may interpret the decoded object further.

---

# 7. Channel capacity is model-relative, not observed bandwidth

Shannon capacity is defined for a declared channel/probability model and asymptotic coding regime.

## K-F19

```text
ChannelCapacity
!= MeasuredThroughputByIdentity.
```

## K-F20

```text
ChannelCapacity
!= LinkBitRateByIdentity.
```

## K-F21

Actual Network topology/congestion/latency/reachability do not become Shannon capacity theorems automatically.

```text
NetworkMeasurement
!= InformationTheoreticCapacityClaim.
```

## K-F22

Conversely a capacity theorem does not establish a deployed link realizes its assumed channel model.

```text
CapacityTheorem
!= NetworkDeploymentEvidence.
```

Network owns actual transport; B/K may reference abstract channel-use/rate bounds.

---

# 8. Mutual information is not meaning or causation

## K-F23

Mutual information measures statistical dependence under a joint distribution.

```text
MutualInformation
!= SemanticRelevanceByIdentity.
```

## K-F24

Mutual information is symmetric while causal influence is directional.

```text
MutualInformation
!= CausalInfluenceByIdentity.
```

## K-F25

A variable can be highly predictive/correlated without being the computational target or cause.

```text
HighMutualInformation
!= ComputationalResponsibilityByIdentity.
```

World owns causal truth; C owns meaning/specification.

---

# 9. Data processing constraints do not define computation

## K-F26

Under a Markov/data-processing setup, postprocessing cannot create additional mutual information about an upstream variable beyond what the intermediate representation contains.

But:

```text
DataProcessingInequality
!= DefinitionOfComputation.
```

## K-F27

A computation can create new derived values/proofs/representations while not creating new statistical information about a specific hidden source.

```text
DerivedComputationalNovelty
!= NewMutualInformationAboutChosenSourceByIdentity.
```

The information quantity is query-variable-relative.

---

# 10. Lossless and lossy compression are different contracts

## K-F28

Lossless coding requires exact reconstruction of the source object under the declared decoding relation.

Lossy coding permits deviations under a distortion/fidelity criterion.

```text
LosslessCompression
!= LossyCompressionByIdentity.
```

## K-F29

A lossy representation can be valid even when the original bytes cannot be recovered.

```text
ValidLossyCode
!= RecoverOriginalRepresentationExactly.
```

## K-F30

Round D is required to define acceptable distortion/error; `compression ratio` alone cannot establish validity.

---

# 11. Rate-distortion destroys intrinsic `minimum bits` intuition

Shannon's fidelity-criterion work makes the minimum asymptotic rate depend on both a source model and an admitted distortion criterion.

## K-F31

```text
RequiredCodingRate
!= SourceOnlyIntrinsicScalarByIdentity.
```

## K-F32

Change the distortion metric/tolerance and the admissible rate can change.

```text
SameSource
!= SameRateDistortionRequirementAcrossSpecifications.
```

## K-F33

Therefore information/coding claims often require D/C specification semantics.

---

# 12. Side information changes required description rate

Slepian-Wolf pressure shows correlated sources can be encoded separately yet jointly decoded at rates depending on correlation/conditional entropies.

## K-F34

```text
RequiredDescriptionLength
!= ObjectIntrinsicLengthIndependentOfSideInformation.
```

## K-F35

```text
InformationNeededToRecoverX
can depend on what decoder already knows about Y.
```

## K-F36

Thus:

```text
InformationRequirement
is context/decoder-side-information-relative.
```

This links directly to J's retained/external state and C's decoding context.

---

# 13. Correlation is not shared semantics

## K-F37

Two sources can be statistically correlated while representing unrelated meanings under a semantic layer.

```text
SourceCorrelation
!= SharedMeaningByIdentity.
```

## K-F38

Likewise semantically related representations need not have high raw statistical correlation under arbitrary encodings.

```text
SemanticRelation
!= StatisticalCorrelationByIdentity.
```

---

# 14. Algorithmic information is not Shannon entropy

Kolmogorov's algorithmic approach moves from ensemble probability to effective shortest descriptions of individual objects, relative to a reference computational formalism.

## K-F39

```text
KolmogorovComplexityOfString
!= ShannonEntropyOfSourceByIdentity.
```

## K-F40

A single fixed string can have an algorithmic description-length notion even when no source distribution is declared.

```text
AlgorithmicInformation
!= RequiresProbabilisticSourceModel.
```

## K-F41

Conversely Shannon entropy can be defined for random variables without asking for the shortest program for each realized sequence.

```text
ShannonInformation
!= AlgorithmicInformationByIdentity.
```

---

# 15. Algorithmic complexity is reference-machine-relative up to invariance structure

## K-F42

Different universal description machines can assign different shortest program lengths to the same finite string.

Therefore:

```text
ProgramDescriptionLength
!= AbsoluteRepresentationIndependentScalarByIdentity.
```

## K-F43

The invariance idea controls differences between suitable universal machines only up to an additive translation constant rather than literal equality.

Therefore:

```text
KolmogorovComplexity
!= ExactMachineIndependentIntegerByIdentity.
```

## K-F44

Reference model/current encoding semantics must be explicit when constants matter for finite objects.

I/C remain relevant.

---

# 16. Practical compressor length is not Kolmogorov complexity

## K-F45

A real codec searches only a tiny structured family of descriptions and adds headers/dictionaries/format costs.

Therefore:

```text
CompressedFileLengthByCodec
!= KolmogorovComplexityByIdentity.
```

## K-F46

A codec failing to compress a string does not prove algorithmic incompressibility.

```text
CodecIncompressibility
!= AlgorithmicIncompressibilityTheorem.
```

Runtime evidence again differs from abstract theorem.

---

# 17. Algorithmic randomness is not probabilistic randomness by identity

## K-F47

An individual finite/infinite sequence can be studied for incompressibility/patternlessness under an algorithmic criterion even without being generated by a stochastic device in the current run.

```text
AlgorithmicRandomness
!= PhysicalOrOperationalRandomGenerationByIdentity.
```

## K-F48

A pseudorandom generator can produce statistically useful-looking sequences from short seeds, which are algorithmically generated from short descriptions.

```text
StatisticalRandomnessAppearance
!= HighAlgorithmicComplexityByIdentity.
```

F/H retain source/randomness realization semantics.

---

# 18. Kolmogorov complexity links to I rather than replacing it

## K-F49

Shortest-description complexity is defined through effective programs/machines, so algorithmic information depends on I's computational model.

```text
AlgorithmicInformation
requires EffectiveDescriptionModelReference.
```

## K-F50

Exact shortest-description complexity is not an ordinary uniformly computable quantity over arbitrary strings in the base effective model.

Therefore:

```text
DefinedInformationQuantity
!= EffectivelyComputableObservableByNecessity.
```

This reinforces I's decidability/computability distinctions.

---

# 19. Information quantity is not computational power

## K-F51

A memory containing many random bits does not thereby provide an oracle for an undecidable language unless the admitted model grants a usable relation between those bits and the target answers.

```text
LargeInformationContent
!= OracleCapabilityByIdentity.
```

## K-F52

A short program can generate arbitrarily long regular output.

```text
OutputLength
!= SolverPowerOrProgramInformationByIdentity.
```

## K-F53

A large table/advice object may increase nonuniform solver power only when explicitly admitted as I auxiliary information.

```text
StoredInformation
!= ComputationalPowerWithoutAccessSemantics.
```

---

# 20. Information quantity is not retained computational state

## K-F54

Two states with equal encoded bit length can have different continuation behavior.

```text
SameInformationSize
!= SameComputationalStateByIdentity.
```

## K-F55

A compact sufficient state can preserve continuation while a much larger archive contains irrelevant history.

```text
MoreStoredInformation
!= MoreContinuationRelevantStateByIdentity.
```

J remains distinct.

---

# 21. Physical information carrier is not abstract information quantity

## K-F56

The same bit/string/code can be realized on different physical substrates.

```text
InformationObject
!= PhysicalCarrierIdentity.
```

## K-F57

A physical system may contain many distinguishable states, but usable coding capacity depends on preparation/readout/noise/control assumptions.

```text
PhysicalStateCardinality
!= UsableInformationCapacityByIdentity.
```

H remains necessary.

---

# 22. Agent-era `tokens = information` is rejected

## K-F58

Two tokenizations can encode semantically equivalent content with different token counts.

```text
TokenCount
!= SemanticInformationByIdentity.
```

## K-F59

A long context can be mostly redundant while a short retrieved fact is task-critical.

```text
ContextLength
!= TaskRelevantInformationByIdentity.
```

## K-F60

Compression/summarization can preserve selected continuation behavior while losing other information.

```text
SummaryValidity
requires declared downstream task/state sufficiency,
not compression ratio alone.
```

C/J/D apply; no Agent-specific information primitive is required.

---

# 23. Owner subtraction

## Mathematics

Entropy, mutual information, coding inequalities, Kolmogorov complexity and related theorems are mathematical constructs. Computing owns their role inside computational claims, not the total ontology of information theory.

## C — semantics/representation

C owns meaning, representation interpretation, equivalence and target specification.

K cannot equate information quantity with semantics.

## B — resource/feasibility

B owns bit/storage/communication/query cost and feasible resource bounds.

K can provide lower bounds/coding limits but does not make those resource dimensions identical to entropy/capacity.

## D — approximation/error

D owns distortion/fidelity/error specification used by lossy coding and recovery criteria.

## F — probability

F owns probabilistic source/channel models, risk and aggregation semantics when K uses distributions.

## H — physical realization

H owns actual physical carriers, noise sources and preparation/readout fidelity.

## J — retention/reconstruction

J owns whether retained information is sufficient/current for continuation after a boundary.

## Network

Network owns actual transport, reachability, topology, latency and congestion. K may state abstract coding/channel capacity claims without absorbing Network truth.

## Media

Media owns media/signals/perception/expression referents where semantic/communicative artifacts are at issue. Generic Shannon/algorithmic coding constraints do not automatically become Media semantics.

---

# 24. Round B relation

K and B are tightly linked but distinct.

```text
InformationTheoreticLowerBound
!= ResourceUsageObservationByIdentity.
```

K can establish lower/achievable rate constraints under a source/channel model; B places those as resource/feasibility claims.

Therefore K is better treated as a theorem/constraint layer feeding B than as a new resource essence.

---

# 25. Round C relation

C absorbs representation and semantics that information theory intentionally abstracts away.

```text
InformationQuantity
!= SemanticInterpretation.
```

K requires C whenever coding correctness depends on what reconstructed representation/property counts as equivalent/acceptable.

---

# 26. Round D relation

Lossy coding/rate-distortion requires D's metric/error/acceptance semantics.

```text
DistortionMeasure
!= InformationQuantityByIdentity.
```

K supplies rate tradeoffs conditional on the declared D criterion.

---

# 27. Round F relation

Shannon entropy/mutual information/source-channel models are distribution-relative.

F therefore supplies probability-space/source assumptions.

But:

```text
ProbabilityDistribution
!= InformationQuantityByIdentity.
```

K derives information quantities from/relative to those models.

---

# 28. Round H relation

Physical carriers/channels instantiate K's abstract encoding/channel assumptions.

```text
PhysicalCarrierTruth
!= AbstractCodeOrCapacityClaim.
```

H remains the realization bridge.

---

# 29. Round I relation

Algorithmic information depends on an effective description machine/model and immediately inherits I's relative-power/decidability constraints.

Therefore:

```text
AlgorithmicInformation
→ reference I computational model
```

rather than creating a separate notion of effective power.

---

# 30. Round J relation

J asks whether retained information is sufficient for future continuation/reconstruction.

K can quantify/encode information, but:

```text
InformationPreserved
!= ContinuationStateSufficiencyByIdentity.
```

A high-fidelity coding theorem cannot decide which semantic state is operationally relevant without J/C.

---

# 31. Strong residual — Computational Information Coding and Recoverability Constraint Responsibility

A narrower cross-cutting responsibility survives:

```text
ComputationalInformationCodingAndRecoverabilityConstraintResponsibility
```

Current minimum burden:

1. `SourceEnsembleOrIndividualObjectModel`
2. `ProbabilityOrEffectiveDescriptionModelReference`
3. `InformationQuantityOrMeasureType`
4. `EncodingOrCodeRelation`
5. `DecoderOrReconstructionRelation`
6. `SideInformationCorrelationOrConditioningAssumptions`
7. `NoiseChannelOrTransformationModelWhenMaterial`
8. `LosslessOrDistortionRecoverabilityCriterion`
9. `RateCapacityCompressionOrRedundancyClaim`
10. `AsymptoticFiniteBlockOrIndividualObjectRegime`
11. `ResourceBoundReference`
12. `SemanticOrTaskRelevanceDisclaimerReference`
13. `ProofOrCodingTheoremBasis`

The survivor is useful but mostly connects existing responsibilities rather than supplying a new ontological axis.

---

# 32. Why K is not a clean sibling

Most apparent `information` ownership reduces as follows:

```text
meaning / representation       → C
bit/storage/communication cost → B
error/distortion criterion     → D
probability/source model       → F
physical carrier/noise         → H
retained state sufficiency     → J
actual transport               → Network
algorithmic effective model    → I
mathematical quantity/theorem  → Mathematics
```

What remains is a cross-cutting coding/recoverability/bound interface.

Therefore:

```text
STRONG_CROSS_CUTTING_ANALYTIC_CANDIDATE
M3_INFORMATION_TRANSFORMATION_REJECTED_AS_UNIVERSAL_DEFINITION
FEEDS_B_RESOURCE_BOUNDS
REFERENCES_C_D_F_H_I_J
NOT_CLEAN_INDEPENDENT_SIBLING
NOT_CDF0
NOT_ROUTE_SELECTED
```

---

# 33. M3 rival verdict

Naive M3:

```text
Computation = Information Transformation
```

is rejected.

Reasons:

```text
information quantity does not specify semantics
information is measure/model-relative
computation need not compress
redundancy can be useful
same computation can have different encodings/information profiles
same information quantities can accompany unrelated computations
algorithmic information itself depends on effective description model
physical information carrier is not computational realization
```

A weaker scoped form survives:

```text
Many computational claims can be constrained/analyzed by
information quantities, coding relations and recoverability bounds.
```

That is an analytic responsibility, not the essence of computation.

---

# 34. Candidate deletion results

Rejected as universal primitives/scalars:

```text
Information
Entropy
MutualInformation
Compression
Redundancy
Code
ChannelCapacity
Bandwidth
DescriptionLength
KolmogorovComplexity
AlgorithmicRandomness
StatisticalRandomness
SideInformation
Distortion
```

All remain powerful typed constructs.

---

# 35. Anti-collapse laws

```text
ShannonInformation != SemanticMeaning
Entropy != IndividualMessagePropertyWithoutDistribution
SameEntropy != SameDistribution
StoredBits != Entropy
Compression != Computation
Redundancy != Waste
MoreBits != MoreSourceInformation
CompressionObjective != ReliabilityObjective
Coding != Encryption
CodewordDecoding != SemanticMeaning
ChannelCapacity != MeasuredThroughput
ChannelCapacity != LinkBitRate
NetworkMeasurement != CapacityTheorem
CapacityTheorem != DeploymentEvidence
MutualInformation != SemanticRelevance
MutualInformation != Causation
DataProcessingInequality != DefinitionOfComputation
LosslessCompression != LossyCompression
RequiredRate != SourceIntrinsicScalar
InformationRequirement != IndependentOfSideInformation
Correlation != SharedMeaning
KolmogorovComplexity != ShannonEntropy
ProgramDescriptionLength != AbsoluteMachineIndependentScalar
CodecCompressedLength != KolmogorovComplexity
CodecIncompressibility != AlgorithmicIncompressibility
AlgorithmicRandomness != PhysicalRandomGeneration
StatisticalRandomnessAppearance != HighAlgorithmicComplexity
DefinedInformationQuantity != ComputableObservableByNecessity
LargeInformationContent != OracleCapability
OutputLength != ComputationalPower
StoredInformation != PowerWithoutAccessSemantics
SameInformationSize != SameComputationalState
MoreStoredInformation != MoreContinuationRelevantState
InformationObject != PhysicalCarrier
PhysicalStateCardinality != UsableInformationCapacity
TokenCount != SemanticInformation
ContextLength != TaskRelevantInformation
InformationPreserved != ContinuationStateSufficiency
```

---

# 36. Rival-model update

## M1 Function evaluation
Still a scoped behavior shape; information theory does not replace A/C.

## M2 Controlled state transition
Information quantities can describe states/transitions but do not determine computational interpretation.

## M3 Information transformation

```text
REJECTED AS UNIVERSAL DEFINITION.
SURVIVES ONLY AS CROSS-CUTTING ANALYTIC/CODING CONSTRAINT FAMILY.
```

## M4 Effective procedure
I remains independent; algorithmic information references effective description models.

## M5 Resource-bounded process
B remains strong; information-theoretic bounds feed resource feasibility without becoming identical to resources.

## M6 Interactive process
Communication/coding is important in interactive computation but does not define all interaction.

## M7 Physical realization
H remains independent; `physical information processing` is insufficient grounding by itself.

---

# 37. Current factorization after K

```text
                         I
             effective solvability / power
                  /      |      \
                 G       B       H
          coordination resources realization
                 │       ▲       │
                 │       │ K     │
                 │   information │
                 │   coding /    │
                 │   bounds      │
                 └───┬───┴───┬───┘
                     ▼       ▼
                     C       J
                 semantics retention
                     ▲       │
                     └── A ◄─┘

D approximation/error and F probability remain overlays.
K is another cross-cutting analytic layer rather than a sibling node.
```

---

# 38. Information gain / coverage signal

Round K information gain is:

```text
HIGH / CONSOLIDATING / RIVAL-RESOLVING
```

It resolves the last initially listed rival model that had remained substantially open:

```text
M3 Information Transformation
→ rejected as universal definition.
```

Like J, K mostly factors into the existing architecture rather than adding a clean sibling.

Two consecutive large continents now show consolidation:

```text
J State/Memory          → mostly reduced
K Information/Coding    → mostly reduced
```

This is a materially stronger signal that Computing may be moving from continent discovery toward architecture consolidation, though unexplored online/real-time/biological/algorithmic-structure spaces still prevent whole-domain closure.

---

# 39. Next frontier — deliberately unselected

Still-open high-value spaces include:

```text
online / streaming / competitive computation
real-time / cyber-physical deadlines and control
algorithm / data-structure / lower-bound structure beyond generic B
biological / molecular / neuromorphic computation
learning/adaptation as computation after Human/Harness subtraction
```

The next pass should be selected for maximum chance of falsifying the current factorization rather than simply extending coding/state vocabulary.

Still:

```text
CDF0               = NOT ADMITTED
NextCDF            = UNKNOWN
NextComputingRoute = UNKNOWN
```

---

# 40. Primary pressure anchors

Used as pressure sources, not ontology authority:

- Claude E. Shannon, *A Mathematical Theory of Communication*, Bell System Technical Journal 27, 1948.
- R. W. Hamming, *Error Detecting and Error Correcting Codes*, Bell System Technical Journal 29(2), 1950.
- Claude E. Shannon, *Coding Theorems for a Discrete Source With a Fidelity Criterion*, IRE Convention Record, 1959.
- David Slepian and Jack K. Wolf, *Noiseless Coding of Correlated Information Sources*, IEEE Transactions on Information Theory 19(4), 1973.
- A. N. Kolmogorov, *Three approaches to the definition of the concept quantity of information*, Problems of Information Transmission 1(1), 1965.
- Gregory J. Chaitin, *On the Length of Programs for Computing Finite Binary Sequences*, Journal of the ACM 13(4), 1966.
