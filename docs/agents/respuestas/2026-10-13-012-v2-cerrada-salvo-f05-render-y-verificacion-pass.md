# 2026-10-13-012 · La v2 del Paper 1 quedó cerrada salvo F05: render y verificación PASS desde 1f4a2e0, y el verificador da rojo con el PDF viejo

## Veredicto

- **[MEDIDO] Render PASS desde `1f4a2e0`** (F01, F06 y F07 aplicados):
  - manuscrito: 18 páginas, `a22515e9…`, 330.511 B, fuente `2fa575c4…`;
  - erratum: 15 páginas, `05052e6e…`, sin cambios, fuente `f2ad0507…`;
  - las dos compilaciones son deterministas y pasan los 19 de 19 chequeos de texto.
- **[MEDIDO] Verificación del depósito PASS** en un clon fresco de `e81a903`, con el json nuevo `55f3ec63…` apuntando a `deposito_013`.
  - **Control negativo:** con el mismo json apuntando al PDF viejo (`d353cf0f…`) da `MD5_DISTINTO` y FAIL.
- **[MEDIDO] Los arreglos de la auditoría de Tao están en el PDF, no sólo en el Markdown** (pypdf, viejo → nuevo):
  - «Sufficient» 1 → 0 (F06);
  - «1/6» 0 → 2 (F06);
  - «138,140» 0 → 1 (F07);
  - «in-degree» 8 → 7 (F01).
- **[MEDIDO] F05 sigue abierto.**
  - «+14,8» aparece 10 veces en el manuscrito: el resumen y las conclusiones lo usan como firme («survives the community-preserving control»).
  - Es la Tabla 8, que no se reprodujo, y tiene el piso de p = 1/6 con 5 realizaciones.
- **[CONCLUSIÓN] Lo técnico de la v2 está listo.** Antes de mergear y depositar falta decidir F05; después, el merge del PR #27 y el token de Zenodo, que son de Abraham.

## Pedido

ClickKit `cerrar_v2_015` (13-oct, 17:11): cerrar el render y la verificación de la v2.

## Herramientas y máquina

- **brain-env:**
  - clon de `titan/v2-cierre-2026-10-12` en `1f4a2e0`;
  - `python3 tools/v2/render_v2.py /workspace/v2cierre_2026-10-13/deposito_013` (pandoc 3.10.2, typst 0.15.0);
  - `python3 tools/zenodo/depositar_v2.py --verificar`, con su control negativo;
  - control de texto con pypdf (`chk.py`, `ddbfb854…`);
  - clon fresco de `e81a903`;
  - prueba del parche del CONTEXTO.
- **GitHub MCP:**
  - `push_files` a la rama del PR #27: json, `render-v2.0.log` y `verificar-v2.0.log`, en el commit `e81a903`;
  - este commit en main.
- **Lo que no se hizo:** ni Zenodo, ni token, ni merge.

## Evidencia cruda

