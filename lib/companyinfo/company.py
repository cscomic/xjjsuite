# -*- coding: UTF-8 -*-
import random
from urllib import parse
from lib.request.webpage import getDynamicPage


def getCompany(url):
    info = {}
    try:
        # 爱企查目前有business所以先不用随机
        # func = ['aiqicha', 'tianyancha']
        # while not info and len(func) != 0:
        #     rand = random.randint(0, len(func) - 1)
        #     info = eval(func[rand])(url)
        #     func.pop(rand)
        info = aiqicha(url)
        if not info:
            info = tianyancha(url)
    except:
        pass
    finally:
        return info



def tianyancha(url: str):
    try:
        url = 'https://www.tianyancha.com/search?key={}'.format(url)
        bf = getDynamicPage(url)
        if bf.findAll(class_='tips-num'):
            info_total = str(bf.findAll(class_='tips-num')[0].string).strip()
            if info_total == '1':
                name = str(bf.findAll(class_='header')[0].findAll('a')[0].string).strip()
                addr = str(bf.findAll(class_='contact row')[1].findAll(class_='col')[0].findAll('span')[1].string).strip()
                # 暂时有点麻烦就先不弄了，毕竟能查到公司为准
                # href = bf.findAll(class_='header')[0].findAll('a')[0]['href']
                # wb = webpage(href)
                # bf = wb.postPage(data={'name': name})
                # business = str(bf.findAll(class_='select-none')[0].string).strip()
                return {'name': name, 'addr': addr, 'business': ''}
    except:
        print('tianyancha No Access')
    return {}


def aiqicha(url: str):
    url = 'https://aiqicha.baidu.com/s?q={url}&t=0'.format(url=parse.quote(url))
    try:
        bf = getDynamicPage(url)
        info_total = bf.findAll(class_='total')
        total = str(info_total[0].string).strip()
        if total == '1':

            info_addr_bus = bf.findAll(class_='legal-txt')
            addr = str(info_addr_bus[3].string).strip()
            business = str(info_addr_bus[4].string).strip()

            info_name = bf.findAll(class_='title')
            name = str(info_name[0].findAll('a')[0].string).strip()
            return {'name': name, 'addr': addr, 'business': business}
    except:
        print('aiqicha for companyinfo No Access')
    return {}
