#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Irshad Ahmad Bhat

from ._decode import DECODERS
from .script_transliterate import (Ind2Target, Rom2Target,
                                   Urd2Target, Ind2IndRB)


def _get_decoder(decode):
    try:
        return DECODERS[decode]
    except KeyError:
        raise ValueError('Unknown decoder {0!r}'.format(decode))


def _get_trans(trans, decode):
    if decode == 'viterbi':
        return trans.transliterate
    else:
        return trans.top_n_trans


class Transliterator():
    """Transliterator for Indic scripts including English and Urdu.

    Parameters
    ----------

    source : str, default: hin
        Source Language (3 letter ISO-639 code)

    target : str, default: eng
        Target Language (3 letter ISO-639 code)

    decode : str, default: viterbi
        Decoding algorithm, either ``viterbi`` or ``beamsearch``.

    build_lookup : bool, default: False
        Flag to build lookup-table. Fastens the transliteration
        process if the input text contains repeating words.

    rb : bool, default: True
        Decides whether to use rule-based system or ML system for
        transliteration. This choice is only for Indic to Indic
        transliterations. If ``True`` uses ruled-based one.

    Examples
    --------

    >>> from indictrans import Transliterator
    >>> trn = Transliterator(source='hin', target='eng', build_lookup=True)
    >>> hin = '''कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमंत्री
    ... जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक
    ... समानता है. ये सभी अलग-अलग कारणों से भारतीय जनता पार्टी के
    ... राज्यसभा सांसद सुब्रमण्यम स्वामी के निशाने पर हैं. उनके
    ... जयललिता और सोनिया गांधी के पीछे पड़ने का कारण कथित
    ... भ्रष्टाचार है.'''
    >>> eng = trn.transform(hin)
    >>> print(eng)
    congress party adhyaksh sonia gandhi, tamilnadu kii mukhyamantri
    jayalalita our reserve baink ke governor raghuram rajan ke beech ek
    samanta hai. ye sabi alag-alag carnon se bharatiya janata party ke
    rajyasabha saansad subramanyam swami ke nishane par hain. unke
    jayalalita our sonia gandhi ke peeche padane ka kaaran kathith
    bhrashtachar hai.
    """
    def __init__(self, source='hin', target='eng', decode='viterbi',
                 build_lookup=False, rb=True):
        source = source.lower()
        target = target.lower()
        impl = '''hin guj pan ben mal kan tam tel
                  ori mar nep kok bod asm eng urd'''.split()
        decoder = (decode, _get_decoder(decode))
        if source in ['eng', 'urd']:
            if target not in impl or source == target:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            if source == 'eng':
                ru2i = Rom2Target(source, target, decoder, build_lookup)
            else:
                ru2i = Urd2Target(source, target, decoder, build_lookup)
            self.transform = _get_trans(ru2i, decode)
        elif target in ['eng', 'urd']:
            if source not in impl or source == target:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            i2o = Ind2Target(source, target, decoder, build_lookup)
            self.transform = _get_trans(i2o, decode)
        else:
            if source not in impl or target not in impl or source == target:
                raise NotImplementedError(
                    'Language pair `%s-%s` is not implemented.' %
                    (source, target))
            if rb:
                self.transform = Ind2IndRB(source, target).rtrans
            else:
                i2i = Ind2Target(source, target, decoder, build_lookup)
                self.transform = _get_trans(i2i, decode)

    def convert(self, line):
        return self.transform(line)
