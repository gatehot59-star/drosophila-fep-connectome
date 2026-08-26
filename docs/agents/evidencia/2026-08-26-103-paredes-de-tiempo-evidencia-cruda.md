# EVIDENCIA CRUDA · 2026-08-26 · bisección de las paredes de tiempo

**W-01:** salida verbatim de las 9 sondas, sin recortar, para que cualquiera recompute el veredicto y lo contradiga.

**Instrumentos:** mi sandbox (bash/Python, sin red) y `gateway build.run` sobre `brain-env`.

---

## Sonda 1 · sandbox, 26 s con el techo por defecto

```
=== SONDA 1: cuanto aguanta una llamada, medido ===
1787721804.260857193
sobrevivio 26 s
exit=0
1787721830.338896669
```

Delta: 26,08 s. **Pasa.**

## Sonda 2 · sandbox, 45 s con el techo por defecto

```
$ S=$(date +%s); echo "inicio $S (SIN timeoutMs: default declarado de 30 s)"; sleep 45; ...
The command timed out. You can try again with a longer `timeout` value, or simplify the command.
```

**Muere.** Pared por defecto entre 26 y 45 s, con 30 s declarado.

## Sonda 3 · sandbox, 110 s con override de 120 s

```
=== SANDBOX: sonda de 110 s con techo declarado de 120 s ===
inicio 1787722116
fin 1787722226  ->  elapsed 110 s  ->  T110_SOBREVIVIO
```

## Sonda 4 · sandbox, persistencia de un proceso desprendido

Lanzamiento:

```
=== SONDA 2: un proceso lanzado en background sobrevive el fin de la llamada? ===
lanzado PID 4245
2 /tmp/superviviente.log
```

Segunda llamada (11 s después):

```
el proceso background sobrevivio?
   4245       00:13 bash -c for i in $(seq 1 400); do echo "$(date +%s) tick $i" >> /tmp/superviviente.log; sleep 1; done
14 /tmp/superviviente.log
1787721842 tick 13
1787721843 tick 14
```

Tercera llamada (6 min 36 s después del lanzamiento, atravesando una llamada que murió por timeout):

```
   4245       06:36 bash -c for i in $(seq 1 400); ...
396 /tmp/superviviente.log
```

Cierre:

```
400 /tmp/superviviente.log
1787721830 tick 1
1787722230 tick 400
primer tick 1787721830  ultimo 1787722230  span 400 s  ticks 400  huecos 1
```

**400 ticks / 400 s de span.** El `huecos 1` es el off-by-one del conteo inclusivo (`span+1 - ticks`), no un hueco real: hay un tick por cada segundo del intervalo.

## Sonda 5 · sandbox, el foreground del timeout NO queda huérfano

```
=== el timeout de la llamada mato el proceso? ===
no quedo ningun sleep 45 huerfano
```

## Sonda 6 · sandbox, qué persiste del filesystem

```
=== /home/user/output se limpia entre llamadas? ===
total 4
drwxr-xr-x 2 user user   60 Aug 26 05:24 .
drwx------ 8 user user 4096 Aug 26 05:24 ..
```

Recreado vacío con mtime nuevo en cada llamada. En cambio:

```
marca de la llamada anterior:
1787721832
ahora:
1787721843
```

`/home/user/scratch` **persiste**.

## Sonda 7 · gateway, el artefacto del reloj

```
$ echo INICIO $(date -u +%H:%M:%S); sleep 30; echo t30_OK $(date -u +%H:%M:%S)
exit=0
INICIO 05:25:23
t30_OK 05:25:23
```

Contra-medición con dos instrumentos distintos:

```
$ cut -d' ' -f1 /proc/uptime; command -v sleep || echo 'NO HAY sleep'; sleep 12; cut -d' ' -f1 /proc/uptime; python3 -c "..."; cut -d' ' -f1 /proc/uptime
413195.49
/usr/bin/sleep
413207.50
--- python sleep ---
durmio 12.0 s
413219.60
```

**`sleep` funciona; `$(date)` está pre-expandido.** El claim «el sleep no duerme» queda refutado por el propio turno.

## Sonda 8 · gateway, bisección de la pared

```
$ echo INICIO ...; sleep 20; ...; sleep 20; ...; sleep 20; ... (60 s en total)
Request timed out

$ cut -d' ' -f1 /proc/uptime; sleep 45; cut -d' ' -f1 /proc/uptime; echo T45_SOBREVIVIO
413229.47
413274.49
T45_SOBREVIVIO

$ cut -d' ' -f1 /proc/uptime; sleep 55; cut -d' ' -f1 /proc/uptime; echo T55_SOBREVIVIO
413280.98
413336.00
T55_SOBREVIVIO
```

**55,02 s pasa · 60 s muere.**

## Sonda 9 · gateway, el trabajo sobrevive la pared

Lanzamiento (la llamada volvió en ~2 s):

```
$ nohup sh -c '... > log; sleep 90; ... >> log; echo TERMINO_SOLO >> log' & echo lanzado; sleep 2; cat log
lanzado
413350.05
```

Verificación ~150 s después:

```
413503.25
--- el log del trabajo lanzado hace ~100 s ---
413350.05
413440.05
TERMINO_SOLO
```

**90,00 s exactos, con la pared en 60. El trabajo no depende de la llamada.**

---

## Contexto de las máquinas al momento de medir

```
sandbox : up 5:14 ... load average: 1.00, 1.00, 1.01   (el motor colgado se come 1 nucleo)
          python3 motor.py --synthetic 600 6000 --nulls 3 --steps 20 --null-kind ms  ->  02:33:15 al 99,8%
brain-env: /proc/uptime 413503.25 s = 4 d 18,8 h
```

---

## NO MEDIDO

- No se bisecó entre 56 y 59 s en el gateway.
- No se midió el tope de llamadas por turno de este entorno; el «default 10» es de documentación de terceros sobre la API.
- No se probó un override de sandbox mayor a 120.000 ms.
- No se midió el umbral de compactación de contexto.
- Las tres sondas de sandbox usan `date +%s`, o sea resolución de 1 s: los «110 s exactos» tienen ±1 s.
