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

def get_time(ln):
    return time(ln.split(',', 1)[0])

def reformat_hours(input, output):
    first = None
    prev = None
    for ln in get_first_n(input, 2):
        output.write(ln + '\n')
    for ln in skip_first_n(input, 2):
        t = get_time(ln)
        if first == None:
            first = t
            prev = first
        while t.hours < prev.hours:
            t.hours += 24
        time_since_start = t - first
        result = str(time_since_start) + ',' + ln.split(',', 1)[1]
        output.write(result + '\n')
        prev = t

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: reformat_hours.py <input_file> <output_file>')
        sys.exit(-1)
    with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
        reformat_hours(input, output)
    
