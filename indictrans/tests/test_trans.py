#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import os

from testtools import TestCase
from indictrans import parse_args, process_args, Transliterator


class TestTransliterator(TestCase):
    def setUp(self):
        super(TestTransliterator, self).setUp()
        # test transliterations with English
        source = 'hin ben mal guj pan kan tam tel ori'.split()
        target_rom = ['eng'] * len(source)
        self.src2trg = list(zip(source, target_rom))
        self.trg2src = list(zip(target_rom, source))
        # test transliterations with Urdu
        source = 'hin pan eng'.split()
        target_urd = ['urd'] * len(source)
        self.src2trg += list(zip(source, target_urd))
        self.trg2src += list(zip(target_urd, source))
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_src2trg(self):
        for lang_pair in self.src2trg:
            src = lang_pair[0]
            trg = lang_pair[1]
            trans = Transliterator(source=src, target=trg)
            with io.open('%s/%s_%s.testpairs' % (self.test_dir, src, trg),
                         encoding='utf-8') as fp:
                for line in fp:
                    word, expected = line.split()
                    self.assertEqual(trans.transform(word), expected)

    def test_trg2src(self):
        for lang_pair in self.trg2src:
            src = lang_pair[0]
            trg = lang_pair[1]
            trans = Transliterator(source=src, target=trg)
            with io.open('%s/%s_%s.testpairs' % (self.test_dir, trg, src),
                         encoding='utf-8') as fp:
                for line in fp:
                    expected, word = line.split()
                    self.assertEqual(trans.transform(word), expected)

    def test_kbest(self):
        k_best = range(2, 15)
        r2i = Transliterator(source='eng',
                             target='hin',
                             decode='beamsearch')
        i2r = Transliterator(source='hin',
                             target='eng',
                             decode='beamsearch')
        for k in k_best:
            hin = r2i.transform('indictrans', k_best=k)
            eng = i2r.transform(hin[0], k_best=k)
            self.assertTrue(len(hin) == k)
            self.assertTrue(len(eng) == k)

    def test_rtrans(self):
        with io.open('%s/indic-test' % self.test_dir, encoding='utf-8') as fp:
            indic = fp.readline().split()
            for line in fp:
                line = line.split()
                for i, src in enumerate(indic):
                    for trg in indic:
                        if src == trg:
                            continue
                        if src in ['tam', 'ben'] or trg in ['tam', 'ben']:
                            # ML systems only for Tamil and Bengali yet
                            i2i_ml = Transliterator(source=src, target=trg,
                                                    by_rule=False)
                            i2i_ml.transform(line[i])
                        i2i_rb = Transliterator(source=src, target=trg,
                                                by_rule=True)
                        i2i_rb.transform(line[i])

    def test_parser(self):
        # test parser arguments
        parser = parse_args(['--input', 'infile',
                             '--output', 'outfile',
                             '--source', 'hin',
                             '--target', 'eng',
                             '--build-lookup',
                             '--by-rule'])
        self.assertEqual(parser.infile, 'infile')
        self.assertEqual(parser.outfile, 'outfile')
        self.assertEqual(parser.source, 'hin')
        self.assertEqual(parser.target, 'eng')
        self.assertTrue(parser.build_lookup)
        self.assertTrue(parser.by_rule)
        # test parser args processing
        process_args(parse_args(['-i', '%s/indic-test' % self.test_dir,
                                 '-o', '/tmp/test.out',
                                 '-s', 'hin',
                                 '-t', 'mal',
                                 '-b', '-r']))
