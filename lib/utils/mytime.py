import time
from datetime import datetime


def timestamp2fofatime(timestamp: float):
    return time.strftime("%Y-%m-%d", time.localtime(timestamp))


def timestamp2timedelta(timestampbigger: float, timestamplower: float):
    return datetime.fromtimestamp(timestampbigger) - datetime.fromtimestamp(timestamplower)
