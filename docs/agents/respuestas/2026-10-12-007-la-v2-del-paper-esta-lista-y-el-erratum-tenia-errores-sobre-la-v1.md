# 2026-10-12-007 · La v2 del paper está lista para depositar, y el erratum tenía errores sobre la v1.0

**Doc de ClickUp:** https://app.clickup.com/90171457413/docs/2kza6fw5-21437 · **PR:** https://github.com/gatehot59-star/drosophila-fep-connectome/pull/27 (rama `titan/v2-cierre-2026-10-12`, commits `c1becef`, `5035c39`, `554f7d9`; sin merge).

**Veredicto:** la v2.0 del Paper 1 está escrita, renderizada y verificada (PASS). El depósito en Zenodo espera sólo el token de Abraham y su sí para publicar. Cotejado contra el texto real del PDF v1.0, el erratum tenía **tres errores propios**, que quedaron corregidos en el PR, y la v1.0 tiene **cinco referencias con datos mal**.

## 1. Pedido

- 10:50: «cerremos el v2». Cerrar la v2.0 del Paper 1 en Zenodo. Coincide con el botón «Preparar la v2 del paper» de la 006.
- 11:14, durante el trabajo: «pide a tao que audite todo el laboratorio creaodo, las prueas, demostracines hipotesso con clusiones. creo que podemos sacarle mas provecho a este lavoratorio que genera circuitos d ela mozca».

## 2. Herramientas y máquina

- **brain-env** (gateway MUDH, servicio `build`, herramienta `python`):
  - bajó el PDF v1.0 por la API pública de Zenodo, sin token;
  - instaló `pypdf 6.16.2` y `typst 0.15.0` con pip;
  - extrajo el texto de la v1.0;
  - leyó el json de la Tabla 7 del pin (`/workspace/dfc-t7/results/table7_reconstruida_2026-10-10/table7_reciprocity_by_class.json`);
  - clonó el repo con sus 36 refs y buscó con `git grep`;
  - renderizó con pandoc 3.10.2 y verificó en dos clones frescos.
  - Escribió sólo en `/workspace/v2cierre_2026-10-12/`. `/workspace/v2` resultó ser un archivo ajeno de 203 B (un script de ssh): no se tocó ni se usó.
- **Sandbox de ClickUp:** Tabla 5 recomputada con scipy (binomial).
- **GitHub:** rama `titan/v2-cierre-2026-10-12` con tres commits, PR #27 y este commit en `main`.
- **Web:** verificó Betzel 2026, Bates 2026, Gouwens & Wilson 2009, Nagel & Wilson 2011, Tuthill & Wilson 2016, Hasani 2022, Costi 2025, Yu 2026, Jin 2026, Gordon & Scott 2009, Shiu 2022 y el registro 10676866 de Zenodo, más los alcances de token en developers.zenodo.org.
- **ClickUp:**
  - encontró al agente TITÁN Tao y leyó su configuración;
  - ubicó la lista Pipeline TITAN;
  - creó el Doc de esta respuesta.
  - **No le escribió a Tao.**
- **Cuota:** sin cuota ajena. En Zenodo sólo hubo lectura pública.

## 3. Qué se midió

1. **El PDF v1.0 es el del registro:** 185.471 B, md5 `c7cb36a261182f6ce895057ebe26e505`, 7 páginas, 23.037 caracteres de texto.
2. **El erratum contra ese texto** (ocurrencias medidas):

   | Cadena | En la v1.0 | Lectura |
   |---|---|---|
   | «rate 100%» | 1 | |
   | «98.5» | 0 | ítem 8 al revés |
   | «1,559» | 0 | ítem 4 correcto |
   | «0.0074» | 1 | |
   | «XXXXXXX» | 1 | |
   | «AGPL» | 1 | |
   | «Mendieta-Architect» | 1 | |
   | «8.7%» | 2 | Tabla 6 y Tabla 7 |

3. **Tabla 5 recomputada**, densidad 7,851969529e-4 y P(exc) 0,600272:
   - Los 8 ratios reproducibles coinciden con el erratum a tres decimales.
   - p binomiales: thermosensory 0,094, hygrosensory 1,3e-10, el resto < 1e-300.
   - Sin la AN quedan **3 enriquecidas, 4 empobrecidas y 1 dentro**; el erratum decía 4, contando la AN.
   - Rango sobre las 8 reproducibles: **713×**. Con la AN completa: 989× sin redondear y 991× con los ratios redondeados.
4. **Las 8 clases del null de grado** son visual, olfactory, mechano, gustatory, hygro, thermo, AN y unk_sens: la AN completa (2.231) y sin visual optic (`src/routing_hierarchy.mjs`, líneas 15 y 26; `README.md`, líneas 61 a 70).
5. **Tabla 7 por fila con el pin:**
   - Sin umbral, sensory→descending da 2.104/24.326 = 8,6492%.
   - Con ≥5, los valores son los de la sección 4.
