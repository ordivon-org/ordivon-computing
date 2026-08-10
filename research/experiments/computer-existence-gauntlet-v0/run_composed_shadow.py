from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
FAMILIES=['harness-evaluation-v0','semantic-core-v0','observation-plane-v0','task-continuation-v0','core-work-system-v1','external-semantic-contract-v0','experiment-loop-v0','skill-compilation-v0','multi-participant-adaptation-v0','owner-pressure-discovery-v0','crosscut-maintenance-p0-v0','crosscut-maintenance-p1-v0','crosscut-maintenance-p2-v0','crosscut-maintenance-p3-v0','p0-consumer-falsification-v0']
CRITICAL_CI=['research/research-method-v1.json','research/world-model-loop-v2.json','research/computer-responsibility-map-v1.json','research/portfolio.json','scripts/check_agent_research_method.py','scripts/check_world_model_loop.py','scripts/check_computer_responsibility_map.py','research/experiments/computer-existence-gauntlet-v0/**']
def run(cmd,cwd,env=None):
 e=os.environ.copy(); e.update(env or {}); p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=e); return {'returncode':p.returncode,'stdoutTail':p.stdout[-5000:],'stderrTail':p.stderr[-5000:]}
def sha(data:bytes)->str:return 'sha256:'+hashlib.sha256(data).hexdigest()
def map_digest(doc):
 payload={k:v for k,v in doc.items() if k!='integrity'}; return sha(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def workflow_patterns(text):
 out=[]; inside=False; indent=0
 for line in text.splitlines():
  s=line.strip()
  if s=='paths:': inside=True; indent=len(line)-len(line.lstrip()); continue
  if inside:
   cur=len(line)-len(line.lstrip())
   if s.startswith('- ') and cur>indent:out.append(s[2:].strip().strip('"'))
   elif s and cur<=indent:inside=False
 return list(dict.fromkeys(out))
def match(pattern,path):
 import fnmatch
 if pattern.endswith('/**'):return path.startswith(pattern[:-2])
 return fnmatch.fnmatchcase(path,pattern)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args(); a.output.parent.mkdir(parents=True,exist_ok=True)
 source=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(); td=Path(tempfile.mkdtemp(prefix='ordivon-composed-shadow-')); repo=td/'repo'; subprocess.run(['git','clone','--shared','--no-hardlinks',str(ROOT),str(repo)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True); subprocess.run(['git','-C',str(repo),'checkout','--detach',source],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 removed=[]; recover={}
 try:
  # Record representative exact bytes before contraction.
  samples=['research/experiments/semantic-core-v0/src/anc_semantic_core/kernel.py','research/experiments/harness-evaluation-v0/run_b4_deterministic_smoke.py','research/experiments/experiment-loop-v0/frontier_freshness.py','packages/content-templates/research/experiment.md','packages/content-fixtures/valid/architecture.md','packages/ordivon-protocol/src/ordivon_semantics/state.py']
  for rel in samples: recover[rel]=sha((repo/rel).read_bytes())
  # Extract the one live utility.
  frontier=(repo/'research/experiments/experiment-loop-v0/frontier_freshness.py').read_text(); (repo/'scripts/frontier_freshness.py').write_text(frontier); f=repo/'scripts/assess_world_model_freshness.py'; s=f.read_text(); s=s.replace('EXPERIMENT = ROOT / "research/experiments/experiment-loop-v0"\nif str(EXPERIMENT) not in sys.path:\n    sys.path.insert(0, str(EXPERIMENT))\n\n',''); f.write_text(s)
  # Archive historical executable apparatus from current tree.
  for fam in FAMILIES:
   base=repo/'research/experiments'/fam
   for p in list(base.rglob('*')):
    if not p.is_file():continue
    executable=p.suffix in {'.py','.sh','.rs','.ts'} or 'tests' in p.parts or 'scripts' in p.parts or 'src' in p.parts or 'integration' in p.parts or 'fixtures' in p.parts or 'benchmarks' in p.parts
    if executable:removed.append({'path':str(p.relative_to(repo)),'bytes':p.stat().st_size,'lines':len(p.read_text(errors='ignore').splitlines())}); p.unlink()
  # Remove unearned active content helpers and zero-current-consumer semantic-state implementation.
  for rel in ('packages/content-templates','packages/content-fixtures','packages/ordivon-protocol/src/ordivon_semantics'):
   p=repo/rel
   if p.exists():
    for q in p.rglob('*'):
     if q.is_file():removed.append({'path':str(q.relative_to(repo)),'bytes':q.stat().st_size,'lines':len(q.read_text(errors='ignore').splitlines())})
    shutil.rmtree(p)
  # Research relations leave active authority; question/source inventory remains.
  p=repo/'research/map.yaml'; s=p.read_text(); start=s.index('\nrelations:\n'); end=s.index('\nquestions:\n'); removed_rel=s[start:end]; p.write_text(s[:start]+'\n# Historical relation hypotheses are recoverable from Git; current status/authority is owned by portfolio + exact evidence.\n'+s[end:])
  # Rewrite known stale status projection without creating a second authority.
  p=repo/'research/experiments/README.md'; s=p.read_text(); s=s.replace('## Current executable research','## Historical executable research'); s=s.replace('The current candidate is only','The retained candidate was only'); s=s.replace('bounded Level A–D execution program; only Level A is active','historical bounded Level A–D execution program; Level A evidence is retained'); s=s.replace('the active Track R evidence contract','the historical Track R evidence contract'); p.write_text(s)
  p=repo/'research/README.md'; p.write_text(p.read_text().replace('`ACR-C1` … `ACR-C5`','`ACR-C1` … `ACR-C6`'))
  # Remove executable evidence pointer but keep result-level evidence already present.
  p=repo/'research/computer-responsibility-map-v1.json'; d=json.loads(p.read_text()); cr=next(x for x in d['responsibilities'] if x['id']=='CR-05'); cr['evidenceRefs']=[x for x in cr['evidenceRefs'] if x!='research/experiments/harness-evaluation-v0/run_b4_deterministic_smoke.py']; d['integrity']['payloadDigest']=map_digest(d); p.write_text(json.dumps(d,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
  # Expand current CI trigger coverage. Preserve existing gate commands for this shadow; trigger repair is separately measurable.
  p=repo/'.github/workflows/deterministic-contracts.yml'; lines=p.read_text().splitlines(); out=[]; in_paths=False; added_for_block=False; path_indent=''
  for i,line in enumerate(lines):
   out.append(line); stripped=line.strip()
   if stripped=='paths:': in_paths=True; added_for_block=False; path_indent=' '*(len(line)-len(line.lstrip())+2); continue
   if in_paths:
    cur=len(line)-len(line.lstrip()); base=len(path_indent)-2
    next_boundary=bool(stripped and cur<=base and not stripped.startswith('- '))
    if next_boundary and not added_for_block:
     out[-1:-1]=[path_indent+'- "'+x+'"' for x in CRITICAL_CI]; added_for_block=True; in_paths=False
  if in_paths and not added_for_block:out.extend([path_indent+'- "'+x+'"' for x in CRITICAL_CI])
  p.write_text('\n'.join(out)+'\n')
  # Current authority/control checks that should survive contraction.
  checks={}
  for name,cmd in [('world',['python3','scripts/check_world_model_loop.py']),('method',['python3','scripts/check_agent_research_method.py']),('responsibility',['python3','scripts/check_computer_responsibility_map.py']),('portfolio',['python3','scripts/check_research_portfolio.py']),('render',['python3','scripts/render_research_portfolio.py','--check']),('compression',['python3','scripts/check_historical_research_compression.py']),('foundational',['python3','scripts/check_foundational_docs.py']),('freshness',['python3','scripts/assess_world_model_freshness.py']),('contentTests',['python3','-m','unittest','discover','-s','packages/content-cli/tests','-q']),('gauntlet',['python3','-m','unittest','discover','-s','research/experiments/computer-existence-gauntlet-v0/tests','-q'])]:checks[name]=run(cmd,repo,{'PYTHONPATH':'packages/content-cli/src'} if name=='contentTests' else None)
  checks['protocolHostWorkload']=run(['/usr/bin/uv','run','--python','3.12','--with','jsonschema==4.25.1','python','-m','unittest','tests.test_host_workload','tests.test_schema_conformance','-q'],repo/'packages/ordivon-protocol',{'PYTHONPATH':'src'})
  # Current owner-native consumers under contracted shared protocol.
  host='/root/projects/ordivon-host'; harness='/root/projects/ordivon-harness'; game='/root/projects/ordivon-game'; ps=repo/'packages/ordivon-protocol/src'
  hostmods=['tests.test_context_provenance','tests.test_a_series_remediation','tests.test_external_executor','tests.test_code_change','tests.test_mcp_server','tests.test_runtime_catalog','tests.test_open_proposal','tests.test_host_workload_contracts','tests.test_boundaries','tests.test_storage','tests.test_goal_coordination','tests.test_cognition_context']
  checks['hostConsumers']=run([host+'/.venv/bin/python','-m','unittest',*hostmods,'-q'],Path(host),{'PYTHONPATH':f'{ps}:{host}/src:{host}'})
  harness_files=subprocess.check_output(['rg','-l','anc_canonical|anc_tool_contract|ordivon_protocol',harness+'/tests'],text=True).splitlines(); harnessmods=[Path(x).relative_to(harness).with_suffix('').as_posix().replace('/','.') for x in harness_files]
  checks['harnessConsumers']=run([harness+'/.venv/bin/python','-m','unittest',*harnessmods,'-q'],Path(harness),{'PYTHONPATH':f'{ps}:{harness}/src:{harness}'})
  checks['gameConsumers']=run(['node','--test','test/host-contract-store.test.ts','test/host-contract-vectors.test.ts'],Path(game))
  # Independent mixed invariants.
  sysenv=os.environ.copy(); sysenv['PYTHONPATH']=str(ps); mixed_code="""import json,sys\nfrom pathlib import Path\nfrom anc_effect_binding import BindingDecision,assess_binding\nfrom anc_tool_contract import ContractChange\nassert assess_binding('unknown',ContractChange.SEMANTIC_BREAK) is BindingDecision.OBSERVE_ORIGINAL\nassert assess_binding('pending',ContractChange.CAPABILITY_CHANGE) is BindingDecision.FAIL_CLOSED\np=json.load(open('research/portfolio.json')); assert not any(q['status'] in ('active','ready') for q in p['questions'])\nm=json.load(open('research/computer-responsibility-map-v1.json')); assert m['reformDisposition']=='stopped_waiting_for_new_owner_pressure'\ne=Path('research/experiments/README.md').read_text(); assert '## Current executable research' not in e and 'only Level A is active' not in e and 'the active Track R' not in e\nassert 'relations:' not in Path('research/map.yaml').read_text()\nprint('mixed invariants ok')\n"""; checks['mixedInvariants']=run(['python3','-c',mixed_code],repo,{'PYTHONPATH':str(ps)})
  # CI coverage oracle.
  pats=workflow_patterns((repo/'.github/workflows/deterministic-contracts.yml').read_text()); untriggered=[x for x in CRITICAL_CI if not any(match(pt,x.replace('/**','/probe')) for pt in pats)]; ci={'patterns':pats,'untriggered':untriggered,'ok':not untriggered}
  # Git history retains exact removed bytes.
  recovery=[]
  for rel,dig in recover.items():
   got=subprocess.check_output(['git','-C',str(repo),'show',f'{source}:{rel}']); recovery.append({'path':rel,'expectedDigest':dig,'gitDigest':sha(got),'ok':sha(got)==dig})
  summary={'sourceRevision':source,'removedFiles':len(removed),'removedBytes':sum(x['bytes'] for x in removed),'removedLines':sum(x['lines'] for x in removed),'removedRelationLines':len(removed_rel.splitlines()),'extractedFreshnessLines':len(frontier.splitlines()),'checks':{k:v['returncode'] for k,v in checks.items()},'ci':ci,'historyRecovery':recovery,'allChecksPassed':all(v['returncode']==0 for v in checks.values()),'allRecoveryPassed':all(x['ok'] for x in recovery)}
  result={'schemaVersion':1,'kind':'ordivon.computer-composed-contraction-shadow','summary':summary,'failures':{k:v for k,v in checks.items() if v['returncode']!=0},'claimBoundary':'This is an isolated shadow contraction. It does not mutate owner repositories or authorize cross-owner localization.'}; a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'); print(json.dumps(summary,indent=2,ensure_ascii=False)); return 0 if summary['allChecksPassed'] and summary['allRecoveryPassed'] and ci['ok'] else 2
 finally:shutil.rmtree(td,ignore_errors=True)
if __name__=='__main__':raise SystemExit(main())
