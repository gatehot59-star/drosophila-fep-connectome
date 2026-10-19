# 2026-10-14-061 · ARRANQUE corregido para el chat nuevo y H_PARES_DATOS medido

**Fecha:** 19-oct-2026, 19:40 (America/Buenos_Aires). **Doc:** [Doc 061](https://app.clickup.com/90171457413/docs/2kza6fw5-23917) (Space del proyecto; la segunda página es el ARRANQUE).

## Veredicto (conclusión)

- El ARRANQUE corregido está en `docs/agents/ARRANQUE-NUEVO-CHAT.md` (main) y, con el mismo texto, en la segunda página del Doc 061. Corrige los 10 rojos de la auditoría 2026-10-19-01 y dos frases mal resumidas (tabla de la sección 3.2).
- H_PARES_DATOS: VÁLIDO, y H_DATOS_EMBUDO, H_DATOS_CRUDO y H_DATOS_PRIMER_DIA SOSTENIDAS (sección 3.1).

## 1. Pedido

Abraham, 19-oct 18:21: «PUES DEBES GENERAR EL DOCUMNTO SIN ERRORES PARA INICAR EN OTRA INSTSNCIA, EL QUE CORREGISTE». Leído como: el ARRANQUE de la 060 con los rojos de la auditoría corregidos, listo para pegar en otra instancia. Además, la curva de H_PARES_DATOS (pedido del 18-oct 22:30) había terminado y nadie la había leído.

## 2. Herramientas y máquinas

- Conector de GitHub: lectura de commits y archivos; push a main de este archivo, del ARRANQUE, del parche del CONTEXTO y de su workflow.
- brain-env (gateway, servicio build): lectura de la re-agregación de H_PARES_DATOS en /workspace/agr061 y diff contra el log de Actions. No escribió en ningún repo.
- Sandbox de ClickUp: índice v2, cruce respuesta a Doc, parche probado sobre el CONTEXTO real, generador del índice de git probado en el repo de prueba y el ARRANQUE. Se reinició a mitad del turno y se llevó /home/user/work y /tmp.
- ClickUp: buscador del workspace; Doc 061 creado; índice v2 adjunto al Doc (.txt) y en el chat (.md); INDICE-COMPLETO-GIT y CONTEXTO traídos como adjuntos .txt para leerlos en el sandbox.
- Un agente de lectura nuevo, sin la conversación, para probar el arranque.
- Actions: el workflow del parche, que se borra solo. Kaggle: nada.

## 3. Qué se midió

### 3.1 H_PARES_DATOS

MEDIDO, de `results/pares_datos_2026-10-18/agregado.log` (bot e5db870, 17:34Z, rama titan/pares-datos-2026-10-18):

- Chequeo: MISMO_SCRIPT, SUBCONJUNTOS, PLAN_COMPLETO, REPRO_TAULIBRE y REPRO_CRUDO en True, 12 de 12 json válidos: VALIDO.
- D_CRUDO +0,0401 [+0,0287; +0,0508]; D_PCA_L +0,1520 [+0,1425; +0,1616]; D_PROY_L +0,0904 [+0,0806; +0,1000].
- E_CRUDO -0,0382 [-0,0599; -0,0170]; E_PCA_L -0,2761 [-0,3054; -0,2482]; E_PROY_L -0,1198 [-0,1325; -0,1065].
- Veredictos del sello: EMBUDO SOSTENIDA (pisos de D_PCA_L y D_PROY_L por encima de +0,01), CRUDO SOSTENIDA (piso de D_CRUDO por encima de +0,01), PRIMER_DIA SOSTENIDA (techos de los tres E por debajo de -0,01).
- Descriptivos: W (sin etiquetas) 0,9276 en c2 y 0,9222 en c5. Etiquetados para alcanzar a W, promedio de celdas: MOSCA_L 96, CRUDO 192, PCA_L 384 y PROY_L 2.400 (c2: 96, 96, 384 y 192; c5: 96, 192, 384 y más de 2.400). Con 2.400: c2 CRUDO 0,9995, PCA 0,9995 y MOSCA_L 0,9943; c5 MOSCA_L 0,9951, CRUDO 0,9910, PCA 0,9950 y PROY 0,8736. Varianza que retiene PCA con 240 componentes: 0,5958 en c2 y 0,2473 en c5.
- Re-agregación en brain-env sobre los 12 json del commit e5db870 (MD5SUMS: 12 OK; agregar_pares.py md5 6ca4306f): las 52 líneas del log salen iguales a las de Actions.

CONCLUSIÓN: con pocos ensayos etiquetados, el embudo de la mosca paga contra sus pares artificiales del mismo tamaño y contra el lector crudo, y el primer día (96 etiquetados) ningún brazo artificial alcanza a la mosca sin etiquetas. Con muchos datos lo clásico la alcanza, y en c2 la pasa. Vale para 2 de 6 celdas y una prueba; W sabe qué ensayos son fondo y PCA ve los 2.400 ensayos sin etiqueta (límites declarados en el sello).

### 3.2 Correcciones del ARRANQUE

| Rojo o frase | Antes (060) | Ahora (061) | Instrumento |
|---|---|---|---|
| 5 · hora de CORRER | 14:15 | 14:07 (17:07:45Z) | commit 1f04d2c |
| 6 · la curva | «todavía corre» | terminada, leída: VALIDO y tres SOSTENIDAS | bot e5db870 y re-agregación en brain-env |
| 8 · link al Doc | título largo con paréntesis, llegó como «#» | textos cortos («Doc 061») | lo confirma Abraham: NO MEDIDO desde acá |
| 9 · mismo texto | git sin tildes y con otro encabezado | git y sandbox iguales byte a byte; el Doc lleva el mismo texto | SHA del blob (git hash-object contra el conector y el commit del bot) |
| 10 · Doc de cada respuesta | «cada respuesta con su Doc» | 97 de 280 en el índice de git; 224 de 280 en el cruce v2; 34 de las 56 sin Doc son la 001 a la 040 | cruce por título revisado a mano |
| 10 · script del índice | el de git no era el probado | el de git (a9b6352d) da en el repo de prueba el mismo índice que el probado (1c8e36b1), salvo una línea de redacción | diff de las dos salidas |
| 11 · lista de ClickUp | 6 al 30-sep solo por barrido | 6 al 30-sep enumerado entero: 594 registros; del proyecto, el auditor externo y Mojo Absoluto | agente de enumeración; el archivo se perdió en el reinicio, quedan los conteos |
| 12 · «578 Docs» | 578 filas | 472 títulos distintos: 405 con vista de Doc y 67 solo como página | deduplicado por título |
| 13 · otras líneas | entraron títulos de MUDH-Mobile | sacados MUDH-Mobile, REA y Ghidra, Corpus e ingresos | relectura a mano y barrido de marcas |
| 15 · brain-env | «caído todo el día» | túnel intermitente, máquina viva (4 días y 10 h de uptime) | uptime leído en brain-env |
| 16 · adjunto | «adjunto al Doc» (era del chat) | índice v2 adjunto de verdad al Doc 061 (.txt) y en el chat (.md) | adjunto creado en el Doc |
| 17 · mojo-absoluto | 88 respuestas | 90 | listado de respuestas/ (auditoría) |
| frase · H_LIF_SHUFG | «el freno es la neurona, no el cableado» | el atajo de k32 venía de nuestra neurona de tasa, no del barajado | Doc de la 055 |
| frase · BANC | «conserva el 92,4% de las aristas fuertes» | en BANC está el 92,4% de las aristas de R2 con 20 sinapsis o más (las evaluables) | Doc de BANC del 14-oct |

### 3.3 Prueba del arranque con un agente nuevo

Un agente de lectura sin la conversación leyó el ARRANQUE y chequeó contra git y ClickUp. OK: CONTEXTO e índice en main (202 y 78; 57, 40 y 183), los seis estadísticos y los tres veredictos contra el agregado.log, el DOI contra el recibo, 10 links de la sección 9 (cada título corresponde a su texto) y el adjunto del índice v2. Encontró cinco problemas: tres de orden, porque corrió antes del push (la ruta de la 061, las 203 respuestas y el CONTEXTO todavía en la 058), y dos de redacción («472 Docs» eran títulos; la cuenta 97 y 183 se leía confusa), corregidos antes del push. Su veredicto, antes de corregir: no arrancaría sin preguntar, por esos cinco.

## 4. Evidencia cruda

Agregado de Actions, leído en brain-env (/workspace/pd061, worktree en e5db870):

    CHEQUEO MISMO_SCRIPT=True SUBCONJUNTOS=True PLAN_COMPLETO=True REPRO_TAULIBRE=True REPRO_CRUDO=True json_validos=12/12 -> VALIDO
    ESTADISTICO D_CRUDO=+0.0401 IC95=[+0.0287, +0.0508]
    ESTADISTICO D_PCA_L=+0.1520 IC95=[+0.1425, +0.1616]
    ESTADISTICO D_PROY_L=+0.0904 IC95=[+0.0806, +0.1000]
    ESTADISTICO E_CRUDO=-0.0382 IC95=[-0.0599, -0.0170]
    ESTADISTICO E_PCA_L=-0.2761 IC95=[-0.3054, -0.2482]
    ESTADISTICO E_PROY_L=-0.1198 IC95=[-0.1325, -0.1065]
    VEREDICTO H_DATOS_EMBUDO=SOSTENIDA
    VEREDICTO H_DATOS_CRUDO=SOSTENIDA
    VEREDICTO H_DATOS_PRIMER_DIA=SOSTENIDA

Re-agregación contra Actions, en brain-env:

    e5db870_2026-10-19T17:34:00Z
       52 pd061/results/pares_datos_2026-10-18/agregado.log
       53 agr061/agregado_brain.log
    52a53
    > FIN_AGR
    b3097a2069db0b39f8518f39b451e1e7  pd061/results/pares_datos_2026-10-18/agregado.log
    a954a68cd8b8c67cf0079e7edcfb24e6  agr061/agregado_brain.log
     22:02:11 up 4 days, 10:57,  0 users,  load average: 0.29, 0.20, 0.18

La línea FIN_AGR la agrega el lanzador; el resto es igual.

Parche del CONTEXTO, en el sandbox sobre la copia real (blob 804cee08, igual a main):

    md5 antes 1173ec1f5a56b7de7afdd39f879e2ee2
    ANCLA apariciones=1 (tres anclas)
    md5 despues de0f8711db31d4d90dbdfde7847d1bc5
    PARCHE OK
    segunda pasada: ANCLA apariciones=0 :: ABORTA: ancla no unica, exit 2

Generador del índice de git: el de git (md5 a9b6352d) corrido sobre el repo de prueba da ed2fb1d5; contra la salida del probado (1c8e36b1, 4ae6b3f6) cambia solo la línea «Doc de cada respuesta» (comillas alrededor de Doc:). El repo de prueba es chico (4 respuestas, 2 ramas).

Archivos de esta entrega: ARRANQUE 28.088 B, md5 3dcfb25939ff47bdb578494fd2663172, blob 00a1a343ccc400972eccc3612b0ff3e21e7c7585. Parche md5 8733eb9c8996e328f32ced7bb57d7a29. Workflow md5 277b55815d50ecbf72c13db7a7460396. Índice v2 203.855 B, md5 86051340d17178908bd6af41aa1cba54 (adjuntos: [.txt en el Doc 061](https://t90171457413.p.clickup-attachments.com/t90171457413/9f9c9f39-7ded-47d6-acb7-2da77ed47a1b/INDICE-CLICKUP-PROYECTO-2026-10-19-v2.txt?view=open), [.md](https://t90171457413.p.clickup-attachments.com/t90171457413/0d98cd8f-6652-5f5a-9d0e-33d57070c18e/INDICE-CLICKUP-PROYECTO-2026-10-19-v2.md?view=open)).

## 5. Archivos

- `docs/agents/ARRANQUE-NUEVO-CHAT.md` (reescrito entero).
- `docs/agents/respuestas/2026-10-14-061-arranque-corregido-y-h-pares-datos-medido.md` (este).
- `tools/contexto/actualizar_contexto_2026-10-14-061.py` y `.github/workflows/contexto-2026-10-14-061.yml` (el workflow aplica el parche, escribe en su commit los md5 del CONTEXTO y del ARRANQUE y el blob del ARRANQUE, y se borra).
- El índice v2 no va a git por tamaño: queda en los adjuntos, con su md5.

## 6. NO MEDIDO

- Que los links le lleguen clickeables a Abraham en el chat.
- Un chat nuevo de Abraham con el ARRANQUE pegado (la prueba de la 3.3 es con un agente, no con su chat).
- Los 12 trabajos de H_PARES_DATOS corridos de nuevo en brain-env (sí se repitió el agregado).
- Robustez y reservorio de H_PARES.
- El índice v2 por contenido: es por título, y pueden faltar Docs del proyecto que la 060 dejó como otra línea.
- La enumeración fina del 6 al 30-sep: se hizo, pero el archivo se perdió en el reinicio del sandbox; quedan los conteos.

## 7. Verificación después del push (agregado en el cierre)

- Commit 82a745d (22:24:48Z). La 061 llegó igual byte a byte: blob 550b9783 en git y en el sandbox. El ARRANQUE y el parche llegaron con una tilde de menos, «rehizo» por «rehízo» (una línea de diff en cada uno; blob d682cc4a contra 00a1a343 y a488a09b contra 179ef6fc).
- Bot ff2d2fb (22:24:55Z): parche aplicado, tres anclas con una aparición cada una, md5 del CONTEXTO de 1173ec1f a a07976bd. El parche de git (md5 b6bc1207), corrido en el sandbox sobre la copia real, da el mismo a07976bd.
- Cierre (`tools/arranque/cierre_2026-10-14-061.py`, aplicado por Actions): pone la tilde en el ARRANQUE y en el CONTEXTO. Esperado y probado en el sandbox: ARRANQUE md5 3dcfb259 y blob 00a1a343, iguales a la copia del sandbox y del Doc; CONTEXTO md5 de0f8711, igual a la prueba del parche en el sandbox. Lo confirma el commit del bot «cierre(2026-10-14-061)». El parche que quedó en git conserva «rehizo»: es el que corrió.
- Segunda vuelta del agente, después del push: los cinco problemas quedaron resueltos (la 061 en main, el blob 00a1a343, el CONTEXTO en la 061 y el Doc con sus dos páginas). Encontró uno nuevo y menor: «auditar el laboratorio» y «pedido a Tao» eran dos links a la misma tarea; queda uno solo (tools/arranque/cierre2_2026-10-14-061.py); el ARRANQUE final queda en md5 de659ba5 y blob d2beec25, y lo confirma el commit del bot del segundo cierre. Su veredicto: arrancaría sin preguntar.

--- METODO PROMETEO ---
Rol: síntesis y corrección (grande). Delicado: no.
Máquinas: conector de GitHub (lectura y push), brain-env (re-agregación y diff), sandbox de ClickUp (índice, cruce, parche y generador probados), Actions (parche del CONTEXTO), un agente de lectura (prueba del arranque). Kaggle: nada.
Archivo: docs/agents/respuestas/2026-10-14-061-arranque-corregido-y-h-pares-datos-medido.md
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23917
