from __future__ import annotations
import argparse, fnmatch, hashlib, json, shutil, subprocess, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def digest(doc:dict)->str:
 payload={k:v for k,v in doc.items() if k!='integrity'}
 data=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
 return 'sha256:'+hashlib.sha256(data).hexdigest()
def write_integrity(path:Path,doc:dict)->None:
 if 'integrity' not in doc: raise ValueError(f'{path} has no integrity block')
 doc['integrity']['payloadDigest']=digest(doc)
 path.write_text(json.dumps(doc,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
def run(repo:Path,cmd:list[str])->dict:
 r=subprocess.run(cmd,cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return {'returncode':r.returncode,'stdout':r.stdout[-12000:],'stderr':r.stderr[-12000:]}
def clone_base()->Path:
 tmp=Path(tempfile.mkdtemp(prefix='ordivon-control-mutant-')); repo=tmp/'repo'
 subprocess.run(['git','clone','--shared','--no-hardlinks',str(ROOT),str(repo)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 subprocess.run(['git','-C',str(repo),'checkout','--detach','HEAD'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 return repo
def mutate_portfolio_binding(repo:Path)->None:
 p=repo/'research/portfolio.json'; d=json.loads(p.read_text()); q=next(x for x in d['questions'] if x['id']=='ANC-MULTI-001'); q['nextAction'] += ' [MUTANT stale binding]'; p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def mutate_wml_authority(repo:Path)->None:
 p=repo/'research/world-model-loop-v2.json'; d=json.loads(p.read_text()); d['purpose']='Automatically treat every owner revision movement as a shared world-model revision and propagate it as current truth.'; d['revisionRules']=[x for x in d['revisionRules'] if x!='owner_revision_movement_creates_review_pressure_not_shared_world_model_change']; d['revisionRules'].append('owner_revision_movement_automatically_changes_shared_world_model'); write_integrity(p,d)
def mutate_research_method_authority(repo:Path)->None:
 p=repo/'research/research-method-v1.json'; d=json.loads(p.read_text()); d['purpose']='Research scores automatically own product merge, deployment, domain truth, and irreversible promotion authority without owner admission.'; write_integrity(p,d)
def mutate_responsibility_retention(repo:Path)->None:
 p=repo/'research/computer-responsibility-map-v1.json'; d=json.loads(p.read_text()); d['decisionRule']='Retain every existing Computer structure by default because prior implementation effort and test count establish its authority to continue.'; write_integrity(p,d)
def mutate_portfolio_judgment(repo:Path)->None:
 p=repo/'research/portfolio.json'; d=json.loads(p.read_text()); d['policy']['judgmentRule']='A single mechanical score owns priority, deletion, exception, and promotion decisions for every participant and product.'; p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def mutate_map_self_dependency(repo:Path)->None:
 p=repo/'research/map.yaml'; s=p.read_text(); old='  - from: ANC-COMPILER-002\n    type: enables\n    to: ANC-MULTI-001\n    meaning: A validated single-Actor temporal cognitive state is the prerequisite for testing whether bounded Child Runs and explicit joins outperform single-Agent work.\n'; new='  - from: ANC-COMPILER-002\n    type: enables\n    to: ANC-COMPILER-002\n    meaning: This question is a mandatory prerequisite for itself and therefore cannot be falsified without first being accepted.\n';
 if old not in s: raise RuntimeError('expected map relation missing')
 p.write_text(s.replace(old,new))
def workflow_patterns(text:str)->list[str]:
 patterns=[]; in_paths=False; indent=0
 for line in text.splitlines():
  stripped=line.strip()
  if stripped=='paths:': in_paths=True; indent=len(line)-len(line.lstrip()); continue
  if in_paths:
   current=len(line)-len(line.lstrip())
   if stripped.startswith('- ') and current>indent: patterns.append(stripped[2:].strip().strip('"'))
   elif stripped and current<=indent: in_paths=False
 return list(dict.fromkeys(patterns))
def path_matches(pattern:str,path:str)->bool:
 if pattern.endswith('/**'): return path==pattern[:-3] or path.startswith(pattern[:-2])
 return fnmatch.fnmatchcase(path,pattern)
def current_state_faults(repo:Path)->list[dict]:
 portfolio=json.loads((repo/'research/portfolio.json').read_text()); active=sum(q['status']=='active' for q in portfolio['questions']); ready=sum(q['status']=='ready' for q in portfolio['questions']); exp=(repo/'research/experiments/README.md').read_text(); rr=(repo/'research/README.md').read_text(); maptext=(repo/'research/map.yaml').read_text(); workflow=(repo/'.github/workflows/deterministic-contracts.yml').read_text(); patterns=workflow_patterns(workflow)
 critical=['research/research-method-v1.json','research/world-model-loop-v2.json','research/computer-responsibility-map-v1.json','scripts/check_agent_research_method.py','scripts/check_world_model_loop.py','scripts/check_computer_responsibility_map.py','research/experiments/owner-pressure-discovery-v0/README.md','research/experiments/crosscut-maintenance-p3-v0/README.md']
 return [{'faultId':'CTRL-F01','oracleViolated':active==0 and ready==0 and ('only Level A is active' in exp or 'active Track R' in exp),'details':{'active':active,'ready':ready}},{'faultId':'CTRL-F02','oracleViolated':'ACR-C1` … `ACR-C5' in rr and '"step": "C6"' in (repo/'research/computer-responsibility-map-v1.json').read_text()},{'faultId':'CTRL-F03','oracleViolated':'A validated single-Actor temporal cognitive state is the prerequisite for testing whether bounded Child Runs' in maptext and next(q for q in portfolio['questions'] if q['id']=='ANC-MULTI-001')['maturity']=='M4'},{'faultId':'CTRL-F04','oracleViolated':True,'untriggered':[p for p in critical if not any(path_matches(pt,p) for pt in patterns)],'patterns':patterns}]
def main()->int:
 parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args(); args.output.parent.mkdir(parents=True,exist_ok=True)
 cases=[('M01-portfolio-binding-positive-control',mutate_portfolio_binding,['python3','scripts/check_computer_responsibility_map.py'],'must_kill'),('M02-wml-authority-inversion',mutate_wml_authority,['python3','scripts/check_world_model_loop.py'],'must_kill'),('M03-research-method-product-authority',mutate_research_method_authority,['python3','scripts/check_agent_research_method.py'],'must_kill'),('M04-responsibility-retention-inversion',mutate_responsibility_retention,['python3','scripts/check_computer_responsibility_map.py'],'must_kill'),('M05-portfolio-mechanical-judgment',mutate_portfolio_judgment,['python3','scripts/check_research_portfolio.py'],'must_kill'),('M06-map-self-dependency',mutate_map_self_dependency,['python3','scripts/check_research_portfolio.py'],'must_kill')]
 rows=[]
 for cid,mutation,checker,expectation in cases:
  repo=clone_base()
  try:
   mutation(repo); result=run(repo,checker); rows.append({'caseId':cid,'checker':' '.join(checker),'expectation':expectation,'mutantKilled':result['returncode']!=0,'result':result})
  finally: shutil.rmtree(repo.parent,ignore_errors=True)
 baseline_repo=clone_base()
 try:
  baseline_checks={name:run(baseline_repo,['python3',path]) for name,path in [('foundational','scripts/check_foundational_docs.py'),('worldModel','scripts/check_world_model_loop.py'),('researchMethod','scripts/check_agent_research_method.py'),('responsibility','scripts/check_computer_responsibility_map.py'),('portfolio','scripts/check_research_portfolio.py')]}; faults=current_state_faults(baseline_repo)
 finally: shutil.rmtree(baseline_repo.parent,ignore_errors=True)
 killed=sum(r['mutantKilled'] for r in rows); semantic=[r for r in rows if not r['caseId'].startswith('M01')]; out={'schemaVersion':1,'kind':'ordivon.computer-control-plane-mutation-gauntlet','sourceRevision':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'baselineChecks':baseline_checks,'currentStateFaults':faults,'mutants':rows,'summary':{'totalMutants':len(rows),'killed':killed,'killRate':killed/len(rows),'positiveControlKilled':rows[0]['mutantKilled'],'semanticMutants':len(semantic),'semanticKilled':sum(r['mutantKilled'] for r in semantic),'semanticKillRate':sum(r['mutantKilled'] for r in semantic)/len(semantic)},'claimBoundary':'A surviving mutant proves only that the named checker does not enforce that independent oracle relation; it does not prove the artifact is wholly useless.'}; args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+'\n'); print(json.dumps(out['summary'],sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
