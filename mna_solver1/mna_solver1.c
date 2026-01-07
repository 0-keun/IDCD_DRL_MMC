/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: mna_solver1.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 05-Jan-2026 13:21:21
 */

/* Include Files */
#include "mna_solver1.h"
#include "colon.h"
#include "mldivide.h"
#include "mna_solver1_types.h"
#include "mod.h"
#include "rt_nonfinite.h"
#include <emmintrin.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

/* Function Definitions */
/*
 * Arguments    : struct0_T *out
 * Return Type  : void
 */

// static void build_H_once(double H[576])
// {
//     // TODO: n==0에서만 H 구성/입력
//     // column-major: H[row + 24*col]
//     // 예시로 단위행렬
//     static const double b_A[576] = {1.0,0.0,0.25,0.0,0.25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-0.25,100000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-100000.0,-0.25,0.0,0.25,0.0,0.25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-0.25,100000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-100000.0,-0.25,9.9999999999999991E-6,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-9.9999999999999991E-6,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,9.9999999999999991E-6,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-9.9999999999999991E-6,0.0,0.25,0.0,0.25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-0.25,100000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-100000.0,-0.25,0.0,0.25,0.0,0.25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-0.25,100000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-100000.0,-0.25,1.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,-1.0,-1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,-1.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,-1.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,0.0,-1.0,-1.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,-1.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,-1.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0};
//     memcpy(H, b_A, 576 * sizeof(double));
//     // for (int i = 0; i < 576; i++) H[i] = 0.0;
//     // for (int d = 0; d < 24; d++) H[d + 24*d] = 1.0;
// }

