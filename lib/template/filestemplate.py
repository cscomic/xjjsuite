# -*- coding: UTF-8 -*-
import os


def writeFiles():
    open("all_hosts.txt", 'w').close()
    open("vuln_hosts.txt", 'w').close()

    with open('__init__.py', 'w') as f:
        f.write('''# -*- coding: UTF-8 -*-
import requests
from lib.core.poc import Base
import urllib3
report_num = 0


class Auto(Base):
    def __init__(self, vulndir, vulnname, todayreportdir):
        ReportInfo = {}
        ReportInfo['FOFASEARCH'] = \'\'\'\'\'\'
        ReportInfo['TITLE'] = \'\'\'\'\'\'
        ReportInfo['SUBSCRIPT'] = \'\'\'\'\'\'
        ReportInfo['COMPONENT'] = \'\'\'\'\'\'
        ReportInfo['REPAIR'] = \'\'\'\'\'\'
        # write the POC into the report 
        ReportInfo['POC'] = \'\'\'
# -*- coding: UTF-8 -*-
import requests

host = '{host}'
if host[-1] == '/':
    host = host[:-1]

def poc(target_url):
    check_url = target_url + ''
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }
    try:
        response = requests.post(url=check_url, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and '' in response.text:
            print("[+]  {} is vulnable, and the result is:{}".format(target_url, response.text))
    except:
        print('error {0}'.format(target_url))

poc(host)
        \'\'\'
        super().__init__(vulndir=vulndir, todayreportdir=todayreportdir, ReportInfo=ReportInfo, vulnname=vulnname)


def _verify(target_url):
    info = {}
    info['host'] = target_url
    info['vulnable'] = 0
    check_url = target_url + ''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(url=check_url, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and '' in response.text:
            # set info['LEVEL']:str and info['vulnable']:int as the return
            info['LEVEL'] = ''
            info['vulnable'] = 1
    except:
        pass
    finally:
        return info''')

writeFiles()
