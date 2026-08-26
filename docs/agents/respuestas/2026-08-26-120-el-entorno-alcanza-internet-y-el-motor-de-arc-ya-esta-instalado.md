# 120 · Tenías razón: hay herramientas en la red, y una de ellas cambia el plan entero

**Fecha:** 2026-08-26 · rama `titan/twohop-nulls` · **TITAN FULL**

**Evidencia cruda:** `docs/agents/evidencia/2026-08-26-120-egress-de-brain-env-evidencia-cruda.md`

**Herramientas declaradas antes de ejecutar (C-03):** búsqueda web, búsqueda de repos en GitHub, `run` del servicio `build` del gateway (5 corridas), integración de GitHub para escribir.

---

## 0. La lista que te pasé hace 20 minutos queda casi toda refutada

En la 119 te di 9 paquetes para instalar. Medí lo que había y lo que faltaba, y **no medí si yo podía instalarlo solo**. Eso es el patrón 3 de mi propio registro: el límite afirmado sin verificar.

<p></p>

**Medido ahora:**

```plain
pip3 install tabulate  -> exit 0, tabulate 0.10.0, import OK
EXTERNALLY-MANAGED     -> NO EXISTE
```

**`pip3 install` funciona.** No hacía falta pedirte nada de Python. Lo único que sigue necesitando `apt-get` de verdad es el binario `git` y `procps`, y ni `git` es imprescindible (ver §3).

---

## 1. El egress está abierto: 33 destinos, cero bloqueos de red

Sondé 33 endpoints. **Ni un solo error de DNS o de conexión.** Los `401` son "alcanzable, falta credencial"; los `400` son respuesta válida de la raíz de una API.

| categoría | estado |
|---|---|
| **PyPI + files.pythonhosted** | 200 → `pip install` de cualquier cosa |
| **Debian + Ubuntu archives** | 200 → `apt-get` funcionaría |
| **GitHub API / raw / codeload** | 200 → leer y **bajar repos enteros** |
| **Kaggle API** | 401 → ya sabíamos, funciona con Bearer |
| **three.arcprize.org** | 200 root, **401 en `/api/*`** |
| Zenodo, arXiv, OpenAlex | 200 → literatura y depósito |
| **neuprint.janelia.org, codex.flywire.ai** | 200 → **las fuentes del conectoma** |
| HuggingFace, OpenRouter, npm, crates | 200 |
| Modal, Lightning AI, Colab | 200 (web, no API sin cuenta) |

**El container no está encerrado. Está en internet.**

---

## 2. El hallazgo que vale la respuesta entera

```plain
401  https://three.arcprize.org/api/games      -> 'unauthorized'
401  https://three.arcprize.org/api/cmd/RESET  -> {"error":"NOT_AUTHORIZED","message":"no key provided"}
```

**Existe una API oficial de ARC-AGI-3, es alcanzable desde `brain-env`, y responde "no key provided".**

<p></p>

Y el otro lado del mismo hallazgo, medido:

```plain
pip3 install arc-agi arcengine  -> exit 0
python3 -c "import arcengine"   -> exit 0
arcengine 0.1.0
GameAction: ['RESET','ACTION1',...,'ACTION7']
```

> **El motor de la competencia está instalado y corriendo dentro de `brain-env`, con sus 8 acciones expuestas.**

**Lo que faltaba no era un paquete. Era una API key gratuita de `three.arcprize.org/platform`.** Con esa key, el agente juega los **entornos reales** desde acá, sin Kaggle, sin GPU y sin esperar un slot.

<p></p>

Eso parte el problema en dos, y es una separación que antes no existía:

- **Desarrollo e iteración:** API de ARC + `brain-env`. Sin límite de 5 submissions diarias.
- **Score oficial:** Kaggle, y ahí sí hacen falta tus tres clicks.

---

## 3. `git` dejó de ser bloqueante, y por dos vías medidas

**Vía A — refutada por su propia corrida.** Propuse `GitPython`. Se instaló con `RC=0` y después:

```plain
The git executable must be specified in one of the following ways:
    - be included in your $PATH
```

Es un *wrapper* del binario, no un reemplazo. **Mi propia propuesta murió al ejecutarla.** Queda escrito.

<p></p>

**Vía B — confirmada.** `dulwich`, git en Python puro:

```plain
dulwich (1, 2, 13)
clone REAL -> exit 0
entradas: ['.git', '.gitignore', 'Makefile', 'README.md', 'agent', 'notebooks', 'scripts']
```

**Clonó un repo con su `.git` completo, sin el binario `git`.**

<p></p>

**Vía C — también sirve y es la más simple:** `codeload.github.com/<owner>/<repo>/zip/refs/heads/main` da **200**. Ya bajé el starter oficial: 15.872 bytes, 12 archivos, extraído en `/workspace/arc-starter`.

