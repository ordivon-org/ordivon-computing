from pathlib import Path
p=Path('research/COMPUTING-DEEP-FOUNDATIONS-WHOLE-DOMAIN-A-K-CLOSEOUT-AND-OPEN-HANDOFF-20260818.md')
s=p.read_text()
checks=[]
def check(name,cond): checks.append((name,bool(cond)))
check('exists', p.exists())
for token in ['WholeComputingSearchA-K = COMPLETED RESEARCH HISTORY','CDF0                    = NOT ADMITTED','NextCDF                 = UNKNOWN','NextComputingRoute      = UNKNOWN','WholeComputingClosure   = NOT CLAIMED']:
    check('frontier-'+token.split()[0], token in s)
for r in ['Round A','Round B','Round C','Round D','Round F','Round G','Round H','Round I','Round J','Round K']:
    check('has-'+r.replace(' ','-').lower(), r in s)
for cand in ['ComputationalResourceAndFeasibilityResponsibility','ComputationalCoordinationConsistencyAndProgressResponsibility','ComputationalPhysicalRealizationAndGroundingResponsibility','ComputationalEffectiveSolvabilityAndRelativePowerResponsibility']:
    check('strong-'+cand.lower(), cand in s)
for cand in ['ComputationalBoundaryAndBehaviorResponsibility','ComputationalInterpretationAndSemanticRelationResponsibility','ComputationalStateRetentionAndReconstructionResponsibility','ComputationalInformationCodingAndRecoverabilityConstraintResponsibility']:
    check('cross-'+cand.lower(), cand in s)
for open_space in ['U-A — Online / Streaming / Competitive Computation','U-B — Real-Time / Embedded / Cyber-Physical Computation','U-C — Algorithms / Data Structures / Lower-Bound Structure','U-D — Biological / Molecular / Neuromorphic Computation','U-E — Learning / Adaptation as Computation','U-F — Proof / Verification / Synthesis / Meta-Computation','U-G — Security/Cryptographic Computational Structure After Owner Subtraction','U-H — Unconventional Spatial / Dynamical Regimes']:
    check('open-'+open_space[:3], open_space in s)
check('m3-rejected', 'M3 Information Transformation\n= REJECTED as universal definition' in s)
check('no-roadmap', 'They are only known partial-open areas.' in s and 'Do not turn U-A through U-H as a roadmap.' not in s)
check('prompt-present', '# 22. New-conversation prompt' in s)
check('fresh-search', 'fresh unexplored-space / information-gain search' in s)
check('reopen-discipline', '# 19. Reopen discipline' in s)
check('a-k-closed', 'A–K research history   = CLOSED FOR THIS CAMPAIGN' in s)
failed=[x for x in checks if not x[1]]
for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
print(f'SUMMARY {len(checks)-len(failed)}/{len(checks)} passed')
raise SystemExit(1 if failed else 0)
