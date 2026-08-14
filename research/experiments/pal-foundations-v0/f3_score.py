from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'f3-cases-v0.json').read_text()); cases=d['cases']
absmap=d['featureScales']['abstraction']; simmap=d['featureScales']['domainSimilarity']
def p_abs(c): return absmap[c['features']['abstraction']]
def p_sim(c): return simmap[c['features']['domainSimilarity']]
def p_det(c): return c['features']['deterministicActionSpecificity']
def credit_score(c):
    f=c['features']
    return f['localIntermediateObservability']+f['evaluatorAlignment']+f['shortCausalCreditPath']+f['mechanisticRepresentation']+f['exactEscapeHatch']-f['modelInterpretationBoundary']
def p_credit(c):
    s=credit_score(c)
    return 2 if s>=8 else (1 if s>=4 else 0)
models={'T0_ABSTRACTION':p_abs,'T1_DOMAIN_SIMILARITY':p_sim,'T2_DETERMINISM':p_det,'T_CREDIT':p_credit}
rows=[]
for c in cases:
    preds={k:f(c) for k,f in models.items()}
    rows.append({'id':c['id'],'split':c['split'],'outcome':c['outcome'],'creditScore':credit_score(c),'predictions':preds,'absoluteError':{k:abs(v-c['outcome']) for k,v in preds.items()}})
def s(split=None):
    rs=[r for r in rows if split is None or r['split']==split]
    return {k:{'exact':sum(r['predictions'][k]==r['outcome'] for r in rs),'total':len(rs),'mae':sum(r['absoluteError'][k] for r in rs)/len(rs)} for k in models}
out={'schemaVersion':1,'kind':'ordivon.computing.pal-f3-transfer-court','status':'completed','development':s('development'),'holdout':s('holdout'),'all':s(),'rows':rows,'residuals':{k:[r['id'] for r in rows if r['predictions'][k]!=r['outcome']] for k in models},'claimBoundary':'Retrospective/held-out case court over existing exact outcomes. T_CREDIT is not a law until prospective transfer evidence; meta-selection residuals are intentionally preserved.'}
(ROOT/'f3-results-v0.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print(json.dumps({'development':out['development'],'holdout':out['holdout'],'all':out['all'],'residuals':out['residuals']},ensure_ascii=False,indent=2))
