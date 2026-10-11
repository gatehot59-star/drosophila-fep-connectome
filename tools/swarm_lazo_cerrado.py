#!/usr/bin/env python3
"""Auditoria de lazo cerrado del sustrato swarm/ ("Cerebro de Enjambre para Micro-Drones").

Mide sobre el SUJETO EXACTO: los archivos de swarm/ tal como estan en git, sin tocarlos.

  G0  procedencia: blob SHA de git de cada archivo de swarm/ contra los pinneados en main 02da943.
  G1  reproducibilidad: gen_swarm.py regenera swarm_drone.h y swarm_drone.substrate.json byte a byte.
  G2  el test original, puede dar rojo?: compila test_swarm.c contra headers mutados y mira el exit.
  G3  la auditoria de gen_swarm.py, puede dar rojo?: regenera con topologias mutadas y lee sus gates.
  G4  signo del escape en lazo cerrado: cuadricoptero X de angulo chico, amenaza en las 4 direcciones.
  G5  informativo: que hace el dron sin amenaza y con rumbo 0 o 90 grados, sin lazo de actitud.

Convenciones fisicas (declaradas; son las de un multirrotor X estandar):
  x adelante, y derecha. Roll phi>0 = lado derecho abajo. Pitch theta>0 = nariz arriba.
  tau_phi   = l * ((T_FL + T_BL) - (T_FR + T_BR))
  tau_theta = l * ((T_FL + T_FR) - (T_BL + T_BR))
  a_x = -g * theta ;  a_y = +g * phi   (angulo chico)
  T_i = T0 * (1 + k * u_i), con u_i = salida_motor_Q15 / 32768 y T0 = m g / 4.
  El lado con mas empuje sube y el vehiculo acelera hacia el lado contrario.

Validez del instrumento (se chequea en cada corrida):
  - un reflejo escrito a mano con la fisica correcta tiene que dar ALEJA en 4/4 direcciones;
  - una red nula (motores en cero) tiene que dar NEUTRO en 4/4.
  Si alguno falla, el instrumento es invalido y no se emite veredicto sobre el sujeto.

Codigos de salida: 0 = el sujeto pasa todos los gates; 1 = el sujeto falla al menos uno;
                   2 = instrumento invalido o falta una herramienta (gcc, numpy).

Uso:  python3 tools/swarm_lazo_cerrado.py --swarm-dir swarm --out results/swarm_lazo_cerrado
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PIN_COMMIT = "02da943ac5ee25468db696c7430d5bc72000627e"
PIN = {
    "gen_swarm.py": "3c335ad54f5c1adb937a4b7e498dbf48e85ff03c",
    "test_swarm.c": "a84b9f7682f00d9505194d328ac1a988bfb84eea",
    "swarm_drone.h": "f18b87611ecaa795be4b2c3f7a3697210c8700c0",
    "swarm_drone.substrate.json": "f6230fcd7f5d684cc5d1450d4e8eed6299227af4",
}
GF_RANGE = range(16, 20)      # gf_f gf_b gf_l gf_r
MOTOR_RANGE = range(30, 34)   # mot_fl mot_fr mot_bl mot_br
DIRS = ["frente", "atras", "izquierda", "derecha"]


def log(line):
    """Imprime una linea de evidencia sin buffer, para que el log quede completo aunque se corte."""
    print(line, flush=True)


def blob_sha(path):
    """SHA-1 de blob de git: lo mismo que devuelve `git hash-object <path>`."""
    with open(path, "rb") as fh:
        data = fh.read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def run(cmd, cwd, timeout=120):
    """Corre un comando y devuelve (exit, stdout, stderr). Nunca lanza por exit distinto de cero."""
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def regenerate(gen_source, workdir):
    """Escribe gen_swarm.py (posiblemente mutado) en workdir, lo corre y devuelve (exit, salida)."""
    os.makedirs(workdir, exist_ok=True)
    with open(os.path.join(workdir, "gen_swarm.py"), "w", encoding="utf-8") as fh:
        fh.write(gen_source)
    code, out, err = run([sys.executable, "gen_swarm.py"], cwd=workdir)
    return code, out + err


def mutate_header(header_text, mode):
    """Devuelve el header con la tabla de sinapsis mutada. mode: 'pesos_cero' o 'gf_motor_invertido'."""
    pattern = re.compile(r"^(\s*)\{(-?\d+), (-?\d+), (-?\d+)\}(,?)$")
    out_lines = []
    changed = 0
    for line in header_text.split("\n"):
        m = pattern.match(line)
        if m:
            indent, s, d, w, comma = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
            if mode == "pesos_cero":
                w, changed = 0, changed + 1
            elif mode == "gf_motor_invertido" and s in GF_RANGE and d in MOTOR_RANGE:
                w, changed = -w, changed + 1
            line = "%s{%d, %d, %d}%s" % (indent, s, d, w, comma)
        out_lines.append(line)
    return "\n".join(out_lines), changed


HARNESS_C = r"""
#include <math.h>
#include <stdio.h>
#include <string.h>
#include "swarm_drone.h"

