import argparse
import datetime
import re
from pathlib import Path

def parse_date(str_date):
    m = re.match(r'\s*(\d\d\d\d)\-(\d\d)\-(\d\d)_(\d\d)_(\d\d)_(\d\d)', str_date)
    if not m:
        msg = f"ERROR dtae {str_date} does not match pattern '\s*(\d\d\d\d)\-(\d\d)\-(\d\d)\s+(\d\d):(\d\d):(\d\d)'"
        raise RuntimeError(msg)
    year, month, day, hour, minute, second = int(m.group(1)), \
                                             int(m.group(2)), \
                                             int(m.group(3)), \
                                             int(m.group(4)), \
                                             int(m.group(5)), \
                                             int(m.group(6))
    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

def get_num_minutes(run_dir, dt):
    pat = re.compile(r'^\s*startDate_1\s*=\s*(\d{8})')
    with open(run_dir + '/data.cal', 'r') as f:
        for line in f.readlines():
            m = re.match(pat, line)
            if m:
                date = m.group(1)
                year = int(date[:4])
                month = int(date[4:6])
                day = int(date[6:])
                d0 = datetime.datetime(year=year, month=month, day=day)
                delta_t = dt - d0
                return int(delta_t.total_seconds() / 60) # minutes
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default='', help="date in YYYY-MM-DD_HH_mm_ss format")
    parser.add_argument("--run_dir", type=str, default='', help="run directory")
    args = parser.parse_args()
    dt = parse_date(args.date)

    # get the number of minutes since date in data.cal
    n = get_num_minutes(args.run_dir, dt)

    for sfx in "meta", "data":
        for prfx in "pickup", "pickup_seaice":
            filename = f'{args.run_dir}/{prfx}.{n:010d}.{sfx}'
            print(filename)
            Path(filename).touch()


if __name__ == '__main__':
    main()
