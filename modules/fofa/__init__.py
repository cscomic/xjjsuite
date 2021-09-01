import time

import pyfofa
from datetime import datetime

from lib.utils.__init__ import addHttp
from lib.utils.mytime import timestamp2fofatime, timestamp2timedelta


class fofasearch:
    def __init__(self, searchparse):
        self.basesearchparse = searchparse
        self.searchparse = self.basesearchparse

    def getAllHosts(self):
        email = ''
        key = ''
        search = pyfofa.FofaAPI(email, key)
        data = search.get_data(self.searchparse, 10000, 'host')#查询的语法，数量，返回内容
        if not data['error']:
            data = data['results']
        else:
            print('[fofa] ' + str(data))
            raise
        print(self.searchparse)
        if data:
            for i, host in enumerate(data):
                data[i] = addHttp(host)
            data = list(set(data))  # 去重
        return data

    def getRecentHosts(self, timestamp: float):
        '''
        run in morning, so after yestoday before today
        :return:
        '''
        timedelta = timestamp2timedelta(time.time(), timestamp)
        print(str(timedelta.days) if timedelta.days > 1 else '1' + '天没更新了')

        lastrun = timestamp2fofatime(timestamp)
        self.searchparse = self.basesearchparse + ' && after="' + str(lastrun) + '"'
        return self.getAllHosts()
