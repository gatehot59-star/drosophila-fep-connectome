# REA y Ghidra operativos por consola, con advertencias globales pendientes

Fecha: 2026-10-14, ART (UTC-3). Revision de la instalacion dejada el 13 de octubre. Repo de contexto leido en `3576311e2569ae5cdeebab68fac75f75d328af87`.

## Pedido

«REVISA COMO QUEDO INSTALADO REA Y GHIDRA».

## Veredicto

**CONFIRMADO / PASS para este camino CLI:** REA 6.4.0, Ghidra 12.1.4 y Temurin JDK 21.0.12.1+1 estan instalados en brain-env y funcionan juntos. REA abrio el binario propio sin simbolos, reporto 29 procedimientos y devolvio pseudocodigo de la funcion principal mediante el proveedor Ghidra, no mediante la inspeccion generica de artefactos.

**CONFIRMADO / FAIL global:** `rea doctor` devuelve exit 1, `healthy: false` y `environment_healthy: false`. Sus cuatro avisos negativos son Debian 13 fuera de la lista de hosts soportados, Hopper ausente, IDA sin registrar e identidad del skill sin instalar. No corresponde convertir este resultado en «todo verde».

**CONFIRMADO / PASS del alcance seleccionado:** `rea doctor --provider ghidra --target /workspace/rea/smoke/caja.stripped` devuelve exit 0 y `healthy: true`, manteniendo `environment_healthy: false`. La ausencia de los motores alternativos no bloqueo la prueba real con Ghidra.

**No hubo reparacion ni reinstalacion.** No se ejecuto `rea setup`, no se modificaron configuraciones de agentes y no se suprimio la advertencia del host.

## Como quedo instalado

- Lanzador: `/workspace/rea/rea`.
- Paquete fijado: `rea-agents@6.4.0`, en `/workspace/rea/node_modules`.
- HOME del lanzador: `/workspace/rea/home`.
- JDK: `/workspace/rea/engines/jdk-21.0.12.1+1`.
- Ghidra: `/workspace/rea/engines/ghidra_12.1.4_PUBLIC`.
- El lanzador usa `env -i` con `JAVA_HOME`, `GHIDRA_INSTALL_DIR` y PATH acotado. El anterior quedo en `/workspace/rea/rea.sin-motor`.

Un HOME separado no es una frontera de permisos del sistema. No se afirma aislamiento frente a credenciales accesibles al mismo usuario.

## El registro que faltaba leer

`install.log` quedo en la descarga inicial. El cierre real esta en `/workspace/rea/engines/install2.log`, del instalador paralelo posterior: registra finalizacion a `2026-10-14T02:11:59Z`, es decir, **13-oct 23:11:59 ART**, antes de la estimacion de las 00:20 del documento anterior.

Ese registro historico contiene `JDK_SHA_OK`, `TAR_OK`, `GHIDRA_SHA_OK` y `UNZIP_OK`; la medicion de hoy no recalcula los archivos comprimidos originales, que el instalador elimino. No confundir un log historico con una nueva verificacion de integridad de toda la instalacion.

## Prueba funcional

Objetivo: `/workspace/rea/smoke/caja.stripped`, ELF x86-64 de 14.488 bytes. SHA-256: `51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e`.

1. `inspect` con proveedor Ghidra: exit 0 en 50,48 s; 31 segmentos, 29 procedimientos y 43 cadenas.
2. `decompile` sobre `0x101070`: exit 0 en 117,76 s; proveedor Ghidra 12.1.4 y operacion `procedure_pseudo_code`.
3. Pseudocodigo obtenido: longitud 9, prefijo `MDH-`, cinco digitos y suma `0x15` (21).
4. Ejecucion de la caja: `MDH-90093` abre, exit 0; `MDH-90092` y `MDH-90A93` cierran, exit 1.
5. Analizador sobre archivo inexistente: `target_unavailable`, exit 1.

Los SHA-256 de la caja y del lanzador coinciden antes y despues. El pseudocodigo no es la fuente original: la funcion aparece como `FUN_00101070`.

