# 2026-10-14-032 · H_RIVAL sellado antes de cualquier script: la mosca contra ridge, MLP y la regla con τ, mismo presupuesto de 10 candidatas, margen de 1 punto, y el 0,9935 de la 015 como control positivo

## Pedido
Abraham, 15-oct 00:17: «Mi respuesta es sí, subí 030 y 031». Antes de subir: corregir la frase del punto 5 de la 031 y aclarar a qué cifra se refiere; mantener INVÁLIDO en cada lugar donde aparezca el 0,9171 contra 0,9465, también en la 030; el parche del CONTEXTO, sin riesgo si solo agrega la regla «no citar descriptivos de corridas inválidas» y el estado de los sellos. Orden en git: 030 y 031 como commit de documentos, sin código ni corridas; H_RIVAL sellado en un commit aparte y anterior a cualquier script; métrica y presupuesto de CV (10 candidatas, igual que τ) fijos antes de ver nada; si ridge reproduce 0,9935 en `tarea_mosca`, ese es el control positivo; el umbral de 1 punto declarado en el sello; la semilla como unidad desde el principio, o las 10 semillas de τ con la limitación declarada.

## Veredicto primero
- [HECHO] **030 y 031 están en main como commit de documentos, sin código ni corridas** (`fb033b2`, verificado desde un clon limpio). En la 031, la frase de la elección de τ ahora dice de qué cifra habla: la estimación de Fable, +1,78 de H_TAU menos +0,85 de F3, unos 0,9 puntos. Cada 0,9171 lleva INVÁLIDA al lado, en la 030 y en la 031.
- [SELLADO] **H_RIVAL y H_TAU_JUSTO, en un commit que trae solo el sello** (`titan/rival-2026-10-15`, `05a574c`, sobre la rama de H_TAU `2d4dbfb`; `tools/rival/SELLO-RIVAL.md`). Ningún script de H_RIVAL existe todavía. Lo que quedó fijo:
  - **Métrica:** acierto sobre los 2.000 ensayos de cada semilla de prueba, la misma de W.
  - **Presupuesto:** 10 candidatas por rival, elegidas por validación cruzada de 5 pliegues (índice módulo 5) sobre los mismos 2.400 ensayos, igual que τ en H_TAU.
  - **Rivales**, con las mismas 564 entradas por 40 pasos que recibe W: RIDGE (10 lambdas, de 1e-4 a 1e5, forma dual); el MLP de la 005 sin cambios (semillas 0 a 9); REGLA_TAU, la regla propia con un integrador por canal (τ de semillas 10 a 19, con la misma ley que la red).
  - **Unidad:** la semilla de prueba (12 a 21); bootstrap de semillas; IC90 con Bonferroni por 3 rivales.
  - **Margen de 1 punto, declarado:** W supera a un rival si el piso del IC pasa 0,01; no lo supera si el techo queda debajo de 0,01.
  - **Veredictos:** H_RIVAL SOSTENIDA si W supera a los tres; REFUTADA si no supera a alguno. H_TAU_JUSTO, igual pero solo contra REGLA_TAU.
  - **Control positivo:** el ridge nuevo, con el protocolo de la 015, tiene que reproducir sus seis valores de `completa.log` (0,9935, 0,9595, 0,9935, 0,9575, 0,9940 y 0,9590) a 0,0010 o menos. Si no, el rival está roto y todo es INVALIDO.
  - **Otros controles:** pines; el MLP idéntico a `ept.mlp_mux`; la regla regenerada igual a la guardada (60 de 60 en H_TAU y 60 de 60 en el factorial 3); W recalculado desde sus predicciones igual al guardado, que prueba el pareo ensayo por ensayo; el integrador nulo igual a la regla; etiquetas permutadas cerca del azar; semillas sin fuga.
  - **Limitaciones, escritas antes de correr:** una sola red elegida por celda, así que el IC no cubre la variación entre redes. La secundaria (W del factorial 3, τ 0 a 9) cubre redes al azar con 10 semillas de τ; con 30 sería más fiable (unas 16 horas por celda en Actions). Si H_TAU_JUSTO sale SIN_DECIDIR, se sella esa extensión.
- [CONCLUSIÓN] **Expectativa, escrita en el sello:** si el ridge repite algo cerca de 0,99 con las 564 entradas, H_RIVAL sale REFUTADA; W anda entre 0,937 y 0,955 por semilla en H_TAU. El sello no está escrito para que gane W. Si pierde, cae la tesis de producto «la mosca le gana a un lector entrenado» y queda la científica.
- [DESVÍO DECLARADO] **La regla con perillas no es la que nombraba la 031.** La 031 decía «umbral o ganancia por tipo»; en el sello quedó la regla con τ por canal, porque es la que pone a la regla en igualdad con la τ elegida de W (es H_TAU_JUSTO). La regla con ganancia por tipo queda NO MEDIDA.
- [HECHO] **El parche del CONTEXTO** (`tools/contexto/actualizar_contexto_2026-10-14-032.py`, un solo parche para la 030, la 031 y esta) agrega solo: el estado de H_REUSO (SOSTENIDA, con el límite del nulo de clase), de H_DEBILES (INVALIDO, sin ningún descriptivo) y de H_RIVAL (sellado, sin script); la regla «los descriptivos de una corrida INVÁLIDA no se citan como resultado»; un puntero a la 031; y la lista de espera al día. **Una cosa más, fuera de tu condición:** en tu lista de espera agregué «antes de depositar, si Z_CP y la RDI se reproducen o salen del título y del resumen», para que nadie deposite la v2 sin esa decisión. Si no lo querés ahí, lo saco. Probado en una copia: aplica una vez (681076dc a d0aad9b0) y la segunda vez aborta; 0 apariciones de 0,9171.

