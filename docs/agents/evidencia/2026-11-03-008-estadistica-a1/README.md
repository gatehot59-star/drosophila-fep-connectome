# Evidencia cruda de 2026-11-03-008 (brain-env)

Salida verbatim de dos llamadas en brain-env. En la segunda, mi propio `print` cortó cada línea de la suite a 260 caracteres; los logs completos están en `/workspace/a1/v2/evid8/prueba_estadistica.log`.

## Bajada desde raw en 5c9492ff y huellas
```
BAJADO tools/a1/estadistica_a1.py 36891 37ab63d7dc94913c010cdc51d89a23a0ace0a4e6e511b4c344ffad15b24503e3
BAJADO tools/a1/prueba_estadistica_a1.py 48950 74aec761d7e63b7607256d97e09cf0941cdf3d5d858b4a65c390ca5d9c0fd108
BAJADO tools/a1/mutantes_estadistica_a1.py 8976 86c5e4f78426c3114a80a02b6a9e04bfe2309319cd9e47a9862f18a61f6ac5b2
BAJADO tools/a1/HUELLAS_ESTADISTICA.sha256 295 0b91d455b16f2bbda939709dd0c652d50c6715f0dc1f2a387f20b522f8027e25
BAJADO tools/a1/comun_a1.py 8679 756e81aba922824f0bf4e6374936b944b7f30c17e88b659adc35b9416c0d93ed
BAJADO tools/a1/plan_a1.py 5408 d1b26450ecf8e9ca5211ab7a78beadf536ff61c4db659ed79c3dd9e142662e5d
BAJADO tools/a1/juntar_a1.py 7757 051d0b474a911930db692fed5826839b426df2953eebd39a86ab69538260d414
BAJADO tools/a1/validar_a1.py 6401 189eb6477e1f9e3685d273d89aaee4dca8c8c8a63a82a734dae74b2a6ad34e20
HUELLAS exit=0
tools/a1/estadistica_a1.py: OK
tools/a1/prueba_estadistica_a1.py: OK
tools/a1/mutantes_estadistica_a1.py: OK

MANIFIESTO 267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9 640908
python=3.12.14 ejecutable=/usr/local/bin/python3
numpy=2.5.3 scipy=1.18.1
nproc_all=4
cpu=Intel(R) Celeron(R) N4020 CPU @ 1.10GHz x2
MemTotal:        7989580 kB MemAvailable:    1263212 kB
kernel=4.19.0-27-amd64
LANZADO pid=2252
```

## Suite en brain-env (inicio 2026-11-03T19:17:53Z, fin 19:18:46Z, exit 0)
```
PRUEBA E01 PASS 300 vectores, max dif contra scipy ttest_1samp(greater)=3.12e-16; constante -> VARIANZA_CERO p=None; rojo: bilateral difiere en 3.381e-01; media negativa p=1.000000 (0.4 s)
PRUEBA E03 PASS 500 vectores de 46 con empates y unos: max dif contra Holm aparte=0.0e+00, decisiones distintas de la regla secuencial=0; rojo: en (0.0001, 0.00022, 44 x 0.9) Holm rechaza 2 y Bonferroni 1 (0.2 s)
PRUEBA E05 PASS denominador con media 0,3 y remuestreos negativos -> INDEFINIDO (estimado 3.3333); denominador -1 -> SIN_ESTIMADO; 0 -> SIN_ESTIMADO; media constante -> DEGENERADO; cociente a/a -> DEGENERADO; control: cociente comun -> OK (0.0 s)
PRUEBA E06 PASS F_B=46 (relevos DQ2, hubs DQ2, T1, T2 = (16, 6, 6, 18)), F_C=6, F_R01=3; registro de 722 ids, identico con celdas validas o invalidas=True; rojo: sin H3 en el manifiesto -> ABORTA: la prueba B|H3|DQ2 no esta en el registro (0.2 s)
PRUEBA E07 PASS escenario todo: 13/13 chequeos (fallan -); B|R01 r_Q1=0.7377 IC95=[0.7207; 0.7553], s4=0.8951 IC95=[0.8639; 0.9176]; B|H1 r_Q1conj=0.7470 IC95=[0.7312; 0.7650] (1.3 s)
PRUEBA E08 PASS R02 con r1=0,20: r_Q1=0.1889 IC95=[0.1720; 0.2122] contradice el margen 0,35=True; T1=NO_PASA:SIN_DECIDIR; P_T1_B=SIN_DECIDIR (1.4 s)
PRUEBA E11 PASS H2 invalida y H3 con rc=0,1: tipos={"CB0172": "NO_PASA:SIN_DECIDIR", "CB0534": "BLOQUEADO", "CB0580": "PASA", "PS100": "PASA"} -> P_T2_B=INVALIDO_TECNICO (1.2 s)
PRUEBA E13 PASS H1b con rc=0,1: CB0580 NO_PASA:SIN_DECIDIR aunque H1 PASA, P_T2_B=SOSTENIDA (3 de 4 tipos); H1b y H4 con rc=0,1: P_T2_B=SIN_DECIDIR (2.5 s)
PRUEBA E14 PASS margen T1 de 0,80 sobre r1=0,75: P_T1_B=SIN_DECIDIR, r_Q1 IC95=[0.7207; 0.7553] con margen 0.8; P_T2_B sigue SOSTENIDA (1.1 s)
PRUEBA E20 PASS freno chico de media 7 Hz con p crudo 0.00704: solo en R04 -> ACTIVADO (Holm 0.00704); en R04 y R10 -> NO_INFORMATIVO_EN_B y NO_INFORMATIVO_EN_B, causa unica ['DQ2_F_B_holm_lt_001'], IC95 de DQ2=[2.12; 11.90], Holm 0.01409 (2.5 s)
PRUEBA E21 PASS 23 estimandos recalculados aparte desde 010: max dif relativa=0.0e+00 (fallan -); tasa por neurona y fracciones C0 iguales=True; rojo: T2c con el maximo de los cortes individuales daria 116.40 y no 238.95 (0.4 s)
PRUEBA E22 PASS driver y x en 10,0 Hz -> ACTIVADO; DQ2 en 5,0 Hz -> ACTIVADO; C_10 en 10,0 Hz -> ON y C_01 en 2,0 Hz -> OFF, transferencia OTRA_TRANSFERENCIA (1.2 s)
PRUEBA E23 PASS ZA3 en contra (QCOL con ZA sube el D): contrastes={"ZA1": true, "ZA2": true, "ZA3": false}, ZA3 media=-126.70 -> firma SIN_DECIDIR; P_T1_B sigue SOSTENIDA (1.3 s)
PRUEBA_ESTADISTICA 23/23 PASS
MUTANTES inicio n=28 sin=E17,E18
CONTROL original exit=0 caidas=- PRUEBA_ESTADISTICA 21/21 PASS (32.8 s)
```
Las líneas de E02, E04, E09, E10, E12 y E15 a E19 salieron cortadas por mi `print` a 260 caracteres; todas dicen PASS y están completas en el log de brain-env. La corrida de mutantes seguía en curso.

## Cómo edita pesos el runner (lectura de `runner_a1.py`, líneas citadas)
```
9 edita una copia de los pesos y verifica que fuera de la mascara queden identicos.
168             chq['mascara_en_cero'] = bool(np.all(leido[filas] == 0.0))
```
De ahí sale la advertencia de la respuesta: con x apagado del todo en Q1, Q1 y Q2 dejan la red idéntica fuera de x.
