"""Lanza los 4 kernels de nm_core en las DOS cuentas: 2 sesiones GPU por cuenta.

El limite de Kaggle es 2 sesiones GPU SIMULTANEAS POR CUENTA, no de cuota. Con dos
cuentas hay 4 slots, y son exactamente los que se usan aca. La cuota medida antes
de lanzar era 27,89 h y 29,31 h libres, o sea que nunca fue el limite.

Guards: md5 de los tres fuentes verificado por el kernel al arrancar, horneado del
SHARD verificado antes del push, y particion verificada en el generador.
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
        data = json.dumps(body).encode(); req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data, timeout=180) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]

def b64(p):
    raw = open(p, "rb").read()
    return base64.b64encode(raw).decode(), hashlib.md5(raw).hexdigest(), len(raw)

B1, M1, L1 = b64(os.path.join(BASE, "motor.py"))
B2, M2, L2 = b64(os.path.join(BASE, "motor_v2.py"))
B3, M3, L3 = b64(os.path.join(BASE, "nm_core.py"))
print("motor.py     md5=%s  %d B" % (M1, L1))
print("motor_v2.py  md5=%s  %d B" % (M2, L2))
print("nm_core.py   md5=%s  %d B" % (M3, L3))

N_NULLS = 12
SHARDS = 4
cub = []
for i in range(SHARDS):
    cub += list(range(i, N_NULLS, SHARDS))
assert sorted(cub) == list(range(N_NULLS)) and len(cub) == len(set(cub))
print("GUARD particion: %d indices, %d unicos, cubre 0..%d -> OK" % (len(cub), len(set(cub)), N_NULLS - 1))

print("\nCUOTA GPU antes de lanzar:")
for c in CRED:
    st, t = api(c, "/kernels/quota")
    q = json.loads(t)["gpuQuota"]
    us = q["timeUsed"]["seconds"] / 3600.0
    tot = q["totalTimeAllowed"]["seconds"] / 3600.0
    print("  %-18s usado %.2f h de %.1f h  LIBRE %.2f h" % (c["username"], us, tot, tot - us))

PRE = '''# GENERATED kernel  \u00b7 no editar a mano
import base64, hashlib, os, sys, pathlib
BASE = "/kaggle/working"
os.makedirs(BASE, exist_ok=True)
BLOBS = {
    "motor.py": ("%(b1)s", "%(m1)s"),
    "motor_v2.py": ("%(b2)s", "%(m2)s"),
    "nm_core.py": ("%(b3)s", "%(m3)s"),
}
for nombre, (blob, esperado) in BLOBS.items():
    raw = base64.b64decode(blob)
    got = hashlib.md5(raw).hexdigest()
    if got != esperado:
        raise SystemExit("ABORTA: md5 de " + nombre + " es " + got + " y se esperaba " + esperado)
    pathlib.Path(os.path.join(BASE, nombre)).write_bytes(raw)
    print("escrito " + nombre + "  " + str(len(raw)) + " B  md5 " + got + "  VERIFICADO", flush=True)
os.environ["NM_SHARD"] = "%(shard)d"
os.environ["NM_TOTAL"] = "%(total)d"
os.environ["NM_NULLS"] = "%(nulls)d"
os.environ["NM_STEPS"] = "150"
os.environ["NM_BASE"] = BASE
os.environ["NM_OUT"] = os.path.join(BASE, "nm_out")
print("SHARD=%(shard)d/%(total)d NULLS=%(nulls)d", flush=True)
sys.argv = ["nm_core.py"]
exec(compile(pathlib.Path(os.path.join(BASE, "nm_core.py")).read_text(), "nm_core.py", "exec"),
     {"__name__": "__main__", "__file__": os.path.join(BASE, "nm_core.py")})
'''

# 2 en cada cuenta: son los 4 slots de GPU que existen con dos cuentas
PLAN = [{"acct": 1, "shard": 0, "titulo": "TITAN nm brazos arpack shard 0 de 4"},
        {"acct": 1, "shard": 1, "titulo": "TITAN nm brazos arpack shard 1 de 4"},
        {"acct": 0, "shard": 2, "titulo": "TITAN nm brazos arpack shard 2 de 4"},
        {"acct": 0, "shard": 3, "titulo": "TITAN nm brazos arpack shard 3 de 4"}]

for p in PLAN:
    c = CRED[p["acct"]]
    texto = PRE % {"b1": B1, "m1": M1, "b2": B2, "m2": M2, "b3": B3, "m3": M3,
                   "shard": p["shard"], "total": SHARDS, "nulls": N_NULLS}
    if ('os.environ["NM_SHARD"] = "%d"' % p["shard"]) not in texto:
        print("ABORTA shard %d: el horneado no entro" % p["shard"]); continue
    body = {"slug": c["username"] + "/titan-nm-brazos-arpack-shard-%d-de-4" % p["shard"],
            "newTitle": p["titulo"], "text": texto, "language": "python",
            "kernelType": "script", "isPrivate": True, "enableGpu": True,
            "enableTpu": False, "enableInternet": True,
            "datasetDataSources": [], "competitionDataSources": [],
            "kernelSources": [], "categoryIds": []}
    st, t = api(c, "/kernels/push", "POST", body)
    print("\nshard %d -> %s  HTTP %s  bytes=%d" % (p["shard"], c["username"], st, len(texto)))
    print("  " + " ".join(t.split())[:240])

print("\n===== REFS REALES =====")
for c in CRED:
    st, t = api(c, "/kernels/list?user=%s&page=1&pageSize=100&sortBy=dateRun" % c["username"])
    try:
        arr = json.loads(t)
    except Exception:
        continue
    for k in arr:
        if "nm-brazos" in (k.get("ref") or ""):
            print("  %s   lastRunTime=%s" % (k["ref"], k.get("lastRunTime")))
