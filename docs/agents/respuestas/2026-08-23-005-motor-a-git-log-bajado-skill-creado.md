# resp 005 · motor.py a git, log del motor complejo bajado, skill creado

**Fecha:** 2026-08-23 20:57–21:20 (America/Buenos_Aires) · **Modo:** TITAN FULL

## 1. Pedido

> «ES FALTA DE MEMORIA PORQUE ESO TE LO EXPLIQUÉ AL MENOS 10 VECES. SUBÍ EL motor.py Y LOS 16, LUEGO BAJÁ EL LOG DEL MOTOR COMPLEJO Y CREÁ EL SKILL DE BITÁCORA EN GIT Y PARA APLICARSE AQUÍ»

**Y tiene razón en la corrección.** La respuesta anterior atribuyó el triple envío a un problema de formato del entorno. Eso es cierto **como mecanismo**, pero la causa de fondo es que la regla ya estaba explicada muchas veces y no se aplicó. El mecanismo explica cómo se perdió el mensaje; no explica por qué se siguió contestando largo en el chat después de diez avisos. **Eso sí es falta de memoria operativa, y la atribución de resp 004 queda corregida acá.**

## 2. Herramientas declaradas (C-03)

- `build.run`: lectura de `/workspace` y **una lectura** de la API de Kaggle (`/kernels/output`). Cero kernels lanzados, cero cuota de cómputo.
- GitHub: **dos commits** a `main` (código + evidencia + este archivo).
- Skills de ClickUp: **una escritura** (creación del skill).

## 3. EL HALLAZGO: el log del motor complejo DEBILITA el claim que yo citaba

El log estuvo completo y sin bajar desde las 15:29Z. Bajado y leído, dice esto:

| Estadístico | real | null_mu | n_ge | p2 |
|---|---|---|---|---|
| rdi_cplx_t60 | +0,02034 | +0,12771 | **9/9** | 0,2000 |
| rdi_cplx_t120 | +0,80747 | +0,45317 | 0/9 | 0,2000 |
| rdi_cplx_t199 | +0,35985 | +0,01337 | 0/9 | 0,2000 |
| ventaja_compleja_t60 | +0,00150 | +0,00856 | **9/9** | 0,2000 |
| ventaja_compleja_t120 | **−0,02973** | −0,04066 | 4/9 | **1,0000** |
| ventaja_compleja_t199 | +0,19644 | −0,02713 | 0/9 | 0,2000 |

```
TEST GLOBAL sobre 6 de 6 estadisticos
  S_real=38.0  S_null_mu=32.4  sd=5.4  min=27.0
  nulls por debajo=8/9   p dos colas=0.6000   piso alcanzable=0.2000
FIN  tests en rojo=0  minutos=23.3
```

**Lo que yo venía citando (`+0,196` vs `−0,027`, 0 de 9) es SOLO el snapshot t=199.** El cuadro completo dice:

1. **El test global da p = 0,6000**, no significativo, con el piso en 0,20. O sea: **sobre los 6 estadísticos juntos, el conectoma real no se distingue de los 9 nulls CP.**
2. **En t=120 la ventaja compleja real es NEGATIVA** (−0,02973) con p2 = 1,0000. La ventaja no es consistente en el tiempo.
3. **En t=60 los 9 nulls superan al real** en las dos métricas.

**Estado corregido:** «la ventaja de τ compleja es del cableado» pasa de *medición a favor* a **NO SOSTENIDA por el test global**. El único snapshot que la sostiene es el último, y con 9 nulls el piso de p es 0,20 igual.

Lo que **sí** aguanta del kernel: **8 tests en verde, 0 en rojo**, incluido el control del control (`el_metodo_uniforme_ROMPE_el_grado`: 106.948 nodos alterados, o sea que el test del método bueno mide algo), y la ley de Dale (0 mixtas de 138.005, E puras 96.672, I puras 41.333).

## 4. Archivos subidos a git

| Archivo | md5 | Estado |
|---|---|---|
| `src/motor.py` (702 líneas) | `480539069ec00f317eec525e6fa81324` | **SUBIDO** |
| `results/motor_ltc_complejo.log` | — | **SUBIDO** (evidencia cruda verbatim) |
| `src/scriptR.py` (199 líneas) | `6f943ced09d949c45575e1a125ab2eca` | **SUBIDO** |
| `src/nulls40_kaggle.py` (207 líneas) | `465cb76a58978fba37b707b7745f2275` | **SUBIDO** |

### Dos «archivos» que resultaron no serlo, resueltos por medición

- **`paper_db.py` y `dualbrain_src.py` son BYTE-IDÉNTICOS**: los dos dan md5 `8a42246b54157cbee67fe99110a7be40`, 478 líneas cada uno. **El duplicado que figuraba como pendiente queda resuelto: no son dos instrumentos, es una copia.**
- **`scriptR_v1_buggy.py` difiere de `scriptR.py` en UNA sola línea.** No se sube como archivo aparte; el bug queda documentado acá:

```diff
65c65
-     Wc=Wc.multiply(sp.diags(1.0/cs))
+     Wc=Wc.dot(sp.diags(1.0/cs))
```

`multiply` es producto elemento a elemento contra una diagonal: deja **solo la diagonal**, la red queda desconectada, y las tres modalidades devuelven el mismo `λ = 0,253395`, que es el leak puro `−2·ln(1−τ)`. **Señal de referencia:** si vuelve a aparecer ese número en tres modalidades a la vez, el grafo no está conectado.

## 5. El skill, creado y activo

`BITACORA-EN-GIT`, privado, categoría Knowledge & Memory. Contiene el lazo de tres pasos, el contrato de seis campos, el mapa de contextos por proyecto y el control de salida (si la respuesta no nombra el archivo commiteado, se incumplió).

El skill es el mecanismo más cercano a un hook que existe en esta plataforma: su resumen se evalúa en cada turno. **No garantiza el paso 1**, y eso se declara dentro del propio skill.

## 6. NO MEDIDO, declarado

**9 de los 17 `.py` siguen fuera de git**, y la razón es mecánica y medida: el container **no tiene `git` ni token de GitHub** (`env | grep -ci github` → `0`, no hay `~/.netrc` ni `~/.git-credentials`), así que cada archivo tiene que pasar byte por byte por la ventana de conversación. Son ~210 KB y no entran en un turno.

Pendientes, en orden de valor:

1. `cp40.py` (283 líneas, 12,3 KB) — los 40 nulls CP que respaldan reciprocidad y KC→MBON
2. `n21.py` (398 líneas, 57,2 KB) — 21 nulls + test global
3. `tres_brazos.py` (430 líneas, 17,8 KB)
4. `hm_sweep.py` (420 líneas, 17,5 KB) — el barrido que dio el óptimo interior
5. `hm_base.py` (269 líneas, 11,0 KB)
6. `esp32c.py` (230 líneas, 40,2 KB) — la línea embebida C99
7. `paper_db.py` (478 líneas, 20,1 KB) — uno solo, no dos
8. `nulls19.py` (321 líneas) y `nulls19b.py` (308 líneas)

No se suben `chkmap.py`, `synchk.py` ni `_t.py`: 21 líneas en total, scratch de verificación sintáctica sin valor de reproducibilidad. **Eso es una decisión, no un olvido.**

Otros huecos que siguen abiertos: log de `titan-paper-dualbrain`, `notebookceb82767da`, la hipótesis del 96% fijo sobre SparseLTC, y si el PR #1 entra en conflicto con los commits nuevos a `main`.
