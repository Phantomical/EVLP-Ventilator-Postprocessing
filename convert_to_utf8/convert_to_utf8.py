#!/bin/python3

from __future__ import print_function

import sys
import codecs

def convert_file(inputfile, outputfile, encoding):
    with codecs.open(inputfile, 'rb', encoding) as source:
        with codecs.open(outputfile, 'wb', 'utf-8') as target:
            while True:
                contents = source.readline().replace('₂', '2')
                if not contents:
                    break
                target.write(contents)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: convert_to_utf8.py <input_file> <output_file>')
        sys.exit(-1)
    convert_file(sys.argv[1], sys.argv[2], 'utf_16_le')
