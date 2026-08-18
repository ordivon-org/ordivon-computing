#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'research/COMPUTING-DEEP-FOUNDATIONS-FINAL-UMBRELLA-CLOSEOUT-AND-OWNER-DECOMPOSITION-INDEX-20260818.md'
EVD = ROOT / 'research/evidence/computing-deep-foundations-final-umbrella-closeout-20260818.json'
text = ART.read_text()
norm = ' '.join(text.split())
data = json.loads(EVD.read_text())
checks=[]

def ck(name, cond): checks.append((name, bool(cond)))
def has(s): return ' '.join(s.split()) in norm

ck('status_complete', data['status']=='complete')
ck('campaign_completed', data['campaign']['state']=='COMPLETED')
ck('campaign_role', data['campaign']['role']=='UMBRELLA_DECOMPOSITION_RESEARCH_HISTORY_ROUTING_INDEX')
ck('broad_owner_rejected', data['campaign']['broad_owner']=='REJECTED_NOT_ADMITTED')
ck('clean_zero', data['campaign']['clean_sibling_count']==0)
ck('exclusive_empty', data['campaign']['exclusive_responsibility']=='EMPTY_AT_CURRENT_EVIDENCE_FRONTIER')
ck('route_reopen_only', data['campaign']['next_broad_route']=='NONE_BY_DEFAULT_REOPEN_ONLY')
ck('projects_two', data['owner_architecture']['project_count']==2)
ck('S_SCD', data['owner_architecture']['S_code']=='SCD')
ck('T_CP', data['owner_architecture']['T']=='COMPUTATIONAL_POSSIBILITY')
ck('shared_nonowner', data['owner_architecture']['shared_role_model_interface']=='PRESERVED_NON_OWNER')
ck('H_bridge', data['owner_architecture']['H_grounding']=='CROSS_OWNER_BRIDGE_HYPEREDGE')
ck('supersession_four', set(data['supersession'])=={'B','G','H','I'})
ck('B_T_owned', data['supersession']['B']['current'].startswith('T_OWNED'))
ck('G_derived', data['supersession']['G']['current']=='DERIVED_COORDINATION_PROFILE')
ck('H_bridge_current', data['supersession']['H']['current']=='CROSS_OWNER_PHYSICAL_GROUNDING_BRIDGE')
ck('I_T_owned', data['supersession']['I']['current'].startswith('T_OWNED'))
ck('I_exist_rejected', data['supersession']['I']['generic_existence']=='REJECTED_DELETION_ESSENTIALITY')
ck('cdf_basis_absent', data['foundation_state']['cdf_namespace_admission_basis']=='ABSENT_UNDER_CURRENT_OWNER_ARCHITECTURE')
ck('cdf0_not', data['foundation_state']['cdf0']=='NOT_ADMITTED')
ck('cdf_count_zero', data['foundation_state']['numbered_cdf_count']==0)
ck('next_cdf_none', data['foundation_state']['next_cdf']=='NONE_UNDER_CURRENT_OWNER_ARCHITECTURE')
ck('saturation_na', data['closure_typing']['single_owner_whole_computing_saturation']=='NOT_APPLICABLE_UNDER_CURRENT_ARCHITECTURE')
ck('exhaustive_not_claimed', data['closure_typing']['whole_computing_exhaustive_complete']=='NOT_CLAIMED')
ck('owner_closeout_complete', data['closure_typing']['owner_decomposition_closeout']=='COMPLETED')
ck('no_historical_rewrite', data['historical_policy']['rewrite_old_provisional_artifacts'] is False)
ck('time_indexed_history', data['historical_policy']['interpret_old_current_claims_as_time_indexed'] is True)
ck('SCD_rev16', data['successor_continuity_observed']['SCD']['revision']==16)
ck('SCD_ready', data['successor_continuity_observed']['SCD']['state']=='ready')
ck('CP_rev6', data['successor_continuity_observed']['ComputationalPossibility']['revision']==6)
ck('CP_ready', data['successor_continuity_observed']['ComputationalPossibility']['state']=='ready')
ck('reopen_six', len(data['reopen_conditions'])==6)
ck('historical_sibling_found', data['consistency_audit']['historical_sibling_phrases_found'] is True)
ck('historical_nextcdf_found', data['consistency_audit']['historical_nextcdf_unknown_phrases_found'] is True)
ck('chronological_supersession', data['consistency_audit']['these_are_chronologically_pre_supersession'] is True)
ck('no_positive_exhaustive_claim', data['consistency_audit']['positive_current_exhaustive_completion_claim_found'] is False)
ck('no_rewrite_required', data['consistency_audit']['historical_rewrite_required'] is False)