6. **Referencias:**
   - 5 con datos mal: Gouwens & Wilson, Nagel & Wilson (que además no trata lo que se le atribuye), Tuthill & Wilson, Hasani y Schlegel (estos dos con el título del preprint).
   - 7 bien: Betzel, Bates (656:957–970), Costi, Yu, Jin, Zenodo 10676866 y, del erratum, Lin y Dorkenwald.
7. **Render en clon fresco de `5035c39`:**
   - manuscrito: 17 páginas, md5 `50df4ab9c88add11282e70ef3668c7d0`;
   - erratum: 14 páginas, md5 `28f7a21f97648c12faf90f2190f3ccbc`;
   - dos compilaciones iguales;
   - 19/19 cadenas.
   - **PASS.**
8. **`depositar_v2.py --verificar`:** PASS en el clon de render y en clon fresco de `554f7d9`.
9. **md5 de lo commiteado contra lo corrido:** 3/3 iguales en clon fresco (los dos logs y la lista de archivos).
10. **Control negativo del chequeo de texto:**
    - 12 de 13 errores de la v1.0 no están en el PDF v2.0. El que está («four parameter-free neural models») es la cita textual del cambio 6 de la lista de cambios.
    - Control positivo: el PDF del erratum sí los cita, 5/5.
11. **Token:** ninguna variable ni archivo `zenodo` en brain-env.
12. **Alcances de Zenodo:** `deposit:write` sube y edita; `deposit:actions` hace falta para `newversion` y `publish` (developers.zenodo.org).

## 4. Evidencia cruda verbatim

**PDF v1.0 y cotejo (brain-env):**

```
pdf bytes 185471 md5 c7cb36a261182f6ce895057ebe26e505
via pypdf 6.16.2
chars 23037 pages 7 txt md5 b7f0f2d9dfcc90aeabe3d08329932ad8
'98.5' 0 []
'98,5' 0 []
'1,559' 0 []
'1559' 0 []
'rate 100' 1 ['rves degree distribu- tion; destroys modularity. Factor 3×, rate 100%. N=100 for static analyses; N=']
'0.0074' 1 [', 60.0%; 6,032,681 inhibitory, 40.0%; E/I =1.50 ). Density =0.0074. 2.2 Normalization For temporal p']
'8.7%' 2 ['ry 0.05% 73% 704% Reflex + gradual contain. Olfactory 0.00% 8.7% 10.7% Free propagation Visual L 12.', 'ntra-sensory 30.7% Sensory→central 24.2% Sensory→descending 8.7% Sensory→motor 3.6% Optic→motor 0.0%']
'XXXXXXX' 1 ['wed Deposited at Zenodo, March 20, 2026·DOI: 10.5281/zenodo.XXXXXXX Signal Propagation Properties in']
'AGPL' 1 ['Mendieta-Architect/ drosophila-connectome-propagation under AGPL v3 license. Numerical results and s']
ENV zenodo-like: []
FILES zenodo-like:
```

**`docs/METHODS.md` en main (git grep):**

```
origin/HEAD:docs/METHODS.md:103:Measured acceptance was 98.5 per cent. A reported rate of exactly 100 per cent is not
```

**Tabla 7 del json del pin (`sin_umbral` y `umbral_5`):**

```
SINU motor -> motor 509 210 41.2574
SINU visual_centrifugal -> visual_centrifugal 7490 2764 36.9025
SINU optic -> optic 6201390 1983172 31.9795
SINU sensory -> sensory 34107 10460 30.6682
SINU sensory -> central 159316 38549 24.1966
SINU sensory -> descending 24326 2104 8.6492
SINU sensory -> motor 1178 42 3.5654
SINU optic -> motor 6 0 0.0
U5 motor -> motor 80 28 35.0
U5 visual_centrifugal -> visual_centrifugal 1324 310 23.4139
U5 optic -> optic 1069721 183060 17.1129
U5 sensory -> sensory 1287 482 37.4514
U5 sensory -> central 33497 4609 13.7594
U5 sensory -> descending 4786 136 2.8416
U5 sensory -> motor 373 5 1.3405
U5 optic -> motor 0 0 None
```

**Tabla 5 (sandbox, scipy):**

