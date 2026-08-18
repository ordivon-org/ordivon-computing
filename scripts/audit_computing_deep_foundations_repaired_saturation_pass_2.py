#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'research/COMPUTING-DEEP-FOUNDATIONS-REPAIRED-SATURATION-PASS-2-OWNER-DECOMPOSITION-RECONCILIATION-20260818.md'
EVD = ROOT / 'research/evidence/computing-deep-foundations-repaired-saturation-pass-2-owner-reconciliation-20260818.json'
text = ART.read_text()
norm = ' '.join(text.split())
data = json.loads(EVD.read_text())
checks=[]

def ck(name, cond): checks.append((name, bool(cond)))
def has(s): return ' '.join(s.split()) in norm

ck('status_complete', data['status']=='complete')
ck('entry_BI', data['entry']['clean_siblings_before_pass2']==['B_RESOURCE_FEASIBILITY','I_EFFECTIVE_SOLVABILITY_RELATIVE_POWER'])
ck('project_count_2', data['canonical_owner_constraint']['project_count']==2)
ck('broad_owner_rejected_constraint', data['canonical_owner_constraint']['broad_computing_owner']=='REJECTED')
ck('resource_inside_T', data['canonical_owner_constraint']['resource_complexity_inside_T'] is True)
ck('shared_not_third', data['canonical_owner_constraint']['shared_role_model_is_third_owner'] is False)
ck('S_is_SCD', data['canonical_successors']['S']['code']=='SCD')
ck('T_is_CP', data['canonical_successors']['T']['project']=='Computational Possibility')
ck('T_responsibility_5', len(data['canonical_successors']['T']['responsibility'])==5)
ck('BI_distinct_truth', data['BI_relation']['resource_complexity_vs_effective_status']=='DISTINCT_TRUTH_DIMENSIONS')
ck('BI_owner_independence_rejected', data['BI_relation']['owner_independence']=='REJECTED')
ck('B_owner_T', data['BI_relation']['B_owner']=='T_COMPUTATIONAL_POSSIBILITY')
ck('I_owner_T', data['BI_relation']['I_owner']=='T_COMPUTATIONAL_POSSIBILITY')
ck('bounded_feasibility_existential', data['BI_relation']['bounded_feasibility_form'].startswith('ORDINARY_EXISTENCE'))
ck('AlgF0_withdrawn', data['I_generic_existence_reconciliation']['current_status']=='WITHDRAWN_SUPERSEDED_AS_NUMBERED_FOUNDATION')
ck('generic_exist_rejected', data['I_generic_existence_reconciliation']['generic_existence_primitive']=='REJECTED_DELETION_ESSENTIALITY')
ck('B_real', data['B_survivor']['status']=='REAL_IRREDUCIBLE_TRUTH_DIMENSION_INSIDE_T')
ck('B_not_broad', data['B_survivor']['broad_clean_sibling'] is False)
ck('I_real', data['I_survivor']['status']=='REAL_T_OWNED_THEORY_AFTER_GENERIC_EXISTENCE_DELETION')
ck('I_not_broad', data['I_survivor']['broad_clean_sibling'] is False)
ck('matrix_12', len(data['owner_subtraction_matrix'])==12)
ck('broad_empty', data['broad_result']['broad_computing_exclusive_responsibility_after_owner_subtraction']=='EMPTY_AT_CURRENT_EVIDENCE_FRONTIER')
ck('clean_count_zero', data['broad_result']['broad_computing_clean_sibling_count']==0)
ck('broad_owner_rejected', data['broad_result']['broad_computing_owner']=='REJECTED_NOT_ADMITTED')
ck('shared_interface_nonowner', data['broad_result']['shared_computational_role_model_interface']=='PRESERVED_NON_OWNER')
ck('H_bridge', data['broad_result']['H_grounding']=='CROSS_OWNER_BRIDGE_HYPEREDGE')
ck('saturation_not_applicable', data['saturation_retyping']['single_owner_whole_computing_saturation']=='NOT_APPLICABLE_UNDER_CURRENT_ARCHITECTURE')
ck('exhaustive_not_claimed', data['saturation_retyping']['whole_computing_exhaustive_complete']=='NOT_CLAIMED')
ck('decomposition_reconfirmed', data['saturation_retyping']['broad_owner_decomposition']=='RECONFIRMED')
ck('cdf0_not_admitted', data['foundation_state']['cdf0']=='NOT_ADMITTED')
ck('cdf_basis_absent', data['foundation_state']['cdf_namespace_admission_basis']=='ABSENT_UNDER_CURRENT_OWNER_ARCHITECTURE')
ck('cdf_count_zero', data['foundation_state']['numbered_cdf_count']==0)
ck('next_cdf_none', data['foundation_state']['next_cdf']=='NONE_UNDER_CURRENT_OWNER_ARCHITECTURE')
ck('campaign_closeout_ready', data['campaign_state']['broad_computing_deep_foundations_campaign'].startswith('CLOSEOUT_READY'))
ck('next_final_audit', data['campaign_state']['next_broad_phase']=='FINAL_UMBRELLA_CLOSEOUT_CONSISTENCY_AUDIT')
ck('successors_2', data['campaign_state']['successor_research']==['SCD','COMPUTATIONAL_POSSIBILITY'])
ck('reopen_5', len(data['reopen_conditions'])==5)
ck('anchors_2', len(data['primary_anchors'])==2)

required = [
    'truth-dimension independence != project-owner independence',
    'GenericComputationalExistence != deletion-essential primitive',
    'B-vs-I truth independence != B-vs-I owner independence',
    'BroadComputingExclusiveResponsibilityAfterOwnerSubtraction = EMPTY AT CURRENT EVIDENCE FRONTIER',
    'BroadComputingOwner = REJECTED / NOT ADMITTED',
    'BroadComputingCleanSiblingCount = 0',
    'SharedComputationalRoleModelInterface = PRESERVED = NOT A THIRD PROJECT = NOT CDF0 = NOT A HIDDEN BROAD ROOT',
    'SingleOwnerWholeComputingSaturation = NOT APPLICABLE UNDER CURRENT ARCHITECTURE',
    'WholeComputingExhaustiveComplete = NOT CLAIMED',
    'CDFNamespaceAdmissionBasis = ABSENT UNDER CURRENT OWNER ARCHITECTURE',
    'BroadComputingDeepFoundationsCampaign = CLOSEOUT-READY AS UMBRELLA DECOMPOSITION / RESEARCH HISTORY',
    'NextBroadComputingResearchPhase = FINAL UMBRELLA CLOSEOUT / CONSISTENCY AUDIT'
]
for s in required:
    ck('required_' + s.split(' = ')[0], has(s))

for heading in [
    'The decisive canonical constraint predates A-K',
    'Canonical successor owner identities now exist',
    'Direct B-vs-I theorem-form attack',
    'Independent Computational Possibility evidence destroys generic-existence primitiveness',
    'Whole A-K owner-subtraction matrix',
    'Shared ComputationalRole / ComputationalModel does not rescue a broad owner',
    'Broad Computing owner verdict',
    'WholeComputingSaturation needs re-typing',
    'Broad campaign closeout state',
    'Reopen condition for broad Computing'
]:
    ck('heading_' + heading.replace(' ','_').replace('/','_'), heading in text)

failed=[n for n,ok in checks if not ok]
print(f'checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)}')
for n,ok in checks:
    print(('PASS' if ok else 'FAIL'), n)
if failed:
    raise SystemExit(1)
