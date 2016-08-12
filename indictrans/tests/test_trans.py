#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

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

    def test_bad_input_lang(self):
        self.assertRaises(NotImplementedError, Transliterator,
                          source='eng', target='unknown')
        self.assertRaises(NotImplementedError, Transliterator,
                          source='unknown', target='eng')
        self.assertRaises(NotImplementedError, Transliterator,
                          source='unknown', target='unknown')

    def test_bad_decoder(self):
        self.assertRaises(ValueError, Transliterator, decode='unknown')

    def test_ind2ru(self):
        """Test Indic-to-[Roman, Urdu] ML models"""
        for lang_pair in self.src2trg:
            src = lang_pair[0]
            trg = lang_pair[1]
            trans = Transliterator(source=src, target=trg)
            with io.open('%s/%s_%s.testpairs' % (self.test_dir, src, trg),
                         encoding='utf-8') as fp:
                for line in fp:
                    word, expected = line.split()
                    self.assertEqual(trans.transform(word), expected)

    def test_ru2ind(self):
        """Test [Roman, Urdu]-to-Indic ML models"""
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
        """Make sure `k-best` works without failure"""
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
        """Test Indic-to-Indic ML and Rule-Based models."""
        with io.open('%s/indic-test' % self.test_dir, encoding='utf-8') as fp:
            # first line contains language codes
            lang_codes = fp.readline().split()
            lang2word = dict(zip(lang_codes,
                                 [[] for i in range(len(lang_codes))]))
            for line in fp:
                line = line.split()
                for i, word in enumerate(line):
                    lang2word[lang_codes[i]].append(word)
        for src in lang_codes:
            for trg in lang_codes:
                if src == trg:
                    continue
                s2t_ml = Transliterator(source=src, target=trg, rb=False)
                s2t_rb = Transliterator(source=src, target=trg, rb=True)
                for word in lang2word[src]:
                    s2t_ml.transform(word)
                    s2t_rb.transform(word)

    def test_parser(self):
        # test parser arguments
        parser = parse_args(['--input', 'infile',
                             '--output', 'outfile',
                             '--source', 'hin',
                             '--target', 'eng',
                             '--build-lookup',
                             '--rb'])
        self.assertEqual(parser.infile, 'infile')
        self.assertEqual(parser.outfile, 'outfile')
        self.assertEqual(parser.source, 'hin')
        self.assertEqual(parser.target, 'eng')
        self.assertTrue(parser.build_lookup)
        self.assertTrue(parser.rb)
        # test parser args processing
        process_args(parse_args(['-i', '%s/indic-test' % self.test_dir,
                                 '-o', '/tmp/test.out',
                                 '-s', 'hin',
                                 '-t', 'mal',
                                 '-b', '-r']))
