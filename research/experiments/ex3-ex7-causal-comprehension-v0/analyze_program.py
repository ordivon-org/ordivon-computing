#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'evidence'
STAGES = ['ex3','ex4','ex5','ex6','ex7']


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path: Path) -> str:
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def pct_delta(new: int, baseline: int) -> float:
    return round((new / baseline - 1.0) * 100.0, 4)


def main() -> int:
    docs = {s: load(EVIDENCE / f'{s}-live-v1.json') for s in STAGES}
    expected = {'ex3':102,'ex4':408,'ex5':204,'ex6':204,'ex7':408}
    for s,d in docs.items():
        assert d['complete'] is True, s
        assert d['analysis']['acceptedTrials'] == expected[s], (s,d['analysis']['acceptedTrials'])
        assert len(d.get('failures',[])) == 0, s
        assert sum(v['correct'] for v in d['analysis']['byTreatment'].values()) == expected[s], s

    conflicts={}
    for s in STAGES:
        corpus=load(ROOT/f'{s}-corpus-v1.json')
        bad=[]
        for c in corpus['cases']:
            if c['oracleDecision'] in c.get('criticalUnsafeOptions',[]):
                bad.append({'familyId':c['familyId'],'oracleDecision':c['oracleDecision'],'criticalUnsafeOptions':c['criticalUnsafeOptions']})
        conflicts[s]=bad

    summaries={}
    for s,d in docs.items():
        a=d['analysis']
        summaries[s]={
          'complete':d['complete'],
          'corpusDigest':d['corpusDigest'],
          'evidenceDigest':sha(EVIDENCE/f'{s}-live-v1.json'),
          'acceptedTrials':a['acceptedTrials'],
          'reportedProviderTokens':a['providerTokens'],
          'acceptedPhysicalProviderCalls':a['physicalProviderCalls'],
          'allPhysicalProviderCalls':a.get('physicalProviderCallsAllAttempts',a['physicalProviderCalls']),
          'unsafeMetricValid':not conflicts[s],
          'oracleUnsafeConflicts':conflicts[s],
          'treatments':a['byTreatment'],
        }

    total_accepted=sum(x['acceptedTrials'] for x in summaries.values())
    total_correct=sum(v['correct'] for d in docs.values() for v in d['analysis']['byTreatment'].values())
    total_tokens=sum(x['reportedProviderTokens'] for x in summaries.values())
    total_accepted_calls=sum(x['acceptedPhysicalProviderCalls'] for x in summaries.values())
    total_all_calls=sum(x['allPhysicalProviderCalls'] for x in summaries.values())
    assert (total_accepted,total_correct,total_tokens,total_accepted_calls,total_all_calls)==(1326,1326,954329,1326,1330)

    ex3=docs['ex3']['analysis']['byTreatment']['compact_prose']
    ex3_deficit = ex3['accuracy'] < .975 or any(
        row['compact_prose']['criticalUnsafe'] >= 2
        for row in docs['ex3']['analysis']['byFamily'].values()
    )
    assert ex3_deficit is False

    ex4=docs['ex4']['analysis']['byTreatment']
    ex4_tokens={k:v['providerTokens'] for k,v in ex4.items()}
    ex4_b=ex4_tokens['compact_prose']
    ex4_deltas={k:pct_delta(v,ex4_b) for k,v in ex4_tokens.items() if k!='compact_prose'}

    ex5=docs['ex5']['analysis']['byTreatment']
    ex6=docs['ex6']['analysis']['byTreatment']
    ex7=docs['ex7']['analysis']['byTreatment']
    paired={
      'ex5_seven_vs_compact_tokenDeltaPct':pct_delta(ex5['seven_question_grammar']['providerTokens'],ex5['compact_prose']['providerTokens']),
      'ex6_seven_vs_compact_tokenDeltaPct':pct_delta(ex6['seven_question_grammar']['providerTokens'],ex6['compact_prose']['providerTokens']),
      'ex7_four_vs_compact_tokenDeltaPct':pct_delta(ex7['four_question_grammar']['providerTokens'],ex7['compact_prose']['providerTokens']),
      'ex7_seven_vs_compact_tokenDeltaPct':pct_delta(ex7['seven_question_grammar']['providerTokens'],ex7['compact_prose']['providerTokens']),
      'ex7_typed_vs_compact_tokenDeltaPct':pct_delta(ex7['typed_relation_notation']['providerTokens'],ex7['compact_prose']['providerTokens']),
    }

    best_acc=max(v['accuracy'] for v in ex7.values())
    eligible={k:v for k,v in ex7.items() if v['accuracy'] >= best_acc-.01}
    selected=min(eligible.items(), key=lambda kv: kv[1]['providerTokens'])[0]
    assert selected=='compact_prose'

    payload={
      'schemaVersion':1,
      'kind':'ordivon.ex3-ex7-causal-comprehension-program-analysis',
      'preregistrationCommit':'42ed685',
      'stages':summaries,
      'formalTotals':{
        'acceptedDecisions':total_accepted,
        'exactCorrectDecisions':total_correct,
        'exactActionAccuracy':total_correct/total_accepted,
        'reportedProviderTokens':total_tokens,
        'acceptedPhysicalProviderCalls':total_accepted_calls,
        'allPhysicalProviderCalls':total_all_calls,
      },
      'validity':{
        'ex3ExplanationDeficitObserved':ex3_deficit,
        'unsafeMetricValidStages':['ex3','ex4','ex6'],
        'unsafeMetricInvalidStages':['ex5','ex7'],
        'ex5FrozenOracleUnsafeConflicts':conflicts['ex5'],
        'ex7FrozenOracleUnsafeConflicts':conflicts['ex7'],
        'ex6TransportRepair':{
          'initialRemoteDisconnectedTrials':4,
          'preRepairFailedPhysicalProviderCalls':docs['ex6']['analysis'].get('preRepairFailedPhysicalProviderCalls'),
          'repairPreservedFrozenCaseTreatmentReplicateIdentity':True,
          'semanticTrialsAfterRepair':204,
        },
      },
      'burden':{
        'ex4TokenDeltasVsCompactPct':ex4_deltas,
        **paired,
      },
      'decisions':{
        'ex3':'NO_MEASURABLE_COMPACT_PROSE_DEFICIT',
        'ex4':'CEILING_EQUIVALENT_COMPACT_LOWEST_BURDEN',
        'ex5':'INTERVENTION_CEILING_GRAMMAR_NO_ACTION_GAIN_UNSAFE_SUBMETRIC_INVALID',
        'ex6':'DEIDENTIFIED_TRANSFER_CEILING_GRAMMAR_NO_ACTION_GAIN',
        'ex7':'SELECT_COMPACT_PROSE_BY_PREREG_MINIMUM_NONINFERIOR_RULE',
        'selectedAgentFacingRepresentation':selected,
        'typedRelationsDisposition':'research_local_optional_not_mandatory',
        'questionGrammarDisposition':'optional_diagnostic_method_not_default_context',
        'serviceOrOntologyPromotion':'REJECT',
        'humanComprehensionClaim':'UNTESTED',
      },
    }
    out=ROOT/'program-analysis-v1.json'
    out.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
