/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: mean.h
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 11-Jan-2026 19:16:15
 */

#ifndef MEAN_H
#define MEAN_H

/* Include Files */
#include "rtwtypes.h"
#include <stddef.h>
#include <stdlib.h>
#include "main.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
double mean(const double x[SimSteps]);
double meanN(double x[SimSteps], int N);
double mean_a(double x[500000], int N);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for mean.h
 *
 * [EOF]
 */
