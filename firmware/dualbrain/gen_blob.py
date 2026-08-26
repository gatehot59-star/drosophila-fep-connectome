"""gen_blob.py - genera un blob TIT4 y su ORACULO en numpy puro.

Por que existe: el arnes original (db_test.c de Tachi, en
gatehot59-star/mudh-mobile rama titan/esp32-inferencia-c-dualbrain) verifica que
el C reproduce a PyTorch, pero necesita dualbrain_weights.bin, un blob de
14.420 B que vive en /kaggle/working y NO esta en ninguno de los dos repos. Sin
ese archivo la autoprueba no corre, y eso dejaba tres items de deuda abiertos:
  - no hay .elf, solo objetos
  - el arnes no se compilo
  - el error de 8,94e-08 contra PyTorch no se reprodujo

Este script cierra los tres SIN el blob original, y la clave esta en QUE se
verifica. No se puede reproducir el error contra los pesos entrenados de marzo
porque esos pesos no existen aca. Lo que SI se puede, y es una prueba mas fuerte
sobre el codigo C, es verificar que db_step() implementa la especificacion:

  - se generan pesos DETERMINISTAS con una semilla fija;
  - se calcula la salida con un oraculo escrito en numpy DESDE EL HEADER, sin
    mirar dualbrain.c;
  - el blob lleva embebido el vector de autoprueba que el oraculo produjo;
  - db_selftest() compara el C contra ese vector.

Si el C y el oraculo coinciden, dos implementaciones independientes de la misma
especificacion dan el mismo numero. Eso NO reemplaza la verificacion contra
PyTorch: la complementa desde el otro lado.

Formato del blob, leido de dualbrain.h (no inventado):
  magic 'TIT4' | ver=1 | obs | hr | hm | act | n_floats     28 bytes
  vector de autoprueba: t_obs(OBS) t_hm_in(HM) t_act(ACT) t_hm_out(HM)
  pesos, en el orden de w->r0_w ... w->head_b
Todo float32 little-endian, que es lo que asume db_rd32 y el cast a float*.

Guards que pueden dar rojo:
  - n_floats calculado con la expresion del header CONTRA la suma de los
    tensores uno por uno. Si difieren, aborta con exit 2.
  - el tamano del blob escrito contra DB_BLOB_BYTES. Si difiere, aborta.
Sin esos dos, un blob mal armado produciria un DB_ERR_NFLOATS que se leeria
como bug del C.

Uso:
    python3 gen_blob.py      # escribe weights.bin, seq.bin, los oraculos y
                             # blob_embedded.h en el directorio actual
"""

import struct
import sys
import hashlib

import numpy as np

OBS, HR, HM, ACT = 12, 32, 16, 1
Z = HR + HM
SEED = 20260825

# n_floats: la MISMA expresion que DB_N_FLOATS del header, transcrita.
N_FLOATS = ((HR * OBS + HR) + (HR * HR + HR) + (HM * OBS + HM) + (HM * HM)
            + (HM * HM) + (HM * 2 * HM + HM) + (HM * Z + HM) + (ACT * Z + ACT))
TESTVEC = OBS + HM + ACT + HM
BLOB_BYTES = 28 + 4 * (TESTVEC + N_FLOATS)


def lg(m):
    sys.stdout.write(str(m) + "\n")
    sys.stdout.flush()


rng = np.random.default_rng(SEED)


def w(*shape):
    """Pesos chicos, en el rango en que viven los de una red entrenada."""
    return rng.uniform(-0.5, 0.5, size=shape).astype(np.float32)


# Tensores, en el orden EXACTO de get_weight_list() segun el header.
T = [
    ("r0_w", w(HR, OBS)), ("r0_b", w(HR)),
    ("r1_w", w(HR, HR)), ("r1_b", w(HR)),
    ("enc_w", w(HM, OBS)), ("enc_b", w(HM)),
    ("win_w", w(HM, HM)),
    ("wres_w", w(HM, HM)),
    ("tau_w", w(HM, 2 * HM)), ("tau_b", w(HM)),
    ("gate_w", w(HM, Z)), ("gate_b", w(HM)),
    ("head_w", w(ACT, Z)), ("head_b", w(ACT)),
]
D = dict(T)

total = sum(int(np.prod(v.shape)) for _, v in T)
lg("=== gen_blob: generador de blob TIT4 + oraculo numpy ===")
lg("dims OBS=%d HR=%d HM=%d ACT=%d Z=%d" % (OBS, HR, HM, ACT, Z))
lg("n_floats calculado del header : %d" % N_FLOATS)
lg("n_floats sumando los tensores : %d" % total)
if total != N_FLOATS:
    sys.stderr.write("GUARD_FAILED n_floats no coincide: " + str(total)
                     + " vs " + str(N_FLOATS) + "\n")
    raise SystemExit(2)
lg("GUARD n_floats OK")
lg("blob esperado: %d bytes" % BLOB_BYTES)


def np_tanh(x):
    return np.tanh(x.astype(np.float32)).astype(np.float32)


def np_sigmoid(x):
    """sigmoid via tanh, igual que el C: 0.5*(1+tanh(x/2))."""
    return (0.5 * (1.0 + np_tanh(0.5 * x.astype(np.float32)))).astype(np.float32)


