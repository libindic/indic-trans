#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from numpy import ndarray
from six.moves import xrange
from testtools import TestCase
from scipy.sparse import issparse

from indictrans import trunk


class TestTrunk(TestCase):
    def setUp(self):
        super(TestTrunk, self).setUp()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_data_load(self):
        X, y = trunk.load_data('%s/hin2rom.tnt' % self.test_dir)
        for i in xrange(len(X)):
            self.assertEqual(len(X[i]), len(y[i]))

    def test_context_build(self):
        X = [list('hello'), list('welcome'), list('testing_is_fun')]
        X_ = trunk.build_context(X, ngram=4)
        # number of sequences should remain same
        self.assertEqual(len(X), len(X_))
        for seq in X_:
            for ch_context in seq[1:]:
                # same amout of context should be generated
                # for each character of each sequence
                self.assertEqual(len(X_[0][0]), len(ch_context))

    def test_encoder(self):
        X, y = trunk.load_data('%s/hin2rom.tnt' % self.test_dir)
        X_ = trunk.build_context(X, ngram=4)
        enc, X_enc = trunk.fit_encoder(X_)
        # number of sequences should remain same
        self.assertEqual(len(X_enc), len(X))
        for x in X_:
            x_ = enc.transform(x, sparse=True)
            self.assertTrue(issparse(x_))
            x_ = enc.transform(x, sparse=False)
            self.assertIsInstance(x_, ndarray)

    def test_sp_train(self):
        X, y = trunk.load_data('%s/hin2rom.tnt' % self.test_dir)
        X_ = trunk.build_context(X, ngram=4)
        enc, X_enc = trunk.fit_encoder(X_)
        clf = trunk.train_sp(X_enc, y)
        y_out = clf.predict(X_enc)
        for i in xrange(len(y_out)):
            # each token of sequence should get a tag
            self.assertEqual(len(y[i]), len(y_out[i]))
        # test direct testing
        trunk.test_sp(clf, enc, '%s/hin2rom.tnt' % self.test_dir)
        # test model dump
        trunk.save_models(clf, enc, '/tmp/models')
        # dump directory should get renamed if it already exists
        trunk.save_models(clf, enc, '/tmp/models')
        trunk.save_models(clf, enc, '/tmp/models')
        trunk.save_models(clf, enc, '/tmp/models')

    def test_parser(self):
        parser = trunk.parse_args(['--data-file', 'path/to/train_file',
                                   '--output-dir', 'path/to/models',
                                   '--ngrams', '4',
                                   '--lr-exp', '0.1',
                                   '--max-iter', '15',
                                   '--random-state', '127',
                                   '--verbosity', '3',
                                   '--test-file', 'path/to/test_file'])
        self.assertEqual(parser.data_file, 'path/to/train_file')
        self.assertEqual(parser.out_dir, 'path/to/models')
        self.assertEqual(parser.ngram, 4)
        self.assertEqual(parser.lr_exp, 0.1)
        self.assertEqual(parser.n_iter, 15)
        self.assertEqual(parser.random_state, 127)
        self.assertEqual(parser.verbose, 3)
        self.assertEqual(parser.test_file, 'path/to/test_file')
