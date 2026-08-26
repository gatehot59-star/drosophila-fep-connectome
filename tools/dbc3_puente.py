"""Que del DBC3 es TRANSFERIBLE a DualBrain y al puente conectoma->chip.

La pregunta no es "cual motor es mejor". Es: hay alguna PROPIEDAD del DBC3 que,
movida a otro de los tres motores, lo mejore. Eso se mide, no se opina.

Los tres motores del expediente, con sus numeros ya medidos:
  motor.py (conectoma) 138.639 neuronas, tau COMPLEJA pero FIJA por neurona
  DBC3-v3              6.888 params, tau REAL y DINAMICA (depende de la entrada)
  DualBrain (ESP32)    3.553 params, tau_learner de 528 params, 800 B de RAM

El eje que los separa NO es el tamano: es COMO se decide tau.

Uso:
    python3 dbc3_puente.py    # requiere dbc3_lib.py en el mismo directorio
"""
import numpy as np
import torch
import torch.nn.functional as F

import dbc3_lib as L

print("=" * 90)
print("P-1  El tau del DBC3 VARIA de verdad? Si no varia, el tau_learner es adorno")
print("=" * 90)
print("  Si tau resultara casi constante, sus 820 params (11,9%) no aportan nada,")
print("  y no habria nada que transferir. Es la primera cosa que hay que falsar.")
print()
torch.manual_seed(5)
cfg = L.DBC3Config(36, 12, 20, 36)
net = L.DBC3Motor(cfg)
with torch.no_grad():
    for lbl, scale in (("entrada chica |x|~0.1", 0.1),
                       ("entrada media |x|~1.0", 1.0),
                       ("entrada grande |x|~3.0", 3.0)):
        hm = torch.zeros(8, 20)
        taus = []
        for t in range(40):
            x = torch.randn(8, 36) * scale
            e = L.gelu_c(F.linear(x, net.W_enc, net.b_enc))
            tau = torch.sigmoid(F.linear(torch.cat([e, hm], -1), net.W_tau, net.b_tau))
            taus.append(tau.numpy())
            _, hm = net._step(x, hm)
        a = np.concatenate(taus)
        print("  %-24s tau: min=%.4f med=%.4f max=%.4f  sd_canales=%.4f  sd_tiempo=%.4f"
              % (lbl, a.min(), np.median(a), a.max(),
                 a.std(axis=0).mean(), a.std(axis=1).mean()))
print()
print("  sigmoid(b_tau=-2.0) = %.6f  <- el punto de partida; motor.py usa 0.119 fijo"
      % float(torch.sigmoid(torch.tensor(-2.0))))
print()

print("=" * 90)
print("P-2  Los tres motores comparten LA MISMA ecuacion. Lo unico distinto es tau")
print("=" * 90)
print("  motor.py     z  <- (1-tau)*z  + tau*f(W^T z + s)          tau COMPLEJA, FIJA")
print("  DBC3         hm <- (1-tau)*hm + tau*f(W_in e + W_res hm)  tau REAL, DINAMICA")
print("  DualBrain    idem DBC3, con tau_learner de 528 params")
print()
rows = [("motor.py (conectoma)", "15.091.983 aristas", "compleja", "NADA (fija)", "si, clip 2.0"),
        ("DBC3-v3", "6.888", "real", "entrada+estado", "no (LN emergente)"),
        ("DBC3-v4", "6.936", "real", "entrada+estado", "si, tanh 3.0"),
        ("DualBrain (ESP32)", "3.553", "real", "entrada+estado", "por medir")]
print("  %-22s %18s %10s %16s %18s" % ("motor", "tamano", "tau", "depende de", "acotado?"))
for a, b, c, d, e in rows:
    print("  %-22s %18s %10s %16s %18s" % (a, b, c, d, e))
print()
print("  EL HUECO QUE ESTO EXPONE: motor.py tiene tau compleja pero ESTATICA.")
print("  DBC3 tiene tau dinamica pero REAL. Nadie probo tau compleja Y dinamica,")
print("  y esa combinacion es exactamente el cruce de los dos motores del proyecto.")
print()

print("=" * 90)
print("P-3  El fix M-2 del DBC3-v4 aplica a motor.py? Se lee el sujeto exacto")
print("=" * 90)
print("  M-2 dice: normalizar el CANDIDATO, no el ESTADO, porque normalizar el")
print("  estado le saca a tau el control de la escala.")
print()
print("  motor.py hace:  z = (1-tau)*z + tau*bounded_complex_tanh(drive)")
print("  o sea: acota la ACTIVACION (el candidato), NO el estado ya mezclado.")
print("  VEREDICTO: motor.py YA hace lo correcto. El defecto es exclusivo del DBC3,")
print("  y la transferencia va del motor del conectoma al del chip, no al reves.")
print()

print("=" * 90)
print("P-4  Que le puede dar el DBC3 al DualBrain del ESP32, con su costo")
print("=" * 90)
m, r = 16, 32
cost_rgate = r * (r + m) + r
cost_bias = 2 * m
print("  El DualBrain embebido tiene el MISMO gate asimetrico que el DBC3-v3:")
print("  modula la memoria y no el reflejo. El fix M-1 le costaria:")
print("    gate de reflejo: %d params sobre 3.553 = +%.1f%%"
      % (cost_rgate, 100.0 * cost_rgate / 3553))
print("    bias en el nucleo: %d params = +%.1f%%" % (cost_bias, 100.0 * cost_bias / 3553))
print("    RAM extra: %d B sobre 800 B = +%.1f%%" % (r * 4, 100.0 * (r * 4) / 800))
print()
print("  El M-1 en el chip es CARO en proporcion: +%.0f%% de parametros."
      % (100.0 * cost_rgate / 3553))
print("  En el DBC3 se pago bajando h_m de 20 a 13. En un micro con 800 B de RAM")
print("  ese pago no es gratis y hay que medirlo ANTES de tocar el firmware.")
print()
print("  NOTA: m=16 y r=32 son las dimensiones SUPUESTAS del DualBrain embebido a")
print("  partir de su blob de 3553 floats. NO estan leidas de su header en esta")
print("  corrida, asi que los tres costos de arriba son ESTIMACIONES, no medicion.")
