# -*- coding: UTF-8 -*-
import os

def writeReport(reportname:str, title: str, ip: str, poc: str, subscript: str, level: str, url: str, repair: str, companyname: str, companyaddr: str, business: str, component=''):
    with open(reportname, 'w', encoding='utf-8') as report_f:
        report_f.writelines('''厂商名称：{companyname}
所属SRC：互联网空间-亿万守护计划
漏洞标题：{title}
漏洞类别：web
漏洞类型: 事件型
利用通用漏洞：是
组件名称：{component}
漏洞等级：{level}
漏洞url：{url}
网站名称：{companyname}
网站ip：{ip}
所属地区：{companyaddr}
漏洞描述：{subscript}
公司业务：{business}
复现步骤：{poc}
修复方案：{repair}'''.format(title=title, level=level, url=url, ip=ip, poc=poc, component=component, repair=repair,
                            subscript=subscript, companyname=companyname, companyaddr=companyaddr, business=business))
        report_f.close()
