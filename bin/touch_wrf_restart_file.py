import argparse
import datetime
import re
from pathlib import Path

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
    parser.add_argument("--date", type=str, default='', help="date in YYYY-MM-DD HH:mm:ss format")
    parser.add_argument("--run_dir", type=str, default='', help="run directory")
    args = parser.parse_args()
    dt = parse_date(args.date)
    filename = f'{args.run_dir}/wrfrst_d01_{dt.year:04d}-{dt.month:02d}-{dt.day:02d}_{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}'
    Path(filename).touch()


if __name__ == '__main__':
    main()
