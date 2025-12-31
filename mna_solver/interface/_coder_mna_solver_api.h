/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_mna_solver_api.h
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 31-Dec-2025 14:00:43
 */

#ifndef _CODER_MNA_SOLVER_API_H
#define _CODER_MNA_SOLVER_API_H

/* Include Files */
#include "emlrt.h"
#include "mex.h"
#include "tmwtypes.h"
#include <string.h>

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

#ifdef __cplusplus
extern "C" {
#endif

/* Function Declarations */
void mna_solver(real_T t[35000001], real_T v7[35000001]);

void mna_solver_api(int32_T nlhs, const mxArray *plhs[2]);

void mna_solver_atexit(void);

void mna_solver_initialize(void);

void mna_solver_terminate(void);

void mna_solver_xil_shutdown(void);

void mna_solver_xil_terminate(void);

#ifdef __cplusplus
}
#endif

#endif
/*
 * File trailer for _coder_mna_solver_api.h
 *
 * [EOF]
 */
