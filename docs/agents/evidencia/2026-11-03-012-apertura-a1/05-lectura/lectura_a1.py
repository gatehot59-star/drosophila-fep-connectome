
import json, hashlib, collections
A='/workspace/a1/v2/apertura'
PA=A+'/prod/agregado_a1.json'; PV=A+'/ver/verificador_a1.json'
sh=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
ag=json.load(open(PA)); vf=json.load(open(PV))
out=[]; P=out.append
P('lectura_a1 | agregado %s | verificador %s'%(sh(PA),sh(PV)))
claves=('P_T1_B','P_T2_B','F_C','F_R01','T3')
ig={k: json.dumps(ag['veredictos'][k],sort_keys=True)==json.dumps(vf['veredictos'][k],sort_keys=True) for k in claves}
P('veredictos decisivos iguales en productor y verificador: %s'%json.dumps(ig,sort_keys=True))
qa={k:(x['DQWEAK_Hz'],x['banda']) for k,x in ag['veredictos']['QWEAK'].items()}
qv={k:(x['DQWEAK_Hz'],x['banda']) for k,x in vf['veredictos']['QWEAK'].items()}
P('QWEAK igual en DQWEAK_Hz y banda: %s (el productor agrega una nota de texto por celda)'%(qa==qv))
P('P_ESTRATOS productor %r | verificador %r'%(ag['veredictos']['P_ESTRATOS'],vf['veredictos']['P_ESTRATOS']))
v=ag['veredictos']
P('P_T1_B %s casos %s'%(v['P_T1_B']['veredicto'],json.dumps(v['P_T1_B']['casos'],sort_keys=True)))
P('P_T2_B %s tipos %s'%(v['P_T2_B']['veredicto'],json.dumps(v['P_T2_B']['tipos'],sort_keys=True)))
P('P_T2_B instancias %s'%json.dumps(v['P_T2_B']['instancias'],sort_keys=True))
P('F_C %s'%json.dumps(v['F_C'],sort_keys=True))
P('F_R01 %s contrastes %s'%(v['F_R01']['firma'],json.dumps(v['F_R01']['contrastes'],sort_keys=True)))
c=ag['casos']
def f(z): return 'NA' if z is None else '%.3f'%z
def q(d,k):
    x=(d.get('cocientes') or {}).get(k) or {}
    ic=x.get('ic95')
    return '%s [%s, %s]%s'%(f(x.get('estimado')), f(ic[0]) if ic else 'NA', f(ic[1]) if ic else 'NA', '' if x.get('estado_ic')=='OK' else ' '+str(x.get('estado_ic')))
P('B | celda | estado | DQ2_Hz [IC95] | x_C0_Hz | c_X | r_Q1 | s4 | criterio')
act=collections.Counter()
for k in sorted(x for x in c if x.startswith('B|')):
    d=c[k]; m=d['activacion']['medido']; e=d['activacion']['estado']
    act[(k[2]=='H', e)]+=1
    if k[2]=='R':
        cr=('T1 '+d['T1']['estado']) if 'T1' in d else ''
        P('B | %s | %s | %.2f [%s, %s] | %.2f | %s | %s | %s | %s'%(k[2:],e,m['DQ2_Hz'],f(m['IC95_DQ2'][0]),f(m['IC95_DQ2'][1]),m['x_C0_Hz'],q(d,'c_X'),q(d,'r_Q1'),q(d,'s4'),cr))
    else:
        P('B | %s | %s | %.2f [%s, %s] | %.2f | conj %s | conj %s | conj %s | T2 %s'%(k[2:],e,m['DQ2_Hz'],f(m['IC95_DQ2'][0]),f(m['IC95_DQ2'][1]),m['x_C0_Hz'],q(d,'c_Xconj'),q(d,'r_Q1conj'),q(d,'s4conj'),d['T2']['estado']))
P('B conteo de estados: relevos %s | hubs %s'%(dict((e,n) for (h,e),n in act.items() if not h),dict((e,n) for (h,e),n in act.items() if h)))
for k in sorted(x for x in c if x.startswith('C|')):
    d=c[k]; fc=d['FC']; ic=fc['intervalo']['ic95']
    P('C | %s | FC %s | sincronizado menos corrido %s Hz [%s, %s] | transferencia %s'%(k[2:],fc['estado'],f(fc['intervalo']['estimado']),f(ic[0]),f(ic[1]),d.get('transferencia')))
P('A (descriptivo) | celda | estado | DQ2_Hz [IC95] | c_X | r_Q1 | s4')
for k in sorted(x for x in c if x.startswith('A|')):
    d=c[k]; e=d['activacion']['estado']
    if e!='RECLUTADO':
        P('A (descriptivo) | %s | %s'%(k[2:],e)); continue
    m=d['activacion']['medido']
    P('A (descriptivo) | %s | %s | %.2f [%s, %s] | %s | %s | %s'%(k[2:],e,m['DQ2_Hz'],f(m['IC95_DQ2'][0]),f(m['IC95_DQ2'][1]),q(d,'c_X'),q(d,'r_Q1'),q(d,'s4')))
for z in ('ZA1','ZA2','ZA3'):
    x=ag['intervalos'].get('A|R01|'+z) or {}
    ic=x.get('ic95')
    P('A | R01 | %s | %s [%s, %s]'%(z,f(x.get('estimado')),f(ic[0]) if ic else 'NA',f(ic[1]) if ic else 'NA'))
P('T3 %s'%json.dumps(v['T3'],sort_keys=True))
P('motores del verificador: %s'%json.dumps(vf.get('motores',{}).get('chequeos'),sort_keys=True))
open(A+'/lectura/lectura_a1.txt','w').write('\n'.join(out)+'\n')
print('\n'.join(out))
