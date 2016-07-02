#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Irshad Ahmad Bhat

"""
Transliteration Tool:
Indic to Roman transliterator
"""
from __future__ import unicode_literals

import re
import json
import string
import os.path
import warnings

import numpy as np

from ._utils import (wxilp, enc)

warnings.filterwarnings("ignore")


class BaseTransliterator(object):
    """Transliterates words from Indic to Roman script"""

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
        self.base_fit()

    def base_fit(self):
        dist_dir = os.path.dirname(os.path.abspath(__file__))
        # load models
        model = '%s-%s' % (self.source, self.target)
        self.vectorizer_ = enc(sparse=True)
        with open('%s/models/%s/sparse.vec' % (dist_dir, model)) as jfp:
            self.vectorizer_.unique_feats = json.load(jfp)
        self.classes_ = np.load(
            '%s/models/%s/classes.npy' %
            (dist_dir, model))[0]
        self.coef_ = np.load(
            '%s/models/%s/coef.npy' % (dist_dir, model),
            encoding='latin1')[0].astype(np.float64)  # FIXME why latin1?
        self.intercept_init_ = np.load(
            '%s/models/%s/intercept_init.npy' %
            (dist_dir, model)).astype(np.float64)
        self.intercept_trans_ = np.load(
            '%s/models/%s/intercept_trans.npy' %
            (dist_dir, model)).astype(np.float64)
        self.intercept_final_ = np.load(
            '%s/models/%s/intercept_final.npy' %
            (dist_dir, model)).astype(np.float64)
        # initialize wx-converter and character-maps
        if self.source in ['eng', 'urd']:
            wxp = wxilp(order='wx2utf', lang=self.target)
            self.wx_process = wxp.wx2utf
            self.non_alpha = re.compile(r"([^a-z]+)")
            self.letters = set(string.ascii_letters[:26])
        else:
            wxp = wxilp(order='utf2wx', lang=self.source)
            self.wx_process = wxp.utf2wx
            self.letters = set(string.ascii_letters)
            self.mask_roman = re.compile(r'([a-zA-Z]+)')
            self.non_alpha = re.compile(r"([^a-zA-Z%s]+)" % (self.esc_ch))

    def feature_extraction(self, letters, n=4):
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

    def predict(self, word, k_best=5):
        X = self.vectorizer_.transform(word)
        scores = X.dot(self.coef_.T).toarray()
        if self.decode == 'viterbi':
            y = self.decoder.decode(
                scores,
                self.intercept_trans_,
                self.intercept_init_,
                self.intercept_final_)
            y = [self.classes_[pid].decode('utf-8') for pid in y]
            y = ''.join(y).replace('_', '')
            return y
        else:
            top_seq = list()
            y = self.decoder.decode(
                scores,
                self.intercept_trans_,
                self.intercept_init_,
                self.intercept_final_,
                k_best)
            for path in y:
                w = [self.classes_[pid].decode('utf-8') for pid in path]
                w = ''.join(w).replace('_', '')
                top_seq.append(w)
            return top_seq

    def convert_to_wx(self, text):
        if self.source in ['eng', 'urd']:
            return text.lower()
        if self.source == 'ben':
            text = text.replace('\u09f0', '\u09b0')
            text = text.replace('\u09f1', '\u09ac')
        text = self.mask_roman.sub(r'%s\1' % (self.esc_ch), text)
        text = self.wx_process(text)
        return text

    def transliterate(self, text, k_best=None):
        """single best transliteration using viterbi decoding"""
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
        """k-best transliterations using beamsearch decoding"""
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