/* lecturas de motores: u[0]=FL u[1]=FR u[2]=BL u[3]=BR en [-1,1] */
enum { RD_ORIGINAL = 0, RD_REFLEJADO = 1, RD_CERO = 2, RD_FISICO = 3, RD_N = 4 };
static const char *RD_NAME[RD_N] = {"ORIGINAL", "REFLEJADO", "CERO", "REFLEJO_FISICO"};
static const char *DIR_NAME[4] = {"frente", "atras", "izquierda", "derecha"};
static const double EX[4] = {1.0, -1.0, 0.0, 0.0};
static const double EY[4] = {0.0, 0.0, -1.0, 1.0};
/* patron del reflejo fisico correcto: sube el lado que mira a la amenaza */
static const double PAT[4][4] = {
    {+1, +1, -1, -1},  /* frente: nariz arriba -> retrocede */
    {-1, -1, +1, +1},  /* atras: cola arriba -> avanza */
    {+1, -1, +1, -1},  /* izquierda: lado izq arriba -> va a la derecha */
    {-1, +1, -1, +1},  /* derecha: lado der arriba -> va a la izquierda */
};

typedef struct { double m, g, l, I, k, D0, net_hz; int sub; } params_t;

static double clamp1(double v) { return v > 1.0 ? 1.0 : (v < -1.0 ? -1.0 : v); }

static void readout(int rd, const swarm_drone_t *b, const int16_t *sens, double u[4]) {
    if (rd == RD_ORIGINAL) {
        int16_t fl, fr, bl, br;
        swarm_get_motors(b, &fl, &fr, &bl, &br);   /* la funcion del header, sin tocar */
        u[0] = fl / 32768.0; u[1] = fr / 32768.0; u[2] = bl / 32768.0; u[3] = br / 32768.0;
    } else if (rd == RD_REFLEJADO) {
        /* parche propuesto: reflexion puntual FL<->BR, FR<->BL de la lectura */
        u[0] = b->h[33] / 32768.0; u[1] = b->h[32] / 32768.0;
        u[2] = b->h[31] / 32768.0; u[3] = b->h[30] / 32768.0;
    } else if (rd == RD_CERO) {
        u[0] = u[1] = u[2] = u[3] = 0.0;
    } else {
        for (int i = 0; i < 4; i++) u[i] = 0.0;
        for (int d = 0; d < 4; d++) {
            double a = (sens[d] + sens[4 + d]) / 32768.0;
            for (int i = 0; i < 4; i++) u[i] += 0.5 * a * PAT[d][i];
        }
        for (int i = 0; i < 4; i++) u[i] = clamp1(u[i]);
    }
}

