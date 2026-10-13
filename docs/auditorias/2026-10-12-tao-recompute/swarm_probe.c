/* Sonda UBSan de los helpers de hardware de swarm/swarm_drone.h (blob f18b876).
 * Cuerpos transcritos literalmente. Uso: ./swarm_probe {control|adc|pwm} */
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static inline int16_t adc_to_q15(uint16_t adc, uint16_t adc_max) {
    int32_t v = ((int32_t)adc * 65536) / (int32_t)(adc_max + 1) - 32768;
    return (int16_t)(v < -32768 ? -32768 : (v > 32767 ? 32767 : v));
}

static inline uint16_t q15_to_pwm(int16_t q, uint16_t pwm_min, uint16_t pwm_max) {
    int32_t v = ((int32_t)(q + 32768) * (pwm_max - pwm_min)) / 65536 + pwm_min;
    if (v < pwm_min) v = pwm_min;
    if (v > pwm_max) v = pwm_max;
    return (uint16_t)v;
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "uso: %s control|adc|pwm\n", argv[0]); return 2; }
    if (strcmp(argv[1], "control") == 0) {
        printf("adc12=%d pwm12=%u\n", adc_to_q15(4095, 4095), q15_to_pwm(32767, 0, 4095));
        return 0;
    }
    if (strcmp(argv[1], "adc") == 0) { printf("%d\n", adc_to_q15(65535, 65535)); return 0; }
    if (strcmp(argv[1], "pwm") == 0) { printf("%u\n", q15_to_pwm(32767, 0, 65535)); return 0; }
    fprintf(stderr, "modo desconocido\n");
    return 2;
}
