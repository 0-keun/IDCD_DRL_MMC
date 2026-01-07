#include "mna_solver1_types.h"
#include <stdio.h>
#include <stdlib.h>

int mna_solver1_alloc(struct0_T *out, int N)
{
    out->t      = (double*)malloc((size_t)N * sizeof(double));
    out->vout   = (double*)malloc((size_t)N * sizeof(double));
    out->icc    = (double*)malloc((size_t)N * sizeof(double));
    out->deltai = (double*)malloc((size_t)N * sizeof(double));

    if (!out->t || !out->vout || !out->icc || !out->deltai) {
        fprintf(stderr, "mna_solver1_alloc: malloc failed for out buffers\n");
        return 0;
    }
    return 1;
}

void mna_solver1_free(struct0_T *out)
{
    free(out->t);      out->t = NULL;
    free(out->vout);   out->vout = NULL;
    free(out->icc);    out->icc = NULL;
    free(out->deltai); out->deltai = NULL;
}