```
density 0.0007851969529044999 pexc 0.600272 N*(N-1) 19220633682
mechanosensory   N=  2656 obs= 23010 exp=   1859.01 ratio= 12.3776 p=0 verdict=enriched
unknown sensory  N=   131 obs=  1179 exp=     91.69 ratio= 12.8585 p=0 verdict=enriched
gustatory        N=   408 obs=  1280 exp=    285.57 ratio=  4.4823 p=0 verdict=enriched
thermosensory    N=    29 obs=    14 exp=     20.30 ratio=  0.6897 p=0.0938 verdict=within
hygrosensory     N=    74 obs=    13 exp=     51.79 ratio=  0.2510 p=1.31e-10 verdict=depleted
olfactory        N=  2279 obs=    80 exp=   1595.14 ratio=  0.0502 p=0 verdict=depleted
visual optic     N= 77530 obs=  1679 exp=  54265.43 ratio=  0.0309 p=0 verdict=depleted
visual           N= 10855 obs=   137 exp=   7597.72 ratio=  0.0180 p=0 verdict=depleted
spread repro 713.0765776473222
spread with AN 989.3119512094088
```

`p=0` es desborde por abajo de scipy (menor que 1e-308).

**Las clases del null de grado (`titan/initial-release:src/routing_hierarchy.mjs`):**

```
  15 const sens=f.filter(x=>[1,2,3,4,5,6,7,8].indexOf(x.gi)>=0);
  26 const dens={visual:0.018,olfactory:0.050,mechano:12.378,gustatory:4.482,hygro:0.251,thermo:0.690,AN:17.839,unk_sens:12.858};
```

**Render y verificación:** los logs crudos están en el PR, `docs/v2/render-v2.0.log` (md5 `2738d6ae761d8b01904542e0d23fa27e`) y `docs/v2/verificar-v2.0.log` (md5 `a1522a9ed09508b00e03660c7ec0c172`). Las líneas de veredicto:

```
PDF Mendieta2026_Paper1_v2.0.pdf 326535 50df4ab9c88add11282e70ef3668c7d0 paginas 17 determinista True
PDF Mendieta2026_Paper1_Erratum_v1.0.pdf 189046 28f7a21f97648c12faf90f2190f3ccbc paginas 14 determinista True
VEREDICTO_RENDER PASS
VEREDICTO_VERIFICAR PASS
```

**Clon fresco de `554f7d9`:**

```
MD5 docs/v2/render-v2.0.log 2738d6ae761d8b01904542e0d23fa27e original 2738d6ae761d8b01904542e0d23fa27e IGUAL
MD5 docs/v2/verificar-v2.0.log a1522a9ed09508b00e03660c7ec0c172 original a1522a9ed09508b00e03660c7ec0c172 IGUAL
MD5 docs/v2/archivos-deposito-v2.0.json 50a6a3adec0bde1feadc36b0141c24a4 original 50a6a3adec0bde1feadc36b0141c24a4 IGUAL
MD5 docs/v2/paper1-v2.0.md ec6dc5d3d599f6c1b6fddc8425fe25d2
MD5 docs/ERRATUM.md f8fbb170e20abaacc5730a102aad5491
MD5 docs/V2-CIERRE.md c130860a7d8fb1151e57f6c1121ed3e8
VERIFICAR_EN_CLON_FRESCO exit 0 VEREDICTO_VERIFICAR PASS
```

**Control negativo y positivo del chequeo de texto:**

```
CONTROL_NEGATIVO (errores de la v1.0 que NO deben estar en la v2.0; se espera FALTA)
   FALTA    Mendieta-Architect
   FALTA    XXXXXXX
   FALTA    rate 100%
   FALTA    AGPL
   FALTA    Zero classes enriched
   PRESENTE four parameter-free neural models
   FALTA    36× over expectation
   FALTA    29(44), 13828
   FALTA    Biophysical basis of coding
   FALTA    10(5), 1295
   FALTA    26(10), 1295
   FALTA    quantifies circuit stereotypy
   FALTA    Closed-form continuous-depth models
CONTROL_POSITIVO (el erratum SI cita los errores de la v1.0)
   PRESENTE Mendieta-Architect
   PRESENTE XXXXXXX
   PRESENTE rate 100%
   PRESENTE 29(44), 13828
   PRESENTE Biophysical mechanisms underlying olfactory receptor neuron
```

**Tao (configuración leída):**

- nombre: TITÁN Tao;
- disparadores: `dm`, `mention`, `assignee`;
- repo por defecto: `gatehot59-star/mudh-mobile`;
- tiene GitHub de lectura y escritura (rama y PR, nunca merge) y `execute_bash`;
- no tiene el gateway de brain-env.

## 5. Archivos