required = [
    'HistoricalClaimAtRoundR != CurrentCanonicalClaim',
    'BroadComputingDeepFoundationsCampaign = COMPLETED = CLOSED AS UMBRELLA DECOMPOSITION / RESEARCH HISTORY',
    'BroadComputingOwner = REJECTED / NOT ADMITTED',
    'BroadComputingCleanSiblingCount = 0',
    'WholeComputingExhaustiveComplete = NOT CLAIMED',
    'SingleOwnerWholeComputingSaturation = NOT APPLICABLE UNDER CURRENT ARCHITECTURE',
    'SharedComputationalRoleModelInterface = PRESERVED = NON-OWNER = NOT THIRD PROJECT = NOT CDF0 = NOT HIDDEN BROAD ROOT',
    'A-KStrongSiblingSetCurrent = {}',
    'CDFNamespaceAdmissionBasis = ABSENT UNDER CURRENT OWNER ARCHITECTURE',
    'NextCDF = NONE UNDER CURRENT OWNER ARCHITECTURE',
    'NextBroadComputingRoute = NONE BY DEFAULT / REOPEN-ONLY',
    'BroadComputingHostContinuity = READY TO COMPLETE'
]
for s in required:
    ck('required_' + s.split(' = ')[0], has(s))

headings = [
    'Supersession ledger — A-K closeout',
    'Supersession ledger — G',
    'Supersession ledger — H',
    'Supersession ledger — B',
    'Supersession ledger — I',
    'Supersession ledger — CDF state',
    'Supersession ledger — WholeComputingSaturation',
    'A-K/post-AK owner projection index',
    'Historical artifacts are immutable research history',
    'No hidden exhaustive-closure claim',
    'Successor owner continuity at closeout time',
    'Reopen conditions for this broad umbrella',
    'Current first-lookup routing',
    'Canonical final state'
]
for h in headings:
    ck('heading_' + h.replace(' ','_').replace('/','_'), h in text)

# Verify historical files still exist and the superseding chain exists as separate artifacts.
files = [
    'research/COMPUTING-DEEP-FOUNDATIONS-WHOLE-DOMAIN-A-K-CLOSEOUT-AND-OPEN-HANDOFF-20260818.md',
    'research/COMPUTING-DEEP-FOUNDATIONS-FORMAL-WHOLE-COMPUTING-SATURATION-TEST-PASS-1-ARCHITECTURE-FALSIFICATION-20260818.md',
    'research/COMPUTING-DEEP-FOUNDATIONS-H-PHYSICAL-REALIZATION-GROUNDING-SIBLING-VS-BRIDGE-RECLASSIFICATION-20260818.md',
    'research/COMPUTING-DEEP-FOUNDATIONS-REPAIRED-SATURATION-PASS-2-OWNER-DECOMPOSITION-RECONCILIATION-20260818.md'
]
for f in files:
    ck('exists_' + Path(f).name, (ROOT/f).exists())

# Current closeout itself must not assert exhaustive completion positively.
ck('artifact_no_positive_exhaustive_true', not has('WholeComputingExhaustiveComplete = TRUE'))
# It must explicitly explain that a historical literal TRUE string, if discussed, is rejected; this closeout avoids using it entirely.

failed=[n for n,ok in checks if not ok]
print(f'checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)}')
for n,ok in checks:
    print(('PASS' if ok else 'FAIL'), n)
if failed:
    raise SystemExit(1)
