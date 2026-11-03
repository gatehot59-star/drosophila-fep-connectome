# Evidencia de 2026-11-03-004

Los tres scripts se ejecutaron inline en `brain-env`, por MUDH Gateway (Python 3.12.14, NumPy 2.5.3), el 3-nov-2026 entre las 13:14 y las 13:20 ART aproximadamente. El orden fue `consultar_actions.py`, `anotaciones_y_huellas.py` y `costo_y_npz.py`. Están transcriptos sin cambios, y cada `.log` es su stdout completo, sin recortes. Los tres terminaron con exit 0.

Ninguno escribe en el repo:

- `anotaciones_y_huellas.py` deja copias de lo publicado en `/workspace/a1/publicado_73cc060/` y `/workspace/a1/publicado_7966f71/`.
- `costo_y_npz.py` lee esas copias y escribe tres npz temporales en `/workspace/a1/tmp*`.

La API pública de GitHub sin token permite 60 consultas por hora por IP. El texto de los logs de Actions no se puede leer: devuelve 403.