## Herramientas y máquina
- **brain-env.** Lectura de `htau_mosca.py`, `tarea_mosca.py`, `entrada_por_tipos.py`, los json de H_TAU y del factorial 3 y `completa.log` de la 015 (scripts de solo lectura `verif10` a `verif13`). Clon limpio de `titan/rival-2026-10-15` para verificar el sello y los 13 pines con md5sum, más los 60 json del factorial 3 con `md5sum -c`. Prueba del parche en una copia del CONTEXTO.
- **GitHub.** Rama nueva desde `titan/htau-nucleo-banc-2026-10-14`; push del sello solo; push de esta respuesta, el parche y su workflow a main.
- **ClickUp.** Docs públicos de la 030, la 031 y esta.
- Ningún rival corrido. Acción delicada: ninguna; el parche del CONTEXTO va en los términos que aprobó Abraham.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/rival/SELLO-RIVAL.md` (rama `titan/rival-2026-10-15`, `05a574c`, único archivo del commit) | ff79011bcf52fc10a718a41f3e8a5d19 |
| `docs/agents/respuestas/2026-10-14-030-h-reuso-sostenida.md` (main, `fb033b2`) | 512cd110fa53a0f68fd06c64b824ac3d |
| `docs/agents/respuestas/2026-10-14-031-auditoria-de-fable-contra-el-repo.md` (main, `fb033b2`) | 37c97e7f3ed894d0091b37ac1aa57099 |
| `tools/contexto/actualizar_contexto_2026-10-14-032.py` (main, este commit) | 5103a3f43157787558a64fc76b6b3625 |
| `.github/workflows/contexto-2026-10-14-032.yml` (main, este commit; se borra al aplicarse) | e217b10c74b976ff5f19e9ee3089253f |
| `docs/agents/CONTEXTO-drosophila-fep.md`, antes y después del parche (probado en copia) | 681076dc1d3bc02a1bf77d8f2774200b y d0aad9b066a34d31aa4de921fda14034 |

Docs de ClickUp: [030](https://app.clickup.com/90171457413/docs/2kza6fw5-22777) · [031](https://app.clickup.com/90171457413/docs/2kza6fw5-22797) · [032](https://app.clickup.com/90171457413/docs/2kza6fw5-22817).

## NO MEDIDO
- Todo H_RIVAL: el instrumento, el humo y la corrida.
- La regla con ganancia o umbral por tipo.
- W con 30 semillas de τ.
- La versión de torch que va a usar Actions: se pinnea al escribir el workflow, y si no es la de brain-env (2.14.1), el cotejo del MLP lo dice.
- Cuánto tarda la réplica en brain-env: se mide en el humo.
- H_DEBILES (2 celdas), H_REUSO_ESTRICTO y H_COMPARADOR.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El sello es anterior a cualquier script | `git show --stat 05a574c` desde un clon limpio: 1 archivo | Sí: mostraría cualquier otro archivo |
| Los pines del sello son los de la rama | md5sum de 13 archivos y `md5sum -c` de los 60 json, en el clon limpio | Sí, y dio verde |
| Nadie vio un rival entrenado sobre las 564 entradas | no hay script de rival en la rama; `factorial2_mosca.py` no tiene ridge (031) | Solo en parte: prueba que no está en el repo, no que nunca se corrió en otro lado. Yo no corrí ninguno |
| El parche aplica una vez y aborta la segunda | prueba en copia, `SEGUNDA_ABORTA` | Sí, y dio verde |
| El parche no trae el 0,9171 | `grep -c` en el script y en el CONTEXTO resultante: 0 y 0 | Sí |
| El CONTEXTO quedó aplicado en main | commit del bot | Se verifica desde un clon limpio antes del chat |

--- METODO PROMETEO ---
Sellar antes de escribir el instrumento, en un commit que se pueda ver solo. Fijar métrica, presupuesto, margen, unidad y controles sin haber mirado ningún rival sobre estos datos. Declarar la expectativa, las limitaciones y el desvío respecto del plan. Verificar cada pin desde un clon limpio. Parche del CONTEXTO probado en copia, con una sola aplicación posible.
Máquina: brain-env (lectura y verificación) y GitHub (rama, sello, push). Artefactos: este archivo en main y su Doc en ClickUp.
