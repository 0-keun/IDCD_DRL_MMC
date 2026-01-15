#include "mna_solver1_types.h"
#include "main.h"
#include <stdio.h>
#include <stdlib.h>

int mna_solver1_alloc(struct0_T *out)
{
    out->t          = (double*)malloc((size_t)SimSteps * sizeof(double));
    out->vout       = (double*)malloc((size_t)SimSteps * sizeof(double));
    out->deltavc    = (double*)malloc((size_t)SimSteps * sizeof(double));
    out->deltai     = (double*)malloc((size_t)SimSteps * sizeof(double));
    out->icc_ac     = (double*)malloc((size_t)SimSteps * sizeof(double));
    // out->vout_rmse  = (double*)malloc((size_t)SimSteps * sizeof(double));

    if (!out->t || !out->vout || !out->deltavc || !out->deltai) {
        fprintf(stderr, "mna_solver1_alloc: malloc failed for out buffers\n");
        return 0;
    }
    return 1;
}

void mna_solver1_free(struct0_T *out)
{
    free(out->t);         out->t = NULL;
    free(out->vout);      out->vout = NULL;
    free(out->deltavc);   out->deltavc = NULL;
    free(out->deltai);    out->deltai = NULL;
    free(out->icc_ac);    out->deltai = NULL;
}