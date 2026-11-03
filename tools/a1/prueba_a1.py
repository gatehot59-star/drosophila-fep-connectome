#!/usr/bin/env python3
import hashlib,sys
import numpy as np
from comun_a1 import *
def check(name,ok): print(('PASS ' if ok else 'FAIL ')+name); return ok
def main():
 ok=True; _,s=seed_for('B_R01',0,59804,'driver'); ok&=check('seed_64bit',s==5428794271745577241 and s>2**32); e=bernoulli_events(s,50); ok&=check('events_known_answer',e.size==55 and e[:6].tolist()==[58,419,473,835,989,1158]); _,s=seed_for('C_H2',0,19257,'replay'); r=replay_ticks(s); ok&=check('replay_unique',len(r)==50 and len(set(r.tolist()))==50 and r[:6].tolist()==[104,155,212,672,913,968]); ok&=check('empty_mask',mask_hash([])==hashlib.sha256(np.array([],dtype='<i8').tobytes()).hexdigest()); ok&=check('paired_input',np.array_equal(e,bernoulli_events(5428794271745577241,50))); print('A1_FIXTURES','PASS' if ok else 'FAIL'); return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