void mna_solver1(struct0_T *out)
{
  const int N = 35000001;   // 길이 상수 (있으면 편함)
  
  // if (!g_ctx_ready) {
  //     fprintf(stderr, "mna_solver1: H not initialized. Call mna_solver1_set_H() first.\n");
  //     exit(1);
  // }

  double *i1;
  double *i10;
  double *i11;
  double *i2;
  double *i3;
  double *i4;
  double *i5;
  double *i7;
  double *i8;
  double *i9;
  double *js1;
  double *js2;
  double *js3;
  double *js4;
  double *js5;
  double *js6;
  double *js7;
  double *js8;
  double *v1;
  double *v10;
  double *v11;
  double *v12;
  double *v13;
  double *v2;
  double *v3;
  double *v4;
  double *v5;
  double *v6;
  double *v9;

  int n;

  i1  = (double *)malloc(N * sizeof(double));
  i10 = (double *)malloc(N * sizeof(double));
  i11 = (double *)malloc(N * sizeof(double));
  i2  = (double *)malloc(N * sizeof(double));
  i3  = (double *)malloc(N * sizeof(double));
  i4  = (double *)malloc(N * sizeof(double));
  i5  = (double *)malloc(N * sizeof(double));
  i7  = (double *)malloc(N * sizeof(double));
  i8  = (double *)malloc(N * sizeof(double));
  i9  = (double *)malloc(N * sizeof(double));
  js1 = (double *)malloc(N * sizeof(double));
  js2 = (double *)malloc(N * sizeof(double));
  js3 = (double *)malloc(N * sizeof(double));
  js4 = (double *)malloc(N * sizeof(double));
  js5 = (double *)malloc(N * sizeof(double));
  js6 = (double *)malloc(N * sizeof(double));
  js7 = (double *)malloc(N * sizeof(double));
  js8 = (double *)malloc(N * sizeof(double));
  v1  = (double *)malloc(N * sizeof(double));
  v10 = (double *)malloc(N * sizeof(double));
  v11 = (double *)malloc(N * sizeof(double));
  v12 = (double *)malloc(N * sizeof(double));
  v13 = (double *)malloc(N * sizeof(double));
  v2  = (double *)malloc(N * sizeof(double));
  v3  = (double *)malloc(N * sizeof(double));
  v4  = (double *)malloc(N * sizeof(double));
  v5  = (double *)malloc(N * sizeof(double));
  v6  = (double *)malloc(N * sizeof(double));
  v9  = (double *)malloc(N * sizeof(double));

  if (!i1 || !i10 || !i11 || !i2 || !i3 || !i4 || !i5 || !i7 || !i8 || !i9 ||
      !js1 || !js2 || !js3 || !js4 || !js5 || !js6 || !js7 || !js8 ||
      !v1 || !v10 || !v11 || !v12 || !v13 || !v2 || !v3 || !v4 || !v5 || !v6 || !v9) {
    fprintf(stderr, "mna_solver1: malloc failed (need huge memory)\n");
    exit(1);   // 메모리 없으면 그냥 종료
  }
  eml_float_colon(out->t);
  /* L_arm */
  /* C_sM */
  memset(&v1[0], 0, 35000001U * sizeof(double));
  memset(&v2[0], 0, 35000001U * sizeof(double));
  memset(&v3[0], 0, 35000001U * sizeof(double));
  memset(&v4[0], 0, 35000001U * sizeof(double));
  memset(&v5[0], 0, 35000001U * sizeof(double));
  memset(&v6[0], 0, 35000001U * sizeof(double));
  memset(&out->vout[0], 0, 35000001U * sizeof(double));
  memset(&v9[0], 0, 35000001U * sizeof(double));
  memset(&v10[0], 0, 35000001U * sizeof(double));
  memset(&v11[0], 0, 35000001U * sizeof(double));
  memset(&v12[0], 0, 35000001U * sizeof(double));
  memset(&v13[0], 0, 35000001U * sizeof(double));
  memset(&i1[0], 0, 35000001U * sizeof(double));
  memset(&i2[0], 0, 35000001U * sizeof(double));
  memset(&i3[0], 0, 35000001U * sizeof(double));
  memset(&i4[0], 0, 35000001U * sizeof(double));
  memset(&i5[0], 0, 35000001U * sizeof(double));
  memset(&i7[0], 0, 35000001U * sizeof(double));
  memset(&i8[0], 0, 35000001U * sizeof(double));
  memset(&i9[0], 0, 35000001U * sizeof(double));
  memset(&i10[0], 0, 35000001U * sizeof(double));
  memset(&i11[0], 0, 35000001U * sizeof(double));
  memset(&js1[0], 0, 35000001U * sizeof(double));
  memset(&js2[0], 0, 35000001U * sizeof(double));
  memset(&js3[0], 0, 35000001U * sizeof(double));
  memset(&js4[0], 0, 35000001U * sizeof(double));
  memset(&js5[0], 0, 35000001U * sizeof(double));
  memset(&js6[0], 0, 35000001U * sizeof(double));
  memset(&js7[0], 0, 35000001U * sizeof(double));
  memset(&js8[0], 0, 35000001U * sizeof(double));
  /*  System Matrix (24x24 constant) */
  for (n = 0; n < 35000000; n++) {
    double x[24];
    double saw;
    double saw_s;
    double sine;
    signed char b_i1;
    signed char b_i2;
    signed char b_i3;
    signed char b_i4;
    signed char b_i5;
    signed char b_i7;
    signed char i;
    signed char i6;
    saw_s = out->t[n];
    sine = sin(376.99111843077515 * saw_s);
    saw = b_mod(6283.1853071795858 * saw_s) / 6.2831853071795862;
    saw_s = b_mod(6283.1853071795858 * saw_s + 2.0943951023931953) /
            6.2831853071795862;
    i = (signed char)(sine >= saw);
    b_i1 = (signed char)(i == 0);
    b_i2 = (signed char)(-sine >= saw_s);
    b_i3 = (signed char)(b_i2 == 0);
    b_i4 = (signed char)(-sine >= saw);
    b_i5 = (signed char)(b_i4 == 0);
    i6 = (signed char)(sine >= saw_s);
    b_i7 = (signed char)(i6 == 0);
    if ((i == 1) && (b_i1 == 0)) {
      js1[n + 1] = i2[n];
      js2[n + 1] = 0.25 * (v1[n] - v3[n]);
    } else if ((i == 0) && (b_i1 == 1)) {
      js1[n + 1] = -0.25 * (v2[n] - v1[n]);
      js2[n + 1] = -i3[n];
    }
    if ((b_i2 == 1) && (b_i3 == 0)) {
      js3[n + 1] = i4[n];
      js4[n + 1] = 0.25 * (v3[n] - v5[n]);
    } else if ((b_i2 == 0) && (b_i3 == 1)) {
      js3[n + 1] = 0.25 * (v4[n] - v3[n]);
      js4[n + 1] = -i5[n];
    }
    if ((b_i4 == 1) && (b_i5 == 0)) {
      js5[n + 1] = i8[n];
      js6[n + 1] = 0.25 * (v9[n] - v11[n]);
    } else if ((b_i4 == 0) && (b_i5 == 1)) {
      js5[n + 1] = -0.25 * (v10[n] - v9[n]);
      js6[n + 1] = -i9[n];
    }
    if ((i6 == 1) && (b_i7 == 0)) {
      js7[n + 1] = i10[n];
      js8[n + 1] = 0.25 * (v11[n] - v13[n]);
    } else if ((i6 == 0) && (b_i7 == 1)) {
      js7[n + 1] = 0.25 * (v12[n] - v11[n]);
      js8[n + 1] = -i11[n];
    }
    x[0] = 2000.0;
    x[1] = 0.0;
    x[2] = -js1[n + 1];
    x[3] = 100000.0 * (v2[n] - v3[n]);
    x[4] = js2[n + 1];
    x[5] = 0.0;
    x[6] = -js3[n + 1];
    x[7] = 100000.0 * (v4[n] - v5[n]);
    x[8] = js4[n + 1];
    x[9] = -i1[n];
    x[10] = 0.0;
    x[11] = 0.0;
    x[12] = 0.0;
    x[13] = 0.0;
    x[14] = -i7[n];
    x[15] = 0.0;
    x[16] = -js5[n + 1];
    x[17] = 100000.0 * (v10[n] - v11[n]);
    x[18] = js6[n + 1];
    x[19] = 0.0;
    x[20] = -js7[n + 1];
    x[21] = 100000.0 * (v12[n] - v13[n]);
    x[22] = js8[n + 1];
    x[23] = -2000.0;
    lu24_solve_inplace(&g_ctx, x);
    v1[n + 1] = x[0];
    v2[n + 1] = x[1];
    v3[n + 1] = x[2];
    v4[n + 1] = x[3];
    v5[n + 1] = x[4];
    v6[n + 1] = x[5];
    out->vout[n + 1] = x[6];
    v9[n + 1] = x[8];
    v10[n + 1] = x[9];
    v11[n + 1] = x[10];
    v12[n + 1] = x[11];
    v13[n + 1] = x[12];
    i1[n + 1] = x[13];
    i2[n + 1] = x[14];
    i3[n + 1] = x[15];
    i4[n + 1] = x[16];
    i5[n + 1] = x[17];
    i7[n + 1] = x[19];
    i8[n + 1] = x[20];
    i9[n + 1] = x[21];
    i10[n + 1] = x[22];
    i11[n + 1] = x[23];
  }
  for (n = 0; n <= 34999998; n += 2) {
    __m128d r;
    __m128d r1;
    r = _mm_loadu_pd(&i1[n]);
    r1 = _mm_loadu_pd(&i7[n]);
    _mm_storeu_pd(&out->icc[n],
                  _mm_div_pd(_mm_add_pd(r, r1), _mm_set1_pd(2.0)));
    r = _mm_loadu_pd(&v5[n]);
    r1 = _mm_loadu_pd(&v6[n]);
    _mm_storeu_pd(&out->deltai[n],
                  _mm_div_pd(_mm_sub_pd(r, r1), _mm_set1_pd(0.01)));
  }
  out->icc[35000000] = (i1[35000000] + i7[35000000]) / 2.0;
  out->deltai[35000000] = (v5[35000000] - v6[35000000]) / 0.01;

  int last = N - 1;  // 35000000
  printf("=== mna_solver1 last sample ===\n");
  printf("t[last]      = %.15e\n", out->t[last]);
  printf("vout[last]   = %.15e\n", out->vout[last]);
  printf("icc[last]    = %.15e\n", out->icc[last]);
  printf("deltai[last] = %.15e\n", out->deltai[last]);

  // 원하면 내부 변수들도 같이 확인
  printf("v1[last]=%.15e v2[last]=%.15e v3[last]=%.15e v4[last]=%.15e v5[last]=%.15e v6[last]=%.15e\n",
          v1[last], v2[last], v3[last], v4[last], v5[last], v6[last]);
  printf("i1[last]=%.15e i2[last]=%.15e i3[last]=%.15e i4[last]=%.15e i5[last]=%.15e i7[last]=%.15e i8[last]=%.15e i9[last]=%.15e i10[last]=%.15e i11[last]=%.15e\n",
          i1[last], i2[last], i3[last], i4[last], i5[last], i7[last], i8[last], i9[last], i10[last], i11[last]);
}
/*
 * File trailer for mna_solver1.c
 *
 * [EOF]
 */
