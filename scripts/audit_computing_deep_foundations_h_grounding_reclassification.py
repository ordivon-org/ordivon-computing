#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'research/COMPUTING-DEEP-FOUNDATIONS-H-PHYSICAL-REALIZATION-GROUNDING-SIBLING-VS-BRIDGE-RECLASSIFICATION-20260818.md'
EVD = ROOT / 'research/evidence/computing-deep-foundations-h-grounding-reclassification-20260818.json'
text = ART.read_text()
norm_text = ' '.join(text.split())
data = json.loads(EVD.read_text())
checks=[]

def ck(name, cond): checks.append((name, bool(cond)))

def has_norm(s): return ' '.join(s.split()) in norm_text

ck('status_complete', data['status']=='complete')
ck('attack_exact', data['attack_target']=='ComputationalPhysicalRealizationAndGroundingResponsibility')
ck('entry_G_falsified', data['entry_state']['G_clean_sibling']=='FALSIFIED')
ck('entry_B_strong', data['entry_state']['B']=='STRONG_SIBLING_CANDIDATE')
ck('entry_I_strong', data['entry_state']['I']=='STRONG_SIBLING_CANDIDATE')
ck('entry_H_reclass', data['entry_state']['H']=='RECLASSIFICATION_REQUIRED')
ck('rivals_4', len(data['rivals'])==4)
ck('H_R3_rejected', data['rivals']['H-R3_independent_H_sibling']=='REJECTED')
ck('H_R4_survives', data['rivals']['H-R4_cross_owner_grounding_bridge']=='STRONG_SURVIVOR')
ck('burdens_11', len(data['burden_deletion'])==11)
ck('sibling_empty', data['sibling_result']['independent_H_sibling_burden_after_subtraction']=='EMPTY_AT_CURRENT_EVIDENCE_FRONTIER')
ck('sibling_rejected', data['sibling_result']['clean_sibling_disposition']=='REJECTED')
ck('bridge_name', data['bridge_result']['name']=='ComputationalPhysicalRealizationGroundingBridge')
ck('bridge_type', data['bridge_result']['architecture_type']=='CROSS_OWNER_BRIDGE_HYPEREDGE')
ck('bridge_survives', data['bridge_result']['status']=='STRONG_SURVIVOR')
ck('bridge_nonempty', data['bridge_result']['independent_bridge_relation']=='NONEMPTY_STRONG')
ck('bridge_schema_14', len(data['bridge_schema'])==14)
ck('anti_pan_7', len(data['anti_pancomputational_laws'])==7)
ck('SCD_rev11', 'revision 11' in data['owner_controls']['SCD'])
ck('World_rev31', 'revision 31' in data['owner_controls']['World'])
ck('repaired_siblings_BI', data['repaired_architecture']['strong_clean_sibling_candidates']==['B_RESOURCE_FEASIBILITY','I_EFFECTIVE_SOLVABILITY_RELATIVE_POWER'])
ck('derived_7', len(data['repaired_architecture']['derived_cross_cutting'])==7)
ck('one_bridge', data['repaired_architecture']['cross_owner_bridges']==['H_PHYSICAL_REALIZATION_GROUNDING_BRIDGE'])
ck('final_complete', data['final_state']['H_reclassification']=='COMPLETED')
ck('final_H_rejected', data['final_state']['H_clean_sibling']=='REJECTED')
ck('final_bridge_survives', data['final_state']['H_bridge']=='STRONG_SURVIVOR')
ck('saturation_not_established', data['final_state']['whole_computing_saturation']=='NOT_ESTABLISHED')
ck('closure_not_claimed', data['final_state']['whole_computing_closure']=='NOT_CLAIMED')
ck('cdf0_not_admitted', data['final_state']['cdf0']=='NOT_ADMITTED')
ck('count_zero', data['final_state']['numbered_cdf_count']==0)
ck('next_unknown', data['final_state']['next_cdf']=='UNKNOWN')
ck('next_restart', data['final_state']['next_computing_research_phase'].startswith('RESTART_FORMAL_WHOLE'))

burden_anchors = {
    'AbstractComputationalTarget': 'H-28.1 Abstract computational target/model',
    'PhysicalSystemBoundary': 'H-28.2 Physical substrate/system boundary',
    'EncodingPreparationRelation': 'H-28.3 Encoding / preparation relation',
    'PhysicalEvolutionOperationRelation': 'H-28.4 Physical evolution / operation relation',
    'ReadoutDecodingObservationRelation': 'H-28.5 Readout / decoding / observation relation',
    'CounterfactualDomainSupport': 'H-28.6 Counterfactual/domain support',
    'FidelityToleranceError': 'H-28.7 Fidelity / tolerance / error relation',
    'PhysicalModelAssumptionsCurrentness': 'H-28.8 Physical-model assumptions/currentness',
    'ResourcePhysicalLimits': 'H-28.9 Resource / physical-limit references',
    'RealizationEvidence': 'H-28.10 Realization evidence / validation basis',
    'MiscomputationOutOfModel': 'H-28.11 Miscomputation / out-of-model disposition'
}
for burden, anchor in burden_anchors.items():
    ck('burden_' + burden, anchor in text)
for law in data['anti_pancomputational_laws']:
    ck('law_' + law.split(' != ')[0], has_norm(law))

required = [
    'IrreducibleRelation != IndependentSiblingOwnerByNecessity',
    'IndependentHSiblingBurdenAfterSubtraction = EMPTY AT CURRENT EVIDENCE FRONTIER',
    'IndependentPhysicalComputationalGroundingBridgeRelation = NONEMPTY / STRONG',
    'ComputationalPhysicalRealizationGroundingBridge',
    'CROSS-OWNER BRIDGE / HYPEREDGE',
    'HBridgeIrreducibility = ESTABLISHED AT CURRENT FRONTIER',
    'HSiblingIrreducibility = REJECTED',
    'WholeComputingSaturation = NOT ESTABLISHED',
    'WholeComputingClosure = NOT CLAIMED',
    'CDF0 = NOT ADMITTED',
    'NextComputingResearchPhase = RESTARTED FORMAL WHOLE-COMPUTING SATURATION TEST'
]
for s in required:
    ck('required_' + s.split(' = ')[0], has_norm(s))

for heading in [
    'Primary rival grounding theories',
    'Direct deletion of Round H',
    'Encoding / preparation relation',
    'Physical evolution / operation relation',
    'Counterfactual/domain support',
    'Anti-pancomputational pressure survives',
    'Cross-owner bridge reconstruction',
    'Why bridge is the correct architecture type',
    'Repaired provisional architecture',
    'Next phase'
]:
    ck('heading_' + heading.replace(' ','_').replace('/','_'), heading in text)

failed=[n for n,ok in checks if not ok]
print(f'checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)}')
for n,ok in checks:
    print(('PASS' if ok else 'FAIL'), n)
if failed:
    raise SystemExit(1)
