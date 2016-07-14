#! /usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function, absolute_import

import sys

import numpy as np
from six.moves import xrange
from scipy.sparse import csc_matrix, issparse

from indictrans._decode import DECODERS
from indictrans._utils import count_tranxn, sparse_add


class StructuredPerceptron():
    """Structured perceptron for sequence classification.

    The implemention is based on average structured perceptron algorithm of
    M. Collins.

    Parameters
    ----------

    lr_exp : float, default: 0.1
        The Exponent used for inverse scaling of learning rate. Given iteration
        number t, the effective learning rate is ``1. / (t ** lr_exp)``

    n_iter : int, default: 15
        Maximum number of epochs of the structured perceptron algorithm

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by ``np.random``.

    verbose : int, default: 0 (quiet mode)
        Verbosity mode.

    References
    ----------

    M. Collins (2002). Discriminative training methods for hidden Markov
    models: Theory and experiments with perceptron algorithms. EMNLP.
    """
    def __init__(self, lr_exp=0.1, n_iter=15,
                 random_state=None, verbose=0):
        self.lr_exp = lr_exp
        self.n_iter = n_iter
        self.verbose = verbose
        self.random_state = random_state

    def _get_random_state(self):
        if self.random_state is None:
            random_state = np.random.mtrand._rand
        elif isinstance(self.random_state, int):
            random_state = np.random.RandomState(self.random_state)
        elif isinstance(self.random_state, np.random.mtrand._rand):
            random_state = self.random_state
        else:
            raise TypeError(
                "Type {0} not supported.".format(type(self.random_state)))
        return random_state

    def fit(self, X, y):
        """Fit the model to the given set of sequences.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_sequences, sequence_length,
                                                n_features)
            Feature matrix of train sequences.

        y : list of arrays, shape (n_sequences, sequence_length)
            Target labels.

        Returns
        -------
        self : object
            Returns self.
        """

        X = np.atleast_2d(X)
        decoder = DECODERS['viterbi']
        classes = np.unique(np.hstack(y))
        n_classes = len(set(classes))

        class_range = np.arange(n_classes)
        class_id = dict(zip(set(classes), xrange(n_classes)))
        id_class = dict(zip(xrange(n_classes), set(classes)))

        y = np.array([np.array([class_id[it] for it in t]) for t in y])
        Y_true = np.array(
                [np.array(t).reshape(-1, 1) == class_range for t in y])

        n_features = X[0][0].shape[1]
        w = np.zeros((n_classes, n_features), order='F')

        # first order transition probabilities
        b_init = np.zeros(n_classes)
        b_final = np.zeros(n_classes)
        b_trans = np.zeros((n_classes, n_classes))

        w_avg = np.zeros_like(w)
        b_init_avg = np.zeros_like(b_init)
        b_final_avg = np.zeros_like(b_final)
        b_trans_avg = np.zeros_like(b_trans)

        sequence_ids = np.arange(X.shape[1])
        rnd = self._get_random_state()

        avg_count = 1.0
        lr_exp = self.lr_exp
        for it in xrange(1, self.n_iter + 1):
            lr = 1.0 / (it ** lr_exp)

            if self.verbose >= 1:
                print("Iteration {0}".format(it), end=" ... \n")
                sys.stdout.flush()

            rnd.shuffle(sequence_ids)

            sum_loss = 0
            for id_i, i in enumerate(sequence_ids):
                X_i = X[0][i]
                if issparse(X_i):
                    score = X_i * w.T
                else:
                    score = np.dot(X_i, w.T)
                y_pred = decoder.decode(score, b_trans, b_init, b_final)
                y_t_i = y[i]
                loss = (y_pred != y_t_i).sum()  # number of wrong predictions
                if self.verbose >= 3 and not id_i:
                    comp = ' '.join(['-'.join(st) for st in zip(
                                map(str, y_pred), map(str, y_t_i))])
                    print("First sequence comparision: "
                          "{0} ... loss: {1}".format(comp, loss))
                if loss:
                    sum_loss += loss
                    Y_t_i = Y_true[i]
                    Y_pred = y_pred.reshape(-1, 1) == class_range
                    Y_pred = Y_pred.astype(np.float64)

                    Y_diff = csc_matrix(Y_pred - Y_t_i)
                    Y_diff *= -lr
                    w_update = Y_diff.T * X_i

                    t_trans = count_tranxn(y_t_i, n_classes)
                    p_trans = count_tranxn(y_pred, n_classes)
                    b_trans_update = lr * (p_trans - t_trans)
                    b_init_update = lr * (Y_pred[0] - Y_true[i][0])
                    b_final_update = lr * (Y_pred[-1] - Y_true[i][-1])

                    if isinstance(w_update, np.ndarray):
                        w += w_update
                    else:
                        sparse_add(w, w_update)
                    b_trans -= b_trans_update
                    b_init -= b_init_update
                    b_final -= b_final_update

                    w_update *= avg_count
                    b_trans_update *= avg_count
                    b_init_update *= avg_count
                    b_final_update *= avg_count

                    if isinstance(w_update, np.ndarray):
                        w_avg += w_update
                    else:
                        sparse_add(w_avg, w_update)
                    b_trans_avg -= b_trans_update
                    b_init_avg -= b_init_update
                    b_final_avg -= b_final_update

            if self.verbose >= 2:
                print("Train-set error = {0:.4f}".format(sum_loss / len(X[0])))
                sys.stdout.flush()

            avg_count += 1.

        w -= w_avg / avg_count
        b_init -= b_init_avg / avg_count
        b_trans -= b_trans_avg / avg_count
        b_final -= b_final_avg / avg_count

        self.coef_ = csc_matrix(w)
        self.intercept_init_ = b_init
        self.intercept_trans_ = b_trans
        self.intercept_final_ = b_final

        self.classes_ = id_class

        return self

    def predict(self, X):
        """Predict output sequences for input sequences in X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_sequences, sequence_length,
                                                n_features)
            Feature matrix of test sequences.

        Returns
        -------
        y : array, shape (n_sequences, sequence_length)
            Labels per sequence in X.
        """
        y = []
        decoder = DECODERS['viterbi']
        if not isinstance(X, list):
            X = [X]
        for x in X:
            if issparse(x):
                scores = x.dot(self.coef_.T).toarray()
            else:
                scores = self.coef_.dot(x.T).T

            y_ = decoder.decode(scores, self.intercept_trans_,
                                self.intercept_init_, self.intercept_final_)
            y.append([self.classes_[pred] for pred in y_])

        return y
