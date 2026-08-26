# 102 · Sí: lo que corrió en Kaggle es el `motor.py` corregido, y acá está la prueba

**Fecha:** 2026-08-26 · **Pregunta de Abraham:** antes de los experimentos de Kaggle vos
habías corregido `motor.py` y luego venía probar la nueva versión. ¿Eso es lo que probaste?
Y me recuerda el peritaje 092.

**Respuesta corta: sí, y no lo había probado. Lo probé ahora.**

Es justo el error que el peritaje 092 me señaló (E-01: verificar el sujeto exacto). Yo
dije «corrí motor v2 en GPU» porque el título del kernel decía `motor v2`. Un título no
es un archivo.

---

## 1. El sujeto, medido

`kernel_shard.py` (76.731 B) contra `motor_v2.py` (65.543 B): **dos bloques de
diferencia y nada más.**

1. una cabecera de **26 caracteres** (`# GENERATED kernel shard`)
2. el `if __name__ == "__main__": sys.exit(main())` cambiado por el corredor de shard

Las **45 funciones** de `motor_v2` están verbatim. El parche GPU agrega **5 funciones
nuevas** (`gpu_info`, `propagate_gpu`, `verify_gpu_against_cpu`, `shard_indices`,
`main_shard`) y **redefine CERO**. `propagate` sigue siendo la de v2; `propagate_gpu` es
una función aparte que se inyecta en runtime **después** de verificarse.

Y se verificó sola, adentro del kernel, sobre el grafo real:

```
OK  gpu_reproduce_a_la_cpu: desvio relativo maximo = 3.857e-16 contra tolerancia 1.0e-09
```

## 2. Los 6 NO MEDIDO del peritaje 092, uno por uno

| # | del peritaje | estado hoy | evidencia |
|---|---|---|---|
| 1 | no se corrió sobre el conectoma real | **CERRADO** | n=138.639, e=15.091.983, md5 del parquet verificado, 623 filas sin match declaradas |
| 2 | el brazo de `W` es NO MEDIDO | **MEDIDO, y da NEGATIVO** | `ventaja_W`: p=0,175 (t50 y t149), p=0,80 (t100). 6 de 39 nulls le ganan |
| 3 | `null_maslov_sneppen` no se ejecutó | **PARCIAL** | corrió sobre sintético; la corrida real usa CP |
| 4 | `phase_jitter` no se barrió | **SIGUE ABIERTO** | — |
| 5 | el defecto de `normalize_spectral` con pesos reales | **CERRADO** | `rho_pre=2152,64 → rho_post=0,990000` en el real, 39/39 nulls OK en 4 brazos, dos instrumentos espectrales coinciden a 3,1e-11, y el test **puede dar rojo** |
| 6 | no se corrigió nada, esto es peritaje | **CERRADO** | `motor_v2.py` es el fix |

**4 cerrados, 1 parcial, 1 abierto.**

## 3. Lo más importante, y es contra mí

El peritaje decía: *«falta EL brazo de control que sostiene la tesis»*. Se agregó. **Y el
brazo dice que la tesis no se sostiene.**

`ventaja_W` con 39 nulls sobre el conectoma real: **p = 0,175**. No es que falte
potencia: con 39 nulls el piso es 0,025 y este dio 0,175, o sea que 6 nulls le ganan al
real. La aritmética compleja en `W` **no aportó nada medible** frente a pesos reales con
signo.

Y no se puede escapar diciendo «los dos brazos eran la misma función», porque eso se
testó antes:

```
OK  los_dos_brazos_comparten_las_MAGNITUDES: desvio maximo de |w| = 8.882e-16
OK  los_dos_brazos_NO_son_la_misma_matriz: desvio maximo de w = 1.1203 -> difieren solo en la fase
OK  los_dos_brazos_producen_DINAMICAS_distintas: desvio maximo del estado final = 5.1666e-02
```

Los brazos difieren, producen dinamicas distintas, y el efecto igual no aparece.

## 4. Corrección de la respuesta 101

En la 101 escribí: *«el cruce CPU contra GPU no está hecho»*. **Era falso dos veces.**
El kernel ya lo había hecho adentro (3,857e-16) y yo tenía el log en la mano sin leerlo
entero. Ahora además lo hice null por null: **36 de 36 pares coinciden**, desvio maximo
4,975e-05, que es exactamente el redondeo del log a 4 decimales. `REAL` CPU 0,6642 vs
GPU 0,66421754.

**W-01 cerrado en serio:** dos maquinas, dos backends, mismos numeros. Ya no soy el
unico testigo.

## 5. NO MEDIDO

- El cruce con precision completa necesita el JSON final de la corrida CPU (iba 36/39).
- El cruce se hizo sobre **una** de las 12 metricas.
- `phase_jitter` sigue sin barrerse.
- `null_maslov_sneppen` no corrió sobre el grafo real.
- CPU y GPU comparten semilla y algoritmo del null: el cruce valida el **backend**, no
  la eleccion del null.

```
--- METODO ---
Accion delicada: NO. Lectura de archivos y de logs ya producidos.
Instrumento:     tools/cruce_kernel_vs_motorv2.py y tools/cruce_cpu_vs_gpu.py,
                 las dos corridas antes de commitearse.
Falsador:        mi propia respuesta 101, que declaro NO MEDIDO algo que estaba
                 medido en un log que yo mismo habia bajado.
Evidencia:       docs/agents/evidencia/2026-08-26-102-identidad-del-kernel-y-cruce-cpu-gpu.md
```
