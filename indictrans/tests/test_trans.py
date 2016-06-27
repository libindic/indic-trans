#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os

from testtools import TestCase
from indictrans import transliterator


class TestTransliterator(TestCase):

    def setUp(self):
        super(TestTransliterator, self).setUp()
        source = 'hin ben mal guj pan kan tam tel ori'.split()
        target = ['eng'] * len(source)
        self.src2trg = zip(source, target)
        self.trg2src = zip(target, source)
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_src2trg(self):
        for lang_pair in self.src2trg:
            src = lang_pair[0]
            trg = lang_pair[1]
            trans = transliterator(source=src, target=trg)
            with io.open('%s/%s_%s.testpairs' % (self.test_dir, src, trg),
                         encoding='utf-8') as fp:
                for line in fp:
                    word, expected = line.split()
                    self.assertEqual(trans.transform(word), expected)

    def test_trg2src(self):
        for lang_pair in self.trg2src:
            src = lang_pair[0]
            trg = lang_pair[1]
            trans = transliterator(source=src, target=trg)
            with io.open('%s/%s_%s.testpairs' % (self.test_dir, trg, src),
                         encoding='utf-8') as fp:
                for line in fp:
                    expected, word = line.split()
                    self.assertEqual(trans.transform(word), expected)

    def test_kbest(self):
        k_best = range(2, 15)
        for k in k_best:
            r2i = transliterator(
                source='eng',
                target='hin',
                decode='beamsearch',
                k_best=k)
            i2r = transliterator(
                source='hin',
                target='eng',
                decode='beamsearch',
                k_best=k)
            hin = r2i.transform('indictrans')
            eng = i2r.transform(hin[0])
            assert len(hin) == k
            assert len(eng) == k