**En `titan/v2-cierre-2026-10-12` (PR #27):**

- `docs/v2/paper1-v2.0.md`: manuscrito v2.0.
- `docs/ERRATUM.md`: revisado antes de depositar.
- `docs/PIVOTE-RECIPROCIDAD.md`: al día.
- `docs/SECCION-V2-DOS-SALTOS.md`: la versión posterior al null anatómico, con el prior art del F.6.
- `tools/v2/render_v2.py`: render determinista.
- `tools/zenodo/depositar_v2.py`: `--verificar`, `--borrador` y `--publicar`.
- `docs/v2/zenodo-v2.0-metadata.json`, `docs/v2/archivos-deposito-v2.0.json`, `docs/v2/render-v2.0.log`, `docs/v2/verificar-v2.0.log` y `docs/V2-CIERRE.md`.

**En `main` (este commit):**

- esta respuesta;
- `docs/agents/CONTEXTO-drosophila-fep.md`, reescrito;
- `docs/auditorias/2026-10-12-pedido-auditoria-tao-laboratorio.md`.

**En brain-env, sin commitear** (binarios derivados):

- `/workspace/v2cierre_2026-10-12/deposito/Mendieta2026_Paper1_v2.0.pdf`
- `/workspace/v2cierre_2026-10-12/deposito/Mendieta2026_Paper1_Erratum_v1.0.pdf`
- el PDF v1.0 bajado y su texto;
- los clones.

## 6. NO MEDIDO

- **Nadie miró los PDF a ojo:** sólo extracción de texto y 19 cadenas. Maquetación, cortes de tablas anchas (la Tabla 5 tiene 9 columnas) y fórmulas se revisan en el borrador de Zenodo.
- **Los metadatos no se probaron contra la API real:** sólo está medido que tienen los campos exigidos.
- **Depósito, borrador y publicación:** no hechos, porque falta el token.
- **El manuscrito se reconstruyó desde el texto del PDF:** tablas y fórmulas se retipearon. Una lectura humana completa contra la v1.0 queda pendiente; los números que cambian vienen del erratum y de las mediciones de esta respuesta.
- **Literatura para §3.4:** barrido básico, no sistemático.
- **Rango 5–20 ms de Gouwens & Wilson:** no se releyó contra el paper. La página de PMC se cortó antes de los resultados.
- **Siguen abiertos:** la Tabla 8 no reproducible, la fila AN, la décima clase de la Tabla 5 y los valores de Lin por neuropilo.
- **El alcance** (sin el control de las salidas, que pasa al Paper 2) es una recomendación de BRAIN, no una decisión de Abraham.
- **La auditoría de Tao:** no se envió ni empezó.

## Antes de firmar

- **¿El chequeo de texto podía dar rojo?** Sí, y se midió:
  - el control negativo dio FALTA en 12 de 13;
  - el único PRESENTE es una cita legítima;
  - el positivo dio 5/5;
  - el render sale con código 1 si falta una cadena o si dos compilaciones difieren.
- **¿Sujeto exacto (E-01)?** Cada afirmación del erratum sobre la v1.0 se coteó contra el PDF depositado (md5 igual al del registro), no contra borradores. Así apareció el ítem 8 al revés.
- **¿Independencia del instrumento (W-01)?** El texto se extrae con pypdf, que es otra librería que la que compone el PDF (typst). Los md5 se verificaron en clones frescos, no en el directorio de trabajo. La mirada humana del PDF sigue faltando y está declarada.
- **¿El 991× y el 4 enriquecidas eran del mismo conjunto?** No, y era el error. Ahora cada número dice sobre qué clases se calcula.
- **¿Algo irreversible?** No. Publicar en Zenodo y mergear quedan para Abraham.

## QA

Aplica la rúbrica de reporte más script de diagnóstico: completitud, ejecutabilidad, documentación y proceso. Testing, seguridad y DevOps quedan N/A, salvo el manejo del token, que se revisó: el script nunca lo imprime ni lo escribe en los recibos.

- **Completitud:** está todo lo que se puede sin el token.
- **Ejecutabilidad:** los dos scripts corrieron en clon fresco.
- **Documentación:** `docs/V2-CIERRE.md` y esta respuesta.
- **Proceso:** cada corrección tiene su medición.
- **Deuda declarada:** la lectura humana de los PDF y la prueba de los metadatos contra la API.

## Cómo sacarle más provecho al laboratorio (opinión de BRAIN, para que Tao la contradiga)

1. **Paper 2 con el control de las salidas** (2026-10-10-005 a 009). Es lo más fuerte que no está publicado: lo que aguanta FWER con los dos nulos (descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes).
2. **La tubería como producto.** El recorrido motivo → nulos S, SL y T → rival clásico → veredicto, con pins y md5, es un compilador de circuitos que se puede correr sobre cada circuito del catálogo, no sólo sobre el escape.
3. **Líneas etiquetadas en Actions.** Es la prueba que la 005 dejó abierta y la única forma en que el cableado por tipos podría pagar.

El pedido completo a Tao está en `docs/auditorias/2026-10-12-pedido-auditoria-tao-laboratorio.md`.
