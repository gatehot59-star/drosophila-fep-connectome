/* db_main.c - arnes de verificacion del nucleo DualBrain.
 *
 * Por que existe: el arnes original (db_test.c de Tachi) necesita
 * dualbrain_weights.bin, un blob de 14.420 B que vive en /kaggle/working y no
 * esta en ningun repo. Sin ese archivo la autoprueba no corre.
 *
 * Este arnes usa un blob generado por gen_blob.py con pesos deterministas y su
 * oraculo calculado en numpy DESDE EL HEADER. Verifica dos cosas distintas:
 *
 *   1. db_selftest() contra el vector embebido en el blob  -> un paso
 *   2. una secuencia de 512 pasos contra el oraculo         -> acumulacion
 *
 * Y los 7 casos negativos de db_bind, cada uno con su codigo esperado. Un arnes
 * que solo prueba el camino feliz no mide nada.
 *
 * Dos modos de compilacion:
 *   -DDB_HOSTED   lee los .bin del disco. Para x86.
 *   (por defecto) el blob va embebido en un array alineado a 4. Para LINKEAR un
 *                 .elf de MCU sin sistema de archivos, sin stdio y sin malloc.
 */
#include <dualbrain.h>

#ifdef DB_HOSTED
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int fails = 0;

static void *slurp(const char *path, long *n_out)
{
    FILE *f = fopen(path, "rb");
    void *p;
    long n;
    if (f == 0) { return 0; }
    fseek(f, 0, SEEK_END);
    n = ftell(f);
    fseek(f, 0, SEEK_SET);
    /* malloc devuelve memoria alineada para cualquier tipo fundamental */
    p = malloc((size_t)n);
    if (p == 0) { fclose(f); return 0; }
    if (fread(p, 1u, (size_t)n, f) != (size_t)n) { fclose(f); free(p); return 0; }
    fclose(f);
    if (n_out != 0) { *n_out = n; }
    return p;
}

static void check(const char *name, int ok)
{
    printf("  %-42s %s\n", name, ok ? "OK" : "FALLA");
    if (!ok) { fails++; }
}

static void neg(const char *name, const unsigned char *blob, long n,
                long corrupt_at, unsigned char newval, db_status want)
{
    unsigned char *copy = (unsigned char *)malloc((size_t)n);
    db_weights w;
    db_status got;
    char line[128];
    if (copy == 0) { check(name, 0); return; }
    memcpy(copy, blob, (size_t)n);
    if (corrupt_at >= 0) { copy[corrupt_at] = newval; }
    got = db_bind(&w, copy, (uint32_t)n);
    sprintf(line, "%s  esperado=%d obtenido=%d", name, (int)want, (int)got);
    check(line, got == want);
    free(copy);
}

