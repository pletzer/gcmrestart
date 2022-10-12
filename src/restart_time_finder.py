import f90nml
from pathlib import Path
import datetime
import glob
import os.path
import re

class RestartTimeFinder(object):

    def __init__(self, top_dir : Path='./'):
        self.top_dir = top_dir

    def getAtmRestartTimes(self):
        atm_restart_files = glob.glob(str(self.top_dir) + '/wrfrst_d01_*')
        atm_restart_files.sort()
        res = []
        for f in atm_restart_files:
            fname = os.path.basename(f)
            _a, _b, year_month_day, hour, minute, second = fname.split('_')
            year, month, day = year_month_day.split('-')
            dt = datetime.datetime(year=int(year), month=int(month), day=int(day),
                hour=int(hour), minute=int(minute), second=int(second))
            res.append(dt)
        return res

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


    def getOcnReferenceTime(self):
        nml = f90nml.read(self.top_dir + '/data.cal')

        std1 = str(nml['CAL_NML']['startDate_1'])
        m = re.match(r'^(\d{4})(\d{2})(\d{2})', std1)
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))

        std2 = f"{nml['CAL_NML']['startDate_2']:06d}"
        hour, minute, second = int(std2[0:2]), int(std2[2:4]), int(std2[4:6])

        return datetime.datetime(year=year, month=month, day=day,
            hour=hour, minute=minute, second=second)


    def getOcnRestartTimes(self):
        ocn_restart_minutes = [int(os.path.basename(f).split('.')[1]) for f in glob.glob(str(self.top_dir) + '/pickup.[0-9]*.meta')]
        ocn_restart_minutes.sort()
        st = self.getOcnReferenceTime()
        return [st + datetime.timedelta(minutes=m) for m in ocn_restart_minutes]

    def getLatestRestartTime(self):
        ats = set(self.getAtmRestartTimes())
        ots = set(self.getOcnRestartTimes())
        res = list(ats.intersection(ots))
        res.sort()
        return res



##################################################################################
def test():
    top_dir = '/nesi/nobackup/pletzera/workflow_restart_capability/runCase_NESI'
    rtf = RestartTimeFinder(top_dir)
    print(f'start_time: {rtf.getStartTime()}')
    print(f'atm restart: {rtf.getAtmRestartTimes()}')
    print(f'ocn restart: {rtf.getOcnRestartTimes()}')
    print(f'latest restart time: {rtf.getLatestRestartTime()}')


if __name__ == '__main__':
    test()
