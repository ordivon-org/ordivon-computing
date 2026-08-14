from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
cases=json.loads((ROOT/'f1-cases-v0.json').read_text())['cases']
classes=['retain_durable','localize_or_narrow','defer_or_contract']

def b0(c):
    return 'retain_durable' if c['coding']['implementedOrPersistent'] else 'defer_or_contract'

def b1(c):
    x=c['coding']
    if x['observedRepeatedBurden'] and x['crosscutUsefulness']:
        return 'retain_durable'
    if x['observedRepeatedBurden']:
        return 'localize_or_narrow'
    return 'defer_or_contract'

def b2(c):
    x=c['coding']
    if x['crosscutUsefulness'] and x['secondMaterialConsumer']:
        return 'retain_durable'
    if x['crosscutUsefulness']:
        return 'localize_or_narrow'
    return 'defer_or_contract'

def m_resp(c):
    x=c['coding']
    # frozen structural rule: promotion requires evidence that a stable responsibility
    # survives a simpler baseline, has a clear lowest owner, and does not create shadow authority.
    if (x['observedRepeatedBurden'] and x['strongSimplerBaselineFailed'] and
        x['futureModelRobustResponsibility'] and x['ownerBoundaryClear'] and
        not x['authorityDuplicationRisk'] and x['measurableOutcome']):
        return 'retain_durable'
    # Stable problem but insufficient shared/promotion evidence -> localize/narrow.
    if x['observedRepeatedBurden'] or x['futureModelRobustResponsibility']:
        return 'localize_or_narrow'
    return 'defer_or_contract'

models={'B0_PERSISTENCE':b0,'B1_CURRENT_BURDEN':b1,'B2_CROSSCUT_SYMMETRY':b2,'M_RESPONSIBILITY':m_resp}
rows=[]
for c in cases:
    preds={k:f(c) for k,f in models.items()}
    rows.append({'id':c['id'],'split':c['split'],'oracle':c['oracle'],'predictions':preds,'correct':{k:v==c['oracle'] for k,v in preds.items()}})

def summary(split=None):
    rs=[r for r in rows if split is None or r['split']==split]
    return {k:{'correct':sum(r['correct'][k] for r in rs),'total':len(rs),'accuracy':sum(r['correct'][k] for r in rs)/len(rs)} for k in models}

out={'schemaVersion':1,'kind':'ordivon.computing.pal-f1-historical-replay','status':'completed-retrospective-replay','caseCount':len(rows),'development':summary('development'),'holdout':summary('holdout'),'all':summary(),'rows':rows,'interpretation':{}}
# Do not auto-promote the winning model; expose its residuals for explicit review.
best=max(models,key=lambda k:out['all'][k]['accuracy'])
out['interpretation']['bestByExactDispositionAccuracy']=best
out['interpretation']['bestResiduals']=[r['id'] for r in rows if not r['correct'][best]]
out['interpretation']['claimBoundary']='Small retrospective case court. Accuracy is discrimination evidence, not causal proof; manually inspect residuals and time leakage before any PAL conclusion.'
(ROOT/'f1-results-v0.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print(json.dumps({'development':out['development'],'holdout':out['holdout'],'all':out['all'],'best':best,'residuals':out['interpretation']['bestResiduals']},ensure_ascii=False,indent=2))
