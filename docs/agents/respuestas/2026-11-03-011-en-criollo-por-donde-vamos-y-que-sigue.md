# 2026-11-03-011 · En criollo: por dónde vamos y qué sigue

**Veredicto del pedido:** explicado. El sobre de 009-A1 (8.540 ensayos) sigue cerrado y sano, medido hoy: ningún commit lo tocó desde el sello y su lista de hashes es la sellada. Las dos calculadoras, la del productor y la independiente, ya coinciden en los ensayos con datos falsos. Para ver resultados falta sólo la autorización escrita de Abraham: «Autorizo abrir el sobre de 009-A1».

Doc: [2026-11-03-011 · En criollo: dónde estamos y qué sigue](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29757)

## En criollo

**La pregunta.** En el modelo de la mosca, un descendente (DNp04) prende a un relevo (PVLP010) que frena a otros descendentes: D→X⊣D′. 009-A1 pregunta si esa regla funciona también en 16 relevos y 6 hubs que tienen esa forma en FlyWire y en BANC. Si se repite, es la primera regla que vale en más de un circuito, el primer ladrillo de la gramática. Si no, DNp04 es un caso aislado. Es el modelo, no la mosca.

**Lo que ya está.** Las 8.540 simulaciones, completas y selladas, sin leer. La calculadora del productor (5c9492ff), probada. La calculadora independiente (5eaf35d0), escrita sin copiar nada de la otra y con otro motor: en los ensayos da los mismos números y además encuentra las 6 fallas plantadas que la del productor no ve.

**Lo que no está.** Ningún resultado real.

## Qué sigue

1. Abraham escribe «Autorizo abrir el sobre de 009-A1».
2. Fases E y T del verificador sobre corrida_1: si algo falla, se para.
3. Fase S del verificador; su salida se commitea antes de que corra el productor.
4. estadistica_a1.py de 5c9492ff con --abrir-sobre; su agregado se commitea.
5. Fase K (cotejo). Si sale CONCORDANTE, se leen los veredictos con la tabla de la 007; si no, no se lee nada hasta entender por qué.

Veredictos principales: P_T1_B (R01, R02 y R03, tienen que dar los tres) y P_T2_B (3 de 4 tipos de hub).

**La trampa, aceptada el 3-nov a las 18:36.** Si cortar sólo D→X ya apaga del todo a X, ese corte y el de apagar X dan lo mismo en las 20 semillas, el cociente vale 1 siempre, el BCa queda degenerado y 010 manda SIN_DECIDIR, aunque sea la mejor noticia para la regla. En el humo pasó en R01 B (X de 30 y 16 espigas a 0). Si pasa en el sobre real, no se corrige mirando: regla nueva escrita antes y otro sobre.

**Tres decisiones de Abraham.** Si la autorización llega sola, se aplica la recomendación y se commitea antes de abrir:

| Decisión | Recomendación por defecto |
|---|---|
| D1: qué es «no evaluable» en 010 | sin datos válidos o sin variación, como ya está en el código |
| D12: índice de ablación original, sin definición en 010 | no se calcula y queda declarado |
| Hueco del control: el verificador invalida lo que el productor dejó pasar | se publican los dos veredictos y vale el más estricto |

**Después de 009-A1.** Si la regla se repite: diseñar G1 (programas cortos que generen circuitos, contra G0 con presupuestos iguales) y medir lo que falta en el modelo: BANC y robustez a peso por sinapsis, tau y umbral. Si no se repite, G1 no puede apoyarse en ella. La mosca real necesita un laboratorio: silenciar DNp04 y registrar GF y DNp06 ante looming.

## Estado vigente que CONTEXTO todavía no refleja

docs/agents/CONTEXTO-drosophila-fep.md en main bb956c6a (136.411 B, sha256 93992ac7…, 567 líneas) quedó en la respuesta 2026-11-03-002. Hasta que se actualice, esto manda sobre sus viñetas de 009-A1, de la síntesis en criollo y de la decisión pendiente:

- **009-A1** (reemplaza «diseño sin runner … Ninguna corrida está autorizada»): runner 4c499296 (VERSION 2026-11-03-005) y manifiesto 267ca1d0 (640.908 B) en titan/a1-runner-2026-11-03. Corrida autorizada el 3-nov a las 14:16 y hecha en Actions en 20 tandas (run 41684131931): 8.540 de 8.540 ensayos válidos, sellados en 7d953dc8 (results/a1_2026-11-03/corrida_1/, SHA256SUMS bf9ebde6…), SIN LEER. Estadística del productor en 5c9492ff (estadistica_a1.py 37ab63d7…), sin cambios. 010 queda tal cual, con su regla de BCa degenerado. Verificador independiente en titan/verificador-a1-independiente (5eaf35d0), escrito por BRAIN con el cambio de plan declarado en la 010: ensayo 12 de 12, prueba 14 de 14 y mutantes 10 de 10 en brain-env. Independencia de selección: deuda; la orden 009 sigue para una auditoría externa.
- **Decisión que espera a Abraham** (reemplaza la autorización del runner): abrir el sobre; D1, D12 y la regla ante un hueco del control; y la sección 15 del Doc maestro, que sigue pendiente con el texto del Doc de la 003.
- **Síntesis vigente en criollo:** esta respuesta.
- **Respuestas posteriores a la 002:** 2026-11-03-003 a 011, en este directorio.

