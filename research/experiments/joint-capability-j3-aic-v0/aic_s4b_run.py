from __future__ import annotations

import argparse, importlib.util, json, random, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError(path)
    mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod); return mod

s2run=load('aic_s2run_s4b',ROOT/'aic_s2_run.py')

ARMS=['RAW_HISTORY','RAW_PLUS_ORTHOGONAL_FRONTIER']
TREAT={'RAW_HISTORY':'RAW_HISTORY','RAW_PLUS_ORTHOGONAL_FRONTIER':'ORTHOGONAL_FRONTIER_V2'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--models',default='deepseek-v4-flash,deepseek-v4-pro'); ap.add_argument('--replicates',type=int,default=2); ap.add_argument('--pairs',default='all'); ap.add_argument('--arms',default=','.join(ARMS)); ap.add_argument('--seed',type=int,default=202608257); ap.add_argument('--secret',default='/root/.config/ordivon/secrets/deepseek.json'); args=ap.parse_args()
    data=json.loads((ROOT/'cases-s4b-v1.json').read_text()); pairs={p['pairId']:p for p in data['pairs']}; pair_ids=list(pairs) if args.pairs=='all' else [x for x in args.pairs.split(',') if x]; models=[x for x in args.models.split(',') if x]; arms=[x for x in args.arms.split(',') if x]
    schedule=[(pid,side,arm,model,rep) for pid in pair_ids for side in ('L','R') for arm in arms for model in models for rep in range(1,args.replicates+1)]; random.Random(args.seed).shuffle(schedule)
    rows=[]; out=Path(args.output); secret=Path(args.secret)
    for i,(pid,side,arm,model,rep) in enumerate(schedule,1):
        scenario=pairs[pid]['left' if side=='L' else 'right']
        try:
            row=s2run.run_one(scenario,TREAT[arm],model,rep,secret)
        except Exception as e:
            row={'scenarioId':scenario['scenarioId'],'treatment':TREAT[arm],'model':model,'replicate':rep,'valid':False,'result':None,'stopCode':'exception','errorType':type(e).__name__,'error':str(e)[:1500],'evaluation':{'strictAccepted':False,'responsesCorrect':False,'consequentialAuthorityCorrect':False,'authorityStandingCorrect':False,'safetyError':False,'gates':{}}}
        row['pairId']=pid; row['side']=side; row['relation']=pairs[pid]['relation']; row['arm']=arm
        rows.append(row)
        payload={'schemaVersion':1,'kind':'ordivon.computing.aic-s4b-campaign','experimentId':'COJC-J3-AIC-METAMORPHIC-S4B','casesDigest':data.get('casesDigest'),'scheduleSeed':args.seed,'plannedTrials':len(schedule),'completedTrials':len(rows),'rows':rows}
        out.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'i':i,'total':len(schedule),'pairId':pid,'side':side,'arm':arm,'model':model,'replicate':rep,'valid':row.get('valid'),'responsesCorrect':row.get('evaluation',{}).get('responsesCorrect'),'strict':row.get('evaluation',{}).get('strictAccepted'),'safetyError':row.get('evaluation',{}).get('safetyError'),'error':row.get('error')},ensure_ascii=False),flush=True)
if __name__=='__main__': main()
