/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: main.c
 *
 * MATLAB Coder version            : 24.2
 * C/C++ source code generated on  : 31-Dec-2025 14:00:43
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

#include <stdio.h>
#include <stdlib.h>

#include "mna_solver.h"
#include "mna_solver_initialize.h"
#include "mna_solver_terminate.h"

int main(void)
{
    /* NOTE:
       Original example used 35,000,001 points.
       Keeping the same size avoids size-mismatch if mna_solver writes full length.
       This allocates about 560MB (2 arrays) on the heap.
    */
    const size_t N = 35000001ULL;

    double *t  = (double*)malloc(sizeof(double) * N);
    double *v7 = (double*)malloc(sizeof(double) * N);

    if (t == NULL || v7 == NULL) {
        fprintf(stderr, "malloc failed (N=%llu). Not enough memory.\n",
                (unsigned long long)N);
        free(t);
        free(v7);
        return 1;
    }

    /* If initialize is called automatically inside mna_solver, calling it again is usually safe,
       but if your generated code explicitly says it's auto-called, you can comment this out. */
    mna_solver_initialize();

    mna_solver(t, v7);

    /* quick sanity print */
    printf("t[0]=%.10f, v7[0]=%.10f\n", t[0], v7[0]);
    printf("t[last]=%.10f, v7[last]=%.10f\n", t[N-1], v7[N-1]);

    mna_solver_terminate();

    free(t);
    free(v7);
    return 0;
}