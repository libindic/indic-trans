#!/usr/bin/env python

# Copyright (C) 2015 Irshad Ahmad Bhat

from .wx import WX
from .ctranxn import count_tranxn
from .sparseadd import sparse_add
from .one_hot_encoder import OneHotEncoder
from .script_normalizer import UrduNormalizer

__all__ = ["WX", "count_tranxn", "sparse_add", "OneHotEncoder",
           "UrduNormalizer", "ngram_context"]


def ngram_context(letters, n=4):
    feats = []
    dummies = ["_"] * n
    context = dummies + letters + dummies
    for i in range(n, len(context) - n):
        unigrams = context[i - n: i] +\
            [context[i]] +\
            context[i + 1: i + (n + 1)]
        ngrams = ['|'.join(ng) for k in range(2, n + 1)
                  for ng in zip(*[unigrams[j:]
                                  for j in range(k)])]
        feats.append(unigrams + ngrams)
    return feats
