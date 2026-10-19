#!/usr/bin/env python3
"""H_PARES_DATOS: prueba unitaria del instrumento y del agregador (sello tools/pares/SELLO-PARES-DATOS.md, 0d30190).

L_IGUAL: el L con guarda da lo mismo que rv.cv_ridge, rv.ridge_ajustar, rv.ridge_predecir y lm.lector con ensayos de
los dos estados, y la guarda predice 0 cuando falta un estado. Ademas: subconjuntos anidados y deterministas, PCA
contra la SVD, proyecciones deterministas, W_n sin fondo, y las reglas de decision del agregador con datos sinteticos.
No usa el conectoma. Salida: 0 si pasan todas; 3 si falla alguna.
"""
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pares_datos as pd  # noqa: E402
import agregar_pares as ag  # noqa: E402

rv, lm, tm = pd.rv, pd.lm, pd.tm


def pr(s):
    print(s, flush=True)


def datos_sinteticos(n, d, semilla):
    rng = np.random.default_rng(semilla)
    v = rng.random(n) < 0.5
    y = np.where(v, rng.choice(tm.CLASES[True], n), rng.choice(tm.CLASES[False], n))
    F = rng.standard_normal((n, d))
    F[:, 0] += 3.0 * y
    F[:, 1] -= 1.5 * y
    return F, y, v


def prueba_l_igual():
    F, y, v = datos_sinteticos(300, 40, 5)
    pl = rv.pliegues(300)
    cv1, acc1 = rv.cv_ridge(F, y, v, pl, rv.LAMBDAS_R)
    cv2, acc2 = pd.validar(F, y, v, pl, rv.LAMBDAS_R)
    cv_igual = bool(np.array_equal(cv1, cv2) and np.array_equal(acc1, acc2))
    ok = cv_igual
    info, mod1 = lm.lector(F, y, v)
    lam, cv, mod2 = pd.lector(F, y, v)
    Ft, yt, vt = datos_sinteticos(120, 40, 6)
    p1, p2 = lm.leer(mod1, Ft, vt), pd.leer(mod2, Ft, vt)
    m1 = rv.ridge_ajustar(F, y, v, np.arange(300), rv.LAMBDAS_R)
    m2 = pd.ajustar(F, y, v, np.arange(300), rv.LAMBDAS_R)
    q1 = rv.ridge_predecir(m1, Ft, vt, np.arange(120))
    q2 = pd.predecir(m2, Ft, vt, np.arange(120), len(rv.LAMBDAS_R))
    val_igual = bool(np.array_equal(cv, np.array(info["validacion"])))
    acierto = float((p2 == yt).mean())
    ok = ok and lam == info["elegida"] and bool(np.array_equal(p1, p2)) and val_igual
    ok = ok and bool(np.array_equal(q1, q2)) and acierto > 0.6
    pr("PRUEBA L_IGUAL cv_ridge_igual=%s lambda=%g (lm %g) validacion_igual=%s predicciones_iguales=%s matriz_iguales=%s "
       "acierto=%.3f -> %s" % (cv_igual, lam, info["elegida"], val_igual, bool(np.array_equal(p1, p2)),
                              bool(np.array_equal(q1, q2)), acierto, ok))
    return ok


def prueba_guarda():
    rng = np.random.default_rng(7)
    F = rng.standard_normal((40, 10))
    v = np.ones(40, dtype=bool)
    y = rng.choice(tm.CLASES[True], 40)
    lam, cv, mod = pd.lector(F, y, v)
    vt = np.array([True, False, False, True])
    p = pd.leer(mod, rng.standard_normal((4, 10)), vt)
    ok = bool(p[1] == 0 and p[2] == 0 and np.isin(p[vt], tm.CLASES[True]).all() and np.isfinite(cv).all())
    v2 = np.array([True, False, False, False, False, False])
    y2 = np.array([2, 0, 1, 0, 1, 0])
    F2 = rng.standard_normal((6, 10))
    lam2, cv2, mod2 = pd.lector(F2, y2, v2)
    p2 = pd.leer(mod2, F2, v2)
    ok = ok and bool(p2[0] == 2 and np.isfinite(cv2).all() and np.isin(p2[~v2], tm.CLASES[False]).all())
    pr("PRUEBA GUARDA un_estado=%s un_ensayo_en_vuelo=%s -> %s" % (p.tolist(), p2.tolist(), ok))
    return ok


def prueba_subconjuntos():
    sub = pd.subconjuntos(2400, 20)
    ok = pd.anidados(sub, 2400) and sorted(sub) == list(pd.NS)
    ok = ok and pd.huella(sub) == pd.huella(pd.subconjuntos(2400, 20))
    ok = ok and bool(np.array_equal(sub[6][0], np.sort(np.random.default_rng([2059, 0]).permutation(2400)[:6])))
    ok = ok and len(sub[2400]) == 1 and bool(np.array_equal(sub[2400][0], np.arange(2400)))
    ok = ok and all(len(sub[n]) == 20 for n in pd.NS if n < 2400)
    chico = pd.subconjuntos(600, 2)
    ok = ok and pd.anidados(chico, 600) and sorted(chico) == [6, 12, 24, 48, 96, 192, 384, 600]
    malo = {6: [np.array([0, 1, 2, 3, 4, 5])], 12: [np.arange(6, 18)]}
    ok = ok and not pd.anidados(malo, 2400)
    pr("PRUEBA SUBCONJUNTOS n=%s anidados=%s deterministas=True -> %s" % (sorted(sub), pd.anidados(sub, 2400), ok))
    return bool(ok)


