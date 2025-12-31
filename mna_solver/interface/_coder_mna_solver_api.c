/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_mna_solver_api.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 31-Dec-2025 14:00:43
 */

/* Include Files */
#include "_coder_mna_solver_api.h"
#include "_coder_mna_solver_mex.h"

/* Variable Definitions */
emlrtCTX emlrtRootTLSGlobal = NULL;

emlrtContext emlrtContextGlobal = {
    true,                                                 /* bFirstTime */
    false,                                                /* bInitialized */
    131659U,                                              /* fVersionInfo */
    NULL,                                                 /* fErrorFunction */
    "mna_solver",                                         /* fFunctionName */
    NULL,                                                 /* fRTCallStack */
    false,                                                /* bDebugMode */
    {2045744189U, 2170104910U, 2743257031U, 4284093946U}, /* fSigWrd */
    NULL                                                  /* fSigMem */
};

/* Function Declarations */
static void emlrtExitTimeCleanupDtorFcn(const void *r);

static const mxArray *emlrt_marshallOut(real_T u[35000001]);

/* Function Definitions */
/*
 * Arguments    : const void *r
 * Return Type  : void
 */
static void emlrtExitTimeCleanupDtorFcn(const void *r)
{
  emlrtExitTimeCleanup(&emlrtContextGlobal);
}

/*
 * Arguments    : real_T u[35000001]
 * Return Type  : const mxArray *
 */
static const mxArray *emlrt_marshallOut(real_T u[35000001])
{
  static const int32_T iv[2] = {0, 0};
  static const int32_T iv1[2] = {1, 35000001};
  const mxArray *m;
  const mxArray *y;
  y = NULL;
  m = emlrtCreateNumericArray(2, (const void *)&iv[0], mxDOUBLE_CLASS, mxREAL);
  emlrtMxSetData((mxArray *)m, &u[0]);
  emlrtSetDimensions((mxArray *)m, &iv1[0], 2);
  emlrtAssign(&y, m);
  return y;
}

/*
 * Arguments    : int32_T nlhs
 *                const mxArray *plhs[2]
 * Return Type  : void
 */
void mna_solver_api(int32_T nlhs, const mxArray *plhs[2])
{
  real_T(*t)[35000001];
  real_T(*v7)[35000001];
  t = (real_T(*)[35000001])mxMalloc(sizeof(real_T[35000001]));
  v7 = (real_T(*)[35000001])mxMalloc(sizeof(real_T[35000001]));
  /* Invoke the target function */
  mna_solver(*t, *v7);
  /* Marshall function outputs */
  plhs[0] = emlrt_marshallOut(*t);
  if (nlhs > 1) {
    plhs[1] = emlrt_marshallOut(*v7);
  }
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void mna_solver_atexit(void)
{
  emlrtStack st = {
      NULL, /* site */
      NULL, /* tls */
      NULL  /* prev */
  };
  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtPushHeapReferenceStackR2021a(
      &st, false, NULL, (void *)&emlrtExitTimeCleanupDtorFcn, NULL, NULL, NULL);
  emlrtEnterRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
  mna_solver_xil_terminate();
  mna_solver_xil_shutdown();
  emlrtExitTimeCleanup(&emlrtContextGlobal);
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void mna_solver_initialize(void)
{
  emlrtStack st = {
      NULL, /* site */
      NULL, /* tls */
      NULL  /* prev */
  };
  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, NULL);
  emlrtEnterRtStackR2012b(&st);
  emlrtFirstTimeR2012b(emlrtRootTLSGlobal);
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void mna_solver_terminate(void)
{
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/*
 * File trailer for _coder_mna_solver_api.c
 *
 * [EOF]
 */
