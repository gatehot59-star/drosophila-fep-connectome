# 2026-10-14-010 · Tres ideas evaluadas: el lenguaje topológico es la más fuerte; cerebelo de borde todavía no; prótesis para avisar, no para mover

**Pedido.** 14-oct 12:43: «Hay muchas más. Por ejemplo pasa ser el cerebelo en una ia de borde. O en prótesis en humanos por tiempo de reacción. El cableado pue er la base de un nuevo lenguaje de control. [...] evalúa esa tres. el cableado o el hecho a mano. Pueden ser realmente un lenguaje gráfico o en este caso toplogico».

## Veredicto primero
- **[CONCLUSIÓN] Lenguaje topológico: la más fuerte y apoyada por los datos.**
  - [MEDIDO, lectura del código sellado `tools/factorial2/factorial2_mosca.py` md5 798a824c, funciones `lc` y `regla`] La regla a mano son seis promedios sobre cuatro tipos (LC4, LPLC2, LPLC4 y LPLC1) por lado, un umbral por línea y una carrera.
  - [MEDIDO, 2026-10-13-010] Esa regla empata con R2, que tiene 4.031.897 conexiones (+0,85 puntos). Barajar los tipos con el cableado fijo cuesta 19 puntos; barajar los destinos, 28.
  - [CONCLUSIÓN] El significado está en tipo × lado × signo → comando. Es topológico (quién se conecta con quién), no gráfico ni geométrico.
- **[CONCLUSIÓN] Cerebelo de borde: la idea sirve, el nombre no.**
  - Lo medido es una capa refleja fija. Un cerebelo se adapta con el error, y eso no está medido.
  - Donde medimos memoria y contexto, DBC3 empató con LSTM (2026-10-12-003) y en la memoria dura una máquina de estados le ganó: 0,77 contra 0,66 a 0,68 (2026-10-12-004).
- **[CONCLUSIÓN] Prótesis: aviso sí, actuación no.**
  - 93 a 95 % de acierto simulado (2026-10-13-010, 2026-10-14-001) equivale a 5 a 7 % de error, aceptable para avisar y peligroso para mover sola.
- **[CONCLUSIÓN] ¿Cableado o hecho a mano?** Los dos, en niveles distintos: la regla es la frase del lenguaje y el cableado es su forma compilada.

## Lenguaje topológico
- **[LITERATURA]** Lo más cercano: NIR, una representación intermedia común para hardware neuromórfico (Pedersen et al., *Nature Communications* 15:8122, 2024, doi 10.1038/s41467-024-52259-9). También Nengo y los lenguajes de bloques industriales (Simulink, IEC 61131-3).
- **[CONCLUSIÓN, búsqueda acotada]** No encontré uno que tome su vocabulario de los tipos de neurona de un conectoma y verifique cada programa contra sus barajados. NO MEDIDO sin una revisión sistemática.
- **Encaje:** un dialecto de la IR semántica y MLIR de Mojo Absoluto, que baje a SparseLTC o a C99.
- **Falsador:**
  - Escribir 4 reflejos en el lenguaje: despegue, aterrizaje, giro y uno nuevo (LC6→GF).
  - Cada programa compilado tiene que empatar con su cableado en el banco (margen 0,01) y ganarle a sus barajados con Holm.
  - Si alguno falla, el lenguaje no alcanza.

## Cerebelo de borde
- **Lo que hay:** la capa refleja barata bajo una IA lenta. Es la arquitectura por etapas (2026-10-12-001) y el portero sensorial (2026-10-13-020).
- **Falsador para llamarlo cerebelo:**
  - una tarea con ganancia que cambia en la marcha;
  - el reflejo adaptativo tiene que adaptarse más rápido que la regla fija con un filtro adaptativo clásico (modelo de cerebelo de Marr, Albus, Dean y Porrill).

## Prótesis
- **A favor:** un reflejo local no espera la reacción humana, que es del orden de cientos de milisegundos.
- **En contra:**
  - error simulado de 5 a 7 %, con sensores simulados;
  - la regulación médica;
  - las rodillas con microprocesador ya usan reglas para tropiezos (literatura no revisada, NO MEDIDO).
- **Uso correcto hoy:** un aviso, o una acción con confirmación.
- **Falsador:** con sensores reales, menos de 1 % de falsas alarmas sin perder detecciones.

## Herramientas y máquina
- brain-env: lectura de `factorial2_mosca.py` desde la rama `titan/factorial3-mosca-2026-10-13`.
- Búsqueda web: NIR.

## NO MEDIDO
- Cuántas conexiones tiene la regla escrita como grafo.
- El costo en microcontrolador.
- La latencia con sensores reales.
- Una revisión sistemática de lenguajes neuromórficos y de prótesis.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| La regla usa solo tipos y lados | Lectura de `lc` y `regla` en el código sellado | Sí, si usara pesos o dinámica | PASA |
| Barajar tipos cuesta 19 puntos y destinos 28 | 2026-10-13-010 | Sí | PASA |
| DBC3 no ganó en memoria | 2026-10-12-003 y 004 | Sí | PASA |
| NIR existe y es lo más cercano | Web (Nature Communications 2024) | Sí | PASA en existencia; «lo más cercano» es búsqueda acotada |
| Novedad del lenguaje | Búsqueda acotada | Parcial | CONCLUSIÓN, no medición |

--- METODO PROMETEO ---
Accion delicada: no.
Maquina: brain-env CPU + web + conector GitHub.
Artefactos: esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22257
