#!/usr/bin/env python

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize


extensions = [
    Extension(
        "indictrans._decode.beamsearch",
        [
            "indictrans/_decode/beamsearch.pyx"
        ]
    ),
    Extension(
        "indictrans._decode.viterbi",
        [
            "indictrans/_decode/viterbi.pyx"
        ]
    )

]

setup(
    setup_requires=['pbr'],
    pbr=True,
    ext_modules=cythonize(extensions)
)
