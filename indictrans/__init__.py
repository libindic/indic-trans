#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

from .transliterator import transliterator

__author__ = "Irshad Ahmad Bhat"
__version__ = "1.0"


def main():
    languages = 'hin ben guj pan mal kan tam tel eng'.split()
    # help messages
    lang_help = "select language (3 letter ISO-639 code) [%s]" % (
        '|'.join(languages))
    # parse command line arguments
    parser = argparse.ArgumentParser(
        prog="indictrans",
        description="Transliterator for Indian Languages including English")
    parser.add_argument('--v', action="version", version="%(prog)s 1.0")
    parser.add_argument(
        '--source',
        dest="source",
        choices=languages,
        default="hin",
        help="%s" % lang_help)
    parser.add_argument(
        '--target',
        dest="target",
        choices=languages,
        default="eng",
        help="%s" % lang_help)
    parser.add_argument(
        '--input',
        dest="INFILE",
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="<input-file>")
    parser.add_argument(
        '--ootput',
        dest="OUTFILE",
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="<output-file>")

    args = parser.parse_args()
    if args.source == args.target:
        sys.stderr.write(parser.format_usage())
        sys.stderr.write(
            'indictrans: error: source must be different from target\n')
        sys.exit(0)

    # initialize transliterator object
    trn = transliterator(args.source, args.target)

    # transliterate text
    for line in args.INFILE:
        tline = trn.convert(line)
        args.OUTFILE.write(tline)

    # close files
    args.INFILE.close()
    args.OUTFILE.close()

if __name__ == "__main__":
    main()
