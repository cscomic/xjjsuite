# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver
from lib.utils import fileRandomLine


def getDynamicPage(url: str) -> BeautifulSoup:
    # chromedriver的绝对路径
    driver_path = r'D:\source\drivers\chromedriver_win32\chromedriver.exe'
    # 设置不要弹出浏览器
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 初始化一个driver，并且指定chromedriver的路径
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
    # 请求网页
    driver.get(url)
    # 通过page_source获取网页源代码
    bf = BeautifulSoup(driver.page_source, 'html.parser')
    return bf

def getPage(url):
    headers = {
        "User-Agent": fileRandomLine('data/user-agents.txt')
    }
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url=url, headers=headers, verify=False, timeout=5)
    bf = BeautifulSoup(response.text, 'html.parser')
    return bf

class webpage:
    def __init__(self, url):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'#fileRandomLine('data/user-agents.txt')
        }
        # proxys={
        #     'http': getProxy(),
        #     'https': getProxy()
        # }
        self.url = url
        self.session = requests.session()
        self.session.headers = headers
        self.headers = headers


    def getPage(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        print(self.headers)
        response = requests.get(url=self.url, headers=self.headers, verify=False, timeout=5)
        bf = BeautifulSoup(response.text, 'html.parser')
        return bf

    def postPage(self, data):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=self.url, data=data, headers=self.headers, verify=False, timeout=5)
        bf = BeautifulSoup(response.text, 'html.parser')
        return bf