---

## 4. Lo que encontré en GitHub, y qué sirve de cada cosa

| repo | qué es | para qué nos sirve |
|---|---|---|
| **`arcprize/ARC-AGI-3-Kaggle-Starter`** | 14 ⭐ · starter oficial local→Kaggle | **el camino corto**: se edita UN archivo y `make submit` sube. Ya bajado |
| **`arcprize/ARC-AGI-3-Agents`** | 312 ⭐ · MIT · framework oficial | el contrato `Agent`, `is_done`, `choose_action`. Es la base |
| `arcprize/arc-agi-3-benchmarking` | 35 ⭐ · MIT | comparar agentes de forma reproducible |
| **`NVIDIA-NeMo/labs-OO-Agents/examples/arc_agi_3`** | ejemplo de NVIDIA (NOOA) | **el estado del arte publicado**: hipótesis, world model escrito como helpers, jail de contexto |
| `arcprize/ARC-AGI-Community-Leaderboard` | vitrina por PR | **vía de visibilidad sin score oficial**, y explicita que los scores self-reported NO se muestran |

**Leí el `my_agent.py` oficial completo.** Es corto y confirma lo que veníamos diciendo: un `MAX_ACTIONS = 80`, `is_done` que corta solo en `WIN`, y un `choose_action` que hoy elige **al azar**. `ACTION6` es la compleja y toma `(x, y)` en una grilla **64×64**.

<p></p>

**El baseline oficial es azar puro. La vara para superarlo es bajísima, y ahí entra tu `gate` y tu τ heterogénea.**

---

## 5. Lo que SÍ sigue faltando, y ahora es corto

1. **API key de `three.arcprize.org/platform`** — gratuita, es tu click. **Esto desbloquea todo el desarrollo.**
2. **`git` + `procps`** por `apt-get` — comodidad, ya no bloqueante.
3. **GPU: NO hay, y ahora está medido, no inferido.** `nvidia-smi` ausente y `/dev/nvidia*` inexistente. La GPU vive en Kaggle. **Y el starter dice literal: "No GPU required for the starter agent".**

---

## 6. Lo que esto cambia en la prioridad (O-01)

En la 118 puse el erratum primero. **Lo mantengo**, y por el criterio declarado: es el único pasivo reputacional y cuesta un día.

<p></p>

Pero lo que **sí** cambia es el ítem 3. Antes "escribir `my_agent.py`" era un proyecto con dependencia de Kaggle. Ahora es:

<p></p>

1. erratum a Zenodo
2. tu key de ARC + tus 3 clicks en Kaggle
3. **iterar el agente en `brain-env` contra los entornos reales**, sin gastar submissions
4. subir a Kaggle solo lo que ya ganó localmente
5. paper del producto

**Verificación de dependencia, no suposición:** el paso 3 depende **solo** de la key, no del erratum ni de Kaggle. Son módulos distintos, así que pueden ir en paralelo.

---

## 7. NO MEDIDO

- **No obtuve la API key** ni probé `make play-local` de punta a punta: sin key devuelve 401. Es el hueco que queda.
- **No probé `apt-get install` de verdad.** El antecedente del 502 del 22-ago sigue en pie y hay 650 MB libres de 8 GB.
- **No probé `push` con dulwich**, solo `clone`. Escribir puede tener otro comportamiento con el token.
- **Discrepancia sin resolver:** PyPI dice `arcengine` 0.9.3 y el import dice 0.1.0. No concluyo.
- **No leí el código del ejemplo de NVIDIA**, solo su README. Es el estado del arte y merece lectura propia.
- **No probé Modal, Lightning ni Colab con cuenta.** Solo verifiqué que la web responde 200: eso **no** prueba que su API sea usable.
- **No medi la causa del load ~2,0** que sigue abierta de la 119.

---

--- METODO TITAN ---
Accion delicada: NO (lectura + 5 pip installs en brain-env, declarados en la evidencia)
Modo aplicado:   TITAN FULL
Rubrica:         43/45 -> 96/100
                 Completitud 13/15 (-2: no obtuve la API key, asi que play-local
                 quedo sin correr punta a punta)
                 Arquitectura del razonamiento 10/10 (tres vias medidas para git,
                 una refutada por su propia corrida)
                 Documentacion 10/10 · Innovacion 5/5 · Proceso QA 5/5
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es un
                 peritaje del entorno, no codigo de produccion)
Review externo:  no pedido (no hay PR: son dos archivos de documentacion)
Instrumento:     gateway MUDH servicio build, 5 corridas python3 en brain-env,
                 exit=0 en las 5. Salida cruda verbatim commiteada aparte (W-01).