/* d_threat: 0..3 o -1 sin amenaza; channel: 0 lamina (flujo optico), 1 antena (proximidad) */
static void simulate(int rd, int d_threat, int channel, const params_t *P, double H,
                     double hsin, double hcos, double res[6]) {
    swarm_drone_t b;
    swarm_init(&b);
    double x = 0, y = 0, vx = 0, vy = 0, phi = 0, th = 0, p = 0, q = 0;
    const double T0 = P->m * P->g / 4.0;
    const double dt_net = 1.0 / P->net_hz, dt = dt_net / P->sub;
    const int nsteps = (int)llround(H / dt_net);
    double u[4] = {0, 0, 0, 0}, t_tilt30 = -1.0, tilt_max = 0.0;
    for (int n = 0; n < nsteps; n++) {
        int16_t sens[12];
        memset(sens, 0, sizeof sens);
        if (d_threat >= 0) {
            double along = x * EX[d_threat] + y * EY[d_threat];
            double dist = P->D0 - along;
            if (dist < 0.05) dist = 0.05;
            double base = (channel == 0) ? 15000.0 : 9000.0;   /* los valores de test_swarm.c */
            double v = base * P->D0 / dist;
            if (v > 32767.0) v = 32767.0;
            sens[(channel == 0 ? 0 : 4) + d_threat] = (int16_t)v;
        }
        sens[8] = (int16_t)lround(hsin * 32767.0);
        sens[9] = (int16_t)lround(hcos * 32767.0);
        swarm_step(&b, sens);
        readout(rd, &b, sens, u);
        for (int s = 0; s < P->sub; s++) {
            double T[4];
            for (int i = 0; i < 4; i++) T[i] = T0 * (1.0 + P->k * clamp1(u[i]));
            double tau_phi = P->l * ((T[0] + T[2]) - (T[1] + T[3]));
            double tau_th = P->l * ((T[0] + T[1]) - (T[2] + T[3]));
            p += tau_phi / P->I * dt;  q += tau_th / P->I * dt;
            phi += p * dt;             th += q * dt;
            vx += -P->g * th * dt;     vy += P->g * phi * dt;
            x += vx * dt;              y += vy * dt;
            double tilt = fabs(phi) > fabs(th) ? fabs(phi) : fabs(th);
            if (tilt > tilt_max) tilt_max = tilt;
            if (t_tilt30 < 0 && tilt > 0.5235987755982988) t_tilt30 = (n * P->sub + s + 1) * dt;
        }
    }
    res[0] = x; res[1] = y; res[2] = tilt_max; res[3] = t_tilt30;
    res[4] = u[0] - u[3]; res[5] = u[1] - u[2];
}

static const char *verdict(double toward) {
    if (toward > 1e-4) return "ACERCA";
    if (toward < -1e-4) return "ALEJA";
    return "NEUTRO";
}

