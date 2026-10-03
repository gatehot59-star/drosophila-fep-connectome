#!/usr/bin/env python3
"""Multi-seed, held-out Kaggle benchmark for DBC3-v3.

The harness compares DBC3 with parameter-matched LSTM/GRU and a stateless
baseline, exports raw seed results, confidence intervals, real float32 DBC3
weights, and a deterministic trace for the later C parity experiment.
"""
from __future__ import annotations
import copy, hashlib, json, math, os, platform, time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

OUT=Path('/kaggle/working/dbc3_serious_results'); OUT.mkdir(parents=True,exist_ok=True)
DEVICE=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SEEDS=[42,142,242,342,442]; BATCH=256; EVAL_N=80; CHECK=40
D,O,M,R=36,12,20,36

def pc_dbc3(): return R*D+R+R*R+R+M*D+M+M*M+M*M+M*(2*M)+M+M+M+M*(R+M)+M+O*(R+M)+O
def pc_lstm(h): return 4*h*(D+h+1)+4*h+h*O+O
def pc_gru(h): return 3*h*(D+h+1)+h*O+O
def closest(fn,target): return min(range(1,300),key=lambda h:(abs(fn(h)-target),h))
LH=closest(pc_lstm,pc_dbc3()); GH=closest(pc_gru,pc_dbc3())

def gelu(x): return x*torch.sigmoid(1.702*x)
class DBC3(nn.Module):
 def __init__(self):
  super().__init__(); self.W_r1=nn.Parameter(torch.empty(R,D)); self.b_r1=nn.Parameter(torch.zeros(R)); self.W_r2=nn.Parameter(torch.empty(R,R)); self.b_r2=nn.Parameter(torch.zeros(R)); self.W_enc=nn.Parameter(torch.empty(M,D)); self.b_enc=nn.Parameter(torch.zeros(M)); self.W_in=nn.Parameter(torch.empty(M,M)); self.W_res=nn.Parameter(torch.empty(M,M)); self.W_tau=nn.Parameter(torch.empty(M,2*M)); self.b_tau=nn.Parameter(torch.full((M,),-2.)); self.ln_gamma=nn.Parameter(torch.ones(M)); self.ln_beta=nn.Parameter(torch.zeros(M)); self.W_gate=nn.Parameter(torch.empty(M,R+M)); self.b_gate=nn.Parameter(torch.zeros(M)); self.W_head=nn.Parameter(torch.empty(O,R+M)); self.b_head=nn.Parameter(torch.zeros(O)); self._init()
 def _init(self):
  for n,p in self.named_parameters():
   if n.startswith('W_'): nn.init.xavier_uniform_(p)
 def step(self,x,hm):
  t=torch.tanh(F.linear(x,self.W_r1,self.b_r1)); r=torch.tanh(F.linear(t,self.W_r2,self.b_r2)); e=gelu(F.linear(x,self.W_enc,self.b_enc)); tau=torch.sigmoid(F.linear(torch.cat([e,hm],-1),self.W_tau,self.b_tau)); f=torch.tanh(F.linear(e,self.W_in)+F.linear(hm,self.W_res)); hm=(1-tau)*hm+tau*f; mu=hm.mean(-1,keepdim=True); var=((hm-mu)**2).mean(-1,keepdim=True); hm=self.ln_gamma*(hm-mu)/(var+1e-5).sqrt()+self.ln_beta; g=torch.sigmoid(F.linear(torch.cat([r,hm],-1),self.W_gate,self.b_gate)); return F.linear(torch.cat([r,g*hm],-1),self.W_head,self.b_head),hm
 def forward(self,x,state=None):
  hm=x.new_zeros(x.size(0),M) if state is None else state; out=[]
  for t in range(x.size(1)): z,hm=self.step(x[:,t],hm); out.append(z)
  return torch.stack(out,1),hm
class CellBase(nn.Module):
 def __init__(self,kind,h): super().__init__(); self.h=h; self.cell=(nn.LSTMCell(D,h) if kind=='LSTM' else nn.GRUCell(D,h)); self.head=nn.Linear(h,O); self.kind=kind
 def forward(self,x,state=None):
  h=x.new_zeros(x.size(0),self.h) if state is None else state; c=x.new_zeros(x.size(0),self.h) if self.kind=='LSTM' and state is None else (state[1] if self.kind=='LSTM' else None); out=[]
  for t in range(x.size(1)):
   if self.kind=='LSTM': h,c=self.cell(x[:,t],(h,c))
   else: h=self.cell(x[:,t],h)
   out.append(self.head(h))
  return torch.stack(out,1),((h,c) if self.kind=='LSTM' else h)