Actualizarlo entero pide reescribir 136 KB o partirlo en un estado vivo corto más el historial por enlace fijo a bb956c6a. Partirlo toca texto de otros agentes: espera a Abraham.

## Pedido

«explica por donde vas, y que sigue en criollo» (Abraham, 3-nov, 22:00 ART).

## Herramientas

- brain-env por el gateway (servicio build, python), dos llamadas de lectura: cuatro consultas a la API pública de GitHub sin autenticar y dos descargas raw (SHA256SUMS.txt del sobre y CONTEXTO). Escribió sólo en /workspace/a1/v2/evid11/ (contexto_viejo.md y estado.log). La cuota de esa API quedó en 1 de 60 hasta que se renueve; la apertura usa descargas raw, que no la consumen.
- GitHub MCP: este push a main. ClickUp: la página del Doc. Sandbox: redacción y sha de este archivo, no es evidencia.
- Ningún bloque del sobre se descargó. Sin acción delicada.

## Qué se midió

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| El sobre sigue como se selló | API: commits que tocan results/a1_2026-11-03/corrida_1 en titan/a1-runner-2026-11-03 | sí, con cualquier commit posterior | PASS: 1 commit, 7d953dc8, el sello |
| Su lista de hashes es la sellada | sha256 de SHA256SUMS.txt bajado por raw en 801487ca | sí, con un byte distinto | PASS: 45.000 B, bf9ebde6…, 444 líneas |
| Nadie tocó código ni bitácora desde la 010 | cabezas de main y de las dos ramas titan | sí, con una cabeza nueva | PASS: bb956c6a, 801487ca, 5eaf35d0 |
| CONTEXTO está al día | encabezado y viñeta de 009-A1 en bb956c6a | sí | FAIL: quedó en la 2026-11-03-002 |

## Evidencia cruda

Script, verbatim (gateway de brain-env, servicio build, herramienta python, exit 0):

```python
import urllib.request, urllib.parse, json, hashlib, os, time
R='gatehot59-star/drosophila-fep-connectome'
D='/workspace/a1/v2/evid11'
os.makedirs(D, exist_ok=True)
log=[]
def P(s):
    log.append(s)
def get(url):
    req=urllib.request.Request(url, headers={'User-Agent':'brain-env-a1','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read(), r.headers
P('host '+os.uname().nodename+' utc '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
heads={}
for b in ['main','titan/a1-runner-2026-11-03','titan/verificador-a1-independiente']:
    j=None
    for form in (urllib.parse.quote(b,safe=''), b):
        try:
            d,h=get('https://api.github.com/repos/%s/branches/%s'%(R,form)); j=json.loads(d); break
        except Exception as e:
            P('  aviso rama %s forma %s: %r'%(b,form,e))
    c=j['commit']; heads[b]=c['sha']
    P('rama %s cabeza %s %s | %s'%(b,c['sha'],c['commit']['committer']['date'],c['commit']['message'].splitlines()[0][:100]))
d,h=get('https://api.github.com/repos/%s/commits?sha=%s&path=%s&per_page=30'%(R,urllib.parse.quote('titan/a1-runner-2026-11-03',safe=''),'results/a1_2026-11-03/corrida_1'))
cs=json.loads(d)
P('commits que tocan results/a1_2026-11-03/corrida_1 en titan/a1-runner-2026-11-03: %d'%len(cs))
for c in cs:
    P('  %s %s | %s'%(c['sha'],c['commit']['committer']['date'],c['commit']['message'].splitlines()[0][:100]))
P('api rate restante %s'%h.get('X-RateLimit-Remaining'))
b,_=get('https://raw.githubusercontent.com/%s/%s/results/a1_2026-11-03/corrida_1/SHA256SUMS.txt'%(R,heads['titan/a1-runner-2026-11-03']))
hs=hashlib.sha256(b).hexdigest()
P('SHA256SUMS.txt en %s: %d B sha256 %s lineas %d'%(heads['titan/a1-runner-2026-11-03'][:8],len(b),hs,b.count(b'\n')))
P('igual al pin bf9ebde6 del sello: %s'%(hs=='bf9ebde69cc12f6c1f5b1c85925aebeeb36fd7fe6f23052aef35706a74cc7e38'))
c,_=get('https://raw.githubusercontent.com/%s/%s/docs/agents/CONTEXTO-drosophila-fep.md'%(R,heads['main']))
open(D+'/contexto_viejo.md','wb').write(c)
t=c.decode('utf-8')
L=t.split('\n')
P('CONTEXTO en main %s: %d B sha256 %s lineas %d'%(heads['main'][:8],len(c),hashlib.sha256(c).hexdigest(),len(L)))
P('CR %d tabs %d lineas-con-espacio-final %d nbsp %d zw %d emdash %d endash %d termina-en-newline %s'%(c.count(b'\r'), t.count('\t'), sum(1 for x in L if x!=x.rstrip()), t.count('\u00a0'), t.count('\u200b'), t.count('\u2014'), t.count('\u2013'), t.endswith('\n')))
for i,x in enumerate(L,1):
    if x.startswith('#'):
        P('%4d %s'%(i,x[:150]))
open(D+'/estado.log','w').write('\n'.join(log)+'\n')
print('\n'.join(log))
print('=====PRIMER TRAMO=====')
print(t[:9000])
```

