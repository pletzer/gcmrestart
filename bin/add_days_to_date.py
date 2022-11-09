import argparse
import datetime
import re

def parse_date(str_date):
    m = re.match(r'^\s*(\d\d\d\d)\-(\d\d)\-(\d\d)\s+(\d\d):(\d\d):(\d\d)', str_date)
    if not m:
        msg = f'ERROR: "{str_date}" does not satisfy pattern "^\s*(\d\d\d\d)\-(\d\d)\-(\d\d)\s+(\d\d):(\d\d):(\d\d)"'
        raise RuntimeError(msg)

    year, month, day, hour, minute, second = int(m.group(1)), \
                                             int(m.group(2)), \
                                             int(m.group(3)), \
                                             int(m.group(4)), \
                                             int(m.group(5)), \
                                             int(m.group(6))
    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=0, help="number of days to add")
    parser.add_argument("--date", type=str, default='', help="date in YYYY-MM-DD HH:mm:ss format")
    args = parser.parse_args()
    dt = parse_date(args.date)
    dt += datetime.timedelta(days=args.days)
    print(f'{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}')


if __name__ == '__main__':
    main()
