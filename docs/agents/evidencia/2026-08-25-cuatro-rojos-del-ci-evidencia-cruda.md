# EVIDENCIA CRUDA · los cuatro rojos del CI, y el 403 de la API

**Fecha:** 2026-08-25 12:00 (America/Buenos_Aires)
**Instrumento:** sandbox propio con `git init` · `gateway build.run` sobre `brain-env` · `githubmcp_pull_request_read get_check_runs`

---

## 1. 🔍 QUÉ API DEVOLVIÓ 403, medido con los headers

**La API es `api.github.com`, llamada con `curl` DESDE EL CONTAINER, sin token.**

```
$ curl -sS -D h3.txt 'https://api.github.com/repos/gatehot59-star/drosophila-fep-connectome/actions/runs?per_page=1'
HTTP=403
x-ratelimit-limit: 60
x-ratelimit-remaining: 0
x-ratelimit-used: 60
x-ratelimit-resource: core
x-ratelimit-reset: 1787672008

$ curl -sS -D h4.txt 'https://api.github.com/repos/gatehot59-star/drosophila-fep-connectome'   # CONTROL
repo HTTP=403
x-ratelimit-remaining: 0
x-ratelimit-resource: core
```

**El control confirma que no es el endpoint de Actions: cualquier endpoint da 403.** Es la cuota entera.

```
$ python3 -c "import os; ks=[k for k in os.environ if any(t in k.upper() for t in ('GITHUB','GH_','TOKEN'))]; print(ks or 'NINGUNA')"
  variables de entorno con token: NINGUNA
```

**Los buckets, medidos contra `/rate_limit`:**

```
  code_search                  limit=   60 remaining=    0 reset_en=2295s
  core                         limit=   60 remaining=    0 reset_en=2295s
  graphql                      limit=    0 remaining=    0 reset_en=3600s
  integration_manifest         limit= 5000 remaining= 5000 reset_en=3600s
  search                       limit=   10 remaining=   10 reset_en=60s
```

> **Causa: `core` sin autenticar son 60 llamadas por hora POR IP.** El container no tiene token, así que cae en ese bucket.

### ⚠️ Y el medidor mismo es poco fiable, medido

Tres minutos antes, la **misma** consulta a `/rate_limit` devolvió:

```
x-ratelimit-limit: 60
x-ratelimit-remaining: 60
x-ratelimit-used: 0
x-ratelimit-reset: 1787673253
```

Y tres minutos después: `remaining 0`, `used 60`, y el **`reset` retrocedió 1.245 segundos** (de `...3253` a `...2008`).

**Yo no hice 60 llamadas en tres minutos.** Las dos lecturas juntas dicen que **la cuota no es solo mía**: la IP de salida del container es compartida, y/o hay varios nodos con contadores distintos. **O sea que `/rate_limit` NO es un medidor confiable de si la próxima llamada va a pasar.** Es el patrón del `$?` mentiroso otra vez, en otra herramienta: **consultar el medidor no sustituye a hacer la llamada.**

### 🔴 Y el error de método, que es el que importa

**Había una vía autenticada disponible todo el tiempo**, y expone exactamente lo que estaba haciendo a mano:

```
githubmcp_pull_request_read  method=get_check_runs  ->  HTTP 200, datos completos
  total_count 2
  bateria de guards (debe poder dar rojo) | completed | failure | 14:48:05Z
  bateria de guards (debe poder dar rojo) | completed | failure | 14:48:03Z
```

**5.000 llamadas por hora contra 60, y un método dedicado a check runs.** Gasté una cuota compartida reimplementando con `curl` algo que tenía una herramienta. **Es D-01 al pie de la letra: antes de pelear con un límite, revisar el catálogo.**

---

## 2. 🔥 EL CUARTO ROJO · causa reproducida, no inferida

Leído por la vía autenticada: **dos check runs, ambos `failure`, 8 segundos cada uno**, a las 14:48:03 y 14:48:05 UTC (son dos porque el workflow dispara en `push` y en `pull_request`).

**Ocho segundos es demasiado poco para un fallo de instalación y demasiado para el checkout solo**, así que el candidato era un paso del final. Reproducido en el sandbox, **esta vez dentro de un repo git de verdad**:

```
$ git init -q . && cp guards.py test_guards_negativo.py ci_mutate_guards.py src/ && git add -A && git commit -qm base
=== arbol limpio al arrancar? ===
   (vacio = limpio)

=== HIPOTESIS: el paso 6 falla por __pycache__ que crea el import ===
paso 1 rc=0
paso 2 rc=0
paso 3 rc=1 (espera !=0)
paso 4 rc=0
paso 5 rc=0
--- paso 6: git status --porcelain ---
   ?? src/__pycache__/
   >>> ARBOL SUCIO: el paso 6 FALLA. Causa reproducida.
```

> **Importar `guards` crea `src/__pycache__/`, y el paso 6 exige árbol limpio.** Los cinco pasos que miden algo daban bien; el sexto fallaba por un efecto colateral de los cinco anteriores.

**El fix, verificado en la misma corrida:**

```
=== EL FIX: PYTHONDONTWRITEBYTECODE=1 ===
bateria con PYTHONDONTWRITEBYTECODE rc=0
mutada rc=1
verde otra vez rc=0
--- git status ahora ---
   >>> LIMPIO: el fix funciona
954815935545435ced0d1a26865c0859  src/guards.py
```

