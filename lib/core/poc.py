import datetime
import importlib
import os
import re
import time
from multiprocessing import Pool

from lib.companyinfo.company import getCompany
from lib.companyinfo.ip2domain import searchDomain
from lib.template.report.vulcloud360 import writeReport
from lib.utils import getIP, getDomainList
from modules.fofa import fofasearch


class Base(object):
    def __init__(self, vulndir, vulnname, todayreportdir, ReportInfo):
        print('----------init-------------')
        print(vulnname + ' ', end='')
        self._verify = importlib.import_module('vulns.' + vulnname)._verify
        self.vulnname = vulnname
        self.result = {}
        self.result['HostsInfo'] = {
            'ALLVULNHOSTS': [],  # 所有有漏洞的主机
            'ALLHOSTS': [],  # 所有的主机
            'TODAYVULNHOSTS': [],  # 今天有漏洞的主机
            'TODAYALLHOSTS': []
        }
        self.result['DirInfo'] = {
            'TODAYREPORTDIR': todayreportdir,
            'VULNDIR': vulndir
        }
        self.result['ReportInfo'] = {
            'FOFASEARCH': ReportInfo['FOFASEARCH'],
            'TITLE': ReportInfo['TITLE'],
            'POC': ReportInfo['POC'],
            'SUBSCRIPT': ReportInfo['SUBSCRIPT'],
            'COMPONENT': ReportInfo['COMPONENT'],
            'REPAIR': ReportInfo['REPAIR']
        }
        self.VULNHOSTSFILE = self.result['DirInfo']['VULNDIR'] + '/vuln_hosts.txt'
        self.ALLHOSTSFILE = self.result['DirInfo']['VULNDIR'] + '/all_hosts.txt'
        self.TODAYINFOFILE = todayreportdir + '/info.txt'

        self._initTime()
        self._updateAllHosts()
        self._initVulnHosts()

    def _initTime(self):
        try:
            if os.path.exists(self.result['DirInfo']['VULNDIR'] + '/lastrun.txt'):
                with open(self.result['DirInfo']['VULNDIR'] + '/lastrun.txt') as f:
                    lastrun = f.readline().strip()
                    if lastrun:
                        self.LASTRUN = float(lastrun)
                    else:
                        yesterday = datetime.date.today() - datetime.timedelta(days=1)
                        self.LASTRUN = float(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
            else:
                open(self.result['DirInfo']['VULNDIR'] + '/lastrun.txt', 'w').close()
        except:
            print('_initTime error')

    def _initVulnHosts(self):
        try:
            vulnhosts = []
            with open(self.VULNHOSTSFILE, 'r', encoding='utf-8') as vf:
                for host in vf.readlines():
                    h = host.strip('\n')
                    vulnhosts.append(h.split(' ')[0])
                vf.close()
            self.result['HostsInfo']['ALLVULNHOSTS'] = vulnhosts
        except:
            print('_initVulnHosts error')

    def _updateAllHosts(self):
        fofa = fofasearch(self.result['ReportInfo']['FOFASEARCH'])
        allhosts = []
        with open(self.ALLHOSTSFILE, 'r') as af:
            # 读取allhosts内容
            for host in af.readlines():
                allhosts.append(host.strip('\n'))
            af.close()

        self.result['HostsInfo']['ALLHOSTS'] = allhosts

        if not self.result['HostsInfo']['ALLHOSTS']:
            # allhosts没有，搜索全部的
            allhosts = fofa.getAllHosts()
            # 写allhosts
            with open(self.ALLHOSTSFILE, 'w') as af:
                for host in allhosts:
                    af.write(host + '\n')
                af.close()
            self.result['HostsInfo']['ALLHOSTS'] = allhosts
            self.result['HostsInfo']['TODAYALLHOSTS'] = allhosts
        else:
            # 更新今天的
            todayhosts = fofa.getRecentHosts(self.LASTRUN)
            with open(self.ALLHOSTSFILE, 'a') as af:
                for host in todayhosts:
                    if host not in allhosts:
                        af.write(host + '\n')
                af.close()
            self.result['HostsInfo']['TODAYALLHOSTS'] = todayhosts
        print('todayhosts:{}'.format(len(self.result['HostsInfo']['TODAYALLHOSTS'])))

    def __del__(self):
        print(self.vulnname + ' over')

    # 对每个host处理的步骤，先判断是否有漏洞，然后是否有域名，再写文件，生成报告
    def run(self, poolnum=5):
        print('--------------running-----------')
        allvulnhosts = self.result['HostsInfo']['ALLVULNHOSTS']
        with Pool(poolnum) as pool:
            for host in self.result['HostsInfo']['TODAYALLHOSTS']:
                if host not in allvulnhosts:  # 优化，如果主机已经有过问题就不会再使用poc攻击主机了
                    pool.apply_async(self._verify, args=(host,), callback=self._deal)
            pool.close()
            pool.join()

    def _writeReport(self, info, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

        host = info['host']
        ip = getIP(host)
        LEVEL = info['LEVEL']
        domainurls = info['domainurls']
        report = dir + '/' + self.vulnname + '_' + ip + '.txt'

        if not os.path.exists(report):
            writeReport(reportname=report, title=self.result['ReportInfo']['TITLE'], ip=ip,
                        poc=self.result['ReportInfo']['POC'].replace('{host}', host),
                        subscript=self.result['ReportInfo']['SUBSCRIPT'], level=LEVEL, url=' '.join(domainurls),
                        component=self.result['ReportInfo']['COMPONENT'],
                        companyname=info['company']['name'], companyaddr=info['company']['addr'],
                        business=info['company']['business'],
                        repair=self.result['ReportInfo']['REPAIR'])

    def _writeFile(self, info, allhosts):
        # 记录主机ip和域名
        try:
            host = info['host']
            domainurls = info['domainurls']
            company = info['company']
            # self.vf就不让写离谱
            vf = open(self.VULNHOSTSFILE, 'a', encoding='utf-8')
            if host not in allhosts:
                if domainurls:
                    if company:
                        vf.write('{host} {domain} {companyname}\n'.format(host=host, domain=' '.join(domainurls),
                                                                          companyname=company['name']))
                    else:
                        vf.write('{host} {domain}\n'.format(host=host, domain=' '.join(domainurls)))
                else:
                    vf.write('{host}\n'.format(host=host))
            vf.close()
        except:
            print('_writeFile error')

    def _deal(self, info):
        vulnable = info['vulnable']
        try:
            if vulnable:
                host = info['host']
                info['domainurls'] = []
                info['company'] = {}
                domainList = getDomainList(searchDomain(getIP(host)))
                allvulnhosts = self.result['HostsInfo']['ALLVULNHOSTS']
                # 有域名
                if domainList:
                    # 把带ip的host替换成带域名的host
                    for domain in domainList:
                        info['domainurls'].append(re.sub('\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', domain, host))
                    self.result['HostsInfo']['TODAYVULNHOSTS'].append(info)
                    dir1 = self.result['DirInfo']['VULNDIR'] + '/reports'
                    dir2 = self.result['DirInfo']['TODAYREPORTDIR']

                    # 查公司信息
                    for domain in domainList:
                        info['company'] = getCompany(domain)
                        if info['company']:
                            break
                    # 查到公司信息之后
                    if info['company']:
                        print('[+] 目标 {target_url} 存在漏洞， domain: {domain}，company:{company}'.format(target_url=host, domain= info['domainurls'][ 0], company= info['company'][ 'name']))
                        # 追加文件，生成报告
                        self._writeReport(info, dir1)
                        self._writeReport(info, dir2)

                self._writeFile(info, allvulnhosts)
        except:
            print('_deal error')
