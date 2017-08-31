#!/bin/python3

from __future__ import print_function
import ventilator_data
import sys
import codecs

time = ventilator_data.time

flags = [
    '--standard-preprocess',
    '--convert-to-csv',
    '--strip-headers',
    '--remove-empty-datapoints',
    '--reformat-hours',
    '--calc-plateau-pressure',
    '--help'
]
arguments = []
helpstr = """Usage:
    preprocess.py <input-file> <output-file> [options]

Options:
    --help
        Prints out this help page and exits.
    --standard-preprocess
        Runs all the preprocessing steps. If you are
        unsure as to which flags to specify, this is 
        the one you most likely want. Equivalent to
        specifying --convert-to-csv, --strip-headers,
        --remove-empty-datapoints, --reformat-hours,
        and --calc-plateau-pressure.
    --convert-to-csv
        Indicates that the input file should be converted
        from the .si format into a .csv format. This step
        must be done before all other steps can be carried
        out.
    --strip-headers
        Causes the script to remove all lines that give 
        information on the machine doing the ventilation
        or information on pre-use tests.
    --remove-empty-datapoints
        Causes the script to remove all time points which
        do not have any associated data values.
    --reformat-hours
        Causes the script to reformat the time values from
        time of day to time since start of ventilation.
    --calc-plateau-pressure
        Adds an extra column to the output that calculates
        the plateau pressure from the tidal volume, static
        compliance and PEEP. The calculated results are 
        generally more accurate than the plateau pressure
        values that are recorded by the machine.
"""

spec_with_standard_error = """Warning:
    %s was specified with --standard-preprocess.
    --standard-preprocess implies %s.
"""

def is_one_of(val, possible):
    for p in possible:
        if val == p:
            return True
    return False

def parse_args(argv):
    result = {}

    params = [x for x in filter(lambda x: not x.startswith('--'), argv)]
    args = [x for x in filter(lambda x: x.startswith('--'), argv)]

    kwargs = [x for x in map(lambda x: x.split('=', 1), filter(lambda arg: arg.count('=') != 0, args))]
    nargs = [x for x in filter(lambda arg: arg.count('=') == 0, args)]

    for argtype in flags:
        result[argtype[2:]] = argtype in nargs

    for arg in nargs:
        if not arg in flags:
            print("WARNING: Unknown flag \"" + arg + "\". Argument will be ignored.")

    for arg in kwargs:
        if not arg[0] in arguments:
            print("WARNING: Unknown argument \"" + arg[0] + "\". Argument will be ignored.")
        else:
            result[arg[0][2:]] = arg[1]

    for i, param in enumerate(params):
        result["arg" + str(i + 1)] = param

    return result
def validate_args(args):
    if args['help']:
        print(helpstr)
        sys.exit(0)
    if not 'arg1' in args:
        print("Error: No input file specified.")
        print(helpstr)
        sys.exit(-1)
    if not 'arg2' in args:
        print("Error: No output file specified.")
        print(helpstr)
        sys.exit(-1)

    if len(args) == 2:
        print("""Warning: 
    No flags were specified! 
    This script will not have any effects.

    Pass --help to the script to see available flags.
""")

    if args['standard-preprocess']:
        for flag in flags[1:]:
            if args[flag[2:]]:
                print(spec_with_standard_error % flag)

def preprocess(
        input, 
        output,
        args):
    result = input

    # Standard preprocess flags
    standard = args['standard-preprocess']
    convert_to_csv = args['convert-to-csv']
    strip_headers = args['strip-headers']
    remove_empty = args['remove-empty-datapoints']
    reformat_hours = args['reformat-hours']
    calc_p_plat = args['calc-plateau-pressure']

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
    args = parse_args(sys.argv[1:])
    validate_args(args)

    with open(args['arg1'], 'r') as input, open(args['arg2'], 'w') as output:
        preprocess(readlines(input), output, args)
