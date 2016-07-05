#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import os

from testtools import TestCase
from indictrans import (transliterator, parse_args)


class TestTransliterator(TestCase):
    def setUp(self):
        super(TestTransliterator, self).setUp()
        source = 'hin ben mal guj pan kan tam tel ori'.split()
        target_rom = ['eng'] * len(source)
        self.src2trg = list(zip(source, target_rom))
        self.trg2src = list(zip(target_rom, source))
        source = 'hin pan'.split()
        target_urd = ['urd'] * len(source)
        self.src2trg += list(zip(source, target_urd))
        self.trg2src += list(zip(target_urd, source))
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
        r2i = transliterator(
            source='eng',
            target='hin',
            decode='beamsearch')
        i2r = transliterator(
            source='hin',
            target='eng',
            decode='beamsearch')
        for k in k_best:
            hin = r2i.transform('indictrans', k_best=k)
            eng = i2r.transform(hin[0], k_best=k)
            assert len(hin) == k
            assert len(eng) == k

    def test_parser(self):
        parser = parse_args(['--input', 'infile',
                             '--output', 'outfile',
                             '--source', 'hin',
                             '--target', 'eng',
                             '--build-lookup'])
        self.assertEqual(parser.infile, 'infile')
        self.assertEqual(parser.outfile, 'outfile')
        self.assertEqual(parser.source, 'hin')
        self.assertEqual(parser.target, 'eng')
        self.assertTrue(parser.build_lookup)
