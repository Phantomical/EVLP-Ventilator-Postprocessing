import codecs

class time:
    def __init__(self, *args):
        if len(args) == 1:
            vals = args[0].split(':')
            if (len(vals) < 2):
                self.mins = int(vals)
            else:
                self.hours = int(vals[0])
                self.mins = int(vals[1])
        else:
            self.hours = args[0]
            self.mins = args[1]

        self.hours += self.mins // 60
        self.mins %= 60

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

    def __lt__(self, other):
        if self.hours == other.hours:
            return self.mins < other.mins
        return self.hours < other.hours
def get_time(ln):
    return time(ln.split(',', 1)[0])

def iterate(gen):
    return [x for x in gen]
    
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
def reformat_hours(inputseq, firstval=None):
    """Reformat time to hours since start of EVLP"""
    prev = None
    first = firstval
    input = iterate(inputseq)
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
        yield result
        prev = t
def calc_plateau_pressure(inputseq):
    """Calculate plateau pressure from tidal volume, static compliance, and PEEP"""
    toappend = [",Plateau Pressure (Calculated)", ",cmH2O"]
    input = iterate(inputseq)

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
    return calc_plateau_pressure(result)

def find_recruitment_indices(input, weight=30):
    is_recruitment = False
    rstart = 0
    # Start considering it a recruitment when
    # the inspiratory tidal volume is above the
    # average of target recruitment and recular
    # tidal volumes. 
    # Regular Vt = 7 mL/Kg * weight
    # Recruitment Vt = 15 mL/Kg * weight  
    cutoff = 11 * weight
    inputvals = [x for x in input]
    for i in range(2, len(inputvals)):
        values = inputvals[i].rstrip().split(',')
        tidal_volume = float(values[12])
        if is_recruitment:
            if tidal_volume < cutoff:
                yield (rstart, i)
                is_recruitment = False
        else:
            if tidal_volume > cutoff:
                rstart = i
                is_recruitment = True
def find_assessment_indices(input):
    is_assessment = False
    start = 0
    # Start considering it an assessment when 
    # %O2 is above 80%
    cutoff = 80
    inputvals = [x for x in input]
    for i in range(2, len(inputvals)):
        values = inputvals[i].rstrip().split(',')
        pO2 = float(values[13])
        if is_assessment:
            if pO2 < cutoff:
                yield (start, i)
                is_assessment = False
        else:
            if pO2 > cutoff:
                start = i
                is_assessment = True

def sample_rel(inputseq, find_indices, offset):
    input = iterate(inputseq)

    # Output table headers
    for ln in get_first_n(input, 2):
        yield ln

    vals = input
    for start, end in find_indices(vals):
        # Make sure not to sample data points
        # before the start of the file
        idx = min(max(2, (start if offset < 0 else end) + offset), len(vals))
        yield vals[idx]
def sample_over(inputseq, find_indices):
    input = iterate(inputseq)

    # Output table headers
    for ln in get_first_n(input, 2):
        yield ln

    vals = [x for x in input]

    for start, end in find_indices(vals):
        for val in vals[start:end]:
            yield val

def sample_prerecruitment(inputseq):
    return sample_rel(inputseq, find_recruitment_indices, -2)
def sample_postrecruitment(inputseq):
    return sample_rel(inputseq, find_recruitment_indices, 2)
def sample_over_recruitment(input):
    return sample_over(input, find_recruitment_indices)

def get_last_plateau(lines, index):
    for i in range(index, 2, -1):
        ln = lines[i]
        plateau = ln.split(',')[24]
        if len(plateau.strip()) != 0:
            return plateau
    return ""
def sample_data(input, timestep=time(1,0)):
    lines = [ln.rstrip() for ln in input]
    prev = None
    for ln in get_first_n(lines, 2):
        yield ln
    for i in range(2, len(lines)):
        ln = lines[i]
        t = get_time(ln)
        
        # Initialize prev
        if prev == None:
            prev = t

        sections = ln.split(',')
        diff = t - prev
        if not diff < timestep:
            prev = t
            last_plateau = get_last_plateau(lines, i)
            sections[24] = last_plateau
            yield str.join(',', sections)
def remove_extra_datapoints(inputseq, minstep=time(0,30)):
    input = iterate(inputseq)

    # Output table headers
    for ln in get_first_n(input, 2):
        yield ln

    prev = None
    
    for val in skip_first_n(input, 2):
        t = get_time(val)

        if prev == None:
            prev = t
            yield val
        elif not t < prev + minstep:
            yield val

def get_relevant_values(input):
    for ln in input:
        vals = ln.rstrip().split(',')
        relevant = [
            vals[0],  # Time
            vals[6],  # Dynamic Compliance
            vals[19], # Mean Airway Pressure
            vals[25], # Peak Airway Pressure
            vals[28], # Static Compliance
            vals[37]  # Plateau Pressure (Calculated)
        ]
        yield str.join(',', relevant)

def reformat_time(linesseq):
    lines = iterate(linesseq)
    for ln in lines[:2]:
        yield ln
    for ln in lines[2:]:
        vals = ln.rstrip().split(',')
        t = time(vals[0])
        vals[0] = str(float(t.hours) + float(t.mins) / 60.0)
        yield str.join(',', vals)