```
1f4a2e038916a1fcef989cec9582f496debc4dcb (HEAD de titan/v2-cierre-2026-10-12 antes de este turno)
ENTORNO pandoc 3.10.2 | typst 0.15.0
FUENTE docs/v2/paper1-v2.0.md 56298 2fa575c41926fdc790cecbb5965ba2a1
PDF Mendieta2026_Paper1_v2.0.pdf 330511 a22515e9e2e7bb02e8d3fd824217dfc7 paginas 18 determinista True
FUENTE docs/ERRATUM.md 41121 f2ad05072086258a8ce76b9d650ed26d
PDF Mendieta2026_Paper1_Erratum_v1.0.pdf 191172 05052e6e7e0dd79cee584c9d285b1b93 paginas 15 determinista True
VEREDICTO_RENDER PASS
RC=0
# clon fresco de e81a903
55f3ec630c7ace5c15211d0ccc779733  docs/v2/archivos-deposito-v2.0.json
644de95c50d2d1954034f3d1fd755e92  docs/v2/render-v2.0.log
74d8649f69876c629ae8a28bb7227fd0  docs/v2/verificar-v2.0.log
ARCHIVO Mendieta2026_Paper1_v2.0.pdf 330511 a22515e9e2e7bb02e8d3fd824217dfc7 OK
ARCHIVO Mendieta2026_Paper1_Erratum_v1.0.pdf 191172 05052e6e7e0dd79cee584c9d285b1b93 OK
VEREDICTO_VERIFICAR PASS
# control negativo (json apuntando a deposito_018)
ARCHIVO Mendieta2026_Paper1_v2.0.pdf 327479 d353cf0fd05e9e5637be2bccca7bc98e MD5_DISTINTO
VEREDICTO_VERIFICAR FAIL
# texto (pypdf), viejo = deposito_018, nuevo = deposito_013
Sufficient   viejo=1 nuevo=0 | md=0 erratum=0
138,140      viejo=0 nuevo=1 | md=1 erratum=0
1/6          viejo=0 nuevo=2 | md=2 erratum=0
in-degree    viejo=8 nuevo=7 | md=7 erratum=2
14.8         viejo=9 nuevo=10 | md=10 erratum=0
MD 14.8 :: ... cosine RDI rises from 0.63 to 0.83 post-stimulus, an effect that survives the community-preserving control (*Z*~CP~ = +14.8σ) ...
MD 14.8 :: ... ttainable permutation *p*-value, (*r* + 1)/(*N* + 1), is 1/6 ≈ 0.17, so this test cannot reach conventional significance on its own; *Z* = +14.8σ rests on a normal approximation whose variance is estimated from five values.
# parche del CONTEXTO (copia en brain-env)
1f47800a3bbcbb30863a5825a1315cd1  parche.py | md5 antes acf55ada… -> despues ca42f33a… PARCHE OK
```

## F05: las dos salidas

- **Suavizar (recomendado).** En el resumen, §4.1 y las conclusiones, cambiar «survives the community-preserving control (+14,8σ)» por una frase descriptiva: observado contra 5 realizaciones CP, con Z por aproximación normal y p mínima 1/6, sin reproducir en esta versión. Se agrega un ítem a «Changes from version 1.0». Es un parche de texto, con render y verificación de nuevo. No necesita correr nada.
- **Reproducir la Tabla 8.** Requiere el script de la dinámica RDI con nulos CP y una corrida nueva con muchas más realizaciones. No se sabe si el script está completo (NO MEDIDO). Demora el depósito.

## Archivos

- **Rama del PR #27 (`e81a903`):**
  - `docs/v2/archivos-deposito-v2.0.json`;
  - `docs/v2/render-v2.0.log`;
  - `docs/v2/verificar-v2.0.log`.
- **main:**
  - este archivo;
  - `tools/contexto/actualizar_contexto_2026-10-13-012.py` (`1f47800a…`);
  - `.github/workflows/contexto-2026-10-13-012.yml`.
- **PDF:** son binarios derivados, no van al repo. Están en `/workspace/v2cierre_2026-10-13/deposito_013/` de brain-env, referenciados por md5 en el json.

## NO MEDIDO

- **F05**, con cualquiera de las dos salidas.
- **El render en Actions.** Sólo corrió en brain-env; la 018 ya había dado md5 iguales en las dos máquinas con la cadena anterior.
- **El erratum.** No se tocaron sus entradas por F06; el texto del erratum no contiene «Sufficient».
- **Merge, token y depósito.**

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El PDF del depósito es el de `1f4a2e0` | `--verificar` con md5 | Sí: con el PDF viejo dio FAIL |
| Los arreglos de Tao están en el PDF | conteo pypdf viejo contra nuevo | Sí: podía dar 0 → 0 |
| El render es determinista | dos compilaciones del script | Sí: lo chequea y sale 1 |

```
--- METODO PROMETEO ---
Accion delicada: no (sin merge, sin token, sin deposito)
Maquina: brain-env (render, verificacion, pypdf)
Artefactos: docs/agents/respuestas/2026-10-13-012-v2-cerrada-salvo-f05-render-y-verificacion-pass.md + Doc de ClickUp 2026-10-13-012
```
