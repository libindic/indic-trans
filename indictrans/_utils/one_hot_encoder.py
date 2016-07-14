#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright Irshad Ahmad Bhat 2016.

import numpy as np
from scipy import sparse as sp


class OneHotEncoder():
    """Transforms categorical features to continuous numeric features.

    Examples
    --------
    >>> from one_hot_encoder import OneHotEncoder
    >>> enc = OneHotEncoder()
    >>> sequences = [list('bat'), list('cat'), list('rat')]
    >>> enc.fit(sequences)
    <one_hot_encoder.OneHotEncoder instance at 0x7f346d71c200>
    >>> enc.transform(sequences, sparse=False).astype(int)
    array([[0, 1, 0, 1, 1],
           [1, 0, 0, 1, 1],
           [0, 0, 1, 1, 1]])
    >>> enc.transform(list('cat'), sparse=False).astype(int)
    array([[1, 0, 0, 1, 1]])
    >>> enc.transform(list('bat'), sparse=True)
    <1x5 sparse matrix of type '<type 'numpy.float64'>'
        with 3 stored elements in Compressed Sparse Row format>
    """
    def fit(self, X):
        """Fit OneHotEncoder to X.

        Parameters
        ----------

        X : array-like, shape [n_samples, n_feature]
            Input array of type int.

        Returns
        -------

        self
        """
        data = np.asarray(X)
        unique_feats = []
        offset = 0
        for i in range(data.shape[1]):
            feat_set_i = set(data[:, i])
            d = {val: i + offset for i, val in enumerate(feat_set_i)}
            unique_feats.append(d)
            offset += len(feat_set_i)

        self.unique_feats = unique_feats
        return self

    def transform(self, X, sparse=True):
        """Transform X using one-hot encoding.

        Parameters
        ----------

        X : array-like, shape [n_samples, n_features]
            Input array of categorical features.

        sparse : bool, default: True
            Return sparse matrix if set True else return an array.

        Returns
        -------
        X_out : sparse matrix if sparse=True else a 2-d array, dtype=int
            Transformed input.
        """
        X = np.atleast_2d(X)
        if sparse:
            one_hot_matrix = sp.lil_matrix(
                (len(X), sum(len(i) for i in self.unique_feats)))
        else:
            one_hot_matrix = np.zeros(
                (len(X), sum(len(i) for i in self.unique_feats)), bool)
        for i, vec in enumerate(X):
            for j, val in enumerate(vec):
                if val in self.unique_feats[j]:
                    one_hot_matrix[i, self.unique_feats[j][val]] = 1.0

        return sp.csr_matrix(one_hot_matrix) if sparse else one_hot_matrix
