# Evidencia cruda · apagado de un proceso huérfano en `brain-env`

**Fecha:** 2026-08-25 18:55 (America/Buenos_Aires) · **Motivo:** Abraham detectó que había algo corriendo y pidió apagarlo.

<hr/>

## 1. Lo que había vivo, medido

Dos entornos distintos, y conviene separarlos porque **el hallazgo estaba en uno solo**:

### Sandbox propio: limpio

```plain
load average: 0.00, 0.00, 0.00
pgrep -af python  ->  ninguno (salvo el propio chequeo)
```

Lo único que quedó son archivos en disco, sin proceso: `motor.py`, `run_motor.py`, `presupuesto_esp32.py`, `corrida_motor.log`, `presupuesto_esp32.log`, `motor_resultados.json`.

### Container `brain-env`: acá sí había un proceso vivo

```plain
1    | sleep infinity
5644 | adb -L tcp:5037 fork-server server --reply-fd 4
9498 | sh -c cd /workspace && PYTHONUNBUFFERED=1 timeout 1100 python3 -u dbc3_benchmark.py 2>&1 | tail -50
9504 | timeout 1100 python3 -u dbc3_benchmark.py
9505 | tail -50
9506 | python3 -u dbc3_benchmark.py
```

<strong>Era </strong>**`dbc3_benchmark.py`**, lanzado sobre `/workspace` (archivo de 16.020 B, `Aug 25 21:27` hora del container), con `timeout 1100`. **No lo estaba esperando nadie y no era parte del trabajo del turno.**

<p><br/></p>

**Y había sobrevivido a su propio `timeout`:** el límite de 1.100 s = 18,3 min ya debería haberlo cortado, y seguía vivo. O sea que **el guard de tiempo no alcanzó para garantizar el apagado.**

<hr/>

## 2. La señal de carga, antes

```plain
loadavg: 5.46 5.66 5.18
```

<hr/>

## 3. Lo que se ejecutó

```plain
kill -TERM 9506 9504 9498 9505
sleep 4
kill -KILL 9506 9504 9498 9505
```

## 4. Resultado, verbatim

```plain
9498 MUERTO
9504 TODAVIA VIVO
9505 TODAVIA VIVO
9506 MUERTO

--- lo que sigue vivo en el container ---
1 | sleep infinity
5644 | adb -L tcp:5037 fork-server server --reply-fd 4
(mas los dos procesos del propio chequeo)

loadavg: 5.46 5.66 5.18
```

**Verificación a los 25 s, y acá está la aclaración que importa:**

```plain
9504 Z
9505 Z

--- procesos con cmdline ---
1 | sleep infinity
5644 | adb -L tcp:5037 fork-server server --reply-fd 4
(mas los dos del chequeo)

loadavg: 4.61 5.43 5.12
```

<hr/>

## 5. Veredicto derivado (conclusión, no medición)

1. **El proceso de cómputo está apagado.** `9506` (el Python que consumía CPU) y `9498` (su shell) están muertos.
2. **`9504` y `9505` NO son procesos vivos: son zombies** (estado `Z` en `/proc/<pid>/stat`). Ya terminaron y sólo esperan que `init` los cosecha. **No consumen CPU ni memoria.** Por eso desaparecieron del listado de procesos con `cmdline`: un zombie tiene el `cmdline` vacío.
3. **Decir «todavía vivo» por la existencia de `/proc/<pid>` era mi propio falso positivo.** `os.path.exists('/proc/<pid>')` **no distingue un proceso corriendo de un zombie**, y hay que leer el estado para saberlo. Es el mismo antipatrón de siempre: un chequeo que responde otra cosa que la que promete.
4. **La carga bajó** de 5,46 a 4,61 en el promedio de 1 minuto, consistente con que el consumidor murió.
5. **Ningún proceso de QEMU estaba corriendo.** El barrido por `qemu` no devolvió nada: el emulador quedó instalado, no ejecutando.

<hr/>

## 6. NO MEDIDO, declarado

1. **No se leyó la salida de `dbc3_benchmark.py` antes de matarlo.** Si había resultados parciales en su stdout, **se perdieron**: iba a `tail -50` de un pipe, no a un archivo. Eso es una consecuencia real de apagarlo y se declara.
2. **No se abrió `dbc3_benchmark.py`** para determinar qué medía ni quién lo lanzó. El archivo sigue en `/workspace` y se puede volver a correr.
3. **No se sabe por qué sobrevivió al `timeout 1100`.** Estado: **NO MEDIDO**, y es lo que habría que entender antes de volver a lanzar algo largo con ese patrón.
4. **La carga de ~4,6 con sólo zombies es alta** y no se explicó. Puede venir del host compartido. No se midió.
5. **No se borró ningún archivo** de `/workspace` ni del sandbox: se apagó un proceso, no se limpió nada.

```plain
--- METODO TITAN ---
Accion delicada: SI (matar un proceso ajeno al turno, en un container compartido)
Modo aplicado:   TITAN FULL
Rubrica:         accion de operacion -> Completitud, Documentacion, Proceso QA
N/A declarados:  Ejecutabilidad, Seguridad, Testing, DevOps, Arquitectura, Innovacion
Review externo:  no aplica
Instrumento:     build.run sobre brain-env, exit 0 en las tres llamadas.
                 Salida cruda de las tres arriba, verbatim.
                 Pedido explicito del usuario para el apagado.
```