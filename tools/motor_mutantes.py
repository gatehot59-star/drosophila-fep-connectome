#!/usr/bin/env python3
"""Prueba de mutacion para src/motor.py.

Por que existe: un test que no puede dar rojo no mide nada, y la unica forma de
saber si puede dar rojo es romper el codigo a proposito y exigir que lo detecte.
Sin esto, "25 tests en verde" es una afirmacion sobre la cantidad de tests, no
sobre su poder de deteccion.

Cada fila de MUTS rompe UNA cosa concreta del motor y declara que test tendria
que encenderse. Si una mutacion pasa en VERDE, ese test es decoracion y hay que
arreglarlo o borrarlo.

Uso:
    python3 tools/motor_mutantes.py --motor src/motor.py

Medido el 2026-08-25 sobre la v2: 9 de 10 detectadas por --self-test-only, y la
decima (M10) solo se puede detectar con datos cargados, asi que se corre aparte
con --synthetic. Total 10/10.

La historia de M2 conviene leerla: al romper la re-medicion del radio espectral
por iteracion de potencia, el veredicto seguia en OK porque ARPACK tapaba el
defecto. Un instrumento que salva al otro esta bien; uno que ESCONDE que el otro
esta roto, no. De ese escape salio el cruce entre los dos instrumentos que ahora
tiene normalize_spectral.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

# (nombre, ancla a reemplazar, reemplazo, test que deberia encenderse)
MUTS = [
    ("M1_sin_fundir_duplicados",
     "    pre_c, post_c, w_c, merged = coalesce_edges(pre, post, w, n)",
     "    pre_c, post_c, w_c, merged = pre, post, w, 0",
     "los_dos_brazos_comparten_las_MAGNITUDES"),
    ("M2_no_re_medir_el_radio_espectral",
     "    rho_post_power, post_conv = spectral_radius_power(Ws, n_iter=n_iter, tol=tol)",
     "    rho_post_power, post_conv = rho_pre, pre_conv",
     "normalizacion_*_queda_en_el_target"),
    ("M3_los_dos_brazos_son_la_misma_funcion",
     "        data = np.where(is_inh[pre_c], -mag, mag).astype(np.complex128)",
     "        rng = np.random.default_rng(seed)\n        data = mag * np.exp(1j * (np.where(is_inh[pre_c], np.pi, 0.0) + rng.normal(0.0, phase_jitter, pre_c.shape[0])))",
     "los_dos_brazos_NO_son_la_misma_matriz"),
    ("M4_piso_de_p_mal_calculado",
     "    return 2.0 / (n_nulls + 1.0)",
     "    return 1.0 / (n_nulls + 1.0)",
     "piso_de_p_*"),
    ("M5_rankdata_vectorizado_roto",
     "        avg = start + (c - 1) / 2.0 + 1.0",
     "        avg = start + 1.0",
     "rankdata_vectorizado_coincide_con_el_ingenuo"),
    ("M6_activacion_sin_cota",
     "    mag = np.abs(out)\n    over = mag > clip",
     "    mag = np.abs(out)\n    over = mag > 1e300",
     "tanh_acotada_respeta_el_clip"),
    ("M7_guard_de_tau_desactivado",
     "    if worst >= limit:",
     "    if False:",
     "tau_rechaza_0.48"),
    ("M8_guard_de_tautologia_desactivado",
     "        if sd == 0.0:",
     "        if False:",
     "el_test_global_marca_NO_TESTEABLE_con_sd_cero"),
    ("M9_cosine_premia_cadaveres",
     '        return float("nan")\n    return 1.0 - float(np.dot(a, b)) / (na * nb)',
     '        return 1.0\n    return 1.0 - float(np.dot(a, b)) / (na * nb)',
     "cosine_de_un_vector_muerto_es_NaN"),
]

# Esta mutacion rompe un invariante que solo se testea CON datos cargados, asi
# que --self-test-only no puede verla por construccion. Se corre aparte.
MUT_CON_DATOS = (
    "M10_null_CP_sortea_en_vez_de_permutar",
    "        p[idx] = rng.permutation(post[idx])",
    "        p[idx] = rng.choice(np.where(block_of_node >= 0)[0], idx.shape[0])",
    "cp_preserva_grado_entrante",
)


def run_mutant(base_src, old, new, extra_args, timeout):
    """Aplica una mutacion, corre el motor mutado y devuelve (rojo, fails, rc)."""
    if old not in base_src:
        return None, [], None
    src = base_src.replace(old, new, 1)
    fd, path = tempfile.mkstemp(suffix="_mut_motor.py", dir=".")
    os.close(fd)
    try:
        with open(path, "w") as f:
            f.write(src)
        proc = subprocess.run([sys.executable, path] + extra_args,
                             capture_output=True, text=True, timeout=timeout)
        out = proc.stdout + proc.stderr
        fails = re.findall(r"FAIL  ([^\s:]+)", out)
        rojo = len(fails) > 0 or proc.returncode != 0
        return rojo, fails, proc.returncode
    finally:
        if os.path.exists(path):
            os.remove(path)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Prueba de mutacion de src/motor.py")
    ap.add_argument("--motor", default="src/motor.py")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--synthetic", nargs=2, type=int, default=[800, 16000],
                    metavar=("N", "E"),
                    help="grafo para la mutacion que necesita datos")
    args = ap.parse_args(argv)

    base = open(args.motor).read()
    rows = []

    for name, old, new, expect in MUTS:
        rojo, fails, rc = run_mutant(base, old, new, ["--self-test-only"], args.timeout)
        if rojo is None:
            rows.append((name, "NO_APLICADA", "el ancla no existe en el archivo"))
            continue
        rows.append((name,
                     "ROJO" if rojo else "VERDE (el test NO mide)",
                     ",".join(fails[:3]) if fails else "exit=" + str(rc)))

    name, old, new, expect = MUT_CON_DATOS
    extra = ["--synthetic", str(args.synthetic[0]), str(args.synthetic[1]),
             "--nulls", "2", "--steps", "30"]
    rojo, fails, rc = run_mutant(base, old, new, extra, args.timeout)
    if rojo is None:
        rows.append((name, "NO_APLICADA", "el ancla no existe en el archivo"))
    else:
        rows.append((name,
                     "ROJO" if rojo else "VERDE (el test NO mide)",
                     ",".join(fails[:3]) if fails else "exit=" + str(rc)))

    print("=" * 100)
    print("PRUEBA DE MUTACION - cada fila rompe una cosa y exige que algun test lo detecte")
    print("=" * 100)
    print("%-40s %-24s %s" % ("mutacion", "resultado", "test que dio rojo"))
    print("-" * 100)
    detectadas = 0
    for nm, res, det in rows:
        print("%-40s %-24s %s" % (nm, res, det[:36]))
        if res == "ROJO":
            detectadas += 1
    print("-" * 100)
    print("DETECTADAS: %d de %d mutaciones" % (detectadas, len(rows)))
    return 0 if detectadas == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
