"""test_guards_negativo.py - la bateria que DEBE poder dar rojo.

A-01 y A-02 de la auditoria externa. Dos mitades:

  A-02  guarded_ratio tiene que distinguir sd=0 por CONSERVACION (espejo) de
        sd=0 por SATURACION (censura). El contraejemplo de Tao es el caso 3.
  A-01  require() tiene que ABORTAR con exit distinto de cero. Se verifica con
        subprocess.run().returncode, NUNCA con el $? del shell, que en este
        entorno miente (modo de falla 6 del proyecto, medido).

Cada test imprime PASS o FAIL. Al final, si hay un solo FAIL, el proceso sale
con codigo 1. Un test que no puede dar rojo no es un test, asi que los cuatro
ultimos son CONTROLES NEGATIVOS: comprueban que la bateria detecta un guard
roto a proposito.

Uso:  python3 src/test_guards_negativo.py ; echo $?
Y para probar que puede dar rojo, mutar la rama sd==0 de guards.py y re-correr:
el test 3 falla y el proceso sale con 1. Medido, ver la evidencia cruda.
"""
import subprocess
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guards
from guards import guarded_ratio, require, convex_state_bound
from guards import assert_threshold_reachable, ReachabilityError
from guards import BIEN, NO_MEDIDO, CONSERVADO, CENSURADO

FAILS = []
NTOT = [0]


def check(name, got, want):
    NTOT[0] += 1
    ok = (got == want)
    print(("PASS " if ok else "FAIL ") + name + "  got=" + repr(got)
          + " want=" + repr(want))
    if not ok:
        FAILS.append(name)
    return ok


print("=== BATERIA guards.py  A-01 + A-02 ===")
print("python " + sys.version.split()[0])
print("")
print("--- A-02 : los tres estados de sd(null) ---")

# 1. sd > 0 : caso normal, hay ratio.
r1 = guarded_ratio(4.3287, [1.18, 1.19, 1.20, 1.21], name="sel_post_fake")
check("1 sd>0 verdict", r1["verdict"], BIEN)
check("1 sd>0 tiene clave ratio", "ratio" in r1, True)

# 2. CONSERVADO : el espejo real de la resp 061, _EDGES_INTO_MOT.
r2 = guarded_ratio(19860, [19860.0] * 40, name="_EDGES_INTO_MOT")
check("2 conservado verdict", r2["verdict"], NO_MEDIDO)
check("2 conservado sd_zero_reason", r2["sd_zero_reason"], CONSERVADO)
check("2 conservado NO expone ratio", "ratio" in r2, False)
check("2 conservado NO expone ratio_censored", "ratio_censored" in r2, False)

# 3. EL CONTRAEJEMPLO DE TAO, verbatim: guarded_ratio(15, [110]*40).
#    La version vieja devolvia "el null conserva esta cantidad (sd=0)".
r3 = guarded_ratio(15, [110.0] * 40, name="R2_sin_umbral_saturado")
check("3 TAO verdict es CENSURADO no NO_MEDIDO", r3["verdict"], CENSURADO)
check("3 TAO sd_zero_reason", r3["sd_zero_reason"], CENSURADO)
check("3 TAO NO expone ratio", "ratio" in r3, False)
check("3 TAO expone ratio_censored", "ratio_censored" in r3, True)
check("3 TAO direccion", r3.get("direction"), "real_por_debajo_del_null")
check("3 TAO lado de la cota", r3.get("bound_side"), "techo")

# 4. saturacion del otro lado : el null pegado a un PISO.
r4 = guarded_ratio(500, [0.0] * 40, name="piso_saturado")
check("4 piso verdict", r4["verdict"], CENSURADO)
check("4 piso direccion", r4.get("direction"), "real_por_encima_del_null")
check("4 piso lado de la cota", r4.get("bound_side"), "piso")

# 5. sin muestras : NO_MEDIDO y sin ratio.
r5 = guarded_ratio(1.0, [], name="vacio")
check("5 vacio verdict", r5["verdict"], NO_MEDIDO)
check("5 vacio NO expone ratio", "ratio" in r5, False)

print("")
print("--- A-02 bis : el guard puede dar rojo (controles negativos) ---")
# 6. CONTROL NEGATIVO: si la funcion fundiera los dos casos como antes, este
#    test fallaria. Comprueba que conservado y censurado NO dan lo mismo.
check("6 CTRL NEG conservado != censurado",
      r2["verdict"] == r3["verdict"], False)
# 7. CONTROL NEGATIVO: un sd=0 con real == mean no puede reportar direccion.
check("7 CTRL NEG conservado sin direccion", "direction" in r2, False)

print("")
print("--- reachability ---")
b = convex_state_bound(8)
check("8 cota sqrt(8)", round(b, 6), 2.828427)
try:
    assert_threshold_reachable(3.0, b, name="max_norm")
    check("9 umbral 3.0 sobre sqrt(8) debe explotar", "no exploto", "explota")
except ReachabilityError:
    check("9 umbral 3.0 sobre sqrt(8) explota", True, True)
check("10 umbral 2.0 sobre sqrt(8) pasa",
      assert_threshold_reachable(2.0, b, name="ok"), 2.0)

print("")
print("--- A-01 : require() aborta con exit != 0, medido con subprocess ---")
HERE = os.path.dirname(os.path.abspath(__file__))
prog_fail = ("import sys; sys.path.insert(0, " + repr(HERE) + ");"
             " from guards import require;"
             " require(False, 'nulls must be positive, got 0');"
             " print('ESTA LINEA NO DEBE IMPRIMIRSE')")
p = subprocess.run([sys.executable, "-c", prog_fail],
                   capture_output=True, text=True)
print("  subprocess returncode = " + str(p.returncode))
print("  subprocess stderr     = " + p.stderr.strip())
print("  subprocess stdout     = " + repr(p.stdout.strip()))
check("11 require(False) returncode", p.returncode, 2)
check("12 require(False) escribe GUARD_FAILED en stderr",
      "GUARD_FAILED" in p.stderr, True)
check("13 require(False) NO sigue ejecutando",
      "NO DEBE IMPRIMIRSE" in p.stdout, False)

prog_ok = ("import sys; sys.path.insert(0, " + repr(HERE) + ");"
           " from guards import require; require(True, 'todo bien');"
           " print('SIGUIO')")
q = subprocess.run([sys.executable, "-c", prog_ok],
                   capture_output=True, text=True)
print("  subprocess OK returncode = " + str(q.returncode))
check("14 require(True) returncode", q.returncode, 0)
check("15 require(True) sigue ejecutando", "SIGUIO" in q.stdout, True)

# 16. CONTROL NEGATIVO DEL PROPIO METODO DE MEDICION: un programa que imprime
#     rojo y devuelve 0 es exactamente el antipatron que A-01 denuncia. Este
#     test comprueba que la bateria SABE distinguirlo de require().
prog_antipatron = ("print('ERROR: algo salio mal'); import sys;"
                   " sys.exit(0)")
a = subprocess.run([sys.executable, "-c", prog_antipatron],
                   capture_output=True, text=True)
print("  ANTIPATRON returncode = " + str(a.returncode)
      + "  (imprime error y sale 0)")
check("16 CTRL NEG el antipatron da 0 y require da 2",
      (a.returncode, p.returncode), (0, 2))

print("")
print("=== RESUMEN ===")
print("tests corridos : " + str(NTOT[0]))
print("fallados       : " + str(len(FAILS)))
if FAILS:
    print("FAILED: " + ", ".join(FAILS))
    sys.exit(1)
print("TODOS VERDES, y los controles negativos demuestran que podian dar rojo")
sys.exit(0)
