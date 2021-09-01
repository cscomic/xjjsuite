import requests


def getProxy():
    req = requests.get('http://127.0.0.1:8082/get')
    print(req.text)
    # return proxy
if __name__ == '__main__':
    getProxy()
