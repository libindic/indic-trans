# Copyright Irshad Ahmad Bhat 2016.

"""Decoding (inference) algorithms."""

from indictrans._decode import viterbi
from indictrans._decode import beamsearch

DECODERS = {"viterbi": viterbi,
            "beamsearch": beamsearch}
