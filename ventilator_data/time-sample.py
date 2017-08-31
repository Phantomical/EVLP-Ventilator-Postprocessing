#/bin/python3
import ventilator_data
import sys

time = ventilator_data.time
get_time = ventilator_data.get_time
iterate = ventilator_data.iterate

flags = [
    '--filter-irrelevant',
    '--help'
]
arguments = [
    '--sample-freq',
    '--sample-start',
    '--sample-end',
    '--sample-offset'
]
helpstr = """Usage:
    time-sample.py <input-file> <output-file> [options]

Options:
    --help
        Prints this help page and exits.
    --filter-irrelevant
        Filters out all columns from the output except
        for time, dynamic compliance, mean airway pressure,
        static compliance, and calculated plateau pressure
    --sample-freq=<time>
        Indicates how often to output a datapoint.
    --sample-start=[<time>|recruitment|assessment]
        Indicates when to start sampling data points.
        If recruitment or assessment are given it
        will start sampling after every recruitment
        or assessment and end before the next one.
    --sample-end=[<time>|recruitment|assessment]
        Indicates when to finish sampling data points.
        If recruitment or assessment are specified
        then it overrides the normal handling by
        --sample-start, allowing for sampling started
        on a recruitment to end on an assessment or
        vice-versa.
    --sample-offset=<time>
        Indicates how much to offset the first sample
        from the start point.
"""

def is_time(v):
    try:
        t = time(v)
        return True
    except:
        return False

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

    for arg in arguments:
        if not arg[2:] in result:
            result[arg[2:]] = None

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

    if args['sample-freq'] == None:
        print("Warning: No sample frequency was given! Assuming --sample-freq=1:00")
        args['sample-freq'] = "1:00"
    elif not is_time(args['sample-freq']):
        print("Error: Sampling frequency must be a time value.")
        sys.exit(1)

    if is_one_of(args['sample-start'], ["recruitment", "assessment"]):
        pass
    elif is_time(args['sample-start']):
        pass
    elif args['sample-start'] == None:
        args['sample-start'] = "0:00"
    else:
        print('Error: Sample start must be a time value, "recruitment", or "assessment"')
        sys.exit(1)

    if is_one_of(args['sample-end'], ["recruitment", "assessment"]):
        pass
    elif is_time(args['sample-end']):
        pass
    elif args['sample-end'] == None:
        if is_time(args['sample-start']):
            # This will be fine for at least the next 1000 years
            args['sample-end'] = "8760000:00"   
        else:
            args['sample-end'] = args['sample-start']
    else:
        print('Error: Sample end must be a time value, "recruitment", or "assessment"')
        sys.exit(1)   

    if args['sample-offset'] == None:
        args['sample-offset'] = "0:00"
    elif not is_time(args['sample-offset']):
        print("Error: Sample offset must be a time value")
        sys.exit(1) 
        
def get_next_time(current_time, lines, indices):
    for (start, end) in indices:
        time = get_time(lines[start])
        if current_time < time:
            return start
    return len(lines) - 1

def sample_indices(lines, stride, offset, ind1, ind2):
    for ln in lines[:2]:
        yield ln
    for i in range(len(ind1)):
        start = ind1[i][1]
        end = get_next_time(get_time(lines[start]), lines, ind2)

        current_time = get_time(lines[start]) + offset
        end_time = get_time(lines[end])

        for j in range(start, end):
            time = get_time(lines[j])
            
            if time.hours == current_time.hours and time.mins == current_time.mins:
                yield lines[j]
                current_time = time + stride    
            
def filter_time(start, end, linesseq):
    lines = iterate(linesseq)
    for ln in lines[:2]:
        yield ln
    for ln in filter(lambda ln: start < get_time(ln) and get_time(ln) < end, lines[2:]):
        yield ln

def sample_stride(linesseq, start, stride, offset):
    lines = iterate(linesseq)

    current_time = start + offset

    for ln in lines[:2]:
        yield ln
    for ln in lines[2:]:
        time = get_time(ln)
        if time.hours == current_time.hours and time.mins == current_time.mins:
            yield ln
            current_time = time + stride

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    validate_args(args)

    with open(args['arg1'], 'r') as input, open(args['arg2'], 'w') as output:
        lines = [ln.rstrip() for ln in input]

        recruitments = iterate(ventilator_data.find_recruitment_indices(lines))
        assessments = iterate(ventilator_data.find_assessment_indices(lines))

        start_indices = None
        end_indices = None

        if args['sample-start'] == 'recruitment':
            start_indices = recruitments
        elif args['sample-start'] == 'assessment':
            start_indices = assessments

        if args['sample-end'] == 'recruitment':
            end_indices = recruitments
        elif args['sample-end'] == 'assessment':
            end_indices = assessments

        stride = time(args['sample-freq'])
        offset = time(args['sample-offset'])

        if start_indices != None and end_indices != None:
            lines = sample_indices(lines, stride, offset, start_indices, end_indices)
        elif start_indices != None and end_indices == None:
            lines = sample_indices(lines, stride, offset, start_indices, start_indices)
        elif start_indices == None and end_indices != None:
            lines = sample_indices(lines, stride, offset, end_indices, end_indices)
        
        start_time = time("0:00")
        end_time = time("8740000:00")

        if start_indices == None:
            start_time = time(args['sample-start'])
        if end_indices == None:
            end_time = time(args['sample-end'])

        if start_indices == None and end_indices == None:
            lines = sample_stride(lines, start_time, stride, offset)

        lines = filter_time(start_time, end_time, lines)

        if args['filter-irrelevant']:
            lines = ventilator_data.get_relevant_values(lines)

        lines = iterate(lines)

        for ln in lines:
            output.write(ln + '\n')
            

        
    