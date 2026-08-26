from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'prefrozen-targets-v1.json').read_text())
packet=json.loads((ROOT/'owner-source-packet-v2.json').read_text())
rows={x['ownerId']:x for x in packet['owners']}
for t in src['targets']:
    if t['ownerId']=='ordivon-game':
        t['quEnglish']='Which follow-on interactive scenarios count as shipped product stages versus current internal research lines?'
    elif t['ownerId']=='ordivon-human':
        t['sourceAnchorQuote']='answer remains the three-engine, four-rail framework in\n[`research/economy/README.md`](research/economy/README.md).'
    elif t['ownerId']=='ordivon-interlocus':
        t['quChinese']='一个研究领域描述跨位置的能力与组合语义，那么它是否真的定义那些底层的数据包、主机、网络地址之类的具体网络内容，还是那只是它的一个具体应用方面？'
problems=[]
latin=re.compile(r'[A-Za-z]')
for t in src['targets']:
    row=rows[t['ownerId']]
    ss=next((s for s in row['sources'] if s['path']==t['sourcePath']),None)
    if ss is None or t['sourceAnchorQuote'] not in ss['text']:
        problems.append(f"{t['ownerId']}: anchor quote not exact")
    unknown=(t['quEnglish']+' '+t['quChinese']).lower()
    if 'ordivon' in unknown or t['ownerId'].lower() in unknown:
        problems.append(f"{t['ownerId']}: unknown query leaks Ordivon/project id")
    if latin.search(t['quChinese']):
        problems.append(f"{t['ownerId']}: Chinese query contains Latin alphabetic text")
out={
 'schemaVersion':2,
 'kind':'ordivon.computing.discoverability-prefrozen-targets',
 'truthRole':src['truthRole'],
 'generatedBeforeAtlasRetrieval':True,
 'sourcePacketDigest':src['sourcePacketDigest'],
 'targets':src['targets'],
 'validationProblems':problems,
 'apparatusRepair':{
   'from':'prefrozen-targets-v1.json',
   'beforeAnyAtlasRetrieval':True,
   'changes':['game QU-E removed generic domain token falsely caught by the original overbroad owner-name validator','Human anchor repaired to an exact contiguous source substring across the actual line break','Interlocus QU-ZH replaced Latin IP with Chinese network-address wording'],
   'semanticTargetChanged':False
 },
 'batches':src['batches'],
 'nonClaims':src['nonClaims']
}
(ROOT/'prefrozen-targets-v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print({'targets':len(out['targets']),'validationProblems':problems})
if problems: raise SystemExit(2)
