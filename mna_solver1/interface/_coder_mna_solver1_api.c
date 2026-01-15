/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_mna_solver1_api.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 11-Jan-2026 19:16:15
 */

/* Include Files */
#include "_coder_mna_solver1_api.h"
#include "_coder_mna_solver1_mex.h"

/* Variable Definitions */
emlrtCTX emlrtRootTLSGlobal = NULL;

emlrtContext emlrtContextGlobal = {
    true,                                                 /* bFirstTime */
    false,                                                /* bInitialized */
    131659U,                                              /* fVersionInfo */
    NULL,                                                 /* fErrorFunction */
    "mna_solver1",                                        /* fFunctionName */
    NULL,                                                 /* fRTCallStack */
    false,                                                /* bDebugMode */
    {2045744189U, 2170104910U, 2743257031U, 4284093946U}, /* fSigWrd */
    NULL                                                  /* fSigMem */
};

/* Function Declarations */
static const mxArray *b_emlrt_marshallOut(const real_T u[10000001]);

static void emlrtExitTimeCleanupDtorFcn(const void *r);

static const mxArray *emlrt_marshallOut(const struct0_T *u);

/* Function Definitions */
/*
 * Arguments    : const real_T u[10000001]
 * Return Type  : const mxArray *
 */
static const mxArray *b_emlrt_marshallOut(const real_T u[10000001])
{
  static const int32_T iv[2] = {1, 10000001};
  const mxArray *m;
  const mxArray *y;
  real_T *pData;
  int32_T i;
  y = NULL;
  m = emlrtCreateNumericArray(2, (const void *)&iv[0], mxDOUBLE_CLASS, mxREAL);
  pData = emlrtMxGetPr(m);
  for (i = 0; i < 10000001; i++) {
    pData[i] = u[i];
  }
  emlrtAssign(&y, m);
  return y;
}

/*
 * Arguments    : const void *r
 * Return Type  : void
 */
static void emlrtExitTimeCleanupDtorFcn(const void *r)
{
  emlrtExitTimeCleanup(&emlrtContextGlobal);
}

/*
 * Arguments    : const struct0_T *u
 * Return Type  : const mxArray *
 */
static const mxArray *emlrt_marshallOut(const struct0_T *u)
{
  static const char_T *sv[5] = {"t", "icc_ac_rms", "vout", "deltai", "deltavc"};
  const mxArray *b_y;
  const mxArray *m;
  const mxArray *y;
  y = NULL;
  emlrtAssign(&y, emlrtCreateStructMatrix(1, 1, 5, (const char_T **)&sv[0]));
  emlrtSetFieldR2017b(y, 0, "t", b_emlrt_marshallOut(u->t), 0);
  b_y = NULL;
  m = emlrtCreateDoubleScalar(u->icc_ac_rms);
  emlrtAssign(&b_y, m);
  emlrtSetFieldR2017b(y, 0, "icc_ac_rms", b_y, 1);
  emlrtSetFieldR2017b(y, 0, "vout", b_emlrt_marshallOut(u->vout), 2);
  emlrtSetFieldR2017b(y, 0, "deltai", b_emlrt_marshallOut(u->deltai), 3);
  emlrtSetFieldR2017b(y, 0, "deltavc", b_emlrt_marshallOut(u->deltavc), 4);
  return y;
}

/*
 * Arguments    : const mxArray **plhs
 * Return Type  : void
 */
void mna_solver1_api(const mxArray **plhs)
{
  static struct0_T out;
  /* Invoke the target function */
  mna_solver1(&out);
  /* Marshall function outputs */
  *plhs = emlrt_marshallOut(&out);
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void mna_solver1_atexit(void)
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
  mna_solver1_xil_terminate();
  mna_solver1_xil_shutdown();
  emlrtExitTimeCleanup(&emlrtContextGlobal);
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void mna_solver1_initialize(void)
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
void mna_solver1_terminate(void)
{
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/*
 * File trailer for _coder_mna_solver1_api.c
 *
 * [EOF]
 */
