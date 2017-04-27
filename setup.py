#!/usr/bin/env python

import os

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

import numpy


os.environ['PBR_VERSION'] = '1.2.3'
os.environ['SKIP_WRITE_GIT_CHANGELOG'] = '1'
os.environ['SKIP_GENERATE_AUTHORS'] = '1'


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
    ),
    Extension(
        "indictrans._utils.ctranxn",
        [
            "indictrans/_utils/ctranxn.pyx"
        ],
        include_dirs=[numpy.get_include()]
    ),
    Extension(
        "indictrans._utils.sparseadd",
        [
            "indictrans/_utils/sparseadd.pyx"
        ],
        include_dirs=[numpy.get_include()]
    )

]

setup(
    setup_requires=['pbr'],
    pbr=True,
    ext_modules=cythonize(extensions)
)
