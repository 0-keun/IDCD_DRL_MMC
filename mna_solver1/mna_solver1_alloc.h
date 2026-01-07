#ifndef MNA_SOLVER1_ALLOC_H
#define MNA_SOLVER1_ALLOC_H

#include "mna_solver1_types.h"

#ifdef __cplusplus
extern "C" {
#endif

int  mna_solver1_alloc(struct0_T *out, int N);
void mna_solver1_free(struct0_T *out);

#ifdef __cplusplus
}
#endif

#endif /* MNA_SOLVER1_ALLOC_H */
