#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Irshad Ahmad Bhat

"""
Transliteration Tool:
Roman to Indic transliterator
"""
from __future__ import unicode_literals

import re
import warnings

from .base import BaseTransliterator

warnings.filterwarnings("ignore")


class rom_to_ind(BaseTransliterator):
    """Transliterates words from Roman to Indic script"""
    def __init__(self, source, target, decoder, build_lookup=False):
        super(rom_to_ind, self).__init__(source,
                                         target,
                                         decoder,
                                         build_lookup)

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
        word_feats = self.feature_extraction(word.split(), n=4)
        op_word = self.predict(word_feats, k_best)
        if self.decode == 'viterbi':
            op_word = self.handle_matra(op_word)
            op_word = self.wx_process(op_word)
        else:
            op_word = [self.handle_matra(w) for w in op_word]
            op_word = [self.wx_process(w) for w in op_word]
        if self.build_lookup:
            self.lookup[word] = op_word
        return op_word
