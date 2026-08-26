# External Source Map — Pressure Selection / Experiment Allocation

Status: bounded comparative source map; external sources are positive solution-domain knowledge, not Ordivon authority.

## Optimal experimental design

- **NIST/SEMATECH Engineering Statistics Handbook — D-Optimal Designs.** D-optimal design maximizes the determinant of the information matrix for a pre-specified model; NIST explicitly notes that optimality is model-dependent and the experimenter must specify the model/objective. This supports `no context-free optimal experiment`.
- **Robert D. McMichael, NIST (2019), Optimal Bayesian Experimental Design.** Bayesian OED can reduce uncertainty with fewer measurements when measurements are costly in money, time, risk, labor or discomfort, while introducing computational/automation cost. This supports closed-loop cost and model-relative design.
- **Wu, Chen & Ghattas (2023), An Offline-Online Decomposition Method for Efficient Linear Bayesian Goal-Oriented Optimal Experimental Design.** Goal-oriented OED targets expected information gain about a model-dependent quantity of interest rather than indiscriminately minimizing uncertainty in every parameter. This supports target-relative information value.

## Value of information

- **Fenwick et al. (2020), ISPOR Value of Information Analysis for Research Decisions — Report 1.** VoI asks whether reducing uncertainty can improve downstream resource-allocation decisions.
- **Rothery et al. (2020), ISPOR Value of Information Analytical Methods — Report 2.** EVPI, EVPPI, EVSI and expected net benefit of sampling connect evidence value to a specified decision problem and sampling cost. This supports `information != value independent of decision/utility`.

## Metareasoning

- **Russell & Wefald / Stuart Russell research summary on rational metareasoning.** Computation steps are selected according to expected value in improving the quality of the agent's next physical-world decision. This absorbs the generic idea of allocating finite internal reasoning/search budget by downstream decision value.

## Existing Ordivon external absorption

`research/experiments/pal-foundations-v0/wave4-external-source-map-v0.json` already preserves adjacent sources including:

- Arumugam & Van Roy (2021), *The Value of Information When Deciding What to Learn*;
- Wang & Powell (2016), knowledge-gradient policy;
- CURIOUS, POET and Unsupervised Environment Design for predefined goal/environment selection;
- recent AI-scientist / co-scientist / open-ended agent work as bounded hypothesis sources rather than authority.

## Comparative conclusion

The generic optimization space is mature and heterogeneous. The stable Ordivon residual is therefore not a new VoI/OED algorithm. It is preserving owner-native admission/currentness/consequence boundaries, selecting the mature criterion that matches the actual uncertainty geometry, and empirically testing whether Agents can acquire the right evidence under partial views and later calibrate their research-selection priors.
