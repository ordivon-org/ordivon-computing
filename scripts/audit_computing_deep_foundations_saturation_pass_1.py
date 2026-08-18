#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'research/COMPUTING-DEEP-FOUNDATIONS-FORMAL-WHOLE-COMPUTING-SATURATION-TEST-PASS-1-ARCHITECTURE-FALSIFICATION-20260818.md'
EVD = ROOT / 'research/evidence/computing-deep-foundations-formal-whole-computing-saturation-pass-1-20260818.json'
text = ART.read_text()
norm_text = ' '.join(text.split())
data = json.loads(EVD.read_text())
checks = []

def ck(name, cond): checks.append((name, bool(cond)))

ck('status_complete', data['status']=='pass-complete')
ck('four_entry_consolidations', len(data['entry']['consolidation_sequence'])==4)
ck('entry_closure_not_claimed', data['entry']['whole_computing_closure']=='NOT_CLAIMED')
ck('entry_cdf0_not_admitted', data['entry']['cdf0']=='NOT_ADMITTED')
ck('seven_attacks', len(data['attacks'])==7)
ck('unknown_none', data['attacks']['unknown_continent']=='NO_FALSIFIER_FOUND')
ck('coverage_no_major_omission', data['attacks']['historical_modern_coverage_checksum']=='NO_MAJOR_OMITTED_CONTINENT_FOUND')
ck('B_survives', data['attacks']['B_contract_stuffing'].startswith('SURVIVES'))
ck('C_guarded', 'OVERBREADTH_RISK' in data['attacks']['C_contract_stuffing'])
ck('G_falsified', data['attacks']['BGHI_merge_split']=='G_CLEAN_SIBLING_FALSIFIED')
ck('JK_profiles', data['attacks']['JK_further_deletion'].startswith('NAMED_PROFILE_UTILITY_SURVIVES'))
ck('owner_inversion_none', data['attacks']['owner_boundary_inversion']=='NO_FALSIFIER_FOUND')
ck('coverage_source_17', data['coverage_checksum']['source']=='ACM_IEEE_CS2023_17_KNOWLEDGE_AREAS')
ck('coverage_not_authority', data['coverage_checksum']['ontology_authority'] is False)
ck('coverage_projection_17', len(data['coverage_checksum']['projection'])==17)
ck('B_guards_4', len(data['B_guards'])==4)
ck('C_guards_3', len(data['C_guards'])==3)
ck('G_exact_falsified', data['G_reopen']['disposition']=='FALSIFIED_AT_CURRENT_EVIDENCE_FRONTIER')
ck('G_profile_derived', data['G_reopen']['profile_status']=='DERIVED_HIGH_VALUE')
ck('G_clean_rejected', data['G_reopen']['clean_sibling']=='REJECTED')
ck('G_burden_10', len(data['G_burden_deletion'])==10)
ck('G_empty', data['independent_G_burden_after_post_I_evidence']=='EMPTY_AT_CURRENT_EVIDENCE_FRONTIER')
ck('siblings_BI', data['provisional_architecture_after_pass1']['strong_sibling_candidates']==['B_RESOURCE_FEASIBILITY','I_EFFECTIVE_SOLVABILITY_RELATIVE_POWER'])
ck('H_reclass', data['provisional_architecture_after_pass1']['reclassification_required']==['H_PHYSICAL_REALIZATION_GROUNDING'])
ck('derived_count_7', len(data['provisional_architecture_after_pass1']['derived_cross_cutting_profiles'])==7)
ck('H_open', data['H_pressure']['status']=='OPEN_HIGH_PRIORITY_RECLASSIFICATION')
ck('H_not_falsified', data['H_pressure']['not_yet_falsified'] is True)
ck('SCD_rev9', 'revision 9' in data['specialized_owner_controls']['SCD'])
ck('Algorithmics_rev8', 'revision 8' in data['specialized_owner_controls']['Algorithmics'])
ck('saturation_not_established', data['saturation_verdict']['whole_computing_saturation']=='NOT_ESTABLISHED')
ck('pass1_falsifier', data['saturation_verdict']['pass1']=='ARCHITECTURE_FALSIFIER_FOUND')
ck('closure_not_claimed', data['saturation_verdict']['whole_computing_closure']=='NOT_CLAIMED')
ck('cdf0_not_admitted', data['foundation_state']['cdf0']=='NOT_ADMITTED')
ck('count_zero', data['foundation_state']['numbered_cdf_count']==0)
ck('next_cdf_unknown', data['foundation_state']['next_cdf']=='UNKNOWN')
ck('next_H', data['next_route'].startswith('H_PHYSICAL_REALIZATION_GROUNDING'))

for law in data['B_guards']:
    ck('B_law_' + law.split(' != ')[0], ' '.join(law.split()) in norm_text)
for law in data['C_guards'][:1]:
    ck('C_law', ' '.join(law.split()) in norm_text)
for burden in data['G_burden_deletion']:
    ck('G_burden_' + burden, burden in text)

required = [
    'IndependentGBurdenAfterPostIEvidence\n= EMPTY AT CURRENT EVIDENCE FRONTIER',
    'ComputationalCoordinationConsistencyAndProgressResponsibility\n= REJECTED AS CLEAN SIBLING',
    'ComputationalCoordinationProfile\n= DERIVED / HIGH-VALUE DOMAIN PROFILE',
    'CurrentArchitectureSaturated\n= FALSIFIED',
    'WholeComputingSaturation\n= NOT ESTABLISHED',
    'WholeComputingClosure\n= NOT CLAIMED',
    'CDF0\n= NOT ADMITTED',
    'NextComputingResearchRoute\n= H SIBLING-VS-GROUNDING-BRIDGE DESTRUCTIVE RECLASSIFICATION'
]
for s in required:
    ck('required_' + s.splitlines()[0], s in text)

for heading in [
    'Historical / modern coverage checksum',
    'Unknown-continent search',
    'B contract-stuffing attack',
    'C contract-stuffing',
    'Direct merge/split attack on G',
    'I/O automata provide a direct hostile reduction',
    'Direct deletion of G',
    'H becomes the next architecture-level pressure point',
    'Owner-boundary inversion',
    'Saturation hypothesis verdict'
]:
    ck('heading_' + heading.replace(' ','_').replace('/','_'), heading in text)

failed=[name for name,ok in checks if not ok]
print(f'checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)}')
for name,ok in checks:
    print(('PASS' if ok else 'FAIL'), name)
if failed:
    raise SystemExit(1)