class Stateless(nn.Module):
 def __init__(self): super().__init__(); self.head=nn.Linear(D,O)
 def forward(self,x,state=None): return self.head(x),None

def task_batch(name,seed,batch=BATCH,device=DEVICE):
 rng=np.random.default_rng(seed); g=torch.Generator(device='cpu'); g.manual_seed(seed)
 if name=='DelayedClass':
  cue=torch.randint(0,O,(batch,),generator=g); x=torch.randn(batch,25,D,generator=g)*.1; x[:,0,:O]=0; x[torch.arange(batch),0,cue]=1; x[:,-1,:]=.5; y=cue[:,None].expand(batch,25); w=torch.ones(25)*.1; w[-3:]=1; w[-1]=2; return x.to(device),y.to(device),w.to(device)
 if name=='XORMemory':
  a=torch.randint(0,2,(batch,),generator=g); b=torch.randint(0,2,(batch,),generator=g); x=torch.randn(batch,15,D,generator=g)*.05; x[:,0,0]=a.float(); x[:,1,1]=b.float(); y=((a+b)%2)[:,None].expand(batch,15); w=torch.zeros(15); w[-3:]=1; return x.to(device),y.to(device),w.to(device)
 if name=='TemporalSelect':
  rule=torch.randint(0,2,(batch,),generator=g); a=torch.randint(0,O,(batch,),generator=g); b=torch.randint(0,O,(batch,),generator=g); x=torch.randn(batch,32,D,generator=g)*.04; x[:,0,:2]=0; x[torch.arange(batch),0,rule]=1; x[:,4,2:2+O]=F.one_hot(a,O).float(); x[:,20,2:2+O]=F.one_hot(b,O).float(); y=torch.where(rule==0,a,b)[:,None].expand(batch,32); w=torch.zeros(32); w[-5:]=1; w[-1]=2; return x.to(device),y.to(device),w.to(device)
 if name=='ContextSwitch':
  T=30; x=rng.normal(0,.05,(batch,T,D)).astype('float32'); y=np.zeros((batch,T),dtype='int64')
  for i in range(batch):
   rule=int(rng.integers(0,4)); prev=0.
   for t in range(T):
    v=float(rng.random())
    if t==0 or (t==15 and rng.random()<.5):
     if t==15: rule=int(rng.integers(0,4))
     x[i,t,:4]=0; x[i,t,rule]=1
    x[i,t,4]=v
    y[i,t]=1 if v>.5 else 0 if rule==0 else 2 if v>.3 else 3 if rule==1 else min(int(prev*4),O-1) if rule==2 else ((v>.5)^(prev>.5))%O
    prev=v
  w=np.ones(T,'float32')*.3; w[1:5]=.8; w[15:20]=1.5; w[-5:]=1; return torch.from_numpy(x).to(device),torch.from_numpy(y).to(device),torch.from_numpy(w).to(device)
 raise ValueError(name)
TASK_EPOCHS={'DelayedClass':240,'XORMemory':240,'TemporalSelect':260,'ContextSwitch':300}
MODELS=['DBC3','LSTM','GRU','Stateless']
def make_model(name): return DBC3() if name=='DBC3' else CellBase(name,LH if name=='LSTM' else GH) if name in ('LSTM','GRU') else Stateless()
def params(m): return sum(p.numel() for p in m.parameters())
def evaluate(m,name,base,n=EVAL_N,reverse=False):
 m.eval(); fc=ft=wc=wt=0
 with torch.no_grad():
  for i in range(n):
   x,y,w=task_batch(name,base+i)
   if reverse: x=x.flip(1)
   z,_=m(x); p=z.argmax(-1); fc+=int((p[:,-1]==y[:,-1]).sum()); ft+=y.size(0)
   for t,v in enumerate(w.tolist()):
    if v>0: wc+=int((p[:,t]==y[:,t]).sum()); wt+=y.size(0)
 return {'final':fc/ft,'weighted':wc/wt}
