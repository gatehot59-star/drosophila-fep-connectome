# Pedido de auditoría a TITÁN Tao · el laboratorio de circuitos de la mosca

**Pide:** Abraham, 2026-10-12 11:14: «pide a tao que audite todo el laboratorio creado, las pruebas, demostraciones, hipótesis, conclusiones. creo que podemos sacarle más provecho a este laboratorio que genera circuitos de la mosca».
**Redacta:** BRAIN, en la respuesta 2026-10-12-007.
**Estado:** **enviado** el 2026-10-12 a las 11:36 como tarea https://app.clickup.com/t/86e3p74xa (lista Pipeline TITAN), con mención a Tao en el comentario https://app.clickup.com/t/86e3p74xa?comment=90170261435881. Asignar agentes a tareas está apagado en el workspace, así que el disparador es la mención.

## 0. Repo y lectura previa

- **El repo de esta auditoría es `gatehot59-star/drosophila-fep-connectome`, no `mudh-mobile`.**
- Tu carta `docs/agents/AGENT-TAO.md` sigue en `mudh-mobile`: leela ahí como siempre y anotá esta auditoría en ella al cerrar.
- **Registrá el HEAD de `main`** que auditás. Este archivo entró en el commit de la respuesta 2026-10-12-007 (`47d940e`).
- **Leé primero:**
  - `docs/agents/CONTEXTO-drosophila-fep.md` (estado vivo);
  - `docs/agents/respuestas/` (append-only, del 2026-10-10-002 al 2026-10-12-007);
  - `00-ENTORNOS-Y-CAPACIDADES.md` (las tres máquinas; es una foto del 26 y 27 de agosto).

## 1. Qué auditar: el laboratorio entero

| # | Bloque | Dónde | Qué afirma |
|---|---|---|---|
| 1 | Paper 1, v2.0 | PR #27, rama `titan/v2-cierre-2026-10-12` | erratum revisado contra el texto de la v1.0; manuscrito v2.0; render determinista |
| 2 | Tabla 7 y control de las salidas | PR #26, rama `titan/tabla7-reconstruida-2026-10-10`, respuestas 2026-10-10-002 a 009 | Tabla 7 8/8 y 8,6; quién controla las salidas; BY, Holm y max-T |
| 3 | Nulo por circuito | respuesta 2026-10-11-003 | FAIL de instrumento; lectura preliminar sin firmar |
| 4 | Brazo S y escape | respuestas 2026-10-11-007 a 016; ramas `titan/brazo-s-recurrente-2026-10-11`, `titan/escape-motivo-2026-10-11` y `titan/swarm-lazo-cerrado-2026-10-11` | la mosca gana por lateralidad (010), por cableado fino (011); la líquida plena contra su control (012 a 015) |
| 5 | Circuitos y DBC3 | respuestas 2026-10-12-001 a 006; ramas `titan/catalogo-circuitos-2026-10-12`, `titan/escape-aterrizaje-2026-10-12`, `titan/memoria-dura-2026-10-12` y `titan/entrada-por-tipos-2026-10-12` | catálogo 10/10; DBC3 en el techo; nadie aprende 90 pasos; entrada por tipos NO PAGA |
| 6 | Expediente de agosto | rama `titan/materializacion-h4-guard-2026-10-02` (respuestas 063 a 124) | null anatómico, LC6→GF, sel_post, 39 nulos |
| 7 | H4 | `main` | 34 contratos; generalización intra-animal p = 0,623 |

## 2. Cómo

- **Auditá contra el repo y los logs crudos**, no contra los Docs de ClickUp ni contra los recibos de BRAIN.
- **Por cada afirmación:**
  - (a) ¿el instrumento podía dar rojo? ¿tuvo control negativo y qué dio?
  - (b) ¿los brazos de cada A/B son funciones distintas?
  - (c) ¿el md5 sellado en el pre-registro coincide con el script que dice el log?
  - (d) ¿el log commiteado dice lo que la respuesta dice?
  - (e) ¿el sujeto es el que se nombra?
- **Recomputá en tu sandbox** lo que no necesite el parquet de 100 MB y declará qué recomputaste. Por ejemplo:
  - las correcciones múltiples desde los p de los logs;
  - la Tabla 5 desde sus conteos;
  - las p de permutación desde los conteos de nulos.
- **Tres estados:** PASS, FAIL, NO MEDIDO.
- **Sólo auditás.** No modificás archivos del laboratorio.
  - Escribí `docs/auditorias/2026-10-12-tao-auditoria-del-laboratorio.md` en una rama `titan/auditoria-tao-laboratorio-2026-10-12`.
  - Abrí un PR sin merge, con el review automático.
  - Dejá un Doc en el Space de ClickUp.

## 3. Qué entregar

1. **Una tabla por afirmación** con estas columnas: respuesta, afirmación, instrumento, ¿podía dar rojo?, recomputado, veredicto y evidencia (archivo y línea, o SHA).
2. **Lo que hay que retirar o angostar.**
3. **Cómo sacarle más provecho al laboratorio**, que es lo que pide Abraham: hasta cinco propuestas priorizadas. Cada una con su falsador, su costo y la máquina en que corre.
4. **Scorecard TITAN de tipo auditoría**, con los N/A declarados.

## 4. Hipótesis de BRAIN, para que las contradigas

- **(2026-10-12-006)** La mosca sirve de mapa y de reflejo chico y fijo. No sirve, hasta ahora, de cerebro entrenable mejor que lo clásico.
- **Lo más sólido:**
  - la v2.0 corregida;
  - el catálogo, como existencia de aristas;
  - el escape a lazo cerrado (010 y 011);
  - la líquida plena contra su control de parámetros (013 y 014).
- **Lo más flojo:**
  - la firma de la 014 vale sólo para la semilla 0 (015);
  - la 003, la 004 y la 005: en el techo, nadie aprende, no paga;
  - toda la robótica es simulación, sin hardware.
- **Dónde creo que hay más provecho:**
  1. el Paper 2 con el control de las salidas;
  2. la tubería motivo → nulos S, SL y T → rival clásico → veredicto, como compilador de circuitos sobre todo el catálogo;
  3. líneas etiquetadas en Actions;
  4. el cordón en BANC para la etapa motora.

## 5. Límites conocidos

- **Tu sandbox no es brain-env.** No tenés el parquet ni torch salvo que los instales y lo midas. No tenemos ese gateway en común.
- **No mergear, no borrar, no tocar `main`.**
- **Si algo necesita una máquina que no tenés**, decilo y dejá la verificación nombrada para BRAIN (brain-env) o para Actions.
