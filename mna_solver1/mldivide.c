#include "mldivide.h"
#include <string.h>
#include <math.h>

void lu24_factor(const double H[576], LU24Ctx *ctx)
{
    double *A = ctx->LU;
    int i, j, k, jA, jp1j, A_tmp, a;
    double smax;

    memcpy(A, H, 576U * sizeof(double));
    for (i = 0; i < 24; i++) ctx->ipiv[i] = (signed char)(i + 1);

    for (j = 0; j < 23; j++) {
        int b_tmp = j * 25;
        int mmj_tmp = 22 - j;
        int jAspan = 25 - j;

        a = 0;
        smax = fabs(A[b_tmp]);
        for (k = 2; k < jAspan; k++) {
            double s = fabs(A[(b_tmp + k) - 1]);
            if (s > smax) { a = k - 1; smax = s; }
        }

        if (A[b_tmp + a] != 0.0) {
            if (a != 0) {
                int piv = j + a;
                ctx->ipiv[j] = (signed char)(piv + 1);
                for (k = 0; k < 24; k++) {
                    int r1 = j   + k * 24;
                    int r2 = piv + k * 24;
                    double tmp = A[r1];
                    A[r1] = A[r2];
                    A[r2] = tmp;
                }
            }
            int i_end = (b_tmp - j) + 24;
            jp1j = b_tmp + 2;
            for (a = jp1j; a <= i_end; a++) A[a - 1] /= A[b_tmp];
        }

        jA = b_tmp;
        for (A_tmp = 0; A_tmp <= mmj_tmp; A_tmp++) {
            smax = A[(b_tmp + A_tmp * 24) + 24];
            if (smax != 0.0) {
                int i_start = jA + 26;
                int i_end2  = (jA - j) + 48;
                for (jp1j = i_start; jp1j <= i_end2; jp1j++) {
                    A[jp1j - 1] += A[((b_tmp + jp1j) - jA) - 25] * -smax;
                }
            }
            jA += 24;
        }
    }

    ctx->ready = 1;
}

void lu24_solve_inplace(const LU24Ctx *ctx, double B[24])
{
    const double *A = ctx->LU;
    double smax;
    int k, a, jA;

    // pivot 적용
    for (int j = 0; j < 23; j++) {
        signed char piv = ctx->ipiv[j];
        if (piv != j + 1) {
            smax = B[j];
            B[j] = B[piv - 1];
            B[piv - 1] = smax;
        }
    }

    // forward (L)
    for (k = 0; k < 24; k++) {
        jA = 24 * k;
        if (B[k] != 0.0) {
            for (a = k + 2; a < 25; a++) {
                B[a - 1] -= B[k] * A[(a + jA) - 1];
            }
        }
    }

    // backward (U)
    for (k = 23; k >= 0; k--) {
        jA = 24 * k;
        smax = B[k];
        if (smax != 0.0) {
            smax /= A[k + jA];
            B[k] = smax;
            for (a = 0; a < k; a++) {
                B[a] -= B[k] * A[a + jA];
            }
        }
    }
}
