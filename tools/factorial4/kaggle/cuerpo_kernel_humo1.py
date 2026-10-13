# ---- cuerpo comun de los kernels del factorial 4 (tools/factorial4/kaggle/cuerpo_kernel.py) ----
# Trae el repo en el SHA sellado, verifica md5 del instrumento y de los insumos, corre cerebro_mosca.py con los
# argumentos del plan y deja logs, json y un recibo en /kaggle/working. Sale siempre 0 para que Kaggle guarde la
# salida; el resultado real va en recibo_<kernel>.json (rc 0 completo, 2 pin distinto, 3 control fallido, 4 git).
import hashlib
import os
import subprocess
import sys
import tarfile
import time
import urllib.request

OUT = "/kaggle/working"
TRAB = "/tmp/f4"


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Kernel:
    def __init__(self):
        self.t0 = time.time()
        os.makedirs(OUT, exist_ok=True)
        os.makedirs(TRAB, exist_ok=True)
        self.log = open(os.path.join(OUT, "kernel_%s.log" % CONFIG["kernel"]), "w")
        self.rec = dict(kernel=CONFIG["kernel"], config=CONFIG, etapas={}, corridas=[],
                        inicio_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def escribir(self, s):
        self.log.write(s + "\n")
        self.log.flush()
        print(s, flush=True)

    def correr(self, cmd, archivo=None):
        self.escribir("$ " + " ".join(cmd))
        try:
            if archivo:
                with open(archivo, "w") as f:
                    r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
                return r.returncode, ""
            r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except OSError as e:
            self.escribir("no se pudo ejecutar: %r" % e)
            return 127, ""
        self.escribir(r.stdout.rstrip() + "\nrc=%d" % r.returncode)
        return r.returncode, r.stdout

    def fin(self, rc, motivo):
        self.rec.update(rc=rc, motivo=motivo, duracion_s=round(time.time() - self.t0, 1),
                        fin_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        ruta = os.path.join(OUT, "recibo_%s.json" % CONFIG["kernel"])
        with open(ruta, "w") as f:
            json.dump(self.rec, f, indent=1)
        self.escribir("FIN rc=%d motivo=%s recibo_md5=%s" % (rc, motivo, md5(ruta)))
        self.log.close()
        sys.exit(0)


def traer_repo(k):
    repo = os.path.join(TRAB, "repo")
    ok = True
    for c in (["git", "init", "-q", repo],
              ["git", "-C", repo, "fetch", "-q", "--depth", "1", CONFIG["repo"], CONFIG["sha"]],
              ["git", "-C", repo, "checkout", "-q", "FETCH_HEAD"]):
        if k.correr(c)[0]:
            ok = False
            break
    if ok:
        head = k.correr(["git", "-C", repo, "rev-parse", "HEAD"])[1].strip()
        k.rec["etapas"]["via"], k.rec["etapas"]["head"] = "git", head
        if head != CONFIG["sha"]:
            k.fin(4, "el HEAD traido no es el SHA sellado")
        return repo
    # sin git: el tarball de GitHub en el mismo SHA; el control es el md5 de cada archivo del instrumento
    tgz = os.path.join(TRAB, "repo.tar.gz")
    try:
        urllib.request.urlretrieve(CONFIG["tarball"] + CONFIG["sha"], tgz)
        with tarfile.open(tgz) as t:
            raiz = t.getnames()[0].split("/")[0]
            t.extractall(TRAB)
    except Exception as e:  # noqa: BLE001
        k.escribir("tarball fallo: %r" % e)
        k.fin(4, "no se pudo traer el repo")
    k.rec["etapas"]["via"], k.rec["etapas"]["head"] = "tarball", CONFIG["sha"]
    return os.path.join(TRAB, raiz)


def main():
    k = Kernel()
    k.escribir("# kernel %s | respuesta %s | sha %s" % (CONFIG["kernel"], CONFIG["respuesta"], CONFIG["sha"]))
    k.rec["etapas"]["pip_rc"] = k.correr([sys.executable, "-m", "pip", "install", "-q", "--no-input"] + CONFIG["pip"])[0]
    repo = traer_repo(k)
    mal = {}
    for p, m in sorted(CONFIG["md5"].items()):
        ruta = os.path.join(repo, p)
        mm = md5(ruta) if os.path.exists(ruta) else "-"
        if mm != m:
            mal[p] = mm
    k.rec["etapas"]["md5_instrumento"] = "OK" if not mal else mal
    k.escribir("MD5 instrumento (%d archivos) -> %s" % (len(CONFIG["md5"]), "OK" if not mal else mal))
    if mal:
        k.fin(2, "md5 del instrumento distinto del pin")
    rutas = {}
    for nombre, (url, m) in sorted(CONFIG["insumos"].items()):
        dest = os.path.join(TRAB, nombre)
        for intento in range(3):
            try:
                urllib.request.urlretrieve(url, dest)
                break
            except Exception as e:  # noqa: BLE001
                k.escribir("descarga %s intento %d fallo: %r" % (nombre, intento + 1, e))
                time.sleep(15)
        mm = md5(dest) if os.path.exists(dest) else "-"
        k.rec["etapas"]["md5_" + nombre] = mm
        k.escribir("MD5 %s = %s (pin %s)" % (nombre, mm, m))
        if mm != m:
            k.fin(2, "md5 del insumo %s distinto del pin" % nombre)
        rutas[nombre] = dest
    k.correr(["nvidia-smi"])
    k.correr([sys.executable, "-c", "import numpy, pandas, scipy, pyarrow, torch; print('versiones', numpy.__version__, "
              "pandas.__version__, scipy.__version__, pyarrow.__version__, torch.__version__, torch.version.cuda, "
              "torch.cuda.is_available())"])
    peor = 0
    for c in CONFIG["corridas"]:
        et = c["etiqueta"]
        dout, rlog = os.path.join(OUT, et), os.path.join(OUT, "%s.log" % et)
        cmd = [sys.executable, os.path.join(repo, CONFIG["script"]), "--conn", rutas["connectivity.parquet"],
               "--annot", rutas["annotations.tsv"], "--out", dout] + c["args"]
        t1 = time.time()
        rc = k.correr(cmd, rlog)[0]
        sal = {a: md5(os.path.join(dout, a)) for a in sorted(os.listdir(dout))} if os.path.isdir(dout) else {}
        with open(rlog) as f:
            lineas = [x for x in f.read().splitlines() if x and not x.startswith(" ") and "Warning" not in x]
        k.escribir("\n".join(lineas[-80:]))
        k.rec["corridas"].append(dict(etiqueta=et, args=c["args"], rc=rc, duracion_s=round(time.time() - t1, 1),
                                      log_md5=md5(rlog), salidas_md5=sal))
        k.escribir("CORRIDA %s rc=%d %.1f s" % (et, rc, time.time() - t1))
        peor = max(peor, rc)
    k.fin(peor, "corridas")


main()
