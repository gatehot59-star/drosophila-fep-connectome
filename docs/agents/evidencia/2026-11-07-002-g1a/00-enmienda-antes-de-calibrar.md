# G1-A · enmiendas fijadas antes de calibrar

Respuesta 2026-11-07-002. Este archivo se commitea **antes de correr la primera réplica de la calibración y antes de cruzar la Y real con el M real**. Diseño de base: docs/agents/respuestas/2026-11-04-001-g1-arrancado-diseno-g1a-y-censo.md (commit c89a3388). Instrumento: g1a.py en esta carpeta, sha256 a1c5ec691636ca57763fd3a37b78a59fd0acc27f14a8b47d948ac1a3db6dcd5e, 34.966 bytes.

## Lo que no cambia

Definiciones de S, D, X, relevo pesado, competidor, Y, M, L y pares; modelos G0 y G1; estadístico primario β̃ (β con θ, φ y γ fijos en el ajuste de G0); nulo de 1.000 recableados de la tabla S→D cableada con grados conservados dentro de cada lado; p = (k + 1)/1.001; Holm sobre las dos moscas; margen OR 1,5; tabla de lectura; moscas (FlyWire entera y BANC cerebro como primarias, BANC entero como secundaria); las cinco secundarias.

## Enmiendas, con el porqué

1. **Cola del p.** k cuenta los recableados con β̃ mayor o igual al observado: una cola, hacia arriba. La regla predice β > 0 y la lectura pide OR ≥ 1,5; el diseño escribió p sin decir la cola.
2. **Intervalo del efecto.** Wald con error estándar robusto a dos vías, por x y por D′: V = Vx·Gx/(Gx − 1) + Vd·Gd/(Gd − 1) − V0, y si V ≤ 0, el mayor de los dos primeros términos. Reemplaza al bootstrap de las X con 2.000 remuestreos. Por qué: el bootstrap de X no ve la dependencia entre X que comparten D′ (cada D′ aparece contra todas las X y su φ es común), y calibrar el intervalo que de verdad se usa, con 200 réplicas por β y dos moscas, pediría 3,2 millones de reajustes. El error estándar del modelo se guarda al lado para comparar.
3. **Reglas de la calibración.** Las literales del diseño voltean a un instrumento correcto demasiado seguido. Con 200 réplicas, un IC95 correcto cae fuera de 93 a 97 % con probabilidad 0,14 en cada β (cerca de 0,70 sumando los ocho chequeos de las dos moscas), y «p < 0,01 en a lo sumo el 1 % de 200» (2 o menos) falla un test correcto con probabilidad 0,32. Las nuevas usan cortes binomiales al 0,5 %, con 200 réplicas en cada β plantado (0; 0,4; 0,7 y 1,1):
   - cobertura del IC95 de β̂: **181 o más de 200** en cada β. Cubrir de más no es falla de validez: cuesta potencia, y se informa como potencia;
   - sesgo de β̂ (ajuste conjunto): **menor a 0,1** en valor absoluto en cada β, como pedía el diseño; una réplica sin β̂ finito cuenta como falla;
   - con β = 0: **6 o menos de 200 con p < 0,01 y 19 o menos con p < 0,05**;
   - **todos los ajustes convergen** (gradiente máximo menor a 1e-6 en 100 iteraciones).

   Probabilidad de que un instrumento correcto falle alguno de los seis cortes de una mosca: 0,018 como mucho.
