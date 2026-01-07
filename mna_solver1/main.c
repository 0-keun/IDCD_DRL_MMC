/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: main.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 05-Jan-2026 13:21:21
 */

/*************************************************************************/
/* This automatically generated example C main file shows how to call    */
/* entry-point functions that MATLAB Coder generated. You must customize */
/* this file for your application. Do not modify this file directly.     */
/* Instead, make a copy of this file, modify it, and integrate it into   */
/* your development environment.                                         */
/*                                                                       */
/* This file initializes entry-point function arguments to a default     */
/* size and value before calling the entry-point functions. It does      */
/* not store or use any values returned from the entry-point functions.  */
/* If necessary, it does pre-allocate memory for returned values.        */
/* You can use this file as a starting point for a main function that    */
/* you can deploy in your application.                                   */
/*                                                                       */
/* After you copy the file, and before you deploy it, you must make the  */
/* following changes:                                                    */
/* * For variable-size function arguments, change the example sizes to   */
/* the sizes that your application requires.                             */
/* * Change the example values of function arguments to the values that  */
/* your application requires.                                            */
/* * If the entry-point functions return values, store these values or   */
/* otherwise use them as required by your application.                   */
/*                                                                       */
/*************************************************************************/

/* Include Files */
#include <stdio.h>
#include <string.h>
#include "main.h"
#include "mna_solver1.h"
#include "mna_solver1_terminate.h"
#include "mna_solver1_types.h"
#include "rt_nonfinite.h"
#include "mldivide.h"
#include "mna_solver1_alloc.h"

LU24Ctx g_ctx;
int g_ctx_ready = 0;

void mna_solver1_set_H(const double H[576])
{
    memset(&g_ctx, 0, sizeof(g_ctx));
    lu24_factor(H, &g_ctx);
    g_ctx_ready = 1;
}

static int read_H(double H[576]) {
    for (int i = 0; i < 576; i++) {
        if (scanf("%lf", &H[i]) != 1) return 0;
    }
    return 1;
}

/* Function Definitions */
/*
 * Arguments    : int argc
 *                char **argv
 * Return Type  : int
 */
int main(int argc, char **argv)
{
  const int N = 35000001;
  double H[576];
    if (!read_H(H)) {
        fprintf(stderr, "Failed to read H (576 doubles)\n");
        return 1;
    }
  (void)argc;
  (void)argv;

  mna_solver1_set_H(H);

  struct0_T out = {0};

  if (!mna_solver1_alloc(&out, N)) {
      return 1;
  }
  mna_solver1(&out);
  mna_solver1_terminate();

  // out->vout[last] 출력
  
  int last = N - 1; // 35000000
  printf("%.15e %.15e %.15e\n",
        out.icc[last],
        out.deltai[last],
        out.vout[last]);
  fflush(stdout);
  return 0;
}

/*
 * Arguments    : void
 * Return Type  : void
 */
void main_mna_solver1(void)
{
  static struct0_T out;
  /* Call the entry-point 'mna_solver1'. */
  mna_solver1(&out);
}

/*
 * File trailer for main.c
 *
 * [EOF]
 */
