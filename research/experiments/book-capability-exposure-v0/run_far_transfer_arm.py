from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--arm',required=True);ap.add_argument('--count',type=int,default=3);a=ap.parse_args();rows=[]
for r in range(1,a.count+1):
    cp=subprocess.run([sys.executable,str(ROOT/'run_far_transfer.py'),'--arm',a.arm,'--replicate',str(r)],text=True,capture_output=True)
    if cp.returncode!=0:
        print(cp.stderr,file=sys.stderr);raise SystemExit(cp.returncode)
    row=json.loads(cp.stdout.strip().splitlines()[-1]);rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
(ROOT/f'far-transfer-{a.arm.lower()}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
