#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Irshad Ahmad Bhat

from ._decode import DECODERS
from .script_trans import (Ind2RU, Rom2Ind, Urd2Ind)


def _get_decoder(decode):
    try:
        return DECODERS[decode]
    except KeyError:
        raise ValueError('Unknown decoder {0!r}'.format(decode))


class transliterator():
    def __init__(
                self,
                source='hin',
                target='eng',
                decode='viterbi',
                build_lookup=False):
        indic = '''hin guj pan ben mal kan tam tel
                ori mar nep bod kok asm'''.split()
        source = source.lower()
        target = target.lower()
        decoder = (decode, _get_decoder(decode))
        if source in ['eng', 'urd']:
            if target not in indic:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            if source == 'eng':
                ru2i_trans = Rom2Ind(source, target, decoder, build_lookup)
            else:
                ru2i_trans = Urd2Ind(source, target, decoder, build_lookup)
            if decode == 'viterbi':
                self.transform = ru2i_trans.transliterate
            else:
                self.transform = ru2i_trans.top_n_trans
        elif target in ['eng', 'urd']:
            if source not in indic:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            i2o_trans = Ind2RU(source, target, decoder, build_lookup)
            if decode == 'viterbi':
                self.transform = i2o_trans.transliterate
            else:
                self.transform = i2o_trans.top_n_trans
        else:
            raise NotImplementedError(
                'Language pair `%s-%s` is not implemented.' %
                (source, target))

    def convert(self, line):
        return self.transform(line)
