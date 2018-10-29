#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Irshad Ahmad Bhat

from __future__ import unicode_literals

import re
import string
from six import unichr

from .base import BaseTransliterator
from ._utils import ngram_context, WX


class Ind2Target(BaseTransliterator):
    """Transliterates text from Indic to Roman/Urdu script"""
    def __init__(self, source, target, decoder, build_lookup=False):
        super(Ind2Target, self).__init__(source,
                                         target,
                                         decoder,
                                         build_lookup)
        self.letters = set(string.ascii_letters)
        self.non_alpha = re.compile(r"([^a-zA-Z%s]+)" % (self.esc_ch))
        # initialize WX back-convertor for Indic to Indic transliteration
        self._to_indic = False
        if target not in ['eng', 'urd']:
            wxp = WX(order='wx2utf', lang=target)
            self._to_utf = wxp.wx2utf
            self._to_indic = True

    def case_trans(self, word, k_best=5):
        oword = word
        if not word:
            return ''
        if word[0] == self.esc_ch:
            return word[1:]
        if word[0] not in self.letters:
            if self.target == 'urd':
                return word.translate(self.punkt_tbl)
            return word
        if oword in self.lookup:
            return self.lookup[oword]
        word = ' '.join(word)
        word = re.sub(r' ([VYZ])', r'\1', word)
        if not self._to_indic:
            word = word.replace(' a', 'a')
        word_feats = ngram_context(word.split())
        t_word = self.predict(word_feats, k_best)
        if self._to_indic:
            t_word = self._to_utf(t_word)
        if self.build_lookup:
            self.lookup[oword] = t_word
        return t_word


