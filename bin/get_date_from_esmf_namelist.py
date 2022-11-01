import argparse
import datetime
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--field", choices=['Start', 'Stop'], help="whether toretrieve the Start or Stop date")
    parser.add_argument("--file", type=str, default='namelist.rc', help="namelist file")
    args = parser.parse_args()

    data = {
        'year': None,
        'month': None,
        'day': None,
        'hour': None,
        'minute': None,
        'second': None,
    }

    with open(args.file) as f:

        for line in f.readlines():

            for x in 'year', 'month', 'day', 'hour', 'minute', 'second':

                x_cap = x[0].upper() + x[1:] # year to Year

                m = re.match(r'^\s*' + args.field + x_cap + r'\s*\:\s*(\d+)', line)
                if m:
                    data[x] = int(m.group(1))
                    break

    print(f'{data["year"]:04d}-{data["month"]:02d}-{data["day"]:02d} {data["hour"]:02d}:{data["minute"]:02d}:{data["second"]:02d}')

if __name__ == '__main__':
    main()
