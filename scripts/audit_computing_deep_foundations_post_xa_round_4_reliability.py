#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'research/COMPUTING-DEEP-FOUNDATIONS-POST-XA-ROUND-4-RELIABLE-FAULT-TOLERANT-SELF-STABILIZING-COMPUTATION-20260818.md'
EVD = ROOT / 'research/evidence/computing-deep-foundations-post-xa-round-4-reliability-20260818.json'
text = ART.read_text()
data = json.loads(EVD.read_text())
checks=[]

def ck(name, cond):
    checks.append((name, bool(cond)))

ck('status_complete', data['status']=='round-complete')
ck('hypothesis_exact', data['hypothesis']=='ComputationalReliabilityAndResilienceUnderFaultsResponsibility')
ck('hypothesis_rejected', data['hypothesis_disposition']=='REJECTED_AS_CLEAN_INDEPENDENT_SIBLING')
ck('derived_profile', data['derived_profile']=='ComputationalFaultResilienceProfile')
ck('no_foundation', data['foundation_admission']=='NONE')
ck('closure_not_claimed', data['whole_computing_closure']=='NOT_CLAIMED')
ck('cdf0_not_admitted', data['cdf0']=='NOT_ADMITTED')
ck('cdf_count_zero', data['numbered_cdf_count']==0)
ck('next_cdf_unknown', data['next_cdf']=='UNKNOWN')
ck('regime_count_12', len(data['regimes'])==12)
ck('anti_collapse_ge_28', len(data['anti_collapse_laws'])>=28)
ck('burden_count_7', len(data['burden_deletion'])==7)
ck('independent_burden_empty', data['independent_reliability_burden_after_subtraction']=='EMPTY_AT_CURRENT_EVIDENCE_FRONTIER')
ck('rival_count_7', len(data['rival_verdicts'])==7)
ck('RF_M6_survives', data['rival_verdicts']['RF-M6_reliability_is_model_indexed_composition']=='STRONG_SURVIVOR')
ck('RF_M7_rejected', data['rival_verdicts']['RF-M7_independent_reliability_responsibility']=='REJECTED_AS_CLEAN_SIBLING')
ck('architecture_count_10', len(data['architecture_effects'])==10)
ck('no_new_owner', data['owner_boundary']['new_owner_boundary']=='NONE')
ck('primary_anchor_count_5', len(data['primary_anchors'])==5)
ck('four_consolidations', len(data['consolidation_sequence'])==4)
ck('stop_new_sibling_none', data['stopping_rule_evaluation']['NewSibling']=='NONE')
ck('stop_BGHI_none', data['stopping_rule_evaluation']['B_G_H_I_Falsified']=='NONE')
ck('stop_crosscut_none', data['stopping_rule_evaluation']['A_C_D_F_J_K_Reopened']=='NONE')
ck('stop_owner_none', data['stopping_rule_evaluation']['NewOwnerBoundary']=='NONE')
ck('stop_trigger', data['stopping_rule_evaluation']['result']=='TRIGGER_FORMAL_WHOLE_COMPUTING_COVERAGE_SATURATION_TEST')
ck('final_round_complete', data['final_state']['round_4']=='COMPLETED')
ck('final_info_gain', data['final_state']['information_gain']=='VERY_HIGH_CONSOLIDATING')
ck('final_closure_not_claimed', data['final_state']['whole_computing_closure']=='NOT_CLAIMED')
ck('final_cdf0_not_admitted', data['final_state']['cdf0']=='NOT_ADMITTED')
ck('final_count_zero', data['final_state']['numbered_cdf_count']==0)
ck('final_next_cdf_unknown', data['final_state']['next_cdf']=='UNKNOWN')
ck('final_phase_saturation', data['final_state']['next_computing_research_phase']=='FORMAL_WHOLE_COMPUTING_COVERAGE_SATURATION_TEST')

for law in data['anti_collapse_laws']:
    ck('law_' + law.split(' != ')[0], law in text)

for burden in data['burden_deletion']:
    ck('burden_' + burden, burden in text)

for heading in [
    'Noisy Boolean formulas',
    'Fault model is not failure probability',
    'Quantum threshold fault tolerance',
    'Error correction and redundancy',
    'Self-stabilization',
    'Byzantine / arbitrary faults',
    'Crash/restart and checkpoint recovery',
    'Detection, masking, correction and recovery',
    'Replication / redundancy / coded computation',
    'Correlated faults and common-mode failure',
    'Reliability is not availability',
    'Approximate / graceful-degradation negative control',
    'Agent/provider/tool failures',
    'Direct deletion',
    'Saturation trigger fires'
]:
    ck('heading_' + heading.replace(' ','_').replace('/','_'), heading in text)

required = [
    'IndependentReliabilityBurdenAfterSubtraction\n= EMPTY AT CURRENT EVIDENCE FRONTIER',
    'ComputationalReliabilityAndResilienceUnderFaultsResponsibility\n= REJECTED AS CLEAN INDEPENDENT SIBLING',
    'ComputationalFaultResilienceProfile\n= DERIVED / OPTIONAL',
    'WholeComputingCoverageSaturationTest\n= SHOULD BEGIN NEXT',
    'WholeComputingClosure\n= NOT CLAIMED',
    'CDF0\n= NOT ADMITTED',
    'NextComputingResearchPhase\n= FORMAL WHOLE-COMPUTING COVERAGE / SATURATION TEST'
]
for s in required:
    ck('required_' + s.splitlines()[0], s in text)

failed=[name for name,ok in checks if not ok]
print(f'checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)}')
for name,ok in checks:
    print(('PASS' if ok else 'FAIL'), name)
if failed:
    raise SystemExit(1)
