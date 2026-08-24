"""guards.py - los tres estados, con propagacion al consumidor.

Por que existe: en este corpus aparecieron TRES guards que no podian dar rojo,
en tres archivos distintos, escritos en momentos distintos.

  1. src/scriptR.py:88-90   np.clip(h, -clip, clip) y despues if mx > 1e6
     Con clip=2.0 la condicion es inalcanzable. Medido sobre results/R_out.json:
     2 de 15 celdas quedaron PEGADAS al clip (max_abs_h60 = 2.0000 exacto) y el
     script las reporto con diverged=False.
  2. BICAMERALITY LiquidChaosCell(H=8, max_norm=3.0)
     La cota analitica es sqrt(8)=2.8284 < 3.0. Rama muerta. Medido: 0 de
     12800 activaciones, y 0 tambien con estimulo x100.
  3. BICAMERALITY survival loss con etiqueta constante
     sd(label)=0 en 56 de 56 lotes. La loss no ensena nada, Y el veto que
     consume su salida sigue castigando la exploracion.

El 3 es el que da la regla que faltaba: NO alcanza con excluir el termino de la
loss. Hay que APAGAR a quien consume la senal. Medido en tres brazos: excluir
el termino y dejar el veto prendido da un resultado PEOR que no hacer nada,
porque la loss tautologica estaba mitigando accidentalmente su propio dano.

src/motor.py:383 ya hace bien la mitad: marca NO_TESTEABLE y omite la clave
"ratio", asi que un consumidor que la lea explota en vez de leer un 1.000x
falso, y excluye el estadistico del test global. Este modulo generaliza eso y
le agrega la propagacion explicita a consumidores arbitrarios.

Evidencia: results/test_guards.log (16 tests, 0 en rojo).
"""
import math

__all__ = [
    "ReachabilityError",
    "convex_state_bound",
    "assert_threshold_reachable",
    "guarded_ratio",
    "TautologyGuard",
]

BIEN = "BIEN"
MAL = "MAL"
NO_MEDIDO = "NO_MEDIDO"


class ReachabilityError(ValueError):
    """Un umbral que ninguna ejecucion puede cruzar.

    Fail-closed a proposito: es mejor no construir el objeto que construir un
    guard decorativo, porque el proximo que lo lea va a razonar sobre un caso
    que no existe.
    """


def convex_state_bound(H):
    """Cota de la norma de h para h = (1-t)*h + t*f(.) con t en (0,1), |f|<=1.

    Cada componente es combinacion convexa de dos valores en [-1,1], asi que
    queda en [-1,1] y la norma euclidea no puede pasar sqrt(H).
    Verificado: con H=8 y estimulo x100 la norma llega a 2.828427 = sqrt(8).
    """
    if H <= 0:
        raise ValueError("H debe ser positivo, no " + repr(H))
    return math.sqrt(float(H))


def assert_threshold_reachable(threshold, bound, name="umbral", margin=0.0):
    """Levanta ReachabilityError si threshold no puede cruzarse nunca.

    bound es el maximo que la cantidad medida puede alcanzar. Si el umbral esta
    en o por encima de esa cota, la rama es codigo muerto.
    Devuelve el umbral para permitir uso en linea.
    """
    b = float(bound)
    t = float(threshold)
    if t >= b - float(margin):
        raise ReachabilityError(
            name + "=" + repr(t) + " es INALCANZABLE: la cantidad medida esta"
            " acotada por " + format(b, ".6f") + ". Un guard cuya rama nunca se"
            " ejecuta no protege nada y hace creer que si.")
    return t


def guarded_ratio(real, null_samples, name="estadistico"):
    """Ratio real/null solo cuando el null tiene varianza. Fail-closed.

    Si sd(null) == 0 el null CONSERVA la cantidad y el test no puede fallar:
    cualquier ratio seria una tautologia con forma de resultado. En ese caso el
    dict devuelto NO tiene la clave "ratio", asi que un consumidor que la lea
    explota en vez de leer un 1.000x falso. Es el patron que ya usa
    src/motor.py:383, generalizado.
    """
    col = [float(x) for x in null_samples]
    n = len(col)
    if n == 0:
        return {"name": name, "verdict": NO_MEDIDO,
                "reason": "no hay muestras del null"}
    mu = sum(col) / n
    var = sum((x - mu) ** 2 for x in col) / n
    sd = var ** 0.5
    if sd == 0.0:
        return {"name": name, "verdict": NO_MEDIDO,
                "reason": "el null conserva esta cantidad (sd=0)",
                "real": float(real), "null_mean": mu, "null_sd": 0.0,
                "n": n}
    ge = sum(1 for x in col if x >= real)
    le = sum(1 for x in col if x <= real)
    return {"name": name, "verdict": BIEN, "real": float(real),
            "null_mean": mu, "null_sd": sd, "n": n,
            "ratio": (float(real) / mu) if mu != 0 else float("inf"),
            "n_ge": ge, "n_le": le,
            "p_two": min(1.0, 2.0 * min(ge + 1.0, le + 1.0) / (n + 1.0)),
            "p_floor": 2.0 / (n + 1.0)}