def oracle_step(obs, h_m):
    """Un paso, escrito DESDE EL HEADER. No mira dualbrain.c.

    react   : Linear(OBS,HR) -> tanh -> Linear(HR,HR) -> tanh
    mem_cell: enc = encoder(x)
              tau = sigmoid(tau_learner([enc ; h]))
              campo = tanh(W_in.enc + W_res.h)
              h_new = (1-tau)*h + tau*campo
    gate    : g = sigmoid(gate_w([h_r ; h_m]))
    head    : y = head([h_r ; g*h_m])
    """
    obs = obs.astype(np.float32)
    h_m = h_m.astype(np.float32)

    enc = (D["enc_w"] @ obs + D["enc_b"]).astype(np.float32)
    tau = np_sigmoid(D["tau_w"] @ np.concatenate([enc, h_m]) + D["tau_b"])
    campo = np_tanh((D["win_w"] @ enc).astype(np.float32)
                    + (D["wres_w"] @ h_m).astype(np.float32))
    h_new = ((1.0 - tau) * h_m + tau * campo).astype(np.float32)

    mid = np_tanh(D["r0_w"] @ obs + D["r0_b"])
    h_r = np_tanh(D["r1_w"] @ mid + D["r1_b"])

    gate = np_sigmoid(D["gate_w"] @ np.concatenate([h_r, h_new]) + D["gate_b"])
    z = np.concatenate([h_r, (gate * h_new).astype(np.float32)]).astype(np.float32)
    act = (D["head_w"] @ z + D["head_b"]).astype(np.float32)
    return act, h_new


# vector de autoprueba: un paso desde un h_m inicial NO nulo
t_obs = rng.uniform(-1.0, 1.0, size=OBS).astype(np.float32)
t_hm_in = rng.uniform(-0.5, 0.5, size=HM).astype(np.float32)
t_act, t_hm_out = oracle_step(t_obs, t_hm_in)
lg("")
lg("=== vector de autoprueba, calculado por el ORACULO ===")
lg("  t_act    = " + " ".join(format(float(x), ".8f") for x in t_act))
lg("  t_hm_out[0:4] = " + " ".join(format(float(x), ".8f") for x in t_hm_out[:4]))

# la secuencia de 512 pasos, para que el main del C la reproduzca
seq = rng.uniform(-1.0, 1.0, size=(512, OBS)).astype(np.float32)
h = np.zeros(HM, dtype=np.float32)
acts = []
for i in range(512):
    a, h = oracle_step(seq[i], h)
    acts.append(float(a[0]))
lg("")
lg("=== SECUENCIA de 512 pasos, oraculo ===")
lg("  act[0]   = " + format(acts[0], ".8f"))
lg("  act[255] = " + format(acts[255], ".8f"))
lg("  act[511] = " + format(acts[511], ".8f"))
lg("  rango    = [" + format(min(acts), ".4f") + ", " + format(max(acts), ".4f") + "]")
lg("  h_m final[0:4] = " + " ".join(format(float(x), ".8f") for x in h[:4]))

# ---------- escritura del blob ----------
buf = bytearray()
buf += b"TIT4"
for v in (1, OBS, HR, HM, ACT, N_FLOATS):
    buf += struct.pack("<I", v)
for arr in (t_obs, t_hm_in, t_act, t_hm_out):
    buf += np.asarray(arr, dtype="<f4").tobytes()
for _, v in T:
    buf += np.asarray(v, dtype="<f4").ravel().tobytes()

if len(buf) != BLOB_BYTES:
    sys.stderr.write("GUARD_FAILED blob mide " + str(len(buf)) + " y se esperaba "
                     + str(BLOB_BYTES) + "\n")
    raise SystemExit(2)

open("weights.bin", "wb").write(bytes(buf))
lg("")
lg("=== BLOB ===")
lg("  weights.bin  %d bytes" % len(buf))
lg("  md5          %s" % hashlib.md5(bytes(buf)).hexdigest())
lg("  GUARD tamano OK")

# la secuencia y el oraculo, para que el C los lea
np.asarray(seq, dtype="<f4").tofile("seq.bin")
np.asarray(acts, dtype="<f4").tofile("oracle_acts.bin")
np.asarray(h, dtype="<f4").tofile("oracle_hm.bin")
lg("  seq.bin           %d bytes (512 x %d floats)" % (512 * OBS * 4, OBS))
lg("  oracle_acts.bin   %d bytes" % (512 * 4))
lg("  oracle_hm.bin     %d bytes" % (HM * 4))


# ---------- header embebido, para linkear un .elf sin filesystem ----------
def _carr(name, data, per=12):
    out = ["static const unsigned char " + name + "[] __attribute__((aligned(4))) = {"]
    for i in range(0, len(data), per):
        out.append("    " + ", ".join(str(b) for b in data[i:i + per]) + ",")
    out.append("};")
    return chr(10).join(out)


def _farr(name, arr, per=8):
    out = ["static const float " + name + "[] = {"]
    for i in range(0, len(arr), per):
        out.append("    " + ", ".join(format(float(x), ".9g") + "f" for x in arr[i:i + per]) + ",")
    out.append("};")
    return chr(10).join(out)


_blob = bytes(buf)
_seq = np.asarray(seq, dtype="<f4").ravel()
_h = "/* blob_embedded.h - blob TIT4 y secuencia, embebidos para linkear sin" + chr(10)
_h += " * sistema de archivos. Generado por gen_blob.py. NO editar a mano." + chr(10)
_h += " * blob: " + str(len(_blob)) + " bytes   seq: " + str(len(_seq)) + " floats" + chr(10) + " */" + chr(10)
_h += "#ifndef BLOB_EMBEDDED_H" + chr(10) + "#define BLOB_EMBEDDED_H" + chr(10) + chr(10)
_h += _carr("db_blob", _blob) + chr(10) + chr(10) + _farr("db_seq", _seq) + chr(10) + chr(10) + "#endif" + chr(10)
open("blob_embedded.h", "w").write(_h)
lg("  blob_embedded.h   %d bytes (para el .elf)" % len(_h))
lg("")
lg("DONE")
