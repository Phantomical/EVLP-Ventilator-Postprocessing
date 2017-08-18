from __future__ import print_function
import sys

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
    def __lt__(self, other):
        if self.hours < other.hours:
            return True
        return self.mins < other.mins

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

def get_last_plateau(lines, index):
    for i in range(index, 2, -1):
        ln = lines[i]
        plateau = ln.split(',')[24]
        if len(plateau.strip()) != 0:
            return plateau
    return ""

def sample_data(input, output, timestep = time(1, 0)):
    lines = [ln.rstrip() for ln in input]
    prev = None
    for ln in get_first_n(lines, 2):
        output.write(ln + '\n')
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
            output.write(str.join(',', sections) + '\n')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: get_hourly_data <input_file> <output_file>')
    with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
        sample_data(input, output)
            

