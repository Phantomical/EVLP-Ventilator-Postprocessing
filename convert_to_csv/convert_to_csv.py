from __future__ import print_function
import sys

def convert_line(line : str):
    return line.replace('\t', ',')

def convert_file(filename : str):
    with open(filename, "r") as f:
        for ln in f:
            yield convert_line(ln.rstrip())

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: convert_to_csv.py <trend file> <output file>")
        sys.exit(-1)
    with open(sys.argv[2], "w") as output:
        for ln in convert_file(sys.argv[1]):
            output.write(ln + '\n')
            
    


