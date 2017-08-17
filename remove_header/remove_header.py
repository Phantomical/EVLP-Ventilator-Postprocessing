from __future__ import print_function
import sys

def strip_header(input):
    # Number of lines in header
    header_size = 20
    ctr = 0
    for ln in input:
        if ctr < header_size:
            ctr += 1
        else:
            yield ln.rstrip()

def strip_all(inputfile):
    for ln in strip_header(inputfile):
        if len(ln) != 0:
            yield ln
        else:
            break

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: remove_header <input_file> <output_file>')
        sys.exit(-1)
    with open(sys.argv[2], 'w') as output, open(sys.argv[1], 'r') as input:
        for ln in strip_all(input):
            print(ln)
            output.write(ln + '\n')
        

