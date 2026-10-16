# 2026-10-14-045 · La mosca entera con líquidas: la intuición tiene media parte medida, y la otra mitad pide una vara externa

**Fecha:** 2026-10-15, 23:10 (America/Buenos_Aires) · **Método:** PROMETEO

## Pedido

Abraham, 15-oct 23:01, verbatim: «lo que yo intuyo es que estamos haciendo algo mal. el conectoma d ela mozca podria ser reproducido en su totalidad con nuronas liquidas. una vez desarrollado y normalizado cn nuestros estandares, estudiarlo y reconocer todas las propiedas, destilarlas y empaquetarlas para trapolar». Contexto elegido: el Doc de la 2026-10-12-011 («No es la neurona: el motivo de 28 tiene el 3% de la entrada de sus descendentes»).

## Veredicto primero

- [MEDIDO, 2026-10-12-011] Sí estamos haciendo algo mal, y está medido. El motivo de 28 neuronas con el que se probó el escape lleva 539 de las 18.191 sinapsis de entrada de sus 4 descendentes (2,96%) y ninguna de las 7.889 inhibitorias (43,4%). Recortar así le saca a la mosca casi todo lo que la hace mosca.
- [MEDIDO, 2026-10-14-038 y 2026-10-14-041] Cuando el sujeto creció a 33.489 neuronas (R2), el cableado le ganó a sus barajados con lector entrenado: H_LECTOR_CABLEADO y H_TAU_LIBRE SOSTENIDAS, p = 1/41 en las cuatro celdas. La escala ayuda: esa mitad de la intuición ya tiene respaldo.
- [CONCLUSIÓN] La otra mitad no se sostiene tal cual. El conectoma no trae constantes de tiempo, umbrales, neuromodulación, uniones eléctricas, plasticidad ni cuerpo, así que «reproducir en su totalidad» no sale del cableado solo. La líquida agrega una τ por neurona: más parámetros libres, no menos. Y «reconocer todas las propiedades» sin una vara externa es pescar: H_RIVAL (REFUTADA) mostró que en tareas inventadas por nosotros una regla o un lector sobre la entrada cruda le gana al cableado.
- [CONCLUSIÓN] Lo que hacemos mal no es la neurona (la 011 ya lo dijo) sino la vara: validamos contra tareas propias con lector entrenado. Los que avanzaron validaron contra la mosca:
  1. **Shiu et al., Nature 2024** (DOI 10.1038/s41586-024-07763-9): LIF del cerebro entero con un solo parámetro libre, signo por neurotransmisor. Predicen qué neuronas responden al azúcar y al agua, y que el azúcar activa la motora MN9, validado con optogenética y conducta. Con los pesos barajados (misma distribución global), MN9 se activa en 1 de 100 simulaciones contra el 100% con el conectoma real.
  2. **Lappalainen et al., Nature 2024** (FlyVis, DOI 10.1038/s41586-024-07939-3): fijan el cableado de 64 tipos del camino de movimiento, aprenden los parámetros desconocidos con una tarea y sus predicciones coinciden con registros de 26 estudios.
- [MEDIDO en la 011, sin md5 contra el original] Nuestro parquet tiene las columnas del de Shiu (Presynaptic_ID, Postsynaptic_ID, Presynaptic_Index, Postsynaptic_Index, Connectivity, Excitatory, Excitatory x Connectivity) y su convención de signo (glutamato inhibitorio, 21.863 de 24.804). Su código es público y está preparado para v783 (`philshiu/Drosophila_brain_model`, Brian 2).
- [RECOMENDACIÓN] Tu plan, con la vara puesta, en cuatro pasos y en este orden:
  1. Correr el LIF de Shiu sobre nuestro parquet y reproducir azúcar a MN9 (y su control de pesos barajados) como referencia.
  2. Cambiar la LIF por nuestra líquida (SparseLTC) en el cerebro entero: mismo estímulo, misma lectura (tasa de MN9 y conjunto de neuronas activadas), sin lector entrenado.
  3. Contra nuestros nulos: pesos barajados como Shiu, más grado y región preservados.
  4. Recién si pasa, destilar: el subgrafo más chico que conserva la predicción dentro de un margen sellado. Eso es lo que se empaqueta y lo que podría ir a edge con DBC3.
  - Falsador: la líquida entera no reproduce lo que Shiu validó, o no le gana a sus barajados.
- [NO MEDIDO] Todo lo de la recomendación; el md5 de nuestro parquet contra el `Connectivity_783.parquet` de Shiu; el tiempo del cerebro entero en brain-env (2 núcleos, ocupada con la réplica de H_LECTOR) o en Actions; si Brian 2 instala en Actions.

## Herramientas y máquina

- Web: Shiu et al. 2024 (Nature y su preprint en PMC), su repositorio, Lappalainen et al. 2024. Nada medido nuevo.
- ClickUp: lectura del Doc de la 2026-10-12-011.
- brain-env: sólo escritura y prueba en copia del parche del CONTEXTO; la réplica de H_LECTOR sigue corriendo sin tocarla.
- GitHub: `push_files` a `main` (esta respuesta, el parche del CONTEXTO y su workflow).
- ClickUp: Doc público de la 045.
- Delicado: no. Ningún merge, nada a Zenodo ni Kaggle.

## Archivos

- `docs/agents/respuestas/2026-10-14-045-la-mosca-entera-con-liquidas-necesita-una-vara-externa.md` (esta).
- `tools/contexto/actualizar_contexto_2026-10-14-045.py` y `.github/workflows/contexto-2026-10-14-045.yml` (se borra al aplicarse).

## NO MEDIDO

1. Reproducir azúcar a MN9 con el LIF de Shiu sobre nuestro parquet.
2. La líquida en el cerebro entero con estímulo y lectura de Shiu, y contra nulos.
3. La destilación a un subgrafo mínimo.
4. Tiempo y memoria del cerebro entero en las tres máquinas.

## Antes de firmar

- El «1 de 100» y el «100%» de Shiu salen del extracto de la versión de Nature (Supplementary Table 1d citada en el texto), leído en el buscador y no en el PDF.
- Los 64 tipos y los 26 estudios son del resumen de Lappalainen.
- «Nuestro parquet es el de Shiu» está apoyado en columnas y convención de signo (011), no en md5: queda NO MEDIDO.
- Las 33.489 neuronas de R2 salen del log de la réplica en brain-env (`SUJETO R2 neuronas=33489 entradas=564`).
- La recomendación es opinión. Lo que la tiraría: que la líquida entera no se pueda correr en ninguna de las tres máquinas, o que el paso 1 no reproduzca a Shiu sobre nuestro parquet.

--- METODO PROMETEO ---
Rol: implementa. Delicado: no.
Máquinas: brain-env (prueba del parche), web y ClickUp (lectura).
Artefactos: esta respuesta, el parche del CONTEXTO y su workflow; Doc de ClickUp de la 045.
