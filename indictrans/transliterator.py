#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Irshad Ahmad Bhat

from ._decode import DECODERS
from .ind2rom import ind_to_rom
from .rom2ind import rom_to_ind


def _get_decoder(decode):
    try:
        return DECODERS[decode]
    except KeyError:
        raise ValueError('Unknown decoder {0!r}'.format(decode))


class transliterator():
    def __init__(self, source='hin', target='eng', decode='viterbi', k_best=5):
        indic = '''hin guj pan ben mal kan tam tel ori
                   mar nep bod kok asm'''.split()
        source = source.lower()
        target = target.lower()
        decoder = (decode, _get_decoder(decode))
        if k_best < 2:
            raise ValueError('`k_best` value should be >= 2')
        if source == "eng":
            if target not in indic:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            r2i_trans = rom_to_ind(target, decoder, k_best)
            if decode == 'viterbi':
                self.transform = r2i_trans.transliterate
            else:
                self.transform = r2i_trans.top_n_trans
        elif target == 'eng':
            if source not in indic:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            i2r_trans = ind_to_rom(source, decoder, k_best)
            if decode == 'viterbi':
                self.transform = i2r_trans.transliterate
            else:
                self.transform = i2r_trans.top_n_trans
        else:
            raise NotImplementedError(
                'Language pair `%s-%s` is not implemented.' %
                (source, target))

    def convert(self, line):
        return self.transform(line)
