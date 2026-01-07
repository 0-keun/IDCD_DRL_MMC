#ifndef MLDIVIDE_H
#define MLDIVIDE_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    double LU[576];      // 24x24 (column-major)
    signed char ipiv[24];
    int ready;           // 0:not factored, 1:factored
} LU24Ctx;

// H를 LU로 한 번만 분해
void lu24_factor(const double H[576], LU24Ctx *ctx);

// 이미 분해된 LU로, B를 in-place로 푼다 (B := H^{-1}B)
void lu24_solve_inplace(const LU24Ctx *ctx, double B[24]);

#ifdef __cplusplus
}
#endif

#endif