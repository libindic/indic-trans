#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Irshad Ahmad Bhat

"""
Transliteration Tool:
Indic to Roman transliterator
"""
from __future__ import unicode_literals

import re
import warnings

from .base import BaseTransliterator

warnings.filterwarnings("ignore")


class ind_to_rom(BaseTransliterator):
    """Transliterates words from Indic to Roman script"""

    def __init__(self, source, target, decoder, build_lookup=False):
        super(ind_to_rom, self).__init__(source,
                                         target,
                                         decoder,
                                         build_lookup)

    def case_trans(self, word, k_best=5):
        if not word:
            return ''
        if word[0] == self.esc_ch:
            word = word[1:]
            return word
        if word[0] not in self.letters:
            return word
        if word in self.lookup:
            return self.lookup[word]
        word_feats = ' '.join(word)
        if self.source == 'hin':
            word_feats = re.sub(r' ([aZ])', r'\1', word_feats)
        else:
            word_feats = re.sub(r' ([VYZ])', r'\1', word_feats)
        if self.source == 'mal':
            word_feats = word_feats.replace('rY rY', 'rYrY')
        word_feats = word_feats.split()
        word_feats = self.feature_extraction(word_feats)
        op_word = self.predict(word_feats, k_best)
        if self.build_lookup:
            self.lookup[word] = op_word
        return op_word
