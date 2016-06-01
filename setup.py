#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import warnings
from setuptools import setup, Extension
from Cython.Distutils import build_ext

dist_dir = os.path.dirname(os.path.abspath(__file__))
os.system("gunzip -kf %s/indictrans/models/* 2> /dev/null" %dist_dir)

try:
    import py2exe
except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        print("Cannot import py2exe", file=sys.stderr)
        exit(1)

py2exe_options = {
    "bundle_files": 1,
    "compressed": 1,
    "optimize": 2,
    "dist_dir": '.',
    "dll_excludes": ['w9xpopen.exe'],
}

py2exe_console = [{
    "script": "./indictrans/__main__.py",
    "dest_base": "indictrans",
}]

py2exe_params = {
    'console': py2exe_console,
    'options': {"py2exe": py2exe_options},
    'zipfile': None
}

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    params = py2exe_params
else:
    files_spec = [
        ('share/doc/indictrans', ['README.rst'])
    ]
    root = os.path.dirname(os.path.abspath(__file__))
    data_files = []
    for dirname, files in files_spec:
        resfiles = []
        for fn in files:
            if not os.path.exists(fn):
                warnings.warn('Skipping file %s since it is not present. Type  make  to build all automatically generated files.' % fn)
            else:
                resfiles.append(fn)
        data_files.append((dirname, resfiles))

    params = {
        'data_files': data_files,
    }
    params['entry_points'] = {'console_scripts': ['indictrans = indictrans:main']}

# Get the package version
exec(compile(open('indictrans/version.py').read(),
             'indictrans/version.py', 'exec'))

setup(
    name = "indictrans",
    version = __version__,
    description="Transliteration Tool: Transliterator for Indian languages including English",
    long_description = open('README.rst', 'rb').read().decode('utf8'),
    keywords = ['Language Transliteration', 'Computational Linguistics', 
		'Indic', 'Roman'],
    author='Irshad Ahmad',
    author_email='irshad.bhat@research.iiit.ac.in',
    maintainer='Irshad Ahmad',
    maintainer_email='irshad.bhat@research.iiit.ac.in',
    license = "MIT",
    url="https://github.com/irshadbhat/indictrans",
    package_dir={"indictrans":"indictrans"},
    packages=['indictrans', 'indictrans._utils', 'indictrans._decode'],
    package_data={'indictrans': ['models/*.npy', 'models/*.vec']},

    classifiers=[
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Operating System :: Unix"
    ],
    cmdclass={'build_ext': build_ext},
    ext_modules=[
        Extension("indictrans._decode.viterbi", ["indictrans/_decode/viterbi.pyx"]),
    ],
    install_requires=["cython", "numpy", "scipy"],
    #requires=["cython", "numpy", "scipy"],
    **params
)