def prueba_pca():
    rng = np.random.default_rng(8)
    X = rng.standard_normal((300, 500)) * np.linspace(3.0, 0.1, 500)
    m, V, var, orto = pd.pca(X, 50)
    Z = (X - m) @ V
    U, S, _ = np.linalg.svd(X - m, full_matrices=False)
    ok = bool(orto < pd.TOL_ORTO and np.allclose(np.abs(Z), np.abs(U[:, :50] * S[:50]), atol=1e-8) and
              abs(var - float((S[:50] ** 2).sum() / (S ** 2).sum())) < 1e-10)
    P1, P2 = pd.proyeccion(3, 500), pd.proyeccion(3, 500)
    ok = ok and P1.shape == (500, pd.ANCHO) and bool(np.array_equal(P1, P2)) and not np.array_equal(P1, pd.proyeccion(4, 500))
    pr("PRUEBA PCA error_ortonormal=%.2e varianza=%.4f proyecciones_deterministas=%s -> %s" % (
        orto, var, bool(np.array_equal(P1, P2)), ok))
    return ok


def prueba_w_n():
    rng = np.random.default_rng(9)
    L = rng.random((50, 40, 6))
    y = np.array([0, 2, 0, 1] * 12 + [3, 4])
    v = np.array([True, True, False, False] * 12 + [True, True])
    S_sin = np.array([1, 3, 48, 49])
    S_con = np.arange(50)
    a = pd.w_n(L, y, v, L, y, v, S_sin)
    b = pd.w_n(L, y, v, L, y, v, S_con)
    ok = bool(a is None and isinstance(b, float) and 0.0 <= b <= 1.0)
    pr("PRUEBA W_N sin_fondo=%s con_fondo=%s -> %s" % (a, b is not None, ok))
    return ok


def sintetico(dfly, dpca, dproy, dcru, w, a96, semilla):
    rng = np.random.default_rng(semilla)
    X = {}
    for c in ag.CELDAS:
        base = 0.85 + 0.01 * rng.standard_normal((9, 20))
        fly = np.stack([base + dfly + 0.002 * rng.standard_normal((9, 20)) for _ in range(10)])
        proy = np.stack([base + dproy + 0.002 * rng.standard_normal((9, 20)) for _ in range(10)])
        cr, pc = base + dcru, base + dpca
        for M in (cr, pc):
            M[4] = a96
        proy[:, 4, :] = a96
        X[c] = dict(FLY=fly, PROY_L=proy, CRUDO=cr, PCA_L=pc, W=np.full(10, w) + 0.001 * rng.standard_normal(10))
    return X


def prueba_agregador():
    ok = True
    casos = (
        ("gana", (0.10, 0.0, 0.0, 0.0, 0.95, 0.80), ("SOSTENIDA", "SOSTENIDA", "SOSTENIDA")),
        ("empata_pca", (0.0, 0.0, -0.10, -0.10, 0.95, 0.80), ("REFUTADA", "SOSTENIDA", "SOSTENIDA")),
        ("alcanza_dia", (0.10, 0.0, 0.0, 0.0, 0.95, 0.95), ("SOSTENIDA", "SOSTENIDA", "REFUTADA")),
    )
    for nombre, (dfly, dpca, dproy, dcru, w, a96), esperado in casos:
        X = sintetico(dfly, dpca, dproy, dcru, w, a96, 11)
        ic = ag.bootstrap(X, list(ag.CELDAS), 4, 8, 300, ag.SEM_BOOT)
        ver = ag.decidir(ic)
        got = (ver["H_DATOS_EMBUDO"], ver["H_DATOS_CRUDO"], ver["H_DATOS_PRIMER_DIA"])
        ok = ok and got == esperado
        pr("PRUEBA AGREGADOR %s -> %s (esperado %s)" % (nombre, got, esperado))
    ic2 = ag.bootstrap(sintetico(0.1, 0, 0, 0, 0.95, 0.8, 11), list(ag.CELDAS), 4, 8, 300, ag.SEM_BOOT)
    ic3 = ag.bootstrap(sintetico(0.1, 0, 0, 0, 0.95, 0.8, 11), list(ag.CELDAS), 4, 8, 300, ag.SEM_BOOT)
    ok = ok and ic2 == ic3
    ok = ok and ag.n_alcanza(np.array([0.5, 0.945, 0.96]), 0.95, [6, 12, 24]) == 12
    ok = ok and ag.n_alcanza(np.array([0.5, 0.93, 0.96]), 0.95, [6, 12, 24]) == 24
    ok = ok and ag.n_alcanza(np.array([0.5, 0.6]), 0.95, [6, 12]) is None
    pr("PRUEBA AGREGADOR determinista=%s n_alcanza=ok -> %s" % (ic2 == ic3, ok))
    return bool(ok)


def main():
    pr("# md5 pares_datos.py = " + rv.md5(os.path.abspath(pd.__file__)))
    pr("# md5 agregar_pares.py = " + rv.md5(os.path.abspath(ag.__file__)))
    res = [prueba_l_igual(), prueba_guarda(), prueba_subconjuntos(), prueba_pca(), prueba_w_n(), prueba_agregador()]
    ok = all(res)
    pr("PRUEBAS %d/%d -> %s" % (sum(res), len(res), "VALIDO" if ok else "INVALIDO"))
    rc = 0 if ok else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
