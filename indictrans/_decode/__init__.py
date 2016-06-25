# Copyright Irshad Ahmad Bhat 2016.

"""Decoding (inference) algorithms."""

import viterbi
import beamsearch

DECODERS = {"viterbi": viterbi,
            "beamsearch": beamsearch}
