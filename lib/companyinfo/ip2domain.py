#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/16 20:02
# @name: ip反查域名
# @author：h2o0o4

'''
需要注意的问题：
有时候没有一个IP能反查出域名，可能是因为你的IP被网站ban了，而不是查不出来，试着挂个代理
这个接口有时候会因为你的频繁访问而拒绝服务，但是有时候是可以跑出结果的。
'''
import json
import re

import requests
import random

from lib.utils import fileRandomLine
from lib.request.webpage import getPage


def searchDomain(ip: str):
    domain = []
    try:
        func = ['aizhan', 'ip138']
        while not domain and len(func) != 0:
            rand = random.randint(0, len(func) - 1)
            domain.extend(eval(func[rand])(ip))
            func.pop(rand)

        #if not domain:
        #    domain.extend(aizhanvip(ip))
    except:
        print('searchDomain Func Error')
    finally:
        return domain


def aizhanvip(ip: str):
    key = '' #自己花钱
    url = 'https://apistore.aizhan.com/site/dnsinfos/{key}?query={ip}&page=1'.format(key=key, ip=ip)
    domain = []
    try:
        response = requests.get(url)
        j = json.loads(response.text)
        if j['code'] == '100005':
            print('余额不足')
            raise
        for d in j['data']['domains']:
            domain.append(d['domain'])
    except:
        print('aizhanvip error')
    finally:
        return domain


def aizhan(ip: str):
    list = []  # 用于存放可以通过IP反查到域名的域名
    ip = re.findall('\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', ip)[0]
    url = "https://dns.aizhan.com/" + ip + "/"
    try:
        bf = getPage(url)
        for t in bf.find_all('td'):
            a = t.find_all('a')
            if a:
                for j in range(len(a)):
                    url = a[j].attrs['href']
                    list.append(url)
    except:
        print('aizhan for Domain No Access')
    return list


def ip138(ip):
    headers_ip138 = {
        'Host': 'site.ip138.com',
        'User-Agent': fileRandomLine('data/user-agents.txt'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://site.ip138.com/'}

    ip138_url = 'https://site.ip138.com/' + str(ip) + '/'
    result_site = []
    try:
        ip138_r = requests.get(url=ip138_url, headers=headers_ip138, timeout=3).text
        # ip138_address = re.findall(r"<h3>(.*?)</h3>", ip138_r)   # 归属地
        # result = re.findall(r"<li>(.*?)</li>", ip138_r)
        if '<li>暂无结果</li>' in ip138_r:
            # print('[+]ip:{}'.format(ip))
            # print('归属地：{}'.format(ip138_address[0]))
            # print('未查到相关绑定信息！')
            return []
        else:
            # print('[+]ip:{}'.format(ip))
            # print('归属地：{}'.format(ip138_address[0]))
            # result_time = re.findall(r"""class="date">(.*?)</span>""", ip138_r)  # 绑定时间
            result_site = re.findall(r"""</span><a href="/(.*?)/" target="_blank">""", ip138_r)  # 绑定域名结果
            # print('绑定信息如下：')
            # for i, j in enumerate(result_time):
            #     print('{}-----{}'.format(j, result_site[i]))
    except:
        pass
        # 垃圾玩应，没爱站一半顶用
        # print('ip138 for Domain No Access')

    return result_site


if __name__ == '__main__':
    print(aizhanvip('39.106.248.112'))