int main(void) {
    params_t P = {0.030, 9.81, 0.0325, 1.4e-5, 0.2, 1.0, 200.0, 10};
    const double H = 0.15;
    double base[6], thr[6];
    /* G4a: signo estatico, como test_swarm.c: 50 pasos con un solo estimulo constante */
    for (int ch = 0; ch < 2; ch++) {
        for (int d = 0; d < 4; d++) {
            swarm_drone_t b; swarm_init(&b);
            int16_t sens[12]; memset(sens, 0, sizeof sens);
            sens[(ch == 0 ? 0 : 4) + d] = (ch == 0) ? 15000 : 9000;
            for (int t = 0; t < 50; t++) swarm_step(&b, sens);
            int16_t fl, fr, bl, br; swarm_get_motors(&b, &fl, &fr, &bl, &br);
            double roll = (fl + bl) - (fr + br), pitch = (fl + fr) - (bl + br);
            double ax = -pitch, ay = roll;  /* direccion de aceleracion inducida, a menos de escala */
            double toward = ax * EX[d] + ay * EY[d];
            printf("ESTATICO canal=%s amenaza=%s motores_FL_FR_BL_BR=%d %d %d %d torque_roll=%+.0f torque_pitch=%+.0f -> %s\n",
                   ch == 0 ? "lamina" : "antena", DIR_NAME[d], fl, fr, bl, br, roll, pitch,
                   toward > 0 ? "ACERCA" : (toward < 0 ? "ALEJA" : "NEUTRO"));
        }
    }
    /* G4b: lazo cerrado, apareado contra la misma lectura sin amenaza */
    for (int ch = 0; ch < 2; ch++) {
        for (int rd = 0; rd < RD_N; rd++) {
            for (int d = 0; d < 4; d++) {
                simulate(rd, -1, ch, &P, H, 0.0, 0.0, base);
                simulate(rd, d, ch, &P, H, 0.0, 0.0, thr);
                double toward = (thr[0] - base[0]) * EX[d] + (thr[1] - base[1]) * EY[d];
                printf("LAZO canal=%s lectura=%s amenaza=%s H=%.2fs delta_hacia_amenaza_m=%+.6f inclinacion_max_grados=%.2f -> %s\n",
                       ch == 0 ? "lamina" : "antena", RD_NAME[rd], DIR_NAME[d], H, toward,
                       thr[2] * 57.29577951308232, verdict(toward));
            }
        }
    }
    /* G4c: sensibilidad del signo a k, horizonte y frecuencia de la red (solo lamina) */
    const double KS[3] = {0.05, 0.2, 0.5}, HS[3] = {0.10, 0.15, 0.20}, FS[3] = {100.0, 200.0, 500.0};
    for (int rd = 0; rd < 2; rd++) {
        int pos = 0, neg = 0, cero = 0;
        double min_abs = 1e300, max_abs = 0.0;
        for (int a = 0; a < 3; a++) for (int c = 0; c < 3; c++) for (int f = 0; f < 3; f++) for (int d = 0; d < 4; d++) {
            params_t Q = P; Q.k = KS[a]; Q.net_hz = FS[f];
            simulate(rd, -1, 0, &Q, HS[c], 0.0, 0.0, base);
            simulate(rd, d, 0, &Q, HS[c], 0.0, 0.0, thr);
            double toward = (thr[0] - base[0]) * EX[d] + (thr[1] - base[1]) * EY[d];
            if (toward > 0) pos++; else if (toward < 0) neg++; else cero++;
            if (fabs(toward) < min_abs) min_abs = fabs(toward);
            if (fabs(toward) > max_abs) max_abs = fabs(toward);
        }
        printf("SENSIBILIDAD lectura=%s combinaciones=108 (k x H x frecuencia x direccion) signo_hacia_amenaza: positivo=%d negativo=%d cero=%d |delta|_min_m=%.3e |delta|_max_m=%.3e\n",
               RD_NAME[rd], pos, neg, cero, min_abs, max_abs);
    }
    /* G5: sin amenaza, rumbo 0 y 90 grados, 1 s, sin lazo de actitud */
    for (int rd = 0; rd < 2; rd++) {
        for (int hdg = 0; hdg < 2; hdg++) {
            double hs = hdg ? 1.0 : 0.0, hc = hdg ? 0.0 : 1.0;
            simulate(rd, -1, 0, &P, 0.15, hs, hc, thr);    /* deriva dentro del rango de angulo chico */
            simulate(rd, -1, 0, &P, 1.0, hs, hc, base);    /* solo para el tiempo a 30 grados */
            printf("REPOSO lectura=%s sin_amenaza rumbo=%d deriva_a_0.15s_x_m=%+.6f y_m=%+.6f inclinacion_a_0.15s_grados=%.2f t_hasta_30grados_s=%.3f\n",
                   RD_NAME[rd], hdg ? 90 : 0, thr[0], thr[1], thr[2] * 57.29577951308232, base[3]);
        }
    }
    printf("FIN_HARNESS\n");
    return 0;
}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--swarm-dir", default="swarm", help="carpeta swarm/ del repo")
    ap.add_argument("--out", default="results/swarm_lazo_cerrado", help="carpeta de salida")
    ap.add_argument("--no-pin", action="store_true", help="no exigir los blob SHA de main 02da943")
    args = ap.parse_args()

    if shutil.which("gcc") is None:
        log("HERRAMIENTA gcc FALTA -> INSTRUMENTO_INVALIDO")
        return 2
    try:
        import numpy  # noqa: F401  (gen_swarm.py lo necesita)
    except ImportError:
        log("HERRAMIENTA numpy FALTA -> INSTRUMENTO_INVALIDO")
        return 2

    sdir = os.path.abspath(args.swarm_dir)
    os.makedirs(args.out, exist_ok=True)
    report = {"pin_commit": PIN_COMMIT, "gates": {}}
    fails = []

    # G0 procedencia
    g0 = True
    for name, expected in PIN.items():
        path = os.path.join(sdir, name)
        if not os.path.exists(path):
            log("G0 %s FALTA" % name)
            g0 = False
            continue
        got = blob_sha(path)
        ok = got == expected
        g0 = g0 and ok
        log("G0 %s blob=%s pin=%s -> %s" % (name, got, expected, "IGUAL" if ok else "DISTINTO"))
    report["gates"]["G0_procedencia"] = "PASS" if g0 else "FAIL"
    if not g0 and not args.no_pin:
        fails.append("G0")
    log("CHEQUEO G0_PROCEDENCIA %s" % report["gates"]["G0_procedencia"])

    with open(os.path.join(sdir, "gen_swarm.py"), encoding="utf-8") as fh:
        gen_src = fh.read()
    with open(os.path.join(sdir, "swarm_drone.h"), encoding="utf-8") as fh:
        header_txt = fh.read()

    tmp = tempfile.mkdtemp(prefix="swarm_audit_")

    # G1 reproducibilidad
    code, out = regenerate(gen_src, os.path.join(tmp, "g1"))
    g1 = code == 0
    for name in ("swarm_drone.h", "swarm_drone.substrate.json"):
        regen = os.path.join(tmp, "g1", name)
        same = os.path.exists(regen) and blob_sha(regen) == blob_sha(os.path.join(sdir, name))
        g1 = g1 and same
        log("G1 %s regenerado_igual_al_commiteado=%s" % (name, same))
    log("G1 gen_swarm_exit=%d salida=%s" % (code, out.strip().replace("\n", " | ")))
    report["gates"]["G1_reproducibilidad"] = "PASS" if g1 else "FAIL"
    if not g1:
        fails.append("G1")
    log("CHEQUEO G1_REPRODUCIBILIDAD %s" % report["gates"]["G1_reproducibilidad"])

    # G2 el test original puede dar rojo?
    g2_rows = []
    for mode in ("original", "pesos_cero", "gf_motor_invertido"):
        wd = os.path.join(tmp, "g2_" + mode)
        os.makedirs(wd)
        shutil.copy(os.path.join(sdir, "test_swarm.c"), wd)
        if mode == "original":
            htxt, changed = header_txt, 0
        else:
            htxt, changed = mutate_header(header_txt, mode)
        with open(os.path.join(wd, "swarm_drone.h"), "w", encoding="utf-8") as fh:
            fh.write(htxt)
        c1, _, e1 = run(["gcc", "-Wall", "-Wextra", "-Werror", "-std=c99", "-O2", "-o", "t", "test_swarm.c"], cwd=wd)
        c2, o2, _ = run(["./t"], cwd=wd) if c1 == 0 else (-1, "", "")
        first = o2.split("\n")[0] if o2 else e1.strip()[:200]
        g2_rows.append({"mutacion": mode, "sinapsis_cambiadas": changed, "gcc_exit": c1, "test_exit": c2, "salida": first})
        log("G2 mutacion=%s sinapsis_cambiadas=%d gcc_exit=%d test_exit=%d salida=%s" % (mode, changed, c1, c2, first))
    can_red = any(r["test_exit"] != 0 for r in g2_rows if r["mutacion"] != "original")
    report["gates"]["G2_test_puede_dar_rojo"] = "PASS" if can_red else "FAIL"
    report["G2"] = g2_rows
    if not can_red:
        fails.append("G2")
    log("CHEQUEO G2_TEST_PUEDE_DAR_ROJO %s" % report["gates"]["G2_test_puede_dar_rojo"])

    # G3 la auditoria de gen_swarm.py puede dar rojo?
    anchor = "# ---------- radio espectral"
    mutations = {
        "sin_mutar": "",
        "mezcla_modalidades": ('conns.append(W("lam_flow_f","pb_alt",0.9)); conns.append(W("ant_prox_l","wta_r",0.9)); '
                               'conns.append(W("hal_alt","gf_f",0.9)); conns.append(W("oc_head_cos","lh_l",0.9))\n'),
        "signos_invertidos": "conns[:] = [[s, d, -w] for s, d, w in conns]\n",
        "sensores_directo_a_motores": ('for _s in idx2name[:12]:\n'
                                       '    for _m in ["mot_fl","mot_fr","mot_bl","mot_br"]:\n'
                                       '        conns.append(W(_s, _m, 0.9))\n'),
    }
    g3_rows = []
    if anchor not in gen_src:
        log("G3 ancla '%s' no encontrada -> INSTRUMENTO_INVALIDO" % anchor)
        return 2
    for name, patch in mutations.items():
        src = gen_src.replace(anchor, patch + anchor, 1)
        wd = os.path.join(tmp, "g3_" + name)
        code, out = regenerate(src, wd)
        row = {"mutacion": name, "gen_exit": code}
        if code == 0:
            with open(os.path.join(wd, "swarm_drone.substrate.json"), encoding="utf-8") as fh:
                meta = json.load(fh)["metadata"]
            ms, gaba = meta["audit"]["maslov_sneppen"], meta["audit"]["gabaergica"]
            row.update({"E": meta["E"], "ms_gate": ms["gate"], "rdi_diseno": ms["rdi_diseno"],
                        "gaba_gate": gaba["gate"], "firewalls": gaba["firewalls"],
                        "motor_starvation": gaba["motor_starvation"]})
        g3_rows.append(row)
        log("G3 " + json.dumps(row, ensure_ascii=False, sort_keys=True))
    mutated = [r for r in g3_rows if r["mutacion"] != "sin_mutar" and r["gen_exit"] == 0]
    constant = bool(mutated) and all(r["ms_gate"] == "PASS" and r["rdi_diseno"] == 0.0 and r["gaba_gate"] == "PASS"
                                     for r in mutated)
    report["gates"]["G3_auditoria_puede_dar_rojo"] = "FAIL" if constant else "PASS"
    report["G3"] = g3_rows
    if constant:
        fails.append("G3")
    log("CHEQUEO G3_AUDITORIA_PUEDE_DAR_ROJO %s" % report["gates"]["G3_auditoria_puede_dar_rojo"])

    # G4 y G5: arnes en C contra el header exacto
    wd = os.path.join(tmp, "g4")
    os.makedirs(wd)
    shutil.copy(os.path.join(sdir, "swarm_drone.h"), wd)
    with open(os.path.join(wd, "harness.c"), "w", encoding="utf-8") as fh:
        fh.write(HARNESS_C)
    c1, _, e1 = run(["gcc", "-Wall", "-Wextra", "-Werror", "-std=c99", "-O2", "-o", "harness", "harness.c", "-lm"], cwd=wd)
    log("G4 harness_gcc_exit=%d %s" % (c1, e1.strip()[:300]))
    if c1 != 0:
        return 2
    c2, hout, herr = run(["./harness"], cwd=wd, timeout=600)
    for line in hout.strip().split("\n"):
        log(line)
    if c2 != 0 or "FIN_HARNESS" not in hout:
        log("G4 harness_exit=%d %s -> INSTRUMENTO_INVALIDO" % (c2, herr.strip()[:300]))
        return 2

    def lazo(lectura, canal="lamina"):
        rows = [l for l in hout.split("\n") if l.startswith("LAZO canal=%s lectura=%s " % (canal, lectura))]
        return [l.rsplit("-> ", 1)[1].strip() for l in rows]

    fisico, cero = lazo("REFLEJO_FISICO"), lazo("CERO")
    valid = fisico == ["ALEJA"] * 4 and cero == ["NEUTRO"] * 4
    log("CHEQUEO INSTRUMENTO control_positivo=%s control_negativo=%s -> %s"
        % ("/".join(fisico), "/".join(cero), "VALIDO" if valid else "INVALIDO"))
    if not valid:
        return 2
    orig, refl = lazo("ORIGINAL"), lazo("REFLEJADO")
    g4 = orig == ["ALEJA"] * 4
    report["gates"]["G4_escape_lamina_aleja_4de4"] = "PASS" if g4 else "FAIL"
    report["G4"] = {"original": dict(zip(DIRS, orig)), "reflejado": dict(zip(DIRS, refl)),
                    "antena_original": dict(zip(DIRS, lazo("ORIGINAL", "antena"))),
                    "antena_reflejado": dict(zip(DIRS, lazo("REFLEJADO", "antena")))}
    if not g4:
        fails.append("G4")
    log("CHEQUEO G4_ESCAPE_LAMINA original=%s reflejado=%s -> %s"
        % ("/".join(orig), "/".join(refl), report["gates"]["G4_escape_lamina_aleja_4de4"]))

    report["harness_stdout"] = hout
    with open(os.path.join(args.out, "swarm_lazo_cerrado.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False, sort_keys=True)
    shutil.rmtree(tmp, ignore_errors=True)
    verdict = "PASS" if not fails else "FAIL"
    log("VEREDICTO_SUJETO=%s gates_en_rojo=%s" % (verdict, ",".join(fails) if fails else "ninguno"))
    log("FIN_SWARM_LAZO_CERRADO")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