4. **Potencia.** Se informan dos: potencia_p (p < 0,005, el peor caso de Holm con dos moscas) y potencia_completa (p < 0,005, OR estimado ≥ 1,5 e IC sin el 1), en cada β. «Potencia a OR 1,5» se lee con potencia_p en β = 0,4 (OR 1,49): la completa no puede pasar de 0,5 ahí por construcción, porque pide que el OR estimado supere justo el verdadero. Si en BANC cerebro potencia_p en 0,4 queda debajo de 0,8, el sello lo dice antes de cruzar.
5. **Identificación.** φ del primer D′ informativo queda fijo en 0. No cambia las predicciones ni β.
6. **Descripción.** bits = (ℓ1 − ℓ0)/ln 2 − ½·log2(pares informativos): código de dos partes con un parámetro más.
7. **Dosis y especificidad.** Δβ = β̂(pesadas inhibitorias) − β̂(grupo de control), con error √(SE1² + SE2²) e IC95. Los grupos son disjuntos en X pero comparten D′, así que esa suma es una aproximación y se declara. «El control da menos» si el IC queda entero arriba de 0. Descriptivas, sin Holm.
8. **Transferencia.** β fijo en el β̂ de FlyWire como offset sobre M; θ, φ y γ reajustados en BANC cerebro; bits por par positivo frente a G0.
9. **Máquina.** brain-env en vez de Actions x64. La medición 2026-11-07-001 dio 0,7 y 1,4 GiB por mosca; las cuatro entradas están fijadas por md5 en brain-env, y en Actions habría que bajar y fijar 0,5 GB de entradas desde afuera. La salida cruda va verbatim a git (W-01: la independencia es del instrumento). Replicar en Actions queda como deuda.
10. **Semillas.** Banco de recableados: 7830711 (FlyWire) y 8880711 (BANC). Calibración: 7830712 y 8880712, con β·10 como segunda componente. El banco se coteja por sha256 entre la calibración y el cruce.
11. **Candados en el código.** El modo cruzar se niega a correr si su propio sha256 no es el sellado, si la calibración de esa mosca no pasó o si su banco no es el calibrado. El modo calibrar ajusta G0 con la Y real (G0 no mira M) y borra la Y real del grupo antes de simular.

## Lo que ya se miró antes de esta enmienda

- Una prueba de la matemática con datos de juguete en el sandbox (40 X, 120 D′): β por bloques contra Newton denso, diferencia 5,6e-11; Vx, Vd y V0 iguales a un sándwich denso; β̃ vectorizado igual al escalar.
- pruebas_g1a.py (sha256 e8e4b5b07df77a0a85e6cbfd5c73f0db0aa183c0d6e6dbbd8656cbe358e5d076) en brain-env sobre FlyWire, salida cruda en 01-pruebas/: **8 de 8 pasan**, rc 0 en 10,3 s.
  - los tres grupos de FlyWire (pesadas inhibitorias, pesadas excitatorias, livianas) dan los mismos 6 números que el censo;
  - M queda contenido en L (0 pares fuera);
  - G0 con la Y real, por bloques contra un ajuste completo independiente: diferencia máxima en el predictor lineal 4,6e-9, misma verosimilitud, 10 iteraciones cada uno (0,14 s contra 0,64 s); quedan 115 X, 583 D′ y 66.911 pares informativos;
  - control del comparador: con L permutada la diferencia sube a 0,127, así que la comparación podía dar rojo;
  - una sola Y sintética con β = 0,7 sobre un banco de 20 recableados: β̂ 0,5859 por bloques y 0,5859 completo (diferencia 2e-11), errores del modelo y Vx, Vd, V0 iguales a un sándwich denso, β̂ a 1,0 error robusto del plantado;
  - β̃ vectorizado igual al escalar en las 21 listas (5e-15);
  - banco determinista con la misma semilla y distinto con otra; grados, unicidad y lado conservados; en promedio sólo 8,9 % de las aristas reales sobreviven a cada recableado.
- El primer intento de las pruebas murió por un error del propio script de pruebas (dos argumentos con el mismo nombre), con pruebas_g1a.py sha256 f33dedea7591d8573ab9e15f26eb45864fd37d011463beb580349fb6752f76fc; queda en 01-pruebas/intento1/. g1a.py no cambió entre los dos intentos.
- **Ninguna réplica de la calibración y ningún cruce de la Y real con el M real.**
