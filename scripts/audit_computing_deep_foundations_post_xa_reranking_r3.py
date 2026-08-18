#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'research/COMPUTING-DEEP-FOUNDATIONS-POST-XA-FRESH-RESIDUAL-RERANKING-R3-20260818.md'
EVD = ROOT / 'research/evidence/computing-deep-foundations-post-xa-fresh-residual-reranking-r3-20260818.json'
text = ART.read_text()
data = json.loads(EVD.read_text())
checks=[]

def ck(name, cond): checks.append((name, bool(cond)))

ck('status_complete', data['status']=='complete')
ck('three_consolidations', data['entry_state']['consolidation_sequence']==['J_STATE_MEMORY','K_INFORMATION_CODING','X-A_ACCESS_REVELATION_CHANGE'])
ck('closure_not_claimed_entry', data['entry_state']['whole_computing_closure']=='NOT_CLAIMED')
ck('cdf0_not_admitted_entry', data['entry_state']['cdf0']=='NOT_ADMITTED')
ck('candidate_count_9', len(data['candidates'])==9)
ck('winner_rank_1', data['candidates'][0]['rank']==1)
ck('winner_exact', data['candidates'][0]['id']=='R3-A' and data['candidates'][0]['verdict']=='WINNER')
ck('control_rank_2', data['candidates'][1]['id']=='CONTROL')
ck('realtime_rank_3', data['candidates'][2]['id']=='R3-B')
ck('proof_rank_4', data['candidates'][3]['id']=='R3-C')
ck('unknown_no_better', data['fresh_unknown_continent_result']['new_continent_above_winner'] is False)
ck('winner_route_fault', data['winner']['route'].startswith('Reliable / Fault-Tolerant / Self-Stabilizing'))
ck('hypothesis_not_admitted', data['winner']['hypothesis_status']=='NOT_ADMITTED')
ck('no_foundation', data['winner']['foundation_status']=='NONE')
ck('subtraction_broad', len(data['winner']['required_subtraction'])>=14)
ck('hostile_cases_12', len(data['winner']['hostile_cases'])==12)
ck('term_separations_12', len(data['term_separations_for_next_round'])==12)
ck('owner_evidence_5', len(data['owner_evidence'])==5)
ck('primary_anchor_5', len(data['primary_anchor_claims'])==5)
ck('saturation_trigger', data['saturation_rule']['if_next_tournament_consolidates_without_new_sibling']=='BEGIN_FORMAL_WHOLE_COMPUTING_COVERAGE_SATURATION_TEST')
ck('saturation_conditions_4', len(data['saturation_rule']['conditions'])==4)
ck('final_r3_complete', data['final_state']['post_xa_reranking_r3']=='COMPLETED')
ck('final_closure_not_claimed', data['final_state']['whole_computing_closure']=='NOT_CLAIMED')
ck('final_cdf0_not_admitted', data['final_state']['cdf0']=='NOT_ADMITTED')
ck('final_count_zero', data['final_state']['numbered_cdf_count']==0)
ck('final_next_cdf_unknown', data['final_state']['next_cdf']=='UNKNOWN')
ck('final_route_selected', data['final_state']['next_computing_research_tournament'].startswith('Reliable / Fault-Tolerant / Self-Stabilizing'))

required = [
    'CoordinationFailureModel\n!= GenericComputationalFaultModel',
    'RecoveryFromKnownRetainedState\n!= SelfStabilizationFromAdmissibleCorruption',
    'QuantumComputation\n!= FaultTolerantQuantumComputation',
    'PhysicalQuantumRealization\n!= ReliabilityUnderNoise',
    'ComputationalReliabilityAndResilienceUnderFaultsResponsibility',
    'ThreeConsecutiveConsolidations',
    'WholeComputingClosure\n= NOT CLAIMED',
    'CDF0\n= NOT ADMITTED',
    'Reliable / Fault-Tolerant / Self-Stabilizing Computation\nunder explicit Fault / Perturbation Models'
]
for s in required:
    ck('artifact_' + s.splitlines()[0], s in text)

for heading in [
    'Reliable / Fault-Tolerant / Self-Stabilizing Computation',
    'Real-Time / Embedded / Cyber-Physical Computation',
    'Proof / Verification / Synthesis / Certification',
    'Optimization / Approximation / Parameterized Structure',
    'Circuit / Nonuniform / Structural computation models',
    'Unknown-continent control',
    'Comparative reranking',
    'Saturation decision rule'
]:
    ck('heading_' + heading.replace(' ','_'), heading in text)

for sep in data['term_separations_for_next_round']:
    ck('term_' + sep.split(' != ')[0], sep in text)

failed=[n for n,ok in checks if not ok]
print(f'checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)}')
for n,ok in checks:
    print(('PASS' if ok else 'FAIL'), n)
if failed:
    raise SystemExit(1)
