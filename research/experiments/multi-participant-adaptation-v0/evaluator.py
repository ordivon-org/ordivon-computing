from __future__ import annotations
import ast, difflib, json, subprocess, sys, tempfile
from pathlib import Path
from typing import Any
FORBIDDEN_CALLS={'open','eval','exec','compile','__import__','input','breakpoint','help','quit','exit'}
FORBIDDEN_NAMES={'__builtins__','os','sys','subprocess','socket','pathlib','shutil'}
FORBIDDEN_NODES=(ast.Import,ast.ImportFrom,ast.ClassDef,ast.AsyncFunctionDef,ast.Global,ast.Nonlocal)

def source_gate(source:str,function_name:str)->tuple[bool,str|None]:
    try: tree=ast.parse(source)
    except SyntaxError as e: return False,f'syntax:{e.msg}'
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function_name]
    if len(funcs)!=1: return False,'function-count'
    for node in ast.walk(tree):
        if isinstance(node,FORBIDDEN_NODES): return False,'forbidden-node:'+type(node).__name__
        if isinstance(node,ast.Name) and node.id in FORBIDDEN_NAMES: return False,'forbidden-name:'+node.id
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in FORBIDDEN_CALLS: return False,'forbidden-call:'+node.func.id
    return True,None

def changed_lines(original:str,candidate:str)->int:
    return sum(1 for line in difflib.ndiff(original.splitlines(),candidate.splitlines()) if line.startswith('+ ') or line.startswith('- '))

def _probe(source:str,function_name:str,cases:list[dict[str,Any]],timeout:float=4.0)->dict[str,Any]:
    safe,reason=source_gate(source,function_name)
    if not safe: return {'safe':False,'gateReason':reason,'caseResults':[],'passed':0,'total':len(cases),'allPassed':False}
    probe="""import copy,json,runpy,sys
ns=runpy.run_path(sys.argv[1]); fn=ns[sys.argv[2]]; cases=json.load(open(sys.argv[3],encoding='utf-8')); out=[]
for case in cases:
    args=copy.deepcopy(case['args']); before=copy.deepcopy(args); ok=False; observed=None
    try:
        value=fn(*args); observed={'returned':value}; ok=('expected' in case and value==case['expected'])
    except Exception as exc:
        observed={'raised':type(exc).__name__}; ok=(case.get('raises')==type(exc).__name__)
    if case.get('preserveArgs') and args!=before: ok=False; observed['mutatedArgs']=True
    out.append({'ok':ok,'observed':observed})
print(json.dumps(out,ensure_ascii=False))"""
    with tempfile.TemporaryDirectory(prefix='ordivon-p4-eval-') as td:
        p=Path(td); src=p/'candidate.py'; data=p/'cases.json'; src.write_text(source,encoding='utf-8'); data.write_text(json.dumps(cases,ensure_ascii=False),encoding='utf-8')
        try: r=subprocess.run([sys.executable,'-I','-c',probe,str(src),function_name,str(data)],capture_output=True,text=True,timeout=timeout)
        except subprocess.TimeoutExpired: return {'safe':True,'gateReason':None,'caseResults':[],'passed':0,'total':len(cases),'allPassed':False,'runtimeFailure':'timeout'}
        if r.returncode!=0: return {'safe':True,'gateReason':None,'caseResults':[],'passed':0,'total':len(cases),'allPassed':False,'runtimeFailure':(r.stderr or r.stdout)[-1000:]}
        try: results=json.loads(r.stdout)
        except Exception: return {'safe':True,'gateReason':None,'caseResults':[],'passed':0,'total':len(cases),'allPassed':False,'runtimeFailure':'invalid-probe-json'}
    passed=sum(1 for x in results if x.get('ok') is True)
    return {'safe':True,'gateReason':None,'caseResults':results,'passed':passed,'total':len(cases),'allPassed':passed==len(cases)}

def evaluate_candidate(scenario:dict[str,Any],source:str,hidden_cases:list[dict[str,Any]]|None=None)->dict[str,Any]:
    visible=_probe(source,scenario['functionName'],scenario['visibleCases'])
    result={'visible':visible,'changedLines':changed_lines(scenario['buggySource'],source)}
    if hidden_cases is not None:
        hidden=_probe(source,scenario['functionName'],hidden_cases); all_cases=_probe(source,scenario['functionName'],scenario['visibleCases']+hidden_cases)
        result['hidden']=hidden; result['authoritative']=all_cases
    return result

def join_verified(candidates:list[dict[str,Any]])->dict[str,Any]:
    accepted=[c for c in candidates if c['evaluation']['authoritative']['allPassed']]
    pool=accepted if accepted else candidates
    selected=min(pool,key=lambda c:(-c['evaluation']['authoritative']['passed'],c['evaluation']['changedLines'],c['artifactDigest']))
    return {'accepted':bool(accepted),'selectedArtifactDigest':selected['artifactDigest'],'selectedCandidateId':selected['candidateId'],'acceptedCandidateCount':len(accepted),'candidateCount':len(candidates),'bestAuthoritativePassed':selected['evaluation']['authoritative']['passed'],'authoritativeTotal':selected['evaluation']['authoritative']['total']}
