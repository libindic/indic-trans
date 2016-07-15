cimport cython
cimport numpy as np
import numpy as np
from scipy.sparse import isspmatrix_csc

np.import_array()


@cython.boundscheck(False)
@cython.wraparound(False)
def sparse_add(np.ndarray[ndim=2, dtype=np.float64_t] A, B):
    """A += B where B is a sparse (CSR or CSC) matrix."""

    cdef:
        np.ndarray[ndim=1, dtype=np.float64_t, mode="c"] data
        np.ndarray[ndim=1, dtype=int, mode="c"] indices
        np.ndarray[ndim=1, dtype=int, mode="c"] idxptr

        int i, j, k

    if isspmatrix_csc(B):
        A = A.T

    data = B.data
    indices = B.indices
    idxptr = B.indptr

    for i in range(A.shape[0]):
        for j in range(idxptr[i], idxptr[i + 1]):
            k = indices[j]
            A[i, k] += data[j]
