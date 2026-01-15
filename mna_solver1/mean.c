/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: mean.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 11-Jan-2026 19:16:15
 */

/* Include Files */
#include "mean.h"
#include "rt_nonfinite.h"
#include "main.h"

/* Function Definitions */
/*
 * Arguments    : const double x[10000001]
 * Return Type  : double
 */
double mean(const double x[SimSteps])
{
  double accumulatedData;
  double y;
  int ib;
  int k;
  accumulatedData = x[0];
  for (k = 0; k < 1023; k++) {
    accumulatedData += x[k + 1];
  }
  for (ib = 0; ib < 9765; ib++) {
    int hi;
    int xblockoffset;
    xblockoffset = (ib + 1) << 10;
    y = x[xblockoffset];
    if (ib + 2 == 9766) {
      hi = 641;
    } else {
      hi = 1024;
    }
    for (k = 2; k <= hi; k++) {
      y += x[(xblockoffset + k) - 1];
    }
    accumulatedData += y;
  }
  return accumulatedData / 5.0000001E+6;
}

double meanN(double *x, int N)
{
    double s = 0.0;
    for (int i = 0; i < N; i++) s += x[i];
    return s / (double)N;
}

double mean_a(double *x, int N)
{
    double s = 0.0;
    for (int i = 0; i < N; i++) s += x[i];
    return s / (double)N;
}

/*
 * File trailer for mean.c
 *
 * [EOF]
 */
