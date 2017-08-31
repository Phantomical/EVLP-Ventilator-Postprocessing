#!/bin/python3

from __future__ import print_function
import ventilator_data
import sys
import codecs

time = ventilator_data.time

def spec_with_standard(switch):
    return "Warning: %s specified in addition to --standard-preprocessor. %s will be ignored!" % switch
def conflicting_argument(arg1, arg2):
    return "Warning: " + arg1 + " specified in addition to " + arg2 + ". " + arg2 + " will be ignored!";

def preprocess(
        input, 
        output,
        args):
    result = input

    # Standard preprocess flags
    standard = (args.count("--standard-preprocess") + args.count("-s")) != 0
    convert_to_csv = args.count("--convert-to-csv") != 0
    strip_headers = args.count('--strip-headers') != 0
    remove_empty = args.count('--remove-empty-datapoints') != 0
    reformat_hours = args.count('--reformat-hours') != 0
    calc_p_plat = args.count('--calc-plateau-pressure') != 0

    if standard:
        result = ventilator_data.standard_preprocess(result)

        if convert_to_csv: print(spec_with_standard('--convert-to-csv'))
        if strip_headers: print(spec_with_standard('--strip-headers'))
        if reformat_hours: print(spec_with_standard('--reformat-hours'))
        if calc_p_plat: print(spec_with_standard('--calc-plateau-pressure'))
        if remove_empty: print(spec_with_standard('--remove-empty'))
    else:
        if convert_to_csv:
            result = ventilator_data.convert_to_csv(result)
        if strip_headers:
            result = ventilator_data.strip_all(result)
        if remove_empty:
            result = ventilator_data.remove_empty(result)
        if reformat_hours:
            result = ventilator_data.reformat_hours(result)
        if calc_p_plat:
            result = ventilator_data.calc_plateau_pressure(result)
   
    result = filter(lambda ln: len(ln.rstrip()) != 0, result)

    for ln in result:
        output.write(ln + '\n')

def readlines(input):
    contents = input.read().split('\n')
    return contents

if __name__ == '__main__':
    args = sys.argv[1:]
    flags = []
    input = None    
    output = None

    try:
        for arg in args:
            if arg.startswith('-'):
                flags.append(arg)
            else:
                if input == None:
                    input = open(arg, "r")
                else:
                    output = open(arg, 'w')

        if input == None:
            print("Error: No input file provided")
            sys.exit(-1)
        if output == None:
            print("Error: No input file provided")
            sys.exit(-1)

        preprocess(readlines(input), output, flags)
    except:
        if input != None:
            input.close()
        if output != None:
            output.close()
        raise