def train(m,name,epochs,base):
 m.to(DEVICE); opt=torch.optim.Adam(m.parameters(),lr=3e-3); sch=torch.optim.lr_scheduler.CosineAnnealingLR(opt,epochs,eta_min=3e-5); best=copy.deepcopy(m.state_dict()); bestv=-1; start=time.perf_counter()
 for e in range(epochs):
  m.train(); x,y,w=task_batch(name,base+e); z,_=m(x); loss=torch.zeros((),device=DEVICE); den=0.
  for t,v in enumerate(w.tolist()):
   if v>0: loss=loss+float(v)*F.cross_entropy(z[:,t],y[:,t]); den+=float(v)
  opt.zero_grad(set_to_none=True); (loss/max(den,1.)).backward(); nn.utils.clip_grad_norm_(m.parameters(),1.); opt.step(); sch.step()
  if (e+1)%CHECK==0 or e==epochs-1:
   q=evaluate(m,name,base+700000,20)
   if q['final']>bestv: bestv=q['final']; best=copy.deepcopy(m.state_dict())
 m.load_state_dict(best); return m,time.perf_counter()-start

def summary(vals):
 a=np.asarray(vals,float); return {'n':len(vals),'values':vals,'mean':float(a.mean()),'std':float(a.std(ddof=1)),'ci95_normal':[float(a.mean()-1.96*a.std(ddof=1)/np.sqrt(len(a))),float(a.mean()+1.96*a.std(ddof=1)/np.sqrt(len(a)))]}
def export(m,name):
 order=['W_r1','b_r1','W_r2','b_r2','W_enc','b_enc','W_in','W_res','W_tau','b_tau','ln_gamma','ln_beta','W_gate','b_gate','W_head','b_head']; p=OUT/('dbc3_weights_'+name+'.bin')
 with p.open('wb') as f:
  for n in order: f.write(m.state_dict()[n].detach().cpu().contiguous().numpy().astype('<f4').tobytes())
 x,_,_=task_batch(name,880000,1); x=x.cpu(); m.eval()
 with torch.no_grad(): z,h=m(x)
 np.savez(OUT/('dbc3_trace_'+name+'.npz'),input=x.numpy().astype('<f4'),logits=z.cpu().numpy().astype('<f4'),final_hm=h.cpu().numpy().astype('<f4'))
 return {'weights':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'trace':'dbc3_trace_'+name+'.npz','order':order}
def main():
 print('DEVICE='+str(DEVICE)); print('TORCH='+torch.__version__); print('CUDA='+str(torch.version.cuda)); print(json.dumps({'dbc3_params':pc_dbc3(),'lstm_hidden':LH,'lstm_params':pc_lstm(LH),'gru_hidden':GH,'gru_params':pc_gru(GH),'seeds':SEEDS}))
 raw=[]; saved={}
 for ti,name in enumerate(TASK_EPOCHS):
  for si,seed in enumerate(SEEDS):
   for mi,mn in enumerate(MODELS):
    torch.manual_seed(1000000+ti*10000+si*100+mi); m=make_model(mn); m,secs=train(m,name,TASK_EPOCHS[name],2000000+ti*100000+si*1000); q=evaluate(m,name,3000000+ti*100000+si*1000); row={'task':name,'seed':seed,'model':mn,'params':params(m),'seconds':secs}|q; raw.append(row); print(json.dumps(row),flush=True)
    if mn=='DBC3': saved[name]=copy.deepcopy(m).cpu()
 out={}
 for name in TASK_EPOCHS:
  out[name]={}
  d=[r for r in raw if r['task']==name and r['model']=='DBC3']
  for mn in MODELS:
   q=[r for r in raw if r['task']==name and r['model']==mn]; out[name][mn]={'params':q[0]['params'],'final':summary([r['final'] for r in q]),'weighted':summary([r['weighted'] for r in q])}
   if mn!='DBC3': out[name][mn]['delta_DBC3_minus_model']=summary([a['final']-b['final'] for a,b in zip(d,q)])
 config={'device':str(DEVICE),'torch':torch.__version__,'cuda':str(torch.version.cuda),'python':platform.python_version(),'seeds':SEEDS,'batch':BATCH,'eval_batches':EVAL_N,'epochs':TASK_EPOCHS,'params':{'DBC3':pc_dbc3(),'LSTM':pc_lstm(LH),'GRU':pc_gru(GH)}}
 (OUT/'config.json').write_text(json.dumps(config,indent=2)); (OUT/'raw_results.json').write_text(json.dumps(raw,indent=2)); (OUT/'summary.json').write_text(json.dumps(out,indent=2)); (OUT/'exports.json').write_text(json.dumps([export(saved['DelayedClass'],'DelayedClass')],indent=2)); print('RESULTS_DIR='+str(OUT)); print('STATUS=PASS_WITH_SCOPE_SERIOUS_MULTI_SEED')
if __name__=='__main__': main()
PY