class TautologyGuard:
    """Guard de tautologia CON propagacion al consumidor.

    La leccion que costo una corrida entera: excluir un termino tautologico de
    la loss NO alcanza. Medido en tres brazos sobre PureMemory 240 ep:

        A original, sin guard, veto ON      factor sobre el std  0.286 -> 0.351
        B con guard en la loss, veto ON      factor sobre el std  0.281 -> 0.290
        C con guard Y veto apagado           factor sobre el std  1.000

    B es PEOR que A. La loss tautologica no ensenaba nada, pero arrastraba el
    estimador hacia el target constante y con eso iba aflojando el castigo que
    ella misma causaba. Al sacar el termino sin apagar el consumidor, queda el
    dano y se pierde la mitigacion.

    Uso:
        g = TautologyGuard()
        g.register("energy", consumers=["veto"])
        ...
        if g.observe("energy", batch_labels):
            loss = loss + mse(pred, batch_labels)
        if g.enabled("veto"):
            lstd = lstd + veto_shift
    """

    def __init__(self):
        self.labels = {}
        self.consumers = {}
        self.counts = {}

    def register(self, label, consumers=()):
        """Declara una etiqueta y que consumidores dependen de su senal."""
        self.labels[label] = list(consumers)
        self.counts[label] = {"usada": 0, "no_testeable": 0}
        for c in consumers:
            self.consumers.setdefault(c, set()).add(label)
        return self

    def observe(self, label, values):
        """Mira un lote de etiquetas. Devuelve True si el termino se puede usar.

        Si sd == 0 el termino se cuenta NO_TESTEABLE y ademas queda marcado el
        lote como no informativo para todos sus consumidores.
        """
        if label not in self.labels:
            raise KeyError(
                "etiqueta " + repr(label) + " no registrada. Llamar register()"
                " primero: sin declarar los consumidores no hay propagacion, y"
                " un guard sin propagacion deja actuar la causa.")
        vals = [float(v) for v in _flatten(values)]
        n = len(vals)
        if n == 0:
            ok = False
        else:
            mu = sum(vals) / n
            ok = any(v != mu for v in vals)
        self.counts[label]["usada" if ok else "no_testeable"] += 1
        self._last = getattr(self, "_last", {})
        self._last[label] = ok
        return ok

    def enabled(self, consumer):
        """Un consumidor esta habilitado solo si TODAS sus etiquetas informan.

        Fail-closed: si una etiqueta no fue observada todavia, se considera no
        informativa. Es la diferencia entre BIEN, MAL y NO_MEDIDO aplicada al
        consumidor y no solo al termino de la loss.
        """
        if consumer not in self.consumers:
            raise KeyError("consumidor " + repr(consumer) + " no registrado")
        last = getattr(self, "_last", {})
        return all(last.get(lb, False) for lb in self.consumers[consumer])

    def report(self):
        """Estado por etiqueta y por consumidor, para commitear como evidencia."""
        last = getattr(self, "_last", {})
        out = {"labels": {}, "consumers": {}}
        for lb, c in self.counts.items():
            tot = c["usada"] + c["no_testeable"]
            out["labels"][lb] = {
                "usada": c["usada"], "no_testeable": c["no_testeable"],
                "frac_no_testeable": (c["no_testeable"] / tot) if tot else None,
                "verdict": (NO_MEDIDO if c["usada"] == 0 and tot else BIEN)}
        for cs, lbs in self.consumers.items():
            out["consumers"][cs] = {
                "depende_de": sorted(lbs),
                "habilitado_en_el_ultimo_lote": all(
                    last.get(lb, False) for lb in lbs)}
        return out


def _flatten(x):
    """Aplana listas, tuplas y tensores o arrays con .reshape(-1).tolist()."""
    if hasattr(x, "reshape") and hasattr(x, "tolist"):
        return x.reshape(-1).tolist()
    if isinstance(x, (list, tuple)):
        out = []
        for it in x:
            out.extend(_flatten(it))
        return out
    return [x]
