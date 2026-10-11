/*
 * dbc3-v3/c/dbc3_motor.h — Reconstructed C99 DBC3 motor contract.
 *
 * This is a clean-room reconstruction of the published Python DBC3Motor
 * _step() equations in benchmark/dbc3_benchmark.py. It is not the recovered
 * original backend and it does not contain trained weights.
 */
#ifndef DBC3_MOTOR_H
#define DBC3_MOTOR_H

#include <float.h>
#include <math.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

#define DBC3_DIN 36
#define DBC3_DOUT 12
#define DBC3_HM 20
#define DBC3_HR 36
#define DBC3_TAU_INPUT (DBC3_HM * 2)
#define DBC3_GATE_INPUT (DBC3_HR + DBC3_HM)
#define DBC3_HEAD_INPUT (DBC3_HR + DBC3_HM)
#define DBC3_PARAM_COUNT 6888
#define DBC3_LAYER_NORM_EPSILON 1.0e-5f

typedef enum {
    DBC3_OK = 0,
    DBC3_ERR_NULL = -1,
    DBC3_ERR_NONFINITE_INPUT = -2,
    DBC3_ERR_NONFINITE_WEIGHTS = -3,
    DBC3_ERR_NONFINITE_STATE = -4,
    DBC3_ERR_NONFINITE_OUTPUT = -5
} DBC3_Status;

typedef struct {
    float W_r1[DBC3_HR * DBC3_DIN];
    float b_r1[DBC3_HR];
    float W_r2[DBC3_HR * DBC3_HR];
    float b_r2[DBC3_HR];
    float W_enc[DBC3_HM * DBC3_DIN];
    float b_enc[DBC3_HM];
    float W_in[DBC3_HM * DBC3_HM];
    float W_res[DBC3_HM * DBC3_HM];
    float W_tau[DBC3_HM * DBC3_TAU_INPUT];
    float b_tau[DBC3_HM];
    float ln_gamma[DBC3_HM];
    float ln_beta[DBC3_HM];
    float W_gate[DBC3_HM * DBC3_GATE_INPUT];
    float b_gate[DBC3_HM];
    float W_head[DBC3_DOUT * DBC3_HEAD_INPUT];
    float b_head[DBC3_DOUT];
} DBC3_Weights;

typedef struct {
    float hm[DBC3_HM];
    uint64_t step_count;
} DBC3_State;

typedef struct {
    float logits[DBC3_DOUT];
    int argmax_token;
    float argmax_prob;
    float coherence;
    float coherence_ema;
    float entropy;
} DBC3_Result;

static inline int dbc3_param_count(void) {
    return DBC3_PARAM_COUNT;
}

static inline void dbc3_state_reset(DBC3_State *state) {
    if (state != NULL) {
        memset(state, 0, sizeof(*state));
    }
}

static inline int dbc3_all_finite(const float *values, size_t count) {
    if (values == NULL) {
        return 0;
    }
    for (size_t i = 0; i < count; ++i) {
        if (!isfinite(values[i])) {
            return 0;
        }
    }
    return 1;
}

static inline float dbc3_sigmoid(float x) {
    if (x >= 0.0f) {
        const float z = expf(-x);
        return 1.0f / (1.0f + z);
    }
    const float z = expf(x);
    return z / (1.0f + z);
}

static inline float dbc3_gelu_c(float x) {
    return x * dbc3_sigmoid(1.702f * x);
}

static inline float dbc3_dot_row(const float *row, const float *vector, int width) {
    float sum = 0.0f;
    for (int i = 0; i < width; ++i) {
        sum += row[i] * vector[i];
    }
    return sum;
}

static inline void dbc3_affine_tanh(const float *weights, const float *bias,
                                    const float *input, float *output,
                                    int rows, int cols) {
    for (int row = 0; row < rows; ++row) {
        output[row] = tanhf(dbc3_dot_row(&weights[row * cols], input, cols) + bias[row]);
    }
}

static inline void dbc3_affine(const float *weights, const float *bias,
                               const float *input, float *output,
                               int rows, int cols) {
    for (int row = 0; row < rows; ++row) {
        output[row] = dbc3_dot_row(&weights[row * cols], input, cols) + bias[row];
    }
}

static inline DBC3_Status dbc3_validate_weights(const DBC3_Weights *weights) {
    if (weights == NULL) {
        return DBC3_ERR_NULL;
    }
    if (!dbc3_all_finite((const float *)weights,
                         sizeof(*weights) / sizeof(float))) {
        return DBC3_ERR_NONFINITE_WEIGHTS;
    }
    return DBC3_OK;
}