**No es una prueba ciega:** la regla y el codigo fuente de la caja ya estaban en el recibo previo leido al abrir el turno. Esta prueba confirma instalacion, ejecucion del proveedor y coherencia con un caso conocido; no mide descubrimiento autonomo ni calidad en aplicaciones grandes.

## Que no se habia medido y si importaba

El doctor de instalacion verificaba rutas, versiones y compatibilidad de componentes, pero eso no demostraba que la JVM pudiera abrir un proyecto, importar el ELF y ejecutar el descompilador nativo en esta maquina. La corrida real de `inspect` y `decompile` cierra ese hueco para esta caja.

## Lo buscado sin encontrar una falla en el camino probado

Se comprobaron version de REA, arranque de JDK 21, configuracion del lanzador, disponibilidad del proveedor Ghidra, importacion del ELF, descompilacion de una funcion, coherencia con tres ejecuciones de la caja, rechazo de objetivo inexistente y estabilidad de hashes. No aparecio un fallo en ese camino. El rojo global sigue presente y declarado.

## NO MEDIDO

- Interfaz grafica de Ghidra.
- Registro y uso de REA dentro de un cliente/agente.
- Otros formatos, arquitecturas o binarios grandes.
- CVE actuales, firma GPG del JDK y aislamiento de credenciales.
- Integridad completa actual de todos los archivos instalados frente a los paquetes originales.

No se propone instalar Hopper o IDA solo para cambiar el color del doctor. No se autoriza ni se ejecuta `setup` como parte de esta revision.

## Herramientas y maquina

Lectura real de inventario, metodo y ultima respuesta en GitHub; documentos previos de REA/Ghidra; servicio sqlite (sin mensajes pendientes para BRAIN ni estado especifico de REA/Ghidra); servicio build de brain-env mediante Python/subprocess y shell. Se capturaron argv, stdout, stderr y codigos de salida. Se crearon temporales y un snapshot diagnostico. Los procesos de analisis terminaron. No se lanzaron experimentos en Actions o Kaggle ni se gasto runtime de otro agente.

## Evidencia y artefactos

- [Bitacora 016 con comandos y evidencia cruda](../agents/respuestas/2026-10-14-016-rea-ghidra-instalados-y-probados.md).
- [Doc de ClickUp](https://app.clickup.com/90171457413/docs/2kza6fw5-22377), ubicado en `Space > REA y Ghidra funcionan juntos por consola: la caja se descompila; el chequeo general sigue con avisos (14-oct, 016)`.
- Se agregan esta auditoria y la bitacora, sin modificar documentacion anterior ni codigo de producto.

## QA del informe

37/40 = 92,5/100. Es la calidad de este informe, no una nota de seguridad de REA o Ghidra.

- Completitud 14/15: evidencia cruda, secciones A a H de la bitacora; no se revalidan los paquetes originales.
- Razonamiento 9/10: separa doctor global, alcance Ghidra y ejecucion real; reconoce el limite de un unico binario conocido.
- Documentacion 9/10: rutas, versiones, comandos, hashes y limites; el inventario general anterior no se actualiza.
- Proceso 5/5: proveedor real, exit codes y positivos/negativos; evidencia persistente y verificacion posterior de los archivos publicados.

60 puntos N/A: ejecutabilidad de codigo nuevo (15), seguridad integral (15), cobertura de suite de producto (15), DevOps (10), innovacion (5). No hay nueva implementacion ni una auditoria integral de seguridad.

```text
--- METODO TITAN ---
Accion delicada: NO. Diagnostico sobre binario propio y documentos nuevos.
Modo aplicado: TITAN FULL, auditoria acotada.
Rubrica: 37/40 -> 92,5/100.
N/A declarados: 60 puntos, detallados arriba.
Review externo: no solicitado; sin PR ni codigo de producto.
Instrumento: REA/Ghidra mediante subprocess y shell; evidencia cruda en bitacora 016.
Maquina: brain-env, Debian 13 x86-64, uid 1000, 2 CPU.
Artefactos: esta auditoria + docs/agents/respuestas/2026-10-14-016-rea-ghidra-instalados-y-probados.md + https://app.clickup.com/90171457413/docs/2kza6fw5-22377
```
