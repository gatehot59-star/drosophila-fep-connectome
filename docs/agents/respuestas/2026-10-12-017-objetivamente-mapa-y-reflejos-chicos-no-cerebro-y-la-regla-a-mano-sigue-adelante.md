# 017: objetivamente, qué tenemos, hacia dónde vamos, potencial y aplicaciones (12-oct, 22:50 ART)

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21597

**Corregido por la 018:** la regla a mano de la 015 es el mismo diseño de la mosca idealizado, no un control clásico, y la corrida completa dio PAGA LA TAREA DE LA MOSCA (6/6 contra SL y T). Ver `docs/agents/respuestas/2026-10-12-018-paga-la-tarea-de-la-mosca-la-regla-era-la-mosca-idealizada-y-la-v2-quedo-corregida.md`.

## Veredicto primero (F-01)

- [MEDIDO] Lo que funciona: un **mapa** verificado (FlyWire v783, 10/10 predicciones de literatura como aristas, 002) y **reflejos chicos** que andan en simulación desde el día cero (escape de 26 neuronas; 0,98 con la τ líquida plena entrenada, firmado sólo para la semilla 0).
- [MEDIDO] Lo que no: la mosca como **cerebro entrenable**. Con lector entrenado o con líneas etiquetadas, el cableado no le gana a sus barajados ni a lo clásico (003, 004, 005, 012).
- [MEDIDO, parcial 3 de 6 celdas, sin Holm] En la tarea de la mosca de la 015 (cinco acciones, 46 neuronas) el cableado les gana a los 300 SL y a los 300 T en las tres celdas leídas (0/300, p 0,0033 cada una). La regla escrita a mano le gana en dos (p 0,025 y 0,0045) y empata en una.
- [MEDIDO] Paper: la v1.0 de Zenodo tiene la densidad inflada 9,42× por overflow int32 (según el PR #27); la v2.0 está armada pero la 010 le encontró tres inconsistencias internas, y el PR #27 no cambió desde las 14:28 UTC.
- [CONCLUSIÓN] Hoy la mosca sirve para saber **qué detector va a qué acción**, como fuente de diseño verificada contra nulos; no reemplaza a la ingeniería. La aplicación honesta son reflejos visuales baratos para microdrones (esquivar, aterrizar, girar). El activo más valioso a corto plazo es corregir el paper publicado.

## 1. Pedido

22:40 ART: «Objetivamente qué tenemos entre manos, hacia dónde vamos, potencial y aplicaciones».

## 2. Herramientas y máquina

- GitHub MCP, lectura: `docs/agents/CONTEXTO-drosophila-fep.md` (blob `f0f7d74452484ade8924530894ce01f51b00667e`), `00-ENTORNOS-Y-CAPACIDADES.md` (blob `214d6d3859acfc660772460e8665f96042de90cd`), PR #27 (`get`).
- brain-env (MUDH Gateway, servicio `build`): clon de lectura de `main` en `/workspace/tm_2026-10-12/lectura_main`, listado de `docs/agents/respuestas/`, lectura de la 010, la 011 y la 012 del 12-oct, y el log de la corrida en curso de la 015.
- Sin corridas nuevas. Escrituras: este archivo y el Doc espejo. Acción delicada: no.

## 3. Qué se midió (lecturas)

1. `main` en `266b629` (22:33:46 ART). Respuestas del 12-oct: 001 a 016. **El CONTEXTO vivo está al día sólo hasta la 009** (11:58): no cubre la 010 a la 016. Deuda declarada; se paga con el cierre de la 016.
2. PR #27: abierto, head `554f7d99be81f27da331dc5e736b89c5e704e8c2`, `updated_at` 2026-10-12T14:28:10Z. Las tres inconsistencias de la 010 (14:15 ART) siguen sin corregir.
3. Log de la 015 a las 01:45:19 UTC: 3 de 6 celdas, proceso vivo (43:50 de tiempo transcurrido a las 01:42:54 UTC).

## 4. Evidencia cruda

```
$ git clone -q --depth 1 https://github.com/gatehot59-star/drosophila-fep-connectome.git lectura_main && git log -1 --format='%H %cd'
266b629a9ad582b480c5e144de365366c4afd9b4 Mon Oct 12 22:33:46 2026 -0300
$ ls docs/agents/respuestas/ | grep 2026-10-12
2026-10-12-001-arquitectura-por-etapas.md
2026-10-12-002-catalogo-de-circuitos-en-flywire.md
2026-10-12-003-escape-o-aterrizaje-con-dbc3.md
2026-10-12-004-memoria-dura-dbc3-contra-lstm.md
2026-10-12-005-entrada-por-tipos-EN-CURSO.md
2026-10-12-005-entrada-por-tipos.md
2026-10-12-006-en-criollo-la-mosca-sirve-de-mapa-y-de-reflejo-chico-no-de-cerebro-entrenable.md
2026-10-12-007-la-v2-del-paper-esta-lista-y-el-erratum-tenia-errores-sobre-la-v1.md
2026-10-12-008-lineas-etiquetadas-disenadas-sin-correr.md
2026-10-12-009-tao-no-audito-pidio-confirmo-y-el-deposito-lo-espera.md
2026-10-12-010-tao-si-dejo-hallazgos-la-v2-no-se-publica.md
2026-10-12-011-no-es-la-neurona-es-el-recorte-y-la-dcmt-invierte-el-glutamato.md
2026-10-12-012-lineas-etiquetadas-no-pagan-y-auditoria-de-la-auditoria.md
2026-10-12-013-lplc2-responde-a-lo-que-pasa-y-la-mosca-lo-usa-para-esquivar.md
2026-10-12-014-auditoria-de-la-013-lplc1-alimenta-a-dnp06-y-las-barras-piden-aterrizaje.md
2026-10-12-015-tarea-de-la-mosca-sellada-con-dnp06-y-giro-bilateral.md
2026-10-12-016-la-corrida-sellada-de-la-015-esta-en-marcha-sin-tocar.md
```

```
PR #27: state=open merged=false head.sha=554f7d99be81f27da331dc5e736b89c5e704e8c2 updated_at=2026-10-12T14:28:10Z
body: "Zenodo tiene sólo la v1.0, con la densidad inflada 9,42× por overflow int32 y dos resultados titulares que dependen de ella."
```

```
Tue Oct 13 01:45:19 UTC 2026
3
CELDA A=0.0 ruido=0.15 W=0.9005 por_condicion=1.000,1.000,0.725,0.930,0.995,0.895,0.940,0.745,0.985,0.790 umbrales=0.306,0.355,0.246,0.261,0.224,0.262 | SL media=0.6967 max=0.8915 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | T media=0.7192 max=0.8730 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | 871.3 s
RIVAL A=0.0 ruido=0.15 regla_a_mano=0.9195 por_condicion=1.000,1.000,0.885,0.840,0.945,0.925,0.950,0.885,0.960,0.805 | H3 W contra regla 118 contra 156 p=0.0252 -> PEOR | ridge_crudo_entrenado(descriptivo)=0.9935
CELDA A=0.0 ruido=0.45 W=0.8805 por_condicion=1.000,1.000,0.820,0.875,0.905,0.785,0.965,0.705,0.965,0.785 umbrales=0.418,0.491,0.534,0.571,0.522,0.590 | SL media=0.6716 max=0.8305 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | T media=0.7033 max=0.8515 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | 943.4 s
RIVAL A=0.0 ruido=0.45 regla_a_mano=0.8705 por_condicion=1.000,1.000,0.925,0.880,0.915,0.880,0.935,0.405,0.960,0.805 | H3 W contra regla 175 contra 155 p=0.296 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9595
CELDA A=0.3 ruido=0.15 W=0.9125 por_condicion=0.995,0.995,0.730,1.000,1.000,0.895,0.940,0.795,0.985,0.790 umbrales=0.676,0.766,0.246,0.261,0.224,0.262 | SL media=0.6655 max=0.8880 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | T media=0.6734 max=0.8625 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | 884.2 s
RIVAL A=0.3 ruido=0.15 regla_a_mano=0.9325 por_condicion=1.000,1.000,0.720,1.000,1.000,0.925,0.950,0.965,0.960,0.805 | H3 W contra regla 75 contra 115 p=0.00454 -> PEOR | ridge_crudo_entrenado(descriptivo)=0.9935
```

Orden de `por_condicion`: posada (LOOM_LATERAL, LOOM_FRONTAL, PUNTO, BARRA, NADA) | vuelo (LOOM_LATERAL, LOOM_FRONTAL, PUNTO, BARRA, NADA).

## 5. Qué tenemos, objetivamente

### 5.1 Un mapa verificado [MEDIDO]

- **Catálogo (2026-10-12-002):** 10 de 10 predicciones de literatura están en el cableado como aristas de 5 sinapsis o más. Vara baja: existencia, no fuerza ni función.
- **Control de las salidas (2026-10-10-005 a 009, para el Paper 2):** con los dos nulos y FWER aguantan descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes.
- **Fisiología cruzada con el cableado (2026-10-12-013 y 014):** LPLC2 responde a objetos que pasan (Kim 2023) y la mosca lo usa para esquivar en vuelo vía DNp06; la mayor entrada de DNp06 es LPLC1 (1.023 sinapsis, 136 neuronas) y después LPLC2 (1.003, 200). Las barras que pasan de adelante hacia atrás piden aterrizaje (Ache 2019, Nat Neurosci).

### 5.2 Reflejos chicos que funcionan en simulación [MEDIDO]

- **Escape de 26 neuronas (2026-10-11-010 a 015):** sin entrenar gana a S por lateralidad y empata con SL; fuera del techo paga el cableado fino (0,8177 contra SL 0,6819, p 0,0348); con la τ líquida plena entrenada llega a 0,98 y gana a SL en promedio (Mann-Whitney 88%, p 0,0002), pero `VEREDICTO_FIRMA = SOLO LA SEMILLA 0`.
- **Letra chica que pesa:** el reflejo escrito a mano rinde 0,9167 sin entrenar (2026-10-11-011).

### 5.3 Lo que no salió: cerebro entrenable [MEDIDO]

- **003:** la tubería SparseLTC → DBC3 anda de punta a punta, en el techo: empate con LSTM y con SL (p 0,38).
- **004:** ni DBC3 ni LSTM recuerdan 90 pasos (0,658 a 0,672); la máquina de estados les gana (0,7663).
- **005:** con entrada por tipos y lector entrenado, NO PAGA; el ridge crudo gana 6/6 (0,8750 a 0,9906 contra 0,6878 a 0,8628).
- **012:** líneas etiquetadas, NO PAGAN; la regla a mano gana 6/6 (0,6094 a 0,7894 contra 0,3383 a 0,3778).
- **011 (12-oct):** no es la neurona. El motivo de 28 lleva 539 de las 18.191 sinapsis de entrada de sus 4 descendentes (2,96%) y **ninguna de las 7.889 inhibitorias (43,4%)**.
- **DualBrain y DBC3** no se ganaron todavía un lugar en la cadena de la mosca; **SparseLTC** empata 48/48 con el control lineal sobre FlyWire real en `mojo-absoluto` (HC-2).

### 5.4 Lo que está corriendo: la tarea de la mosca (015) [MEDIDO, parcial 3 de 6, sin Holm]

| Celda | W | SL media / máx. | T media / máx. | Regla a mano | H3 W contra regla | Ridge crudo |
|---|---|---|---|---|---|---|
| A 0,0, ruido 0,15 | 0,9005 | 0,6967 / 0,8915 | 0,7192 / 0,8730 | 0,9195 | PEOR, 118 contra 156, p 0,0252 | 0,9935 |
| A 0,0, ruido 0,45 | 0,8805 | 0,6716 / 0,8305 | 0,7033 / 0,8515 | 0,8705 | EMPATE, 175 contra 155, p 0,296 | 0,9595 |
| A 0,3, ruido 0,15 | 0,9125 | 0,6655 / 0,8880 | 0,6734 / 0,8625 | 0,9325 | PEOR, 75 contra 115, p 0,00454 | 0,9935 |

- [MEDIDO] 0 de 300 SL y 0 de 300 T igualan a W en cada celda leída.
- [MEDIDO] La diferencia con la regla está sobre todo en el objeto que pasa (PUNTO): en la celda 1, posada 0,725 contra 0,885 y en vuelo 0,745 contra 0,885; en la celda 3, en vuelo 0,795 contra 0,965. Con ruido 0,45 la regla se cae en el giro en vuelo (0,405) y W aguanta (0,705).
- [CONCLUSIÓN provisoria] Es la primera tarea del 12-oct donde el cableado les gana claro a sus barajados (en la 005 y la 012 no pagaba). Lo que cambió es la tarea (cinco acciones de la mosca real, DNp06 con LPLC1, giro bilateral), no la neurona. El veredicto global es NO MEDIDO hasta `VEREDICTO_GLOBAL` (estimado ~02:35 UTC).

### 5.5 Paper 1 [MEDIDO]

- v1.0 en Zenodo (20-mar): densidad inflada 9,42× por overflow int32 y dos resultados titulares que dependen de ella (cuerpo del PR #27).
- v2.0 en el PR #27: render determinista PASS y erratum cotejado (007); la 010 confirmó tres inconsistencias internas: el «2.4-fold» que con la Tabla 5b da 4,16×; «tres modelos amplifican» con LIF-soft que decae (−0,251); invariancia sin precisar umbral (Tabla 5c con desvíos 0,9 y 0,16). Tabla 8 sin productor archivado. Informe de Tao sin archivar.

## 6. Hacia dónde vamos [CONCLUSIÓN]

1. **Esta noche: leer la 015 entera.** Si W gana a sus nulos pero no a la regla a mano, la lectura es que el cableado tiene información específica de la mosca, pero no mejor que una regla simple escrita con la misma idea. El robot llevaría la regla (inspirada y verificada en la mosca) y el conectoma queda como fuente de diseño.
2. **Paper:** corregir las tres inconsistencias en el PR #27 (son de texto), cotejar el informe de Tao cuando lo archive, merge, token de Zenodo, borrador y publicación. Es lo único con un error público bajo el nombre de Abraham.
3. **Ciencia del cableado:** el falsador que falta es la inhibición (43,4% de la entrada de las descendentes, afuera de todos los motivos probados), con un barajado que respete Dale. Si con inhibición la mosca tampoco le gana a la regla, la pregunta se cierra a este nivel de modelo.
4. **Robot:** el reflejo que gane (mosca o regla) en C99/Q15, con paridad contra numpy, `.text` medido en Actions y cross a ESP32 con el toolchain del taller. Antes, arreglar el dron de `swarm/`, que escapa hacia la amenaza (2026-10-11-007).
5. **Máquinas:** las corridas selladas largas van a **Actions** (11,6× medido en agosto con el mismo script, gratis en repo público, VM limpia que es mejor testigo para W-01). **Corrección a la 016:** para el script sellado, la máquina rápida sin tocar el instrumento era Actions, no Kaggle con GPU; falta resolver cómo baja el parquet (100,8 MB) el workflow. Kaggle sólo con un port a torch verificado contra numpy.

## 7. Potencial [CONCLUSIÓN, opinión]

- **Alto y cercano:** un paper corregido y citable, y un segundo paper con el control de las salidas y resultados negativos honestos (dónde el conectoma paga y dónde no, contra nulos y contra lo clásico).
- **Medio:** un método reusable (sellar antes de correr, SL y T, rival clásico, Holm) para probar circuitos de FlyWire en su función, extensible a MANC y BANC.
- **Bajo hoy:** «el cerebro de la mosca como cerebro de robot»; lo medido no lo sostiene.
- **Plata:** nada de esto es efectivo en semanas. Lo más cercano es reputacional (paper y repo público como portfolio) y una demo de reflejo en placa.

## 8. Aplicaciones [CONCLUSIÓN]

- Microdrones y robots chicos: esquivar lo que se acerca, aterrizar ante lo que se agranda de frente, girar ante lo que pasa; reflejo de pocos KB, latencia baja, sin GPU.
- Antidrones como detección y evasión, no interceptación; antimisiles fuera del roadmap (2026-10-12-001).
- Benchmarks de neuromórfico y docencia: tareas selladas con nulos.
- Fuera de lo medido: cerebro entrenable general y «todas las capacidades son reutilizables».

## 9. Archivos

- Este archivo.
- Doc espejo: https://app.clickup.com/90171457413/docs/2kza6fw5-21597

## 10. NO MEDIDO

- Veredicto global de la 015, sus controles (reproduce, AGNOSTICA, regla mínima) y los brazos descriptivos LPLC1_SILENCIOSA y LPLC4_SILENCIOSA.
- Cualquier cosa en hardware: placa, latencia, energía, bytes en ESP32.
- El informe completo de Tao y las correcciones del PR #27.
- La velocidad de Actions hoy (foto del 26 y 27-ago) y un workflow que baje el parquet.
- El valor de producto o de mercado: opinión.
- El CONTEXTO vivo sigue en la 009.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| La 015 parcial gana a sus nulos | `igualan=0/300` y `p_sup` del propio script en cada CELDA | Sí: en la 005 y la 012 el mismo tipo de línea dio 283 a 300 de 300 |
| La regla a mano gana en 2 de 3 | McNemar del propio script (H3) | Sí: en la celda 2 dio EMPATE |
| El PR #27 no cambió | `updated_at` y head del PR | Sí: un commit nuevo cambia los dos |
| El CONTEXTO está vencido | encabezado del archivo contra la lista de respuestas | Sí: si nombrara la 010 a la 016 |
| Mapa, reflejos y cerebro entrenable | veredictos de las respuestas citadas, leídos en el repo | Sí: cada uno tiene su nulo y su rival |
| Potencial y aplicaciones | ninguno | No: es opinión, marcada como tal |

--- METODO PROMETEO ---
Acción delicada: no
Máquina: brain-env (MUDH Gateway, build: clon de lectura, log de la 015) y GitHub MCP (lecturas y este commit)
Artefactos: docs/agents/respuestas/2026-10-12-017-objetivamente-mapa-y-reflejos-chicos-no-cerebro-y-la-regla-a-mano-sigue-adelante.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21597
