#import f90nml
from pathlib import Path
import datetime
import glob
import os.path
import re

class RestartTimeFinder(object):

    def __init__(self, top_dir : Path='./'):
        self.top_dir = top_dir

    def getAtmRestartTime(self):
        atm_restart_files = glob.glob(str(self.top_dir) + '/wrfrst_d01_*')
        atm_restart_files.sort()
        fname = os.path.basename(atm_restart_files[-1])
        _a, _b, year_month_day, hour, minute, second = fname.split('_')
        year, month, day = year_month_day.split('-')
        dt = datetime.datetime(year=int(year), month=int(month), day=int(day),
            hour=int(hour), minute=int(minute), second=int(second))
        return dt

    def getStartTime(self):

        with open(self.top_dir + '/namelist.rc') as f:
            data = {
                'year': None,
                'month': None,
                'day': None,
                'hour': None,
                'minute': None,
                'second': None
            }
            for line in f.readlines():
                if not re.match(r'^\s*Start', line):
                    continue
                for u in 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second':
                    m = re.match(r'^\s*Start' + u + r'\s*:\s*([0-9]+)', line)
                    if m:
                        data[u.lower()] = int(m.group(1))
            return datetime.datetime(**data)


    def getOcnRestartTime(self):
        ocn_restart_files = glob.glob(str(self.top_dir) + '/pickup.[0-9]*.meta')
        ocn_restart_files.sort()
        fname = os.path.basename(ocn_restart_files[-1])
        minutes_from_start = int(fname.split('.')[1])
        return self.getStartTime() + datetime.timedelta(minutes=minutes_from_start)


##################################################################################
def test():
    top_dir = '/nesi/nobackup/pletzera/workflow_restart_capability/runCase_NESI'
    rtf = RestartTimeFinder(top_dir)
    print(f'start_time: {rtf.getStartTime()}')
    print(f'atm restart: {rtf.getAtmRestartTime()}')
    print(f'ocn restart: {rtf.getOcnRestartTime()}')


if __name__ == '__main__':
    test()
