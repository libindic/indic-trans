#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Irshad Ahmad Bhat

from __future__ import unicode_literals

import io
import re
import json
import os.path

import numpy as np
from scipy.sparse import issparse

from ._utils import WX, OneHotEncoder, UrduNormalizer


class BaseTransliterator(object):
    """Base class for transliterator.

    Attributes
    ----------
    vectorizer_ : instance
        `OneHotEncoder` instance for converting categorical features to
        one-hot features.

    classes_ : dict
        Dictionary of set of tags with unique ids ({id: tag}).

    coef_ : array
        HMM coefficient array

    intercept_init_ : array
        HMM intercept array for first layer of trellis.

    intercept_trans_ : array
        HMM intercept/transition array for middle layers of trellis.

    intercept_final_ : array
        HMM intercept array for last layer of trellis.

    wx_process : method
        `wx2utf`/`utf2wx` method of `WX` instance

    nu : instance
        `UrduNormalizer` instance for normalizing Urdu scripts.

    """

    def __init__(self, source, target, decoder, build_lookup=False):
        if source in ('mar', 'nep', 'kok', 'bod'):
            source = 'hin'
        elif source == 'asm':
            source = 'ben'
        if target in ('mar', 'nep', 'kok', 'bod'):
            target = 'hin'
        elif target == 'asm':
            target = 'ben'
        self.source = source
        self.target = target
        self.lookup = dict()
        self.build_lookup = build_lookup
        self.decode, self.decoder = decoder
        self.tab = '\x01\x03'  # mask tabs
        self.space = '\x02\x04'  # mask spaces
        self.esc_ch = '\x00'  # escape-sequence for Roman in WX
        self.dist_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_fit()

    def load_models(self):
        """Loads transliteration models."""
        self.vectorizer_ = OneHotEncoder()
        model = '%s-%s' % (self.source, self.target)
        with open('%s/models/%s/sparse.vec' % (self.dist_dir, model)) as jfp:
            self.vectorizer_.unique_feats = json.load(jfp)
        self.classes_ = np.load(
            '%s/models/%s/classes.npy' %
            (self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True)[0]
        self.coef_ = np.load(
            '%s/models/%s/coef.npy' % (self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True)[0].astype(np.float64)
        self.intercept_init_ = np.load(
            '%s/models/%s/intercept_init.npy' %
            (self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True).astype(np.float64)
        self.intercept_trans_ = np.load(
            '%s/models/%s/intercept_trans.npy' %
            (self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True).astype(np.float64)
        self.intercept_final_ = np.load(
            '%s/models/%s/intercept_final.npy' %
            (self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True).astype(np.float64)
        # convert numpy.bytes_/numpy.string_ to numpy.unicode_
        if not isinstance(self.classes_[0], np.unicode_):
            self.classes_ = {k: v.decode('utf-8')
                             for k, v in self.classes_.items()}

    def load_mappings(self):
        # initialize punctuation map table
        self.punkt_tbl = dict()
        with io.open('%s/mappings/punkt.map' % self.dist_dir,
                     encoding='utf-8') as punkt_fp:
            for line in punkt_fp:
                s, t = line.split()
                if self.target == 'urd':
                    if s in ["'", '"']:
                        continue
                    self.punkt_tbl[ord(s)] = t
                else:
                    self.punkt_tbl[ord(t)] = s

    def base_fit(self):
        # load models
        self.load_models()
        # load mapping tables for Urdu
        if 'urd' in [self.source, self.target]:
            self.load_mappings()
        # initialize Urdu Normalizer
        if self.source == 'urd':
            self.nu = UrduNormalizer()
        # initialize wx-converter and character-maps
        if self.source in ['eng', 'urd']:
            wxp = WX(order='wx2utf', lang=self.target)
            self.wx_process = wxp.wx2utf
        else:
            wxp = WX(order='utf2wx', lang=self.source)
            self.wx_process = wxp.utf2wx
            self.mask_roman = re.compile(r'([a-zA-Z]+)')

    def predict(self, word, k_best=5):
        """Given encoded word matrix and HMM parameters, predicts output
        sequence (target word)"""
        X = self.vectorizer_.transform(word)
        if issparse(X):
            scores = X.dot(self.coef_.T).toarray()
        else:
            scores = self.coef_.dot(X.T).T
        if self.decode == 'viterbi':
            y = self.decoder.decode(scores,
                                    self.intercept_trans_,
                                    self.intercept_init_,
                                    self.intercept_final_)
            y = [self.classes_[pid] for pid in y]
            y = ''.join(y).replace('_', '')
            return y
        else:
            top_seq = list()
            y = self.decoder.decode(scores,
                                    self.intercept_trans_,
                                    self.intercept_init_,
                                    self.intercept_final_,
                                    k_best)
            for path in y:
                w = [self.classes_[pid] for pid in path]
                w = ''.join(w).replace('_', '')
                top_seq.append(w)
            return top_seq

    def convert_to_wx(self, text):
        """Converts Indic scripts to WX."""
        if self.source == 'eng':
            return text.lower()
        if self.source == 'urd':
            return self.nu.normalize(text)
        if self.source == 'ben':
            # Assamese `ra` to Bengali `ra`
            text = text.replace('\u09f0', '\u09b0')
            # Assamese `va` to Bengali `va`
            text = text.replace('\u09f1', '\u09ac')
        text = self.mask_roman.sub(r'%s\1' % (self.esc_ch), text)
        text = self.wx_process(text)
        return text

    def transliterate(self, text, k_best=None):
        """Single best transliteration using viterbi decoding."""
        trans_list = []
        text = self.convert_to_wx(text)
        text = text.replace('\t', self.tab)
        text = text.replace(' ', self.space)
        lines = text.split("\n")
        for line in lines:
            if not line.strip():
                trans_list.append(line)
                continue
            trans_line = str()
            line = self.non_alpha.split(line)
            for word in line:
                trans_line += self.case_trans(word)
            trans_list.append(trans_line)
        trans_line = '\n'.join(trans_list)
        trans_line = trans_line.replace(self.space, ' ')
        trans_line = trans_line.replace(self.tab, '\t')
        return trans_line

    def top_n_trans(self, text, k_best=5):
        """Returns k-best transliterations using beamsearch decoding.

        Parameters
        ----------
        k_best : int, default: 5, optional
            Used by `Beamsearch` decoder to return k-best transliterations.
        """
        if k_best < 2:
            raise ValueError('`k_best` value should be >= 2')
        trans_word = []
        text = self.convert_to_wx(text)
        words = self.non_alpha.split(text)
        for word in words:
            op_word = self.case_trans(word, k_best)
            if isinstance(op_word, list):
                trans_word.append(op_word)
            else:
                trans_word.append([word] * k_best)
        return [''.join(w) for w in zip(*trans_word)]
