from __future__ import annotations
import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPOS={k:Path('/root/projects')/('ordivon-'+k) for k in ('harness','runtime','world','game','host','security','finance','studio','web','human')}
SPECS=[
 {'cardId':'harness-rsi-p3','split':'development','owner':'harness','revision':'9032d0f3784317fa2cbab1da399bb0720c2d8d43','title':'evidence: record Harness RSI P3 recursive improvement','files':['evidence/harness-rsi-p3-recursive-improvement-aea4ec1.json']},
 {'cardId':'runtime-self-release','split':'development','owner':'runtime','revision':'053adf74de851ad569963d7826b29599ebfc468b','title':'runtime: add structured self-release effect','files':['docs/status.md']},
 {'cardId':'world-hp0-hp4','split':'development','owner':'world','revision':'b60a3e830fb5e1561e1a48cc13365d7bd5514e14','title':'world: pressure-test hp0-hp4 surfaces','files':['docs/high-pressure-survival-hp0-hp4.md']},
 {'cardId':'game-action-binding','split':'development','owner':'game','revision':'9610d166fc9fa3601b34c34706b6c36e8148e59e','title':'game: bind agent actions to exact subject and cognition','files':['evidence/acceptance/station-zero-v3-agent-action-admission-8d89410.json']},
 {'cardId':'host-client-disconnect','split':'development','owner':'host','revision':'6495822162c69179e8ad4f8a0d79cc42902ff599','title':'mcp: swallow ClientDisconnect behind the public tunnel','files':['src/ordivon_host/mcp_server.py']},
 {'cardId':'security-ruff-ci','split':'development','owner':'security','revision':'f109cb8cc548479e852c8a4dbc914bd7d3e22ce0','title':'fix: declare ruff in dev dependency group for CI lint step','files':['pyproject.toml']},
 {'cardId':'finance-contained-research','split':'holdout','owner':'finance','revision':'5b625bd116c7c5cb5a9ed376eba8777cd88bb834','title':'finance: provision contained research runner','files':['design/LABORATORY-GRADUATION.md']},
 {'cardId':'studio-off-machine-blob','split':'holdout','owner':'studio','revision':'dcd038665bfa59e77a561524f36c68270f0005fb','title':'feat(studio): prove off-machine blob recovery','files':['docs/storage-layout.md']},
 {'cardId':'web-project-directory','split':'holdout','owner':'web','revision':'4f9503b8089a8301ceba773be9ed68372221b320','title':'fix(web): expose projects in directory entry','files':['app/projects/page.tsx','design/expression-profile.md']},
 {'cardId':'human-family-link','split':'holdout','owner':'human','revision':'8d55d31062d0e85e5b306ca94ea0165ebec314f7','title':'docs: link Human into project family','files':['README.md']},
]
def show(repo:Path,rev:str,path:str)->str:
 return subprocess.run(['git','-C',str(repo),'show',f'{rev}:{path}'],check=True,capture_output=True,text=True).stdout
def digest(text:str)->str:return 'sha256:'+hashlib.sha256(text.encode()).hexdigest()
def bounded(card:str,path:str,text:str)->str:
 # Preserve the most decision-relevant exact owner statements while bounding model context.
 if card=='runtime-self-release':
  lines=[x for x in text.splitlines() if 'release.apply' in x or 'release.get' in x or 'arbitrary command execution remains effect-opaque' in x or 'semantic Task completion' in x]
  return '\n'.join(lines)[:10000]
 if card=='finance-contained-research':
  keys=('Trusted instrument / Agent program separation','Replay-before-world invariant','does not make a generic command DSL','A canonical `ExperimentResult`','ProgramBundle','same Python process','process-isolated provenance','research.run')
  lines=text.splitlines(); out=[]
  for i,line in enumerate(lines):
   if any(k.lower() in line.lower() for k in keys): out.extend(lines[max(0,i-3):min(len(lines),i+18)])
  return '\n'.join(dict.fromkeys(out))[:12000]
 return text[:12000]
cards=[]
for spec in SPECS:
 repo=REPOS[spec['owner']]
 observed=subprocess.run(['git','-C',str(repo),'cat-file','-e',spec['revision']+'^{commit}']).returncode
 if observed: raise RuntimeError('unreachable '+spec['cardId'])
 chunks=[]; refs=[]
 for path in spec['files']:
  raw=show(repo,spec['revision'],path); excerpt=bounded(spec['cardId'],path,raw); chunks.append(f'FILE {path}\n{excerpt}'); refs.append({'path':path,'fullDigest':digest(raw),'excerptDigest':digest(excerpt)})
 stat=subprocess.run(['git','-C',str(repo),'show','--stat','--oneline','--format=%H%n%s',spec['revision']],check=True,capture_output=True,text=True).stdout[:5000]
 evidence='\n\n'.join(chunks)
 # Bound the complete card, not merely each source file, so one multi-file churn card cannot dominate the strong baseline Context.
 complete_limit=12000
 evidence=evidence[:complete_limit]
 cards.append({**spec,'repositoryId':'ordivon-'+spec['owner'],'changedSummary':stat,'evidence':evidence,'evidenceDigest':digest(evidence),'sourceRefs':refs,'evidenceTruncated':len('\n\n'.join(chunks))>complete_limit})
out={'schemaVersion':1,'kind':'ordivon.owner-pressure-cards','cards':cards}
(HERE/'fixtures/cards.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
print(json.dumps({'cards':len(cards),'development':sum(c['split']=='development' for c in cards),'holdout':sum(c['split']=='holdout' for c in cards)},sort_keys=True))