static inline void dbc3_zero_result(DBC3_Result *result) {
    if (result != NULL) {
        memset(result, 0, sizeof(*result));
        result->argmax_token = -1;
    }
}

static inline DBC3_Status dbc3_step(const DBC3_Weights *weights,
                                    DBC3_State *state,
                                    const float input[DBC3_DIN],
                                    DBC3_Result *result) {
    if (weights == NULL || state == NULL || input == NULL || result == NULL) {
        dbc3_zero_result(result);
        return DBC3_ERR_NULL;
    }
    dbc3_zero_result(result);
    if (dbc3_validate_weights(weights) != DBC3_OK) {
        dbc3_state_reset(state);
        return DBC3_ERR_NONFINITE_WEIGHTS;
    }
    if (!dbc3_all_finite(input, DBC3_DIN)) {
        dbc3_state_reset(state);
        return DBC3_ERR_NONFINITE_INPUT;
    }
    if (!dbc3_all_finite(state->hm, DBC3_HM)) {
        dbc3_state_reset(state);
        return DBC3_ERR_NONFINITE_STATE;
    }

    float t[DBC3_HR];
    float r[DBC3_HR];
    float e[DBC3_HM];
    float tau_input[DBC3_TAU_INPUT];
    float tau[DBC3_HM];
    float f[DBC3_HM];
    float normalized[DBC3_HM];
    float gate_input[DBC3_GATE_INPUT];
    float gate[DBC3_HM];
    float head_input[DBC3_HEAD_INPUT];

    dbc3_affine_tanh(weights->W_r1, weights->b_r1, input, t, DBC3_HR, DBC3_DIN);
    dbc3_affine_tanh(weights->W_r2, weights->b_r2, t, r, DBC3_HR, DBC3_HR);
    dbc3_affine(weights->W_enc, weights->b_enc, input, e, DBC3_HM, DBC3_DIN);
    for (int i = 0; i < DBC3_HM; ++i) {
        e[i] = dbc3_gelu_c(e[i]);
        tau_input[i] = e[i];
        tau_input[DBC3_HM + i] = state->hm[i];
    }
    dbc3_affine(weights->W_tau, weights->b_tau, tau_input, tau, DBC3_HM, DBC3_TAU_INPUT);
    for (int i = 0; i < DBC3_HM; ++i) {
        tau[i] = dbc3_sigmoid(tau[i]);
    }
    for (int row = 0; row < DBC3_HM; ++row) {
        f[row] = tanhf(dbc3_dot_row(&weights->W_in[row * DBC3_HM], e, DBC3_HM)
                       + dbc3_dot_row(&weights->W_res[row * DBC3_HM], state->hm, DBC3_HM));
    }
    for (int i = 0; i < DBC3_HM; ++i) {
        state->hm[i] = (1.0f - tau[i]) * state->hm[i] + tau[i] * f[i];
    }

    float mean = 0.0f;
    for (int i = 0; i < DBC3_HM; ++i) {
        mean += state->hm[i];
    }
    mean /= (float)DBC3_HM;
    float variance = 0.0f;
    for (int i = 0; i < DBC3_HM; ++i) {
        const float delta = state->hm[i] - mean;
        variance += delta * delta;
    }
    variance /= (float)DBC3_HM;
    const float inverse_std = 1.0f / sqrtf(variance + DBC3_LAYER_NORM_EPSILON);
    for (int i = 0; i < DBC3_HM; ++i) {
        state->hm[i] = weights->ln_gamma[i] * (state->hm[i] - mean) * inverse_std
                     + weights->ln_beta[i];
        normalized[i] = state->hm[i];
    }

    for (int i = 0; i < DBC3_HR; ++i) {
        gate_input[i] = r[i];
        head_input[i] = r[i];
    }
    for (int i = 0; i < DBC3_HM; ++i) {
        gate_input[DBC3_HR + i] = normalized[i];
    }
    dbc3_affine(weights->W_gate, weights->b_gate, gate_input, gate, DBC3_HM, DBC3_GATE_INPUT);
    for (int i = 0; i < DBC3_HM; ++i) {
        gate[i] = dbc3_sigmoid(gate[i]);
        head_input[DBC3_HR + i] = gate[i] * normalized[i];
    }
    dbc3_affine(weights->W_head, weights->b_head, head_input, result->logits,
                DBC3_DOUT, DBC3_HEAD_INPUT);

    if (!dbc3_all_finite(state->hm, DBC3_HM)
        || !dbc3_all_finite(result->logits, DBC3_DOUT)) {
        dbc3_state_reset(state);
        dbc3_zero_result(result);
        return DBC3_ERR_NONFINITE_OUTPUT;
    }
    state->step_count += 1;
    return DBC3_OK;
}

#endif