int main(void)
{
    db_weights w;
    db_state s;
    unsigned char *blob;
    float *seq, *ora_act, *ora_hm;
    long nb = 0, ns = 0, na = 0, nh = 0;
    float act[DB_ACT];
    float err, worst_act = 0.0f, worst_hm = 0.0f, selferr = 0.0f;
    int i, t, worst_t = -1;
    db_status st;

    printf("=== ARNES DualBrain (blob sintetico + oraculo numpy) ===\n");
#ifdef DB_FAST_TANH
    printf("  tanh          : PADE [7/8], sin libm\n");
#else
    printf("  tanh          : tanhf de libm\n");
#endif
    printf("  dims          : OBS=%d HR=%d HM=%d ACT=%d Z=%d\n",
           DB_OBS, DB_HR, DB_HM, DB_ACT, DB_Z);
    printf("  DB_N_FLOATS   : %d\n", DB_N_FLOATS);
    printf("  DB_BLOB_BYTES : %u\n", (unsigned)DB_BLOB_BYTES);
    printf("  MACs por paso : %u\n", (unsigned)db_macs_per_step());
    printf("  RAM de estado : %u bytes\n", (unsigned)db_state_bytes());
    printf("  sizeof(float) : %u\n", (unsigned)sizeof(float));

    blob = (unsigned char *)slurp("weights.bin", &nb);
    seq = (float *)slurp("seq.bin", &ns);
    ora_act = (float *)slurp("oracle_acts.bin", &na);
    ora_hm = (float *)slurp("oracle_hm.bin", &nh);
    if (blob == 0 || seq == 0 || ora_act == 0 || ora_hm == 0) {
        printf("GUARD_FAILED falta uno de los .bin\n");
        return 2;
    }

    printf("\n=== BIND ===\n");
    printf("  weights.bin   : %ld bytes\n", nb);
    st = db_bind(&w, blob, (uint32_t)nb);
    printf("  db_bind       : %d %s\n", (int)st, st == DB_OK ? "DB_OK" : "ERROR");
    if (st != DB_OK) { return 2; }
    printf("  header dims   : obs=%u hr=%u hm=%u act=%u n_floats=%u\n",
           (unsigned)w.obs, (unsigned)w.hr, (unsigned)w.hm,
           (unsigned)w.act, (unsigned)w.n_floats);

    printf("\n=== AUTOPRUEBA EMBEBIDA (1 paso desde t_hm_in) ===\n");
    st = db_selftest(&w, 1.0e-5f, &selferr);
    printf("  err_max       : %.4e\n", (double)selferr);
    printf("  veredicto     : %s\n", st == DB_OK ? "DB_OK" : "DB_ERR_SELFTEST");
    check("autoprueba embebida", st == DB_OK);

    printf("\n=== SECUENCIA CONTRA EL ORACULO numpy ===\n");
    db_reset(&s);
    for (t = 0; t < 512; ++t) {
        db_step(&w, &s, seq + (long)t * DB_OBS, act);
        err = act[0] - ora_act[t];
        if (err < 0.0f) { err = -err; }
        if (err > worst_act) { worst_act = err; worst_t = t; }
    }
    for (i = 0; i < DB_HM; ++i) {
        err = s.h_m[i] - ora_hm[i];
        if (err < 0.0f) { err = -err; }
        if (err > worst_hm) { worst_hm = err; }
    }
    printf("  pasos         : 512\n");
    printf("  err_max act   : %.4e  (peor en t=%d)\n", (double)worst_act, worst_t);
    printf("  err_max h_m   : %.4e\n", (double)worst_hm);
    /* el ultimo act de la secuencia, contra su oraculo. En la v1 de este
       arnes esta linea imprimia (double)0.0f en vez del valor real: un bug
       cosmetico que no afectaba el veredicto pero mentia en la salida. */
    printf("  act[511]      : %.8f   oraculo %.8f\n",
           (double)act[0], (double)ora_act[511]);
    check("secuencia de 512 pasos vs oraculo", worst_act < 1.0e-4f);

    printf("\n=== CASOS NEGATIVOS (deben FALLAR) ===\n");
    neg("magic corrupto        ", blob, nb, 0, 88u, DB_ERR_MAGIC);
    neg("version 99            ", blob, nb, 4, 99u, DB_ERR_VERSION);
    neg("HR declarado 33       ", blob, nb, 12, 33u, DB_ERR_DIMS);
    neg("n_floats declarado +1 ", blob, nb, 24,
        (unsigned char)((DB_N_FLOATS & 0xFF) + 1), DB_ERR_NFLOATS);
    {
        db_weights w2;
        db_status g = db_bind(&w2, blob, 20u);
        char line[96];
        sprintf(line, "buffer truncado        esperado=%d obtenido=%d",
                (int)DB_ERR_SIZE, (int)g);
        check(line, g == DB_ERR_SIZE);
        g = db_bind(&w2, 0, (uint32_t)nb);
        sprintf(line, "puntero nulo           esperado=%d obtenido=%d",
                (int)DB_ERR_NULL, (int)g);
        check(line, g == DB_ERR_NULL);
        /* alineacion: se copia el blob INTACTO a una direccion impar, para que
           el guard de magic no se dispare primero y la rama sea alcanzable.
           Este es el caso que el propio Tachi encontro mal en su v2. */
        {
            unsigned char *raw = (unsigned char *)malloc((size_t)nb + 4u);
            unsigned char *odd = raw + 1;
            memcpy(odd, blob, (size_t)nb);
            g = db_bind(&w2, odd, (uint32_t)nb);
            sprintf(line, "blob desalineado +1    esperado=%d obtenido=%d",
                    (int)DB_ERR_ALIGN, (int)g);
            check(line, g == DB_ERR_ALIGN);
            free(raw);
        }
    }

    printf("\n=== RESUMEN ===\n");
    printf("  fallas: %d\n", fails);
    printf("  %s\n", fails == 0 ? "TODO VERDE" : "HAY ROJOS");
    return fails == 0 ? 0 : 1;
}

#else  /* modo MCU: sin stdio, blob embebido, para linkear un .elf */

#include "blob_embedded.h"

/* El blob va en un array alineado a 4: db_bind lo exige y lo verifica. */
static db_weights g_w;
static db_state g_s;
static float g_act[DB_ACT];

/* Punto de entrada minimo. Devuelve 0 si todo verifica, y un codigo si no.
   No usa stdio ni malloc: es lo que se linkea para un MCU. */
int db_run_selfcheck(void)
{
    float err = 0.0f;
    db_status st;
    int t;

    st = db_bind(&g_w, db_blob, (uint32_t)sizeof(db_blob));
    if (st != DB_OK) { return 10 - (int)st; }

    st = db_selftest(&g_w, 1.0e-5f, &err);
    if (st != DB_OK) { return 20; }

    db_reset(&g_s);
    for (t = 0; t < 512; ++t) {
        db_step(&g_w, &g_s, db_seq + (long)t * DB_OBS, g_act);
    }
    return 0;
}

int main(void) { return db_run_selfcheck(); }

#endif
