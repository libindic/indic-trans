#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import sys
import codecs
import argparse

from .transliterator import transliterator

__author__ = "Irshad Ahmad Bhat"
__version__ = "1.0"


def main():
    languages = '''hin guj pan ben mal kan tam tel ori eng
                   mar nep bod kok asm'''.split()
    # help messages
    lang_help = "select language (3 letter ISO-639 code) {%s}" % (
        ', '.join(languages))
    # parse command line arguments
    parser = argparse.ArgumentParser(
        prog="indictrans",
        description="Transliterator for Indian Languages including English")
    parser.add_argument('-v',
                        '--vserion',
                        action="version",
                        version="%(prog)s 1.0")
    parser.add_argument(
        '-s',
        '--source',
        dest="source",
        choices=languages,
        default="hin",
        metavar='',
        help="%s" % lang_help)
    parser.add_argument(
        '-t',
        '--target',
        dest="target",
        choices=languages,
        default="eng",
        metavar='',
        help="%s" % lang_help)
    parser.add_argument(
        '-i',
        '--input',
        dest="infile",
        type=str,
        metavar='',
        help="<input-file>")
    parser.add_argument(
        '-o',
        '--output',
        dest="outfile",
        type=str,
        metavar='',
        help="<output-file>")

    args = parser.parse_args()
    if args.source == args.target:
        sys.stderr.write(
            'indictrans: error: source must be different from target\n')
        sys.stderr.write(parser.parse_args(['-h']))

    if args.infile:
        ifp = io.open(args.infile, encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ifp = codecs.getreader('utf8')(sys.stdin.buffer)
        else:
            ifp = codecs.getreader('utf8')(sys.stdin)

    if args.outfile:
        ofp = io.open(args.outfile, mode='w', encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ofp = codecs.getwriter('utf8')(sys.stdout.buffer)
        else:
            ofp = codecs.getwriter('utf8')(sys.stdout)

    # initialize transliterator object
    trn = transliterator(args.source, args.target)

    # transliterate text
    for line in ifp:
        tline = trn.convert(line)
        ofp.write(tline)

    # close files
    ifp.close()
    ofp.close()

if __name__ == "__main__":
    main()
