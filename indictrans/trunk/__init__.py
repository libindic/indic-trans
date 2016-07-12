#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
import json
import argparse
from builtins import input

import numpy as np
from six.moves import xrange

from .._utils import OneHotEncoder
from .._utils import ngram_context
from .perceptron import StructuredPerceptron


def save_models(clf, enc, out_dir):
    if os.path.isdir(out_dir):
        sys.stderr.write(
            "UserWarnning: Output directory '{0}' already exists."
            " Any existing models will get overwritten.".format(out_dir))
        try:
            input('\n---Press any key to continue---\n'
                  '-----Press Crtl+C to return------\n')
        except KeyboardInterrupt:
            sys.stderr.write('\nModel dump aborted successfully\n')
            return
    else:
        os.makedirs(out_dir)

    with open('%s/sparse.enc' % out_dir, 'w') as j_fp:
        json.dump(enc.unique_feats, j_fp)
    np.save('%s/classes' % out_dir, [clf.classes_])
    np.save('%s/coef' % out_dir, [clf.coef_.astype(np.float16)])
    np.save('%s/intercept_init' % out_dir,
            clf.intercept_init_.astype(np.float16))
    np.save('%s/intercept_trans' % out_dir,
            clf.intercept_trans_.astype(np.float16))
    np.save('%s/intercept_final' % out_dir,
            clf.intercept_final_.astype(np.float16))


def test_sp(clf, enc, test_file, ngram=4):
    X, y = load_data(test_file)
    X_ = [enc.transform(ngram_context(x, n=ngram)) for x in X]
    y_out = clf.predict(X_)
    with open('%s.out' % test_file, 'w') as fp:
        for i in xrange(len(X)):
            fp.write('%s\n\n' % '\n'.join(
                    ['\t'.join(st) for st in zip(X[i], y_out[i])]))


def train_sp(X, y, n_iter=10, lr_exp=0.1,
             random_state=37, verbose=0):
    clf = StructuredPerceptron(random_state=random_state,
                               n_iter=n_iter, verbose=verbose)
    clf.fit(X, y)
    return clf


def fit_encoder(X):
    enc = OneHotEncoder()
    enc.fit(np.vstack(X))
    X = [enc.transform(x) for x in X]
    return enc, X


def build_context(X, ngram=4):
    X = [ngram_context(x, n=ngram) for x in X]
    return X


def load_data(data_file):
    X, y = [], []
    input_seq, output_seq = [], []
    with io.open(data_file, encoding='utf-8') as fp:
        for line in fp:
            if not line.strip():
                X.append(input_seq)
                y.append(output_seq)
                input_seq, output_seq = [], []
            else:
                s, t = line.split()
                input_seq.append(s)
                output_seq.append(t)

    return X, y


def parse_args(args):
    # parse command line arguments
    parser = argparse.ArgumentParser(
        prog="StructuredPerceptron",
        description="Structured perceptron for sequence classification.")
    parser.add_argument('-v',
                        '--version',
                        action="version",
                        version="%(prog)s 1.0")
    parser.add_argument('-d',
                        '--data-file',
                        dest="data_file",
                        type=str,
                        required=True,
                        metavar='',
                        help="training data-file: set of sequences")
    parser.add_argument('-o',
                        '--output-dir',
                        dest="out_dir",
                        type=str,
                        required=True,
                        metavar='',
                        help="output directory to dump trained models")
    parser.add_argument('-n',
                        '--ngrams',
                        dest="ngram",
                        type=int,
                        default=4,
                        metavar='',
                        help="ngram context for feature extraction:"
                             " default 4")
    parser.add_argument('-e',
                        '--lr-exp',
                        dest="lr_exp",
                        type=float,
                        default=0.1,
                        metavar='',
                        help="The Exponent used for inverse scaling of"
                             "learning rate: default 0.1")
    parser.add_argument('-m',
                        '--max-iter',
                        dest="n_iter",
                        type=int,
                        default=15,
                        metavar='',
                        help="Maximum number of iterations for training:"
                             " default 15")
    parser.add_argument('-r',
                        '--random-state',
                        dest="random_state",
                        type=int,
                        default=127,
                        metavar='',
                        help="Random seed for shuffling sequences within"
                             " each iteration.")
    parser.add_argument('-l',
                        '--verbosity',
                        dest="verbose",
                        type=int,
                        default=0,
                        metavar='',
                        help="Verbosity level: default 0 (quiet moe)")
    parser.add_argument('-t',
                        '--test-file',
                        dest="test_file",
                        type=str,
                        metavar='',
                        help="testing data-file: optional: stores output"
                             " sequences in `test_file.out`")
    args = parser.parse_args(args)
    return args


def main():
    args = parse_args(sys.argv[1:])
    # load and encode data
    X, y = load_data(args.data_file)
    # build ngram context for each sequence
    X = build_context(X, ngram=args.ngram)
    # fit OneHotEncoder and encode data
    enc, X = fit_encoder(X)
    # train classifier
    clf = train_sp(X, y, args.n_iter, args.lr_exp,
                   args.random_state, args.verbose)
    # save models
    save_models(clf, enc, args.out_dir)
    # test classifier
    if args.test_file:
        sys.stderr.write('Testing ...\n')
        test_sp(clf, enc, args.test_file, ngram=args.ngram)
