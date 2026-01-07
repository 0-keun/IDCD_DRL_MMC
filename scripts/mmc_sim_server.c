#include <stdio.h>
#include <stdlib.h>

/* -----------------------------
 * 1) 입력: 한 줄 읽기
 *    성공 시 1, EOF/형식 불일치 시 0
 * ----------------------------- */
static int read_input(
    double *L_arm, double *C_arm,
    double *V_in,  double *I_in,
    double *V_out, double *I_out
) {
    int n = scanf("%lf %lf %lf %lf %lf %lf",
                  L_arm, C_arm, V_in, I_in, V_out, I_out);
    return (n == 6) ? 1 : 0;
}

/* -----------------------------
 * 2) 계산: (현재 더미 계산) -> 나중에 MMC 시뮬레이션으로 교체
 * ----------------------------- */
static void compute_metrics(
    double L_arm, double C_arm,
    double V_in,  double I_in,
    double V_out, double I_out,
    double *I_circ_rms, double *I_ripple, double *eta
) {
    (void)V_in;  (void)I_in;  (void)V_out; (void)I_out; // 지금은 미사용(경고 방지)

    const double L_min = 1e-3;
    const double C_min = 1e-3;
    const double L_max = 10e-3;
    const double C_max = 10e-3;

    *I_circ_rms = 1.0 / (L_arm / L_min + 1e-3);
    *I_ripple   = 1.0 / (C_arm / C_min + 1e-3);

    const double L_mid = (L_min + L_max) / 2.0;
    const double C_mid = (C_min + C_max) / 2.0;

    double L_norm = (L_arm - L_mid) / (L_max - L_min);
    double C_norm = (C_arm - C_mid) / (C_max - C_min);

    double eta_local = 0.9 - 0.05 * (L_norm * L_norm) - 0.05 * (C_norm * C_norm);

    if (eta_local < 0.0) eta_local = 0.0;
    if (eta_local > 1.0) eta_local = 1.0;

    *eta = eta_local;
}

/* -----------------------------
 * 3) 출력: 한 줄 출력 + flush
 * ----------------------------- */
static void write_output(double I_circ_rms, double I_ripple, double eta) {
    printf("%.10f %.10f %.10f\n", I_circ_rms, I_ripple, eta);
    fflush(stdout);
}

/* -----------------------------
 * main loop: read -> compute -> write
 * ----------------------------- */
int main(void) {
    double L_arm, C_arm, V_in, I_in, V_out, I_out;

    while (read_input(&L_arm, &C_arm, &V_in, &I_in, &V_out, &I_out)) {
        double I_circ_rms, I_ripple, eta;

        compute_metrics(L_arm, C_arm, V_in, I_in, V_out, I_out,
                        &I_circ_rms, &I_ripple, &eta);

        write_output(I_circ_rms, I_ripple, eta);
    }

    return 0;
}