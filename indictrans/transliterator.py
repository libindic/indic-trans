#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#Copyright (C) 2016 Irshad Ahmad Bhat

import os
import re
import sys

from .ind2rom import ind_to_rom
from .rom2ind import rom_to_ind

class transliterator():
    def __init__(self, source='hin', target='eng'):
        if source != "eng":
            ir_trans = ind_to_rom(source)
            self.transform = ir_trans.transliterate
        else:
            ri_trans = rom_to_ind(target)
            self.transform = ri_trans.transliterate

    def convert(self, line):
        return self.transform(line)
