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
        'start': {
            'year': s.year,
            'month': s.month,
            'day': s.day,
            'hour': s.hour,
        },
        'end': {
            'year': e.year,
            'month': e.month,
            'day': e.day,
            'hour': e.hour,
        },
    }

    with open(args.file) as f:

        for line in f.readlines():

            edited_line = line

            # 'start', 'end'
            for x in data:

                for y in 'year', 'month', 'day', 'hour':

                    m = re.match(r'^\s*' + x + '_' + y + r'\s*=\s*\d+', line)
                    if m:
                        # edit this line
                        if y == 'year':
                            edited_line = x + '_' + y + f' = {data[x][y]:04d},\n'
                        else:
                            edited_line = x + '_' + y + f' = {data[x][y]:02d},\n'
                            break

            m = re.match(r'^\s*restart\s*=', line)
            if m:
                edited_line = ' restart = .true.,\n'

            print(edited_line, end='')



if __name__ == '__main__':
    main()
