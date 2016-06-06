#!/usr/bin/env python 
# -*- coding: utf-8 -*-

__author__     = "Irshad Ahmad Bhat"
__version__    = "1.0"

import sys
import argparse

from .transliterator import transliterator

def main():
    languages = ["hin", "eng"]
    # help messages
    lang_help = "select language (3 letter ISO-639 code) [hin|eng]"
    # parse command line arguments 
    parser = argparse.ArgumentParser(prog="indictrans", description="Transliterator for Indian Languages including English")
    parser.add_argument('--v', action="version", version="%(prog)s 1.0")
    parser.add_argument('--s', metavar='source', dest="source", choices=languages, default="hin", help="%s" %lang_help)
    parser.add_argument('--t', metavar='target', dest="target", choices=languages, default="eng", help="%s" %lang_help)
    parser.add_argument('--i', metavar='input', dest="INFILE", type=argparse.FileType('r'), default=sys.stdin, help="<input-file>")
    parser.add_argument('--o', metavar='output', dest="OUTFILE", type=argparse.FileType('w'), default=sys.stdout, help="<output-file>")

    args = parser.parse_args()
    if args.source == args.target:
        sys.stderr.write(parser.format_usage())
        sys.stderr.write('indictrans: error: either source and target must be different\n')
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