**Entran dos cosas y no una:** la variable a nivel de job, **y** un `.gitignore` con `__pycache__`, para que el árbol siga limpio si alguien corre la batería a mano sin la variable. **El repo no tenía `.gitignore`.**

---

## 3. El patrón común de los cuatro rojos

| # | Síntoma | Causa | Por qué no lo vi antes |
|---|---|---|---|
| v1 | `IndentationError` | heredoc indentado en un `run:` de YAML | escribí el YAML y no lo corrí |
| v2 | `pip` aborta | cuatro pins **de memoria** bajo la etiqueta «MEDIDAS»; `pandas 2.3.4` no existe | no consulté PyPI antes de escribirlos |
| v3 | `pip` aborta | seguí arreglando la instalación | no pregunté si la instalación hacía falta |
| v4 | árbol sucio | `__pycache__` del import | probé el ciclo en un directorio que **no es un repo git** |

> **La forma es la misma cuatro veces: mi banco de pruebas no reproducía la condición que el paso mide.** En la v4 corrí «el ciclo completo, los siete pasos» y lo declaré verificado, pero el paso 6 **no podía ejecutarse** porque `/tmp/ci_repro` no era un repo. **Es E-01 aplicado a un workflow: el experimento correcto sobre el sujeto equivocado se siente como rigor y no lo es.**

**Y el lado bueno, que hay que decir:** las cuatro las encontró **el CI**, no yo. Un instrumento sin lealtades que dice «no» cuatro veces seguidas es exactamente lo que B-01 pide, y es la primera vez que este repo tiene uno.

---

## 4. Qué quedó corriendo, y dónde

| Qué | Dónde | Estado medido |
|---|---|---|
| **El barrido de sensibilidad** | `brain-env`, `/workspace/sens/`, lanzado con `nohup` | **VIVO.** 3 procesos con el patrón en `/proc/*/cmdline`. **8 de 30 puntos** escritos en `sens.log`. Escribe `out.json` al final |
| **El job de guards** | runners de GitHub Actions | **4 corridas terminadas, todas `failure`.** La quinta la dispara este commit |
| El `.mat` de Betzel | `/workspace/ab_models/betzel_connectome.mat` | **descarga COMPLETA**, 106.587.606 B, md5 coincide |

**Los 8 puntos del barrido, verbatim:**

```
  p=0.0001 seed=  1  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.00  spread=    inf  no-sat
  p=0.0001 seed=  4  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.05  spread=    inf  no-sat
  p=0.0001 seed= 16  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.05  spread=    inf  no-sat
  p=0.0001 seed= 64  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.03  | AZAR=  0.12  spread=    inf  no-sat
  p=0.0001 seed=256  vis=  0.00  olf=  0.00  mec=  0.07  gus=  0.10  | AZAR=  0.30  spread=    inf  no-sat
  p=0.0010 seed=  1  vis=  0.00  olf=  0.10  mec=  0.30  gus=  0.75  | AZAR=  1.48  spread=    inf  no-sat
  p=0.0010 seed=  4  vis=  0.00  olf=  3.92  mec=  0.65  gus=  6.40  | AZAR=  5.42  spread=    inf  no-sat
  p=0.0010 seed= 16  vis=  0.00  olf=  7.33  mec=  5.40  gus= 20.85  | AZAR= 16.00  spread=    inf  no-sat
```

**🔴 Lo que ya se ve y hay que declarar como PARCIAL:** en `p=0.001, seed=16` el **control negativo al azar alcanza 16,00 motoras**, más que **visual (0,00)** y más que **mechanosensorial (5,40)**. O sea que en el régimen bajo el estadístico **separa clases pero el azar le gana a dos de las cuatro.** **Eso puede angostar el veredicto de la resp 082 y NO se emite conclusión hasta los 30 puntos.**

---

## 5. Cómo se resuelve y cómo se mejora

**Del 403, tres niveles:**

1. **Inmediato, y ya aplicado:** usar la **integración autenticada** (`get_check_runs`) en vez de `curl` anónimo. 5.000/hora contra 60, y un método dedicado.
2. **Estructural, si hace falta `curl` desde el container:** un token de solo lectura en el entorno del container sube el bucket de 60 a 5.000. **Eso es rotar/crear una credencial y es decisión de Abraham** (P-01). **No se hizo.**
3. **El que evita la pregunta entera:** que el CI **deje su recibo en el repo** en vez de que haya que ir a preguntarle a la API. Un job que escribe su conclusión como artefacto o como commit de recibo se lee con las mismas herramientas que todo lo demás. **Es la misma idea que la bitácora: si está commiteado, no hay que pedir permiso para leerlo.**

**Del CI:** los cuatro rojos se cierran con este commit, **y la mejora de proceso vale más que los cuatro fixes**: el banco de pruebas ahora es un **repo git inicializado**, para que el paso que mide el árbol tenga un árbol que medir.

---

## 6. NO MEDIDO, declarado

1. **La quinta corrida del CI no se vio.** La dispara este commit. **No se declara verde.**
2. **Los logs del job no se leyeron nunca:** la API de logs devuelve 403 sin token y la integración no expone un método de logs. **Las cuatro causas se identificaron por reproducción en el sandbox, no leyendo el log del runner.** Si alguna corrida falló por otro motivo además del reproducido, no lo sé.
3. **El barrido sigue corriendo:** 8 de 30. Sin veredicto.
4. **No se agregó ningún token al container.** Es decisión de Abraham.
5. **El recibo del CI en el repo (nivel 3) no se implementó**, solo se propone.
