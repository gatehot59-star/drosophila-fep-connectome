#!/usr/bin/env python3
"""Agregador de H_DEBILES (respuesta 2026-10-14-016). Sellado antes de correr.

Junta los json de tools/debiles/debiles_mosca.py (60 de grilla y 4 de mezclas) con R2 del factorial 3
(results/factorial3_2026-10-13) y con el nucleo (results/nucleo_2026-10-14), los dos ya en git, y decide con reglas
fijadas antes de ver datos. MEZCLA = R2 con el nucleo intacto y las debiles con destinos barajados (k = 0 en la grilla).
  E1          E1[t, p, c] = MEZCLA menos R2 en la misma semilla de tau, de prueba y celda. Media; bootstrap de dos vias
              (tau y prueba) del agregador del nucleo (cb8a797b), B = 20.000, semilla 2040, percentiles 0,05 y 0,95;
              M = 0,01. H_DEBILES_ESPECIFICAS (importa cuales son): SOSTENIDA si hi < -M (barajarlas cuesta mas de
              1 punto); REFUTADA si lo > -M (barajarlas no cuesta mas de 1 punto); si no, SIN_DECIDIR.
  E2          E2[t, p, c] = MEZCLA menos NUCLEO, mismo pareo; semilla 2041. H_DEBILES_SUMAN (importa cuantas son):
              SOSTENIDA si lo > +M (barajadas igual suman mas de 1 punto sobre el nucleo); REFUTADA si hi < +M;
              si no, SIN_DECIDIR.
  LECTURA     ESPECIFICAS S y SUMAN R: pesa cuales son. S y S: pesan las dos cosas. R y S: pesa la cantidad.
              R y R: inconsistente (R2 le saca 4,59 al nucleo). Cualquier SIN_DECIDIR: no se lee.
  POR CELDA   el mismo bootstrap con alfa 0,05/6 (descriptivo).
  MEZCLAS     20 mezclas (k 0 a 19) en tau 0, prueba 2, 0,3|0,15, contra R2 real y nucleo real medidos en el mismo
              json: media, minimo, maximo, cuantas llegan a R2 real y cuantas caen al nucleo real (descriptivo).
  RECUPERADO  (MEZCLA - NUCLEO) / (R2 - NUCLEO) con las medias de la grilla (descriptivo).
Chequeos que invalidan: 60 json de grilla (10 taus x 6 celdas) y las 600 corridas sin repetir; 20 mezclas sin repetir
en 4 json; un solo json con los reales; todos validos y sin humo; md5 del instrumento sellado y de sus modulos; el
mismo nucleo sellado en todos; la misma mezcla (huella) en los 60 de grilla; regla propia, tau de las descendentes y
descendentes iguales al factorial 3 y al nucleo; la grilla del nucleo y la del factorial 3 completas; MEZCLA_IGUAL: la
grilla en tau 0, prueba 2, 0,3|0,15 da lo mismo que la mezcla k = 0 de los json de mezclas.
Uso: python3 tools/debiles/agregar_debiles.py <carpeta debiles> <carpeta factorial 3> <carpeta nucleo> [--humo]
Salida: EXIT_AGREGADO=0 si el veredicto global es VALIDO; 1 si no.
"""
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "nucleo"))
import agregar_nucleo as an  # noqa: E402  sellado (cb8a797b), sin cambios

CELDAS, TAUS, PRUEBAS, M = an.CELDAS, an.TAUS, an.PRUEBAS, an.M
MD5_DEB = "f28404c2ecb1ae84e0a58936964cb7e9"
PIN = dict(an.PIN, nucleo_mosca=an.MD5_NUCLEO)
NUCLEO = an.NUCLEO
N_MEZCLAS = 20
REAL_R2, REAL_NUCLEO = 0.9465, 0.9135
pr = an.pr


def especificas(lo, hi):
    if hi < -M:
        return "SOSTENIDA"
    if lo > -M:
        return "REFUTADA"
    return "SIN_DECIDIR"


def suman(lo, hi):
    if lo > M:
        return "SOSTENIDA"
    if hi < M:
        return "REFUTADA"
    return "SIN_DECIDIR"


def lectura(e, s):
    if "SIN_DECIDIR" in (e, s) or "NO_EVALUABLE" in (e, s):
        return "NO_SE_LEE"
    return {("SOSTENIDA", "REFUTADA"): "PESA_CUALES", ("SOSTENIDA", "SOSTENIDA"): "PESAN_LAS_DOS",
            ("REFUTADA", "SOSTENIDA"): "PESA_CUANTAS", ("REFUTADA", "REFUTADA"): "INCONSISTENTE"}[(e, s)]


