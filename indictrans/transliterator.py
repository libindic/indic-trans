#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Irshad Ahmad Bhat

from .ind2rom import ind_to_rom
from .rom2ind import rom_to_ind


class transliterator():

    def __init__(self, source='hin', target='eng'):
        indic = 'hin guj pan ben mal kan tam tel'.split()
        source = source.lower()
        target = target.lower()
        if source == "eng":
            if target not in indic:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            r2i_trans = rom_to_ind(target)
            self.transform = r2i_trans.transliterate
        elif target == 'eng':
            if source not in indic:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            i2r_trans = ind_to_rom(source)
            self.transform = i2r_trans.transliterate
        else:
            raise NotImplementedError(
                'Language pair `%s-%s` is not implemented.' %
                (source, target))

    def convert(self, line):
        return self.transform(line)
