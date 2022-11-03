import argparse
import datetime
import glob
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

def get_niter0_from_the_latest_ocn_pickup_file(run_dir: str='./*', type=''):
    files = glob.glob(run_dir + '/pickup' + type + '.*.data')
    files.sort()
    last_file = files[-1]
    niter0 = int(last_file.split('.')[-2])
    return niter0

def replace_nIter0(filename, nIter0):
    pat = re.compile(r'\s+niter0\s*=\s*\d+', re.I)
    with open(filename, 'r') as f:
        for line in f.readlines():
            m = re.match(pat, line)
            if m:
                print(f' nIter0           = {nIter0}.,')
            else:
                print(line, end='')

def get_start_date(run_dir, nIter0):
    pat = re.compile(r'^\s*startDate_1\s*=\s*(\d{8})', re.I)
    with open(run_dir + '/data.cal', 'r') as f:
        for line in f.readlines():
            m = re.match(pat, line)
            if m:
                sd = m.group(1)
                y = int(sd[:4])
                m = int(sd[4:6])
                d = int(sd[6:])
                return datetime.datetime(year=y, month=m, day=d)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str, help="start date YYYY-MM-DD HH:mm:ss")
    parser.add_argument("--file", type=str, default='data', help="input file to edit")
    args = parser.parse_args()

    run_dir = str(Path(args.file).parent)

    # get the latest nIter0 from the restart files
    nIter0_1 = get_niter0_from_the_latest_ocn_pickup_file(run_dir, type='')
    nIter0_2 = get_niter0_from_the_latest_ocn_pickup_file(run_dir, type='_seaice')
    # take the oldest of the two
    nIter0 = min(nIter0_1, nIter0_2)
   
    # print out the data content with the new nIter0
    replace_nIter0(run_dir + '/data', nIter0)

    #sd = get_start_date(run_dir, nIter0)
    #sd2 = parse_date(args.start)
    #assert(sd == sd2)

if __name__ == '__main__':
    main()
