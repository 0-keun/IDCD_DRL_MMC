/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_mna_solver1_api.h
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 05-Jan-2026 13:21:21
 */

#ifndef _CODER_MNA_SOLVER1_API_H
#define _CODER_MNA_SOLVER1_API_H

/* Include Files */
#include "emlrt.h"
#include "mex.h"
#include "tmwtypes.h"
#include <string.h>

/* Type Definitions */
#ifndef typedef_struct0_T
#define typedef_struct0_T
typedef struct {
  real_T t[35000001];
  real_T vout[35000001];
  real_T icc[35000001];
  real_T deltai[35000001];
} struct0_T;
#endif /* typedef_struct0_T */

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
void mna_solver1(struct0_T *out);

void mna_solver1_api(const mxArray **plhs);

void mna_solver1_atexit(void);

void mna_solver1_initialize(void);

void mna_solver1_terminate(void);

void mna_solver1_xil_shutdown(void);

void mna_solver1_xil_terminate(void);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for _coder_mna_solver1_api.h
 *
 * [EOF]
 */
