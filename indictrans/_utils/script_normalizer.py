#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import os
import re


class UrduNormalizer():
    """Normalizer for Urdu scripts. Normalizes different unicode canonical
    equivalances to a single unicode code-point.

    Examples
    --------
    >>> from indictrans import UrduNormalizer
    >>> text = u'''ﺎﻧ کﻭ ﻍیﺮﻗﺎﻧﻮﻧی ﺝگہ کﺱ ﻥے ﺩی؟
    ... ﻝﻭگﻭں کﻭ ﻖﺘﻟ کیﺍ ﺝﺍﺭ ہﺍ ہے ۔
    ... ﺏڑے ﻡﺎﻣﻭں ﺎﻧ ﺪﻧﻭں ﻢﺤﻟہ ﺥﺩﺍﺩﺍﺩ ﻡیں ﺭہﺕے ﺕھے۔
    ... ﻉﻭﺎﻣی یﺍ ﻑﻼﺣی ﺥﺪﻣﺎﺗ ﺍیک ﺎﻟگ ﺩﺎﺋﺭہ ﻊﻤﻟ ہے۔'''
    >>> nu = UrduNormalizer()
    >>> print(nu.normalize(text))
    ان کو غیرقانونی جگہ کس نے دی؟
    لوگوں کو قتل کیا جار ہا ہے ۔
    بڑے ماموں ان دنوں محلہ خداداد میں رہتے تھے۔
    عوامی یا فلاحی خدمات ایک الگ دائرہ عمل ہے۔
    """
    def __init__(self):
        self.norm_tbl = dict()
        dist_dir = os.path.dirname(os.path.abspath(__file__))
        with io.open('%s/../mappings/urdu_urdu.map' % (dist_dir),
                     encoding='utf-8') as fp:
            for line in fp:
                s, t = line.split()
                self.norm_tbl[ord(s)] = t

    def cnorm(self, text):
        """Normalize NO_BREAK_SPACE, SOFT_HYPHEN, WORD_JOINER, H_SPACE,
        ZERO_WIDTH[SPACE, NON_JOINER, JOINER],
        MARK[LEFT_TO_RIGHT, RIGHT_TO_LEFT, BYTE_ORDER, BYTE_ORDER_2]
        """
        text = text.replace('\u00A0', ' ')  # NO_BREAK_SPACE
        text = text.replace('\u00AD', '')  # SOFT_HYPHEN
        text = text.replace('\u2060', '')  # WORD_JOINER
        text = text.replace('\u200A', ' ')  # H_SP
        text = text.replace('\u200B', ' ')  # ZERO_WIDTH_SPACE
        text = text.replace('\u200C', '')  # ZERO_WIDTH_NON_JOINER
        text = text.replace('\u200D', '')  # ZERO_WIDTH_JOINER
        text = text.replace('\u200E', '')  # LEFT_TO_RIGHT_MARK
        text = text.replace('\u200F', '')  # RIGHT_TO_LEFT_MARK
        text = text.replace('\uFEFF', '')  # BYTE_ORDER_MARK
        text = text.replace('\uFFFE', '')  # BYTE_ORDER_MARK_2

        return text

    def normalize(self, text):
        """normalize text"""
        text = self.cnorm(text)
        # canonical normalizations
        text = text.translate(self.norm_tbl)
        # matra normalizations
        text = re.sub('[\u064d\u0652\u0654-\u065b]', '', text)
        text = re.sub('([^\u06a9\u06af\u0686\u062c\u0679\u0688'
                      '\u062a\u062f\u067e\u0628\u0691])\u06be',
                      r'\1%s' % '\u06c1', text)
        # remove vowels
        text = re.sub('[\u0650\u064e\u064f]', '', text)
        # hamza and mada normalizations
        text = text.replace('\u0627\u0653', '\u0622')
        text = text.replace('\u0648\u0654', '\u0624')
        text = text.replace('\u06cc\u0654', '\u0626')
        text = text.replace('\u06d2\u0654', '\u06d3')
        text = text.replace('\u0626\u0626', '\u0626\u06cc')
        text = text.replace('\u06d5\u0654', '\u06c1\u0654')

        return text
