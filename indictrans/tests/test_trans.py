#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from testtools import TestCase
from indictrans import transliterator


class TestTransliterator(TestCase):

    def setUp(self):
        super(TestTransliterator, self).setUp()
        source = 'hin ben mal guj pan kan tam tel'.split()
        target = ['eng'] * len(source)
        self.src2trg = zip(source, target)
        self.trg2src = zip(target, source)
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_src2trg(self):
        for lang_pair in self.src2trg:
            src = lang_pair[0]
            trg = lang_pair[1]
            trans = transliterator(source=src, target=trg)
            with open('%s/%s_%s.testpairs' % (self.test_dir, src, trg)) as fp:
                for line in fp:
                    word, expected = line.split()
                    self.assertEqual(trans.transform(word), expected)

    def test_trg2src(self):
        for lang_pair in self.trg2src:
            src = lang_pair[0]
            trg = lang_pair[1]
            trans = transliterator(source=src, target=trg)
            with open('%s/%s_%s.testpairs' % (self.test_dir, trg, src)) as fp:
                for line in fp:
                    expected, word = line.split()
                    self.assertEqual(trans.transform(word), expected)
