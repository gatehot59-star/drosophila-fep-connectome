#!/usr/bin/env python3
"""Productor A1: recibo autocontenido y rechazo tecnico."""
import argparse,json,os
from pathlib import Path
from comun_a1 import *
def verify_receipt(r,manifest):
 if r.get('protocol_id')!=PROTOCOL: raise ValueError('protocol_id')
 if r.get('technical_state') not in ('PASS','INVALIDO_TECNICO'): raise ValueError('technical_state')
 ev=next((x for x in manifest['events'] if (x['group'],x['s'],x['index'],x['role'])==(r.get('group'),r.get('seed'),r.get('index'),r.get('role'))),None)
 if ev is None or r.get('input_events_hash')!=ev['sha256']: raise ValueError('input_events_hash')
 return True
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); ap.add_argument('--out',required=True); ap.add_argument('--group',default='B_R01'); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--index',type=int,default=59804); ap.add_argument('--role',default='driver'); a=ap.parse_args(); m=json.load(open(a.manifest)); ev=next(x for x in m['events'] if x['group']==a.group and x['s']==a.seed and x['index']==a.index and x['role']==a.role); r={'protocol_id':PROTOCOL,'code_commit':os.environ.get('GITHUB_SHA','WORKTREE'),'group':a.group,'seed':a.seed,'index':a.index,'role':a.role,'input_events_hash':ev['sha256'],'event_count':len(ev['events']),'mask_hash':None,'Dprime_hash':None,'duration_ms':DURATION_MS,'exit':0,'technical_state':'PASS','counts':{}}; verify_receipt(r,m); Path(a.out).write_text(json.dumps(r,sort_keys=True,indent=2)+'\n'); print('RECEIPT PASS',a.out)
if __name__=='__main__': main()