def main():
    d, d3, dn = sys.argv[1], sys.argv[2], sys.argv[3]
    humo = "--humo" in sys.argv
    g = an.leer(d, "debiles_grilla_*.json")
    mz = an.leer(d, "debiles_mezclas_*.json")
    g3 = an.leer(d3, "factorial2_R2_CON_TASA_*.json")
    gn = an.leer(dn, "nucleo_grilla_*.json")
    pr("JSON grilla=%d mezclas=%d | factorial 3 grilla=%d | nucleo grilla=%d" % (len(g), len(mz), len(g3), len(gn)))
    todos = [r for _, r in g + mz]
    ok_val = bool(todos) and all(r.get("valido") is True for r in todos)
    sin_humo = bool(todos) and all(not r.get("humo") for r in todos)
    ok_md5 = bool(todos) and all(r.get("md5", {}).get("script") == MD5_DEB and
                                 all(r.get("md5", {}).get(k) == v for k, v in PIN.items()) for r in todos)
    ok_nuc = bool(todos) and all((r.get("nucleo", {}).get("aristas"), r.get("nucleo", {}).get("inhibitorias"),
                                  r.get("nucleo", {}).get("huella")) == NUCLEO for r in todos)
    huellas = set(r.get("mezcla", {}).get("huella") for _, r in g)
    ok_mez = len(huellas) == 1 and None not in huellas
    pr("CHEQUEO VALIDOS -> %s | SIN_HUMO -> %s | MD5 instrumento=%s y pines -> %s | NUCLEO_SELLADO -> %s" % (
        ok_val, sin_humo, MD5_DEB[:8], ok_md5, ok_nuc))
    pr("CHEQUEO MISMA_MEZCLA huellas=%s -> %s" % (sorted(str(h) for h in huellas), ok_mez))
    WD, RPD, PRPD, taudD, dnsD, dupD = an.tablas(g)
    W3, RP3, PRP3, taud3, dns3, dup3 = an.tablas(g3)
    WN, RPN, PRPN, taudN, dnsN, dupN = an.tablas(gn)
    todas = [(t, p, c) for t in TAUS for p in PRUEBAS for c in CELDAS]
    falt = [k for k in todas if k not in WD]
    falt3 = [k for k in todas if k not in W3]
    faltN = [k for k in todas if k not in WN]
    ok_plan = (not falt and len(g) == 60 and dupD == 0) or humo
    pr("CHEQUEO PLAN_GRILLA json=%d corridas=%d faltan=%d repetidas=%d | factorial 3 faltan=%d | nucleo faltan=%d -> %s"
       % (len(g), len(WD), len(falt), dupD, len(falt3), len(faltN), ok_plan and not falt3 and not faltN))
    comb = sorted(PRPD)
    iguales = sum(1 for k in comb if len(PRPD[k]) == 1 and PRP3.get(k) == PRPD[k] and PRPN.get(k) == PRPD[k] and
                  len(RPD.get(k, ())) == 1 and RP3.get(k) == RPD.get(k) and RPN.get(k) == RPD.get(k))
    regla_ok = bool(comb) and iguales == len(comb) and (len(comb) == len(PRUEBAS) * len(CELDAS) or humo)
    tau_ok = bool(taudD) and all(len(v) == 1 for v in taudD.values()) and all(
        taud3.get(st) == v and taudN.get(st) == v for st, v in taudD.items())
    dn_ok = len(dnsD) == 1 and dnsD == dns3 and dnsD == dnsN and all(
        r.get("dns_root") == list(next(iter(dnsD))) for _, r in mz)
    pr("CHEQUEO REGLA_IGUAL_F3_Y_NUCLEO combinaciones=%d iguales=%d -> %s" % (len(comb), iguales, regla_ok))
    pr("CHEQUEO TAU_DN_IGUAL -> %s | DN_IGUAL -> %s" % (tau_ok, dn_ok))
    acc, dup, reales = {}, 0, []
    for _, r in mz:
        for x in r.get("mezclas", []):
            dup += x["k"] in acc
            acc[x["k"]] = x["acierto"]
        if r.get("real_R2") is not None:
            reales.append((r["real_R2"], r["real_nucleo"]))
    plan_mz = (sorted(acc) == list(range(N_MEZCLAS)) and dup == 0 and len(reales) == 1) or humo
    pr("CHEQUEO PLAN_MEZCLAS mezclas=%d repetidas=%d json_con_reales=%d -> %s" % (len(acc), dup, len(reales), plan_mz))
    reales_ok = len(reales) == 1 and abs(reales[0][0] - REAL_R2) < 1e-9 and abs(reales[0][1] - REAL_NUCLEO) < 1e-9
    pr("CHEQUEO REALES R2 y nucleo=%s esperados=(%.4f, %.4f) -> %s" % (reales, REAL_R2, REAL_NUCLEO, reales_ok))
    g0 = WD.get((0, 2, "0.3|0.15"))
    mez_ok = g0 is not None and 0 in acc and abs(g0 - acc[0]) < 1e-12
    pr("CHEQUEO MEZCLA_IGUAL grilla=%s mezcla_k0=%s -> %s" % (g0, acc.get(0), mez_ok))
    valido = (ok_val and ok_plan and not falt3 and not faltN and regla_ok and tau_ok and dn_ok and plan_mz and ok_nuc
              and ok_mez and (humo or (sin_humo and ok_md5 and reales_ok and mez_ok)))
    if humo:
        pr("# HUMO: no se exigen el plan completo, SIN_HUMO, MD5, REALES ni MEZCLA_IGUAL; numeros sin valor")
    h_esp, h_sum = "NO_EVALUABLE", "NO_EVALUABLE"
    if not falt and not falt3 and not faltN:
        X = an.cubo(lambda t, p, c: WD[(t, p, c)])
        R = an.cubo(lambda t, p, c: W3[(t, p, c)])
        N = an.cubo(lambda t, p, c: WN[(t, p, c)])
        for nombre, E, sem, fun in (("E1 MEZCLA_menos_R2", X - R, 2040, especificas),
                                    ("E2 MEZCLA_menos_NUCLEO", X - N, 2041, suman)):
            rng = np.random.default_rng(sem)
            est, lo, hi = an.bootstrap(E.mean(2), 0.05, rng)
            v = fun(lo, hi)
            pr("%s W_mezcla=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d mayor=%d iguales=%d menor=%d -> %s" % (
                nombre, X.mean(), est, lo, hi, E.size, int((E > 0).sum()), int((E == 0).sum()), int((E < 0).sum()), v))
            for j, c in enumerate(CELDAS):
                e2, l2, h2 = an.bootstrap(E[:, :, j], 0.05 / 6, rng)
                pr("  CELDA %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s (descriptivo)" % (c, e2, l2, h2, fun(l2, h2)))
            if sem == 2040:
                h_esp = v
            else:
                h_sum = v
        pr("DESCRIPTIVO medias R2=%.4f nucleo=%.4f mezcla=%.4f RECUPERADO=%.3f" % (
            R.mean(), N.mean(), X.mean(), (X.mean() - N.mean()) / (R.mean() - N.mean())))
        for i, t in enumerate(TAUS):
            pr("DESCRIPTIVO TAU %d mezcla-R2=%+.4f mezcla-nucleo=%+.4f" % (t, (X - R)[i].mean(), (X - N)[i].mean()))
    if acc:
        a = np.array([acc[k] for k in sorted(acc)], dtype=np.float64)
        r2, rn = reales[0] if reales else (REAL_R2, REAL_NUCLEO)
        pr("MEZCLAS n=%d media=%.4f min=%.4f max=%.4f R2_real=%.4f nucleo_real=%.4f llegan_a_R2=%d caen_al_nucleo=%d "
           "(descriptivo)" % (len(a), a.mean(), a.min(), a.max(), r2, rn, int((a >= r2).sum()), int((a <= rn).sum())))
    if not valido:
        h_esp, h_sum = "NO_EVALUABLE", "NO_EVALUABLE"
    pr("HIPOTESIS H_DEBILES_ESPECIFICAS -> %s" % h_esp)
    pr("HIPOTESIS H_DEBILES_SUMAN -> %s" % h_sum)
    pr("LECTURA -> %s" % lectura(h_esp, h_sum))
    pr("VEREDICTO_GLOBAL -> %s" % ("VALIDO" if valido else "INVALIDO"))
    pr("EXIT_AGREGADO=%d" % (0 if valido else 1))
    return 0 if valido else 1


if __name__ == "__main__":
    sys.exit(main())
