#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fd4runner', ROOT/'run_preflight.py')
mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod)
d=json.loads((ROOT/'evidence/preflight-v1.json').read_text())
failures=d['failures']
if failures != [{'taskId':'FD0-COMP-01','arm':'baseline','replicate':2,'type':'IncompleteRead','message':'IncompleteRead(2094 bytes read)'}]:
    raise SystemExit(f'unexpected failure set: {failures!r}')
task=next(t for t in mod.CONTRACT['tasks'] if t['id']=='FD0-COMP-01')
creds=mod.secrets(); original_index=37
row=mod.trial((original_index,task,'baseline',2,creds[original_index%len(creds)]))
rows=d['trials']+[row]
rows.sort(key=lambda r:(r['taskId'],r['arm'],r['replicate']))
summary={
 'acceptedTrials':len(rows),'failures':0,'byTask':{},
 'totalSubjectTokens':sum(r['subjectUsage']['totalTokens'] for r in rows),
 'totalJudgeTokens':sum(r['judgeUsage']['totalTokens'] for r in rows),
 'physicalProviderCallsAccepted':sum(r['subjectUsage']['providerCalls']+r['judgeUsage']['providerCalls'] for r in rows),
 'failedPhysicalProviderCallsLowerBound':1,
}
for tid in sorted({r['taskId'] for r in rows}):
    summary['byTask'][tid]={}
    for arm in ('baseline','treatment'):
        rs=[r for r in rows if r['taskId']==tid and r['arm']==arm]
        correct=sum(bool(r['score']['decisionCorrect']) for r in rs)
        summary['byTask'][tid][arm]={
          'trials':len(rs),'correct':correct,'majorityCorrect':correct>=2,
          'criticalOverinference':sum(int(r['score']['criticalOverinferenceCount']) for r in rs),
          'unsupportedAuthorityClaims':sum(int(r['score']['unsupportedAuthorityClaimCount']) for r in rs),
          'requiredPointsCoveredTotal':sum(int(r['score']['requiredPointsCovered']) for r in rs),
          'inputDocumentBytes':rs[0]['inputDocumentBytes'] if rs else None,
          'providerTokens':sum(r['subjectUsage']['totalTokens']+r['judgeUsage']['totalTokens'] for r in rs),
        }
blockers=[]
for tid,v in summary['byTask'].items():
    b=v['baseline']; t=v['treatment']
    if b['majorityCorrect'] and not t['majorityCorrect']:
        blockers.append({'taskId':tid,'reason':'baseline-correct_to_treatment-wrong'})
    if t['criticalOverinference']>b['criticalOverinference']:
        blockers.append({'taskId':tid,'reason':'new-treatment-critical-overinference'})
summary['publicationBlockers']=blockers
summary['admissible']=not blockers and len(rows)==mod.CONTRACT['expectedSubjectCalls']
out={
 'schemaVersion':1,'kind':'ordivon.feynman-documentation.second-wave-preflight-evidence',
 'contractDigest':mod.digest((ROOT/'contract-v1.json').read_bytes()),
 'initialEvidence':'evidence/preflight-v1-initial.json',
 'repair':{'taskId':'FD0-COMP-01','arm':'baseline','replicate':2,'reason':'initial HTTP IncompleteRead after one physical call; replayed only the missing frozen trial','originalIndex':37},
 'trials':rows,'failures':[],'summary':summary,
}
(ROOT/'evidence/preflight-v1.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
if not summary['admissible']: raise SystemExit(3)
