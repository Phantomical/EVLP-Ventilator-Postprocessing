
class fakefile:
    def __init__(self, iter=None):
        if iter == None:
            self.lines = []
        else:
            self.lines = [x for x in iter]

    def __iter__(self):
        return iter(self.lines)

    def write(self, ln):
        self.lines.append(ln)
    def writelines(self, lns):
        self.lines += [x for x in lns]

class time:
    def __init__(self, *args):
        if len(args) == 1:
            vals = args[0].split(':')
            self.hours = int(vals[0])
            self.mins = int(vals[1])
        else:
            self.hours = args[0] + args[1] // 60
            self.mins = args[1] % 60

    def __add__(self, other):
        hrs = self.hours + other.hours
        mns = self.mins + other.mins
        return time(hrs, mns)
    def __sub__(self, other):
        hrs = self.hours - other.hours
        mns = self.mins - other.mins
        while mns < 0:
            mns += 60
            hrs -= 1
        return time(hrs, mns)
    def __str__(self):
        return str(self.hours) + ':' + str(self.mins)
def get_time(ln):
    return time(ln.split(',', 1)[0])
    
def skip_first_n(iter, n):
    cnt = 0
    for v in iter:
        if cnt < n:
            cnt += 1
        else:
            yield v.rstrip()
def get_first_n(iter, n):
    cnt = 0
    for v in iter:
        if cnt < n:
            cnt += 1
            yield v.rstrip()
        else:
            break

# Preprocessing pipeline
def convert_to_csv(input):
    """Convert tabs within the file to commas"""
    for ln in input:
        yield ln.rstrip('\r\n').replace('\t', ',')
def strip_all(input):
    """Remove all lines except table headers
and data values.
    """    
    # There are 20 lines in the header, skip them
    for ln in skip_first_n(input, 20):
        if len(ln) != 0:
            yield ln
        else:
            break
def remove_empty(input):
    """Remove data points with no values"""
    return filter(lambda ln: len(ln.rstrip(',\r\n')) > 5, input)
def reformat_hours(input, first=None):
    """Reformat time to hours since start of EVLP"""
    prev = None
    for ln in get_first_n(input, 2):
        yield ln
    for ln in skip_first_n(input, 2):
        t = get_time(ln)
        if first == None:
            first = t
            prev = first
        while t.hours < prev.hours:
            t.hours += 24
        time_since_start = t - first
        result = str(time_since_start) + ',' + ln.split(',', 1)[1]
        yield results
        prev = t
def calc_plateau_pressure(input):
    """Calculate plateau pressure from tidal volume, static compliance, and PEEP"""
    toappend = [",Plateau Pressure (Calculated)", ",cmH2O"]

    for ln, end in zip(input, toappend):
        yield ln + end
    for ln in skip_first_n(input, 2):
        values = ln.rstrip().split(',')

        if len(values[12]) == 0 or len(values[28]) == 0 or len(values[9]) == 0:
            values.append('')
        else:
            v_t = float(values[12])
            c_stat = float(values[28])
            peep = float(values[9])
            p_plat = v_t / c_stat + peep

            values.append(str(p_plat))

        yield str.join(',', values)

def standard_preprocess(input):
    result = convert_to_csv(input)
    result = strip_all(result)
    result = remove_empty(result)
    result = reformat_hours(result)
    yield calc_plateau_pressure(result)

def find_recruitment_indices(input):
    is_recruitment = False
    rstart = 0
    # Start considering it a recruitment when
    # the inspiratory tidal volume is above 400mL
    cutoff = 400
    for i in range(2, len(input)):
        values = input[i].rstrip().split(',')
        tidal_volume = float(values[12])
        if is_recruitment:
            if tidal_volume < cutoff:
                yield (rstart, i)
                is_recruitment = False
        else:
            if tidal_volume > cutoff:
                rstart = i
                is_recruitment = True

        
