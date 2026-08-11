from __future__ import annotations
import importlib.util,json,os,pathlib,sys
BASE=pathlib.Path('/tmp/ordivon-p8-p9-transfer/p9-finance/trial.py')
spec=importlib.util.spec_from_file_location('p9finance',BASE); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
ORDERS={
'canonical':['holdability','wrapper_screen','instruments','funding_settlements','swap_daily_bars','index_daily_bars'],
'reverse':['index_daily_bars','swap_daily_bars','funding_settlements','instruments','wrapper_screen','holdability'],
'bars_first':['swap_daily_bars','index_daily_bars','funding_settlements','holdability','instruments','wrapper_screen'],
'identity_first':['instruments','wrapper_screen','holdability','funding_settlements','index_daily_bars','swap_daily_bars'],
'funding_first':['funding_settlements','holdability','wrapper_screen','instruments','swap_daily_bars','index_daily_bars'],
'interleaved':['wrapper_screen','swap_daily_bars','holdability','index_daily_bars','instruments','funding_settlements'],
}
def main():
 name=sys.argv[1]; rep=int(os.environ.get('ORDIVON_REPLICATE','1')); secret=b.sec(rep); order=ORDERS[name]
 obs=[{'dataset':ds,'output':b.inspect(ds)} for ds in order]
 final,usage,diag=b.synth(obs,secret)
 print(json.dumps({'schemaVersion':1,'kind':'ordivon.computing.p9-finance-order-trial','order':name,'replicate':rep,'datasetSequence':order,'final':final,'metrics':b.score(final),'protocolDiagnostics':diag,'usage':usage},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
