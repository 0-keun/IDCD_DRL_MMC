#include <stdio.h>
#include <stdlib.h>

int main() {
    // 입력 파라미터
    double L_arm, C_arm, V_in, I_in, V_out, I_out;

    // 한 줄 단위로 계속 처리 (EOF 오면 종료)
    while (1) {
        int n = scanf("%lf %lf %lf %lf %lf %lf", &L_arm, &C_arm, &V_in, &I_in, &V_out, &I_out);
        if (n != 6) break;

        // -----------------------------
        // TODO: 여기서 "실제 MMC 시뮬레이션" 수행
        // 현재는 Python 더미 모델과 비슷한 형태의 더미 계산만 넣어둠
        // -----------------------------
        // (주의) Python 쪽 범위를 그대로 쓰려면 L_min/C_min을 C에도 맞춰야 함
        // 여기서는 예시로 임의 상수 사용
        const double L_min = 1e-3;
        const double C_min = 1e-3;
        const double L_max = 10e-3;
        const double C_max = 10e-3;

        double I_circ_rms = 1.0 / (L_arm / L_min + 1e-3);
        double I_ripple   = 1.0 / (C_arm / C_min + 1e-3);

        double L_mid = (L_min + L_max) / 2.0;
        double C_mid = (C_min + C_max) / 2.0;

        double eta = 0.9
            - 0.05 * ((L_arm - L_mid) / (L_max - L_min)) * ((L_arm - L_mid) / (L_max - L_min))
            - 0.05 * ((C_arm - C_mid) / (C_max - C_min)) * ((C_arm - C_mid) / (C_max - C_min));

        if (eta < 0.0) eta = 0.0;
        if (eta > 1.0) eta = 1.0;

        // 결과를 한 줄로 출력하고 flush (★필수)
        printf("%.10f %.10f %.10f\n", I_circ_rms, I_ripple, eta);
        fflush(stdout);
    }

    return 0;
}