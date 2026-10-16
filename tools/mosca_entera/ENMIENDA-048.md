# Enmienda 048 al sello de H_MOSCA_ENTERA: latencia y nulos a ganancia igual

**Sellada:** 2026-10-16, 00:50 (America/Buenos_Aires), respuesta 2026-10-14-048, pedido de Abraham (botón `enmienda_mosca_entera_048`, 00:48).
**Enmienda a:** `tools/mosca_entera/SELLO-MOSCA-ENTERA.md` (`500f66d`, md5 55bc4c76657e35f341300d0e082c7ebe).
**Por qué:** el humo de la 047 (bot `1603190`) mostró dos fallas del sello. (1) En la ventana 151 a 200, LIQ y TASA leen el mismo punto fijo (MN9 difiere en 3,2e-10): H_ENTERA_LIQ no puede discriminar. (2) Llevar cada grafo a radio 0,9 da a cada sinapsis de los nulos de 6 a 8 veces la ganancia del real (radio crudo 2164,29 contra 267,52 y 339,68), mientras el LIF de Shiu usa pesos crudos.

**Qué no cambia:** brazos, nulos, controles, hipótesis y bandas de la 046. Todo se corre y se reporta igual. La enmienda **agrega**; no saca ni mueve nada.

**Estado al sellar:** CORRER no corrió. Visto en el humo: LIQ y TASA con τ 30 (sólo la media en la ventana, sin trayectoria), PROX, SHUF_W k0 y SHUF_G k0 normalizados a 0,9, y el LIF real y SHUF_W k0 con 2 ensayos. No visto: ninguna latencia, ningún nulo a ganancia igual, los 30 ensayos LIF reales y todo lo demás.

## 1. Marca de degeneración para H_ENTERA_LIQ

La banda de la 046 se aplica tal cual. Además, si la mediana sobre τ 30 a 39 de max|r_LIQ − r_TASA| en la ventana es menor que 1e-6, el veredicto se imprime como `REFUTADA_DEGENERADA` y **no cuenta como evidencia** contra la líquida: los brazos son iguales en lo que se lee.

## 2. H_ENTERA_LAT: la líquida contra la tasa, leídas por latencia

- **Latencia LIF:** para cada neurona de S_LIF y cada ensayo real en que dispara, el tiempo de su primera espiga desde el inicio del estímulo (t = 0). Su latencia es la mediana sobre esos ensayos.
- **Latencia LIQ y TASA:** para cada neurona con r > 0, el primer paso t (de 1 a 200) en que z_t ≥ 0,5·r, con r la media de la ventana 151 a 200 del mismo brazo, el mismo τ y la misma entrada del sello.
- **Conjunto:** S_LAT = neuronas de S_LIF con r > 0 en LIQ y en TASA para ese τ.
- **Estadístico:** ρ = Spearman (rangos promedio en empates) entre la latencia LIF y la del brazo, sobre S_LAT. D_LAT = mediana sobre τ 30 a 39 de ρ(LIQ) − ρ(TASA).
- **Precondiciones (si alguna falla, NO_MEDIDO):** REPRO_SHIU pasa; |S_LAT| ≥ 10 en las 10 τ; con τ 30, al menos el 1% de S_LAT tiene latencia distinta en LIQ y en TASA (si no, los brazos vuelven a ser la misma función).
- **Bandas:** D_LAT ≥ +0,05 → SOSTENIDA; D_LAT ≤ 0 → REFUTADA; en el medio, SIN_DECIDIR.
- **Se reporta además, sin banda:** ρ(LIQ) y ρ(TASA) con τ 30, y la mediana de cada uno sobre las 10 τ.

## 3. H_ENTERA_MN9_G1 y H_ENTERA_CONJUNTO_G1: nulos a ganancia igual

- **Nulos G1:** los mismos 40 SHUF_W y 40 SHUF_G de la 046 (misma función `nulo()`, semillas 0 a 39), pero cada uno se multiplica por **el factor del real**, c = 0,9 / r_real, con r_real el radio crudo del grafo real medido en la misma corrida, en vez de su propio factor. Cada sinapsis pesa lo mismo que en el real, como en el LIF. Los radios esperados son ~0,11 (W) y ~0,14 (G); se miden y se reportan.
- **Dinámica:** la de LIQ con τ 30, la misma entrada y la misma ventana.
- **H_ENTERA_MN9_G1:** r_MN9 real (LIQ, τ 30) contra los 40 G1 de cada tipo, con las mismas bandas que H_ENTERA_MN9.
- **H_ENTERA_CONJUNTO_G1:** J real contra los 40 G1 de cada tipo, con las mismas bandas que H_ENTERA_CONJUNTO, con K y S_LIF de la 046.

## 4. Cómo se leen juntas (fijado antes de ver)

| MN9 contra nulos a 0,9 | MN9 contra nulos G1 | Lectura |
|---|---|---|
| SOSTENIDA | SOSTENIDA | el cableado lleva el azúcar a MN9 mejor que sus barajados, con y sin igualar ganancia |
| no SOSTENIDA | SOSTENIDA | la ventaja del real es ganancia concentrada en lazos, no ruteo específico hacia MN9 |
| SOSTENIDA | no SOSTENIDA | ruteo específico que la ganancia de los nulos G1 no alcanza a mostrar; se reporta como tensión |
| no SOSTENIDA | no SOSTENIDA | la líquida en el cableado no reproduce a MN9 por encima de sus barajados |

La misma tabla vale para CONJUNTO.

## 5. Expectativa honesta

- H_ENTERA_LIQ: `REFUTADA_DEGENERADA`, casi seguro.
- H_ENTERA_LAT: dudosa. La líquida acelera las neuronas con |u| grande, pero τ es al azar por neurona y no biofísico. Espero D_LAT chico, entre −0,05 y +0,05.
- H_ENTERA_MN9_G1 y _CONJUNTO_G1: espero SOSTENIDA. Con radio 0,11 a 0,14 la señal de los nulos se apaga en pocos saltos. Por eso la fila «no SOSTENIDA / SOSTENIDA» de la tabla es la más probable, y se va a leer como ganancia en lazos, no como ruteo.

## 6. Instrumento, máquina y orden

- `liq_entera.py` agrega latencias por brazo y el modo de nulos G1. `lif_shiu.py` agrega la latencia por neurona desde el parquet de espigas. `agregar_mosca_entera.py` agrega las bandas de esta enmienda y la marca de degeneración.
- La prueba suma, como mínimo: latencia a mano en una cadena; que LIQ y TASA difieran en latencia donde la prueba de la 047 no miraba; que los nulos G1 usen el factor del real; y las bandas nuevas con números plantados, incluido un caso que tiene que dar REFUTADA.
- **Máquina:** Actions. Orden: instrumento, prueba, humo, y recién después CORRER con todo junto. El workflow de CORRER no lista su propio MD5SUMS.
- La destilación sigue sellándose aparte, y sólo si MN9 y CONJUNTO salen SOSTENIDA contra las dos familias de nulos.

--- METODO PROMETEO ---
Rol: implementa (sello). Delicado: no.
Máquina: ninguna para la enmienda; los números citados son del humo de la 047.
