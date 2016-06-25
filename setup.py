#!/usr/bin/env python

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

import numpy


extensions = [
    Extension(
        "indictrans._decode.beamsearch",
        [
            "indictrans/_decode/beamsearch.pyx"
        ],
        include_dirs=[numpy.get_include()]
    ),
    Extension(
        "indictrans._decode.viterbi",
        [
            "indictrans/_decode/viterbi.pyx"
        ],
        include_dirs=[numpy.get_include()]
    )

]

setup(
    setup_requires=['pbr'],
    pbr=True,
    ext_modules=cythonize(extensions)
)
