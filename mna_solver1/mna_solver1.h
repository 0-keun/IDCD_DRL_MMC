/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: mna_solver1.h
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 05-Jan-2026 13:21:21
 */

#ifndef MNA_SOLVER1_H
#define MNA_SOLVER1_H

/* Include Files */
#include "mna_solver1_types.h"
#include "rtwtypes.h"
#include "mldivide.h"
#include "main.h"
#include <stddef.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

extern LU24Ctx g_ctx;
extern int g_ctx_ready;
/* Function Declarations */
extern void mna_solver1(struct0_T *out);
void mna_solver1_set_H(const double H[576]);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for mna_solver1.h
 *
 * [EOF]
 */
