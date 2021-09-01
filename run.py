from datetime import datetime
import datetime
import importlib
import os
import time

from lib.utils.mytime import timestamp2timedelta


class Run:
    def __init__(self):
        today = datetime.date.today()
        self.TODAYREPORTDIR = 'reports/' + str(today)
        if not os.path.exists(self.TODAYREPORTDIR):
            os.mkdir(self.TODAYREPORTDIR)
        self.VULNS = os.listdir('vulns/')
        self.deal()

    def deal(self):
        # try:
        for vuln in self.VULNS:
            if vuln == '__init__.py': continue
            VULNPATH = 'vulns/' + vuln
            if os.path.exists(VULNPATH + '/lastrun.txt'):
                f = open(VULNPATH + '/lastrun.txt', 'r')
                timestamp = f.readline().strip()
                if timestamp:
                    timestamp = float(timestamp)
                    date = time.localtime(timestamp)
                    today = time.localtime(time.time())
                    if date.tm_year == today.tm_year and date.tm_mon == today.tm_mon and date.tm_mday == today.tm_mday:
                        f.close()
                        print(vuln + '今天已更新')
                        continue
            # 开始测试今天更新的主机

            Auto = importlib.import_module('vulns.' + vuln).Auto
            auto = Auto(VULNPATH, vuln, self.TODAYREPORTDIR)
            auto.run(6)
            with open(VULNPATH + '/lastrun.txt', 'w') as f:
                f.write(str(time.time()))
        # except:
        #     print('run.deal error')


if __name__ == '__main__':
    Run()
