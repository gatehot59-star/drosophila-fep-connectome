#!/usr/bin/env python3
"""Prueba del instrumento de H_RIVAL (respuesta 2026-10-14-033), sin datos del conectoma.

Cada chequeo puede dar rojo, y uno esta hecho para dar rojo a proposito: un solver con el lambda al doble tiene que
notarse contra ept._ridge_fit. Salida 0 si pasan todos; 1 si falla alguno.
"""
import os
import sys
import tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import rival_mosca as rv  # noqa: E402
import agregar_rival as ag  # noqa: E402

RES = []


def chk(nombre, ok):
    RES.append(bool(ok))
    print("%s -> %s" % (nombre, "OK" if ok else "FALLA"), flush=True)


def main():
    rng = np.random.default_rng(0)
    for n, d in ((120, 300), (300, 40)):
        A = rng.standard_normal((n, d))
        Bm = rng.standard_normal((50, d))
        Y = np.eye(3)[rng.integers(0, 3, n)]
        prim = rv.ept._ridge_fit(A, Y, rv.ept.LAMBDAS)
        Ac, am, ym, alfas = rv._dual(A.copy(), Y, rv.ept.LAMBDAS)
        G = (Bm - am) @ Ac.T
        md = max(float(np.abs(Bm @ W + b - (G @ al + ym)).max()) for (W, b), al in zip(prim, alfas))
        chk("DUAL_IGUAL_PRIMAL n=%d d=%d max_dif=%.2e" % (n, d, md), md < 1e-7)
        Ac2, am2, ym2, alfas2 = rv._dual(A.copy(), Y, [2.0 * x for x in rv.ept.LAMBDAS])
        G2 = (Bm - am2) @ Ac2.T
        md2 = max(float(np.abs(Bm @ W + b - (G2 @ al + ym2)).max()) for (W, b), al in zip(prim, alfas2))
        chk("ROJO_A_PROPOSITO lambda al doble n=%d d=%d max_dif=%.2e" % (n, d, md2), md2 > 1e-6)

    cl = np.array([0, 2, 3, 4])
    y = rng.choice(cl, 400)
    X = rng.standard_normal((400, 60))
    X[:, 0] += y
    Xt = rng.standard_normal((100, 60))
    Xt[:, 0] += rng.choice(cl, 100)
    pe, le = rv.ept.ridge(X, y, Xt, cl)
    pm, lm = rv.ridge_015(X, y, Xt, cl)
    chk("RIDGE_015_IGUAL_A_EPT lambda=%g/%g iguales=%d/%d" % (le, lm, int((pe == pm).sum()), len(pe)),
        np.array_equal(pe, pm) and le == lm)

    v = rng.random(400) < 0.5
    yy = np.where(v, rng.choice(rv.tm.CLASES[True], 400), rng.choice(rv.tm.CLASES[False], 400))
    XX = rng.standard_normal((400, 30))
    XX[:, 0] += yy
    mods = rv.ridge_ajustar(XX, yy, v, np.arange(300), rv.LAMBDAS_R)
    P = rv.ridge_predecir(mods, XX, v, np.arange(300, 400))
    enc = all(np.isin(P[k][v[300:] == st], rv.tm.CLASES[st]).all() for k in range(len(rv.LAMBDAS_R)) for st in (True, False))
    chk("RIDGE_POR_ESTADO forma=%s en_clases=%s" % (P.shape, enc), P.shape == (10, 100) and enc)

    pl = rv.pliegues(23)
    part = sorted(np.concatenate([it for _, it in pl]).tolist()) == list(range(23))
    disj = all(len(np.intersect1d(ia, it)) == 0 for ia, it in pl)
    mod5 = all((it % 5 == j).all() for j, (_, it) in enumerate(pl))
    chk("PLIEGUES particion=%s disjuntos=%s modulo5=%s" % (part, disj, mod5), part and disj and mod5)

    U = rng.standard_normal((5, 40, 6))
    chk("INTEGRADOR_NULO", np.array_equal(rv.integrar(U, np.ones(6)), U))
    z = np.zeros((5, 6))
    man = np.empty_like(U)
    for t in range(40):
        z = 0.5 * z + 0.5 * U[:, t, :]
        man[:, t, :] = z
    chk("INTEGRADOR_MEDIO", np.array_equal(rv.integrar(U, np.full(6, 0.5)), man))
    a1, a2, b1 = rv.t_k(10), rv.t_k(10), rv.t_k(11)
    rango = bool((a1 >= rv.DT / 0.18 - 1e-12).all() and (a1 <= rv.DT / 0.06 + 1e-12).all())
    chk("TK determinista=%s distinto=%s rango=%s" % (np.array_equal(a1, a2), not np.array_equal(a1, b1), rango),
        np.array_equal(a1, a2) and not np.array_equal(a1, b1) and rango)
    s = "0120340"
    chk("PRED_STR ida y vuelta", rv.a_str(rv.de_str(s)) == s)

    vm = rng.random(240) < 0.5
    ymm = np.where(vm, rng.integers(0, 4, 240), rng.integers(0, 3, 240))
    Xm = rng.standard_normal((240, 25))
    tr, te = np.arange(180), np.arange(180, 240)
    pE = rv.ept.mlp_mux(Xm[tr], ymm[tr], vm[tr], Xm[te], vm[te], 3, 7)
    pM = rv.mlp_predecir(rv.mlp_ajustar(Xm, ymm, vm, tr, 3, rv.ept.CLASES, 7), Xm, vm, te)
    chk("MLP_IGUAL_A_EPT iguales=%d/%d" % (int((pE == pM).sum()), len(pE)), np.array_equal(pE, pM))

    S, N, Z = "SUPERA_POR_MARGEN", "NO_SUPERA", "SIN_DECIDIR"
    chk("ETIQUETAS", ag.etiqueta(0.011, 0.03) == S and ag.etiqueta(-0.02, 0.0099) == N and
        ag.etiqueta(0.0, 0.02) == Z and ag.etiqueta(0.01, 0.02) == Z)
    v1 = ag.veredictos({"RIDGE": S, "MLP": S, "REGLA_TAU": S}) == ("SOSTENIDA", "SOSTENIDA")
    v2 = ag.veredictos({"RIDGE": N, "MLP": S, "REGLA_TAU": Z}) == ("REFUTADA", "SIN_DECIDIR")
    v3 = ag.veredictos({"RIDGE": S, "MLP": Z, "REGLA_TAU": S}) == ("SIN_DECIDIR", "SOSTENIDA")
    v4 = ag.veredictos({"RIDGE": S, "MLP": S, "REGLA_TAU": N}) == ("REFUTADA", "REFUTADA")
    chk("VEREDICTOS", v1 and v2 and v3 and v4)
    bp = ag.boot_primaria({r: np.full((6, 10), 0.03) for r in ag.RIVALES})
    chk("BOOT_CONSTANTE", all(abs(bp[r]["lo"] - 0.03) < 1e-12 and abs(bp[r]["hi"] - 0.03) < 1e-12 and
                              bp[r]["etiqueta"] == S for r in ag.RIVALES))
    Dv = {r: rng.normal(0.02, 0.01, (6, 10)) for r in ag.RIVALES}
    bp = ag.boot_primaria(Dv)
    idx = np.random.default_rng(ag.SEM_P).integers(0, 10, (ag.B, 10))
    lazo = np.array([Dv["RIDGE"][:, idx[b]].mean() for b in range(ag.B)])
    ok_l = (abs(np.percentile(lazo, ag.Q_LO) - bp["RIDGE"]["lo"]) < 1e-12 and
            abs(np.percentile(lazo, ag.Q_HI) - bp["RIDGE"]["hi"]) < 1e-12)
    chk("BOOT_PRIMARIA_IGUAL_AL_LAZO", ok_l and bp["RIDGE"]["lo"] < bp["RIDGE"]["D"] < bp["RIDGE"]["hi"])
    D2 = {r: rng.normal(0.0, 0.01, (6, 10, 10)) for r in ag.RIVALES}
    bs = ag.boot_secundaria(D2)
    r2 = np.random.default_rng(ag.SEM_S)
    it = r2.integers(0, 10, (ag.B, 10))
    ip = r2.integers(0, 10, (ag.B, 10))
    lazo2 = np.array([D2["MLP"][:, it[b]][:, :, ip[b]].mean() for b in range(ag.B)])
    chk("BOOT_SECUNDARIA_IGUAL_AL_LAZO", abs(np.percentile(lazo2, ag.Q_LO) - bs["MLP"]["lo"]) < 1e-12 and
        abs(np.percentile(lazo2, ag.Q_HI) - bs["MLP"]["hi"]) < 1e-12)
    rvac = ag.agregar(tempfile.mkdtemp())
    chk("AGREGADOR_SIN_ARCHIVOS_ES_INVALIDO", rvac["H_RIVAL"] == "INVALIDO" and rvac["H_TAU_JUSTO"] == "INVALIDO")
    print("PRUEBA %d/%d" % (sum(RES), len(RES)), flush=True)
    return 0 if all(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
