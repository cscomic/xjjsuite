"""
Copyright (c) 2006-2021 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""


class xjjBaseException(IOError):
    pass


class FOFASizeException(xjjBaseException):
    pass

class NoSuchKeyException(xjjBaseException):
    pass
