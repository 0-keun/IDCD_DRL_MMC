/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: colon.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 05-Jan-2026 13:21:21
 */

/* Include Files */
#include "colon.h"
#include "rt_nonfinite.h"

/* Function Definitions */
/*
 * Arguments    : double y[35000001]
 * Return Type  : void
 */
void eml_float_colon(double y[5000001])
{
  int k;
  y[0] = 0.0;
  y[5000000] = 0.5;
  for (k = 0; k < 2499999; k++) {
    double kd;
    kd = ((double)k + 1.0) * 1.0E-7;
    y[k + 1] = kd;
    y[4999999 - k] = 0.5 - kd;
  }
  y[2500000] = 1.75;
}

/*
 * File trailer for colon.c
 *
 * [EOF]
 */