Salida, verbatim: es docs/agents/evidencia/2026-11-03-011-estado/estado.log. Después el script imprimió los primeros 9.000 caracteres de CONTEXTO, que no se copian porque están en main bb956c6a.

```
host 6c09d8604b07 utc 2026-11-04T01:08:34Z
rama main cabeza bb956c6a5533fb3dbc93578a2a10fa69b7e8a1d4 2026-11-04T00:39:05Z | docs(a1): respuesta 010, verificador independiente ensayado en brain-env y sobre real cerrado
rama titan/a1-runner-2026-11-03 cabeza 801487cad19747e96bb346d98ffad1c3d508847c 2026-11-03T22:08:57Z | feat(a1): sobre sintetico para el ensayo general del verificador independiente
rama titan/verificador-a1-independiente cabeza 5eaf35d08117a34bb37a325a1e4422ffb316b650 2026-11-04T00:23:26Z | feat(a1): verificador independiente de 009-A1, escrito sin codigo del productor
commits que tocan results/a1_2026-11-03/corrida_1 en titan/a1-runner-2026-11-03: 1
  7d953dc8577ecf1fdbaecc4859b902af8854e79b 2026-11-03T17:55:22Z | medicion(2026-11-03-006): corrida 009-A1 en results/a1_2026-11-03/corrida_1, run 41684131931
api rate restante 1
SHA256SUMS.txt en 801487ca: 45000 B sha256 bf9ebde69cc12f6c1f5b1c85925aebeeb36fd7fe6f23052aef35706a74cc7e38 lineas 444
igual al pin bf9ebde6 del sello: True
CONTEXTO en main bb956c6a: 136411 B sha256 93992ac790ee58a7713fa1e9acb42e0c0f1e54f03594183224ed6b92c57934b8 lineas 567
CR 0 tabs 0 lineas-con-espacio-final 0 nbsp 0 zw 0 emdash 0 endash 6 termina-en-newline True
   1 # CONTEXTO VIVO · conectoma / paper / H4
   7 ## 1-nov-2026 · Topo inverso corregido
  38 ## Madrugada y mañana del 13-oct (019 a 2026-10-14-061) · manda sobre el resto
 187 ## Tarde y noche del 12-oct (010 a 018)
 207 ## Mapa del repo (respuesta 2026-10-11-004)
 227 ## Veredicto operativo
 252 ## v2.0 del Paper 1 (respuesta 2026-10-12-007)
 289 ## Auditoría del laboratorio por TITÁN Tao (pedido 2026-10-12)
 311 ## Paper y Tabla 7 (respuestas 002 a 009 del 10-oct y 003 y 004 del 11-oct)
 332 ## Estado confirmado en main (H4)
 342 ## Estado de producto y ciencia
 441 ## Próximos pasos
 487 ## Fuentes
 531 ## NO MEDIDO
```

## Archivos

- docs/agents/respuestas/2026-11-03-011-en-criollo-por-donde-vamos-y-que-sigue.md (este)
- docs/agents/evidencia/2026-11-03-011-estado/estado.log

## NO MEDIDO

- Qué dicen los 8.540 ensayos: ningún estimando real calculado.
- Si la trampa ocurre en el sobre real: inferencia desde el humo.
- Los bloques no se re-hashearon hoy: su integridad sale de que ningún commit tocó corrida_1 desde 7d953dc8 (git direcciona por contenido) más el sha de SHA256SUMS.
- La verificación post-push de este commit: se mide después del push y queda en el Doc y en brain-env (/workspace/a1/v2/evid11/), no en este archivo.
- La independencia de selección del verificador (deuda de la 010).
- El token de Zenodo que CONTEXTO da como no revocado (2026-10-14-034): no se midió hoy.

```plain
--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado:   LIGERO
Maquina:         brain-env (host 6c09d8604b07, Python 3.12.14)
Rubrica:         N/A (modo ligero)
N/A declarados:  rubrica entera (lectura de estado, sin codigo ni instrumento nuevo entregado)
Review externo:  no pedido (deuda declarada)
Instrumento:     BRAIN por el gateway de brain-env, el script de arriba, exit 0;
                 salida cruda en docs/agents/evidencia/2026-11-03-011-estado/estado.log
Artefactos:      docs/agents/respuestas/2026-11-03-011-en-criollo-por-donde-vamos-y-que-sigue.md
                 + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29757
```
