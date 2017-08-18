from __future__ import print_function
import sys

def is_data_line(line):
    return len(line.rstrip(',\r\n')) > 5

def remove_dataless(lines):
    return filter(is_data_line, lines)

def remove_empty(input, output):
    output.writelines(remove_dataless(input))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: remove_empty.py <input_file> <output_file>')
        sys.exit(-1)
    with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
        remove_empty(input, output)
        
