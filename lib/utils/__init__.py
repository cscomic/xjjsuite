import datetime
import linecache
import random
import re
import socket
import time
from urllib.parse import urlparse


# 正则返回ip
def getIP(host: str):
    ip = re.findall('\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', host)
    if ip:
        return ip[0]
    else:
        ip = socket.gethostbyname(host)
        if ip:
            return ip
        else:
            return ''


def getDomain(host: str):
    return urlparse(host).netloc


def addHttp(host: str):
    # if re.match('^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', host) is not None:
    if host[:7] != 'http://' and host[:8] != 'https://':
        return 'http://' + host
    return host


def getDomainList(host: list):
    for i, item in enumerate(host):
        host[i] = getDomain(addHttp(item))
    return host


# 批量获取主机
def getHosts():
    hosts = []
    with open('all_hosts.txt', 'r') as f:
        for host in f.readlines():
            host = host.strip('\n')
            host = addHttp(host)
            if host[-1] == '/':
                host = host[:-1]
            hosts.append(host)
    return hosts


def fileLineNum(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)


def fileRandomLine(filename):
    return linecache.getline(filename, random.randrange(1, fileLineNum(filename))).strip('\n')


def file2str(file):
    file = ''
    with open(file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            file += line
    return file


def delTime(stamp1, stamp2):
    datetime.time(stamp1)
    t1 = time.localtime(stamp1)
    t2 = time.localtime(stamp2)
    t1 = time.strftime("%Y-%m-%d %H:%M:%S", t1)
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t2)
    time1 = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    datetime.timedelta()
    return (time2 - time1).seconds
