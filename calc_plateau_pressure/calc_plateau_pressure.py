from __future__ import print_function
import sys

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

def calc_plateau_pressure(input, output):
    output.write(input.readline().rstrip() + ",Plateau Pressure (Calculated)\n")
    output.write(input.readline().rstrip() + ",cmH2O\n")

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

        output.write(str.join(',', values) + '\n')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: calc_plateau_pressure.py <input_file> <output_file>')
        sys.exit(-1)
    with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
        calc_plateau_pressure(input, output)
        