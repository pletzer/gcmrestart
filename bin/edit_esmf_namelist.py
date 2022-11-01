import argparse
import datetime
import re


def parse_date(str_date):
    m = re.match(r'\s*(\d\d\d\d)\-(\d\d)\-(\d\d)\s+(\d\d):(\d\d):(\d\d)', str_date)
    year, month, day, hour, minute, second = int(m.group(1)), \
                                             int(m.group(2)), \
                                             int(m.group(3)), \
                                             int(m.group(4)), \
                                             int(m.group(5)), \
                                             int(m.group(6))
    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str, help="start date YYYY-MM-DD HH:mm:ss")
    parser.add_argument("--end", type=str, help="end date YYYY-MM-DD HH:mm:ss")
    parser.add_argument("--file", type=str, default='namelist.rc', help="namelist file")
    args = parser.parse_args()

    s = parse_date(args.start)
    e = parse_date(args.end)

    data = {
        'Start': {
            'year': s.year,
            'month': s.month,
            'day': s.day,
            'hour': s.hour,
            'minute': s.minute,
            'second': s.second,
        },
        'Stop': {
            'year': e.year,
            'month': e.month,
            'day': e.day,
            'hour': e.hour,
            'minute': e.minute,
            'second': e.second,
        },
    }

    with open(args.file) as f:

        for line in f.readlines():

            edited_line = line

            # 'Start', 'Stop'
            for x in data:

                for y in 'year', 'month', 'day', 'hour', 'minute', 'second':

                    y_cap = y[0].upper() + y[1:] # year to Year

                    m = re.match(r'^\s*' + x + y_cap + r'\s*\:\s*\d+', line)
                    if m:
                        # edit this line
                        if y == 'year':
                            edited_line = x + y_cap + f': {data[x][y]:04d}\n'
                        else:
                            edited_line = x + y_cap + f': {data[x][y]:02d}\n'
                            break
            
            print(edited_line, end='')


if __name__ == '__main__':
    main()
