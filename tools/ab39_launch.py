"""Construye y lanza los 5 kernels de cierre en Kaggle GPU.

Que lanza:
  4 kernels MODE=ab      -> los 39 nulls del A/B v1 vs v2, repartidos intercalados
  1 kernel  MODE=extras  -> distribucion de la semilla de fase, barrido de jitter,
                            escala hasta n real y RSS por proceso hijo

Guards, porque un horneado silencioso arruina la corrida:
  1. los tres fuentes se embeben en base64 y el kernel VERIFICA su md5 al arrancar.
     Un kernel que corre otra version del motor no mide lo que dice medir.
  2. si el horneado del SHARD_ID no entro, ABORTA: dos shards con el mismo id
     corren los mismos nulls y dejan un hueco en la particion.
  3. despues del push se lee el ref REAL de /kernels/list, porque Kaggle slugifica
     el TITULO y no el slug enviado (docs/agents/KAGGLE-REGLA-DEL-SLUG.md).
  4. la particion se verifica en el generador: los 4 shards tienen que cubrir
     0..38 exactamente una vez.

Autenticacion: Bearer, la unica que funciona con los tokens KGAT_
(docs/agents/MANIFIESTO-KAGGLE.md).
"""
import base64, hashlib, json, os, urllib.request, urllib.error

BASE = "/workspace"
CRED = json.load(open(os.path.join(BASE, "kaggle.json")))
API = "https://www.kaggle.com/api/v1"

def api(c, path, method="GET", body=None):
    req = urllib.request.Request(API + path, method=method)
    req.add_header("Authorization", "Bearer " + c["token"])
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data, timeout=180) as r:
            t = r.read().decode()
            return r.status, t
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]

def b64(p):
    raw = open(p, "rb").read()
    return base64.b64encode(raw).decode(), hashlib.md5(raw).hexdigest(), len(raw)

B1, M1, L1 = b64(os.path.join(BASE, "motor.py"))
B2, M2, L2 = b64(os.path.join(BASE, "motor_v2.py"))
B3, M3, L3 = b64(os.path.join(BASE, "ab39_core.py"))
print("motor.py     md5=%s  %d B" % (M1, L1))
print("motor_v2.py  md5=%s  %d B" % (M2, L2))
print("ab39_core.py md5=%s  %d B" % (M3, L3))

N_NULLS = 39
SHARDS = 4

# Guard 4: la particion tiene que ser exacta ANTES de gastar un segundo de GPU
cub = []
for i in range(SHARDS):
    cub += list(range(i, N_NULLS, SHARDS))
assert sorted(cub) == list(range(N_NULLS)), "la particion no cubre 0..%d" % (N_NULLS - 1)
assert len(cub) == len(set(cub)), "la particion tiene duplicados"
print("GUARD 4 particion: %d indices, %d unicos, cubre 0..%d -> OK"
      % (len(cub), len(set(cub)), N_NULLS - 1))

PREAMBULO = '''# GENERATED kernel de cierre  ·  no editar a mano
#
# Escribe los tres fuentes desde base64, VERIFICA sus md5 y corre el arnes.
# Si un md5 no coincide, aborta: un kernel que corre otra version del motor no
# mide lo que su titulo dice que mide.
import base64, hashlib, os, sys, pathlib

BASE = "/kaggle/working"
os.makedirs(BASE, exist_ok=True)
BLOBS = {
    "motor.py": ("%(b1)s", "%(m1)s"),
    "motor_v2.py": ("%(b2)s", "%(m2)s"),
    "ab39_core.py": ("%(b3)s", "%(m3)s"),
}
for nombre, (blob, esperado) in BLOBS.items():
    raw = base64.b64decode(blob)
    got = hashlib.md5(raw).hexdigest()
    if got != esperado:
        raise SystemExit("ABORTA: md5 de " + nombre + " es " + got + " y se esperaba " + esperado)
    pathlib.Path(os.path.join(BASE, nombre)).write_bytes(raw)
    print("escrito " + nombre + "  " + str(len(raw)) + " B  md5 " + got + "  VERIFICADO", flush=True)

os.environ["AB_MODE"] = "%(modo)s"
os.environ["AB_SHARD"] = "%(shard)d"
os.environ["AB_SHARD_TOTAL"] = "%(total)d"
os.environ["AB_NULLS"] = "%(nulls)d"
os.environ["AB_STEPS"] = "150"
os.environ["AB_BASE"] = BASE
os.environ["AB_OUT"] = os.path.join(BASE, "ab39_out")
print("MODO=%(modo)s SHARD=%(shard)d/%(total)d NULLS=%(nulls)d", flush=True)

sys.argv = ["ab39_core.py"]
exec(compile(pathlib.Path(os.path.join(BASE, "ab39_core.py")).read_text(), "ab39_core.py", "exec"),
     {"__name__": "__main__", "__file__": os.path.join(BASE, "ab39_core.py")})
'''

PLAN = [
    {"acct": 1, "modo": "ab", "shard": 0, "titulo": "TITAN cierre ab39 shard 0 de 4"},
    {"acct": 1, "modo": "ab", "shard": 1, "titulo": "TITAN cierre ab39 shard 1 de 4"},
    {"acct": 0, "modo": "ab", "shard": 2, "titulo": "TITAN cierre ab39 shard 2 de 4"},
    {"acct": 0, "modo": "ab", "shard": 3, "titulo": "TITAN cierre ab39 shard 3 de 4"},
    {"acct": 1, "modo": "extras", "shard": 0, "titulo": "TITAN cierre extras semilla jitter escala rss"},
]

for p in PLAN:
    c = CRED[p["acct"]]
    texto = PREAMBULO % {"b1": B1, "m1": M1, "b2": B2, "m2": M2, "b3": B3, "m3": M3,
                         "modo": p["modo"], "shard": p["shard"], "total": SHARDS,
                         "nulls": N_NULLS}
    # Guard 2: el horneado del shard tiene que estar en el texto
    marca = 'os.environ["AB_SHARD"] = "%d"' % p["shard"]
    marca_modo = 'os.environ["AB_MODE"] = "%s"' % p["modo"]
    if marca not in texto or marca_modo not in texto:
        print("ABORTA %s shard %d: el horneado no entro" % (p["modo"], p["shard"]))
        continue
    slug = "titan-cierre-%s-%d" % (p["modo"], p["shard"])
    body = {
        "slug": c["username"] + "/" + slug,
        "newTitle": p["titulo"],
        "text": texto,
        "language": "python",
        "kernelType": "script",
        "isPrivate": True,
        "enableGpu": True,
        "enableTpu": False,
        "enableInternet": True,
        "datasetDataSources": [], "competitionDataSources": [],
        "kernelSources": [], "categoryIds": [],
    }
    st, txt = api(c, "/kernels/push", "POST", body)
    print("\n%s shard %d -> %s  HTTP %s  bytes=%d" % (p["modo"], p["shard"], c["username"], st, len(texto)))
    print("  " + " ".join(txt.split())[:260])

print("\n===== REFS REALES (Kaggle slugifica el TITULO, no el slug) =====")
for c in CRED:
    st, txt = api(c, "/kernels/list?user=%s&page=1&pageSize=100&sortBy=dateRun" % c["username"])
    try:
        arr = json.loads(txt)
    except Exception:
        print("  %s: list HTTP %s" % (c["username"], st)); continue
    for k in arr:
        if "cierre" in (k.get("ref") or ""):
            print("  %s   lastRunTime=%s" % (k["ref"], k.get("lastRunTime")))
