import ventilator_data
import sys
from functools import partial

flags = [
    '--filter-irrelevant',
    '--help'
]
arguments = [
    '--sample-param',
    '--sample-period',
    '--sample-offset',
    '--subject-weight'
]
helpstr = """Usage:
    sample.py <input-file> <output-file> [options]

Options:
    --help
        Prints this help page and exits.
    --filter-irrelevant
        Filters out all columns from the output except
        for time, dynamic compliance, mean airway pressure,
        static compliance, and calculated plateau pressure
    --sample-period=[pre|post|during]
        Indicates whether to sample before the recruitment/
        assessment, during it, or after it.
    --sample-param=[recruitment|assessment]
        Indicates whether to sample around recruitments or
        assessments.
    --sample-offset=<time>
        Indicates how long before or after recruitment/assessment
        to sample. <time> is in minutes.
    --subject-weight=<weight-in-kg>
        For pigs this is the weight of the subject in kg. For human
        subjects this should be the Ideal Body Weight. (This is not
        tested for human use)
"""

time = ventilator_data.time

def is_one_of(val, possible):
    for p in possible:
        if val == p:
            return True
    return False
def is_float(v):
    try:
        i = float(v)
        return True
    except:
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
    if not 'arg1' in args:
        print(helpstr)
        sys.exit(-1)
    if not 'arg2' in args:
        print(helpstr)
        sys.exit(-1)
    if args['help']:
        print(helpstr)
        sys.exit(0)

    if not 'sample-param' in args:
        args['sample-param'] = 'recruitment'
        print("Warning: --sample-param was not specified. Using 'recruitment' as sample parameter.")
    
    if not 'sample-period' in args:
        args['sample-period'] = 'pre'
        print("Warning: --sample-period was not specified. Using 'pre' as sample period.")
        
    if args['sample-period'] == 'during':
        if 'sample-offset' in args:
            print('Warning: --sample-offset specified with --sample-period=during. --sample-offset will be ignored.')
    elif not 'sample-offset' in args:
        args['sample-offset'] = "2"

    if not 'subject-weight' in args:
        args['subject-weight'] = "30"
        print("Warning: No subject weight given. Using 30kg as default.")
    elif args['subject-weight'] == None:
        args['subject-weight'] = "30"
        print("Warning: No subject weight given. Using 30kg as default.")
    elif not is_float(args['subject-weight']):
        print("Error: Subject weight was not a recognisable number.")
        sys.exit(1)

    if not is_one_of(args['sample-param'], ['recruitment', 'assessment']):
        print('Error: Invalid argument passed to --sample-param. Expected one either "recruitment" or "assessment".')
    if not is_one_of(args['sample-period'], ['pre', 'post', 'during']):
        print('Error: Invalid argument passed to --sample-period. Expected "pre", "post", or "during".')
def bind_method(func, arg):
    def revargs(f, a, b):
        return f(b, a)
    return partial(revargs, func, arg)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    validate_args(args)

    find_indices = None
    if args['sample-param'] == 'recruitment':
        find_indices = bind_method(ventilator_data.find_recruitment_indices, args['subject-weight'])
    elif args['sample-param'] == 'assessment':
        find_indices = ventilator_data.find_assessment_indices

    with open(args['arg1'], "r") as input, open(args['arg2'], 'w') as output:
        result = [ln.rstrip() for ln in input]
        
        if args['sample-period'] == 'pre':
            result = ventilator_data.sample_rel(result, find_indices, -int(args['sample-offset']))
            result = ventilator_data.remove_extra_datapoints(result, time(0, 45))
        elif args['sample-period'] == 'post':
            result = ventilator_data.sample_rel(result, find_indices, int(args['sample-offset']))
            result = ventilator_data.remove_extra_datapoints(result, time(0, 45))
        elif args['sample-period'] == 'during':
            result = ventilator_data.sample_over(result, find_indices)

        if args['filter-irrelevant']:
            result = ventilator_data.get_relevant_values(result)

        for ln in result:
            output.write(ln + '\n')
