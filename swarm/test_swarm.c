#include "swarm_drone.h"
#include <stdio.h>
int main(void) {
    swarm_drone_t b;
    int16_t sens[12] = {0};
    swarm_init(&b);
    // estimulo: amenaza frontal + vecino a la izquierda
    sens[0] = 15000;  // lam_flow_f (obstaculo frontal)
    sens[6] = 9000;   // ant_prox_l (vecino izq)
    for (int t = 0; t < 50; t++) swarm_step(&b, sens);
    int16_t fl, fr, bl, br;
    swarm_get_motors(&b, &fl, &fr, &bl, &br);
    printf("motores (FL FR BL BR): %d %d %d %d\n", fl, fr, bl, br);
    printf("esperado: pitch atras (BL/BR > FL/FR) + roll derecha (FR/BR > FL/BL)\n");
    return 0;
}
