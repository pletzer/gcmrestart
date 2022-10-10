import f90nml
from pathlib import Path
import datetime
import glob
import os.path
import re

class RestartTimeFinder(obj):

    def __init__(self, top_dir : Path='./'):
        self.top_dir = top_dir



    getAtmRestartTime(self):
        atm_restart_files = glob.glob(self.top_dir / Path('wrfrst_d01_*'))
        atm_restart_files.sort()
        fname = os.path.basename(atm_restart_files[-1])
        _, _, year, month, day, hour, minute, second = fname.split('_')
        dt = datetime.datetime(year=int(year), month=int(month), day=int(day),
            hour=int(hour), minute=int(minute), second=int(second))
        return dt


    getStartTime(self):

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


    getOcnRestartTime(self):
        pass



