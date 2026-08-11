from __future__ import annotations
import importlib.util,json,os,pathlib
V3_PATH=pathlib.Path('/tmp/ordivon-rsi-lab-p4-p9/p9v3/trial.py')
spec=importlib.util.spec_from_file_location('p9v3',V3_PATH); v3=importlib.util.module_from_spec(spec); spec.loader.exec_module(v3); b=v3.b
def main():
 rep=int(os.environ.get('ORDIVON_REPLICATE','1')); sec=b.secret(rep); final,u,diag=v3.synth([],sec)
 print(json.dumps({'schemaVersion':1,'kind':'ordivon.computing.p9-v7-zero-observation-trial','replicate':rep,'observationCount':0,'final':final,'protocolDiagnostics':diag,'metrics':b.score(final),'usage':u},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
