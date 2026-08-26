/* probe_c99.c - prueba de compilacion nativa en el runner de Actions.
 *
 * Por que existe: brain-env NO tiene compilador de host (medido: FALTA gcc,
 * FALTA cc), asi que los tests nativos del C99 de DualBrain hoy no se pueden
 * correr en ningun lado. Este archivo es el minimo que demuestra que el runner
 * si puede, y ademas reproduce las dos operaciones que importan del expediente:
 *
 *   1. el gate escalar reflejo-vs-memoria de DualBrain,
 *   2. el overflow int32 que fue el bug real del paper 1.
 *
 * Compila con -Wall -Wextra -Werror a proposito: si el runner no tiene un
 * compilador serio, este archivo no pasa.
 */
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

/* Arbitro entre reflejo y memoria: la primitiva del gate de DualBrain. */
static int32_t gate(int32_t reflejo, int32_t memoria, int32_t umbral)
{
    return (memoria > umbral) ? memoria : reflejo;
}

int main(void)
{
    int32_t acc = 0;
    int i;

    for (i = 0; i < 1000; ++i) {
        acc = gate(i, acc + (i % 7), 500);
    }
    printf("gate_acc=%" PRId32 "\n", acc);

    printf("sizeof(int32_t)=%zu sizeof(long)=%zu sizeof(void*)=%zu\n",
           sizeof(int32_t), sizeof(long), sizeof(void *));

    /* El bug real del expediente: int32 se pasa, int64 aguanta. */
    {
        int32_t maximo = INT32_MAX;
        int64_t seguro = (int64_t)maximo + 1;
        printf("INT32_MAX=%" PRId32 "  INT32_MAX+1_en_int64=%" PRId64 "\n",
               maximo, seguro);
    }

    /* Conteo de aristas del conectoma: comprobacion de que no desborda. */
    {
        int64_t neuronas = 138639;
        int64_t densidad_num = 785197;      /* 0.000785197 * 1e9 */
        int64_t pares = neuronas * (neuronas - 1);
        int64_t aristas = (pares / 1000000000) * densidad_num;
        printf("pares_ordenados=%" PRId64 "  aristas_aprox=%" PRId64 "\n",
               pares, aristas);
        if (pares < 0) {
            printf("ERROR: desbordo el conteo de pares\n");
            return 1;
        }
    }

    printf("probe_c99 OK\n");
    return 0;
}