class Rom2Target(BaseTransliterator):
    """Transliterates text from Roman to Indic script"""
    def __init__(self, source, target, decoder, build_lookup=False):
        super(Rom2Target, self).__init__(source,
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
        oword = word
        if not word:
            return ''
        elif word[0] not in self.letters:
            return word
        if oword in self.lookup:
            if self.target == 'urd':
                return self.lookup[oword]
            if self.decode == 'viterbi':
                return self.wx_process(self.lookup[oword])
            else:
                return [self.wx_process(w) for w in self.lookup[oword]]
        word = re.sub(r'([a-z])\1\1+', r'\1\1', word)
        word = ' '.join(word)
        word = re.sub(r'([bcdgjptsk]) h', r'\1h', word)
        word_feats = ngram_context(word.split(), n=4)
        t_word = self.predict(word_feats, k_best)
        if self.target != 'urd':
            if self.decode == 'viterbi':
                t_word = self.handle_matra(t_word)
                t_word = self.wx_process(t_word)
            else:
                t_word = [self.handle_matra(w) for w in t_word]
                t_word = [self.wx_process(w) for w in t_word]
        if self.build_lookup:
            self.lookup[oword] = t_word
        return t_word


class Urd2Target(BaseTransliterator):
    """Transliterate text from Persio-Arabic to Indic script"""
    def __init__(self, source, target, decoder, build_lookup=False):
        super(Urd2Target, self).__init__(source,
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
        oword = word
        if not word:
            return ''
        elif word[0] not in self.letters:
            return word.translate(self.punkt_tbl)
        if oword in self.lookup:
            if self.target == 'eng':
                return self.lookup[oword]
            if self.decode == 'viterbi':
                return self.wx_process(self.lookup[oword])
            else:
                return [self.wx_process(w) for w in self.lookup[oword]]
        word = ' '.join(word)
        word = word.replace(' \u06be', '\u06be')
        word_feats = ngram_context(word.split(), n=4)
        t_word = self.predict(word_feats, k_best)
        if self.target != 'eng':
            if self.decode == 'viterbi':
                t_word = self.wx_process(t_word)
            else:
                t_word = [self.wx_process(w) for w in t_word]
        if self.build_lookup:
            self.lookup[oword] = t_word
        return t_word


class Ind2IndRB():
    """Transliterates text bewteen Indic scripts"""
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.get_wx = WX(order='utf2wx', lang=self.source).utf2wx
        self.get_utf = WX(order='wx2utf', lang=self.target).wx2utf
        self.esc_ch = '\x00'  # escape-sequence for Roman in WX
        self.mask_roman = re.compile(r'([a-zA-Z]+)')
        self.non_alpha = re.compile(r"([^a-zA-Z%s]+)" % (self.esc_ch))

    def _to_ben(self, text):
        if self.target != 'ben':
            return text
        text = text.replace('Y', '')
        text = text.replace('v', 'b')
        text = re.sub(r'([oe])([^V])', r'\1V\2', text)
        return text

    def _to_guj(self, text):
        if self.target != 'guj':
            return text
        if self.source == 'ori':
            return text
        text = text.replace('V', '')
        text = re.sub(r'([^lOE])Y', r'\1', text)
        return text

    def _to_kan(self, text):
        if self.target != 'kan':
            return text
        if self.source in ('mal', 'tam'):
            return text
        text = text.replace('z', 'M')
        if self.source == 'hin':
            text = re.sub(r'([^lrY])Y', r'\1', text)
        return text

    def _to_mal(self, text):
        if self.target != 'mal':
            return text
        if self.source in ('tam', 'tel'):
            return text
        text = text.replace('Z', '')
        if self.source == 'kan':
            return text
        text = text.replace('z', 'M')
        if self.source in ('ori', 'pan', 'ben'):
            return text
        text = re.sub(r'([^lrY])Y', r'\1', text)
        return text

    def _to_ori(self, text):
        if self.target != 'ori':
            return text
        text = text.replace('V', '')
        text = text.replace('v', 'b')
        if self.source in ('kan', 'ben', 'pan'):
            return text
        text = re.sub(r'([^l])Y', r'\1', text)
        return text

    def _to_tam(self, text):
        if self.target != 'tam':
            return text
        text = text.replace('Z', '')
        text = text.replace('J', 'j')
        text = text.replace('q', 'ru')
        text = re.sub(r'[CS]', r'c', text)
        text = re.sub(r'[zM]', r'f', text)
        text = re.sub(r'[bBP]', r'p', text)
        text = re.sub(r'[dDT]', r't', text)
        text = re.sub(r'[gGK]', r'k', text)
        text = re.sub(r'[xXW]', r'w', text)
        if self.source in ('guj', 'hin'):
            text = re.sub(r'([^nrlY])Y', r'\1', text)
        return text

    def _to_tel(self, text):
        if not self.target == 'tel':
            return text
        text = text.replace('Z', '')
        if self.source in ('ori', 'pan', 'ben'):
            return text
        text = re.sub(r'([^lr])Y', r'\1', text)
        if self.source == 'hin':
            text = text.replace('z', 'M')
        return text

    def apply_rules(self, text):
        if self.source == 'pan':
            # remove Punjabi Addak
            text = text.replace('\u0a71', '')
        elif self.source == 'ben':
            # Assamese `ra` to Bengali `ra`
            text = text.replace('\u09f0', '\u09b0')
            # Assamese `va` to Bengali `va`
            text = text.replace('\u09f1', '\u09ac')
        text = self._to_ben(text)
        text = self._to_guj(text)
        text = self._to_kan(text)
        text = self._to_mal(text)
        text = self._to_ori(text)
        text = self._to_tam(text)
        text = self._to_tel(text)
        return text

    def rtrans(self, text):
        """Rule based transliteration b/w Indic scripts."""
        target = []
        text = self.mask_roman.sub(r'%s\1' % (self.esc_ch), text)
        text = text.split('\n')
        for sent in text:
            sent = self.non_alpha.split(sent)
            t_sent = str()
            for word in sent:
                if not word:
                    continue
                if word[0] == self.esc_ch:
                    t_sent += word[1:]
                    continue
                wx = self.get_wx(word)
                wx = self.apply_rules(wx)
                t_sent += self.get_utf(wx)
            target.append(t_sent)
        return '\n'.join(target)
