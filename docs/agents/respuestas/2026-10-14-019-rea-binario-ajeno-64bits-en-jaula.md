# 2026-10-14-019: el binario ajeno de 64 bits corrio en jaula y confirmo 43 escrituras previstas

## 1. Pedido

«Proba el binario de 64 bits en una jaula aislada».

## Veredicto derivado

**PASS.** El ELF de terceros se ejecuto en una jaula con aislamiento comprobado y termino con codigo 0. La segunda corrida, observada, registro **43/43 llamadas fputc iguales a la prediccion hecha antes de ejecutar**. Los caracteres ordenados por posicion reconstruyen:

```text
SharifCTF{b70c59275fcfa8aebf2d5911223c6589}
```

La jaula paso **15/15 controles**. El control fuera de la jaula fue rechazado, exit 42. El binario y el archivo artificial de control externo no cambiaron. No se ejecuto este programa en brain-env, no se modifico REA/Ghidra ni se tocaron configuraciones de agentes.

## 2. Herramientas, maquina y sujeto exacto

Analisis previo: REA 6.4.0 y Ghidra 12.1.4 en brain-env, sobre el ELF `getit` de Sharif CTF archivado por angr. Se descargo el binario, sin abrir fuentes ni `solve.py`.

[Origen fijado a commit](https://github.com/angr/angr-doc/blob/bf380700f2baa092c2970a2dceb0eb2793bd9837/examples/sharif7_rev50/getit).

- 9.449 bytes; ELF x86-64.
- Git blob SHA-1: `9b24e330f47bdb725dd73254c7c4972445acc6b6`.
- SHA-256: `b350963759f5a6c7d516e340e8114a7b14824ac8665063d276a5672be61a9ba5`.

Ejecucion: sandbox de ClickUp, kernel `6.1.158+`, distinto de brain-env. Este sandbox no tiene acceso a internet; se agregaron namespaces de usuario/montajes/red/PID, chroot minimo, raiz de solo lectura, temporal privado noexec, cero capacidades, no_new_privs y seccomp. Se compilaron los controles locales con GCC, no el binario objetivo. Sin Actions, Kaggle ni runtime de otro agente.

Se leyo el historial actual de respuestas antes de publicar; la respuesta previa en main era la 018, commit `effce96422ac7739bb29d3d6b822170100f5d87a`. No se modifica el estado de los experimentos del conectoma de otros turnos.

## 3. Mediciones

### Prediccion anterior al objetivo

El pseudocodigo de REA y los datos del propio ELF llevaron a una prediccion guardada el **14-oct 17:34:28 ART** (`2026-10-14T20:34:28.769839+00:00`). SHA-256 del archivo original:

```text
bad58cf3ebff01c755f4f694f3d92d062da8ec8da2896142bbcbff76a502705b
```

Predijo salida 0, consola vacia, 43 escrituras en posiciones permutadas, sobrescritura con asteriscos y borrado de `/tmp/flag.txt`. El hash de esa prediccion seguia igual al ejecutar a las **17:44:01 ART**. Es un registro local previo, no una preregistracion publica independiente.

### Aislamiento

Antes del objetivo: 15 controles verdes, exit 0. Probaron archivo externo, escape por symlink, escritura del binario, archivo 0666 protegido por montaje read-only, temporal escribible, ausencia de /proc hacia el host, sockets IP/Unix, remount, chroot, unshare, ptrace, fork, no_new_privs y capacidades vacias. Los cuatro namespaces difieren de los del proceso llamador.

El control externo leyo un archivo artificial y creo un socket, y devolvio REJECT/42. No realizo ninguna conexion de red; crear un socket no significa que el sandbox tenga internet.

Limites aplicados: CPU 2 s, espacio de direcciones 128 MiB, archivo 1 MiB, 16 descriptores, core 0 y creacion de procesos bloqueada.

### Ejecucion original

Sin LD_PRELOAD ni modificacion del ELF: exit 0, stdout vacio, stderr del objetivo vacio, archivo temporal ausente al finalizar. El comando completo con preparacion de jaula duro 0,0518 s; no se presenta como benchmark del objetivo solo.

### Ejecucion observada

Mismo SHA-256, exit 0, salida vacia. Un observador fputc que no contiene la cadena esperada registro **43 eventos**, coincidentes en orden, posicion, byte y retorno. Ordenarlos por posicion recupera exactamente la cadena anterior.

En esta segunda corrida se precreo un archivo vacio manteniendo un descriptor abierto para leer su inode despues del unlink: **43 asteriscos y salto de linea**, contador de enlaces **0**, ruta ausente. Esta preparacion y LD_PRELOAD se declaran como instrumentacion; por eso se hizo por separado la corrida original.

Cambiar un byte de la traza produjo discrepancia en el comparador. No se juzgo el resultado por el codigo de salida solamente.

## 4. Evidencia cruda

[Comandos, stdout, stderr, prediccion, 43 eventos y codigo completo de los instrumentos](../evidencia/2026-10-14-019-rea-jaula-64bits.md).

Los dos gates inicialmente rojos se conservan: primero se consulto un sysfs heredado en vez de las interfaces del namespace de red actual; luego se esperaba EROFS sobre un archivo 0555 que correctamente devolvio EACCES. Se corrigio el instrumento con consulta real de interfaces y un control separado de archivo 0666 sobre el montaje read-only. **El binario ajeno no corrio en ninguno de esos intentos.**

## 5. Archivos y Doc

- Este archivo de respuesta.
- `docs/agents/evidencia/2026-10-14-019-rea-jaula-64bits.md`, en este mismo commit.
- [Doc de ClickUp](https://app.clickup.com/90171457413/docs/2kza6fw5-22457), ruta `Space > REA: binario ajeno confirmado en jaula (14-oct, 019)`.

Solo documentacion y evidencia textual en main; no binarios derivados ni cambios de producto.

## 6. NO MEDIDO

No se certifico ausencia de malware, resistencia a exploits del kernel ni CVE actuales. La jaula comparte el kernel del sandbox: no es una VM con kernel independiente. No demuestra rendimiento o correccion sobre cualquier programa. El ELF conserva simbolos y el observador mide fputc, no todas sus instrucciones.

No se consultaron la fuente ni la solucion publicada del objetivo. Eso no garantiza que un desafio publico nunca haya estado en datos de entrenamiento. La deduccion la hizo Brain usando evidencia de REA y los bytes; no se atribuye a REA una resolucion autonoma.

## QA previa a ejecutar

56/60 = **93,3/100**, registrada por el gate antes del objetivo. Completitud 14/15: sujeto exacto y alcance acotado. Ejecutabilidad 15/15: compilacion y 15 controles reales. Seguridad 13/15: barreras medidas, sin auditoria de kernel/CVE. Documentacion 9/10: instrumentos y registros completos; publicacion posterior a la corrida. Proceso 5/5: control negativo y prediccion previa inalterada. 40 puntos N/A: cobertura de producto, arquitectura, DevOps e innovacion.

```text
--- METODO PROMETEO ---
Accion delicada: SI, ejecucion aislada de binario ajeno pedida expresamente.
Modo aplicado: FULL.
Maquina: sandbox ClickUp x86-64, kernel 6.1.158+; analisis previo en brain-env.
Rubrica: 56/60 -> 93,3/100.
N/A declarados: 40 puntos por tipo de entrega.
Review externo: no solicitado; diagnostico, sin PR ni cambios de producto.
Instrumento: gate 15/15, control exterior REJECT, baseline y observada exit 0, 43/43 eventos, hashes.
Artefactos: esta respuesta + docs/agents/evidencia/2026-10-14-019-rea-jaula-64bits.md + https://app.clickup.com/90171457413/docs/2kza6fw5-22457
```
