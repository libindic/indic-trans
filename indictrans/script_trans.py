#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Irshad Ahmad Bhat

from __future__ import unicode_literals

import re
import string
from six import unichr

from ._utils import ngram_context
from .base import BaseTransliterator


class Ind2RU(BaseTransliterator):
    """Transliterates words from Indic to Roman/Urdu script"""

    def __init__(self, source, target, decoder, build_lookup=False):
        super(Ind2RU, self).__init__(source,
                                     target,
                                     decoder,
                                     build_lookup)
        self.letters = set(string.ascii_letters)
        self.non_alpha = re.compile(r"([^a-zA-Z%s]+)" % (self.esc_ch))

    def case_trans(self, word, k_best=5):
        if not word:
            return ''
        if word[0] == self.esc_ch:
            return word[1:]
        if word[0] not in self.letters:
            if self.target == 'urd':
                return word.translate(self.punkt_tbl)
            return word
        if word in self.lookup:
            return self.lookup[word]
        word = ' '.join(word)
        if self.target == 'urd':
            word = re.sub(r' ([aVYZ])', r'\1', word)
        elif self.source == 'hin':
            word = re.sub(r' ([aZ])', r'\1', word)
        else:
            word = re.sub(r' ([VYZ])', r'\1', word)
        if self.source == 'mal':
            word = word.replace('rY rY', 'rYrY')
        word_feats = ngram_context(word.split())
        t_word = self.predict(word_feats, k_best)
        if self.build_lookup:
            self.lookup[word] = t_word
        return t_word


class Rom2Ind(BaseTransliterator):
    """Transliterates words from Roman to Indic script"""

    def __init__(self, source, target, decoder, build_lookup=False):
        super(Rom2Ind, self).__init__(source,
                                      target,
                                      decoder,
                                      build_lookup)
        self.non_alpha = re.compile(r"([^a-z]+)")
        self.letters = set(string.ascii_letters[:26])

    def handle_matra(self, text):
        """temporary fix for misfitted matras"""
        text = text.replace('aMM', 'aMm')
        text = re.sub(r'([AEIOUeiou])MM', r'\1M', text)
        text = text.replace('MM', 'M')
        text = text.replace('nM', 'nn')
        text = text.replace('xM', 'dan')
        text = re.sub(r'([DPK])([Mz])', r'\1Z\2', text)
        text = re.sub(r'([rm])M', r'\1n', text)
        text = re.sub(r'([gw])M', r'\1af', text)
        text = re.sub(r'\bM', r'f', text)
        text = re.sub(r'\bz', r'n', text)
        text = re.sub(r'([bcdhjklpstvy])M', r'\1aM', text)
        return text

    def case_trans(self, word, k_best=5):
        if not word:
            return ''
        elif word[0] not in self.letters:
            return word
        if word in self.lookup:
            if self.decode == 'viterbi':
                return self.wx_process(self.lookup[word])
            else:
                return [self.wx_process(w) for w in self.lookup[word]]
        word = re.sub(r'([a-z])\1\1+', r'\1\1', word)
        word = ' '.join(word)
        word = re.sub(r'([bcdgjptsk]) h', r'\1h', word)
        word_feats = ngram_context(word.split(), n=4)
        t_word = self.predict(word_feats, k_best)
        if self.decode == 'viterbi':
            t_word = self.handle_matra(t_word)
            t_word = self.wx_process(t_word)
        else:
            t_word = [self.handle_matra(w) for w in t_word]
            t_word = [self.wx_process(w) for w in t_word]
        if self.build_lookup:
            self.lookup[word] = t_word
        return t_word


class Urd2Ind(BaseTransliterator):
    """Transliterate words from Persio-Arabic to Indic script"""

    def __init__(self, source, target, decoder, build_lookup=False):
        super(Urd2Ind, self).__init__(source,
                                      target,
                                      decoder,
                                      build_lookup)
        self.non_alpha = re.compile(
            '([^\u0621-\u063a\u0641-\u064a\u0674-\u06d3\u064b\u0651\u0670]+)')
        self.letters = set(map(unichr,
                               list(range(ord("\u0621"), ord("\u063b"))) +
                               list(range(ord("\u0641"), ord("\u064b"))) +
                               list(range(ord("\u0674"), ord("\u06d4")))))

    def case_trans(self, word, k_best=5):
        if not word:
            return ''
        elif word[0] not in self.letters:
            return word.translate(self.punkt_tbl)
        if word in self.lookup:
            if self.decode == 'viterbi':
                return self.wx_process(self.lookup[word])
            else:
                return [self.wx_process(w) for w in self.lookup[word]]
        word = ' '.join(word)
        word = word.replace(' \u06be', '\u06be')
        word_feats = ngram_context(word.split(), n=4)
        t_word = self.predict(word_feats, k_best)
        if self.decode == 'viterbi':
            t_word = self.wx_process(t_word)
        else:
            t_word = [self.wx_process(w) for w in t_word]
        if self.build_lookup:
            self.lookup[word] = t_word
        return t_word
