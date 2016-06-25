# Copyright Irshad Ahmad Bhat 2015.
cimport cython
cimport numpy as np
import numpy as np

np.import_array()

cdef np.float64_t NEGINF = -np.inf

@cython.boundscheck(False)
@cython.wraparound(False)
def decode(np.ndarray[ndim=2, dtype=np.float64_t] emissions,
           np.ndarray[ndim=2, dtype=np.float64_t] b_trans,
           np.ndarray[ndim=1, dtype=np.float64_t] init,
           np.ndarray[ndim=1, dtype=np.float64_t] final,
           np.uint8_t beamwidth):

    cdef tuple new_seq, beamItem
    cdef np.npy_intp n_samples, n_states
    cdef list sequences, newSequences, partial
    cdef np.float64_t score, em_score, prevScore
    cdef np.uint16_t i, j, k
    
    sequences = list() 
    n_states = emissions.shape[1]
    n_samples = emissions.shape[0]
    for j in range(n_states):
        score = emissions[0, j] + init[j]
        sequences.append((score, j, [j]))

    sequences = sorted(sequences, reverse=True)
    sequences = sequences[:beamwidth]

    for i in range(1, n_samples):
        newSequences = list()
        for k in range(n_states):
            em_score = emissions[i][k]
            for beamItem in sequences:
                j = beamItem[1]
                prevScore = beamItem[0]
                partial = beamItem[2][:] # copy by value
                score = prevScore + b_trans[j][k] + em_score
                partial.append(k)
                new_seq = (score, k, partial)
                newSequences.append(new_seq)
        sequences = sorted(newSequences, reverse=True)
        sequences = sequences[:beamwidth]
    
    newSequences = list()
    for beamItem in sequences:
        j = beamItem[1]
        prevScore = beamItem[0]
        partial = beamItem[2][:]
        score = prevScore + final[j]
        new_seq = (score, j, partial)
        newSequences.append(new_seq)
    sequences = sorted(newSequences, reverse=True)
    sequences = sequences[:beamwidth]

    return [sequence[2] for sequence in sequences]
