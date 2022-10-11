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

        with open(self.top_dir / 'namelist.rc') as f:
            data = {
                'year': None,
                'month': None,
                'day': None,
                'hour': None,
                'minute': None,
                'second': None
            }
            for u in 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second':
                for line in f.readlines():
                    m = re.match(r'^\s*Start' + u, line)
                    if m:
                        data[u.lower()] = int(m.group(1))
            return datetime.datetime(**data)


    def getOcnRestartTime(self):
        pass

##################################################################################
def test():
    top_dir = '/nesi/nobackup/pletzera/workflow_restart_capability/runCase_NESI'
    rtf = RestartTimeFinder(top_dir)
    atm_restart = rtf.getAtmRestartTime()
    print(f'atm restart: {atm_restart}')

if __name__ == '__main__':
    test()
