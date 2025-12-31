/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: mna_solver.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 31-Dec-2025 14:00:43
 */

/* Include Files */
#include "mna_solver.h"
#include "colon.h"
#include "mldivide.h"
#include "mod.h"
#include "rt_nonfinite.h"
#include <math.h>
#include <string.h>

#include <stdio.h>

/* Function Definitions */
/*
 * MNA-based converter model (Coder compatible)
 *
 * Arguments    : double t[35000001]
 *                double v7[35000001]
 * Return Type  : void
 */
void mna_solver(double t[35000001], double v7[35000001])
{
  static double i1[35000001];
  static double v1[35000001];
  static double v2[35000001];
  static double v3[35000001];
  static double v4[35000001];
  static double v5[35000001];
  int n;
  /*  Time settings */
  eml_float_colon(t);
  /*  Parameters */
  /*  Preallocation (VERY IMPORTANT for Coder) */
  memset(&v1[0], 0, 35000001U * sizeof(double));
  memset(&v2[0], 0, 35000001U * sizeof(double));
  memset(&v3[0], 0, 35000001U * sizeof(double));
  memset(&v4[0], 0, 35000001U * sizeof(double));
  memset(&v5[0], 0, 35000001U * sizeof(double));
  memset(&v7[0], 0, 35000001U * sizeof(double));
  memset(&i1[0], 0, 35000001U * sizeof(double));
  /*  System Matrix (24x24 constant) */
  /*  Main Time Loop */
  for (n = 0; n < 35000000; n++) {
    double x[24];
    double d;
    double d1;
    /*  sawtooth replacement (Coder compatible) */
    d = t[n];
    if (sin(376.99111843077515 * d) >=
        b_mod(6283.1853071795858 * d) / 6.2831853071795862) {
      d = 0.0;
      d1 = 0.25 * (v1[n] - v3[n]);
    } else {
      d = -0.25 * (v2[n] - v1[n]);
      d1 = -0.0;
    }
    x[0] = 2000.0;
    x[1] = 0.0;
    x[2] = -d;
    x[3] = 100000.0 * (v2[n] - v3[n]);
    x[4] = d1;
    x[5] = 0.0;
    x[6] = -0.0;
    x[7] = 100000.0 * (v4[n] - v5[n]);
    x[8] = 0.0;
    x[9] = -i1[n];
    x[10] = 0.0;
    x[11] = 0.0;
    x[12] = 0.0;
    x[13] = 0.0;
    x[14] = -0.0;
    x[15] = 0.0;
    x[16] = -0.0;
    x[17] = 0.0;
    x[18] = 0.0;
    x[19] = 0.0;
    x[20] = -0.0;
    x[21] = 0.0;
    x[22] = 0.0;
    x[23] = -2000.0;
    mldivide(x);
    v1[n + 1] = x[0];
    v2[n + 1] = x[1];
    v3[n + 1] = x[2];
    v4[n + 1] = x[3];
    v5[n + 1] = x[4];
    v7[n + 1] = x[6];
    i1[n + 1] = x[13];
    if ((n % 1000000) == 0) {
      float timing = 100 * n / 35000000;
      printf("iteration %f [percent] \n", timing);
      fflush(stdout);
    }
  }
}

/*
 * File trailer for mna_solver.c
 *
 * [EOF]
 */
